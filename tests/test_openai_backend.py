import asyncio

from locallama_gui.backends.openai import OpenAICompatibleBackend
from locallama_gui.core.domain import ChatMessage


class _FakeResponse:
    def raise_for_status(self):
        return None

    def json(self):
        return {"choices": [{"message": {"content": "ok"}}]}


class _FakeAsyncClient:
    def __init__(self, captured, **_kwargs):
        self.captured = captured

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_exc):
        return None

    async def post(self, _url, json=None):
        self.captured["payload"] = json
        return _FakeResponse()


def test_openai_payload_excludes_empty_assistant_and_tool_messages(monkeypatch):
    captured = {}
    monkeypatch.setattr(
        "locallama_gui.backends.openai.httpx.AsyncClient",
        lambda **kwargs: _FakeAsyncClient(captured, **kwargs),
    )
    backend = OpenAICompatibleBackend("http://localhost:8000/v1")
    messages = [
        ChatMessage("user", "hello"),
        ChatMessage("assistant", ""),
        ChatMessage("assistant", "   "),
        ChatMessage("tool", "\n"),
        ChatMessage("assistant", "answer"),
        ChatMessage("tool", "result"),
    ]

    asyncio.run(backend.chat("model", messages, {}, False).__anext__())

    assert captured["payload"]["messages"] == [
        {"role": "user", "content": "hello"},
        {"role": "assistant", "content": "answer"},
        {"role": "tool", "content": "result"},
    ]
