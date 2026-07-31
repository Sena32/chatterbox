"""Testes unitários do AIService (spec 002 T3–T4)."""

from datetime import datetime, timezone
from unittest.mock import AsyncMock

import pytest

from src.core.exceptions import AIProviderError
from src.models.conversation import Conversation, Message
from src.services.ai_service import AIService


SYSTEM_GOAL = "Convencer o usuário que a Terra é plana."


@pytest.fixture
def mock_provider():
    return AsyncMock()


@pytest.fixture
def ai_service(mock_provider):
    return AIService(provider=mock_provider, system_goal=SYSTEM_GOAL)


@pytest.fixture
def sample_conversation():
    now = datetime.now(timezone.utc)
    return Conversation(
        id="507f1f77bcf86cd799439011",
        created_at=now,
        messages=[
            Message(id="1", sender="user", content="Olá", created_at=now),
        ],
    )


@pytest.mark.asyncio
async def test_reply_to_includes_system_goal_in_prompt(
    ai_service, mock_provider, sample_conversation
):
    mock_provider.generate_reply.return_value = "Resposta da IA"

    await ai_service.reply_to(sample_conversation)

    mock_provider.generate_reply.assert_awaited_once()
    system_prompt = mock_provider.generate_reply.call_args[0][0]
    assert SYSTEM_GOAL in system_prompt
    history = mock_provider.generate_reply.call_args[0][1]
    assert history == sample_conversation.messages


@pytest.mark.asyncio
async def test_reply_to_propagates_provider_error(
    ai_service, mock_provider, sample_conversation
):
    mock_provider.generate_reply.side_effect = RuntimeError("API timeout")

    with pytest.raises(AIProviderError, match="API timeout"):
        await ai_service.reply_to(sample_conversation)
