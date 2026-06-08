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
        self.workers = []
        self.events = []
        self.refreshes = 0
        self.async_calls = []

    def model_name(self):
        return self._model_name

    def begin_operation(self, operation):
        self.events.append(("start", operation))
        return len([event for event in self.events if event[0] == "start"])

    def update_operation(self, update, *, operation_id=None):
        self.events.append(("update", update, operation_id))

    def complete_operation(self, operation, *, operation_id=None):
        self.events.append(("ok", operation, operation_id))

    def fail_operation(self, operation, error, *, operation_id=None):
        self.events.append(("error", operation, error, operation_id))

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


def test_run_async_routes_lifecycle_to_operations_before_dialog(monkeypatch):
    events = []
    window = SimpleNamespace(
        worker_refs=[],
        begin_operation=lambda operation: events.append(("start", operation)) or 1,
        complete_operation=lambda operation, **_kwargs: events.append(("ok", operation)),
        fail_operation=lambda operation, error, **_kwargs: events.append(("error", operation, error)),
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
    window.worker_refs[0].error.emit("offline")

    assert events == [
        ("start", "Delete model llama3"),
        ("error", "Delete model llama3", "offline"),
        ("dialog", "Delete Model", "offline"),
    ]


def test_pull_stream_collapses_repeated_status_and_updates_progress(monkeypatch):
    _patch_widgets(monkeypatch, text=("  llama3.1:8b  ", True))
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
    task.token.emit('{"status":"pulling manifest"}')
    task.token.emit('{"status":"pulling manifest"}')
    task.token.emit('{"status":"pulling","digest":"667b0c1932bcffff","total":100,"completed":50}')
    task.completed.emit("done")

    histories = [event[1].history_text for event in window.events if event[0] == "update"]
    assert histories == ["pulling manifest", "", "pulling 667b0c1932bc"]
    progress = [event[1] for event in window.events if event[0] == "update"][-1]
    assert (progress.completed, progress.total) == (50, 100)
    assert window.events[0] == ("start", "Pull Model: llama3.1:8b")
    assert window.events[-1] == ("ok", "Pull Model: llama3.1:8b", 1)
    assert window.refreshes == 1


def test_pull_partial_chunks_do_not_create_corrupt_history(monkeypatch):
    _patch_widgets(monkeypatch)
    monkeypatch.setattr(
        "locallama_gui.ui.controllers.model_controller.StreamTask", _StreamTask
    )
    monkeypatch.setattr(
        "locallama_gui.ui.controllers.model_controller.create_backend",
        lambda _profile: SimpleNamespace(pull_model=lambda _name: None),
    )
    window = _ModelWindow()
    ModelController(SimpleNamespace(active_profile=lambda: object()), window).pull_model(None)

    window.workers[0].token.emit('{"status":"verifying sha')
    assert [event for event in window.events if event[0] == "update"] == []
    window.workers[0].token.emit('256 digest"}')

    updates = [event[1] for event in window.events if event[0] == "update"]
    assert [update.history_text for update in updates] == ["verifying sha256 digest"]


def test_stream_error_updates_operations_before_dialog(monkeypatch):
    dialog_events = _patch_widgets(monkeypatch, events=[])
    monkeypatch.setattr(
        "locallama_gui.ui.controllers.model_controller.StreamTask", _StreamTask
    )
    monkeypatch.setattr(
        "locallama_gui.ui.controllers.model_controller.create_backend",
        lambda _profile: SimpleNamespace(push_model=lambda _name: None),
    )
    window = _ModelWindow()
    controller = ModelController(SimpleNamespace(active_profile=lambda: object()), window)

    controller.push_model(None)
    window.workers[0].error.emit("not supported")

    assert window.events[-1] == ("error", "Push Model: model", "not supported", 1)
    assert dialog_events[-1] == ("critical", "Push Model", "not supported")


def test_clone_strips_names_and_delete_contract_remains_public(monkeypatch):
    _patch_widgets(monkeypatch, text=("  destination  ", True))
    window = _ModelWindow("  source  ")
    controller = ModelController(SimpleNamespace(active_profile=lambda: object()), window)

    controller.clone_model(None)

    assert window.async_calls[0][1] == "Clone model source -> destination"
    assert window.async_calls[0][2]["error_title"] == "Clone Model"


def test_create_stream_uses_operations_without_console_output(monkeypatch):
    monkeypatch.setattr("locallama_gui.ui.main_window.StreamTask", _StreamTask)
    monkeypatch.setattr(
        "locallama_gui.ui.main_window.create_backend",
        lambda _profile: SimpleNamespace(create_model=lambda _name, _modelfile: None),
    )
    events = []
    window = SimpleNamespace(
        config=SimpleNamespace(active_profile=lambda: object()),
        worker_refs=[],
        begin_operation=lambda operation: events.append(("start", operation)) or 1,
        update_operation=lambda update, **_kwargs: events.append(("update", update)),
        complete_operation=lambda operation, **_kwargs: events.append(("ok", operation)),
        fail_operation=lambda operation, error, **_kwargs: events.append(("error", operation, error)),
        refresh_backend=lambda: events.append(("refresh",)),
    )

    MainWindow.build_model_from_modelfile(window, " custom ", "FROM llama3")
    window.worker_refs[0].token.emit('{"status":"writing manifest"}')
    window.worker_refs[0].completed.emit("done")

    assert events[0] == ("start", "Create model: custom")
    assert events[1][1].history_text == "writing manifest"
    assert events[2:] == [("ok", "Create model: custom"), ("refresh",)]


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


def test_templates_route_lifecycle_to_operations_before_dialog(monkeypatch):
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
        model_combo=SimpleNamespace(currentText=lambda: " llama3 "),
        config=SimpleNamespace(active_profile=lambda: object()),
        worker_refs=[],
        begin_operation=lambda operation: events.append(("start", operation)) or 1,
        complete_operation=lambda operation, **_kwargs: events.append(("ok", operation)),
        fail_operation=lambda operation, error, **_kwargs: events.append(("error", operation, error)),
        _show_text_dialog=lambda title, text: events.append(("result", title, text)),
    )

    MainWindow.open_template_viewer(window)
    window.worker_refs[0].result.emit({"template": "value"})
    MainWindow.open_template_viewer(window)
    window.worker_refs[1].error.emit("lookup failed")

    assert events[:3] == [
        ("start", "Load template: llama3"),
        ("ok", "Load template: llama3"),
        ("result", "Template Viewer", '{\n  "template": "value"\n}'),
    ]
    assert events[-2:] == [
        ("error", "Load template: llama3", "lookup failed"),
        ("dialog", "Template Viewer", "lookup failed"),
    ]


