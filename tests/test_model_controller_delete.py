from types import SimpleNamespace

from locallama_gui.ui.controllers.model_controller import ModelController


class _Window:
    def __init__(self, model_name=""):
        self._model_name = model_name
        self.async_calls = []

    def model_name(self):
        return self._model_name

    def append_terminal(self, _text):
        pass

    def refresh_backend(self):
        pass

    def add_worker(self, _worker):
        pass

    def run_async(self, coro_factory, done_msg):
        self.async_calls.append((coro_factory, done_msg))

    def open_modelfile_editor(self):
        pass


def test_delete_model_without_selection_shows_info(monkeypatch):
    events = []

    class _MessageBox:
        class StandardButton:
            Yes = 1
            No = 2

        @staticmethod
        def information(_parent, title, text):
            events.append(("info", title, text))

        @staticmethod
        def question(*_args, **_kwargs):
            raise AssertionError("question should not be called")

    class _QtWidgets:
        QMessageBox = _MessageBox

    original_import = __import__

    def fake_import(name, *args, **kwargs):
        if name == "PySide6.QtWidgets":
            return _QtWidgets
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr("builtins.__import__", fake_import)

    window = _Window(model_name="")
    ctrl = ModelController(SimpleNamespace(active_profile=lambda: None), window)
    ctrl.delete_model(parent=None)

    assert events and events[0][0] == "info"
    assert window.async_calls == []


def test_delete_model_confirmed_runs_async(monkeypatch):
    class _MessageBox:
        class StandardButton:
            Yes = 1
            No = 2

        @staticmethod
        def information(*_args, **_kwargs):
            raise AssertionError("information should not be called")

        @staticmethod
        def question(*_args, **_kwargs):
            return _MessageBox.StandardButton.Yes

    class _QtWidgets:
        QMessageBox = _MessageBox

    original_import = __import__

    def fake_import(name, *args, **kwargs):
        if name == "PySide6.QtWidgets":
            return _QtWidgets
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr("builtins.__import__", fake_import)

    window = _Window(model_name="llama3:8b")
    ctrl = ModelController(SimpleNamespace(active_profile=lambda: SimpleNamespace()), window)

    monkeypatch.setattr("locallama_gui.ui.controllers.model_controller.create_backend", lambda _profile: SimpleNamespace(delete_model=lambda _name: None))

    ctrl.delete_model(parent=None)

    assert len(window.async_calls) == 1
    assert window.async_calls[0][1] == "Model deleted: llama3:8b"
