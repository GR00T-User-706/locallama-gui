from __future__ import annotations

import json
import time
from collections.abc import AsyncIterator
from typing import Any

import httpx

from locallama_gui.backends.base import BackendStatus, LLMBackend
from locallama_gui.core.domain import ChatMessage, ModelInfo


class OpenAICompatibleBackend(LLMBackend):
    name = "openai"

    def _headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    async def test_connection(self) -> BackendStatus:
        started = time.perf_counter()
        try:
            async with httpx.AsyncClient(timeout=5, headers=self._headers()) as client:
                response = await client.get(f"{self.base_url}/models")
                response.raise_for_status()
            return BackendStatus("connected", (time.perf_counter() - started) * 1000, self.base_url)
        except Exception as exc:  # noqa: BLE001
            return BackendStatus("disconnected", (time.perf_counter() - started) * 1000, str(exc))

    async def list_models(self) -> list[ModelInfo]:
        async with httpx.AsyncClient(timeout=15, headers=self._headers()) as client:
            response = await client.get(f"{self.base_url}/models")
            response.raise_for_status()
        return [
            ModelInfo(name=item.get("id", ""), backend="OpenAI-compatible", metadata=item)
            for item in response.json().get("data", [])
        ]

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
            "temperature": options.get("temperature", 0.7),
            "top_p": options.get("top_p", 0.9),
            "max_tokens": options.get("num_predict", 512),
            "stream": stream,
        }
        if options.get("stop"):
            payload["stop"] = options["stop"]
        async with httpx.AsyncClient(timeout=None, headers=self._headers()) as client:
            if stream:
                async with client.stream("POST", f"{self.base_url}/chat/completions", json=payload) as response:
                    response.raise_for_status()
                    async for line in response.aiter_lines():
                        if not line.startswith("data: "):
                            continue
                        raw = line[6:]
                        if raw == "[DONE]":
                            break
                        data = json.loads(raw)
                        delta = data.get("choices", [{}])[0].get("delta", {}).get("content")
                        if delta:
                            yield delta
            else:
                response = await client.post(f"{self.base_url}/chat/completions", json=payload)
                response.raise_for_status()
                yield response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
