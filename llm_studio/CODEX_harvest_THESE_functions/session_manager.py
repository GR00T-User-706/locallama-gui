"""
SessionManager — manages chat sessions lifecycle.
Sessions are JSON files under ~/.llm_studio/sessions/.
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional

from app.models.session import ChatSession
from app.models.chat_message import ChatMessage

log = logging.getLogger(__name__)


class SessionManager:
    def __init__(self, sessions_dir: Path):
        self._dir = sessions_dir
        self._dir.mkdir(parents=True, exist_ok=True)
        self._sessions: Dict[str, ChatSession] = {}
        self._load_all()

    def _load_all(self):
        for path in sorted(self._dir.glob("*.json"),
                           key=lambda p: p.stat().st_mtime, reverse=True):
            try:
                s = ChatSession.load(path)
                self._sessions[s.id] = s
            except Exception as e:
                log.warning("Could not load session %s: %s", path.name, e)
        log.debug("Loaded %d sessions from disk.", len(self._sessions))

    # ── CRUD ──────────────────────────────────────────────────────────────

    def new_session(self, model: str = "", backend: str = "ollama",
                    system_prompt: str = "") -> ChatSession:
        s = ChatSession(model=model, backend=backend, system_prompt=system_prompt)
        self._sessions[s.id] = s
        self._save(s)
        return s

    def get(self, session_id: str) -> Optional[ChatSession]:
        return self._sessions.get(session_id)

    def list_sessions(self) -> List[ChatSession]:
        return sorted(self._sessions.values(),
                      key=lambda s: s.updated_at, reverse=True)

    def save_session(self, session: ChatSession):
        self._sessions[session.id] = session
        self._save(session)

    def delete_session(self, session_id: str) -> bool:
        session = self._sessions.pop(session_id, None)
        if session:
            path = self._dir / f"{session_id}.json"
            if path.exists():
                path.unlink()
            return True
        return False

    def _save(self, session: ChatSession):
        try:
            session.save(self._dir)
        except Exception as e:
            log.error("Failed to save session %s: %s", session.id, e)

    # ── Message helpers ───────────────────────────────────────────────────

    def append_message(self, session_id: str, msg: ChatMessage) -> bool:
        s = self._sessions.get(session_id)
        if s:
            s.add_message(msg)
            self._save(s)
            return True
        return False

    def update_last_assistant(self, session_id: str, content: str):
        """Update the content of the last assistant message (for streaming)."""
        s = self._sessions.get(session_id)
        if s:
            for msg in reversed(s.messages):
                if msg.role == "assistant":
                    msg.content = content
                    self._save(s)
                    return

    def delete_message(self, session_id: str, message_id: str) -> bool:
        s = self._sessions.get(session_id)
        if s:
            before = len(s.messages)
            s.messages = [m for m in s.messages if m.id != message_id]
            if len(s.messages) < before:
                self._save(s)
                return True
        return False

    def update_message(self, session_id: str, message_id: str,
                       content: str) -> bool:
        s = self._sessions.get(session_id)
        if s:
            for m in s.messages:
                if m.id == message_id:
                    m.content = content
                    self._save(s)
                    return True
        return False

    def duplicate_session(self, session_id: str) -> Optional[ChatSession]:
        src = self._sessions.get(session_id)
        if not src:
            return None
        import copy, uuid
        new_s = copy.deepcopy(src)
        new_s.id = str(uuid.uuid4())
        new_s.title = f"{src.title} (copy)"
        self._sessions[new_s.id] = new_s
        self._save(new_s)
        return new_s

    def import_session(self, path: Path) -> ChatSession:
        s = ChatSession.load(path)
        self._sessions[s.id] = s
        self._save(s)
        return s

    def export_session(self, session_id: str, path: Path,
                       fmt: str = "json") -> bool:
        s = self._sessions.get(session_id)
        if not s:
            return False
        try:
            if fmt == "json":
                import json
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(s.to_dict(), f, indent=2, ensure_ascii=False)
            elif fmt == "markdown":
                path.write_text(s.export_markdown(), encoding="utf-8")
            elif fmt == "txt":
                path.write_text(s.export_txt(), encoding="utf-8")
            return True
        except Exception as e:
            log.error("Export failed: %s", e)
            return False
