"""FakeAIProvider — implementação determinística para testes."""

from __future__ import annotations

from collections.abc import AsyncIterator

from src.models.conversation import Message


class FakeAIProvider:
    def __init__(
        self,
        reply: str = "Resposta fake da IA",
        stream_chunks: list[str] | None = None,
    ) -> None:
        self._reply = reply
        self._stream_chunks = stream_chunks
        self.last_system_prompt: str | None = None
        self.last_history: list[Message] | None = None

    async def generate_reply(
        self,
        system_prompt: str,
        history: list[Message],
    ) -> str:
        self.last_system_prompt = system_prompt
        self.last_history = history
        return self._reply

    async def generate_reply_stream(
        self,
        system_prompt: str,
        history: list[Message],
    ) -> AsyncIterator[str]:
        self.last_system_prompt = system_prompt
        self.last_history = history
        chunks = self._stream_chunks if self._stream_chunks is not None else [self._reply]
        for chunk in chunks:
            yield chunk
