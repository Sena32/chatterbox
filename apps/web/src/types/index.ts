/**
 * Tipos de domínio compartilhados entre services, hooks e components.
 *
 * Estado: PLACEHOLDER — tipos serão refinados conforme a API for implementada.
 * Spec: specs/001-iniciar-conversa/plan.md (seção "Camadas — Web")
 * Skill: .cursor/skills/react-hooks-separation/SKILL.md
 */

export type MessageSender = "user" | "ai"

export interface Message {
  id: string
  sender: MessageSender
  content: string
  created_at: string
}

export interface Conversation {
  id: string
  created_at: string
  messages: Message[]
}

/** Payload para enviar uma mensagem via REST */
export interface SendMessagePayload {
  content: string
}

/** Eventos recebidos via WebSocket (spec 003) */
export type WsEvent =
  | { type: "ai_message_chunk"; content: string }
  | { type: "ai_message_done"; message: Message }
  | { type: "error"; message: string }
