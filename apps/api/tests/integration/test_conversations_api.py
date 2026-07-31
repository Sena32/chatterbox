"""Testes de integração — endpoints REST da API de conversas (spec 001/002)."""

import httpx
import pytest

from src.core.config import settings
from src.core.dependencies import get_conversation_service, get_db
from src.main import app
from src.repositories.conversation_repository import ConversationRepository
from src.services.ai_service import AIService
from src.services.conversation_service import ConversationService
from src.services.providers.fake_provider import FakeAIProvider


@pytest.fixture
async def client(test_db):
    fake_provider = FakeAIProvider(reply="Resposta fake da IA")
    ai_service = AIService(
        provider=fake_provider,
        system_goal=settings.ai_system_goal,
    )

    def override_get_conversation_service() -> ConversationService:
        return ConversationService(
            repository=ConversationRepository(test_db),
            ai_service=ai_service,
        )

    app.dependency_overrides[get_db] = lambda: test_db
    app.dependency_overrides[get_conversation_service] = override_get_conversation_service
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_full_conversation_flow_create_post_and_get_ordered(client):
    create_response = await client.post("/conversations")
    assert create_response.status_code == 201
    conversation_id = create_response.json()["id"]
    assert conversation_id

    first_message_response = await client.post(
        f"/conversations/{conversation_id}/messages",
        json={"content": "Primeira mensagem"},
    )
    assert first_message_response.status_code == 201
    first_ai_message = first_message_response.json()
    assert first_ai_message["sender"] == "ai"
    assert first_ai_message["content"] == "Resposta fake da IA"

    second_message_response = await client.post(
        f"/conversations/{conversation_id}/messages",
        json={"content": "Segunda mensagem"},
    )
    assert second_message_response.status_code == 201
    second_ai_message = second_message_response.json()
    assert second_ai_message["sender"] == "ai"
    assert second_ai_message["content"] == "Resposta fake da IA"

    get_response = await client.get(f"/conversations/{conversation_id}")
    assert get_response.status_code == 200
    conversation = get_response.json()
    assert conversation["id"] == conversation_id
    assert len(conversation["messages"]) == 4
    assert conversation["messages"][0]["content"] == "Primeira mensagem"
    assert conversation["messages"][0]["sender"] == "user"
    assert conversation["messages"][1]["sender"] == "ai"
    assert conversation["messages"][2]["content"] == "Segunda mensagem"
    assert conversation["messages"][2]["sender"] == "user"
    assert conversation["messages"][3]["sender"] == "ai"
    assert (
        conversation["messages"][0]["created_at"]
        <= conversation["messages"][1]["created_at"]
    )


@pytest.mark.asyncio
async def test_post_message_returns_ai_response_with_fake_provider(client):
    create_response = await client.post("/conversations")
    conversation_id = create_response.json()["id"]

    response = await client.post(
        f"/conversations/{conversation_id}/messages",
        json={"content": "A Terra é redonda?"},
    )

    assert response.status_code == 201
    ai_message = response.json()
    assert ai_message["sender"] == "ai"
    assert ai_message["content"] == "Resposta fake da IA"

    get_response = await client.get(f"/conversations/{conversation_id}")
    messages = get_response.json()["messages"]
    assert len(messages) == 2
    assert messages[0]["sender"] == "user"
    assert messages[0]["content"] == "A Terra é redonda?"
    assert messages[1]["sender"] == "ai"


@pytest.mark.asyncio
async def test_post_message_returns_503_when_ai_fails(test_db):
    class FailingProvider:
        async def generate_reply(self, system_prompt, history):
            raise RuntimeError("API timeout")

    ai_service = AIService(
        provider=FailingProvider(),
        system_goal=settings.ai_system_goal,
    )

    def override_get_conversation_service() -> ConversationService:
        return ConversationService(
            repository=ConversationRepository(test_db),
            ai_service=ai_service,
        )

    app.dependency_overrides[get_db] = lambda: test_db
    app.dependency_overrides[get_conversation_service] = override_get_conversation_service
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        create_response = await client.post("/conversations")
        conversation_id = create_response.json()["id"]

        response = await client.post(
            f"/conversations/{conversation_id}/messages",
            json={"content": "Olá"},
        )

        assert response.status_code == 503

        get_response = await client.get(f"/conversations/{conversation_id}")
        messages = get_response.json()["messages"]
        assert len(messages) == 1
        assert messages[0]["sender"] == "user"
        assert messages[0]["content"] == "Olá"

    app.dependency_overrides.clear()
