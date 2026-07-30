"""Testes unitários do ConversationService (repository mockado — spec 001 T5–T7)."""

from datetime import datetime, timezone
from unittest.mock import AsyncMock

import pytest

from src.core.exceptions import ConversationNotFoundError
from src.models.conversation import Conversation, Message
from src.services.conversation_service import ConversationService


@pytest.fixture
def mock_repository():
    return AsyncMock()


@pytest.fixture
def service(mock_repository):
    return ConversationService(repository=mock_repository)


@pytest.mark.asyncio
async def test_start_conversation_delegates_to_repository(service, mock_repository):
    expected = Conversation(
        id="507f1f77bcf86cd799439011",
        created_at=datetime.now(timezone.utc),
        messages=[],
    )
    mock_repository.create.return_value = expected

    result = await service.start_conversation()

    mock_repository.create.assert_awaited_once()
    assert result == expected


@pytest.mark.asyncio
async def test_get_conversation_raises_when_not_found(service, mock_repository):
    conversation_id = "507f1f77bcf86cd799439011"
    mock_repository.get_by_id.return_value = None

    with pytest.raises(ConversationNotFoundError) as exc_info:
        await service.get_conversation(conversation_id)

    assert exc_info.value.conversation_id == conversation_id
    mock_repository.get_by_id.assert_awaited_once_with(conversation_id)


@pytest.mark.asyncio
async def test_post_user_message_persists_user_message(service, mock_repository):
    conversation_id = "507f1f77bcf86cd799439011"
    now = datetime.now(timezone.utc)

    async def add_message_side_effect(cid, message):
        return Conversation(id=cid, created_at=now, messages=[message])

    mock_repository.add_message.side_effect = add_message_side_effect

    result = await service.post_user_message(conversation_id, "Olá")

    mock_repository.add_message.assert_awaited_once()
    call_args = mock_repository.add_message.call_args
    assert call_args[0][0] == conversation_id
    persisted_message = call_args[0][1]
    assert isinstance(persisted_message, Message)
    assert persisted_message.sender == "user"
    assert persisted_message.content == "Olá"
    assert persisted_message.id
    assert persisted_message.created_at
    assert result.sender == "user"
    assert result.content == "Olá"
    assert result.id == persisted_message.id
