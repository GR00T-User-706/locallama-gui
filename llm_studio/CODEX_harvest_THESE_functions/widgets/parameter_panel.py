"""
Parameter Panel — exposes all generation/sampling parameters with
sliders, spinboxes, and preset management.
"""

import logging
from typing import Dict, Any

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider,
    QDoubleSpinBox, QSpinBox, QComboBox, QPushButton,
    QScrollArea, QFormLayout, QGroupBox, QCheckBox,
    QPlainTextEdit, QInputDialog, QMessageBox, QFrame,
)

from app.ui.widgets.collapsible_section import CollapsibleSection

log = logging.getLogger(__name__)


class ParamRow(QWidget):
    """A parameter row: label + slider + spinbox."""

    value_changed = Signal(str, object)   # param_name, value

    def __init__(self, name: str, label: str, min_val: float, max_val: float,
                 default: float, decimals: int = 2, step: float = None,
                 tooltip: str = "", parent=None):
        super().__init__(parent)
        self.name = name
        self._decimals = decimals
        self._updating = False

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        lbl = QLabel(label)
        lbl.setFixedWidth(120)
        lbl.setToolTip(tooltip)
        lbl.setObjectName("dimLabel")

        self._slider = QSlider(Qt.Orientation.Horizontal)
        self._slider.setRange(0, 1000)
        self._slider.setToolTip(tooltip)

        if decimals == 0:
            self._spin = QSpinBox()
            self._spin.setRange(int(min_val), int(max_val))
            self._spin.setValue(int(default))
            self._spin.setSingleStep(int(step) if step else 1)
        else:
            self._spin = QDoubleSpinBox()
            self._spin.setRange(min_val, max_val)
            self._spin.setDecimals(decimals)
            self._spin.setValue(default)
            self._spin.setSingleStep(step or 0.01)

        self._spin.setFixedWidth(80)
        self._min = min_val
        self._max = max_val
        self._range = max_val - min_val

        self._set_slider_from_value(default)

        self._slider.valueChanged.connect(self._slider_changed)
        self._spin.valueChanged.connect(self._spin_changed)

        layout.addWidget(lbl)
        layout.addWidget(self._slider, stretch=1)
        layout.addWidget(self._spin)

    def _value_to_slider(self, v: float) -> int:
        if self._range == 0:
            return 0
        return int((v - self._min) / self._range * 1000)

    def _slider_to_value(self, s: int) -> float:
        v = self._min + (s / 1000.0) * self._range
        if self._decimals == 0:
            return int(round(v))
        return round(v, self._decimals)

    def _set_slider_from_value(self, v: float):
        self._slider.blockSignals(True)
        self._slider.setValue(self._value_to_slider(v))
        self._slider.blockSignals(False)

    def _slider_changed(self, s: int):
        if self._updating:
            return
        self._updating = True
        v = self._slider_to_value(s)
        self._spin.setValue(v)
        self.value_changed.emit(self.name, v)
        self._updating = False

    def _spin_changed(self, v):
        if self._updating:
            return
        self._updating = True
        self._set_slider_from_value(float(v))
        self.value_changed.emit(self.name, v)
        self._updating = False

    def get_value(self):
        return self._spin.value()

    def set_value(self, v):
        self._updating = True
        self._spin.setValue(v)
        self._set_slider_from_value(float(v))
        self._updating = False


