from __future__ import annotations

import json
import time
from collections.abc import AsyncIterator
from typing import Any

import httpx

from locallama_gui.backends.base import BackendStatus, LLMBackend
from locallama_gui.core.domain import ChatMessage, ModelInfo


class OllamaBackend(LLMBackend):
    name = "ollama"

    async def test_connection(self) -> BackendStatus:
        started = time.perf_counter()
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                response.raise_for_status()
            return BackendStatus("connected", (time.perf_counter() - started) * 1000, self.base_url)
        except Exception as exc:  # noqa: BLE001 - surfaced to diagnostics UI
            return BackendStatus("disconnected", (time.perf_counter() - started) * 1000, str(exc))

    async def list_models(self) -> list[ModelInfo]:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(f"{self.base_url}/api/tags")
            response.raise_for_status()
        models: list[ModelInfo] = []
        for item in response.json().get("models", []):
            details = item.get("details", {}) or {}
            models.append(
                ModelInfo(
                    name=item.get("name", ""),
                    size=item.get("size", 0),
                    parameter_size=details.get("parameter_size", ""),
                    quantization=details.get("quantization_level", ""),
                    context_size=(item.get("model_info", {}) or {}).get("llama.context_length", 0),
                    backend="Ollama",
                    metadata=item,
                )
            )
        return models

    async def chat(
        self,
        model: str,
        messages: list[ChatMessage],
        options: dict[str, Any],
        stream: bool,
    ) -> AsyncIterator[str]:
        payload = {
            "model": model,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "options": options,
            "stream": stream,
        }
        async with httpx.AsyncClient(timeout=None) as client:
            if stream:
                async with client.stream("POST", f"{self.base_url}/api/chat", json=payload) as response:
                    response.raise_for_status()
                    async for line in response.aiter_lines():
                        if not line:
                            continue
                        data = json.loads(line)
                        if data.get("message", {}).get("content"):
                            yield data["message"]["content"]
                        if data.get("done"):
                            break
            else:
                response = await client.post(f"{self.base_url}/api/chat", json=payload)
                response.raise_for_status()
                yield response.json().get("message", {}).get("content", "")

    async def pull_model(self, name: str) -> AsyncIterator[str]:
        async for text in self._stream_endpoint("/api/pull", {"name": name, "stream": True}):
            yield text

    async def push_model(self, name: str) -> AsyncIterator[str]:
        async for text in self._stream_endpoint("/api/push", {"name": name, "stream": True}):
            yield text

    async def delete_model(self, name: str) -> None:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.request("DELETE", f"{self.base_url}/api/delete", json={"name": name})
            response.raise_for_status()

    async def copy_model(self, source: str, destination: str) -> None:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(f"{self.base_url}/api/copy", json={"source": source, "destination": destination})
            response.raise_for_status()

    async def create_model(self, name: str, modelfile: str) -> AsyncIterator[str]:
        async for text in self._stream_endpoint("/api/create", {"name": name, "modelfile": modelfile, "stream": True}):
            yield text

    async def show_model(self, name: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(f"{self.base_url}/api/show", json={"name": name})
            response.raise_for_status()
            return response.json()

    async def _stream_endpoint(self, path: str, payload: dict[str, Any]) -> AsyncIterator[str]:
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream("POST", f"{self.base_url}{path}", json=payload) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if not line:
                        continue
                    data = json.loads(line)
                    yield data.get("status") or data.get("error") or json.dumps(data)
