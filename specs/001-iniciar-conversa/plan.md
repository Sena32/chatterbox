# Plan 001 — Iniciar Conversa

## Modelo de dados (MongoDB)

Coleção `conversations`:

```json
{
  "_id": "ObjectId",
  "created_at": "datetime",
  "messages": [
    {
      "id": "uuid",
      "sender": "user | ai",
      "content": "string",
      "created_at": "datetime"
    }
  ]
}
```

> Decisão: embutir mensagens dentro do documento da conversa (embedding) em
> vez de coleção separada, dado o volume esperado por conversa nesta POC.
> Se o volume crescer, revisitar para coleção `messages` referenciada por
> `conversation_id` (documentar essa decisão caso mude).

## Camadas — API

- `models/conversation.py`: `Conversation`, `Message` (Pydantic).
- `repositories/conversation_repository.py`:
  - `create() -> Conversation`
  - `get_by_id(id) -> Conversation | None`
  - `add_message(id, message) -> Conversation`
- `services/conversation_service.py`:
  - `start_conversation() -> Conversation`
  - `get_conversation(id) -> Conversation`
  - `post_user_message(id, content) -> Message` (persiste a mensagem do
    usuário; a resposta da IA é orquestrada pela spec 002)
- `controllers/conversation_controller.py` (APIRouter):
  - `POST /conversations`
  - `GET /conversations/{id}`
  - `POST /conversations/{id}/messages`

## Camadas — Web

- `services/conversationApi.ts`: `createConversation()`, `getConversation(id)`,
  `sendMessage(id, content)`.
- `hooks/useConversation.ts`: mantém estado da conversa atual, `messages`,
  `isLoading`, expõe `startConversation()` e `sendMessage(content)`.
- `components/Chat/ConversationView.tsx`: renderiza lista de mensagens
  (via `components/Chat/MessageBubble.tsx`), sem lógica de fetch.
- `components/Chat/MessageBubble.tsx`: recebe `sender` e `content` via props,
  aplica estilo diferente por `sender`.
- `components/Chat/MessageInput.tsx`: input controlado, dispara callback
  `onSend(content)`.
- `pages/ChatPage.tsx`: usa `useConversation`, compõe os componentes acima.

## Testes (TDD — backend)

1. `tests/unit/models/test_conversation_model.py` — validação de schema.
2. `tests/unit/repositories/test_conversation_repository.py` — usa Mongo em
   memória/mock (ex: `mongomock` ou `mongomock-motor`) para `create`,
   `get_by_id`, `add_message`.
3. `tests/unit/services/test_conversation_service.py` — mocka o repository,
   testa orquestração.
4. `tests/integration/test_conversations_api.py` — sobe app FastAPI (TestClient
   / httpx AsyncClient) contra um Mongo de teste, testa os 3 endpoints
   end-to-end.

## Ordem sugerida de implementação

`model → repository (TDD) → service (TDD) → controller → testes de
integração → frontend (service → hook → components → page)`.
