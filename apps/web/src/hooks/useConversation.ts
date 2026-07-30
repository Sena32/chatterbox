import { useCallback, useEffect, useState } from "react"

import * as conversationApi from "../services/conversationApi"
import type { Conversation, Message } from "../types"

const STORAGE_KEY = "chatterbox:conversationId"

export interface UseConversationReturn {
  conversation: Conversation | null
  messages: Message[]
  isLoading: boolean
  error: string | null
  startConversation: () => Promise<void>
  sendMessage: (content: string) => Promise<void>
}

export function useConversation(): UseConversationReturn {
  const [conversation, setConversation] = useState<Conversation | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const messages = conversation?.messages ?? []

  const loadConversation = useCallback(async (id: string) => {
    setIsLoading(true)
    setError(null)
    try {
      const data = await conversationApi.getConversation(id)
      setConversation(data)
      localStorage.setItem(STORAGE_KEY, data.id)
    } catch {
      localStorage.removeItem(STORAGE_KEY)
      setConversation(null)
      setError("Não foi possível carregar a conversa.")
    } finally {
      setIsLoading(false)
    }
  }, [])

  useEffect(() => {
    const savedId = localStorage.getItem(STORAGE_KEY)
    if (savedId) {
      void loadConversation(savedId)
    }
  }, [loadConversation])

  const startConversation = useCallback(async () => {
    setIsLoading(true)
    setError(null)
    try {
      const data = await conversationApi.createConversation()
      setConversation(data)
      localStorage.setItem(STORAGE_KEY, data.id)
    } catch {
      setError("Não foi possível iniciar a conversa.")
    } finally {
      setIsLoading(false)
    }
  }, [])

  const sendMessage = useCallback(
    async (content: string) => {
      if (!conversation) return

      setIsLoading(true)
      setError(null)
      try {
        await conversationApi.sendMessage(conversation.id, content)
        const updated = await conversationApi.getConversation(conversation.id)
        setConversation(updated)
      } catch {
        setError("Não foi possível enviar a mensagem.")
      } finally {
        setIsLoading(false)
      }
    },
    [conversation],
  )

  return {
    conversation,
    messages,
    isLoading,
    error,
    startConversation,
    sendMessage,
  }
}
