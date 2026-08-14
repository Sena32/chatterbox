# Tasks 003 — Stream de Mensagens via WebSocket (Opcional)

## Backend

- [x] T1. Escrever teste unitário de `ConnectionManager` (connect/disconnect/
      send_json) → implementar.
- [x] T2. Estender `AIProvider`/`FakeAIProvider` com `generate_reply_stream`
      (async generator) → testar que `AIService.stream_reply_to` repassa os
      chunks corretamente.
- [x] T3. Implementar `GeminiProvider.generate_reply_stream` (streaming
      real via SDK, ou emulação por chunking se necessário).
- [x] T4. Criar `websocket/chat_ws_controller.py`, registrar rota WS no
      `main.py`, reutilizando `ConversationService`.
- [x] T5. Teste manual/integração: abrir WS, enviar mensagem, validar
      sequência de eventos `ai_message_chunk` → `ai_message_done` e
      persistência final no Mongo.

## Frontend

- [x] T6. `services/chatSocket.ts` (wrapper sobre WebSocket nativo).
- [x] T7. `hooks/useChatSocket.ts` com estados `streamingMessage`,
      `isStreaming`, `connectionStatus`.
- [x] T8. `components/Chat/StreamingMessageBubble.tsx` (apresentação pura).
- [x] T9. Integrar `useChatSocket` à `ChatPage`/`useConversation`, garantindo
      que ao terminar o streaming a mensagem definitiva substitua a "parcial".
- [x] T10. Testar fallback: se WS não conectar, REST da spec 002 continua
      funcionando (degradação suave).

## Infra / Backend

- [x] T11. Habilitar CORS na API (`CORSMiddleware` em `main.py`), com origens
      configuráveis em `core/config.py`, cobrindo rotas REST e handshake
      WebSocket — necessário quando o frontend acessa a API diretamente
      (sem proxy Vite) ou em deploy com origens distintas.
