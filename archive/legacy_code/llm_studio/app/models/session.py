"""Chat session data model."""

import uuid
import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any

from app.models.chat_message import ChatMessage


@dataclass
class ChatSession:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = "New Chat"
    model: str = ""
    backend: str = "ollama"
    system_prompt: str = ""
    messages: List[ChatMessage] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    parameters: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    agent_id: Optional[str] = None

    def add_message(self, msg: ChatMessage):
        self.messages.append(msg)
        self.updated_at = datetime.now()
        if self.title == "New Chat" and msg.role == "user" and len(self.messages) == 1:
            self.title = msg.content[:60].strip().replace("\n", " ")

    def get_api_messages(self) -> List[dict]:
        """Build message list suitable for API call, including system prompt."""
        result = []
        if self.system_prompt:
            result.append({"role": "system", "content": self.system_prompt})
        for m in self.messages:
            result.append(m.api_dict())
        return result

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "model": self.model,
            "backend": self.backend,
            "system_prompt": self.system_prompt,
            "messages": [m.to_dict() for m in self.messages],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "parameters": self.parameters,
            "tags": self.tags,
            "agent_id": self.agent_id,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "ChatSession":
        s = cls(
            id=d.get("id", str(uuid.uuid4())),
            title=d.get("title", "Untitled"),
            model=d.get("model", ""),
            backend=d.get("backend", "ollama"),
            system_prompt=d.get("system_prompt", ""),
            messages=[ChatMessage.from_dict(m) for m in d.get("messages", [])],
            parameters=d.get("parameters", {}),
            tags=d.get("tags", []),
            agent_id=d.get("agent_id"),
        )
        for attr in ("created_at", "updated_at"):
            if attr in d:
                try:
                    setattr(s, attr, datetime.fromisoformat(d[attr]))
                except Exception:
                    pass
        return s

    def save(self, directory: Path):
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / f"{self.id}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)

    @classmethod
    def load(cls, path: Path) -> "ChatSession":
        with open(path, "r", encoding="utf-8") as f:
            return cls.from_dict(json.load(f))

    def export_markdown(self) -> str:
        lines = [f"# {self.title}", "", f"**Model:** {self.model}",
                 f"**Date:** {self.created_at.strftime('%Y-%m-%d %H:%M')}", ""]
        if self.system_prompt:
            lines += [f"**System:** {self.system_prompt}", ""]
        for msg in self.messages:
            role_label = {"user": "👤 User", "assistant": "🤖 Assistant",
                          "system": "⚙️ System", "tool": "🔧 Tool"}.get(msg.role, msg.role)
            lines += [f"### {role_label}", msg.content, ""]
        return "\n".join(lines)

    def export_txt(self) -> str:
        lines = [f"Session: {self.title}", f"Model: {self.model}",
                 f"Date: {self.created_at.strftime('%Y-%m-%d %H:%M')}", "=" * 60, ""]
        if self.system_prompt:
            lines += [f"[SYSTEM]: {self.system_prompt}", ""]
        for msg in self.messages:
            ts = msg.timestamp.strftime("%H:%M:%S")
            lines += [f"[{ts}] {msg.role.upper()}:", msg.content, ""]
        return "\n".join(lines)
