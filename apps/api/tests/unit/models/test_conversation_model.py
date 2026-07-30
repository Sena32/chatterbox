"""Testes de schema: Conversation e Message (spec 001 — T1)."""

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from src.models.conversation import Conversation, Message


def test_message_accepts_user_sender():
    msg = Message(
        id="msg-1",
        sender="user",
        content="Olá",
        created_at=datetime.now(timezone.utc),
    )
    assert msg.sender == "user"


def test_message_accepts_ai_sender():
    msg = Message(
        id="msg-2",
        sender="ai",
        content="Resposta",
        created_at=datetime.now(timezone.utc),
    )
    assert msg.sender == "ai"


def test_message_rejects_invalid_sender():
    with pytest.raises(ValidationError):
        Message(
            id="msg-3",
            sender="bot",
            content="oi",
            created_at=datetime.now(timezone.utc),
        )


def test_conversation_starts_with_empty_messages():
    conv = Conversation(
        id="conv-1",
        created_at=datetime.now(timezone.utc),
    )
    assert conv.messages == []


def test_conversation_id_is_string():
    conv = Conversation(
        id="507f1f77bcf86cd799439011",
        created_at=datetime.now(timezone.utc),
    )
    assert isinstance(conv.id, str)


def test_conversation_holds_message_list():
    created = datetime.now(timezone.utc)
    msg = Message(id="m1", sender="user", content="teste", created_at=created)
    conv = Conversation(id="c1", created_at=created, messages=[msg])
    assert len(conv.messages) == 1
    assert conv.messages[0].content == "teste"
