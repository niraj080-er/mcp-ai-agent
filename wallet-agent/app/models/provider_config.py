from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel


ProviderType = Literal["openai", "google", "anthropic", "openai_compatible"]


class ProviderConfig(BaseModel):
    type: ProviderType
    model: str
    temperature: float = 0.0
    max_tokens: Optional[int] = None
    api_url: Optional[str] = None
    top_p: Optional[float] = None