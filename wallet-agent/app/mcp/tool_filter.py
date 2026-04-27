# from __future__ import annotations

# import hashlib
# import re
# from typing import Any, Dict, List

# from langchain_core.tools import StructuredTool
# from pydantic import create_model

# from app.mcp.tool_aliases import TOOL_ALIASES, TOOL_DESCRIPTIONS


# def _slugify(value: str) -> str:
#     value = value.strip()
#     value = value.replace("/", "_").replace("-", "_").replace(".", "_")
#     value = re.sub(r"[^a-zA-Z0-9_]", "_", value)
#     value = re.sub(r"_+", "_", value)
#     return value.strip("_")


# def _llm_tool_name(backend_name: str) -> str:
#     """
#     Name exposed to the LLM.
#     Must be short, deterministic, and <= 64 chars for OpenAI tool calling.
#     """
#     alias = TOOL_ALIASES.get(backend_name)
#     if alias:
#         safe = _slugify(alias)
#         if len(safe) <= 64:
#             return safe

#     safe_backend = _slugify(backend_name)
#     if len(safe_backend) <= 55:
#         return safe_backend

#     digest = hashlib.md5(backend_name.encode("utf-8")).hexdigest()[:8]
#     return f"{safe_backend[:55]}_{digest}"[:64]


# def _normalize_description(tool: Dict[str, Any]) -> str:
#     backend_name = tool["name"]
#     llm_name = _llm_tool_name(backend_name)

#     description = TOOL_DESCRIPTIONS.get(llm_name)
#     if description:
#         return description

#     backend_description = tool.get("description")
#     if backend_description:
#         return backend_description

#     return llm_name


# def _json_type_to_python(field_meta: Dict[str, Any]):
#     json_type = field_meta.get("type", "string")

#     if json_type == "number":
#         return float
#     if json_type == "integer":
#         return int
#     if json_type == "boolean":
#         return bool
#     return str


# def _build_args_schema(tool: Dict[str, Any]):
#     properties = tool.get("inputSchema", {}).get("properties", {})
#     required_fields = set(tool.get("inputSchema", {}).get("required", []))

#     fields = {}

#     for field_name, field_meta in properties.items():
#         field_type = _json_type_to_python(field_meta)

#         if field_name in required_fields:
#             default = ...
#         else:
#             default = None

#         fields[field_name] = (field_type, default)

#     model_name = f"{_llm_tool_name(tool['name'])}_Args"
#     return create_model(model_name, **fields)


# def _extract_tool_list_payload(raw_response: Dict[str, Any]) -> List[Dict[str, Any]]:
#     return raw_response.get("result", {}).get("tools", [])


# def _extract_tool_call_text(raw_response: Dict[str, Any]) -> str:
#     result = raw_response.get("result", {})
#     content = result.get("content")

#     if isinstance(content, list):
#         text_parts: List[str] = []
#         for item in content:
#             if isinstance(item, dict):
#                 if item.get("type") == "text":
#                     text_parts.append(item.get("text", ""))
#                 elif "text" in item:
#                     text_parts.append(str(item["text"]))
#             else:
#                 text = getattr(item, "text", None)
#                 if text:
#                     text_parts.append(str(text))

#         joined = "\n".join(part for part in text_parts if part)
#         if joined:
#             return joined

#     # fallback to raw JSON string if MCP returns a non-standard payload
#     return str(raw_response)


# async def load_all_tools(client: Any) -> List[StructuredTool]:
#     raw = await client.tools_list()
#     all_tools = _extract_tool_list_payload(raw)

#     wrapped_tools: List[StructuredTool] = []

#     # Optional debug: print MCP tool mapping once at startup
#     # for tool in all_tools:
#     #     print(f"MCP backend tool: {tool['name']} -> LLM tool: {_llm_tool_name(tool['name'])}")

#     for tool_def in all_tools:
#         backend_name = tool_def["name"]           # exact name required by tools/call
#         llm_name = _llm_tool_name(backend_name)   # clean name shown to the LLM
#         description = _normalize_description(tool_def)
#         args_schema = _build_args_schema(tool_def)

