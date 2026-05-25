"""Plugin Manager Panel — list, enable/disable, reload plugins."""

import logging
from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QListWidget, QListWidgetItem, QTextEdit, QCheckBox,
    QFileDialog, QMessageBox, QSplitter, QFrame, QGroupBox,
    QFormLayout,
)

from app.core.plugin_manager import PluginManager, PluginRecord

log = logging.getLogger(__name__)


class PluginManagerPanel(QWidget):
    """UI for managing plugins."""

    plugins_changed = Signal()

    def __init__(self, plugin_manager: PluginManager, config, parent=None):
        super().__init__(parent)
        self.pm = plugin_manager
        self.config = config
        self._setup_ui()
        self._refresh()

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

        btn_install = QPushButton("⊕ Install…")
        btn_install.clicked.connect(self._on_install)
        btn_reload_all = QPushButton("⟳ Reload All")
        btn_reload_all.clicked.connect(self._on_reload_all)

        self._dev_mode_chk = QCheckBox("Developer Mode")
        self._dev_mode_chk.setChecked(self.config.get("developer_mode", False))
        self._dev_mode_chk.toggled.connect(
            lambda v: self.config.set("developer_mode", v)
        )

        plugins_dir_lbl = QLabel(f"📁 {str(self.pm._dir)}")
        plugins_dir_lbl.setObjectName("dimLabel")
        plugins_dir_lbl.setWordWrap(False)

        tb.addWidget(btn_install)
        tb.addWidget(btn_reload_all)
        tb.addWidget(self._dev_mode_chk)
        tb.addStretch()
        tb.addWidget(plugins_dir_lbl)

        layout.addWidget(toolbar)

        # Splitter: list | detail
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Plugin list
        list_widget = QWidget()
        list_layout = QVBoxLayout(list_widget)
        list_layout.setContentsMargins(6, 6, 6, 6)
        list_layout.setSpacing(4)

        count_lbl_row = QHBoxLayout()
        self._count_lbl = QLabel("0 plugins")
        self._count_lbl.setObjectName("dimLabel")
        count_lbl_row.addWidget(self._count_lbl)
        count_lbl_row.addStretch()
        list_layout.addLayout(count_lbl_row)

        self._list = QListWidget()
        self._list.currentRowChanged.connect(self._on_selection_changed)
        list_layout.addWidget(self._list, stretch=1)

        splitter.addWidget(list_widget)

        # Plugin detail
        detail_widget = QWidget()
        detail_layout = QVBoxLayout(detail_widget)
        detail_layout.setContentsMargins(8, 8, 8, 8)
        detail_layout.setSpacing(8)

        detail_title = QLabel("Plugin Details")
        detail_title.setObjectName("headingLabel")
        detail_layout.addWidget(detail_title)

        info_group = QGroupBox("Information")
        info_form = QFormLayout(info_group)
        self._det_id = QLabel("—")
        self._det_name = QLabel("—")
        self._det_version = QLabel("—")
        self._det_author = QLabel("—")
        self._det_desc = QLabel("—")
        self._det_desc.setWordWrap(True)
        self._det_path = QLabel("—")
        self._det_path.setWordWrap(True)
        self._det_error = QLabel("")
        self._det_error.setWordWrap(True)
        self._det_error.setStyleSheet("color:#f38ba8;")

        for label, widget in [
            ("ID:", self._det_id),
            ("Name:", self._det_name),
            ("Version:", self._det_version),
            ("Author:", self._det_author),
            ("Description:", self._det_desc),
            ("Source:", self._det_path),
        ]:
            info_form.addRow(QLabel(label), widget)
        detail_layout.addWidget(info_group)

        detail_layout.addWidget(self._det_error)

        # Tools & commands
        ext_group = QGroupBox("Extensions")
        ext_layout = QVBoxLayout(ext_group)
        self._tools_lbl = QLabel("Tools: —")
        self._cmds_lbl = QLabel("Commands: —")
        ext_layout.addWidget(self._tools_lbl)
        ext_layout.addWidget(self._cmds_lbl)
        detail_layout.addWidget(ext_group)

        # Actions
        action_row = QHBoxLayout()
        self._btn_enable = QPushButton("Enable")
        self._btn_enable.setObjectName("primaryButton")
        self._btn_enable.clicked.connect(self._on_enable_toggle)
        self._btn_reload = QPushButton("⟳ Reload")
        self._btn_reload.clicked.connect(self._on_reload)
        action_row.addWidget(self._btn_enable)
        action_row.addWidget(self._btn_reload)
        action_row.addStretch()
        detail_layout.addLayout(action_row)
        detail_layout.addStretch()

        splitter.addWidget(detail_widget)
        splitter.setSizes([260, 400])

        layout.addWidget(splitter, stretch=1)

    def _refresh(self):
        records = self.pm.list_all()
        self._count_lbl.setText(f"{len(records)} plugin(s)")

        self._list.clear()
        for r in records:
            item = QListWidgetItem()
            status = "✓" if r.enabled else "○"
            color = "#a6e3a1" if r.enabled else "#6c7086"
            if r.error:
                status = "✕"
                color = "#f38ba8"
            item.setText(f"{status}  {r.plugin.PLUGIN_NAME or r.plugin.PLUGIN_ID}")
            item.setForeground(__import__("PySide6.QtGui", fromlist=["QColor"]).QColor(color))
            item.setData(Qt.ItemDataRole.UserRole, r.plugin.PLUGIN_ID)
            item.setToolTip(r.plugin.PLUGIN_DESC)
            self._list.addItem(item)

    def _on_selection_changed(self, row: int):
        item = self._list.item(row)
        if not item:
            return
        pid = item.data(Qt.ItemDataRole.UserRole)
        r = self.pm.get(pid)
        if not r:
            return
        p = r.plugin
        self._det_id.setText(p.PLUGIN_ID)
        self._det_name.setText(p.PLUGIN_NAME or "—")
        self._det_version.setText(p.PLUGIN_VERSION)
        self._det_author.setText(p.PLUGIN_AUTHOR or "—")
        self._det_desc.setText(p.PLUGIN_DESC or "—")
        self._det_path.setText(str(r.source_path))
        self._det_error.setText(r.error or "")

        tools = p.get_tools() if r.enabled else []
        cmds = p.get_commands() if r.enabled else []
        self._tools_lbl.setText(
            f"Tools: {', '.join(t.name for t in tools) or 'none'}"
        )
        self._cmds_lbl.setText(
            f"Commands: {', '.join(c.name for c in cmds) or 'none'}"
        )

        self._btn_enable.setText("Disable" if r.enabled else "Enable")

    def _on_enable_toggle(self):
        item = self._list.currentItem()
        if not item:
            return
        pid = item.data(Qt.ItemDataRole.UserRole)
        r = self.pm.get(pid)
        if not r:
            return
        if r.enabled:
            self.pm.disable(pid)
        else:
            self.pm.enable(pid)

        # Persist disabled list
        self.config.set("disabled_plugins", self.pm.get_disabled_ids())
        self._refresh()
        # Re-select
        for i in range(self._list.count()):
            if self._list.item(i).data(Qt.ItemDataRole.UserRole) == pid:
                self._list.setCurrentRow(i)
                break
        self.plugins_changed.emit()

    def _on_reload(self):
        item = self._list.currentItem()
        if not item:
            return
        pid = item.data(Qt.ItemDataRole.UserRole)
        self.pm.reload_plugin(pid)
        self._refresh()
        self.plugins_changed.emit()

    def _on_reload_all(self):
        self.pm.reload_all()
        self._refresh()
        self.plugins_changed.emit()

    def _on_install(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Install Plugin",
            "", "Python Files (*.py);;All Files (*)"
        )
        if path:
            from pathlib import Path
            ok = self.pm.install_from_file(Path(path))
            if ok:
                self._refresh()
                self.plugins_changed.emit()
                QMessageBox.information(self, "Installed",
                                        "Plugin installed successfully.")
            else:
                QMessageBox.critical(self, "Install Failed",
                                     "Could not install plugin.")
