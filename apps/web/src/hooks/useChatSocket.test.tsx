import { renderHook, act } from "@testing-library/react"
import { describe, expect, it, vi, beforeEach } from "vitest"

import type { Message } from "../types"

const mockSocket = {
  onChunk: vi.fn(),
  onDone: vi.fn(),
  onError: vi.fn(),
  onConnectionChange: vi.fn(),
  sendMessage: vi.fn(),
  disconnect: vi.fn(),
  status: 0,
}

vi.mock("../services/chatSocket", () => ({
  createChatSocket: vi.fn(() => mockSocket),
}))

import { useChatSocket } from "./useChatSocket"
import { createChatSocket } from "../services/chatSocket"

describe("useChatSocket", () => {
  beforeEach(() => {
    vi.clearAllMocks()
    mockSocket.status = 0
  })

  it("transiciona connecting → streaming → done ao receber eventos WS", async () => {
    let chunkHandler: ((chunk: string) => void) | undefined
    let doneHandler: ((message: Message) => void) | undefined
    let connectionHandler: ((status: number) => void) | undefined

    mockSocket.onChunk.mockImplementation((cb) => {
      chunkHandler = cb
    })
    mockSocket.onDone.mockImplementation((cb) => {
      doneHandler = cb
    })
    mockSocket.onConnectionChange.mockImplementation((cb) => {
      connectionHandler = cb
      cb(0)
    })

    const onAiMessageDone = vi.fn()
    const { result } = renderHook(() =>
      useChatSocket("conv-1", { onAiMessageDone }),
    )

    expect(createChatSocket).toHaveBeenCalledWith("conv-1")
    expect(result.current.connectionStatus).toBe("connecting")

    act(() => {
      connectionHandler?.(1)
    })
    expect(result.current.connectionStatus).toBe("open")

    act(() => {
      chunkHandler?.("Hel")
    })
    expect(result.current.isStreaming).toBe(true)
    expect(result.current.streamingMessage).toBe("Hel")

    act(() => {
      chunkHandler?.("lo")
    })
    expect(result.current.streamingMessage).toBe("Hello")

    const doneMessage: Message = {
      id: "ai-1",
      sender: "ai",
      content: "Hello",
      created_at: "2026-01-01T00:00:00Z",
    }

    act(() => {
      doneHandler?.(doneMessage)
    })

    expect(result.current.isStreaming).toBe(false)
    expect(result.current.streamingMessage).toBe("")
    expect(onAiMessageDone).toHaveBeenCalledWith(doneMessage)

    act(() => {
      result.current.sendMessage("Oi")
    })
    expect(mockSocket.sendMessage).toHaveBeenCalledWith("Oi")
  })

  it("não abre socket quando conversationId é null", () => {
    renderHook(() => useChatSocket(null))
    expect(createChatSocket).not.toHaveBeenCalled()
  })
})
