import json
from types import SimpleNamespace

from locallama_gui.core.config import APP_SYSTEM_PROMPT
from locallama_gui.core.domain import ChatMessage, ChatSession
from locallama_gui.ui.chat_view import INTERNAL_PROMPT_REDACTION
from locallama_gui.ui.main_window import MainWindow


class _Signal:
    def __init__(self):
        self.callbacks = []

    def connect(self, callback):
        self.callbacks.append(callback)


class _StreamTask:
    def __init__(self, iterator_factory):
        self.iterator_factory = iterator_factory
        self.token = _Signal()
        self.error = _Signal()
        self.completed = _Signal()
        self.started = False
        self.cancelled = False

    def start(self):
        self.started = True

    def cancel(self):
        self.cancelled = True


class _TextWidget:
    def __init__(self):
        self.text = ""

    def setPlainText(self, text):
        self.text = text

    def clear(self):
        self.text = ""


class _Tab:
    def __init__(self, messages=None):
        self.session = ChatSession(model="llama3", messages=list(messages or []))
        self.streaming = SimpleNamespace(isChecked=lambda: True)
        self.generating = False
        self.render_count = 0

    def set_generating(self, generating):
        self.generating = generating

    def render(self, _model=""):
        self.render_count += 1


class _Backend:
    def __init__(self):
        self.messages = None

    def chat(self, _model, messages, _options, _stream):
        self.messages = messages

        async def response():
            if False:
                yield ""

        return response()


class _LifecycleWindow:
    _finish_stream_message = MainWindow._finish_stream_message
    _stream_error = MainWindow._stream_error
    _stream_done = MainWindow._stream_done
    stop_generation = MainWindow.stop_generation

    def __init__(self, tab, current_tab=None):
        self._active_stream_owner = 7
        self._active_stream_tab = tab
        self._active_stream_message = tab.session.messages[-1]
        self.current_stream = _StreamTask(lambda: None)
        self.status = SimpleNamespace(showMessage=lambda message: setattr(self, "status_text", message))
        self.model_combo = SimpleNamespace(currentText=lambda: "llama3")
        self.sessions = SimpleNamespace(save=lambda session: setattr(self, "saved_session", session))
        self.current_tab_value = current_tab
        self.logs = []
        self.refresh_count = 0

    def current_tab(self):
        return self.current_tab_value

    def refresh_sessions(self):
        self.refresh_count += 1

    def log(self, text):
        self.logs.append(text)


def _generation_window(monkeypatch, backend, interceptors):
    profile = SimpleNamespace(
        name="Local Ollama",
        base_url="http://localhost:11434",
        default_model="",
    )
    window = SimpleNamespace(
        config=SimpleNamespace(
            active_profile=lambda: profile,
            parameters=SimpleNamespace(to_backend_options=lambda: {}),
        ),
        model_combo=SimpleNamespace(currentText=lambda: "llama3"),
        plugin_context=SimpleNamespace(chat_interceptors=interceptors),
        request_view=_TextWidget(),
        token_view=_TextWidget(),
        status=SimpleNamespace(showMessage=lambda _message: None),
        _stream_owner_seq=0,
        _active_stream_owner=None,
        _active_stream_tab=None,
        _active_stream_message=None,
        current_stream=None,
        worker_refs=[],
    )
    monkeypatch.setattr("locallama_gui.ui.main_window.create_backend", lambda _profile: backend)
    monkeypatch.setattr("locallama_gui.ui.main_window.StreamTask", _StreamTask)
    return window


def test_generate_filters_historical_and_plugin_injected_empty_messages(monkeypatch):
    historical = [
        ChatMessage("user", "hello"),
        ChatMessage("assistant", ""),
        ChatMessage("tool", "   "),
    ]
    tab = _Tab(historical)
    backend = _Backend()

    def inject_empty_messages(messages):
        return messages + [ChatMessage("assistant", "\n"), ChatMessage("tool", "")]

    window = _generation_window(monkeypatch, backend, [inject_empty_messages])

    MainWindow._generate(window, tab)
    window.current_stream.iterator_factory()

    assert [(message.role, message.content) for message in backend.messages] == [
        ("system", APP_SYSTEM_PROMPT),
        ("user", "hello"),
    ]
    preview = json.loads(window.request_view.text)
    assert preview["messages"] == [
        {"role": "system", "content": INTERNAL_PROMPT_REDACTION},
        {"role": "user", "content": "hello"},
    ]


def test_stream_error_removes_empty_placeholder_from_originating_tab(monkeypatch):
    owner_message = ChatMessage("assistant", "")
    owner_tab = _Tab([ChatMessage("user", "hello"), owner_message])
    other_tab = _Tab([ChatMessage("assistant", "other")])
    window = _LifecycleWindow(owner_tab, current_tab=other_tab)
    monkeypatch.setattr("locallama_gui.ui.main_window.QMessageBox.critical", lambda *_args: None)

    window._stream_error("failed", 7)

    assert owner_message not in owner_tab.session.messages
    assert owner_tab.generating is False
    assert owner_tab.render_count == 1
    assert other_tab.render_count == 0


def test_stream_error_preserves_partial_message_with_metadata(monkeypatch):
    message = ChatMessage("assistant", "partial")
    tab = _Tab([message])
    window = _LifecycleWindow(tab)
    monkeypatch.setattr("locallama_gui.ui.main_window.QMessageBox.critical", lambda *_args: None)

    window._stream_error("failed", 7)

    assert message in tab.session.messages
    assert message.metadata == {"error": True, "interrupted": True}


def test_stop_removes_empty_placeholder_and_preserves_partial_with_metadata():
    empty = ChatMessage("assistant", "")
    empty_tab = _Tab([empty])
    empty_window = _LifecycleWindow(empty_tab)
    stream = empty_window.current_stream

    empty_window.stop_generation()

    assert stream.cancelled is True
    assert empty not in empty_tab.session.messages

    partial = ChatMessage("assistant", "partial")
    partial_tab = _Tab([partial])
    partial_window = _LifecycleWindow(partial_tab)

    partial_window.stop_generation()

    assert partial in partial_tab.session.messages
    assert partial.metadata == {"canceled": True, "interrupted": True}


def test_successful_empty_response_removes_placeholder_before_save():
    message = ChatMessage("assistant", "   ")
    tab = _Tab([message])
    window = _LifecycleWindow(tab)

    window._stream_done(tab, 7)

    assert message not in tab.session.messages
    assert window.saved_session is tab.session
    assert window.refresh_count == 1
