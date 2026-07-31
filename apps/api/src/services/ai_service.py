"""AIService e AIProvider — abstração sobre o provedor de IA."""

from __future__ import annotations

from typing import Protocol

from src.core.exceptions import AIProviderError
from src.models.conversation import Conversation, Message


class AIProvider(Protocol):
    async def generate_reply(
        self,
        system_prompt: str,
        history: list[Message],
    ) -> str: ...


class AIService:
    def __init__(self, provider: AIProvider, system_goal: str) -> None:
        self._provider = provider
        self._system_goal = system_goal

    def _build_system_prompt(self) -> str:
        return (
            "Você é um assistente de chat. Seu objetivo nesta conversa é: "
            f"{self._system_goal}. Responda de forma natural, mantendo esse objetivo."
        )

    async def reply_to(self, conversation: Conversation) -> str:
        system_prompt = self._build_system_prompt()
        try:
            return await self._provider.generate_reply(
                system_prompt,
                conversation.messages,
            )
        except Exception as exc:
            print("console error ai service", str(exc))
            raise AIProviderError(str(exc)) from exc
