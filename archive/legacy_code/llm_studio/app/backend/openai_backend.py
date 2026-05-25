"""
OpenAI-compatible backend.
Works with OpenAI, Groq, Together AI, LM Studio, vLLM, llama.cpp server, etc.
"""

import json
import logging
import time
from typing import Iterator, List, Dict, Any, Optional

import httpx

from app.backend.base_backend import BaseBackend, BackendError
from app.models.model_info import ModelInfo

log = logging.getLogger(__name__)
TIMEOUT = httpx.Timeout(connect=5.0, read=None, write=30.0, pool=5.0)


class OpenAIBackend(BaseBackend):
    name = "openai"

    def _headers(self) -> dict:
        h = {"Content-Type": "application/json"}
        if self.api_key:
            h["Authorization"] = f"Bearer {self.api_key}"
        return h

    def _client(self, timeout=TIMEOUT) -> httpx.Client:
        return httpx.Client(base_url=self.base_url, headers=self._headers(),
                            timeout=timeout)

    def test_connection(self) -> bool:
        try:
            with self._client(timeout=httpx.Timeout(5.0)) as c:
                r = c.get("/models")
                return r.status_code in (200, 401)  # 401 = reachable, bad key
        except Exception:
            return False

    def get_status(self) -> Dict[str, Any]:
        t0 = time.time()
        try:
            with self._client(timeout=httpx.Timeout(5.0)) as c:
                r = c.get("/models")
                latency = int((time.time() - t0) * 1000)
                return {
                    "connected": r.status_code in (200, 401),
                    "version": "openai-compat",
                    "latency_ms": latency,
                }
        except Exception:
            return {"connected": False, "version": "", "latency_ms": 0}

    def list_models(self) -> List[ModelInfo]:
        try:
            with self._client() as c:
                r = c.get("/models")
                r.raise_for_status()
                data = r.json()
                models = data.get("data", data) if isinstance(data, dict) else data
                return [ModelInfo.from_openai(m) for m in models]
        except Exception as e:
            raise BackendError(f"list_models failed: {e}")

    def chat(
        self,
        messages: List[Dict[str, Any]],
        model: str,
        params: Dict[str, Any],
    ) -> Dict[str, Any]:
        payload = self._build_payload(messages, model, params, stream=False)
        try:
            with self._client() as c:
                r = c.post("/chat/completions", json=payload)
                r.raise_for_status()
                data = r.json()
                choice = data["choices"][0]
                usage = data.get("usage", {})
                return {
                    "content": choice["message"]["content"],
                    "model": data.get("model", model),
                    "usage": {
                        "prompt_tokens": usage.get("prompt_tokens", 0),
                        "completion_tokens": usage.get("completion_tokens", 0),
                        "total_duration_ms": 0,
                    },
                }
        except BackendError:
            raise
        except Exception as e:
            raise BackendError(f"chat failed: {e}")

    def stream_chat(
        self,
        messages: List[Dict[str, Any]],
        model: str,
        params: Dict[str, Any],
    ) -> Iterator[str]:
        payload = self._build_payload(messages, model, params, stream=True)
        try:
            with httpx.Client(base_url=self.base_url, headers=self._headers(),
                               timeout=TIMEOUT) as c:
                with c.stream("POST", "/chat/completions", json=payload) as resp:
                    resp.raise_for_status()
                    for line in resp.iter_lines():
                        line = line.strip()
                        if not line or not line.startswith("data:"):
                            continue
                        chunk = line[5:].strip()
                        if chunk == "[DONE]":
                            return
                        try:
                            data = json.loads(chunk)
                            delta = data["choices"][0].get("delta", {})
                            token = delta.get("content", "")
                            if token:
                                yield token
                        except (json.JSONDecodeError, KeyError, IndexError):
                            pass
        except Exception as e:
            raise BackendError(f"stream_chat failed: {e}")

    def _build_payload(
        self,
        messages: List[Dict],
        model: str,
        params: Dict[str, Any],
        stream: bool,
    ) -> dict:
        payload: Dict[str, Any] = {
            "model": model,
            "messages": messages,
            "stream": stream,
        }
        mapping = {
            "temperature": "temperature",
            "top_p": "top_p",
            "num_predict": "max_tokens",
            "seed": "seed",
            "stop": "stop",
        }
        for src, dst in mapping.items():
            if src in params and params[src] not in (None, -1, ""):
                payload[dst] = params[src]
        return payload
