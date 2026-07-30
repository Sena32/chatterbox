import type { Message } from "../../types"

interface Props {
  message: Message
}

export function MessageBubble({ message }: Props) {
  const isUser = message.sender === "user"

  return (
    <div
      data-testid="message-bubble"
      data-sender={message.sender}
      className={
        isUser
          ? "ml-auto max-w-[80%] rounded-2xl bg-brand/10 px-4 py-3 text-ink"
          : "mr-auto max-w-[80%] rounded-2xl bg-surface/30 px-4 py-3 text-ink"
      }
    >
      <span
        className={`mb-1 block text-xs font-medium ${
          isUser ? "text-brand" : "text-accent"
        }`}
      >
        {isUser ? "Você" : "IA"}
      </span>
      <p className="whitespace-pre-wrap text-sm">{message.content}</p>
    </div>
  )
}
