from app.backend.base_backend import BaseBackend, BackendError
from app.backend.ollama_backend import OllamaBackend
from app.backend.openai_backend import OpenAIBackend


BACKEND_REGISTRY = {
    "ollama": OllamaBackend,
    "openai": OpenAIBackend,
}


def create_backend(name: str, base_url: str, api_key: str = "") -> BaseBackend:
    cls = BACKEND_REGISTRY.get(name)
    if cls is None:
        raise ValueError(f"Unknown backend: {name}")
    return cls(base_url=base_url, api_key=api_key)
