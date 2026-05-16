from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any
from dataclasses import asdict

import psutil
from PySide6.QtCore import QByteArray, Qt
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDockWidget,
    QFileDialog,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QSplitter,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QToolBar,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from locallama_gui.backends.manager import create_backend
from locallama_gui.core.config import AppConfig
from locallama_gui.core.domain import ChatMessage, ChatSession, ModelInfo
from locallama_gui.core.managers import AgentManager, PluginContext, PluginManager, PromptManager, SessionManager
from locallama_gui.ui.dialogs import AgentBuilderDialog, EndpointDialog, ModelfileEditor, ParameterDialog, PluginManagerDialog, PromptManagerDialog
from locallama_gui.ui.theme import DARK_QSS
from locallama_gui.ui.workers import AsyncTask, StreamTask

LOG = logging.getLogger(__name__)


class ChatTab(QWidget):
    def __init__(self, session: ChatSession) -> None:
        super().__init__()
        self.session = session
        self.chat = QTextEdit(); self.chat.setReadOnly(True)
        self.input = QPlainTextEdit(); self.input.setPlaceholderText("Write a message. Ctrl+Enter sends."); self.input.setMaximumHeight(140)
        self.streaming = QCheckBox("Stream"); self.streaming.setChecked(True)
        self.send = QPushButton("Send"); self.stop = QPushButton("Stop"); self.regen = QPushButton("Regenerate"); self.retry = QPushButton("Retry")
        self.copy_last = QPushButton("Copy Last"); self.edit_msg = QPushButton("Edit Message"); self.delete_msg = QPushButton("Delete Message")
        row = QHBoxLayout(); row.addWidget(self.streaming); row.addStretch(); row.addWidget(self.copy_last); row.addWidget(self.edit_msg); row.addWidget(self.delete_msg); row.addWidget(self.retry); row.addWidget(self.regen); row.addWidget(self.stop); row.addWidget(self.send)
        layout = QVBoxLayout(self); layout.setContentsMargins(6, 6, 6, 6); layout.addWidget(self.chat); layout.addWidget(self.input); layout.addLayout(row)
        self.render()

    def render(self) -> None:
        html = []
        colors = {"system": "#8fbcbb", "user": "#a3be8c", "assistant": "#81a1c1", "tool": "#d08770"}
        for idx, msg in enumerate(self.session.messages):
            safe = msg.content.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
            html.append(f"<div style='margin:8px 0;padding:8px;border-left:3px solid {colors.get(msg.role, '#ccc')};background:#171a21'><b>{idx+1}. {msg.role}</b><br>{safe}</div>")
        self.chat.setHtml("".join(html))
        self.chat.verticalScrollBar().setValue(self.chat.verticalScrollBar().maximum())


