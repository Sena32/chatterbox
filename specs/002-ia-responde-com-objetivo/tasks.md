# Tasks 002 — IA Responde com Objetivo

## Backend

- [x] T1. Criar `core/config.py` com `Settings` (pydantic-settings) lendo as
      env vars de IA e Mongo.
- [x] T2. Definir `AIProvider` (Protocol) e `FakeAIProvider` em
      `services/ai_service.py` / `services/providers/fake_provider.py`.
- [x] T3. Escrever teste: `AIService.reply_to` inclui `system_goal` no
      prompt enviado ao provider (falha) → implementar `AIService` (passa).
- [x] T4. Escrever teste: `AIService.reply_to` propaga erro quando o provider
      lança exceção (falha) → implementar tratamento (passa).
- [x] T5. Estender teste de `ConversationService.post_user_message` para
      cobrir persistência da resposta da IA (falha) → implementar chamada ao
      `AIService` + `repository.add_message` (passa).
- [x] T6. Estender teste para cenário de falha do `AIService` (mensagem do
      usuário permanece salva) → implementar tratamento de erro no service.
- [x] T7. Implementar `services/providers/anthropic_provider.py` (implementação
      real do `AIProvider`, sem cobertura de teste unitário contra API real —
      apenas smoke test manual).
- [x] T8. Ajustar `controllers/conversation_controller.py` para injetar
      `ConversationService` com `AIService` real via `Depends`.
- [x] T9. Teste de integração: `POST /conversations/{id}/messages` retorna
      mensagem da IA usando `FakeAIProvider` (override de dependência).

## Frontend

- [x] T10. Atualizar `hooks/useConversation.ts`: após `sendMessage`, refletir
      também a mensagem de resposta da IA vinda do backend no estado local.
- [x] T11. Tratar estado de erro (`error`) quando a IA falhar — exibir aviso
      simples na UI sem quebrar a conversa existente.
