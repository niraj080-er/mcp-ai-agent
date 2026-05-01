from __future__ import annotations

from typing import List

import httpx
from langchain_core.messages import AIMessage, BaseMessage


class LocalLLM:
    def __init__(
        self,
        api_url: str,
        model_name: str,
        temperature: float = 0.0,
        top_p: float = 0.0001,
        max_tokens: int = 2000,
    ) -> None:
        self.api_url = api_url
        self.model_name = model_name
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens

    def _role(self, message: BaseMessage) -> str:
        if message.type == "system":
            return "system"
        if message.type == "human":
            return "user"
        if message.type == "ai":
            return "assistant"
        return "user"

    def _format_messages(self, messages: List[BaseMessage]) -> List[dict]:
        return [
            {
                "role": self._role(message),
                "content": str(message.content),
            }
            for message in messages
        ]

    async def ainvoke(self, messages: List[BaseMessage]) -> AIMessage:
        body = {
            "model": self.model_name,
            "messages": self._format_messages(messages),
            "temperature": self.temperature,
            "top_p": self.top_p,
            "max_tokens": self.max_tokens,
        }

        async with httpx.AsyncClient(timeout=120.0, verify=False) as client:
            response = await client.post(
                self.api_url,
                headers={"Content-Type": "application/json"},
                json=body,
            )
            response.raise_for_status()

        data = response.json()
        return AIMessage(content=data["choices"][0]["message"]["content"])