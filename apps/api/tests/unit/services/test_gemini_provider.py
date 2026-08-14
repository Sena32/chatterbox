"""Testes do GeminiProvider — streaming (spec 003 T3)."""

from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.models.conversation import Message
from src.services.providers.gemini_provider import GeminiProvider


@pytest.fixture
def sample_history():
    return [
        Message(
            id="1",
            sender="user",
            content="Olá",
            created_at=datetime.now(timezone.utc),
        )
    ]


@pytest.mark.asyncio
async def test_gemini_generate_reply_stream_yields_text_in_chunks(sample_history):
    provider = GeminiProvider(
        gcp_project_id="test-project",
        gcp_region="us-central1",
        model="gemini-test",
    )
    mock_response = MagicMock()
    mock_response.text = "Hello world"

    with patch.object(
        provider._client.aio.models,
        "generate_content",
        new_callable=AsyncMock,
        return_value=mock_response,
    ):
        chunks = [
            c
            async for c in provider.generate_reply_stream("system", sample_history)
        ]

    assert "".join(chunks) == "Hello world"
    assert len(chunks) >= 1
