import { useCallback, useEffect, useState } from "react"

import * as conversationApi from "../services/conversationApi"
import { ApiError } from "../services/conversationApi"
import type { Conversation, Message } from "../types"

const STORAGE_KEY = "chatterbox:conversationId"

export type ConversationErrorType = "ai" | "general"

export interface UseConversationReturn {
  conversation: Conversation | null
  messages: Message[]
  isLoading: boolean
  error: string | null
  errorType: ConversationErrorType | null
  startConversation: () => Promise<void>
  sendMessage: (content: string) => Promise<void>
}

export function useConversation(): UseConversationReturn {
  const [conversation, setConversation] = useState<Conversation | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [errorType, setErrorType] = useState<ConversationErrorType | null>(null)

  const messages = conversation?.messages ?? []

  const clearError = useCallback(() => {
    setError(null)
    setErrorType(null)
  }, [])

  const setConversationError = useCallback(
    (message: string, type: ConversationErrorType) => {
      setError(message)
      setErrorType(type)
    },
    [],
  )

  const loadConversation = useCallback(async (id: string) => {
    setIsLoading(true)
    clearError()
    try {
      const data = await conversationApi.getConversation(id)
      setConversation(data)
      localStorage.setItem(STORAGE_KEY, data.id)
    } catch {
      localStorage.removeItem(STORAGE_KEY)
      setConversation(null)
      setConversationError("Não foi possível carregar a conversa.", "general")
    } finally {
      setIsLoading(false)
    }
  }, [clearError, setConversationError])

  useEffect(() => {
    const savedId = localStorage.getItem(STORAGE_KEY)
    if (savedId) {
      void loadConversation(savedId)
    }
  }, [loadConversation])

  const startConversation = useCallback(async () => {
    setIsLoading(true)
    clearError()
    try {
      const data = await conversationApi.createConversation()
      setConversation(data)
      localStorage.setItem(STORAGE_KEY, data.id)
    } catch {
      setConversationError("Não foi possível iniciar a conversa.", "general")
    } finally {
      setIsLoading(false)
    }
  }, [clearError, setConversationError])

  const sendMessage = useCallback(
    async (content: string) => {
      if (!conversation) return

      const conversationId = conversation.id
      const optimisticUserMessage: Message = {
        id: `pending-${Date.now()}`,
        sender: "user",
        content,
        created_at: new Date().toISOString(),
      }

      setConversation((prev) =>
        prev
          ? { ...prev, messages: [...prev.messages, optimisticUserMessage] }
          : prev,
      )

      setIsLoading(true)
      clearError()

      try {
        const aiMessage = await conversationApi.sendMessage(conversationId, content)

        setConversation((prev) => {
          if (!prev) return prev
          const withoutPending = prev.messages.filter(
            (message) => message.id !== optimisticUserMessage.id,
          )
          return {
            ...prev,
            messages: [...withoutPending, optimisticUserMessage, aiMessage],
          }
        })

        const updated = await conversationApi.getConversation(conversationId)
        setConversation(updated)
      } catch (err) {
        if (err instanceof ApiError && err.status === 503) {
          try {
            const updated = await conversationApi.getConversation(conversationId)
            setConversation(updated)
          } catch {
            setConversation((prev) => {
              if (!prev) return prev
              return {
                ...prev,
                messages: prev.messages.filter(
                  (message) => message.id !== optimisticUserMessage.id,
                ),
              }
            })
          }
          setConversationError(
            "A IA está indisponível no momento. Sua mensagem foi salva.",
            "ai",
          )
        } else {
          setConversation((prev) => {
            if (!prev) return prev
            return {
              ...prev,
              messages: prev.messages.filter(
                (message) => message.id !== optimisticUserMessage.id,
              ),
            }
          })
          setConversationError("Não foi possível enviar a mensagem.", "general")
        }
      } finally {
        setIsLoading(false)
      }
    },
    [conversation, clearError, setConversationError],
  )

  return {
    conversation,
    messages,
    isLoading,
    error,
    errorType,
    startConversation,
    sendMessage,
  }
}
