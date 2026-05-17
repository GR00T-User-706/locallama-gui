"""
PromptManager — persistent system prompt library.
Prompts stored as JSON files under ~/.llm_studio/prompts/.
"""

import json
import uuid
import logging
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

log = logging.getLogger(__name__)


@dataclass
class PromptEntry:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = "Untitled Prompt"
    content: str = ""
    category: str = "General"
    tags: List[str] = field(default_factory=list)
    favorite: bool = False
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    version: int = 1
    history: List[Dict] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "id": self.id, "title": self.title, "content": self.content,
            "category": self.category, "tags": self.tags,
            "favorite": self.favorite, "created_at": self.created_at,
            "updated_at": self.updated_at, "version": self.version,
            "history": self.history,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "PromptEntry":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})

    def update_content(self, new_content: str):
        self.history.append({"version": self.version, "content": self.content,
                              "updated_at": self.updated_at})
        self.content = new_content
        self.version += 1
        self.updated_at = datetime.now().isoformat()


class PromptManager:
    def __init__(self, prompts_dir: Path):
        self._dir = prompts_dir
        self._dir.mkdir(parents=True, exist_ok=True)
        self._prompts: Dict[str, PromptEntry] = {}
        self._load_all()
        if not self._prompts:
            self._create_defaults()

    def _load_all(self):
        for path in self._dir.glob("*.json"):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    p = PromptEntry.from_dict(json.load(f))
                self._prompts[p.id] = p
            except Exception as e:
                log.warning("Could not load prompt %s: %s", path.name, e)

    def _create_defaults(self):
        defaults = [
            ("Helpful Assistant", "You are a helpful, harmless, and honest assistant.",
             "General"),
            ("Code Expert", "You are an expert software engineer. Write clean, well-documented "
             "code. Explain your reasoning. Use best practices and design patterns.",
             "Coding"),
            ("Socratic Teacher", "You are a Socratic teacher. Ask questions to help the user "
             "discover answers themselves. Don't give direct answers — guide through questioning.",
             "Education"),
            ("Concise Responder", "Respond as concisely as possible. Use bullet points. "
             "No preamble. No fluff.", "General"),
            ("System Analyst", "You are a senior system architect. Analyze problems from "
             "first principles. Consider scalability, reliability, and maintainability.",
             "Technical"),
        ]
        for title, content, category in defaults:
            self.create(title=title, content=content, category=category)

    def _save(self, prompt: PromptEntry):
        path = self._dir / f"{prompt.id}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(prompt.to_dict(), f, indent=2, ensure_ascii=False)

    def create(self, title: str, content: str, category: str = "General",
               tags: List[str] = None) -> PromptEntry:
        p = PromptEntry(title=title, content=content, category=category,
                        tags=tags or [])
        self._prompts[p.id] = p
        self._save(p)
        return p

    def get(self, prompt_id: str) -> Optional[PromptEntry]:
        return self._prompts.get(prompt_id)

    def list_all(self) -> List[PromptEntry]:
        return sorted(self._prompts.values(), key=lambda p: p.title.lower())

    def list_by_category(self, category: str) -> List[PromptEntry]:
        return [p for p in self._prompts.values() if p.category == category]

    def list_favorites(self) -> List[PromptEntry]:
        return [p for p in self._prompts.values() if p.favorite]

    def search(self, query: str) -> List[PromptEntry]:
        q = query.lower()
        return [p for p in self._prompts.values()
                if q in p.title.lower() or q in p.content.lower()
                or any(q in t.lower() for t in p.tags)]

    def update(self, prompt_id: str, title: str = None, content: str = None,
               category: str = None, tags: List[str] = None,
               favorite: bool = None) -> bool:
        p = self._prompts.get(prompt_id)
        if not p:
            return False
        if content is not None and content != p.content:
            p.update_content(content)
        if title is not None:
            p.title = title
        if category is not None:
            p.category = category
        if tags is not None:
            p.tags = tags
        if favorite is not None:
            p.favorite = favorite
        p.updated_at = datetime.now().isoformat()
        self._save(p)
        return True

    def delete(self, prompt_id: str) -> bool:
        p = self._prompts.pop(prompt_id, None)
        if p:
            path = self._dir / f"{prompt_id}.json"
            if path.exists():
                path.unlink()
            return True
        return False

    def get_categories(self) -> List[str]:
        return sorted(set(p.category for p in self._prompts.values()))

    def import_from_file(self, path: Path) -> Optional[PromptEntry]:
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                entries = []
                for item in data:
                    p = PromptEntry.from_dict(item)
                    p.id = str(uuid.uuid4())
                    self._prompts[p.id] = p
                    self._save(p)
                    entries.append(p)
                return entries[0] if entries else None
            else:
                p = PromptEntry.from_dict(data)
                p.id = str(uuid.uuid4())
                self._prompts[p.id] = p
                self._save(p)
                return p
        except Exception as e:
            log.error("Prompt import failed: %s", e)
            return None

    def export_to_file(self, prompt_id: str, path: Path) -> bool:
        p = self._prompts.get(prompt_id)
        if not p:
            return False
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(p.to_dict(), f, indent=2)
            return True
        except Exception as e:
            log.error("Prompt export failed: %s", e)
            return False
