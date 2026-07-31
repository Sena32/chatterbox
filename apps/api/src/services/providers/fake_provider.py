"""FakeAIProvider — implementação determinística para testes."""

from __future__ import annotations

from src.models.conversation import Message


class FakeAIProvider:
    def __init__(self, reply: str = "Resposta fake da IA") -> None:
        self._reply = reply
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
