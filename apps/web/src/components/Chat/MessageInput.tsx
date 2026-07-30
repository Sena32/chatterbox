import { FormEvent, useState } from "react"
import { PaperAirplaneIcon } from "@heroicons/react/24/outline"

interface Props {
  onSend: (content: string) => void
  isLoading?: boolean
  disabled?: boolean
}

export function MessageInput({
  onSend,
  isLoading = false,
  disabled = false,
}: Props) {
  const [value, setValue] = useState("")
  const isDisabled = isLoading || disabled

  function handleSubmit(event: FormEvent) {
    event.preventDefault()
    const trimmed = value.trim()
    if (!trimmed || isDisabled) return

    onSend(trimmed)
    setValue("")
  }

  return (
    <form
      data-testid="message-input"
      onSubmit={handleSubmit}
      className="mt-4 flex items-center gap-2"
    >
      <input
        type="text"
        value={value}
        onChange={(event) => setValue(event.target.value)}
        placeholder="Digite sua mensagem..."
        disabled={isDisabled}
        className="flex-1 rounded-xl border border-surface/60 bg-white px-4 py-3 text-sm text-ink placeholder:text-ink/40 focus:border-brand focus:outline-none focus:ring-2 focus:ring-brand/20 disabled:cursor-not-allowed disabled:opacity-50"
      />
      <button
        type="submit"
        disabled={isDisabled || !value.trim()}
        className="flex items-center gap-2 rounded-xl bg-brand px-4 py-3 text-sm font-medium text-white transition hover:bg-brand/90 disabled:cursor-not-allowed disabled:opacity-50"
      >
        <PaperAirplaneIcon className="h-5 w-5" aria-hidden="true" />
        {isLoading ? "Aguardando..." : "Enviar"}
      </button>
    </form>
  )
}
