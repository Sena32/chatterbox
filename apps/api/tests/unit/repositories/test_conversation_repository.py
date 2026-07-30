"""
Testes unitários do ConversationRepository (com Mongo em memória).

Estado: PLACEHOLDER — escrever testes ANTES de implementar o repository (TDD).
Spec: specs/001-iniciar-conversa/tasks.md — Tasks T2, T3, T4
Skill: .cursor/skills/mongodb-repository-pattern/SKILL.md

Exemplos de testes a escrever:
  - create() retorna Conversation com id preenchido e messages vazia
  - get_by_id() com id existente retorna a conversa correta
  - get_by_id() com id inexistente retorna None
  - add_message() adiciona mensagem e retorna conversa atualizada
"""

import pytest
from mongomock_motor import AsyncMongoMockClient


@pytest.fixture
async def conversation_repository(test_db):
    # TODO: importar e instanciar ConversationRepository quando implementado
    # from src.repositories.conversation_repository import ConversationRepository
    # return ConversationRepository(test_db)
    pass


# TODO (spec 001 tasks T2–T4):
# @pytest.mark.asyncio
# async def test_create_returns_conversation_with_id(conversation_repository):
#     ...
#
# async def test_get_by_id_returns_none_for_unknown(conversation_repository):
#     ...
#
# async def test_add_message_appends_to_conversation(conversation_repository):
#     ...
