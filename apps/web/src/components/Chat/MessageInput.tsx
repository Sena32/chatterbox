/**
 * MessageInput — campo de texto para o usuário enviar mensagens.
 *
 * Estado: PLACEHOLDER (boilerplate)
 * Spec: specs/001-iniciar-conversa/tasks.md — Task T14
 * Skill: .cursor/skills/react-hooks-separation/SKILL.md
 *
 * Regras:
 *  - useState local para o valor do input (UI efêmera — permitido).
 *  - Não tem lógica de negócio; dispara onSend(content) e limpa o campo.
 *  - Desabilitar envio quando isLoading=true.
 *
 * TODO (spec 001 task T14): implementar.
 */

interface Props {
  onSend: (content: string) => void
  isLoading?: boolean
  disabled?: boolean
}

export function MessageInput({ onSend, isLoading = false, disabled = false }: Props) {
  // TODO: implementar — ver spec 001 task T14
  return (
    <div data-testid="message-input">
      <input
        type="text"
        placeholder="Digite sua mensagem..."
        disabled={isLoading || disabled}
      />
      <button
        onClick={() => onSend("TODO: pegar valor do input")}
        disabled={isLoading || disabled}
      >
        {isLoading ? "Aguardando..." : "Enviar"}
      </button>
    </div>
  )
}
