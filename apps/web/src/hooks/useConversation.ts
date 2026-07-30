/**
 * useConversation — hook central para estado e ações de uma conversa.
 *
 * Estado: PLACEHOLDER (boilerplate)
 * Spec: specs/001-iniciar-conversa/tasks.md — Task T11
 *       specs/002-ia-responde-com-objetivo/tasks.md — Task T10
 * Skill: .cursor/skills/react-hooks-separation/SKILL.md
 *
 * Responsabilidades:
 *  - Manter estado: conversation, messages, isLoading, error
 *  - Expor ações: startConversation(), sendMessage(content)
 *  - Consumir conversationApi (service) — nunca fetch direto
 *  - NÃO renderizar JSX
 *
 * TODO (spec 001 task T11):
 *  - Implementar startConversation()
 *  - Implementar sendMessage(content), refletindo msg do user e da IA no estado
 * TODO (spec 002 task T10):
 *  - Tratar estado de erro quando IA falhar
 */

import type { Conversation, Message } from "../types"

export interface UseConversationReturn {
  conversation: Conversation | null
  messages: Message[]
  isLoading: boolean
  error: string | null
  startConversation: () => Promise<void>
  sendMessage: (content: string) => Promise<void>
}

export function useConversation(): UseConversationReturn {
  // TODO: implementar — ver spec 001 task T11
  throw new Error("useConversation not implemented yet — ver spec 001 task T11")
}
