"""ConversationService — regras de negócio e orquestração."""

from datetime import datetime, timezone
from uuid import uuid4

from src.core.exceptions import (
    AIProviderError,
    AIUnavailableError,
    ConversationNotFoundError,
)
from src.models.conversation import Conversation, Message
from src.repositories.conversation_repository import ConversationRepository
from src.services.ai_service import AIService


class ConversationService:
    def __init__(
        self,
        repository: ConversationRepository,
        ai_service: AIService,
    ) -> None:
        self._repository = repository
        self._ai_service = ai_service

    async def start_conversation(self) -> Conversation:
        return await self._repository.create()

    async def get_conversation(self, conversation_id: str) -> Conversation:
        conversation = await self._repository.get_by_id(conversation_id)
        if conversation is None:
            raise ConversationNotFoundError(conversation_id)
        conversation.messages.sort(key=lambda m: m.created_at)
        return conversation

    async def post_user_message(self, conversation_id: str, content: str) -> Message:
        user_message = Message(
            id=str(uuid4()),
            sender="user",
            content=content,
            created_at=datetime.now(timezone.utc),
        )
        try:
            conversation = await self._repository.add_message(
                conversation_id,
                user_message,
            )
        except ValueError:
            raise ConversationNotFoundError(conversation_id) from None

        try:
            ai_content = await self._ai_service.reply_to(conversation)
        except AIProviderError:
            raise AIUnavailableError(conversation_id) from None

        ai_message = Message(
            id=str(uuid4()),
            sender="ai",
            content=ai_content,
            created_at=datetime.now(timezone.utc),
        )
        await self._repository.add_message(conversation_id, ai_message)
        return ai_message
