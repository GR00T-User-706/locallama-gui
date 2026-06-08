from types import SimpleNamespace

from locallama_gui.ui.controllers.model_controller import ModelController
from locallama_gui.ui.main_window import MainWindow


class _Signal:
    def __init__(self):
        self.callbacks = []

    def connect(self, callback):
        self.callbacks.append(callback)

    def emit(self, *args):
        for callback in self.callbacks:
            callback(*args)


class _AsyncTask:
    def __init__(self, coro_factory):
        self.coro_factory = coro_factory
        self.finished_ok = _Signal()
        self.error = _Signal()
        self.result = _Signal()
        self.started = False

    def start(self):
        self.started = True


class _StreamTask:
    def __init__(self, iterator_factory):
        self.iterator_factory = iterator_factory
        self.token = _Signal()
        self.completed = _Signal()
        self.error = _Signal()
        self.started = False

    def start(self):
        self.started = True


class _ModelWindow:
    def __init__(self, model_name=""):
        self._model_name = model_name
        self.terminal = []
        self.workers = []
        self.refreshes = 0
        self.async_calls = []

    def model_name(self):
        return self._model_name

    def append_terminal(self, text):
        self.terminal.append(text)

    def refresh_backend(self):
        self.refreshes += 1

    def add_worker(self, worker):
        self.workers.append(worker)

    def run_async(self, coro_factory, done_msg, **kwargs):
        self.async_calls.append((coro_factory, done_msg, kwargs))

    def open_modelfile_editor(self):
        pass


def _patch_widgets(monkeypatch, *, text=("model", True), question=1, events=None):
    events = events if events is not None else []

    class _InputDialog:
        @staticmethod
        def getText(*_args, **_kwargs):
            return text

    class _MessageBox:
        class StandardButton:
            Yes = 1
            No = 2

        @staticmethod
        def information(_parent, title, message):
            events.append(("information", title, message))

        @staticmethod
        def question(*_args, **_kwargs):
            return question

        @staticmethod
        def critical(_parent, title, message):
            events.append(("critical", title, message))

    class _Widgets:
        QInputDialog = _InputDialog
        QMessageBox = _MessageBox

    original_import = __import__

    def fake_import(name, *args, **kwargs):
        if name == "PySide6.QtWidgets":
            return _Widgets
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr("builtins.__import__", fake_import)
    return events


def test_main_window_run_async_is_public_and_reports_terminal_before_dialog(monkeypatch):
    events = []
    window = SimpleNamespace(
        worker_refs=[],
        append_terminal=lambda text: events.append(("terminal", text)),
        log=lambda text: events.append(("log", text)),
        refresh_backend=lambda: events.append(("refresh",)),
    )
    monkeypatch.setattr("locallama_gui.ui.main_window.AsyncTask", _AsyncTask)
    monkeypatch.setattr(
        "locallama_gui.ui.main_window.QMessageBox.critical",
        lambda _parent, title, error: events.append(("dialog", title, error)),
    )

    MainWindow.run_async(
        window,
        lambda: None,
        "Delete model llama3",
        start_msg="Delete model llama3",
        error_title="Delete Model",
        parent=object(),
    )

    task = window.worker_refs[0]
    assert task.started is True
    assert events == [("terminal", "[START] Delete model llama3\n")]

    task.error.emit("offline")
    assert events[-2:] == [
        ("terminal", "[ERROR] Delete model llama3: offline\n"),
        ("dialog", "Delete Model", "offline"),
    ]


def test_main_window_run_async_reports_success_and_refreshes(monkeypatch):
    events = []
    window = SimpleNamespace(
        worker_refs=[],
        append_terminal=lambda text: events.append(("terminal", text)),
        log=lambda text: events.append(("log", text)),
        refresh_backend=lambda: events.append(("refresh",)),
    )
    monkeypatch.setattr("locallama_gui.ui.main_window.AsyncTask", _AsyncTask)

    MainWindow.run_async(
        window,
        lambda: None,
        "Clone model source -> destination",
        start_msg="Clone model source -> destination",
        error_title="Clone Model",
        parent=None,
    )
    window.worker_refs[0].finished_ok.emit()

    assert events == [
        ("terminal", "[START] Clone model source -> destination\n"),
        ("terminal", "[OK] Clone model source -> destination\n"),
        ("log", "Clone model source -> destination"),
        ("refresh",),
    ]


def test_stream_model_operation_strips_name_and_reports_lifecycle(monkeypatch):
    _patch_widgets(monkeypatch, text=("  llama3:8b  ", True))
    monkeypatch.setattr(
        "locallama_gui.ui.controllers.model_controller.StreamTask", _StreamTask
    )
    monkeypatch.setattr(
        "locallama_gui.ui.controllers.model_controller.create_backend",
        lambda _profile: SimpleNamespace(pull_model=lambda _name: None),
    )
    window = _ModelWindow()
    controller = ModelController(SimpleNamespace(active_profile=lambda: object()), window)

    controller.pull_model(parent=None)
    task = window.workers[0]
    task.token.emit("downloading")
    task.completed.emit("done")

    assert task.started is True
    assert window.terminal == [
        "[START] Pull Model: llama3:8b\n",
        "downloading\n",
        "[OK] Pull Model: llama3:8b\n",
    ]
    assert window.refreshes == 1


