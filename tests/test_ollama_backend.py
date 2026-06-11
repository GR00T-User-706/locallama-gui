import asyncio

import httpx

from locallama_gui.backends.ollama import OllamaBackend


class _FakeResponse:
    def __init__(self, payload=None, should_raise=False):
        self._payload = payload or {}
        self._should_raise = should_raise

    def raise_for_status(self):
        if self._should_raise:
            raise httpx.HTTPStatusError("boom", request=httpx.Request("GET", "http://test"), response=httpx.Response(500))

    def json(self):
        return self._payload


class _FakeAsyncClient:
    def __init__(self, response=None, error=None, **_kwargs):
        self._response = response
        self._error = error

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_exc):
        return None

    async def get(self, _url):
        if self._error:
            raise self._error
        return self._response

    async def post(self, _url, json=None):
        if self._error:
            raise self._error
        self.last_json = json
        return self._response or _FakeResponse(payload={"message": {"content": "ok"}})


class _FakeStreamResponse(_FakeResponse):
    def __init__(self, lines):
        super().__init__()
        self._lines = lines

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_exc):
        return None

    async def aiter_lines(self):
        for line in self._lines:
            yield line


class _FakeStreamClient(_FakeAsyncClient):
    def __init__(self, lines, **kwargs):
        super().__init__(**kwargs)
        self._lines = lines

    def stream(self, _method, _url, json=None):
        self.last_json = json
        return _FakeStreamResponse(self._lines)


def test_list_models_parses_missing_and_partial_fields(monkeypatch):
    payload = {
        "models": [
            {
                "name": "llama3",
                "size": 123,
                "details": {"parameter_size": "8B", "quantization_level": "Q4_K_M"},
                "model_info": {"llama.context_length": 8192},
            },
            {
                "name": "partial",
                "details": {"parameter_size": "3B"},
                "model_info": None,
            },
            {},
        ]
    }

    monkeypatch.setattr(
        "locallama_gui.backends.ollama.httpx.AsyncClient",
        lambda **kwargs: _FakeAsyncClient(response=_FakeResponse(payload=payload), **kwargs),
    )

    backend = OllamaBackend("http://localhost:11434")
    models = asyncio.run(backend.list_models())

    assert [m.name for m in models] == ["llama3", "partial", ""]
    assert models[0].parameter_size == "8B"
    assert models[0].quantization == "Q4_K_M"
    assert models[0].context_size == 8192
    assert models[1].size == 0
    assert models[1].quantization == ""
    assert models[1].context_size == 0
    assert models[2].size == 0
    assert models[2].parameter_size == ""


def test_test_connection_returns_disconnected_on_http_error(monkeypatch):
    monkeypatch.setattr(
        "locallama_gui.backends.ollama.httpx.AsyncClient",
        lambda **kwargs: _FakeAsyncClient(response=_FakeResponse(should_raise=True), **kwargs),
    )

    backend = OllamaBackend("http://localhost:11434")
    status = asyncio.run(backend.test_connection())

    assert status.state == "disconnected"
    assert "boom" in status.detail


def test_test_connection_returns_disconnected_on_timeout(monkeypatch):
    monkeypatch.setattr(
        "locallama_gui.backends.ollama.httpx.AsyncClient",
        lambda **kwargs: _FakeAsyncClient(error=httpx.TimeoutException("timeout"), **kwargs),
    )

    backend = OllamaBackend("http://localhost:11434")
    status = asyncio.run(backend.test_connection())

    assert status.state == "disconnected"
    assert "timeout" in status.detail


def test_chat_payload_emits_only_selected_reasoning_mode(monkeypatch):
    captured = {}

    class _CaptureClient(_FakeAsyncClient):
        async def post(self, _url, json=None):
            captured["payload"] = json
            return _FakeResponse(payload={"message": {"content": "ok"}})

    monkeypatch.setattr(
        "locallama_gui.backends.ollama.httpx.AsyncClient",
        lambda **kwargs: _CaptureClient(**kwargs),
    )

    backend = OllamaBackend("http://localhost:11434")
    asyncio.run(
        backend.chat(
            "llama3",
            [],
            {"temperature": 0.7, "plan": True, "think": True, "mirostat": 1},
            stream=False,
        ).__anext__()
    )

    assert captured["payload"]["think"] is True
    assert "plan" not in captured["payload"]["options"]
    assert "think" not in captured["payload"]["options"]
    assert "mirostat" not in captured["payload"]["options"]


def test_sanitize_options_preserves_supported_and_filters_invalid_and_stop_fragments():
    sanitized = OllamaBackend.sanitize_options(
        {
            "temperature": 0.5,
            "mirostat": 1,
            "tfs_z": 1.0,
            "think": True,
            "stop": ["", " <|eot_id|> ", "   "],
            "top_p": 0.95,
        }
    )

    assert sanitized["temperature"] == 0.5
    assert sanitized["top_p"] == 0.95
    assert sanitized["stop"] == ["<|eot_id|>"]
    assert "mirostat" not in sanitized
    assert "tfs_z" not in sanitized
    assert "think" not in sanitized


def test_sanitize_request_fields_only_forwards_supported_top_level_fields():
    request_fields = OllamaBackend.sanitize_request_fields({"think": True, "plan": True, "raw": True})

    assert request_fields == {"think": True}


def test_stream_endpoint_raises_for_successful_http_response_with_error_payload(monkeypatch):
    monkeypatch.setattr(
        "locallama_gui.backends.ollama.httpx.AsyncClient",
        lambda **kwargs: _FakeStreamClient(
            ['{"status":"pulling manifest"}', '{"error":"model not found"}'],
            **kwargs,
        ),
    )

    async def consume():
        backend = OllamaBackend("http://localhost:11434")
        return [chunk async for chunk in backend.pull_model("missing")]

    try:
        asyncio.run(consume())
    except RuntimeError as exc:
        assert str(exc) == "model not found"
    else:
        raise AssertionError("streamed Ollama errors must fail the operation")


def test_chat_payload_excludes_empty_assistant_and_tool_messages():
    from locallama_gui.core.domain import ChatMessage

    payload = OllamaBackend.build_chat_payload(
        "llama3",
        [
            ChatMessage("user", "hello"),
            ChatMessage("assistant", ""),
            ChatMessage("assistant", "   "),
            ChatMessage("tool", "\n"),
            ChatMessage("assistant", "answer"),
            ChatMessage("tool", "result"),
        ],
        {},
        False,
    )

    assert payload["messages"] == [
        {"role": "user", "content": "hello"},
        {"role": "assistant", "content": "answer"},
        {"role": "tool", "content": "result"},
    ]
