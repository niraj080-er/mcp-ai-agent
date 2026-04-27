from __future__ import annotations

from typing import List, Dict


def summarize_recent_messages(messages: List[Dict[str, str]], max_items: int = 8) -> str:
    """
    Minimal local summarizer placeholder.
    Replace with LLM summarization if needed.
    """
    if not messages:
        return ""

    trimmed = messages[-max_items:]
    parts = []
    for msg in trimmed:
        role = msg.get("role", "unknown")
        content = msg.get("content", "")
        if len(content) > 160:
            content = content[:157] + "..."
        parts.append(f"{role}: {content}")
    return "\n".join(parts)