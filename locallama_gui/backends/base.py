from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from dataclasses import dataclass
from typing import Any

from locallama_gui.core.domain import ChatMessage, ModelInfo


@dataclass(slots=True)
class BackendStatus:
    state: str
    latency_ms: float = 0.0
    detail: str = ""


class LLMBackend(ABC):
    name: str

    def __init__(self, base_url: str, api_key: str = "") -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    @abstractmethod
    async def test_connection(self) -> BackendStatus: ...

    @abstractmethod
    async def list_models(self) -> list[ModelInfo]: ...

    @abstractmethod
    async def chat(
        self,
        model: str,
        messages: list[ChatMessage],
        options: dict[str, Any],
        stream: bool,
    ) -> AsyncIterator[str]: ...

    async def pull_model(self, name: str) -> AsyncIterator[str]:
        raise NotImplementedError("Model pull is not supported by this backend")

    async def push_model(self, name: str) -> AsyncIterator[str]:
        raise NotImplementedError("Model push is not supported by this backend")

    async def delete_model(self, name: str) -> None:
        raise NotImplementedError("Model deletion is not supported by this backend")

    async def copy_model(self, source: str, destination: str) -> None:
        raise NotImplementedError("Model copy is not supported by this backend")

    async def create_model(self, name: str, modelfile: str) -> AsyncIterator[str]:
        raise NotImplementedError("Model creation is not supported by this backend")

    async def show_model(self, name: str) -> dict[str, Any]:
        raise NotImplementedError("Model metadata is not supported by this backend")
