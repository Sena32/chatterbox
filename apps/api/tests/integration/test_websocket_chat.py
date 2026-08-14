"""Testes de integração — WebSocket de conversas (spec 003 T5)."""

import pytest
from starlette.testclient import TestClient

from src.core.config import settings
from src.core.dependencies import get_conversation_service, get_db
from src.main import app
from src.repositories.conversation_repository import ConversationRepository
from src.services.ai_service import AIService
from src.services.conversation_service import ConversationService
from src.services.providers.fake_provider import FakeAIProvider


@pytest.fixture
def ws_test_client(test_db):
    fake_provider = FakeAIProvider(stream_chunks=["chunk-", "final"])
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
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


def test_websocket_stream_emits_chunks_then_done_and_persists(ws_test_client):
    create_response = ws_test_client.post("/conversations")
    conversation_id = create_response.json()["id"]

    with ws_test_client.websocket_connect(
        f"/ws/conversations/{conversation_id}"
    ) as websocket:
        websocket.send_json({"content": "Olá via WS"})

        chunk_event = websocket.receive_json()
        assert chunk_event["type"] == "ai_message_chunk"
        assert chunk_event["conversation_id"] == conversation_id
        assert chunk_event["content"] == "chunk-"

        chunk_event_2 = websocket.receive_json()
        assert chunk_event_2["type"] == "ai_message_chunk"
        assert chunk_event_2["content"] == "final"

        done_event = websocket.receive_json()
        assert done_event["type"] == "ai_message_done"
        assert done_event["conversation_id"] == conversation_id
        assert done_event["message"]["sender"] == "ai"
        assert done_event["message"]["content"] == "chunk-final"

    get_response = ws_test_client.get(f"/conversations/{conversation_id}")
    messages = get_response.json()["messages"]
    assert len(messages) == 2
    assert messages[0]["sender"] == "user"
    assert messages[0]["content"] == "Olá via WS"
    assert messages[1]["sender"] == "ai"
    assert messages[1]["content"] == "chunk-final"
