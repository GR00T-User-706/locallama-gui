from locallama_gui.core.domain import ChatMessage
from locallama_gui.ui.chat_view import (
    INTERNAL_PROMPT_REDACTION,
    assistant_label,
    backend_bound_messages,
    compute_scroll_restore_plan,
    redacted_request_messages,
    visible_chat_messages,
)


def test_scroll_restore_policy_near_bottom_pins():
    plan = compute_scroll_restore_plan(value=880, maximum=950, threshold=120)
    assert plan.should_pin_bottom is True


def test_scroll_restore_policy_scrolled_up_preserves_position():
    plan = compute_scroll_restore_plan(value=100, maximum=950, threshold=120)
    assert plan.should_pin_bottom is False
    assert plan.previous_value == 100


def test_visible_messages_exclude_internal_system():
    messages = [
        ChatMessage("system", "internal", metadata={"internal": True, "source": "app"}),
        ChatMessage("user", "hello"),
        ChatMessage("assistant", "world"),
    ]
    visible = visible_chat_messages(messages)
    assert [m.role for m in visible] == ["user", "assistant"]


def test_assistant_label_prefers_message_model_then_fallback_active_model():
    with_model = ChatMessage("assistant", "text", metadata={"model": "llama3.1:8b"})
    no_model = ChatMessage("assistant", "text")
    assert assistant_label(with_model, "ignored") == "llama3.1:8b"
    assert assistant_label(no_model, "active-model") == "active-model"


def test_request_redaction_only_for_internal_system_prompt():
    messages = [
        ChatMessage("system", "app secret", metadata={"internal": True, "source": "app"}),
        ChatMessage("system", "user system", metadata={"source": "user"}),
        ChatMessage("user", "hello"),
    ]
    redacted = redacted_request_messages(messages)
    assert redacted[0]["content"] == INTERNAL_PROMPT_REDACTION
    assert redacted[1]["content"] == "user system"
    assert redacted[2]["content"] == "hello"


def test_backend_bound_messages_excludes_empty_assistant_and_tool_messages():
    messages = [
        ChatMessage("system", ""),
        ChatMessage("user", ""),
        ChatMessage("assistant", ""),
        ChatMessage("assistant", "   \n"),
        ChatMessage("tool", ""),
        ChatMessage("tool", " \t "),
        ChatMessage("assistant", "answer"),
        ChatMessage("tool", "result"),
    ]

    sanitized = backend_bound_messages(messages)

    assert [(message.role, message.content) for message in sanitized] == [
        ("system", ""),
        ("user", ""),
        ("assistant", "answer"),
        ("tool", "result"),
    ]