def test_stream_model_error_reaches_terminal_before_dialog(monkeypatch):
    events = []
    _patch_widgets(monkeypatch, text=("model", True), events=events)
    monkeypatch.setattr(
        "locallama_gui.ui.controllers.model_controller.StreamTask", _StreamTask
    )
    monkeypatch.setattr(
        "locallama_gui.ui.controllers.model_controller.create_backend",
        lambda _profile: SimpleNamespace(push_model=lambda _name: None),
    )
    window = _ModelWindow()
    window.append_terminal = lambda text: events.append(("terminal", text))
    controller = ModelController(SimpleNamespace(active_profile=lambda: object()), window)

    controller.push_model(parent=None)
    window.workers[0].error.emit("not supported")

    assert events[-2:] == [
        ("terminal", "[ERROR] Push Model: model: not supported\n"),
        ("critical", "Push Model", "not supported"),
    ]


def test_stream_model_operation_rejects_whitespace_name(monkeypatch):
    events = _patch_widgets(monkeypatch, text=("   ", True))
    window = _ModelWindow()
    controller = ModelController(SimpleNamespace(active_profile=lambda: None), window)

    controller.pull_model(parent=None)

    assert window.workers == []
    assert events == [("information", "Pull Model", "Model name is required.")]


def test_clone_strips_names_and_uses_public_async_scheduler(monkeypatch):
    _patch_widgets(monkeypatch, text=("  destination  ", True))
    window = _ModelWindow("  source  ")
    controller = ModelController(SimpleNamespace(active_profile=lambda: object()), window)

    controller.clone_model(parent=None)

    assert len(window.async_calls) == 1
    _factory, done_msg, kwargs = window.async_calls[0]
    assert done_msg == "Clone model source -> destination"
    assert kwargs["start_msg"] == done_msg
    assert kwargs["error_title"] == "Clone Model"


def test_create_model_reports_streamed_success(monkeypatch):
    monkeypatch.setattr("locallama_gui.ui.main_window.StreamTask", _StreamTask)
    monkeypatch.setattr(
        "locallama_gui.ui.main_window.create_backend",
        lambda _profile: SimpleNamespace(create_model=lambda _name, _modelfile: None),
    )
    window = SimpleNamespace(
        config=SimpleNamespace(active_profile=lambda: object()),
        worker_refs=[],
        terminal=[],
        refreshes=0,
    )
    window.append_terminal = lambda text: window.terminal.append(text)
    window.refresh_backend = lambda: setattr(window, "refreshes", window.refreshes + 1)

    MainWindow.build_model_from_modelfile(window, "  custom-model  ", "FROM llama3")
    task = window.worker_refs[0]
    task.token.emit("building")
    task.completed.emit("done")

    assert window.terminal == [
        "[START] Create model: custom-model\n",
        "building\n",
        "[OK] Create model: custom-model\n",
    ]
    assert window.refreshes == 1


def test_create_model_error_reaches_terminal_before_dialog(monkeypatch):
    events = []
    monkeypatch.setattr("locallama_gui.ui.main_window.StreamTask", _StreamTask)
    monkeypatch.setattr(
        "locallama_gui.ui.main_window.create_backend",
        lambda _profile: SimpleNamespace(create_model=lambda _name, _modelfile: None),
    )
    monkeypatch.setattr(
        "locallama_gui.ui.main_window.QMessageBox.critical",
        lambda _parent, title, error: events.append(("dialog", title, error)),
    )
    window = SimpleNamespace(
        config=SimpleNamespace(active_profile=lambda: object()),
        worker_refs=[],
        append_terminal=lambda text: events.append(("terminal", text)),
    )

    MainWindow.build_model_from_modelfile(window, "custom-model", "FROM llama3")
    window.worker_refs[0].error.emit("build failed")

    assert events[-2:] == [
        ("terminal", "[ERROR] Create model: custom-model: build failed\n"),
        ("dialog", "Create Model", "build failed"),
    ]


def test_templates_require_a_selected_model(monkeypatch):
    events = []
    monkeypatch.setattr(
        "locallama_gui.ui.main_window.QMessageBox.information",
        lambda _parent, title, message: events.append((title, message)),
    )
    window = SimpleNamespace(model_combo=SimpleNamespace(currentText=lambda: "   "))

    MainWindow.open_template_viewer(window)

    assert events == [
        ("Template Viewer", "Select a model before inspecting its template.")
    ]


def test_templates_report_success_and_error_to_terminal(monkeypatch):
    events = []
    monkeypatch.setattr("locallama_gui.ui.main_window.AsyncTask", _AsyncTask)
    monkeypatch.setattr(
        "locallama_gui.ui.main_window.create_backend",
        lambda _profile: SimpleNamespace(show_model=lambda _name: None),
    )
    monkeypatch.setattr(
        "locallama_gui.ui.main_window.QMessageBox.critical",
        lambda _parent, title, error: events.append(("dialog", title, error)),
    )
    window = SimpleNamespace(
        model_combo=SimpleNamespace(currentText=lambda: "  llama3  "),
        config=SimpleNamespace(active_profile=lambda: object()),
        worker_refs=[],
        append_terminal=lambda text: events.append(("terminal", text)),
        _show_text_dialog=lambda title, text: events.append(("result", title, text)),
    )

    MainWindow.open_template_viewer(window)
    success_task = window.worker_refs[0]
    success_task.result.emit({"template": "value"})

    assert events[:3] == [
        ("terminal", "[START] Load template: llama3\n"),
        ("terminal", "[OK] Load template: llama3\n"),
        ("result", "Template Viewer", '{\n  "template": "value"\n}'),
    ]

    MainWindow.open_template_viewer(window)
    error_task = window.worker_refs[1]
    error_task.error.emit("lookup failed")

    assert events[-2:] == [
        ("terminal", "[ERROR] Load template: llama3: lookup failed\n"),
        ("dialog", "Template Viewer", "lookup failed"),
    ]
