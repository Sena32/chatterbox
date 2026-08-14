import { useEffect, useRef } from "react"

import type { Message } from "../../types"
import { MessageBubble } from "./MessageBubble"
import { StreamingMessageBubble } from "./StreamingMessageBubble"

interface Props {
  messages: Message[]
  streamingMessage?: string
  isStreaming?: boolean
}

export function ConversationView({
  messages,
  streamingMessage,
  isStreaming = false,
}: Props) {
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages, streamingMessage])

  if (messages.length === 0 && !streamingMessage && !isStreaming) {
    return (
      <div
        data-testid="conversation-view"
        className="flex min-h-48 items-center justify-center rounded-xl border border-dashed border-surface/60 bg-surface/10 px-4 py-8"
      >
        <p className="text-center text-sm text-ink/60">
          Nenhuma mensagem ainda. Envie a primeira!
        </p>
      </div>
    )
  }

  return (
    <div
      data-testid="conversation-view"
      className="flex max-h-[28rem] flex-col gap-3 overflow-y-auto rounded-xl bg-surface/10 p-4"
    >
      {messages.map((msg) => (
        <MessageBubble key={msg.id} message={msg} />
      ))}

      {streamingMessage !== undefined && (streamingMessage || isStreaming) && (
        <StreamingMessageBubble
          content={streamingMessage}
          isStreaming={isStreaming}
        />
      )}

      <div ref={bottomRef} />
    </div>
  )
}
