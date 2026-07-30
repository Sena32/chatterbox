# Tasks 001 — Iniciar Conversa

## Backend

- [x] T1. Escrever teste de schema para `Message` e `Conversation` (falha) →
      criar `models/conversation.py` (passa).
- [ ] T2. Escrever teste de `ConversationRepository.create` (falha) →
      implementar (passa).
- [ ] T3. Escrever teste de `ConversationRepository.get_by_id` (falha) →
      implementar (passa).
- [ ] T4. Escrever teste de `ConversationRepository.add_message` (falha) →
      implementar (passa).
- [ ] T5. Escrever teste de `ConversationService.start_conversation` (mock do
      repository) → implementar.
- [ ] T6. Escrever teste de `ConversationService.get_conversation` (não
      encontrado deve levantar erro de domínio) → implementar.
- [ ] T7. Escrever teste de `ConversationService.post_user_message` →
      implementar.
- [ ] T8. Criar `controllers/conversation_controller.py` com as 3 rotas,
      registrar no `main.py`.
- [ ] T9. Teste de integração cobrindo o fluxo completo (criar → postar
      mensagem → buscar e conferir ordenação).

## Frontend

- [ ] T10. `services/conversationApi.ts` com as 3 chamadas HTTP (sem estado,
      sem JSX).
- [ ] T11. `hooks/useConversation.ts` com estado (`conversation`, `messages`,
      `isLoading`, `error`) e funções `startConversation`, `sendMessage`.
- [ ] T12. `components/Chat/MessageBubble.tsx` (apresentação pura, estilo por
      `sender`).
- [ ] T13. `components/Chat/ConversationView.tsx` (lista mensagens).
- [ ] T14. `components/Chat/MessageInput.tsx` (input controlado + callback).
- [ ] T15. `pages/ChatPage.tsx` compondo tudo via `useConversation`.
- [ ] T16. Testar manualmente: reload da página mantém histórico.