class ParameterPanel(QWidget):
    """Full parameter editor with presets."""

    params_changed = Signal(dict)

    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
        self._rows: Dict[str, ParamRow] = {}
        self._setup_ui()
        self._load_from_config()

    def _setup_ui(self):
        main = QVBoxLayout(self)
        main.setContentsMargins(0, 0, 0, 0)
        main.setSpacing(0)

        # ── Preset bar ────────────────────────────────────────────────────
        preset_bar = QWidget()
        preset_bar.setStyleSheet(
            "background:#181825; border-bottom:1px solid #313244;"
        )
        preset_bar.setFixedHeight(42)
        pb = QHBoxLayout(preset_bar)
        pb.setContentsMargins(8, 4, 8, 4)
        pb.setSpacing(6)

        pb.addWidget(QLabel("Preset:"))
        self._preset_combo = QComboBox()
        self._preset_combo.setFixedWidth(160)
        self._refresh_presets()
        self._preset_combo.currentTextChanged.connect(self._on_preset_selected)

        btn_load = QPushButton("Load")
        btn_load.clicked.connect(self._on_preset_selected)
        btn_save = QPushButton("Save As…")
        btn_save.clicked.connect(self._on_save_preset)
        btn_delete = QPushButton("Delete")
        btn_delete.clicked.connect(self._on_delete_preset)
        btn_reset = QPushButton("⟳ Reset")
        btn_reset.setToolTip("Reset to defaults")
        btn_reset.clicked.connect(self._on_reset)

        pb.addWidget(self._preset_combo)
        pb.addWidget(btn_load)
        pb.addWidget(btn_save)
        pb.addWidget(btn_delete)
        pb.addStretch()
        pb.addWidget(btn_reset)

        main.addWidget(preset_bar)

        # ── Scrollable parameter area ──────────────────────────────────────
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border:none; }")

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(8, 8, 8, 8)
        content_layout.setSpacing(4)

        # Sampling parameters
        sampling_sec = CollapsibleSection("Sampling", collapsed=False)
        self._add_param(sampling_sec, "temperature", "Temperature",
                        0.0, 2.0, 0.7, 2, 0.05,
                        "Controls randomness. Higher = more creative, lower = more focused.")
        self._add_param(sampling_sec, "top_k", "Top-K",
                        0, 200, 40, 0, 5,
                        "Limits vocabulary to top K tokens. 0 = disabled.")
        self._add_param(sampling_sec, "top_p", "Top-P",
                        0.0, 1.0, 0.9, 2, 0.05,
                        "Nucleus sampling. Consider tokens up to this cumulative probability.")
        self._add_param(sampling_sec, "min_p", "Min-P",
                        0.0, 1.0, 0.0, 2, 0.01,
                        "Minimum probability filter. Discards tokens below this threshold.")
        self._add_param(sampling_sec, "repeat_penalty", "Repeat Penalty",
                        1.0, 2.0, 1.1, 2, 0.01,
                        "Penalize repeated tokens. 1.0 = off.")
        self._add_param(sampling_sec, "repeat_last_n", "Repeat Last N",
                        0, 512, 64, 0, 8,
                        "How many tokens to check for repetition.")
        self._add_param(sampling_sec, "tfs_z", "TFS-Z",
                        0.0, 2.0, 1.0, 2, 0.05,
                        "Tail Free Sampling. 1.0 = disabled.")
        content_layout.addWidget(sampling_sec)

        # Mirostat
        mirostat_sec = CollapsibleSection("Mirostat", collapsed=True)
        self._add_param(mirostat_sec, "mirostat", "Mode",
                        0, 2, 0, 0, 1,
                        "0=off, 1=Mirostat v1, 2=Mirostat v2")
        self._add_param(mirostat_sec, "mirostat_tau", "Tau",
                        0.0, 10.0, 5.0, 2, 0.1,
                        "Target perplexity (Mirostat)")
        self._add_param(mirostat_sec, "mirostat_eta", "Eta",
                        0.0, 1.0, 0.1, 2, 0.01,
                        "Learning rate (Mirostat)")
        content_layout.addWidget(mirostat_sec)

        # Generation
        gen_sec = CollapsibleSection("Generation", collapsed=False)
        self._add_param(gen_sec, "num_predict", "Max Tokens",
                        -1, 32768, -1, 0, 64,
                        "Maximum tokens to generate. -1 = unlimited.")
        self._add_param(gen_sec, "seed", "Seed",
                        -1, 2147483647, -1, 0, 1,
                        "Random seed for reproducibility. -1 = random.")
        self._add_param(gen_sec, "num_ctx", "Context Size",
                        512, 131072, 4096, 0, 512,
                        "Context window size in tokens.")
        self._add_param(gen_sec, "num_batch", "Batch Size",
                        1, 4096, 512, 0, 64,
                        "Batch size for prompt processing.")
        self._add_param(gen_sec, "num_gpu", "GPU Layers",
                        -1, 128, -1, 0, 1,
                        "Number of layers to offload to GPU. -1 = all.")
        content_layout.addWidget(gen_sec)

        # Stop sequences
        stop_sec = CollapsibleSection("Stop Sequences", collapsed=True)
        stop_lbl = QLabel("One stop sequence per line:")
        stop_lbl.setObjectName("dimLabel")
        self._stop_edit = QPlainTextEdit()
        self._stop_edit.setPlaceholderText("</s>\n<|end|>\n...")
        self._stop_edit.setFixedHeight(80)
        self._stop_edit.textChanged.connect(self._on_stop_changed)
        stop_sec.add_widget(stop_lbl)
        stop_sec.add_widget(self._stop_edit)
        content_layout.addWidget(stop_sec)

        content_layout.addStretch()

        scroll.setWidget(content)
        main.addWidget(scroll, stretch=1)

    def _add_param(self, section: CollapsibleSection, name: str, label: str,
                   min_v: float, max_v: float, default: float, decimals: int,
                   step: float, tooltip: str = ""):
        row = ParamRow(name, label, min_v, max_v, default, decimals, step, tooltip)
        row.value_changed.connect(self._on_value_changed)
        self._rows[name] = row
        section.add_widget(row)

    # ── Value changes ─────────────────────────────────────────────────────

    def _on_value_changed(self, name: str, value):
        self.config.update_parameters({name: value})
        self.params_changed.emit(self.get_params())

    def _on_stop_changed(self):
        stops = [
            s.strip() for s in self._stop_edit.toPlainText().splitlines()
            if s.strip()
        ]
        self.config.update_parameters({"stop": stops})

    def get_params(self) -> Dict[str, Any]:
        params = {}
        for name, row in self._rows.items():
            params[name] = row.get_value()
        stops = [
            s.strip() for s in self._stop_edit.toPlainText().splitlines()
            if s.strip()
        ]
        params["stop"] = stops
        return params

    def set_params(self, params: Dict[str, Any]):
        for name, row in self._rows.items():
            if name in params:
                row.set_value(params[name])
        if "stop" in params:
            self._stop_edit.blockSignals(True)
            self._stop_edit.setPlainText("\n".join(params["stop"]))
            self._stop_edit.blockSignals(False)

    def _load_from_config(self):
        self.set_params(self.config.parameters)

    # ── Presets ───────────────────────────────────────────────────────────

    def _refresh_presets(self):
        self._preset_combo.blockSignals(True)
        self._preset_combo.clear()
        presets = self.config.get("parameter_presets", {})
        self._preset_combo.addItems(sorted(presets.keys()))
        self._preset_combo.blockSignals(False)

    def _on_preset_selected(self, name: str = None):
        if not name:
            name = self._preset_combo.currentText()
        presets = self.config.get("parameter_presets", {})
        if name in presets:
            self.set_params(presets[name])
            self.config.update_parameters(presets[name])

    def _on_save_preset(self):
        name, ok = QInputDialog.getText(
            self, "Save Preset", "Preset name:"
        )
        if not ok or not name.strip():
            return
        presets = self.config.get("parameter_presets", {})
        presets[name.strip()] = self.get_params()
        self.config.set("parameter_presets", presets)
        self._refresh_presets()
        idx = self._preset_combo.findText(name.strip())
        if idx >= 0:
            self._preset_combo.setCurrentIndex(idx)

    def _on_delete_preset(self):
        name = self._preset_combo.currentText()
        if not name:
            return
        reply = QMessageBox.question(
            self, "Delete Preset", f"Delete preset '{name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            presets = self.config.get("parameter_presets", {})
            presets.pop(name, None)
            self.config.set("parameter_presets", presets)
            self._refresh_presets()

    def _on_reset(self):
        from app.core.config_manager import DEFAULT_CONFIG
        default_params = DEFAULT_CONFIG["parameters"]
        self.set_params(default_params)
        self.config.update_parameters(default_params)
