from __future__ import annotations

from dataclasses import dataclass

from locallama_gui.core.domain import ChatMessage

INTERNAL_PROMPT_REDACTION = "[redacted app system prompt]"


@dataclass(frozen=True)
class ScrollRestorePlan:
    should_pin_bottom: bool
    previous_value: int


def compute_scroll_restore_plan(value: int, maximum: int, threshold: int = 120) -> ScrollRestorePlan:
    return ScrollRestorePlan(should_pin_bottom=(maximum - value) <= threshold, previous_value=value)


def message_is_internal_system(message: ChatMessage) -> bool:
    if message.role != "system":
        return False
    return bool(message.metadata.get("internal") or message.metadata.get("source") == "app")


def visible_chat_messages(messages: list[ChatMessage]) -> list[ChatMessage]:
    return [message for message in messages if not message_is_internal_system(message)]


def assistant_label(message: ChatMessage, active_model: str) -> str:
    if message.role != "assistant":
        return message.role.upper()
    model_name = str(message.metadata.get("model") or active_model).strip()
    return model_name if model_name else "ASSISTANT"


def redacted_request_messages(messages: list[ChatMessage]) -> list[dict[str, object]]:
    sanitized: list[dict[str, object]] = []
    for message in messages:
        content = message.content
        if message_is_internal_system(message):
            content = INTERNAL_PROMPT_REDACTION
        sanitized.append(
            {
                "role": message.role,
                "content": content,
                "id": message.id,
                "created_at": message.created_at,
                "name": message.name,
                "metadata": message.metadata,
            }
        )
    return sanitized
