/**
 * MessageBubble — exibe uma única mensagem com estilo por remetente.
 *
 * Estado: PLACEHOLDER (boilerplate)
 * Spec: specs/001-iniciar-conversa/tasks.md — Task T12
 * Skill: .cursor/skills/react-hooks-separation/SKILL.md
 *
 * Regras:
 *  - Apresentação pura: recebe props, não tem estado de negócio.
 *  - Não faz fetch, não usa useEffect de rede.
 *  - Estilo visualmente distinto para sender="user" vs sender="ai" (requisito b).
 *
 * TODO (spec 001 task T12): implementar o componente.
 */

import type { Message } from "../../types"

interface Props {
  message: Message
}

export function MessageBubble({ message }: Props) {
  // TODO: implementar — ver spec 001 task T12
  return (
    <div data-sender={message.sender} data-testid="message-bubble">
      {/* placeholder */}
      <strong>{message.sender === "user" ? "Você" : "IA"}:</strong>{" "}
      {message.content}
    </div>
  )
}
