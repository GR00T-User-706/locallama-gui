from types import SimpleNamespace

from locallama_gui.core.domain import ChatSession
from locallama_gui.ui.controllers.chat_controller import ChatController
from locallama_gui.ui.controllers.model_controller import ModelController


class _FakeWindow:
    def __init__(self):
        self.generated = False
        self.logs = []
        self.tab = SimpleNamespace(
            session=ChatSession(provider="p", model="m"),
            input=SimpleNamespace(_text="", toPlainText=lambda: self.tab.input._text, clear=lambda: setattr(self.tab.input, "_text", "")),
        )

    def current_tab(self):
        return self.tab

    def set_tab_title(self, _title):
        pass

    def render_tab(self, _tab):
        pass

    def generate_for_tab(self, _tab):
        self.generated = True

    def refresh_sessions(self):
        pass

    def log(self, text):
        self.logs.append(text)


class _FakeSessions:
    def save(self, _session):
        pass


def test_chat_controller_invalid_prompt_no_crash():
    win = _FakeWindow()
    ctrl = ChatController(_FakeSessions(), SimpleNamespace(paths=SimpleNamespace(sessions_dir=None)), win)

    win.tab.input._text = "   "
    ctrl.send_message()

    assert win.generated is False
    assert win.tab.session.messages == []


def test_model_controller_invalid_model_name_no_crash(monkeypatch):
    class _Window:
        def __init__(self):
            self.added = []

        def model_name(self):
            return ""

        def append_terminal(self, _text):
            pass

        def refresh_backend(self):
            pass

        def add_worker(self, worker):
            self.added.append(worker)

        def run_async(self, *_args, **_kwargs):
            raise AssertionError("run_async should not be called")

        def open_modelfile_editor(self):
            pass

    class _InputDialog:
        @staticmethod
        def getText(*_args, **_kwargs):
            return "", True

    events = []

    class _MessageBox:
        @staticmethod
        def information(_parent, title, message):
            events.append((title, message))

    class _QtWidgets:
        QInputDialog = _InputDialog
        QMessageBox = _MessageBox

    original_import = __import__

    def fake_import(name, *args, **kwargs):
        if name == "PySide6.QtWidgets":
            return _QtWidgets
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr("builtins.__import__", fake_import)

    ctrl = ModelController(SimpleNamespace(active_profile=lambda: None), _Window())
    ctrl.pull_model(parent=None)
    ctrl.push_model(parent=None)

    assert events == [
        ("Pull Model", "Model name is required."),
        ("Push Model", "Model name is required."),
    ]
