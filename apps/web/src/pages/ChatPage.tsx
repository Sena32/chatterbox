import { ChatBubbleLeftRightIcon } from "@heroicons/react/24/outline"

import { ConversationView } from "../components/Chat/ConversationView"
import { MessageInput } from "../components/Chat/MessageInput"
import { AppLayout } from "../components/Layout/AppLayout"
import { useConversation } from "../hooks/useConversation"

export function ChatPage() {
  const {
    conversation,
    messages,
    isLoading,
    error,
    startConversation,
    sendMessage,
  } = useConversation()

  return (
    <AppLayout>
      <div data-testid="chat-page" className="flex flex-col">
        {error && (
          <div
            role="alert"
            className="mb-4 rounded-xl border border-brand/30 bg-brand/10 px-4 py-3 text-sm text-ink"
          >
            {error}
          </div>
        )}

        {!conversation ? (
          <div className="flex flex-col items-center gap-4 py-12">
            <div className="flex h-16 w-16 items-center justify-center rounded-full bg-surface/30">
              <ChatBubbleLeftRightIcon
                className="h-8 w-8 text-brand"
                aria-hidden="true"
              />
            </div>
            <p className="text-center text-ink/70">
              Inicie uma conversa para começar a trocar mensagens.
            </p>
            <button
              type="button"
              onClick={() => void startConversation()}
              disabled={isLoading}
              className="rounded-xl bg-brand px-6 py-3 text-sm font-medium text-white transition hover:bg-brand/90 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {isLoading ? "Iniciando..." : "Iniciar conversa"}
            </button>
          </div>
        ) : (
          <>
            <ConversationView messages={messages} />
            <MessageInput
              onSend={(content) => void sendMessage(content)}
              isLoading={isLoading}
            />
          </>
        )}
      </div>
    </AppLayout>
  )
}
