from __future__ import annotations

from PySide6.QtWidgets import QLabel, QTextEdit, QVBoxLayout, QWidget


class Plugin:
    manifest = {
        "id": "sample_plugin",
        "name": "Sample Productivity Plugin",
        "version": "1.0.0",
        "description": "Adds a command, a chat interceptor, a tool, and a custom dock panel.",
    }

    def __init__(self) -> None:
        self._active = False

    def activate(self, context) -> None:
        self._active = True
        context.register_tool("uppercase", lambda text: str(text).upper())
        context.register_command("insert_timestamp", lambda: context.main_window.terminal.appendPlainText("Timestamp command executed"))
        context.register_chat_interceptor(self.add_metadata)
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.addWidget(QLabel("Sample plugin panel"))
        note = QTextEdit()
        note.setPlaceholderText("Plugin-provided scratchpad")
        layout.addWidget(note)
        context.add_panel("Sample Plugin", panel)

    def deactivate(self) -> None:
        self._active = False

    def add_metadata(self, messages):
        return messages
