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