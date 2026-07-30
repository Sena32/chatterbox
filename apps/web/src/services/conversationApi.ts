/**
 * conversationApi — chamadas HTTP para a API de conversas.
 *
 * Estado: PLACEHOLDER (boilerplate)
 * Spec: specs/001-iniciar-conversa/tasks.md — Task T10
 * Skill: .cursor/skills/react-hooks-separation/SKILL.md
 *
 * Regras:
 *  - Sem imports de React aqui.
 *  - Sem estado. Apenas funções puras que retornam Promises tipadas.
 *  - Tratamento de erros HTTP (res.ok) — lançar Error com mensagem descritiva.
 *
 * TODO (spec 001 task T10):
 *  - Implementar createConversation()
 *  - Implementar getConversation(id)
 *  - Implementar sendMessage(id, content)
 */

import type { Conversation, Message } from "../types"

const BASE = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000"

export async function createConversation(): Promise<Conversation> {
  // TODO: implementar
  throw new Error("createConversation not implemented yet — ver spec 001 task T10")
}

export async function getConversation(id: string): Promise<Conversation> {
  // TODO: implementar
  throw new Error("getConversation not implemented yet — ver spec 001 task T10")
}

export async function sendMessage(id: string, content: string): Promise<Message> {
  // TODO: implementar
  throw new Error("sendMessage not implemented yet — ver spec 001 task T10")
}

export { BASE }
