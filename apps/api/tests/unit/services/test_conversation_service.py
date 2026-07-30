"""
Testes unitários do ConversationService (repository e AIService mockados).

Estado: PLACEHOLDER — escrever testes ANTES de implementar o service (TDD).
Spec: specs/001-iniciar-conversa/tasks.md — Tasks T5, T6, T7
      specs/002-ia-responde-com-objetivo/tasks.md — Tasks T5, T6
Skill: .cursor/skills/fastapi-layered-tdd/SKILL.md

Exemplos de testes a escrever:
  [Spec 001]
  - start_conversation() chama repository.create() e retorna Conversation
  - get_conversation() com id inexistente levanta ConversationNotFoundError
  - post_user_message() chama repository.add_message() com sender="user"

  [Spec 002]
  - post_user_message() após persistir user msg chama ai_service.reply_to()
  - post_user_message() persiste resposta da IA com sender="ai"
  - post_user_message() com AIService falhando: msg do user permanece salva,
    AIUnavailableError é propagado
"""

import pytest
from unittest.mock import AsyncMock


# TODO (spec 001 tasks T5–T7 + spec 002 tasks T5–T6):
# from src.services.conversation_service import ConversationService
#
# @pytest.fixture
# def mock_repository():
#     return AsyncMock()
#
# @pytest.fixture
# def mock_ai_service():
#     return AsyncMock()
#
# @pytest.fixture
# def service(mock_repository, mock_ai_service):
#     return ConversationService(repository=mock_repository, ai_service=mock_ai_service)
#
# async def test_start_conversation_delegates_to_repository(service, mock_repository):
#     ...
