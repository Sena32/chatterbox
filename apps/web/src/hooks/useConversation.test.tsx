import { renderHook, act, waitFor } from "@testing-library/react"
import { describe, expect, it, vi, beforeEach } from "vitest"

import type { Conversation, Message } from "../types"

const mockSendViaSocket = vi.fn()
const mockUseChatSocket = vi.fn()

vi.mock("./useChatSocket", () => ({
  useChatSocket: (...args: unknown[]) => mockUseChatSocket(...args),
}))

vi.mock("../services/conversationApi", () => ({
  ApiError: class ApiError extends Error {
    constructor(
      message: string,
      public status: number,
    ) {
      super(message)
    }
  },
  createConversation: vi.fn(),
  getConversation: vi.fn(),
  sendMessage: vi.fn(),
}))

import * as conversationApi from "../services/conversationApi"
import { useConversation } from "./useConversation"

const baseConversation: Conversation = {
  id: "conv-1",
  created_at: "2026-01-01T00:00:00Z",
  messages: [],
}

describe("useConversation — WebSocket x REST", () => {
  beforeEach(() => {
    vi.clearAllMocks()
    mockUseChatSocket.mockReturnValue({
      streamingMessage: "",
      isStreaming: false,
      connectionStatus: "closed",
      sendMessage: mockSendViaSocket,
      isSocketReady: false,
    })
    vi.mocked(conversationApi.createConversation).mockResolvedValue(baseConversation)
  })

  it("usa REST quando o WebSocket não está pronto (fallback)", async () => {
    localStorage.setItem("chatterbox:conversationId", "conv-1")
    vi.mocked(conversationApi.getConversation).mockResolvedValue(baseConversation)

    const aiMessage: Message = {
      id: "ai-1",
      sender: "ai",
      content: "Resposta REST",
      created_at: "2026-01-01T00:01:00Z",
    }
    vi.mocked(conversationApi.sendMessage).mockResolvedValue(aiMessage)
    vi.mocked(conversationApi.getConversation)
      .mockResolvedValueOnce(baseConversation)
      .mockResolvedValueOnce({
        ...baseConversation,
        messages: [
          {
            id: "u1",
            sender: "user",
            content: "Olá",
            created_at: "2026-01-01T00:00:30Z",
          },
          aiMessage,
        ],
      })

    const { result } = renderHook(() => useConversation())

    await waitFor(() => {
      expect(result.current.conversation?.id).toBe("conv-1")
    })

    await act(async () => {
      await result.current.sendMessage("Olá")
    })

    expect(mockSendViaSocket).not.toHaveBeenCalled()
    expect(conversationApi.sendMessage).toHaveBeenCalledWith("conv-1", "Olá")
  })

  it("envia via WebSocket quando a conexão está aberta", async () => {
    localStorage.setItem("chatterbox:conversationId", "conv-1")
    vi.mocked(conversationApi.getConversation).mockResolvedValue(baseConversation)

    mockUseChatSocket.mockReturnValue({
      streamingMessage: "",
      isStreaming: false,
      connectionStatus: "open",
      sendMessage: mockSendViaSocket,
      isSocketReady: true,
    })

    const { result } = renderHook(() => useConversation())

    await waitFor(() => {
      expect(result.current.conversation?.id).toBe("conv-1")
    })

    await act(async () => {
      await result.current.sendMessage("Olá via WS")
    })

    expect(mockSendViaSocket).toHaveBeenCalledWith("Olá via WS")
    expect(conversationApi.sendMessage).not.toHaveBeenCalled()
  })

  it("adiciona mensagem definitiva da IA ao concluir streaming (T9)", async () => {
    let onAiMessageDone: ((message: Message) => void) | undefined

    mockUseChatSocket.mockImplementation((_id, options) => {
      onAiMessageDone = options?.onAiMessageDone
      return {
        streamingMessage: "Resposta",
        isStreaming: true,
        connectionStatus: "open",
        sendMessage: mockSendViaSocket,
        isSocketReady: true,
      }
    })

    localStorage.setItem("chatterbox:conversationId", "conv-1")
    vi.mocked(conversationApi.getConversation).mockResolvedValue(baseConversation)

    const { result } = renderHook(() => useConversation())

    await waitFor(() => {
      expect(result.current.conversation?.id).toBe("conv-1")
    })

    const aiMessage: Message = {
      id: "ai-final",
      sender: "ai",
      content: "Resposta completa",
      created_at: "2026-01-01T00:02:00Z",
    }

    act(() => {
      onAiMessageDone?.(aiMessage)
    })

    await waitFor(() => {
      expect(result.current.messages).toContainEqual(aiMessage)
    })
  })
})
