"""
AIService e AIProvider — abstração sobre o provedor de IA.

Estado: PLACEHOLDER (boilerplate)
Spec de referência: specs/002-ia-responde-com-objetivo/plan.md
Skill de referência: .cursor/skills/fastapi-layered-tdd/SKILL.md

TODO (tasks T2, T3, T4 da spec 002 — TDD):
  1. Definir Protocol AIProvider com generate_reply() e generate_reply_stream()
  2. Implementar FakeAIProvider para testes
  3. Escrever testes para AIService.reply_to() (system_goal injetado no prompt) — RED
  4. Implementar AIService — GREEN
  5. Implementar AnthropicProvider (real) em services/providers/anthropic_provider.py

O system_goal é lido de core/config.settings.ai_system_goal — nunca hardcoded aqui.

Estrutura esperada:
  class AIProvider(Protocol):
      async def generate_reply(system_prompt, history) -> str: ...
      async def generate_reply_stream(system_prompt, history) -> AsyncIterator[str]: ...

  class FakeAIProvider:
      async def generate_reply(...) -> str: return "Resposta fake da IA"
      async def generate_reply_stream(...) -> AsyncIterator[str]: yield "Resposta fake"

  class AIService:
      def __init__(self, provider: AIProvider, system_goal: str): ...
      async def reply_to(self, conversation) -> str: ...
      async def stream_reply_to(self, conversation) -> AsyncIterator[str]: ...
"""

# TODO: implementar — aguardando spec 002 tasks T1–T4
