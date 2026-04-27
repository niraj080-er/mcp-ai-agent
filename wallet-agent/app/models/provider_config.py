from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel


ProviderType = Literal["openai", "google", "anthropic"]


class ProviderConfig(BaseModel):
    type: ProviderType
    model: str
    temperature: float = 0.0
    max_tokens: Optional[int] = None