from __future__ import annotations

from typing import Any, Dict

from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

from app.core.config import get_settings, load_yaml_config
from app.core.exceptions import ConfigurationError
from app.models.provider_config import ProviderConfig
from app.models.local_llm import LocalLLM


class LLMFactory:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.config = load_yaml_config()

    def _get_provider_config(self, provider: str | None) -> ProviderConfig:
        provider_name = provider or self.config["default_provider"]
        providers: Dict[str, Any] = self.config["providers"]

        if provider_name not in providers:
            raise ConfigurationError(f"Unknown provider: {provider_name}")

        return ProviderConfig(**providers[provider_name])

    def get_llm(self, provider: str | None = None):
        cfg = self._get_provider_config(provider)

        common_kwargs = {
            "model": cfg.model,
            "temperature": cfg.temperature,
        }
        if cfg.max_tokens is not None:
            common_kwargs["max_tokens"] = cfg.max_tokens

        if cfg.type == "openai":
            if not self.settings.openai_api_key:
                raise ConfigurationError("OPENAI_API_KEY is missing")
            return ChatOpenAI(
                api_key=self.settings.openai_api_key,
                **common_kwargs,
            )

        if cfg.type == "google":
            if not self.settings.google_api_key:
                raise ConfigurationError("GOOGLE_API_KEY is missing")
            return ChatGoogleGenerativeAI(
                google_api_key=self.settings.google_api_key,
                **common_kwargs,
            )

        if cfg.type == "anthropic":
            if not self.settings.anthropic_api_key:
                raise ConfigurationError("ANTHROPIC_API_KEY is missing")
            return ChatAnthropic(
                api_key=self.settings.anthropic_api_key,
                **common_kwargs,
            )
        
        if cfg.type == "openai_compatible":
            return LocalLLM(
                api_url=cfg.api_url,
                model_name=cfg.model,
                temperature=cfg.temperature,
                top_p=cfg.top_p,
                max_tokens=cfg.max_tokens,
            )

        raise ConfigurationError(f"Unsupported provider type: {cfg.type}")