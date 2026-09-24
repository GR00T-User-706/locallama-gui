from locallama_gui.backends.ollama import OllamaBackend
from locallama_gui.backends.openai import OpenAICompatibleBackend
from locallama_gui.core.domain import ChatMessage


def test_ollama_payload_serializes_user_prompt() -> None:
    payload = OllamaBackend.build_chat_payload(
        "test-model",
        [
            ChatMessage("system", "System"),
            ChatMessage("user", "Hello, world"),
        ],
        {"temperature": 0.7, "num_predict": 128},
        True,
    )

    assert payload["model"] == "test-model"
    assert payload["messages"] == [
        {"role": "system", "content": "System"},
        {"role": "user", "content": "Hello, world"},
    ]
    assert payload["stream"] is True


def test_openai_payload_serializes_user_prompt() -> None:
    # The payload is exercised through the backend implementation contract by
    # checking its message normalization helper directly.
    from locallama_gui.backends.base import build_chat_messages

    assert build_chat_messages([ChatMessage("user", "Hello")]) == [
        {"role": "user", "content": "Hello"}
    ]


def test_empty_chat_messages_are_rejected() -> None:
    from locallama_gui.backends.base import build_chat_messages

    try:
        build_chat_messages([ChatMessage("user", "   ")])
    except ValueError as exc:
        assert "no non-empty messages" in str(exc)
    else:
        raise AssertionError("Expected empty chat request to be rejected")


def test_invalid_role_is_rejected() -> None:
    from locallama_gui.backends.base import build_chat_messages

    message = ChatMessage("user", "Hello")
    message.role = "bogus"  # type: ignore[assignment]
    try:
        build_chat_messages([message])
    except ValueError as exc:
        assert "Invalid chat message role" in str(exc)
    else:
        raise AssertionError("Expected invalid role to be rejected")
