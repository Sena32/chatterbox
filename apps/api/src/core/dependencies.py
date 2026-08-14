"""Injeção de dependências FastAPI."""

from __future__ import annotations

from fastapi import Depends, Request, WebSocket
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.core.config import settings
from src.repositories.conversation_repository import ConversationRepository
from src.services.ai_service import AIService, AIProvider
from src.services.conversation_service import ConversationService
from src.services.providers.anthropic_provider import AnthropicProvider
from src.services.providers.gemini_provider import GeminiProvider
from src.services.providers.fake_provider import FakeAIProvider


def get_db(request: Request = None, websocket: WebSocket = None) -> AsyncIOMotorDatabase:
    """
    Dependência universal para Motor DB que extrai o estado 
    tanto de requisições HTTP quanto de conexões WebSocket.
    """
    ctx = request or websocket
    if not ctx:
        raise RuntimeError("Nenhum contexto HTTP ou WebSocket foi fornecido para a dependência get_db.")
        
    return ctx.app.state.db


def get_conversation_repository(
    db: AsyncIOMotorDatabase = Depends(get_db),
) -> ConversationRepository:
    return ConversationRepository(db)


def get_ai_provider() -> AIProvider:
    if settings.ai_provider == "anthropic":
        return AnthropicProvider(
            gcp_project_id=settings.gcp_project_id,
            region=settings.gcp_region,
            model=settings.ai_model,
        )
    elif settings.ai_provider == "gemini":
        return GeminiProvider(
            gcp_project_id=settings.gcp_project_id,
            gcp_region=settings.gcp_region,
            model=settings.ai_model
        )
    return FakeAIProvider()


def get_ai_service(
    provider: AIProvider = Depends(get_ai_provider),
) -> AIService:
    return AIService(provider=provider, system_goal=settings.ai_system_goal)


def get_conversation_service(
    repository: ConversationRepository = Depends(get_conversation_repository),
    ai_service: AIService = Depends(get_ai_service),
) -> ConversationService:
    return ConversationService(repository=repository, ai_service=ai_service)
