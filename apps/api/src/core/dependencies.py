"""Injeção de dependências FastAPI."""

from __future__ import annotations

from fastapi import Depends, Request
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.repositories.conversation_repository import ConversationRepository
from src.services.conversation_service import ConversationService


def get_db(request: Request) -> AsyncIOMotorDatabase:
    return request.app.state.db


def get_conversation_repository(
    db: AsyncIOMotorDatabase = Depends(get_db),
) -> ConversationRepository:
    return ConversationRepository(db)


def get_conversation_service(
    repository: ConversationRepository = Depends(get_conversation_repository),
) -> ConversationService:
    return ConversationService(repository=repository)
