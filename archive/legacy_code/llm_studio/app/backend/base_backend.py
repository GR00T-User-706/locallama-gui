"""
Abstract backend interface.
All LLM backends must implement this protocol.
"""

from abc import ABC, abstractmethod
from typing import Iterator, List, Dict, Any, Optional
from app.models.model_info import ModelInfo


class BackendError(Exception):
    """Raised by backend operations on failure."""
    pass


class BaseBackend(ABC):
    """Abstract base for all LLM provider backends."""

    name: str = "base"

    def __init__(self, base_url: str, api_key: str = ""):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    # ── Connection ────────────────────────────────────────────────────────

    @abstractmethod
    def test_connection(self) -> bool:
        """Return True if backend is reachable."""

    def get_status(self) -> Dict[str, Any]:
        """Return dict with: connected, version, latency_ms."""
        return {"connected": False, "version": "", "latency_ms": 0}

    # ── Models ────────────────────────────────────────────────────────────

    @abstractmethod
    def list_models(self) -> List[ModelInfo]:
        """Return list of available models."""

    def get_model_info(self, model_name: str) -> Optional[ModelInfo]:
        return None

    def pull_model(self, model_name: str) -> Iterator[Dict[str, Any]]:
        """Yield progress dicts: {status, completed, total, digest}."""
        raise NotImplementedError(f"{self.name} does not support pull")

    def push_model(self, model_name: str) -> Iterator[Dict[str, Any]]:
        raise NotImplementedError(f"{self.name} does not support push")

    def delete_model(self, model_name: str) -> bool:
        raise NotImplementedError(f"{self.name} does not support delete")

    def create_model(self, name: str, modelfile: str) -> Iterator[Dict[str, Any]]:
        raise NotImplementedError(f"{self.name} does not support create")

    def copy_model(self, source: str, destination: str) -> bool:
        raise NotImplementedError(f"{self.name} does not support copy")

    def show_model(self, model_name: str) -> Dict[str, Any]:
        raise NotImplementedError(f"{self.name} does not support show")

    # ── Chat ──────────────────────────────────────────────────────────────

    @abstractmethod
    def chat(
        self,
        messages: List[Dict[str, Any]],
        model: str,
        params: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Non-streaming chat. Return dict with 'content' and 'usage'."""

    @abstractmethod
    def stream_chat(
        self,
        messages: List[Dict[str, Any]],
        model: str,
        params: Dict[str, Any],
    ) -> Iterator[str]:
        """Streaming chat. Yield token strings."""

    # ── Embeddings ────────────────────────────────────────────────────────

    def embed(self, text: str, model: str) -> List[float]:
        raise NotImplementedError(f"{self.name} does not support embeddings")
