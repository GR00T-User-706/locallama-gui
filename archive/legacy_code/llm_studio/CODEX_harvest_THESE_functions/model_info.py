"""Model metadata data class."""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any


@dataclass
class ModelInfo:
    name: str
    size: int = 0                    # bytes
    digest: str = ""
    parameter_size: str = ""         # e.g. "7B"
    quantization_level: str = ""     # e.g. "Q4_K_M"
    family: str = ""
    format: str = ""
    context_length: int = 0
    embedding_length: int = 0
    num_attention_heads: int = 0
    num_layers: int = 0
    modified_at: str = ""
    details: Dict[str, Any] = field(default_factory=dict)

    @property
    def size_gb(self) -> float:
        return self.size / (1024 ** 3)

    @property
    def size_str(self) -> str:
        if self.size >= 1024 ** 3:
            return f"{self.size_gb:.1f} GB"
        if self.size >= 1024 ** 2:
            return f"{self.size / (1024**2):.0f} MB"
        return f"{self.size} B"

    @property
    def display_name(self) -> str:
        return self.name

    def ram_estimate_gb(self) -> float:
        """Very rough estimate of RAM required."""
        if self.size > 0:
            return self.size_gb * 1.1
        return 0.0

    @classmethod
    def from_ollama(cls, data: dict) -> "ModelInfo":
        details = data.get("details", {})
        info = data.get("model_info", {})
        return cls(
            name=data.get("name", ""),
            size=data.get("size", 0),
            digest=data.get("digest", ""),
            parameter_size=details.get("parameter_size", ""),
            quantization_level=details.get("quantization_level", ""),
            family=details.get("family", ""),
            format=details.get("format", ""),
            context_length=info.get("llama.context_length", 0),
            embedding_length=info.get("llama.embedding_length", 0),
            num_attention_heads=info.get("llama.attention.head_count", 0),
            num_layers=info.get("llama.block_count", 0),
            modified_at=data.get("modified_at", ""),
            details={**details, **info},
        )

    @classmethod
    def from_openai(cls, data: dict) -> "ModelInfo":
        return cls(
            name=data.get("id", ""),
            modified_at=str(data.get("created", "")),
        )
