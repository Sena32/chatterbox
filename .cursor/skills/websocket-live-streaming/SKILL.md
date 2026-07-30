---
name: websocket-live-streaming
description: Use esta skill ao implementar qualquer funcionalidade relacionada ao endpoint WebSocket em apps/api/src/websocket/ ou ao hook useChatSocket em apps/web/src/hooks/. Cobre o padrão de streaming de chunks de IA via WS, gerenciamento de conexão e integração com o ConversationService existente.
---

# WebSocket Live Streaming — FastAPI ↔ React

## Visão geral do fluxo

```
[React useChatSocket]
      │  ws.send({ content: "msg do user" })
      ▼
[FastAPI /ws/conversations/{id}]
      │  ConversationService.post_user_message (persiste user msg)
      │  AIService.stream_reply_to (async generator)
      │    ├─ ws.send_json({ type: "ai_message_chunk", content: "..." })   × N
      │    └─ ws.send_json({ type: "ai_message_done", message: {...} })    × 1
      ▼
[React useChatSocket]
      │  onChunk → acumula em streamingMessage (estado local)
      └─ onDone  → atualiza lista definitiva de mensagens
```

## Backend — WebSocket Controller

```python
# src/websocket/chat_ws_controller.py
from fastapi import WebSocket, WebSocketDisconnect
from src.websocket.connection_manager import ConnectionManager
from src.services.conversation_service import ConversationService

manager = ConnectionManager()

async def ws_conversation_endpoint(
    websocket: WebSocket,
    conversation_id: str,
    service: ConversationService,  # injetado via Depends no registro da rota
):
    await manager.connect(conversation_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            content = data.get("content", "")

            # Persiste msg do usuário
            await service.add_user_message(conversation_id, content)

            # Streaming da IA
            full_response = ""
            async for chunk in service.stream_ai_reply(conversation_id):
                full_response += chunk
                await websocket.send_json({
                    "type": "ai_message_chunk",
                    "content": chunk,
                })

            # Persiste msg final e notifica cliente
            ai_message = await service.finalize_ai_message(conversation_id, full_response)
            await websocket.send_json({
                "type": "ai_message_done",
                "message": ai_message.model_dump(),
            })

    except WebSocketDisconnect:
        manager.disconnect(conversation_id, websocket)
    except Exception as e:
        await websocket.send_json({"type": "error", "message": str(e)})
        manager.disconnect(conversation_id, websocket)
```

## Backend — ConnectionManager

```python
# src/websocket/connection_manager.py
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        # Simples para a POC (instância única)
        self._connections: dict[str, list[WebSocket]] = {}

    async def connect(self, conversation_id: str, ws: WebSocket):
        await ws.accept()
        self._connections.setdefault(conversation_id, []).append(ws)

    def disconnect(self, conversation_id: str, ws: WebSocket):
        conns = self._connections.get(conversation_id, [])
        if ws in conns:
            conns.remove(ws)
```

## Frontend — Service (sem React)

```typescript
// src/services/chatSocket.ts
const WS_BASE = import.meta.env.VITE_WS_BASE_URL

export type ChunkHandler = (chunk: string) => void
export type DoneHandler  = (message: import("../types").Message) => void
export type ErrorHandler = (msg: string) => void

export function createChatSocket(conversationId: string) {
  const ws = new WebSocket(`${WS_BASE}/ws/conversations/${conversationId}`)

  return {
    onChunk(cb: ChunkHandler)  { ws.addEventListener("message", e => {
      const d = JSON.parse(e.data)
      if (d.type === "ai_message_chunk") cb(d.content)
    })},
    onDone(cb: DoneHandler)    { ws.addEventListener("message", e => {
      const d = JSON.parse(e.data)
      if (d.type === "ai_message_done") cb(d.message)
    })},
    onError(cb: ErrorHandler)  { ws.addEventListener("message", e => {
      const d = JSON.parse(e.data)
      if (d.type === "error") cb(d.message)
    })},
    sendMessage(content: string) {
      ws.send(JSON.stringify({ content }))
    },
    disconnect() { ws.close() },
    get status() { return ws.readyState },
  }
}
```

## Frontend — Hook

```typescript
// src/hooks/useChatSocket.ts
import { useEffect, useRef, useState, useCallback } from "react"
import { createChatSocket } from "../services/chatSocket"
import type { Message } from "../types"

export function useChatSocket(conversationId: string | null) {
  const socketRef = useRef<ReturnType<typeof createChatSocket> | null>(null)
  const [streamingMessage, setStreamingMessage] = useState("")
  const [isStreaming, setIsStreaming] = useState(false)

  useEffect(() => {
    if (!conversationId) return
    const socket = createChatSocket(conversationId)
    socketRef.current = socket

    socket.onChunk(chunk => {
      setIsStreaming(true)
      setStreamingMessage(prev => prev + chunk)
    })
    socket.onDone(_message => {
      setIsStreaming(false)
      setStreamingMessage("")
      // Notificar useConversation para refetch ou atualizar estado
    })

    return () => socket.disconnect()
  }, [conversationId])

  const sendMessage = useCallback((content: string) => {
    socketRef.current?.sendMessage(content)
  }, [])

  return { streamingMessage, isStreaming, sendMessage }
}
```

## Checklist de implementação

- [ ] `ConnectionManager` testado isoladamente (unit).
- [ ] `AIService` tem `stream_reply_to` como async generator.
- [ ] Mensagem completa da IA é persistida no Mongo **uma vez** ao final
      do streaming (não a cada chunk).
- [ ] Se WS não conectar, os endpoints REST da spec 001/002 continuam
      funcionando (degradação suave).
- [ ] `chatSocket.ts` não importa React.
- [ ] `useChatSocket` não faz queries Mongo nem fetch HTTP direto.
