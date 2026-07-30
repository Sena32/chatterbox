"""Testes unitários do ConversationRepository (Mongo em memória — spec 001 T2–T4)."""

from datetime import datetime, timezone

import pytest

from src.models.conversation import Message
from src.repositories.conversation_repository import ConversationRepository


@pytest.fixture
async def conversation_repository(test_db):
    return ConversationRepository(test_db)


@pytest.mark.asyncio
async def test_create_returns_conversation_with_id(conversation_repository):
    conversation = await conversation_repository.create()

    assert conversation.id is not None
    assert conversation.id != ""
    assert conversation.messages == []
    assert conversation.created_at is not None


@pytest.mark.asyncio
async def test_get_by_id_returns_conversation_when_exists(conversation_repository):
    created = await conversation_repository.create()

    found = await conversation_repository.get_by_id(created.id)

    assert found is not None
    assert found.id == created.id
    assert found.messages == []


@pytest.mark.asyncio
async def test_get_by_id_returns_none_for_unknown(conversation_repository):
    found = await conversation_repository.get_by_id("507f1f77bcf86cd799439011")

    assert found is None


@pytest.mark.asyncio
async def test_add_message_appends_to_conversation(conversation_repository):
    conversation = await conversation_repository.create()
    created_at = datetime.now(timezone.utc)
    message = Message(
        id="msg-uuid-1",
        sender="user",
        content="Olá",
        created_at=created_at,
    )

    updated = await conversation_repository.add_message(conversation.id, message)

    assert len(updated.messages) == 1
    assert updated.messages[0].id == "msg-uuid-1"
    assert updated.messages[0].sender == "user"
    assert updated.messages[0].content == "Olá"

    persisted = await conversation_repository.get_by_id(conversation.id)
    assert persisted is not None
    assert len(persisted.messages) == 1
    assert persisted.messages[0].content == "Olá"
