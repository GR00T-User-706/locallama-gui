from __future__ import annotations

from pathlib import Path
from typing import Protocol


from locallama_gui.core.domain import ChatMessage, ChatSession
from locallama_gui.ui.chat_view import message_is_internal_system


class ChatWindowPort(Protocol):
    def current_tab(self): ...
    def set_tab_title(self, title: str) -> None: ...
    def render_tab(self, tab) -> None: ...
    def generate_for_tab(self, tab) -> None: ...
    def refresh_sessions(self) -> None: ...
    def log(self, text: str) -> None: ...
    def open_session(self, session_id: str) -> None: ...


class ChatController:
    def __init__(self, sessions, config, window: ChatWindowPort) -> None:
        self.sessions = sessions
        self.config = config
        self.window = window

    def save_current(self) -> None:
        tab = self.window.current_tab()
        if tab:
            self.sessions.save(tab.session)
            self.window.refresh_sessions()
            self.window.log("Saved chat session")

    def open_chat_file(self, parent) -> None:
        path, _ = __import__("PySide6.QtWidgets", fromlist=["QFileDialog"]).QFileDialog.getOpenFileName(parent, "Open Chat", filter="JSON (*.json)")
        if path:
            session = ChatSession.from_file(Path(path))
            session.save(self.config.paths.sessions_dir)
            self.window.open_session(session.id)

    def send_message(self) -> None:
        tab = self.window.current_tab()
        if not tab:
            return
        text = tab.input.toPlainText().strip()
        if not text:
            return
        tab.input.clear()
        tab.session.messages.append(ChatMessage("user", text))
        tab.session.title = text[:48]
        self.window.set_tab_title(tab.session.title)
        self.window.render_tab(tab)
        self.window.generate_for_tab(tab)

    def regenerate(self) -> None:
        tab = self.window.current_tab()
        if tab and tab.session.messages and tab.session.messages[-1].role == "assistant":
            tab.session.messages.pop()
            self.window.render_tab(tab)
            self.window.generate_for_tab(tab)

    def retry(self) -> None:
        self.regenerate()

    def copy_last_message(self) -> None:
        tab = self.window.current_tab()
        if tab and tab.session.messages:
            __import__("PySide6.QtWidgets", fromlist=["QApplication"]).QApplication.clipboard().setText(tab.session.messages[-1].content)
            self.window.log("Copied last message to clipboard")

    def edit_message(self, parent) -> None:
        tab = self.window.current_tab()
        if not tab or not tab.session.messages:
            return
        visible = [msg for msg in tab.session.messages if not message_is_internal_system(msg)]
        if not visible:
            return
        number, ok = __import__("PySide6.QtWidgets", fromlist=["QInputDialog"]).QInputDialog.getInt(parent, "Edit Message", "Message number:", len(visible), 1, len(visible))
        if not ok:
            return
        msg = visible[number - 1]
        text, ok = __import__("PySide6.QtWidgets", fromlist=["QInputDialog"]).QInputDialog.getMultiLineText(parent, "Edit Message", f"{msg.role} content:", msg.content)
        if ok:
            msg.content = text
            self.window.render_tab(tab)
            self.sessions.save(tab.session)

    def delete_message(self, parent) -> None:
        tab = self.window.current_tab()
        if not tab or not tab.session.messages:
            return
        visible = [msg for msg in tab.session.messages if not message_is_internal_system(msg)]
        if not visible:
            return
        number, ok = __import__("PySide6.QtWidgets", fromlist=["QInputDialog"]).QInputDialog.getInt(parent, "Delete Message", "Message number:", len(visible), 1, len(visible))
        if ok:
            message = visible[number - 1]
            tab.session.messages.remove(message)
            self.window.render_tab(tab)
            self.sessions.save(tab.session)
