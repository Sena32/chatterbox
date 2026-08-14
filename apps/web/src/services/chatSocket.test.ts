/**
 * @vitest-environment node
 */
import { describe, expect, it, vi } from "vitest"

import { createChatSocket } from "./chatSocket"
import type { Message } from "../types"

type WebSocketFactory = (url: string) => WebSocket

function createMockWebSocket() {
  let messageHandler: ((event: MessageEvent) => void) | undefined
  let openHandler: ((event: Event) => void) | undefined

  const ws = {
    url: "",
    readyState: 0,
    send: vi.fn(),
    close: vi.fn(() => {
      ws.readyState = 3
    }),
    addEventListener: vi.fn((type: string, cb: (event: Event) => void) => {
      if (type === "message") messageHandler = cb as (event: MessageEvent) => void
      if (type === "open") openHandler = cb
    }),
    emitMessage(data: unknown) {
      messageHandler?.({ data: JSON.stringify(data) } as MessageEvent)
    },
    emitOpen() {
      ws.readyState = 1
      openHandler?.({} as Event)
    },
  }
  return { ws: ws as unknown as WebSocket, wsObj: ws }
}

describe("createChatSocket", () => {
  it("registra handlers e repassa eventos chunk, done e error", () => {
    const { ws, wsObj } = createMockWebSocket()
    const factory: WebSocketFactory = vi.fn(() => ws)

    const onChunk = vi.fn()
    const onDone = vi.fn()
    const onError = vi.fn()

    const socket = createChatSocket("conv-1", factory)
    socket.onChunk(onChunk)
    socket.onDone(onDone)
    socket.onError(onError)

    expect(factory).toHaveBeenCalledWith(
      expect.stringContaining("/ws/conversations/conv-1"),
    )

    wsObj.emitMessage({
      type: "ai_message_chunk",
      content: "Hel",
    })
    expect(onChunk).toHaveBeenCalledWith("Hel")

    const doneMessage: Message = {
      id: "ai-1",
      sender: "ai",
      content: "Hello",
      created_at: "2026-01-01T00:00:00Z",
    }
    wsObj.emitMessage({ type: "ai_message_done", message: doneMessage })
    expect(onDone).toHaveBeenCalledWith(doneMessage)

    wsObj.emitMessage({ type: "error", message: "falhou" })
    expect(onError).toHaveBeenCalledWith("falhou")

    socket.sendMessage("Oi")
    expect(wsObj.send).toHaveBeenCalledWith(JSON.stringify({ content: "Oi" }))

    socket.disconnect()
    expect(wsObj.close).toHaveBeenCalled()
  })
})
