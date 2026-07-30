# Tasks 003 — Stream de Mensagens via WebSocket (Opcional)

## Backend

- [ ] T1. Escrever teste unitário de `ConnectionManager` (connect/disconnect/
      send_json) → implementar.
- [ ] T2. Estender `AIProvider`/`FakeAIProvider` com `generate_reply_stream`
      (async generator) → testar que `AIService.stream_reply_to` repassa os
      chunks corretamente.
- [ ] T3. Implementar `AnthropicProvider.generate_reply_stream` (streaming
      real via SDK, ou emulação por chunking se necessário).
- [ ] T4. Criar `websocket/chat_ws_controller.py`, registrar rota WS no
      `main.py`, reutilizando `ConversationService`.
- [ ] T5. Teste manual/integração: abrir WS, enviar mensagem, validar
      sequência de eventos `ai_message_chunk` → `ai_message_done` e
      persistência final no Mongo.

## Frontend

- [ ] T6. `services/chatSocket.ts` (wrapper sobre WebSocket nativo).
- [ ] T7. `hooks/useChatSocket.ts` com estados `streamingMessage`,
      `isStreaming`, `connectionStatus`.
- [ ] T8. `components/Chat/StreamingMessageBubble.tsx` (apresentação pura).
- [ ] T9. Integrar `useChatSocket` à `ChatPage`/`useConversation`, garantindo
      que ao terminar o streaming a mensagem definitiva substitua a "parcial".
- [ ] T10. Testar fallback: se WS não conectar, REST da spec 002 continua
      funcionando (degradação suave).
