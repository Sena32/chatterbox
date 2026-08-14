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
- `AIProvider` ganha um método `generate_reply_stream` (async generator).
  A implementação de produção usa `GeminiProvider` (Vertex AI / Google GenAI);
  provedores que não suportam streaming nativo emulam chunking da resposta
  completa (suficiente para a POC).

### Reuso de camadas

- **Não duplicar regra de negócio**: o WS controller chama o mesmo
  `ConversationService`/`AIService` da spec 002, apenas com um caminho de
  callback de streaming a mais. O controller HTTP (REST) continua existindo
  e funcionando normalmente (fallback sem streaming).

### CORS (infra transversal)

- Registrar `CORSMiddleware` em `apps/api/src/main.py` com origens
  configuráveis via `core/config.py` (ex.: `http://localhost:5173` em dev).
- Objetivo: frontend e API em origens distintas conseguirem REST **e**
  WebSocket sem bloqueio de preflight/CORS — complementar ao proxy do Vite,
  não substituto obrigatório em produção.
- WebSocket: o middleware CORS do Starlette/FastAPI cobre o handshake HTTP
  de upgrade; manter `allow_credentials=True` apenas se a POC passar cookies
  (não é o caso hoje).

## Frontend

### `services/chatSocket.ts`

- Wrapper fino sobre `WebSocket` nativo: `connect(conversationId)`,
  `onChunk(cb)`, `onDone(cb)`, `onError(cb)`, `sendMessage(content)`,
  `disconnect()`. Sem JSX, sem estado React.
- URL do WS: preferir mesma origem via proxy Vite (`/ws/...`) **ou**
  `VITE_WS_BASE_URL` apontando direto para a API quando CORS estiver
  habilitado (task T11).

### Ciclo de vida do `useChatSocket`

- `useConversation` chama `useChatSocket(conversation?.id ?? null)`.
- Enquanto `conversation` for `null` (antes de "Iniciar conversa"), o
  `useEffect` **executa**, mas retorna cedo — não abre socket (comportamento
  esperado).
- Após `setConversation(data)`, `conversationId` muda → `useEffect`
  reexecuta e chama `createChatSocket`.
- `isSocketReady` só fica `true` após evento `open` do WebSocket; enviar
  mensagem antes disso cai no fallback REST (T10).

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
