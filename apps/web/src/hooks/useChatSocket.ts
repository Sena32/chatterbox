/**
 * useChatSocket — hook para streaming ao vivo via WebSocket.
 *
 * Estado: PLACEHOLDER (boilerplate)
 * Spec: specs/003-stream-mensagens-websocket/tasks.md — Task T7
 * Skill: .cursor/skills/websocket-live-streaming/SKILL.md
 *
 * Responsabilidades:
 *  - Gerenciar ciclo de vida da conexão WS (abrir ao receber conversationId,
 *    fechar no cleanup do useEffect)
 *  - Acumular chunks em streamingMessage
 *  - Sinalizar isStreaming e connectionStatus
 *  - Expor sendMessage(content) que delega ao chatSocket service
 *  - NÃO renderizar JSX
 *
 * TODO (spec 003 task T7):
 *  - Implementar usando createChatSocket do services/chatSocket.ts
 */

export interface UseChatSocketReturn {
  streamingMessage: string
  isStreaming: boolean
  connectionStatus: "connecting" | "open" | "closed" | "error"
  sendMessage: (content: string) => void
}

export function useChatSocket(_conversationId: string | null): UseChatSocketReturn {
  // TODO: implementar — ver spec 003 task T7
  throw new Error("useChatSocket not implemented yet — ver spec 003 task T7")
}
