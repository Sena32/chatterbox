interface Props {
  content: string
  isStreaming: boolean
}

export function StreamingMessageBubble({ content, isStreaming }: Props) {
  if (!content && !isStreaming) return null

  return (
    <div
      data-testid="streaming-bubble"
      className="mr-auto max-w-[80%] rounded-2xl bg-surface/30 px-4 py-3 text-ink"
    >
      <span className="mb-1 block text-xs font-medium text-accent">IA</span>
      <p className="text-sm text-ink/80">
        {content}
        {isStreaming && (
          <span className="ml-0.5 inline-block animate-pulse text-brand">▍</span>
        )}
      </p>
    </div>
  )
}
