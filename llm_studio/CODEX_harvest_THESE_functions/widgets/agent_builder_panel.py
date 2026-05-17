"""
Agent Builder Panel — visual agent profile editor.
"""

import logging
from typing import Optional, List

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QListWidget, QListWidgetItem, QLineEdit, QComboBox,
    QPlainTextEdit, QCheckBox, QGroupBox, QFormLayout,
    QSplitter, QFileDialog, QMessageBox, QScrollArea,
    QButtonGroup, QRadioButton, QTabWidget, QFrame,
)

from app.core.agent_manager import AgentManager
from app.models.agent_profile import AgentProfile
from app.core.prompt_manager import PromptManager

log = logging.getLogger(__name__)


class AgentBuilderPanel(QWidget):
    """Visual agent builder and manager."""

    agent_chat_requested = Signal(object)   # AgentProfile

    def __init__(self, agent_manager: AgentManager,
                 prompt_manager: PromptManager,
                 app_state, parent=None):
        super().__init__(parent)
        self.am = agent_manager
        self.pm = prompt_manager
        self.app_state = app_state
        self._selected: Optional[AgentProfile] = None
        self._setup_ui()
        self._refresh_list()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Toolbar
        toolbar = QWidget()
        toolbar.setStyleSheet("background:#181825; border-bottom:1px solid #313244;")
        toolbar.setFixedHeight(42)
        tb = QHBoxLayout(toolbar)
        tb.setContentsMargins(8, 4, 8, 4)
        tb.setSpacing(6)

        btn_new = QPushButton("⊕ New Agent")
        btn_new.setObjectName("primaryButton")
        btn_new.clicked.connect(self._on_new)
        btn_import = QPushButton("⇓ Import")
        btn_import.clicked.connect(self._on_import)
        btn_export = QPushButton("⇑ Export")
        btn_export.clicked.connect(self._on_export)

        tb.addWidget(btn_new)
        tb.addWidget(btn_import)
        tb.addWidget(btn_export)
        tb.addStretch()

        layout.addWidget(toolbar)

        # Main splitter: list | editor
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # ── Agent list ─────────────────────────────────────────────────────
        list_widget = QWidget()
        list_layout = QVBoxLayout(list_widget)
        list_layout.setContentsMargins(6, 6, 6, 6)
        list_layout.setSpacing(4)

        list_layout.addWidget(QLabel("Agents:"))
        self._list = QListWidget()
        self._list.currentRowChanged.connect(self._on_selection_changed)
        list_layout.addWidget(self._list, stretch=1)

        agent_btns = QHBoxLayout()
        btn_chat = QPushButton("▶ Chat")
        btn_chat.setObjectName("primaryButton")
        btn_chat.clicked.connect(self._on_chat_with_agent)
        btn_dup = QPushButton("⧉")
        btn_dup.setToolTip("Duplicate agent")
        btn_dup.setFixedWidth(30)
        btn_dup.clicked.connect(self._on_duplicate)
        btn_del = QPushButton("✕")
        btn_del.setObjectName("dangerButton")
        btn_del.setFixedWidth(30)
        btn_del.clicked.connect(self._on_delete)
        agent_btns.addWidget(btn_chat)
        agent_btns.addStretch()
        agent_btns.addWidget(btn_dup)
        agent_btns.addWidget(btn_del)
        list_layout.addLayout(agent_btns)

        splitter.addWidget(list_widget)

        # ── Agent editor ───────────────────────────────────────────────────
        editor_scroll = QScrollArea()
        editor_scroll.setWidgetResizable(True)
        editor_scroll.setStyleSheet("QScrollArea { border:none; }")

        editor = QWidget()
        editor_layout = QVBoxLayout(editor)
        editor_layout.setContentsMargins(10, 10, 10, 10)
        editor_layout.setSpacing(10)

        # Identity
        identity_group = QGroupBox("Identity")
        id_form = QFormLayout(identity_group)
        id_form.setSpacing(6)

        icon_layout = QHBoxLayout()
        self._icon_edit = QLineEdit("🤖")
        self._icon_edit.setFixedWidth(48)
        icon_lbl = QLabel("(emoji)")
        icon_lbl.setObjectName("dimLabel")
        icon_layout.addWidget(self._icon_edit)
        icon_layout.addWidget(icon_lbl)
        icon_layout.addStretch()

        self._name_edit = QLineEdit()
        self._name_edit.setPlaceholderText("Agent name…")
        self._desc_edit = QPlainTextEdit()
        self._desc_edit.setPlaceholderText("Brief description of this agent…")
        self._desc_edit.setFixedHeight(60)

        id_form.addRow("Icon:", icon_layout)
        id_form.addRow("Name:", self._name_edit)
        id_form.addRow("Description:", self._desc_edit)

        editor_layout.addWidget(identity_group)

        # Model
        model_group = QGroupBox("Model")
        model_form = QFormLayout(model_group)
        model_form.setSpacing(6)

        self._model_combo = QComboBox()
        self._model_combo.setEditable(True)
        models = self.app_state.get_model_names()
        self._model_combo.addItems(models)

        self._backend_combo = QComboBox()
        self._backend_combo.addItems(["ollama", "openai"])

        model_form.addRow("Model:", self._model_combo)
        model_form.addRow("Backend:", self._backend_combo)
        editor_layout.addWidget(model_group)

        # System Prompt
        prompt_group = QGroupBox("System Prompt")
        prompt_layout = QVBoxLayout(prompt_group)

        prompt_selector = QHBoxLayout()
        self._prompt_lib_combo = QComboBox()
        self._prompt_lib_combo.addItem("— Custom —", None)
        for p in self.pm.list_all():
            self._prompt_lib_combo.addItem(p.title, p.id)
        self._prompt_lib_combo.currentIndexChanged.connect(self._on_prompt_lib_changed)
        btn_refresh_prompts = QPushButton("⟳")
        btn_refresh_prompts.setFixedWidth(28)
        btn_refresh_prompts.clicked.connect(self._refresh_prompt_lib)
        prompt_selector.addWidget(QLabel("Library:"))
        prompt_selector.addWidget(self._prompt_lib_combo, stretch=1)
        prompt_selector.addWidget(btn_refresh_prompts)
        prompt_layout.addLayout(prompt_selector)

        self._system_prompt_edit = QPlainTextEdit()
        self._system_prompt_edit.setPlaceholderText("System prompt for this agent…")
        self._system_prompt_edit.setFixedHeight(100)
        prompt_layout.addWidget(self._system_prompt_edit)
        editor_layout.addWidget(prompt_group)

        # Tools
        tools_group = QGroupBox("Tools")
        tools_layout = QVBoxLayout(tools_group)
        tools_lbl = QLabel("Available tools from enabled plugins:")
        tools_lbl.setObjectName("dimLabel")
        tools_layout.addWidget(tools_lbl)
        self._tools_list = QListWidget()
        self._tools_list.setFixedHeight(120)
        self._tools_list.setSelectionMode(
            QListWidget.SelectionMode.MultiSelection
        )
        self._refresh_tools()
        tools_layout.addWidget(self._tools_list)
        editor_layout.addWidget(tools_group)

        # Memory + Reasoning
        behavior_group = QGroupBox("Behavior")
        beh_form = QFormLayout(behavior_group)
        beh_form.setSpacing(8)

        self._memory_combo = QComboBox()
        self._memory_combo.addItems(["none", "session", "persistent"])
        self._memory_combo.setToolTip(
            "none: no memory\n"
            "session: remembers within one conversation\n"
            "persistent: remembers across conversations"
        )

        self._reasoning_combo = QComboBox()
        self._reasoning_combo.addItems(["normal", "thinking", "plan"])
        self._reasoning_combo.setToolTip(
            "normal: standard generation\n"
            "thinking: chain-of-thought reasoning\n"
            "plan: generates a plan first, then executes"
        )

        self._exec_mode_combo = QComboBox()
        self._exec_mode_combo.addItems([
            "executor", "planner", "autonomous", "constrained"
        ])
        self._exec_mode_combo.setToolTip(
            "executor: directly executes tasks\n"
            "planner: creates plans before acting\n"
            "autonomous: operates independently with minimal oversight\n"
            "constrained: strict rules, confirms before each action"
        )

        beh_form.addRow("Memory Mode:", self._memory_combo)
        beh_form.addRow("Reasoning Mode:", self._reasoning_combo)
        beh_form.addRow("Execution Mode:", self._exec_mode_combo)
        editor_layout.addWidget(behavior_group)

        # Tags
        tags_layout = QHBoxLayout()
        tags_lbl = QLabel("Tags:")
        self._tags_edit = QLineEdit()
        self._tags_edit.setPlaceholderText("comma, separated")
        tags_layout.addWidget(tags_lbl)
        tags_layout.addWidget(self._tags_edit)
        editor_layout.addLayout(tags_layout)

        # Save button
        save_row = QHBoxLayout()
        btn_save = QPushButton("⊙ Save Agent")
        btn_save.setObjectName("primaryButton")
        btn_save.clicked.connect(self._on_save)
        save_row.addWidget(btn_save)
        save_row.addStretch()
        editor_layout.addLayout(save_row)

        editor_layout.addStretch()
        editor_scroll.setWidget(editor)
        splitter.addWidget(editor_scroll)
        splitter.setSizes([220, 500])

        layout.addWidget(splitter, stretch=1)

    # ── List ──────────────────────────────────────────────────────────────

    def _refresh_list(self):
        self._list.clear()
        for a in self.am.list_all():
            item = QListWidgetItem(f"{a.icon}  {a.name}")
            item.setData(Qt.ItemDataRole.UserRole, a.id)
            item.setToolTip(a.description)
            self._list.addItem(item)

    def _on_selection_changed(self, row: int):
        item = self._list.item(row)
        if not item:
            return
        aid = item.data(Qt.ItemDataRole.UserRole)
        a = self.am.get(aid)
        if a:
            self._selected = a
            self._load_agent(a)

    def _load_agent(self, a: AgentProfile):
        self._icon_edit.setText(a.icon)
        self._name_edit.setText(a.name)
        self._desc_edit.setPlainText(a.description)

        # Model
        idx = self._model_combo.findText(a.model)
        if idx >= 0:
            self._model_combo.setCurrentIndex(idx)
        else:
            self._model_combo.setCurrentText(a.model)
        idx = self._backend_combo.findText(a.backend)
        if idx >= 0:
            self._backend_combo.setCurrentIndex(idx)

        self._system_prompt_edit.setPlainText(a.system_prompt)

        # Tools
        for i in range(self._tools_list.count()):
            item = self._tools_list.item(i)
            tool_id = item.data(Qt.ItemDataRole.UserRole)
            item.setSelected(tool_id in a.tools)

        self._memory_combo.setCurrentText(a.memory_mode)
        self._reasoning_combo.setCurrentText(a.reasoning_mode)
        self._exec_mode_combo.setCurrentText(a.execution_mode)
        self._tags_edit.setText(", ".join(a.tags))

    def _refresh_tools(self):
        self._tools_list.clear()
        for tool in self.app_state.plugin_manager.all_tools():
            item = QListWidgetItem(f"🔧 {tool.name}  —  {tool.description[:50]}")
            item.setData(Qt.ItemDataRole.UserRole, tool.name)
            self._tools_list.addItem(item)
        if self._tools_list.count() == 0:
            item = QListWidgetItem("No tools available (enable plugins)")
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
            self._tools_list.addItem(item)

    def _refresh_prompt_lib(self):
        self._prompt_lib_combo.clear()
        self._prompt_lib_combo.addItem("— Custom —", None)
        for p in self.pm.list_all():
            self._prompt_lib_combo.addItem(p.title, p.id)

    def _on_prompt_lib_changed(self, idx: int):
        pid = self._prompt_lib_combo.currentData()
        if pid:
            p = self.pm.get(pid)
            if p:
                self._system_prompt_edit.setPlainText(p.content)

    # ── CRUD ──────────────────────────────────────────────────────────────

    def _on_new(self):
        a = self.am.create(name="New Agent", icon="🤖")
        self._refresh_list()
        for i in range(self._list.count()):
            if self._list.item(i).data(Qt.ItemDataRole.UserRole) == a.id:
                self._list.setCurrentRow(i)
                break

    def _on_save(self):
        selected_tools = [
            self._tools_list.item(i).data(Qt.ItemDataRole.UserRole)
            for i in range(self._tools_list.count())
            if self._tools_list.item(i).isSelected()
        ]
        tags = [t.strip() for t in self._tags_edit.text().split(",") if t.strip()]

        if self._selected:
            self._selected.icon = self._icon_edit.text()
            self._selected.name = self._name_edit.text()
            self._selected.description = self._desc_edit.toPlainText()
            self._selected.model = self._model_combo.currentText()
            self._selected.backend = self._backend_combo.currentText()
            self._selected.system_prompt = self._system_prompt_edit.toPlainText()
            self._selected.tools = selected_tools
            self._selected.memory_mode = self._memory_combo.currentText()
            self._selected.reasoning_mode = self._reasoning_combo.currentText()
            self._selected.execution_mode = self._exec_mode_combo.currentText()
            self._selected.tags = tags
            self.am.update(self._selected)
        else:
            self.am.create(
                icon=self._icon_edit.text(),
                name=self._name_edit.text(),
                description=self._desc_edit.toPlainText(),
                model=self._model_combo.currentText(),
                backend=self._backend_combo.currentText(),
                system_prompt=self._system_prompt_edit.toPlainText(),
                tools=selected_tools,
                memory_mode=self._memory_combo.currentText(),
                reasoning_mode=self._reasoning_combo.currentText(),
                execution_mode=self._exec_mode_combo.currentText(),
                tags=tags,
            )
        self._refresh_list()

    def _on_delete(self):
        if not self._selected:
            return
        reply = QMessageBox.question(
            self, "Delete Agent",
            f"Delete agent '{self._selected.name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.am.delete(self._selected.id)
            self._selected = None
            self._refresh_list()

    def _on_duplicate(self):
        if not self._selected:
            return
        new_a = self.am.duplicate(self._selected.id)
        if new_a:
            self._refresh_list()

    def _on_chat_with_agent(self):
        if self._selected:
            self.agent_chat_requested.emit(self._selected)

    def _on_import(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Import Agent", "", "JSON (*.json);;All Files (*)"
        )
        if path:
            from pathlib import Path
            a = self.am.import_from_file(Path(path))
            self._refresh_list()
            QMessageBox.information(self, "Imported", f"Imported: {a.name}")

    def _on_export(self):
        if not self._selected:
            QMessageBox.information(self, "No Selection", "Select an agent first.")
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Export Agent",
            f"{self._selected.name}.json", "JSON (*.json)"
        )
        if path:
            from pathlib import Path
            ok = self.am.export_to_file(self._selected.id, Path(path))
            if not ok:
                QMessageBox.warning(self, "Export Failed", "Could not export agent.")

    def refresh_models(self, models=None):
        """Called when model list changes."""
        current = self._model_combo.currentText()
        self._model_combo.clear()
        names = self.app_state.get_model_names()
        self._model_combo.addItems(names)
        idx = self._model_combo.findText(current)
        if idx >= 0:
            self._model_combo.setCurrentIndex(idx)
