"""Testes do FakeAIProvider (spec 002 T2)."""

from datetime import datetime, timezone

import pytest

from src.models.conversation import Message
from src.services.providers.fake_provider import FakeAIProvider


@pytest.mark.asyncio
async def test_fake_provider_returns_configured_reply():
    provider = FakeAIProvider(reply="Resposta fake da IA")
    history = [
        Message(
            id="1",
            sender="user",
            content="Olá",
            created_at=datetime.now(timezone.utc),
        )
    ]

    result = await provider.generate_reply("system prompt", history)

    assert result == "Resposta fake da IA"
    assert provider.last_system_prompt == "system prompt"
    assert provider.last_history == history


@pytest.mark.asyncio
async def test_fake_provider_generate_reply_stream_yields_configured_chunks():
    provider = FakeAIProvider(stream_chunks=["Hel", "lo", " world"])
    history = [
        Message(
            id="1",
            sender="user",
            content="Oi",
            created_at=datetime.now(timezone.utc),
        )
    ]

    chunks = [chunk async for chunk in provider.generate_reply_stream("sys", history)]

    assert chunks == ["Hel", "lo", " world"]
    assert provider.last_system_prompt == "sys"
    assert provider.last_history == history
