from __future__ import annotations

import json
import uuid
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal

Role = Literal["system", "user", "assistant", "tool"]


def now_iso() -> str:
    return datetime.now(UTC).isoformat()


@dataclass(slots=True)
class ChatMessage:
    role: Role
    content: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now_iso)
    name: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ChatSession:
    title: str = "New Chat"
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now_iso)
    updated_at: str = field(default_factory=now_iso)
    provider: str = "Local Ollama"
    model: str = ""
    system_prompt: str = ""
    messages: list[ChatMessage] = field(default_factory=list)
    parameters: dict[str, Any] = field(default_factory=dict)

    def touch(self) -> None:
        self.updated_at = now_iso()

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)

    @classmethod
    def from_file(cls, path: Path) -> "ChatSession":
        data = json.loads(path.read_text(encoding="utf-8"))
        data["messages"] = [ChatMessage(**item) for item in data.get("messages", [])]
        return cls(**data)

    def save(self, directory: Path) -> Path:
        self.touch()
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / f"{self.id}.json"
        path.write_text(self.to_json(), encoding="utf-8")
        return path

    def export_markdown(self) -> str:
        parts = [f"# {self.title}", ""]
        for msg in self.messages:
            parts.extend([f"## {msg.role.title()}", "", msg.content, ""])
        return "\n".join(parts)

    def export_text(self) -> str:
        return "\n\n".join(f"[{msg.role}]\n{msg.content}" for msg in self.messages)


@dataclass(slots=True)
class ModelInfo:
    name: str
    size: int = 0
    parameter_size: str = ""
    quantization: str = ""
    context_size: int = 0
    backend: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def size_display(self) -> str:
        if self.size <= 0:
            return "unknown"
        value = float(self.size)
        for unit in ("B", "KB", "MB", "GB", "TB"):
            if value < 1024 or unit == "TB":
                return f"{value:.1f} {unit}"
            value /= 1024
        return f"{self.size} B"


@dataclass(slots=True)
class PromptRecord:
    title: str
    content: str
    category: str = "General"
    favorite: bool = False
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    versions: list[dict[str, str]] = field(default_factory=list)
    updated_at: str = field(default_factory=now_iso)


@dataclass(slots=True)
class AgentProfile:
    name: str
    model: str = ""
    system_prompt_id: str = ""
    tools: list[str] = field(default_factory=list)
    plugins: list[str] = field(default_factory=list)
    memory_mode: str = "session"
    reasoning_mode: str = "normal"
    behavior: str = "constrained"
    execution_policy: str = "confirm_tools"
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
