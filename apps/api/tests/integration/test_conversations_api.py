"""
Testes de integração — endpoints REST da API de conversas.

Estado: PLACEHOLDER — implementar após services e repositories estarem prontos.
Spec: specs/001-iniciar-conversa/tasks.md — Task T9
      specs/002-ia-responde-com-objetivo/tasks.md — Task T9

Cenários a cobrir:
  - POST /conversations retorna 201 com id
  - GET  /conversations/{id} retorna conversa com messages[]
  - GET  /conversations/{id} com id inválido retorna 404
  - POST /conversations/{id}/messages persiste msg do user e retorna msg da IA
  - POST /conversations/{id}/messages com AIService falhando retorna 503
    e a msg do user foi salva (GET seguinte mostra)

Setup:
  - Usar httpx.AsyncClient com ASGITransport apontando para app FastAPI
  - Sobrescrever dependência do AIService com FakeAIProvider
  - Sobrescrever dependência do MongoDB com banco de teste em memória
"""

import pytest

# TODO (spec 001 task T9 + spec 002 task T9):
# import httpx
# from src.main import app
#
# @pytest.fixture
# async def client():
#     # Override de dependências aqui (FakeAIProvider, db de teste)
#     async with httpx.AsyncClient(
#         transport=httpx.ASGITransport(app=app), base_url="http://test"
#     ) as c:
#         yield c
#
# async def test_create_conversation(client):
#     response = await client.post("/conversations")
#     assert response.status_code == 201
#     assert "id" in response.json()
