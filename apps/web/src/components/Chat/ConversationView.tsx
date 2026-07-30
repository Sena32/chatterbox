/**
 * ConversationView — lista de mensagens de uma conversa.
 *
 * Estado: PLACEHOLDER (boilerplate)
 * Spec: specs/001-iniciar-conversa/tasks.md — Task T13
 * Skill: .cursor/skills/react-hooks-separation/SKILL.md
 *
 * Regras:
 *  - Apresentação pura: recebe messages via props.
 *  - Scroll automático para a última mensagem (único useState local permitido:
 *    ref para o container — isso é UI, não negócio).
 *  - Não faz fetch.
 *
 * TODO (spec 001 task T13): implementar renderização com MessageBubble.
 * TODO (spec 003 task T9): aceitar streamingMessage prop opcional.
 */

import type { Message } from "../../types"

interface Props {
  messages: Message[]
  /** Mensagem parcial durante streaming (spec 003, opcional) */
  streamingMessage?: string
}

export function ConversationView({ messages, streamingMessage }: Props) {
  // TODO: implementar — ver spec 001 task T13
  return (
    <div data-testid="conversation-view">
      {messages.map((msg) => (
        <div key={msg.id}>{/* TODO: usar MessageBubble */}{msg.content}</div>
      ))}
      {streamingMessage && (
        <div data-testid="streaming-bubble">{streamingMessage}</div>
      )}
    </div>
  )
}
