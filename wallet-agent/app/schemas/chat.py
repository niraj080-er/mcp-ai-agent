from __future__ import annotations

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    thread_id: str
    message: str
    provider: Optional[str] = None


class ChatResponse(BaseModel):
    thread_id: str
    provider: Optional[str] = None
    response: str

    success: bool = True
    error: Optional[str] = None

    tool_name: Optional[str] = None
    backend_tool_name: Optional[str] = None
    tool_args: Dict[str, Any] = Field(default_factory=dict)
    tool_response: Optional[Dict[str, Any]] = None