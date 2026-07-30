"""ConversationController — rotas REST para conversas."""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from src.core.dependencies import get_conversation_service
from src.core.exceptions import ConversationNotFoundError
from src.models.conversation import Conversation, Message
from src.services.conversation_service import ConversationService

router = APIRouter()


class PostMessageRequest(BaseModel):
    content: str


@router.post("", status_code=status.HTTP_201_CREATED, response_model=Conversation)
async def create_conversation(
    service: ConversationService = Depends(get_conversation_service),
) -> Conversation:
    return await service.start_conversation()


@router.get("/{conversation_id}", response_model=Conversation)
async def get_conversation(
    conversation_id: str,
    service: ConversationService = Depends(get_conversation_service),
) -> Conversation:
    try:
        return await service.get_conversation(conversation_id)
    except ConversationNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )


@router.post(
    "/{conversation_id}/messages",
    status_code=status.HTTP_201_CREATED,
    response_model=Message,
)
async def post_message(
    conversation_id: str,
    body: PostMessageRequest,
    service: ConversationService = Depends(get_conversation_service),
) -> Message:
    try:
        return await service.post_user_message(conversation_id, body.content)
    except ConversationNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )
