from __future__ import annotations

from locallama_gui.backends.base import LLMBackend
from locallama_gui.backends.ollama import OllamaBackend
from locallama_gui.backends.openai import OpenAICompatibleBackend
from locallama_gui.core.config import ProviderProfile


def create_backend(profile: ProviderProfile) -> LLMBackend:
    if profile.provider_type == "openai":
        return OpenAICompatibleBackend(profile.base_url, profile.api_key)
    if profile.provider_type == "llama.cpp":
        return OpenAICompatibleBackend(profile.base_url, profile.api_key)
    return OllamaBackend(profile.base_url, profile.api_key)
