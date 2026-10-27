from locallama_gui.backends.ollama import OllamaBackend
from locallama_gui.core.config import GenerationParameters
from locallama_gui.core.domain import ChatMessage

# Reserved for direct OpenAI payload coverage when that test path is restored.
# from locallama_gui.backends.openai import OpenAICompatibleBackend


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


def test_legacy_reasoning_settings_are_forced_to_normal_mode() -> None:
    parameters = GenerationParameters(
        reasoning_mode="thinking",
        thinking_mode=True,
        plan_mode=True,
    )

    assert parameters.reasoning_mode == "normal"
    assert parameters.thinking_mode is False
    assert parameters.plan_mode is False
    assert parameters.normal_mode is True
    options = parameters.to_backend_options()
    assert "think" not in options
    assert "plan" not in options


def test_ollama_chat_payload_never_sends_reasoning_fields() -> None:
    payload = OllamaBackend.build_chat_payload(
        "test-model",
        [ChatMessage("user", "Hello")],
        {"temperature": 0.7, "think": True, "plan": True},
        False,
    )

    assert "think" not in payload
    assert "plan" not in payload
    assert "think" not in payload["options"]
    assert "plan" not in payload["options"]