#         async def _arun(_backend_name=backend_name, **kwargs):
#             result = await client.tool_call(_backend_name, kwargs)
#             return _extract_tool_call_text(result)

#         wrapped_tool = StructuredTool.from_function(
#             coroutine=_arun,
#             name=llm_name,
#             description=description,
#             args_schema=args_schema,
#         )
#         wrapped_tools.append(wrapped_tool)

#     return wrapped_tools


from __future__ import annotations

import hashlib
import re
from typing import Any, Dict, List

from app.mcp.tool_aliases import TOOL_ALIASES, TOOL_DESCRIPTIONS


def _slugify(value: str) -> str:
    value = value.strip()
    value = value.replace("/", "_").replace("-", "_").replace(".", "_")
    value = re.sub(r"[^a-zA-Z0-9_]", "_", value)
    value = re.sub(r"_+", "_", value)
    return value.strip("_")


def llm_tool_name(backend_name: str) -> str:
    alias = TOOL_ALIASES.get(backend_name)
    if alias:
        safe = _slugify(alias)
        return safe[:64]

    safe_backend = _slugify(backend_name)
    if len(safe_backend) <= 55:
        return safe_backend

    digest = hashlib.md5(backend_name.encode("utf-8")).hexdigest()[:8]
    return f"{safe_backend[:55]}_{digest}"[:64]


def tool_description(tool: Dict[str, Any]) -> str:
    backend_name = tool["name"]
    clean_name = llm_tool_name(backend_name)

    if clean_name in TOOL_DESCRIPTIONS:
        return TOOL_DESCRIPTIONS[clean_name]

    return tool.get("description") or clean_name


def extract_tools(raw_response: Dict[str, Any]) -> List[Dict[str, Any]]:
    return raw_response.get("result", {}).get("tools", [])


def get_tool_required_fields(tool: Dict[str, Any]) -> List[str]:
    schema = tool.get("inputSchema", {}) or {}
    properties = schema.get("properties", {}) or {}

    required = schema.get("required")

    # If backend does not provide required list, treat all request-body fields as required.
    if not required:
        return list(properties.keys())

    return list(required)


def build_tool_catalog(raw_tools: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    catalog: Dict[str, Dict[str, Any]] = {}

    for tool in raw_tools:
        backend_name = tool["name"]
        clean_name = llm_tool_name(backend_name)

        catalog[clean_name] = {
            "llm_name": clean_name,
            "backend_name": backend_name,
            "description": tool_description(tool),
            "inputSchema": tool.get("inputSchema", {}) or {},
            "required_fields": get_tool_required_fields(tool),
            "raw": tool,
        }

    return catalog


def compact_tool_catalog_for_prompt(catalog: Dict[str, Dict[str, Any]]) -> str:
    lines = []

    for tool_name, item in catalog.items():
        schema = item.get("inputSchema", {}) or {}
        properties = schema.get("properties", {}) or {}
        required = item.get("required_fields", [])

        field_parts = []
        for field_name, meta in properties.items():
            field_type = meta.get("type", "string") if isinstance(meta, dict) else "string"
            field_parts.append(f"{field_name}:{field_type}")

        lines.append(
            f"- tool_name: {tool_name}\n"
            f"  description: {item['description']}\n"
            f"  fields: {', '.join(field_parts) if field_parts else 'none'}\n"
            f"  required_fields: {', '.join(required) if required else 'none'}"
        )

    return "\n".join(lines)


def extract_tool_call_text(raw_response: Dict[str, Any]) -> str:
    result = raw_response.get("result", {})
    content = result.get("content")

    if isinstance(content, list):
        text_parts: List[str] = []
        for item in content:
            if isinstance(item, dict):
                if item.get("type") == "text":
                    text_parts.append(item.get("text", ""))
                elif "text" in item:
                    text_parts.append(str(item["text"]))
            else:
                text = getattr(item, "text", None)
                if text:
                    text_parts.append(str(text))

        joined = "\n".join(part for part in text_parts if part)
        if joined:
            return joined

    return str(raw_response)