import { ChatBubbleLeftRightIcon } from "@heroicons/react/24/outline"
import type { ReactNode } from "react"

interface AppLayoutProps {
  children: ReactNode
}

export function AppLayout({ children }: AppLayoutProps) {
  return (
    <div className="min-h-screen bg-surface/20">
      <header className="bg-brand px-6 py-4 shadow-md">
        <div className="mx-auto flex max-w-3xl items-center gap-3">
          <ChatBubbleLeftRightIcon
            className="h-6 w-6 text-white"
            aria-hidden="true"
          />
          <h1 className="text-xl font-bold text-white">ChatterBox 2.0</h1>
        </div>
      </header>

      <main className="mx-auto max-w-3xl px-4 py-8">
        <div className="rounded-2xl border border-surface/40 bg-white p-6 shadow-sm">
          {children}
        </div>
      </main>
    </div>
  )
}
