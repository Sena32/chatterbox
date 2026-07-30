# Plan 002 — IA Responde com Objetivo

## Componentes novos

### `services/ai_service.py`

Abstração sobre o provedor de IA:

```python
class AIProvider(Protocol):
    async def generate_reply(self, system_prompt: str, history: list[Message]) -> str: ...

class AIService:
    def __init__(self, provider: AIProvider, system_goal: str): ...
    async def reply_to(self, conversation: Conversation) -> str: ...
```

- `system_goal` vem de `core/config.py` (lê `AI_SYSTEM_GOAL` do ambiente).
- `AIService.reply_to` monta o *system prompt* (ex: "Você é um assistente de
  chat. Seu objetivo nesta conversa é: {system_goal}. Responda de forma
  natural, mantendo esse objetivo.") e delega ao `provider`.
- Implementação concreta de `AIProvider` (ex: `AnthropicProvider`) vive em
  `services/providers/anthropic_provider.py`, isolando o SDK externo.
- Para testes, usar `FakeAIProvider` (retorna resposta fixa/determinística).

### Alteração em `services/conversation_service.py`

- `post_user_message` passa a, após persistir a mensagem do usuário, chamar
  `AIService.reply_to(conversation)` e persistir o resultado como mensagem
  `sender=ai` via `repository.add_message`.
- Tratamento de exceção: se `AIService` levantar `AIProviderError`, o service
  propaga um erro de domínio (`AIUnavailableError`) — a mensagem do usuário
  já foi salva antes dessa chamada, então não é revertida.

### `core/config.py`

- Centraliza leitura de env vars: `AI_PROVIDER`, `AI_API_KEY`, `AI_MODEL`,
  `AI_SYSTEM_GOAL`, `MONGO_URI`, `MONGO_DB_NAME`.
- Usar `pydantic-settings` (`BaseSettings`).

## Injeção de dependência

- `controllers/conversation_controller.py` recebe `ConversationService` via
  `Depends(...)` (FastAPI), que por sua vez recebe `AIService` já configurado
  com o provider real (produção) — testável trocando por `FakeAIProvider` nos
  testes de integração.

## Testes (TDD)

1. `tests/unit/services/test_ai_service.py`:
   - Testa que o *system prompt* contém o `system_goal` configurado.
   - Testa que `reply_to` delega corretamente ao `provider.generate_reply`
     com o histórico correto.
   - Testa propagação de erro quando o provider falha.
2. `tests/unit/services/test_conversation_service.py` (estender):
   - Ao chamar `post_user_message`, verificar que a mensagem da IA é
     persistida via repository (mockado) usando `FakeAIProvider`.
   - Testar cenário de falha do provider: mensagem do usuário permanece
     persistida, exceção de domínio é levantada.
3. `tests/integration/test_conversations_api.py` (estender):
   - `POST /conversations/{id}/messages` com `FakeAIProvider` injetado via
     override de dependência do FastAPI — valida resposta HTTP contém a
     mensagem da IA.

## Ordem sugerida de implementação

`core/config → AIProvider (Protocol) + FakeAIProvider (TDD) → AIService (TDD)
→ AnthropicProvider (implementação real, sem testes de unidade contra API
real) → integração no ConversationService (TDD) → wiring no controller
(Depends) → testes de integração`.
