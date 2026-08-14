/**
 * chatSocket — wrapper sobre WebSocket nativo para streaming de mensagens da IA.
 */

import type { Message } from "../types"

function buildWebSocketUrl(conversationId: string): string {
  const configuredBase = import.meta.env.VITE_WS_BASE_URL?.replace(/\/$/, "")
  if (configuredBase) {
    return `${configuredBase}/ws/conversations/${conversationId}`
  }
  return `/ws/conversations/${conversationId}`
}

export type ChunkHandler = (chunk: string) => void
export type DoneHandler = (message: Message) => void
export type ErrorHandler = (msg: string) => void
export type WebSocketFactory = (url: string) => WebSocket

export interface ChatSocket {
  onChunk(cb: ChunkHandler): void
  onDone(cb: DoneHandler): void
  onError(cb: ErrorHandler): void
  onConnectionChange(cb: (status: number) => void): void
  sendMessage(content: string): void
  disconnect(): void
  readonly status: number
}

const defaultWebSocketFactory: WebSocketFactory = (url) => new WebSocket(url)

export function createChatSocket(
  conversationId: string,
  webSocketFactory: WebSocketFactory = defaultWebSocketFactory,
): ChatSocket {
  const ws = webSocketFactory(buildWebSocketUrl(conversationId))
  const chunkHandlers = new Set<ChunkHandler>()
  const doneHandlers = new Set<DoneHandler>()
  const errorHandlers = new Set<ErrorHandler>()
  const connectionHandlers = new Set<(status: number) => void>()

  const notifyConnection = () => {
    connectionHandlers.forEach((cb) => cb(ws.readyState))
  }

  ws.addEventListener("open", () => {
    notifyConnection()
  })

  ws.addEventListener("close", () => {
    notifyConnection()
  })

  ws.addEventListener("error", () => {
    errorHandlers.forEach((cb) => cb("Falha na conexão WebSocket"))
    notifyConnection()
  })

  ws.addEventListener("message", (event) => {
    const data = JSON.parse(event.data as string) as {
      type: string
      content?: string
      message?: Message
      message_text?: string
    }

    if (data.type === "ai_message_chunk" && data.content !== undefined) {
      chunkHandlers.forEach((cb) => cb(data.content!))
      return
    }

    if (data.type === "ai_message_done" && data.message) {
      doneHandlers.forEach((cb) => cb(data.message!))
      return
    }

    if (data.type === "error") {
      const message =
        (data as { message?: string }).message ?? "Erro desconhecido no WebSocket"
      errorHandlers.forEach((cb) => cb(message))
    }
  })

  return {
    onChunk(cb) {
      chunkHandlers.add(cb)
    },
    onDone(cb) {
      doneHandlers.add(cb)
    },
    onError(cb) {
      errorHandlers.add(cb)
    },
    onConnectionChange(cb) {
      connectionHandlers.add(cb)
      cb(ws.readyState)
    },
    sendMessage(content: string) {
      ws.send(JSON.stringify({ content }))
    },
    disconnect() {
      ws.close()
    },
    get status() {
      return ws.readyState
    },
  }
}

export { buildWebSocketUrl }
