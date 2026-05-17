"""
Data models for chat messages and sessions.
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Any, Dict


@dataclass
class ChatMessage:
    role: str                        # system | user | assistant | tool
    content: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    model: str = ""
    tokens: int = 0                  # token count if available
    duration_ms: int = 0             # generation duration
    tool_calls: List[Dict] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "model": self.model,
            "tokens": self.tokens,
            "duration_ms": self.duration_ms,
            "tool_calls": self.tool_calls,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "ChatMessage":
        msg = cls(
            role=d["role"],
            content=d.get("content", ""),
            id=d.get("id", str(uuid.uuid4())),
            model=d.get("model", ""),
            tokens=d.get("tokens", 0),
            duration_ms=d.get("duration_ms", 0),
            tool_calls=d.get("tool_calls", []),
            metadata=d.get("metadata", {}),
        )
        if "timestamp" in d:
            try:
                msg.timestamp = datetime.fromisoformat(d["timestamp"])
            except Exception:
                pass
        return msg

    def api_dict(self) -> dict:
        """Minimal dict for LLM API requests."""
        d = {"role": self.role, "content": self.content}
        if self.tool_calls:
            d["tool_calls"] = self.tool_calls
        return d
