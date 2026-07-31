"""Testes unitários do ConversationService (repository mockado — spec 001/002)."""

from datetime import datetime, timezone
from unittest.mock import AsyncMock

import pytest

from src.core.exceptions import (
    AIProviderError,
    AIUnavailableError,
    ConversationNotFoundError,
)
from src.models.conversation import Conversation, Message
from src.services.conversation_service import ConversationService


@pytest.fixture
def mock_repository():
    return AsyncMock()


@pytest.fixture
def mock_ai_service():
    return AsyncMock()


@pytest.fixture
def service(mock_repository, mock_ai_service):
    return ConversationService(
        repository=mock_repository,
        ai_service=mock_ai_service,
    )


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
async def test_post_user_message_persists_user_and_ai_messages(
    service, mock_repository, mock_ai_service
):
    conversation_id = "507f1f77bcf86cd799439011"
    now = datetime.now(timezone.utc)

    async def add_message_side_effect(cid, message):
        if message.sender == "user":
            return Conversation(id=cid, created_at=now, messages=[message])
        return Conversation(
            id=cid,
            created_at=now,
            messages=[
                Message(id="user-1", sender="user", content="Olá", created_at=now),
                message,
            ],
        )

    mock_repository.add_message.side_effect = add_message_side_effect
    mock_ai_service.reply_to.return_value = "Resposta da IA"

    result = await service.post_user_message(conversation_id, "Olá")

    assert mock_repository.add_message.await_count == 2
    mock_ai_service.reply_to.assert_awaited_once()

    user_call = mock_repository.add_message.call_args_list[0][0][1]
    assert user_call.sender == "user"
    assert user_call.content == "Olá"

    ai_call = mock_repository.add_message.call_args_list[1][0][1]
    assert ai_call.sender == "ai"
    assert ai_call.content == "Resposta da IA"

    assert result.sender == "ai"
    assert result.content == "Resposta da IA"


@pytest.mark.asyncio
async def test_post_user_message_keeps_user_message_when_ai_fails(
    service, mock_repository, mock_ai_service
):
    conversation_id = "507f1f77bcf86cd799439011"
    now = datetime.now(timezone.utc)

    async def add_message_side_effect(cid, message):
        return Conversation(id=cid, created_at=now, messages=[message])

    mock_repository.add_message.side_effect = add_message_side_effect
    mock_ai_service.reply_to.side_effect = AIProviderError("API timeout")

    with pytest.raises(AIUnavailableError) as exc_info:
        await service.post_user_message(conversation_id, "Olá")

    assert exc_info.value.conversation_id == conversation_id
    mock_repository.add_message.assert_awaited_once()
    user_message = mock_repository.add_message.call_args[0][1]
    assert user_message.sender == "user"
    assert user_message.content == "Olá"
