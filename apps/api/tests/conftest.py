"""
Fixtures compartilhadas entre todos os testes da API.

Adicione aqui fixtures reutilizáveis (ex: cliente HTTP de integração,
banco de teste, instâncias de fake providers).
"""

import pytest
from mongomock_motor import AsyncMongoMockClient


@pytest.fixture
async def test_db():
    """Banco MongoDB em memória para testes unitários de repository."""
    client = AsyncMongoMockClient()
    yield client["test_chatterbox"]
    # mongomock não precisa de cleanup explícito


# TODO (spec 001 task T9 / spec 002 task T9):
# Adicionar fixture de AsyncClient (httpx) apontando para a app FastAPI
# com overrides de dependência (FakeAIProvider, banco de teste)
