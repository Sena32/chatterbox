---
name: react-hooks-separation
description: Use esta skill ao criar ou modificar qualquer arquivo em apps/web/src/. Garante que a separação entre hooks (lógica) e components (apresentação) seja mantida, e que serviços de rede fiquem isolados em services/.
---

# React — Hooks x Components x Services

## Regra de ouro

> **Componente não busca dado. Hook não renderiza. Service não conhece React.**

## Fluxo correto

```
ChatPage (page)
  └─ usa useConversation (hook)
       ├─ chama conversationApi (service)   ← fetch/axios
       └─ chama chatSocket (service)        ← WebSocket
  └─ renderiza ConversationView (component) ← recebe props
       └─ renderiza MessageBubble (component) ← props puras
  └─ renderiza MessageInput (component)     ← callback onSend
```

## Criando um Hook customizado

```typescript
// src/hooks/useConversation.ts
import { useState, useCallback } from "react"
import * as conversationApi from "../services/conversationApi"
import type { Conversation, Message } from "../types"

export function useConversation() {
  const [conversation, setConversation] = useState<Conversation | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const startConversation = useCallback(async () => {
    setIsLoading(true)
    try {
      const data = await conversationApi.createConversation()
      setConversation(data)
    } catch (e) {
      setError("Não foi possível iniciar a conversa.")
    } finally {
      setIsLoading(false)
    }
  }, [])

  // sendMessage, etc.

  return { conversation, isLoading, error, startConversation }
}
```

## Criando um Component de apresentação

```tsx
// src/components/Chat/MessageBubble.tsx
import type { Message } from "../../types"

interface Props {
  message: Message
}

// Sem useState de negócio, sem fetch, sem useEffect de rede
export function MessageBubble({ message }: Props) {
  const isUser = message.sender === "user"
  return (
    <div className={isUser ? "bubble bubble--user" : "bubble bubble--ai"}>
      <span className="bubble__sender">{isUser ? "Você" : "IA"}</span>
      <p>{message.content}</p>
    </div>
  )
}
```

## Criando um Service (sem React)

```typescript
// src/services/conversationApi.ts
import type { Conversation, Message } from "../types"

const BASE = import.meta.env.VITE_API_BASE_URL

export async function createConversation(): Promise<Conversation> {
  const res = await fetch(`${BASE}/conversations`, { method: "POST" })
  if (!res.ok) throw new Error("Erro ao criar conversa")
  return res.json()
}

export async function sendMessage(id: string, content: string): Promise<Message> {
  const res = await fetch(`${BASE}/conversations/${id}/messages`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ content }),
  })
  if (!res.ok) throw new Error("Erro ao enviar mensagem")
  return res.json()
}
```

## Sinais de alerta (anti-patterns a evitar)

- `useEffect(() => { fetch(...) }, [])` dentro de um componente → mova para hook.
- `axios.get(...)` dentro de um component → mova para service.
- `useState` com dados de API dentro de um component de apresentação → mova para hook.
- Um hook fazendo 3 coisas não relacionadas → quebre em dois hooks compostos.

## Tipos compartilhados

Defina em `src/types/index.ts`:

```typescript
export interface Message {
  id: string
  sender: "user" | "ai"
  content: string
  created_at: string
}

export interface Conversation {
  id: string
  created_at: string
  messages: Message[]
}
```