class MainWindow(QMainWindow):
    def __init__(self, config: AppConfig) -> None:
        super().__init__()
        self.config = config
        self.setWindowTitle("LocalLama Control Center")
        self.resize(1440, 900)
        self.setStyleSheet(DARK_QSS)
        self.sessions = SessionManager(config)
        self.prompts = PromptManager(config)
        self.agents = AgentManager(config)
        self.plugin_context = PluginContext(self, config)
        self.plugins = PluginManager(config, self.plugin_context)
        self.models: list[ModelInfo] = []
        self.worker_refs: list[Any] = []
        self.current_stream: StreamTask | None = None
        self._build_ui()
        self._build_menus()
        self._restore_state()
        self.plugins.load_enabled()
        self.new_chat()
        self.refresh_backend()

    def _build_ui(self) -> None:
        self.tabs = QTabWidget(); self.tabs.setTabsClosable(True); self.tabs.tabCloseRequested.connect(self.close_tab); self.setCentralWidget(self.tabs)
        self.status = self.statusBar(); self.status.showMessage("Disconnected")
        self.toolbar = QToolBar("Main"); self.addToolBar(self.toolbar)
        for label, slot in [("New Chat", self.new_chat), ("Save", self.save_current), ("Refresh Models", self.refresh_backend), ("Parameters", self.open_parameters), ("Plugins", self.open_plugins)]:
            action = QAction(label, self); action.triggered.connect(slot); self.toolbar.addAction(action)
        self.provider_combo = QComboBox(); self.provider_combo.addItems([p.name for p in self.config.provider_profiles]); self.provider_combo.setCurrentText(self.config.active_provider); self.provider_combo.currentTextChanged.connect(self.switch_provider); self.toolbar.addWidget(QLabel(" Provider ")); self.toolbar.addWidget(self.provider_combo)
        self.model_combo = QComboBox(); self.model_combo.currentTextChanged.connect(self.model_changed); self.toolbar.addWidget(QLabel(" Model ")); self.toolbar.addWidget(self.model_combo)
        self._create_docks()

    def _create_docks(self) -> None:
        self.model_table = QTableWidget(0, 8); self.model_table.setHorizontalHeaderLabels(["Name", "Size", "Quant", "Params", "Ctx", "Backend", "RAM/VRAM", "Metadata"])
        self._dock("Models", self.model_table, Qt.DockWidgetArea.LeftDockWidgetArea)
        self.sessions_list = QListWidget(); self.sessions_list.itemDoubleClicked.connect(lambda item: self.open_session(item.data(Qt.ItemDataRole.UserRole)))
        self._dock("Chat Sessions", self.sessions_list, Qt.DockWidgetArea.LeftDockWidgetArea)
        self.prompt_list = QListWidget(); self.prompt_list.itemDoubleClicked.connect(self.apply_prompt_item); self._dock("System Prompts", self.prompt_list, Qt.DockWidgetArea.RightDockWidgetArea)
        self.log_view = QPlainTextEdit(); self.log_view.setReadOnly(True); self._dock("Logs", self.log_view, Qt.DockWidgetArea.BottomDockWidgetArea)
        self.request_view = QPlainTextEdit(); self.request_view.setReadOnly(True); self._dock("Request Viewer", self.request_view, Qt.DockWidgetArea.BottomDockWidgetArea)
        self.token_view = QPlainTextEdit(); self.token_view.setReadOnly(True); self._dock("Token Viewer", self.token_view, Qt.DockWidgetArea.BottomDockWidgetArea)
        self.terminal = QPlainTextEdit(); self.terminal.setReadOnly(True); self.terminal.setPlainText("LocalLama diagnostics terminal. Menu actions append operational output here.\n"); self._dock("Terminal", self.terminal, Qt.DockWidgetArea.BottomDockWidgetArea)
        self.refresh_sessions(); self.refresh_prompts()

    def _dock(self, title: str, widget: QWidget, area: Qt.DockWidgetArea) -> QDockWidget:
        dock = QDockWidget(title, self); dock.setWidget(widget); dock.setObjectName(title); self.addDockWidget(area, dock); return dock

    def add_plugin_panel(self, title: str, widget: QWidget, area: Any = None) -> None:
        self._dock(title, widget, area or Qt.DockWidgetArea.RightDockWidgetArea)

    def _build_menus(self) -> None:
        def act(menu, text, slot, shortcut: str | None = None):
            a = QAction(text, self); a.triggered.connect(slot)
            if shortcut: a.setShortcut(QKeySequence(shortcut))
            menu.addAction(a); return a
        file = self.menuBar().addMenu("File"); act(file, "New Chat", self.new_chat, "Ctrl+N"); act(file, "Open Chat", self.open_chat_file, "Ctrl+O"); act(file, "Save", self.save_current, "Ctrl+S"); act(file, "Save As", self.save_as); act(file, "Export", self.export_current); act(file, "Import", self.import_chat); file.addSeparator(); act(file, "Exit", self.close, "Ctrl+Q")
        models = self.menuBar().addMenu("Models"); act(models, "Pull", self.pull_model); act(models, "Push", self.push_model); act(models, "Clone", self.clone_model); act(models, "Create", self.create_model); act(models, "Delete", self.delete_model); act(models, "Modelfiles", self.open_modelfile_editor); act(models, "Templates", self.open_template_viewer)
        agents = self.menuBar().addMenu("Agents"); act(agents, "Create", self.open_agent_builder); act(agents, "Manage", self.open_agent_builder); act(agents, "Import", self.import_agent); act(agents, "Export", self.export_agent)
        plugins = self.menuBar().addMenu("Plugins"); act(plugins, "Plugin Manager", self.open_plugins); act(plugins, "Install", self.install_plugin); act(plugins, "Reload", self.reload_plugins); act(plugins, "Developer Mode", self.open_plugin_docs)
        settings = self.menuBar().addMenu("Settings"); act(settings, "API Endpoints", self.open_endpoints); act(settings, "Parameters", self.open_parameters); act(settings, "Themes", self.toggle_theme); act(settings, "Keyboard Shortcuts", self.show_shortcuts); act(settings, "Model Settings", self.refresh_backend)
        view = self.menuBar().addMenu("View"); act(view, "Toggle Panels", self.toggle_all_docks); act(view, "Layout Presets", self.reset_layout); act(view, "Logs", lambda: self.log_view.parent().show()); act(view, "Terminal", lambda: self.terminal.parent().show())
        dev = self.menuBar().addMenu("Developer"); act(dev, "Logs", lambda: self.log_view.parent().show()); act(dev, "Request Viewer", lambda: self.request_view.parent().show()); act(dev, "Token Viewer", lambda: self.token_view.parent().show()); act(dev, "API Inspector", self.inspect_api); act(dev, "Debug Console", lambda: self.terminal.parent().show())
        helpm = self.menuBar().addMenu("Help"); act(helpm, "Documentation", self.open_docs); act(helpm, "About", self.about); act(helpm, "Diagnostics", self.diagnostics)

    def current_tab(self) -> ChatTab | None:
        w = self.tabs.currentWidget(); return w if isinstance(w, ChatTab) else None

    def new_chat(self) -> None:
        session = ChatSession(provider=self.config.active_provider, model=self.model_combo.currentText(), system_prompt=self.config.global_system_prompt)
        if session.system_prompt:
            session.messages.append(ChatMessage("system", session.system_prompt))
        tab = ChatTab(session); self._wire_chat_tab(tab); self.tabs.addTab(tab, session.title); self.tabs.setCurrentWidget(tab)


    def _wire_chat_tab(self, tab: ChatTab) -> None:
        tab.send.clicked.connect(self.send_message)
        tab.stop.clicked.connect(self.stop_generation)
        tab.regen.clicked.connect(self.regenerate)
        tab.retry.clicked.connect(self.retry)
        tab.copy_last.clicked.connect(self.copy_last_message)
        tab.edit_msg.clicked.connect(self.edit_message)
        tab.delete_msg.clicked.connect(self.delete_message)

    def copy_last_message(self) -> None:
        tab = self.current_tab()
        if tab and tab.session.messages:
            QApplication.clipboard().setText(tab.session.messages[-1].content)
            self.log("Copied last message to clipboard")

    def edit_message(self) -> None:
        tab = self.current_tab()
        if not tab or not tab.session.messages:
            return
        number, ok = QInputDialog.getInt(self, "Edit Message", "Message number:", len(tab.session.messages), 1, len(tab.session.messages))
        if not ok:
            return
        msg = tab.session.messages[number - 1]
        text, ok = QInputDialog.getMultiLineText(self, "Edit Message", f"{msg.role} content:", msg.content)
        if ok:
            msg.content = text
            tab.render()
            self.sessions.save(tab.session)

    def delete_message(self) -> None:
        tab = self.current_tab()
        if not tab or not tab.session.messages:
            return
        number, ok = QInputDialog.getInt(self, "Delete Message", "Message number:", len(tab.session.messages), 1, len(tab.session.messages))
        if ok:
            del tab.session.messages[number - 1]
            tab.render()
            self.sessions.save(tab.session)

    def close_tab(self, idx: int) -> None:
        if self.tabs.count() > 1: self.tabs.removeTab(idx)

    def send_message(self) -> None:
        tab = self.current_tab()
        if not tab: return
        text = tab.input.toPlainText().strip()
        if not text: return
        tab.input.clear(); tab.session.messages.append(ChatMessage("user", text)); tab.session.title = text[:48]; self.tabs.setTabText(self.tabs.currentIndex(), tab.session.title); tab.render(); self._generate(tab)

    def _generate(self, tab: ChatTab) -> None:
        profile = self.config.active_profile(); backend = create_backend(profile); model = self.model_combo.currentText() or profile.default_model
        if not model:
            QMessageBox.warning(self, "No model", "Select or configure a model before generating."); return
        tab.session.model = model; tab.session.provider = profile.name
        messages = list(tab.session.messages)
        for interceptor in self.plugin_context.chat_interceptors:
            messages = interceptor(messages)
        self.request_view.setPlainText(json.dumps({"provider": profile.name, "url": profile.base_url, "model": model, "messages": [asdict(m) for m in messages], "options": self.config.parameters.to_backend_options()}, indent=2, default=str))
        self.status.showMessage("generating" if not tab.streaming.isChecked() else "streaming")
        assistant = ChatMessage("assistant", ""); tab.session.messages.append(assistant); tab.render()
        task = StreamTask(lambda: backend.chat(model, messages, self.config.parameters.to_backend_options(), tab.streaming.isChecked()))
        self.current_stream = task; self.worker_refs.append(task)
        task.token.connect(lambda tok: self._append_token(tab, assistant, tok)); task.error.connect(self._stream_error); task.completed.connect(lambda _: self._stream_done(tab))
        task.start()

    def _append_token(self, tab: ChatTab, msg: ChatMessage, token: str) -> None:
        msg.content += token; self.token_view.insertPlainText(token); tab.render()

    def _stream_error(self, error: str) -> None:
        self.status.showMessage("idle"); self.log(f"Generation error: {error}"); QMessageBox.critical(self, "Generation Error", error)

    def _stream_done(self, tab: ChatTab) -> None:
        self.status.showMessage("idle"); self.sessions.save(tab.session); self.refresh_sessions(); tab.render()

    def stop_generation(self) -> None:
        if self.current_stream: self.current_stream.cancel(); self.status.showMessage("idle")

    def regenerate(self) -> None:
        tab = self.current_tab()
        if tab and tab.session.messages and tab.session.messages[-1].role == "assistant": tab.session.messages.pop(); tab.render(); self._generate(tab)

    def retry(self) -> None: self.regenerate()
    def model_changed(self, text: str) -> None:
        tab = self.current_tab()
        if tab: tab.session.model = text

    def refresh_backend(self) -> None:
        profile = self.config.active_profile(); self.status.showMessage(f"testing {profile.base_url}")
        backend = create_backend(profile)
        async def work():
            status = await backend.test_connection(); models = await backend.list_models() if status.state == "connected" else [] ; return status, models
        task = AsyncTask(work); self.worker_refs.append(task); task.result.connect(self._backend_refreshed); task.error.connect(lambda e: self.log(f"Backend refresh error: {e}")); task.start()

    def _backend_refreshed(self, result: Any) -> None:
        status, self.models = result; self.status.showMessage(f"{status.state} | {status.latency_ms:.0f} ms | {self.config.active_profile().base_url}"); self.log(f"Backend {status.state}: {status.detail}")
        self.model_combo.blockSignals(True); self.model_combo.clear(); self.model_combo.addItems([m.name for m in self.models]); self.model_combo.blockSignals(False)
        self.model_table.setRowCount(0)
        for m in self.models:
            r = self.model_table.rowCount(); self.model_table.insertRow(r)
            ram = m.size_display if m.size else "backend reported"
            vals = [m.name, m.size_display, m.quantization, m.parameter_size, str(m.context_size or ""), m.backend, ram, json.dumps(m.metadata)[:400]]
            for c, v in enumerate(vals): self.model_table.setItem(r, c, QTableWidgetItem(v))

    def switch_provider(self, name: str) -> None:
        self.config.active_provider = name; self.config.save(); self.refresh_backend()

    def refresh_sessions(self) -> None:
        self.sessions_list.clear()
        for s in self.sessions.list_sessions():
            item = QTreeWidgetItem() if False else None
            self.sessions_list.addItem(f"{s.updated_at[:19]}  {s.title}"); self.sessions_list.item(self.sessions_list.count()-1).setData(Qt.ItemDataRole.UserRole, s.id)

    def refresh_prompts(self) -> None:
        self.prompt_list.clear()
        for p in self.prompts.list():
            self.prompt_list.addItem(("★ " if p.favorite else "") + f"{p.category}: {p.title}"); self.prompt_list.item(self.prompt_list.count()-1).setData(Qt.ItemDataRole.UserRole, p.content)

    def apply_prompt_item(self, item) -> None:
        tab = self.current_tab()
        if not tab: return
        content = item.data(Qt.ItemDataRole.UserRole); tab.session.system_prompt = content
        if tab.session.messages and tab.session.messages[0].role == "system": tab.session.messages[0].content = content
        else: tab.session.messages.insert(0, ChatMessage("system", content))
        tab.render()

    def save_current(self) -> None:
        tab = self.current_tab();
        if tab: self.sessions.save(tab.session); self.refresh_sessions(); self.log("Saved chat session")

    def save_as(self) -> None:
        tab = self.current_tab();
        if not tab: return
        path, _ = QFileDialog.getSaveFileName(self, "Save Chat As", f"{tab.session.title}.json", "JSON (*.json)")
        if path: Path(path).write_text(tab.session.to_json(), encoding="utf-8")

    def open_session(self, session_id: str) -> None:
        session = self.sessions.load(session_id); tab = ChatTab(session); self._wire_chat_tab(tab); self.tabs.addTab(tab, session.title); self.tabs.setCurrentWidget(tab)

    def open_chat_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Open Chat", filter="JSON (*.json)")
        if path:
            session = ChatSession.from_file(Path(path)); session.save(self.config.paths.sessions_dir); self.open_session(session.id)

    def import_chat(self) -> None: self.open_chat_file()
    def export_current(self) -> None:
        tab = self.current_tab();
        if not tab: return
        path, selected = QFileDialog.getSaveFileName(self, "Export Chat", f"{tab.session.title}.md", "Markdown (*.md);;JSON (*.json);;Text (*.txt)")
        if not path: return
        p = Path(path)
        content = tab.session.to_json() if p.suffix == ".json" else tab.session.export_text() if p.suffix == ".txt" else tab.session.export_markdown()
        p.write_text(content, encoding="utf-8")

    def pull_model(self) -> None: self._model_stream_op("Pull model", "pull_model")
    def push_model(self) -> None: self._model_stream_op("Push model", "push_model")
    def create_model(self) -> None: self.open_modelfile_editor()
    def clone_model(self) -> None:
        source = self.model_combo.currentText(); dest, ok = QInputDialog.getText(self, "Clone Model", "Destination model name:")
        if ok and source and dest: self._async(lambda: create_backend(self.config.active_profile()).copy_model(source, dest), "Model cloned")
    def delete_model(self) -> None:
        name = self.model_combo.currentText()
        if name and QMessageBox.question(self, "Delete", f"Delete {name}?") == QMessageBox.StandardButton.Yes: self._async(lambda: create_backend(self.config.active_profile()).delete_model(name), "Model deleted")
    def _model_stream_op(self, title: str, method: str) -> None:
        name, ok = QInputDialog.getText(self, title, "Model name:", text=self.model_combo.currentText())
        if not ok or not name: return
        backend = create_backend(self.config.active_profile()); task = StreamTask(lambda: getattr(backend, method)(name)); self.worker_refs.append(task); task.token.connect(lambda t: self.terminal.insertPlainText(t + "\n")); task.completed.connect(lambda _: self.refresh_backend()); task.error.connect(lambda e: QMessageBox.critical(self, title, e)); task.start()

    def _async(self, coro_factory, done_msg: str) -> None:
        task = AsyncTask(coro_factory); self.worker_refs.append(task); task.finished_ok.connect(lambda: (self.log(done_msg), self.refresh_backend())); task.error.connect(lambda e: QMessageBox.critical(self, "Error", e)); task.start()

    def open_modelfile_editor(self) -> None: ModelfileEditor(self.config, self).exec()

    def build_model_from_modelfile(self, name: str, modelfile: str) -> None:
        if not name.strip():
            QMessageBox.warning(self, "Create Model", "Model name is required.")
            return
        backend = create_backend(self.config.active_profile())
        task = StreamTask(lambda: backend.create_model(name.strip(), modelfile))
        self.worker_refs.append(task)
        task.token.connect(lambda t: self.terminal.insertPlainText(t + "\n"))
        task.completed.connect(lambda _: self.refresh_backend())
        task.error.connect(lambda e: QMessageBox.critical(self, "Create Model", e))
        task.start()
    def open_template_viewer(self) -> None:
        model = self.model_combo.currentText();
        if not model: return
        async def show(): return await create_backend(self.config.active_profile()).show_model(model)
        task = AsyncTask(show); self.worker_refs.append(task); task.result.connect(lambda data: self._show_text_dialog("Template Viewer", json.dumps(data, indent=2))); task.error.connect(lambda e: QMessageBox.critical(self, "Template Viewer", e)); task.start()
    def _show_text_dialog(self, title: str, text: str) -> None:
        d = QMessageBox(self); d.setWindowTitle(title); d.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse); d.setDetailedText(text); d.setText(text[:1000]); d.exec()

    def open_endpoints(self) -> None:
        if EndpointDialog(self.config, self).exec(): self.provider_combo.clear(); self.provider_combo.addItems([p.name for p in self.config.provider_profiles]); self.refresh_backend()
    def open_parameters(self) -> None: ParameterDialog(self.config, self).exec()
    def open_plugins(self) -> None: PluginManagerDialog(self.plugins, self).exec()
    def reload_plugins(self) -> None: self.plugins.reload(); self.log("Plugins reloaded")
    def install_plugin(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Install Plugin", filter="Python (*.py)")
        if path:
            dest = self.config.paths.plugins_dir / Path(path).name; dest.write_text(Path(path).read_text(encoding="utf-8"), encoding="utf-8"); self.log(f"Installed plugin {dest}")
    def open_plugin_docs(self) -> None: self._show_text_dialog("Plugin SDK", (Path.cwd()/"docs"/"PLUGIN_SDK.md").read_text(encoding="utf-8"))
    def open_agent_builder(self) -> None: AgentBuilderDialog(self.agents, [m.name for m in self.models], list(self.plugins.loaded), self).exec()
    def import_agent(self) -> None: self.open_agent_builder()
    def export_agent(self) -> None: self.open_agent_builder()
    def toggle_theme(self) -> None: self.setStyleSheet("" if self.styleSheet() else DARK_QSS)
    def show_shortcuts(self) -> None: self._show_text_dialog("Keyboard Shortcuts", "Ctrl+N New Chat\nCtrl+O Open Chat\nCtrl+S Save\nCtrl+Q Exit\nCtrl+Enter Send from composer")
    def toggle_all_docks(self) -> None:
        docks = self.findChildren(QDockWidget); visible = not all(d.isVisible() for d in docks)
        for d in docks: d.setVisible(visible)
    def reset_layout(self) -> None:
        for d in self.findChildren(QDockWidget): d.show()
    def inspect_api(self) -> None: self.request_view.parent().show(); self.request_view.setFocus()
    def open_docs(self) -> None: self._show_text_dialog("Documentation", (Path.cwd()/"README.md").read_text(encoding="utf-8")[:12000])
    def about(self) -> None: QMessageBox.about(self, "About", "LocalLama Control Center\nA PySide6 IDE-grade desktop application for local and remote LLMs.")
    def diagnostics(self) -> None:
        mem = psutil.virtual_memory(); self.terminal.appendPlainText(f"CPU cores: {psutil.cpu_count()}\nRAM: {mem.available/1024**3:.1f} GiB available / {mem.total/1024**3:.1f} GiB total\nConfig: {self.config.file_path}\nData: {self.config.paths.data_dir}\nLogs: {self.config.paths.logs_dir}\n")
    def log(self, text: str) -> None: LOG.info(text); self.log_view.appendPlainText(text)
    def _restore_state(self) -> None:
        if self.config.ui.geometry_hex: self.restoreGeometry(QByteArray.fromHex(self.config.ui.geometry_hex.encode()))
        if self.config.ui.state_hex: self.restoreState(QByteArray.fromHex(self.config.ui.state_hex.encode()))
    def closeEvent(self, event) -> None:
        self.config.ui.geometry_hex = bytes(self.saveGeometry().toHex()).decode(); self.config.ui.state_hex = bytes(self.saveState().toHex()).decode(); self.config.save(); super().closeEvent(event)
