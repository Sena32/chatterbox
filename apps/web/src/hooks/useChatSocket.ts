import { useCallback, useEffect, useRef, useState } from "react"

import { createChatSocket } from "../services/chatSocket"
import type { Message } from "../types"

export type ConnectionStatus = "connecting" | "open" | "closed" | "error"

export interface UseChatSocketOptions {
  onAiMessageDone?: (message: Message) => void
}

export interface UseChatSocketReturn {
  streamingMessage: string
  isStreaming: boolean
  connectionStatus: ConnectionStatus
  sendMessage: (content: string) => void
  isSocketReady: boolean
}

function mapReadyState(readyState: number): ConnectionStatus {
  if (readyState === WebSocket.CONNECTING) return "connecting"
  if (readyState === WebSocket.OPEN) return "open"
  if (readyState === WebSocket.CLOSING || readyState === WebSocket.CLOSED) {
    return "closed"
  }
  return "connecting"
}

export function useChatSocket(
  conversationId: string | null,
  options: UseChatSocketOptions = {},
): UseChatSocketReturn {
  const socketRef = useRef<ReturnType<typeof createChatSocket> | null>(null)
  const [streamingMessage, setStreamingMessage] = useState("")
  const [isStreaming, setIsStreaming] = useState(false)
  const [connectionStatus, setConnectionStatus] =
    useState<ConnectionStatus>("closed")

  const onAiMessageDoneRef = useRef(options.onAiMessageDone)
  onAiMessageDoneRef.current = options.onAiMessageDone

  useEffect(() => {
    if (!conversationId) {
      setConnectionStatus("closed")
      return
    }

    const socket = createChatSocket(conversationId)
    socketRef.current = socket

    socket.onChunk((chunk) => {
      setIsStreaming(true)
      setStreamingMessage((prev) => prev + chunk)
    })

    socket.onDone((message) => {
      setIsStreaming(false)
      setStreamingMessage("")
      onAiMessageDoneRef.current?.(message)
    })

    socket.onError(() => {
      setConnectionStatus("error")
    })

    socket.onConnectionChange((status) => {
      setConnectionStatus(mapReadyState(status))
    })

    return () => {
      socket.disconnect()
      socketRef.current = null
    }
  }, [conversationId])

  const sendMessage = useCallback((content: string) => {
    socketRef.current?.sendMessage(content)
  }, [])

  return {
    streamingMessage,
    isStreaming,
    connectionStatus,
    sendMessage,
    isSocketReady: connectionStatus === "open",
  }
}
