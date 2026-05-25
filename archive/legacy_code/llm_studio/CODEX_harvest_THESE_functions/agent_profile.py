"""Agent profile data model."""

import uuid
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Any, Optional


@dataclass
class AgentProfile:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "New Agent"
    description: str = ""
    model: str = ""
    backend: str = "ollama"
    system_prompt: str = ""
    system_prompt_id: Optional[str] = None
    tools: List[str] = field(default_factory=list)       # plugin tool ids
    plugins: List[str] = field(default_factory=list)     # enabled plugin ids
    memory_mode: str = "none"        # none | session | persistent
    reasoning_mode: str = "normal"   # normal | thinking | plan
    execution_mode: str = "executor" # planner | executor | autonomous | constrained
    parameters: Dict[str, Any] = field(default_factory=dict)
    template: str = ""
    icon: str = "🤖"
    tags: List[str] = field(default_factory=list)
    created_at: str = ""
    updated_at: str = ""

    def to_dict(self) -> dict:
        from datetime import datetime
        return {
            "id": self.id, "name": self.name, "description": self.description,
            "model": self.model, "backend": self.backend,
            "system_prompt": self.system_prompt,
            "system_prompt_id": self.system_prompt_id,
            "tools": self.tools, "plugins": self.plugins,
            "memory_mode": self.memory_mode,
            "reasoning_mode": self.reasoning_mode,
            "execution_mode": self.execution_mode,
            "parameters": self.parameters, "template": self.template,
            "icon": self.icon, "tags": self.tags,
            "created_at": self.created_at or datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }

    @classmethod
    def from_dict(cls, d: dict) -> "AgentProfile":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})

    def save(self, directory: Path):
        directory.mkdir(parents=True, exist_ok=True)
        with open(directory / f"{self.id}.json", "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load(cls, path: Path) -> "AgentProfile":
        with open(path, "r", encoding="utf-8") as f:
            return cls.from_dict(json.load(f))
