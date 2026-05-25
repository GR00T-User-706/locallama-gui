"""
Ollama backend — full Ollama REST API implementation.
Docs: https://github.com/ollama/ollama/blob/main/docs/api.md
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


class OllamaBackend(BaseBackend):
    name = "ollama"

    def _headers(self) -> dict:
        h = {"Content-Type": "application/json"}
        if self.api_key:
            h["Authorization"] = f"Bearer {self.api_key}"
        return h

    def _client(self, timeout=TIMEOUT) -> httpx.Client:
        return httpx.Client(base_url=self.base_url, headers=self._headers(),
                            timeout=timeout)

    # ── Connection ────────────────────────────────────────────────────────

    def test_connection(self) -> bool:
        try:
            with self._client(timeout=httpx.Timeout(5.0)) as c:
                r = c.get("/")
                return r.status_code == 200
        except Exception as e:
            log.debug("Ollama connection test failed: %s", e)
            return False

    def get_status(self) -> Dict[str, Any]:
        t0 = time.time()
        try:
            with self._client(timeout=httpx.Timeout(5.0)) as c:
                r = c.get("/api/version")
                latency = int((time.time() - t0) * 1000)
                if r.status_code == 200:
                    data = r.json()
                    return {
                        "connected": True,
                        "version": data.get("version", "unknown"),
                        "latency_ms": latency,
                    }
        except Exception as e:
            log.debug("Ollama status check: %s", e)
        return {"connected": False, "version": "", "latency_ms": 0}

    # ── Models ────────────────────────────────────────────────────────────

    def list_models(self) -> List[ModelInfo]:
        try:
            with self._client() as c:
                r = c.get("/api/tags")
                r.raise_for_status()
                return [ModelInfo.from_ollama(m) for m in r.json().get("models", [])]
        except httpx.ConnectError:
            raise BackendError("Cannot connect to Ollama. Is it running?")
        except Exception as e:
            raise BackendError(f"list_models failed: {e}")

    def get_model_info(self, model_name: str) -> Optional[ModelInfo]:
        data = self.show_model(model_name)
        if data:
            data["name"] = model_name
            return ModelInfo.from_ollama(data)
        return None

    def show_model(self, model_name: str) -> Dict[str, Any]:
        try:
            with self._client() as c:
                r = c.post("/api/show", json={"name": model_name})
                r.raise_for_status()
                return r.json()
        except Exception as e:
            raise BackendError(f"show_model failed: {e}")

    def pull_model(self, model_name: str) -> Iterator[Dict[str, Any]]:
        try:
            with httpx.Client(base_url=self.base_url, headers=self._headers(),
                               timeout=httpx.Timeout(connect=5.0, read=None,
                                                      write=30.0, pool=5.0)) as c:
                with c.stream("POST", "/api/pull",
                               json={"name": model_name, "stream": True}) as resp:
                    resp.raise_for_status()
                    for line in resp.iter_lines():
                        if line:
                            try:
                                yield json.loads(line)
                            except json.JSONDecodeError:
                                pass
        except Exception as e:
            raise BackendError(f"pull_model failed: {e}")

    def push_model(self, model_name: str) -> Iterator[Dict[str, Any]]:
        try:
            with httpx.Client(base_url=self.base_url, headers=self._headers(),
                               timeout=TIMEOUT) as c:
                with c.stream("POST", "/api/push",
                               json={"name": model_name, "stream": True}) as resp:
                    resp.raise_for_status()
                    for line in resp.iter_lines():
                        if line:
                            try:
                                yield json.loads(line)
                            except json.JSONDecodeError:
                                pass
        except Exception as e:
            raise BackendError(f"push_model failed: {e}")

    def delete_model(self, model_name: str) -> bool:
        try:
            with self._client() as c:
                r = c.request("DELETE", "/api/delete", json={"name": model_name})
                return r.status_code == 200
        except Exception as e:
            raise BackendError(f"delete_model failed: {e}")

    def create_model(self, name: str, modelfile: str) -> Iterator[Dict[str, Any]]:
        try:
            with httpx.Client(base_url=self.base_url, headers=self._headers(),
                               timeout=TIMEOUT) as c:
                with c.stream("POST", "/api/create",
                               json={"name": name, "modelfile": modelfile,
                                     "stream": True}) as resp:
                    resp.raise_for_status()
                    for line in resp.iter_lines():
                        if line:
                            try:
                                yield json.loads(line)
                            except json.JSONDecodeError:
                                pass
        except Exception as e:
            raise BackendError(f"create_model failed: {e}")

    def copy_model(self, source: str, destination: str) -> bool:
        try:
            with self._client() as c:
                r = c.post("/api/copy", json={"source": source,
                                               "destination": destination})
                return r.status_code == 200
        except Exception as e:
            raise BackendError(f"copy_model failed: {e}")

    # ── Chat ──────────────────────────────────────────────────────────────

    def _build_options(self, params: Dict[str, Any]) -> dict:
        option_keys = {
            "temperature", "top_k", "top_p", "min_p", "repeat_penalty",
            "repeat_last_n", "mirostat", "mirostat_eta", "mirostat_tau",
            "tfs_z", "num_predict", "seed", "stop", "num_ctx",
            "num_batch", "num_gpu",
        }
        return {k: v for k, v in params.items()
                if k in option_keys and v is not None}

    def chat(
        self,
        messages: List[Dict[str, Any]],
        model: str,
        params: Dict[str, Any],
    ) -> Dict[str, Any]:
        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": self._build_options(params),
        }
        try:
            with self._client() as c:
                r = c.post("/api/chat", json=payload)
                r.raise_for_status()
                data = r.json()
                return {
                    "content": data.get("message", {}).get("content", ""),
                    "model": data.get("model", model),
                    "usage": {
                        "prompt_tokens": data.get("prompt_eval_count", 0),
                        "completion_tokens": data.get("eval_count", 0),
                        "total_duration_ms": data.get("total_duration", 0) // 1_000_000,
                    },
                }
        except httpx.ConnectError:
            raise BackendError("Cannot connect to Ollama.")
        except Exception as e:
            raise BackendError(f"chat failed: {e}")

    def stream_chat(
        self,
        messages: List[Dict[str, Any]],
        model: str,
        params: Dict[str, Any],
    ) -> Iterator[str]:
        payload = {
            "model": model,
            "messages": messages,
            "stream": True,
            "options": self._build_options(params),
        }
        try:
            with httpx.Client(base_url=self.base_url, headers=self._headers(),
                               timeout=TIMEOUT) as c:
                with c.stream("POST", "/api/chat", json=payload) as resp:
                    resp.raise_for_status()
                    for line in resp.iter_lines():
                        if line:
                            try:
                                data = json.loads(line)
                                if data.get("done"):
                                    return
                                token = data.get("message", {}).get("content", "")
                                if token:
                                    yield token
                            except json.JSONDecodeError:
                                pass
        except httpx.ConnectError:
            raise BackendError("Cannot connect to Ollama.")
        except Exception as e:
            raise BackendError(f"stream_chat failed: {e}")

    def embed(self, text: str, model: str) -> List[float]:
        try:
            with self._client() as c:
                r = c.post("/api/embed", json={"model": model, "input": text})
                r.raise_for_status()
                data = r.json()
                embeddings = data.get("embeddings", [])
                return embeddings[0] if embeddings else []
        except Exception as e:
            raise BackendError(f"embed failed: {e}")
