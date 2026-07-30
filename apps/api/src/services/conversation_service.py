"""ConversationService — regras de negócio e orquestração."""

from datetime import datetime, timezone
from uuid import uuid4

from src.core.exceptions import ConversationNotFoundError
from src.models.conversation import Conversation, Message
from src.repositories.conversation_repository import ConversationRepository


class ConversationService:
    def __init__(self, repository: ConversationRepository) -> None:
        self._repository = repository

    async def start_conversation(self) -> Conversation:
        return await self._repository.create()

    async def get_conversation(self, conversation_id: str) -> Conversation:
        conversation = await self._repository.get_by_id(conversation_id)
        if conversation is None:
            raise ConversationNotFoundError(conversation_id)
        conversation.messages.sort(key=lambda m: m.created_at)
        return conversation

    async def post_user_message(self, conversation_id: str, content: str) -> Message:
        message = Message(
            id=str(uuid4()),
            sender="user",
            content=content,
            created_at=datetime.now(timezone.utc),
        )
        try:
            await self._repository.add_message(conversation_id, message)
        except ValueError:
            raise ConversationNotFoundError(conversation_id) from None
        return message
