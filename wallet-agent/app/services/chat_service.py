from __future__ import annotations

import json
import re
from typing import Any, Dict, Iterable, List

from langchain_core.messages import HumanMessage, SystemMessage

from app.agents.context_builder import build_context_block
from app.agents.prompts import (
    ARGUMENT_ENRICHMENT_PROMPT,
    CLARIFICATION_PROMPT,
    FINAL_ANSWER_PROMPT,
    MISSING_FIELDS_PROMPT,
    PENDING_ARGUMENT_EXTRACTION_PROMPT,
    TOOL_SELECTION_PROMPT,
)
from app.core.logging import get_logger
from app.mcp.client import get_mcp_client
from app.mcp.tool_filter import (
    build_tool_catalog,
    compact_tool_catalog_for_prompt,
    extract_tool_call_text,
    extract_tools,
)
from app.memory.summarizer import summarize_recent_messages
from app.models.llm_factory import LLMFactory
from app.services.state_service import StateService

logger = get_logger(__name__)


class ChatService:
    def __init__(self) -> None:
        self.state_service = StateService()
        self.llm_factory = LLMFactory()

    def _extract_message_content(self, llm_response: Any) -> str:
        content = getattr(llm_response, "content", None)

        if isinstance(content, str):
            return content

        if isinstance(content, list):
            parts: List[str] = []
            for item in content:
                if isinstance(item, dict):
                    if item.get("type") == "text":
                        parts.append(item.get("text", ""))
                    elif "text" in item:
                        parts.append(str(item["text"]))
                else:
                    text = getattr(item, "text", None)
                    if text:
                        parts.append(str(text))
            return "\n".join(parts)

        return str(llm_response)

    def _extract_json_object(self, text: str) -> Dict[str, Any]:
        text = text.strip()

        try:
            return json.loads(text)
        except Exception:
            pass

        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group(0))

        raise ValueError(f"LLM did not return valid JSON: {text}")

    def _update_recent_messages(self, state, user_query: str, assistant_text: str) -> None:
        state.recent_messages.append({"role": "user", "content": user_query})
        state.recent_messages.append({"role": "assistant", "content": assistant_text})
        state.recent_messages = state.recent_messages[-20:]
        state.conversation_summary = summarize_recent_messages(state.recent_messages)

    def _walk_values(self, value: Any) -> Iterable[Any]:
        if isinstance(value, dict):
            for key, sub_value in value.items():
                yield key, sub_value
                yield from self._walk_values(sub_value)
        elif isinstance(value, list):
            for item in value:
                yield from self._walk_values(item)

    def _normalize_key(self, key: str) -> str:
        return str(key).replace("_", "").replace("-", "").lower()

    def _memory_field_map(self) -> Dict[str, str]:
        return {
            "programmanagerid": "programManagerId",
            "programmngrid": "programManagerId",
            "walletid": "walletId",
            "personid": "personId",
            "mobilenumber": "mobileNumber",
            "mobileno": "mobileNumber",
            "cifnumber": "cifNumber",
            "transactionid": "transactionId",
            "tagid": "tagId",
            "transfertypeid": "transferTypeId",
            "groupid": "groupId",
            "customfieldid": "customFieldId",
            "customfieldvalue": "customFieldValue",
            "clientrequestid": "clientRequestId",
            "systemaccountid": "systemAccountId",
            "lasttoolname": "last_tool_name",
        }

    def _maybe_set_from_key(self, state, key: str, value: Any) -> None:
        if value in (None, "", {}):
            return

        attr = self._memory_field_map().get(self._normalize_key(key))
        if attr and hasattr(state, attr):
            setattr(state, attr, str(value))

    def _update_state_from_args(self, state, args: Dict[str, Any]) -> None:
        for key, value in (args or {}).items():
            self._maybe_set_from_key(state, key, value)

    def _update_state_from_tool_result(self, state, result: Any) -> None:
        for key, value in self._walk_values(result):
            self._maybe_set_from_key(state, key, value)

        state.last_tool_result_summary = {
            "programManagerId": getattr(state, "programManagerId", None),
            "walletId": getattr(state, "walletId", None),
            "personId": getattr(state, "personId", None),
            "mobileNumber": getattr(state, "mobileNumber", None),
            "transactionId": getattr(state, "transactionId", None),
            "tagId": getattr(state, "tagId", None),
            "groupId": getattr(state, "groupId", None),
            "transferTypeId": getattr(state, "transferTypeId", None),
            "customFieldId": getattr(state, "customFieldId", None),
            "customFieldValue": getattr(state, "customFieldValue", None),
            "clientRequestId": getattr(state, "clientRequestId", None),
            "systemAccountId": getattr(state, "systemAccountId", None),
        }

    def _merge_args_with_state(
        self,
        state,
        args: Dict[str, Any],
        tool_info: Dict[str, Any],
    ) -> Dict[str, Any]:
        merged = dict(args or {})
        schema = tool_info.get("inputSchema", {}) or {}
        properties = schema.get("properties", {}) or {}

        for field_name in properties.keys():
            if field_name in merged and merged[field_name] not in (None, ""):
                continue

            attr = self._memory_field_map().get(self._normalize_key(field_name))
            if not attr:
                continue

            value = getattr(state, attr, None)
            if value:
                merged[field_name] = value

        return merged

    def _coerce_args_by_schema(
        self,
        args: Dict[str, Any],
        tool_info: Dict[str, Any],
    ) -> Dict[str, Any]:
        coerced = dict(args or {})
        schema = tool_info.get("inputSchema", {}) or {}
        properties = schema.get("properties", {}) or {}

        for field_name, meta in properties.items():
            if field_name not in coerced:
                continue

            value = coerced[field_name]
            field_type = str(meta.get("type", "")).lower() if isinstance(meta, dict) else ""

            if value in (None, ""):
                continue

            if field_type in {"number", "integer", "int"}:
                if isinstance(value, (int, float)):
                    continue

                if isinstance(value, str):
                    cleaned = value.strip()

                    if cleaned.lower() in {
                        "limit",
                        "pagenumber",
                        "pagesize",
                        "number",
                        "integer",
                    }:
                        coerced.pop(field_name, None)
                        continue

                    try:
                        coerced[field_name] = int(cleaned)
                    except ValueError:
                        try:
                            coerced[field_name] = float(cleaned)
                        except ValueError:
                            coerced.pop(field_name, None)

        return coerced

    def _missing_fields(self, required_fields: List[str], args: Dict[str, Any]) -> List[str]:
        return [
            field
            for field in required_fields
            if field not in args or args[field] in (None, "")
        ]

    async def _select_tool(
        self,
        llm,
        user_query: str,
        catalog: Dict[str, Dict[str, Any]],
        state,
    ) -> Dict[str, Any]:
        catalog_text = compact_tool_catalog_for_prompt(catalog)
        context_block = build_context_block(state)

        response = await llm.ainvoke(
            [
                SystemMessage(content=TOOL_SELECTION_PROMPT),
                HumanMessage(
                    content=(
                        f"Structured session context:\n{context_block}\n\n"
                        f"Available tool catalog:\n{catalog_text}\n\n"
                        f"User request:\n{user_query}\n\n"
                        f"Return JSON only."
                    )
                ),
            ]
        )

        text = self._extract_message_content(response)
        return self._extract_json_object(text)

    async def _enrich_args_from_context(
        self,
        llm,
        user_query: str,
        state,
        tool_info: Dict[str, Any],
        current_args: Dict[str, Any],
    ) -> Dict[str, Any]:
        context_block = build_context_block(state)

        response = await llm.ainvoke(
            [
                SystemMessage(content=ARGUMENT_ENRICHMENT_PROMPT),
                HumanMessage(
                    content=(
                        f"Latest user message:\n{user_query}\n\n"
                        f"Recent conversation history:\n{state.recent_messages}\n\n"
                        f"Structured session context:\n{context_block}\n\n"
                        f"Already known arguments:\n{current_args}\n\n"
                        f"Selected tool name:\n{tool_info.get('llm_name')}\n\n"
                        f"Selected tool description:\n{tool_info.get('description')}\n\n"
                        f"Selected tool input schema:\n{tool_info.get('inputSchema')}\n\n"
                        f"Return JSON only."
                    )
                ),
            ]
        )

        text = self._extract_message_content(response)
        parsed = self._extract_json_object(text)
        enriched = parsed.get("arguments", {})

        merged = dict(current_args or {})
        for key, value in (enriched or {}).items():
            if value not in (None, "", {}):
                merged[key] = value

        return merged

    async def _ask_for_missing_fields(
        self,
        llm,
        user_query: str,
        tool_info: Dict[str, Any],
        missing_fields: List[str],
        known_args: Dict[str, Any],
    ) -> str:
        response = await llm.ainvoke(
            [
                SystemMessage(content=MISSING_FIELDS_PROMPT),
                HumanMessage(
                    content=(
                        f"User request:\n{user_query}\n\n"
                        f"Selected tool description:\n{tool_info.get('description')}\n\n"
                        f"Required fields still missing:\n{missing_fields}\n\n"
                        f"Arguments already known:\n{known_args}\n\n"
                        f"Ask the user for the missing information."
                    )
                ),
            ]
        )
        return self._extract_message_content(response)

    async def _clarify_no_tool(
        self,
        llm,
        user_query: str,
        catalog: Dict[str, Dict[str, Any]],
        state,
    ) -> str:
        catalog_text = compact_tool_catalog_for_prompt(catalog)
        context_block = build_context_block(state)

        response = await llm.ainvoke(
            [
                SystemMessage(content=CLARIFICATION_PROMPT),
                HumanMessage(
                    content=(
                        f"Structured session context:\n{context_block}\n\n"
                        f"User request:\n{user_query}\n\n"
                        f"Available tool catalog:\n{catalog_text}\n\n"
                        f"Ask one clarification question."
                    )
                ),
            ]
        )
        return self._extract_message_content(response)

    async def _extract_pending_args(
        self,
        llm,
        user_query: str,
        missing_fields: List[str],
        state,
    ) -> Dict[str, Any]:
        context_block = build_context_block(state)

        response = await llm.ainvoke(
            [
                SystemMessage(content=PENDING_ARGUMENT_EXTRACTION_PROMPT),
                HumanMessage(
                    content=(
                        f"Structured session context:\n{context_block}\n\n"
                        f"Missing fields:\n{missing_fields}\n\n"
                        f"User message:\n{user_query}\n\n"
                        f"Return JSON only."
                    )
                ),
            ]
        )

        text = self._extract_message_content(response)
        return self._extract_json_object(text)

    async def _answer_from_tool_result(
        self,
        llm,
        user_query: str,
        tool_name: str,
        tool_result_text: str,
    ) -> str:
        response = await llm.ainvoke(
            [
                SystemMessage(content=FINAL_ANSWER_PROMPT),
                HumanMessage(
                    content=(
                        f"User request:\n{user_query}\n\n"
                        f"Tool used:\n{tool_name}\n\n"
                        f"Tool result:\n{tool_result_text}"
                    )
                ),
            ]
        )
        return self._extract_message_content(response)

    async def _explain_tool_error(
        self,
        llm,
        user_query: str,
        tool_name: str,
        args: Dict[str, Any],
        tool_error_response: Dict[str, Any],
    ) -> str:
        response = await llm.ainvoke(
            [
                SystemMessage(
                    content="""
You are a wallet operations assistant.

A backend MCP tool failed.

Explain the actual error to the client in simple business language.

Rules:
- Do not say only "tool execution failed".
- Explain what likely went wrong based on the real error.
- If required data appears missing, tell the client exactly what is missing.
- If an ID/value seems invalid, ask the client to verify that value.
- Do not invent causes not supported by the error.
- Keep it short and useful.
"""
                ),
                HumanMessage(
                    content=(
                        f"User request:\n{user_query}\n\n"
                        f"Tool name:\n{tool_name}\n\n"
                        f"Tool arguments sent:\n{args}\n\n"
                        f"Raw tool/MCP error:\n{tool_error_response}\n\n"
                        f"Explain this error to the client."
                    )
                ),
            ]
        )

        return self._extract_message_content(response)

    def _extract_exception_response(self, exc: Exception) -> Dict[str, Any]:
        error_text = str(exc)

        tool_error_response: Dict[str, Any] = {
            "success": False,
            "error": error_text,
            "exception_type": exc.__class__.__name__,
        }

        http_response = getattr(exc, "response", None)

        if http_response is not None:
            tool_error_response["status_code"] = getattr(http_response, "status_code", None)
            tool_error_response["reason_phrase"] = getattr(http_response, "reason_phrase", None)
            tool_error_response["url"] = str(getattr(http_response, "url", ""))

            try:
                tool_error_response["body"] = http_response.json()
            except Exception:
                tool_error_response["body"] = getattr(http_response, "text", None)

        return tool_error_response

    async def _execute_tool_and_answer(
        self,
        llm,
        client,
        state,
        user_query: str,
        tool_name: str,
        backend_tool_name: str,
        args: Dict[str, Any],
    ) -> Dict[str, Any]:
        self._update_state_from_args(state, args)
        state.last_tool_name = tool_name

        try:
            raw_result = await client.tool_call(backend_tool_name, args)
            self._update_state_from_tool_result(state, raw_result)

            tool_result_text = extract_tool_call_text(raw_result)

            response_text = await self._answer_from_tool_result(
                llm=llm,
                user_query=user_query,
                tool_name=tool_name,
                tool_result_text=tool_result_text,
            )

            return {
                "success": True,
                "error": None,
                "response_text": response_text,
                "tool_name": tool_name,
                "backend_tool_name": backend_tool_name,
                "tool_args": args,
                "tool_response": raw_result,
            }

        except Exception as exc:
            tool_error_response = self._extract_exception_response(exc)

            response_text = await self._explain_tool_error(
                llm=llm,
                user_query=user_query,
                tool_name=tool_name,
                args=args,
                tool_error_response=tool_error_response,
            )

            return {
                "success": False,
                "error": tool_error_response.get("error"),
                "response_text": response_text,
                "tool_name": tool_name,
                "backend_tool_name": backend_tool_name,
                "tool_args": args,
                "tool_response": tool_error_response,
            }

    async def chat(
        self,
        thread_id: str,
        user_query: str,
        provider: str | None = None,
    ) -> Dict[str, Any]:
        state = self.state_service.get_or_create(thread_id)

        llm = self.llm_factory.get_llm(provider)
        client = get_mcp_client()

        raw_tools_response = await client.tools_list()
        raw_tools = extract_tools(raw_tools_response)
        catalog = build_tool_catalog(raw_tools)

        if state.pending_tool_name and state.pending_backend_tool_name:
            tool_name = state.pending_tool_name
            backend_tool_name = state.pending_backend_tool_name
            tool_info = catalog.get(tool_name)

            if not tool_info:
                self.state_service.clear_pending_tool(state)
                response_text = await self._clarify_no_tool(
                    llm=llm,
                    user_query=user_query,
                    catalog=catalog,
                    state=state,
                )
                self._update_recent_messages(state, user_query, response_text)
                self.state_service.save(state)

                return {
                    "thread_id": thread_id,
                    "provider": provider,
                    "response_text": response_text,
                    "success": False,
                    "error": "Pending tool is no longer available",
                    "tool_name": tool_name,
                    "backend_tool_name": backend_tool_name,
                    "tool_args": state.pending_arguments or {},
                    "tool_response": None,
                    "state": state.model_dump(),
                }

            new_args = await self._extract_pending_args(
                llm=llm,
                user_query=user_query,
                missing_fields=state.pending_missing_fields,
                state=state,
            )

            args = dict(state.pending_arguments or {})
            args.update(new_args)
            args = self._merge_args_with_state(state, args, tool_info)

            args = await self._enrich_args_from_context(
                llm=llm,
                user_query=user_query,
                state=state,
                tool_info=tool_info,
                current_args=args,
            )

            args = self._coerce_args_by_schema(args, tool_info)

            self._update_state_from_args(state, args)
            self.state_service.save(state)

            missing = self._missing_fields(tool_info["required_fields"], args)

            if missing:
                self.state_service.set_pending_tool(
                    state=state,
                    tool_name=tool_name,
                    backend_tool_name=backend_tool_name,
                    arguments=args,
                    missing_fields=missing,
                )

                response_text = await self._ask_for_missing_fields(
                    llm=llm,
                    user_query=user_query,
                    tool_info=tool_info,
                    missing_fields=missing,
                    known_args=args,
                )

                self._update_recent_messages(state, user_query, response_text)
                self.state_service.save(state)

                return {
                    "thread_id": thread_id,
                    "provider": provider,
                    "response_text": response_text,
                    "success": False,
                    "error": "Missing required fields",
                    "tool_name": tool_name,
                    "backend_tool_name": backend_tool_name,
                    "tool_args": args,
                    "tool_response": None,
                    "state": state.model_dump(),
                }

            self.state_service.clear_pending_tool(state)

            execution = await self._execute_tool_and_answer(
                llm=llm,
                client=client,
                state=state,
                user_query=user_query,
                tool_name=tool_name,
                backend_tool_name=backend_tool_name,
                args=args,
            )

            self._update_recent_messages(state, user_query, execution["response_text"])
            self.state_service.save(state)

            return {
                "thread_id": thread_id,
                "provider": provider,
                **execution,
                "state": state.model_dump(),
            }

        selection = await self._select_tool(
            llm=llm,
            user_query=user_query,
            catalog=catalog,
            state=state,
        )

        tool_name = selection.get("tool_name")
        args = selection.get("arguments") or {}

        if not tool_name:
            reason = str(selection.get("reason", ""))

            if reason == "OUT_OF_SCOPE":
                response_text = (
                    "I can only help with wallet, customer, payment, program manager, "
                    "and MCP tool-related queries."
                )
                error = "Out of scope"
            else:
                response_text = await self._clarify_no_tool(
                    llm=llm,
                    user_query=user_query,
                    catalog=catalog,
                    state=state,
                )
                error = "No suitable tool selected"

            self._update_recent_messages(state, user_query, response_text)
            self.state_service.save(state)

            return {
                "thread_id": thread_id,
                "provider": provider,
                "response_text": response_text,
                "success": False,
                "error": error,
                "tool_name": None,
                "backend_tool_name": None,
                "tool_args": {},
                "tool_response": None,
                "state": state.model_dump(),
            }

        tool_info = catalog.get(tool_name)

        if not tool_info:
            response_text = await self._clarify_no_tool(
                llm=llm,
                user_query=user_query,
                catalog=catalog,
                state=state,
            )

            self._update_recent_messages(state, user_query, response_text)
            self.state_service.save(state)

            return {
                "thread_id": thread_id,
                "provider": provider,
                "response_text": response_text,
                "success": False,
                "error": f"Selected tool `{tool_name}` not found in catalog",
                "tool_name": tool_name,
                "backend_tool_name": None,
                "tool_args": args,
                "tool_response": None,
                "state": state.model_dump(),
            }

        args = self._merge_args_with_state(state, args, tool_info)

        args = await self._enrich_args_from_context(
            llm=llm,
            user_query=user_query,
            state=state,
            tool_info=tool_info,
            current_args=args,
        )

        args = self._coerce_args_by_schema(args, tool_info)

        self._update_state_from_args(state, args)
        self.state_service.save(state)

        missing = self._missing_fields(tool_info["required_fields"], args)

        if missing:
            self.state_service.set_pending_tool(
                state=state,
                tool_name=tool_name,
                backend_tool_name=tool_info["backend_name"],
                arguments=args,
                missing_fields=missing,
            )

            response_text = await self._ask_for_missing_fields(
                llm=llm,
                user_query=user_query,
                tool_info=tool_info,
                missing_fields=missing,
                known_args=args,
            )

            self._update_recent_messages(state, user_query, response_text)
            self.state_service.save(state)

            return {
                "thread_id": thread_id,
                "provider": provider,
                "response_text": response_text,
                "success": False,
                "error": "Missing required fields",
                "tool_name": tool_name,
                "backend_tool_name": tool_info["backend_name"],
                "tool_args": args,
                "tool_response": None,
                "state": state.model_dump(),
            }

        execution = await self._execute_tool_and_answer(
            llm=llm,
            client=client,
            state=state,
            user_query=user_query,
            tool_name=tool_name,
            backend_tool_name=tool_info["backend_name"],
            args=args,
        )

        self._update_recent_messages(state, user_query, execution["response_text"])
        self.state_service.save(state)

        logger.info("thread_id=%s provider=%s tool=%s", thread_id, provider, tool_name)

        return {
            "thread_id": thread_id,
            "provider": provider,
            **execution,
            "state": state.model_dump(),
        }