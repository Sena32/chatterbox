/**
 * ChatPage — página principal de chat, orquestra hooks e componentes.
 *
 * Spec: specs/001-iniciar-conversa/tasks.md — Task T15
 *       specs/004-ui-design-system/tasks.md — Task T7 (AppLayout)
 * Skill: .cursor/skills/react-hooks-separation/SKILL.md
 *
 * TODO (spec 001 task T15): implementar composição completa com hooks e chat.
 */

import { AppLayout } from "../components/Layout/AppLayout"

export function ChatPage() {
  return (
    <AppLayout>
      <div data-testid="chat-page">
        <h2 className="text-lg font-bold text-ink">Chat</h2>
        <p className="mt-2 text-ink/70">
          Placeholder — aguardando implementação (spec 001 task T15).
        </p>
      </div>
    </AppLayout>
  )
}
