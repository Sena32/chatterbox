# Plan 003 — Stream de Mensagens via WebSocket

## Backend

### `websocket/connection_manager.py`

- Gerencia conexões ativas por `conversation_id` (dict simples em memória —
  suficiente para a POC de instância única).
- `connect(conversation_id, websocket)`, `disconnect(...)`,
  `send_json(conversation_id, payload)`.

### `websocket/chat_ws_controller.py`

- Endpoint `@app.websocket("/ws/conversations/{conversation_id}")`.
- Recebe mensagens do usuário via WS (`{"content": "..."}`).
- Delega para `ConversationService`, que por sua vez usa uma variante
  streaming do `AIService` (`AIService.stream_reply_to`), emitindo callback
  a cada chunk recebido do provedor.
- `AIProvider` ganha um método opcional `generate_reply_stream` (async
  generator). Provedores que não suportam streaming nativo podem "emular"
  quebrando a resposta completa em pedaços (apenas para a POC).

### Reuso de camadas

- **Não duplicar regra de negócio**: o WS controller chama o mesmo
  `ConversationService`/`AIService` da spec 002, apenas com um caminho de
  callback de streaming a mais. O controller HTTP (REST) continua existindo
  e funcionando normalmente (fallback sem streaming).

## Frontend

### `services/chatSocket.ts`

- Wrapper fino sobre `WebSocket` nativo: `connect(conversationId)`,
  `onChunk(cb)`, `onDone(cb)`, `onError(cb)`, `sendMessage(content)`,
  `disconnect()`. Sem JSX, sem estado React.

### `hooks/useChatSocket.ts`

- Usa `services/chatSocket.ts` internamente.
- Estado exposto: `streamingMessage` (texto parcial acumulado),
  `isStreaming`, `connectionStatus`.
- Ao receber `ai_message_done`, delega a atualização da lista definitiva de
  mensagens para `useConversation` (composição de hooks) ou centraliza tudo
  em um único hook `useConversation` que internamente usa `useChatSocket`
  como detalhe de implementação — decisão de implementação a ser tomada na
  task correspondente, respeitando a regra de "um hook, uma responsabilidade"
  sempre que possível.

### `components/Chat/StreamingMessageBubble.tsx`

- Apresentação pura da mensagem em construção (efeito "digitando"), recebe
  `content` parcial e `isStreaming` via props.

## Testes

- Backend: testar `ConnectionManager` isoladamente (unit). Testar
  `AIService.stream_reply_to` com `FakeAIProvider` que emite chunks
  conhecidos, validar que o texto final concatenado bate com o persistido.
- Frontend: teste do hook `useChatSocket` com um WebSocket mockado
  (ex: `vi.fn()` / mock-socket), validando transições de estado
  (`connecting → streaming → done`).

## Observação de escopo

Este é o requisito **opcional** — só deve ser iniciado após as specs 001 e
002 estarem completas e testadas.
