from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from dataclasses import dataclass
from typing import Any

import httpx

from locallama_gui.core.domain import ChatMessage, ModelInfo


@dataclass(slots=True)
class BackendStatus:
    state: str
    latency_ms: float = 0.0
    detail: str = ""




VALID_CHAT_ROLES = {"system", "user", "assistant", "tool"}


def build_chat_messages(messages: list[ChatMessage]) -> list[dict[str, str]]:
    """Validate and serialize chat messages before sending them to a backend."""
    serialized: list[dict[str, str]] = []
    for index, message in enumerate(messages):
        role = str(message.role).strip().lower()
        content = message.content if isinstance(message.content, str) else str(message.content)
        if role not in VALID_CHAT_ROLES:
            raise ValueError(f"Invalid chat message role at index {index}: {role!r}")
        if not content.strip():
            continue
        serialized.append({"role": role, "content": content})
    if not serialized:
        raise ValueError("Chat request contains no non-empty messages.")
    return serialized


def raise_for_chat_response(response: httpx.Response) -> None:
    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        detail = response.text.strip()
        if len(detail) > 1000:
            detail = detail[:1000] + "…"
        raise RuntimeError(
            f"Chat request failed with HTTP {response.status_code}: {detail or response.reason_phrase}"
        ) from exc


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
