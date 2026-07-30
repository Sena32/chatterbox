/**
 * chatSocket — wrapper sobre WebSocket nativo para streaming de mensagens da IA.
 *
 * Estado: PLACEHOLDER (boilerplate)
 * Spec: specs/003-stream-mensagens-websocket/tasks.md — Task T6
 * Skill: .cursor/skills/websocket-live-streaming/SKILL.md
 *
 * Regras:
 *  - Sem imports de React aqui.
 *  - Encapsula apenas o transporte WS. Lógica de estado fica em useChatSocket.
 *
 * TODO (spec 003 task T6):
 *  - Implementar createChatSocket(conversationId)
 *  - Expor onChunk, onDone, onError, sendMessage, disconnect, status
 */

import type { Message } from "../types"

const WS_BASE = import.meta.env.VITE_WS_BASE_URL ?? "ws://localhost:8000"

export type ChunkHandler = (chunk: string) => void
export type DoneHandler = (message: Message) => void
export type ErrorHandler = (msg: string) => void

export interface ChatSocket {
  onChunk(cb: ChunkHandler): void
  onDone(cb: DoneHandler): void
  onError(cb: ErrorHandler): void
  sendMessage(content: string): void
  disconnect(): void
  readonly status: number
}

export function createChatSocket(_conversationId: string): ChatSocket {
  // TODO: implementar — ver spec 003 task T6
  throw new Error("createChatSocket not implemented yet — ver spec 003 task T6")
}

export { WS_BASE }
