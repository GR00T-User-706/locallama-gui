from types import SimpleNamespace

from locallama_gui.core.domain import ChatMessage, ChatSession
from locallama_gui.ui.controllers.chat_controller import ChatController


class FakeWindow:
    def __init__(self, session):
        self.tab = SimpleNamespace(session=session, input=SimpleNamespace(_text="", toPlainText=lambda: self.tab.input._text, clear=lambda: setattr(self.tab.input, "_text", "")))
        self.title = ""
        self.generated = False
        self.saved = False
        self.logs = []

    def current_tab(self):
        return self.tab

    def set_tab_title(self, title):
        self.title = title

    def render_tab(self, tab):
        pass

    def generate_for_tab(self, tab):
        self.generated = True

    def refresh_sessions(self):
        self.saved = True

    def log(self, text):
        self.logs.append(text)

    def open_session(self, session_id):
        self.opened = session_id


class FakeSessions:
    def save(self, session):
        self.last = session


def test_send_and_regenerate_regression():
    session = ChatSession(provider="p", model="m")
    window = FakeWindow(session)
    sessions = FakeSessions()
    controller = ChatController(sessions, SimpleNamespace(paths=SimpleNamespace(sessions_dir=None)), window)

    window.tab.input._text = "hello"
    controller.send_message()
    assert session.messages[-1].role == "user"
    assert window.generated is True

    session.messages.append(ChatMessage("assistant", "answer"))
    window.generated = False
    controller.regenerate()
    assert session.messages[-1].role == "user"
    assert window.generated is True


def test_save_current_regression():
    session = ChatSession(provider="p", model="m")
    window = FakeWindow(session)
    sessions = FakeSessions()
    controller = ChatController(sessions, SimpleNamespace(paths=SimpleNamespace(sessions_dir=None)), window)

    controller.save_current()
    assert sessions.last is session
    assert window.saved is True
    assert "Saved chat session" in window.logs

from locallama_gui.ui.controllers.model_controller import ModelController
from locallama_gui.ui.controllers.plugin_controller import PluginController


def test_model_create_delegates_to_editor():
    called = {"open": False}

    class ModelWindow:
        def open_modelfile_editor(self):
            called["open"] = True

    ctrl = ModelController(SimpleNamespace(active_profile=lambda: None), ModelWindow())
    ctrl.create_model()
    assert called["open"] is True


def test_plugin_reload_regression():
    called = {"reload": False}

    class Plugins:
        def reload(self):
            called["reload"] = True

    class PWindow:
        def __init__(self):
            self.logs = []

        def log(self, text):
            self.logs.append(text)

    win = PWindow()
    ctrl = PluginController(Plugins(), SimpleNamespace(paths=SimpleNamespace(plugins_dir=None)), win)
    ctrl.reload_plugins()
    assert called["reload"] is True
    assert "Plugins reloaded" in win.logs
