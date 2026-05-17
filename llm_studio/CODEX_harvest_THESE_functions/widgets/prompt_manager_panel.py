"""System Prompt Manager panel."""

import logging
from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QListWidget, QListWidgetItem, QPlainTextEdit, QLineEdit,
    QComboBox, QFileDialog, QMessageBox, QInputDialog,
    QCheckBox, QSplitter, QToolButton, QFrame,
)

from app.core.prompt_manager import PromptManager, PromptEntry

log = logging.getLogger(__name__)


class PromptManagerPanel(QWidget):
    """Panel for managing the system prompt library."""

    prompt_selected = Signal(str)   # content — send to current chat

    def __init__(self, prompt_manager: PromptManager, parent=None):
        super().__init__(parent)
        self.pm = prompt_manager
        self._selected: Optional[PromptEntry] = None
        self._setup_ui()
        self._refresh_list()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # ── Toolbar ────────────────────────────────────────────────────────
        toolbar = QWidget()
        toolbar.setStyleSheet("background:#181825; border-bottom:1px solid #313244;")
        toolbar.setFixedHeight(42)
        tb = QHBoxLayout(toolbar)
        tb.setContentsMargins(8, 4, 8, 4)
        tb.setSpacing(6)

        btn_new = QPushButton("⊕ New")
        btn_new.clicked.connect(self._on_new)
        btn_import = QPushButton("⇓ Import")
        btn_import.clicked.connect(self._on_import)
        btn_export = QPushButton("⇑ Export")
        btn_export.clicked.connect(self._on_export)

        # Category filter
        cat_lbl = QLabel("Category:")
        cat_lbl.setObjectName("dimLabel")
        self._cat_combo = QComboBox()
        self._cat_combo.setFixedWidth(120)
        self._cat_combo.addItem("All")
        self._cat_combo.currentTextChanged.connect(self._refresh_list)

        # Search
        self._search = QLineEdit()
        self._search.setPlaceholderText("Search prompts…")
        self._search.setFixedWidth(160)
        self._search.textChanged.connect(self._refresh_list)

        # Favorites toggle
        self._fav_chk = QCheckBox("★ Favorites")
        self._fav_chk.toggled.connect(self._refresh_list)

        tb.addWidget(btn_new)
        tb.addWidget(btn_import)
        tb.addWidget(btn_export)
        tb.addWidget(QFrame())
        tb.addWidget(cat_lbl)
        tb.addWidget(self._cat_combo)
        tb.addWidget(self._search)
        tb.addWidget(self._fav_chk)
        tb.addStretch()

        layout.addWidget(toolbar)

        # ── Split: list | editor ───────────────────────────────────────────
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # List side
        list_widget = QWidget()
        list_layout = QVBoxLayout(list_widget)
        list_layout.setContentsMargins(6, 6, 6, 6)
        list_layout.setSpacing(4)

        self._list = QListWidget()
        self._list.currentRowChanged.connect(self._on_selection_changed)
        self._list.itemDoubleClicked.connect(self._on_apply)
        list_layout.addWidget(self._list)

        # List actions
        list_btns = QHBoxLayout()
        btn_apply = QPushButton("▶ Apply to Chat")
        btn_apply.setObjectName("primaryButton")
        btn_apply.setToolTip("Use this prompt as system prompt for current chat")
        btn_apply.clicked.connect(self._on_apply)
        btn_delete = QPushButton("✕ Delete")
        btn_delete.setObjectName("dangerButton")
        btn_delete.clicked.connect(self._on_delete)
        list_btns.addWidget(btn_apply)
        list_btns.addStretch()
        list_btns.addWidget(btn_delete)
        list_layout.addLayout(list_btns)

        splitter.addWidget(list_widget)

        # Editor side
        editor_widget = QWidget()
        editor_layout = QVBoxLayout(editor_widget)
        editor_layout.setContentsMargins(6, 6, 6, 6)
        editor_layout.setSpacing(6)

        # Title & category
        meta_layout = QHBoxLayout()
        self._title_edit = QLineEdit()
        self._title_edit.setPlaceholderText("Prompt title…")
        self._cat_edit = QLineEdit()
        self._cat_edit.setPlaceholderText("Category")
        self._cat_edit.setFixedWidth(100)
        self._fav_btn = QPushButton("☆")
        self._fav_btn.setFixedWidth(30)
        self._fav_btn.setCheckable(True)
        self._fav_btn.setToolTip("Toggle favorite")
        self._fav_btn.toggled.connect(self._on_fav_toggled)
        meta_layout.addWidget(self._title_edit)
        meta_layout.addWidget(self._cat_edit)
        meta_layout.addWidget(self._fav_btn)
        editor_layout.addLayout(meta_layout)

        # Tags
        tags_layout = QHBoxLayout()
        tags_lbl = QLabel("Tags:")
        tags_lbl.setObjectName("dimLabel")
        self._tags_edit = QLineEdit()
        self._tags_edit.setPlaceholderText("comma, separated, tags")
        tags_layout.addWidget(tags_lbl)
        tags_layout.addWidget(self._tags_edit)
        editor_layout.addLayout(tags_layout)

        # Content
        content_lbl = QLabel("Prompt Content:")
        content_lbl.setObjectName("sectionLabel")
        editor_layout.addWidget(content_lbl)

        self._content_edit = QPlainTextEdit()
        self._content_edit.setPlaceholderText("Enter system prompt content…")
        self._content_edit.setFont(
            __import__("PySide6.QtGui", fromlist=["QFont"]).QFont("Consolas", 11)
        )
        editor_layout.addWidget(self._content_edit, stretch=1)

        # Version info
        self._version_lbl = QLabel("v1")
        self._version_lbl.setObjectName("dimLabel")
        editor_layout.addWidget(self._version_lbl)

        # Save button
        save_btns = QHBoxLayout()
        btn_save = QPushButton("⊙ Save Changes")
        btn_save.setObjectName("primaryButton")
        btn_save.clicked.connect(self._on_save)
        btn_duplicate = QPushButton("⧉ Duplicate")
        btn_duplicate.clicked.connect(self._on_duplicate)
        save_btns.addWidget(btn_save)
        save_btns.addWidget(btn_duplicate)
        save_btns.addStretch()
        editor_layout.addLayout(save_btns)

        splitter.addWidget(editor_widget)
        splitter.setSizes([240, 400])

        layout.addWidget(splitter, stretch=1)

    # ── List management ───────────────────────────────────────────────────

    def _refresh_list(self):
        query = self._search.text().strip()
        cat = self._cat_combo.currentText()
        favorites_only = self._fav_chk.isChecked()

        if query:
            prompts = self.pm.search(query)
        elif favorites_only:
            prompts = self.pm.list_favorites()
        elif cat and cat != "All":
            prompts = self.pm.list_by_category(cat)
        else:
            prompts = self.pm.list_all()

        self._list.clear()
        for p in prompts:
            item = QListWidgetItem()
            star = "★ " if p.favorite else ""
            item.setText(f"{star}{p.title}")
            item.setData(Qt.ItemDataRole.UserRole, p.id)
            item.setToolTip(f"Category: {p.category}\nv{p.version}\n{p.content[:100]}…")
            self._list.addItem(item)

        # Refresh categories
        cats = ["All"] + self.pm.get_categories()
        current_cat = self._cat_combo.currentText()
        self._cat_combo.blockSignals(True)
        self._cat_combo.clear()
        self._cat_combo.addItems(cats)
        idx = self._cat_combo.findText(current_cat)
        self._cat_combo.setCurrentIndex(max(0, idx))
        self._cat_combo.blockSignals(False)

    def _on_selection_changed(self, row: int):
        item = self._list.item(row)
        if not item:
            return
        pid = item.data(Qt.ItemDataRole.UserRole)
        p = self.pm.get(pid)
        if not p:
            return
        self._selected = p
        self._title_edit.setText(p.title)
        self._cat_edit.setText(p.category)
        self._tags_edit.setText(", ".join(p.tags))
        self._fav_btn.blockSignals(True)
        self._fav_btn.setChecked(p.favorite)
        self._fav_btn.setText("★" if p.favorite else "☆")
        self._fav_btn.blockSignals(False)
        self._content_edit.setPlainText(p.content)
        self._version_lbl.setText(f"Version {p.version}  |  {p.updated_at[:10]}")

    def _on_apply(self):
        if self._selected:
            self.prompt_selected.emit(self._selected.content)

    def _on_new(self):
        title, ok = QInputDialog.getText(self, "New Prompt", "Prompt title:")
        if ok and title.strip():
            p = self.pm.create(title=title.strip(), content="")
            self._refresh_list()
            # Select new prompt
            for i in range(self._list.count()):
                if self._list.item(i).data(Qt.ItemDataRole.UserRole) == p.id:
                    self._list.setCurrentRow(i)
                    break

    def _on_save(self):
        if not self._selected:
            # Create new
            title = self._title_edit.text().strip() or "Untitled"
            category = self._cat_edit.text().strip() or "General"
            tags = [t.strip() for t in self._tags_edit.text().split(",") if t.strip()]
            content = self._content_edit.toPlainText()
            p = self.pm.create(title=title, content=content,
                               category=category, tags=tags)
            self._selected = p
            self._refresh_list()
        else:
            title = self._title_edit.text().strip()
            category = self._cat_edit.text().strip() or "General"
            tags = [t.strip() for t in self._tags_edit.text().split(",") if t.strip()]
            content = self._content_edit.toPlainText()
            self.pm.update(
                self._selected.id,
                title=title,
                content=content,
                category=category,
                tags=tags,
            )
            self._refresh_list()

    def _on_delete(self):
        if not self._selected:
            return
        reply = QMessageBox.question(
            self, "Delete Prompt",
            f"Delete '{self._selected.title}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.pm.delete(self._selected.id)
            self._selected = None
            self._refresh_list()

    def _on_fav_toggled(self, checked: bool):
        self._fav_btn.setText("★" if checked else "☆")
        if self._selected:
            self.pm.update(self._selected.id, favorite=checked)
            self._refresh_list()

    def _on_import(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Import Prompt", "", "JSON (*.json);;All Files (*)"
        )
        if path:
            from pathlib import Path
            p = self.pm.import_from_file(Path(path))
            if p:
                self._refresh_list()
                QMessageBox.information(self, "Imported",
                                        f"Imported: {p.title}")
            else:
                QMessageBox.warning(self, "Import Failed",
                                    "Could not import prompt file.")

    def _on_export(self):
        if not self._selected:
            QMessageBox.information(self, "No Selection", "Select a prompt first.")
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Export Prompt",
            f"{self._selected.title}.json", "JSON (*.json)"
        )
        if path:
            from pathlib import Path
            ok = self.pm.export_to_file(self._selected.id, Path(path))
            if not ok:
                QMessageBox.warning(self, "Export Failed", "Could not export.")

    def _on_duplicate(self):
        if not self._selected:
            return
        p = self.pm.create(
            title=f"{self._selected.title} (copy)",
            content=self._selected.content,
            category=self._selected.category,
            tags=list(self._selected.tags),
        )
        self._refresh_list()
