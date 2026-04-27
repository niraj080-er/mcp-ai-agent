from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes_chat import router as chat_router
from app.core.config import get_settings
from app.core.logging import setup_logging

settings = get_settings()
setup_logging()

description = """
Wallet Agent API for MCP-based chat orchestration.

## Features

- Multi-model support: OpenAI, Gemini, Anthropic
- MCP tool routing
- Thread-based conversation memory
- Follow-up query handling using structured session context

## Main endpoint

- `POST /chat` — Send a chat message to the agent
"""

app = FastAPI(
    title="Wallet Agent API",
    summary="FastAPI backend for a multi-model MCP-enabled wallet assistant",
    description=description,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)


@app.get("/health", tags=["health"], summary="Health check")
async def health():
    return {"status": "ok"}