class _OperationLabel:
    def __init__(self):
        self.text = ""

    def setText(self, text):
        self.text = text


class _OperationProgress:
    def __init__(self):
        self.range = (0, 0)
        self.value = 0

    def setRange(self, minimum, maximum):
        self.range = (minimum, maximum)

    def setValue(self, value):
        self.value = value


def test_stale_operation_callbacks_do_not_overwrite_active_status():
    from locallama_gui.ui.diagnostics import OperationUpdate

    history = []
    window = SimpleNamespace(
        _operation_seq=0,
        _active_operation_id=None,
        operation_status=_OperationLabel(),
        operation_progress=_OperationProgress(),
        append_operation_history=history.append,
    )
    first_id = MainWindow.begin_operation(window, "Pull Model: older")
    second_id = MainWindow.begin_operation(window, "Push Model: newer")

    MainWindow.update_operation(
        window,
        OperationUpdate(status="older still running", history_text="older progress"),
        operation_id=first_id,
    )
    MainWindow.complete_operation(window, "Pull Model: older", operation_id=first_id)

    assert window.operation_status.text == "Push Model: newer"
    assert window.operation_progress.range == (0, 0)

    MainWindow.update_operation(
        window,
        OperationUpdate(status="newer progress", history_text="", completed=50, total=100),
        operation_id=second_id,
    )
    MainWindow.complete_operation(window, "Push Model: newer", operation_id=second_id)

    assert window.operation_status.text == "Completed: Push Model: newer"
    assert window.operation_progress.range == (0, 1)
    assert window.operation_progress.value == 1
    assert history == [
        "[START] Pull Model: older",
        "[START] Push Model: newer",
        "older progress",
        "[OK] Pull Model: older",
        "[OK] Push Model: newer",
    ]
