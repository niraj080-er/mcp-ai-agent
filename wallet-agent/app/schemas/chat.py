# from __future__ import annotations

# from typing import Any, Dict, Optional

# from pydantic import BaseModel, Field


# class ChatRequest(BaseModel):
#     thread_id: str = Field(
#         ...,
#         description="Conversation thread id. Use same thread_id for follow-up queries.",
#         examples=["thread-001"],
#     )
#     message: str = Field(
#         ...,
#         description="User query in simple English.",
#         examples=["list transfer types for testpm"],
#     )
#     provider: Optional[str] = Field(
#         default=None,
#         description="Model provider: openai, gemini, anthropic",
#         examples=["openai"],
#     )


# class ChatResponse(BaseModel):
#     thread_id: str
#     provider: Optional[str] = None

#     response: str

#     success: bool = True
#     error: Optional[str] = None

#     tool_name: Optional[str] = None
#     backend_tool_name: Optional[str] = None
#     tool_args: Dict[str, Any] = Field(default_factory=dict)
#     tool_response: Optional[Dict[str, Any]] = None


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