"""Testes de integração — endpoints REST da API de conversas (spec 001 T9)."""

import httpx
import pytest

from src.core.dependencies import get_db
from src.main import app


@pytest.fixture
async def client(test_db):
    app.dependency_overrides[get_db] = lambda: test_db
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
    first_message = first_message_response.json()
    assert first_message["sender"] == "user"
    assert first_message["content"] == "Primeira mensagem"

    second_message_response = await client.post(
        f"/conversations/{conversation_id}/messages",
        json={"content": "Segunda mensagem"},
    )
    assert second_message_response.status_code == 201
    second_message = second_message_response.json()
    assert second_message["sender"] == "user"
    assert second_message["content"] == "Segunda mensagem"

    get_response = await client.get(f"/conversations/{conversation_id}")
    assert get_response.status_code == 200
    conversation = get_response.json()
    assert conversation["id"] == conversation_id
    assert len(conversation["messages"]) == 2
    assert conversation["messages"][0]["content"] == "Primeira mensagem"
    assert conversation["messages"][1]["content"] == "Segunda mensagem"
    assert (
        conversation["messages"][0]["created_at"]
        <= conversation["messages"][1]["created_at"]
    )
