"""Dark theme stylesheet for LLM Studio."""


DARK_QSS = """
/* ── Global ──────────────────────────────────────────────── */
QWidget {
    background-color: #1e1e2e;
    color: #cdd6f4;
    font-family: "Segoe UI", "Inter", "SF Pro Text", system-ui, sans-serif;
    font-size: 13px;
    border: none;
}

QMainWindow, QDialog {
    background-color: #1e1e2e;
}

/* ── Menu Bar ─────────────────────────────────────────────── */
QMenuBar {
    background-color: #181825;
    color: #cdd6f4;
    border-bottom: 1px solid #313244;
    padding: 2px 4px;
}
QMenuBar::item {
    padding: 4px 10px;
    border-radius: 4px;
}
QMenuBar::item:selected, QMenuBar::item:pressed {
    background-color: #45475a;
}
QMenu {
    background-color: #1e1e2e;
    border: 1px solid #45475a;
    border-radius: 6px;
    padding: 4px;
}
QMenu::item {
    padding: 6px 24px 6px 12px;
    border-radius: 4px;
}
QMenu::item:selected {
    background-color: #45475a;
}
QMenu::separator {
    height: 1px;
    background-color: #313244;
    margin: 4px 8px;
}
QMenu::indicator {
    width: 14px;
    height: 14px;
}

/* ── Tool Bar ─────────────────────────────────────────────── */
QToolBar {
    background-color: #181825;
    border-bottom: 1px solid #313244;
    spacing: 2px;
    padding: 2px 4px;
}
QToolBar::separator {
    width: 1px;
    background-color: #313244;
    margin: 4px 2px;
}
QToolButton {
    background-color: transparent;
    color: #cdd6f4;
    padding: 4px 8px;
    border-radius: 4px;
    border: none;
}
QToolButton:hover {
    background-color: #313244;
}
QToolButton:pressed, QToolButton:checked {
    background-color: #45475a;
}

/* ── Status Bar ───────────────────────────────────────────── */
QStatusBar {
    background-color: #181825;
    border-top: 1px solid #313244;
    color: #a6adc8;
    font-size: 12px;
}
QStatusBar::item {
    border: none;
}

/* ── Dock Widgets ─────────────────────────────────────────── */
QDockWidget {
    titlebar-close-icon: none;
    titlebar-normal-icon: none;
    color: #cdd6f4;
}
QDockWidget::title {
    background-color: #181825;
    border-bottom: 1px solid #313244;
    padding: 6px 10px;
    font-weight: 600;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: #a6adc8;
}
QDockWidget::close-button, QDockWidget::float-button {
    padding: 0px;
    border-radius: 3px;
}
QDockWidget::close-button:hover, QDockWidget::float-button:hover {
    background-color: #45475a;
}

/* ── Tab Widget ───────────────────────────────────────────── */
QTabWidget::pane {
    border: 1px solid #313244;
    border-radius: 4px;
    background-color: #1e1e2e;
}
QTabBar {
    background-color: transparent;
}
QTabBar::tab {
    background-color: #181825;
    color: #a6adc8;
    padding: 7px 16px;
    margin-right: 1px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    border: 1px solid #313244;
    border-bottom: none;
    font-size: 12px;
}
QTabBar::tab:selected {
    background-color: #1e1e2e;
    color: #cdd6f4;
    border-bottom: 2px solid #89b4fa;
}
QTabBar::tab:hover:!selected {
    background-color: #313244;
    color: #cdd6f4;
}
QTabBar::close-button {
    image: none;
    subcontrol-position: right;
}

/* ── Scroll Bars ──────────────────────────────────────────── */
QScrollBar:vertical {
    background-color: #1e1e2e;
    width: 8px;
    margin: 0;
}
QScrollBar::handle:vertical {
    background-color: #45475a;
    border-radius: 4px;
    min-height: 20px;
}
QScrollBar::handle:vertical:hover {
    background-color: #585b70;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
QScrollBar:horizontal {
    background-color: #1e1e2e;
    height: 8px;
    margin: 0;
}
QScrollBar::handle:horizontal {
    background-color: #45475a;
    border-radius: 4px;
    min-width: 20px;
}
QScrollBar::handle:horizontal:hover {
    background-color: #585b70;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

/* ── Push Buttons ─────────────────────────────────────────── */
QPushButton {
    background-color: #313244;
    color: #cdd6f4;
    border: 1px solid #45475a;
    border-radius: 5px;
    padding: 6px 14px;
    font-weight: 500;
}
QPushButton:hover {
    background-color: #45475a;
    border-color: #585b70;
}
QPushButton:pressed {
    background-color: #585b70;
}
QPushButton:disabled {
    color: #585b70;
    background-color: #1e1e2e;
    border-color: #313244;
}
QPushButton#primaryButton {
    background-color: #89b4fa;
    color: #1e1e2e;
    border-color: #89b4fa;
    font-weight: 600;
}
QPushButton#primaryButton:hover {
    background-color: #74c7ec;
    border-color: #74c7ec;
}
QPushButton#primaryButton:disabled {
    background-color: #313244;
    color: #585b70;
    border-color: #313244;
}
QPushButton#dangerButton {
    background-color: #f38ba8;
    color: #1e1e2e;
    border-color: #f38ba8;
    font-weight: 600;
}
QPushButton#dangerButton:hover {
    background-color: #eba0ac;
}

/* ── Line Edit / Text Edit ────────────────────────────────── */
QLineEdit, QTextEdit, QPlainTextEdit {
    background-color: #181825;
    color: #cdd6f4;
    border: 1px solid #313244;
    border-radius: 5px;
    padding: 6px 8px;
    selection-background-color: #45475a;
}
QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border-color: #89b4fa;
}
QLineEdit:disabled, QTextEdit:disabled, QPlainTextEdit:disabled {
    color: #585b70;
    background-color: #1e1e2e;
}

/* ── Combo Box ────────────────────────────────────────────── */
QComboBox {
    background-color: #181825;
    color: #cdd6f4;
    border: 1px solid #313244;
    border-radius: 5px;
    padding: 5px 10px;
    min-width: 80px;
}
QComboBox:hover {
    border-color: #45475a;
}
QComboBox:focus {
    border-color: #89b4fa;
}
QComboBox::drop-down {
    border: none;
    width: 20px;
}
QComboBox::down-arrow {
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 6px solid #a6adc8;
    margin-right: 4px;
}
QComboBox QAbstractItemView {
    background-color: #1e1e2e;
    border: 1px solid #45475a;
    border-radius: 4px;
    selection-background-color: #45475a;
    color: #cdd6f4;
}

/* ── Spin Box ─────────────────────────────────────────────── */
QSpinBox, QDoubleSpinBox {
    background-color: #181825;
    color: #cdd6f4;
    border: 1px solid #313244;
    border-radius: 5px;
    padding: 5px 8px;
}
QSpinBox:focus, QDoubleSpinBox:focus {
    border-color: #89b4fa;
}
QSpinBox::up-button, QSpinBox::down-button,
QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
    background-color: #313244;
    border-radius: 2px;
    width: 16px;
}

/* ── Slider ───────────────────────────────────────────────── */
QSlider::groove:horizontal {
    background-color: #313244;
    height: 4px;
    border-radius: 2px;
}
QSlider::handle:horizontal {
    background-color: #89b4fa;
    width: 14px;
    height: 14px;
    margin: -5px 0;
    border-radius: 7px;
}
QSlider::handle:horizontal:hover {
    background-color: #74c7ec;
}
QSlider::sub-page:horizontal {
    background-color: #89b4fa;
    border-radius: 2px;
}

/* ── Check Box ────────────────────────────────────────────── */
QCheckBox {
    spacing: 8px;
}
QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border-radius: 3px;
    border: 1px solid #45475a;
    background-color: #181825;
}
QCheckBox::indicator:checked {
    background-color: #89b4fa;
    border-color: #89b4fa;
}
QCheckBox::indicator:hover {
    border-color: #89b4fa;
}

/* ── Radio Button ─────────────────────────────────────────── */
QRadioButton {
    spacing: 8px;
}
QRadioButton::indicator {
    width: 16px;
    height: 16px;
    border-radius: 8px;
    border: 1px solid #45475a;
    background-color: #181825;
}
QRadioButton::indicator:checked {
    background-color: #89b4fa;
    border-color: #89b4fa;
}

/* ── List Widget ──────────────────────────────────────────── */
QListWidget, QListView {
    background-color: #181825;
    border: 1px solid #313244;
    border-radius: 5px;
    alternate-background-color: #1e1e2e;
    outline: none;
}
QListWidget::item, QListView::item {
    padding: 6px 8px;
    border-radius: 3px;
    margin: 1px 2px;
}
QListWidget::item:selected, QListView::item:selected {
    background-color: #313244;
    color: #cdd6f4;
}
QListWidget::item:hover, QListView::item:hover {
    background-color: #25253a;
}

/* ── Table Widget ─────────────────────────────────────────── */
QTableWidget, QTableView {
    background-color: #181825;
    border: 1px solid #313244;
    border-radius: 5px;
    gridline-color: #313244;
    outline: none;
}
QTableWidget::item, QTableView::item {
    padding: 6px 10px;
}
QTableWidget::item:selected, QTableView::item:selected {
    background-color: #313244;
    color: #cdd6f4;
}
QHeaderView::section {
    background-color: #1e1e2e;
    color: #a6adc8;
    border: none;
    border-bottom: 1px solid #313244;
    border-right: 1px solid #313244;
    padding: 6px 10px;
    font-weight: 600;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* ── Group Box ────────────────────────────────────────────── */
QGroupBox {
    border: 1px solid #313244;
    border-radius: 6px;
    margin-top: 14px;
    padding: 8px 8px 8px 8px;
    font-weight: 600;
    color: #a6adc8;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 10px;
    padding: 0 4px;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* ── Label ────────────────────────────────────────────────── */
QLabel {
    color: #cdd6f4;
}
QLabel#dimLabel {
    color: #6c7086;
    font-size: 11px;
}
QLabel#headingLabel {
    font-size: 15px;
    font-weight: 700;
    color: #cdd6f4;
}
QLabel#sectionLabel {
    font-size: 11px;
    font-weight: 600;
    color: #a6adc8;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

/* ── Splitter ─────────────────────────────────────────────── */
QSplitter::handle {
    background-color: #313244;
}
QSplitter::handle:horizontal {
    width: 2px;
}
QSplitter::handle:vertical {
    height: 2px;
}

/* ── Tooltip ──────────────────────────────────────────────── */
QToolTip {
    background-color: #313244;
    color: #cdd6f4;
    border: 1px solid #45475a;
    border-radius: 4px;
    padding: 4px 8px;
    font-size: 12px;
}

/* ── Progress Bar ─────────────────────────────────────────── */
QProgressBar {
    background-color: #313244;
    border-radius: 4px;
    height: 8px;
    text-align: center;
    border: none;
}
QProgressBar::chunk {
    background-color: #89b4fa;
    border-radius: 4px;
}

/* ── Frame ────────────────────────────────────────────────── */
QFrame[frameShape="4"], QFrame[frameShape="5"] {  /* HLine, VLine */
    color: #313244;
    background-color: #313244;
    max-height: 1px;
}

/* ── Text Browser ─────────────────────────────────────────── */
QTextBrowser {
    background-color: #181825;
    color: #cdd6f4;
    border: 1px solid #313244;
    border-radius: 5px;
    padding: 8px;
    selection-background-color: #45475a;
}
"""


def apply_dark_theme(app):
    """Apply dark theme to a QApplication instance."""
    app.setStyleSheet(DARK_QSS)
