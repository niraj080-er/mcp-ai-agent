# from __future__ import annotations

# from fastapi import APIRouter

# from app.schemas.chat import ChatRequest, ChatResponse
# from app.services.chat_service import ChatService

# router = APIRouter(prefix="/chat", tags=["chat"])
# chat_service = ChatService()


# @router.post(
#     "",
#     response_model=ChatResponse,
#     summary="Send a chat message to the wallet agent",
#     description=(
#         "Accepts a user query, lets the LLM select the correct MCP tool, "
#         "validates required fields, calls the tool, and returns both the "
#         "assistant response and raw tool response."
#     ),
# )
# async def chat(request: ChatRequest) -> ChatResponse:
#     result = await chat_service.chat(
#         thread_id=request.thread_id,
#         user_query=request.message,
#         provider=request.provider,
#     )

#     return ChatResponse(
#         thread_id=result["thread_id"],
#         provider=result.get("provider"),
#         response=result["response_text"],
#         success=result.get("success", True),
#         error=result.get("error"),
#         tool_name=result.get("tool_name"),
#         backend_tool_name=result.get("backend_tool_name"),
#         tool_args=result.get("tool_args") or {},
#         tool_response=result.get("tool_response"),
#     )


from __future__ import annotations

from fastapi import APIRouter

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["chat"])
chat_service = ChatService()


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    result = await chat_service.chat(
        thread_id=request.thread_id,
        user_query=request.message,
        provider=request.provider,
    )

    return ChatResponse(
        thread_id=result["thread_id"],
        provider=result.get("provider"),
        response=result["response_text"],
        success=result.get("success", True),
        error=result.get("error"),
        tool_name=result.get("tool_name"),
        backend_tool_name=result.get("backend_tool_name"),
        tool_args=result.get("tool_args") or {},
        tool_response=result.get("tool_response"),
    )