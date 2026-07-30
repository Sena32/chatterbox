import type { Conversation, Message } from "../types"

const BASE = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000"

async function handleResponse<T>(res: Response, errorMessage: string): Promise<T> {
  if (!res.ok) {
    throw new Error(errorMessage)
  }
  return res.json() as Promise<T>
}

export async function createConversation(): Promise<Conversation> {
  const res = await fetch(`${BASE}/conversations`, { method: "POST" })
  return handleResponse(res, "Erro ao criar conversa")
}

export async function getConversation(id: string): Promise<Conversation> {
  const res = await fetch(`${BASE}/conversations/${id}`)
  return handleResponse(res, "Erro ao buscar conversa")
}

export async function sendMessage(id: string, content: string): Promise<Message> {
  const res = await fetch(`${BASE}/conversations/${id}/messages`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ content }),
  })
  return handleResponse(res, "Erro ao enviar mensagem")
}

export { BASE }
