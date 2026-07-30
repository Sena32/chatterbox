# Arquitetura — ChatterBox 2.0 POC

## Visão geral

```
┌──────────────────────────────────────────────────────────────────┐
│                        Docker Compose                            │
│                                                                  │
│   ┌─────────────┐    REST / WS    ┌─────────────────────────┐   │
│   │  chatterbox │ ─────────────►  │     chatterbox-api       │   │
│   │    -web     │                 │  (FastAPI · Python 3.12) │   │
│   │  (React 18) │ ◄───────────── │                          │   │
│   └─────────────┘   JSON / WS     └──────────┬──────────────┘   │
│        :5173          events                  │                  │
│                                               │ Motor (async)    │
│                                     ┌─────────▼──────────┐      │
│                                     │  chatterbox-mongo   │      │
│                                     │    (MongoDB 7)      │      │
│                                     └────────────────────┘      │
│                                              :27017              │
└──────────────────────────────────────────────────────────────────┘
                                      │ HTTP (AI_API_KEY)
                                      ▼
                               Provedor de IA
                           (Anthropic / OpenAI / Fake)
```

## Camadas da API

```
HTTP Request
     │
     ▼
controllers/          ← FastAPI router, Pydantic I/O, HTTPException
     │ Depends(...)
     ▼
services/             ← Regras de negócio, orquestração, AIService
     │ injeção
     ▼
repositories/         ← Motor queries, mapeamento ObjectId→str
     │
     ▼
MongoDB               ← Coleção: conversations (mensagens embutidas)
```

## Camadas do Web

```
pages/                ← Composição de hooks + componentes
  └─ hooks/           ← Estado, efeitos, chamadas a services
       └─ services/   ← fetch/WebSocket (sem React)
  └─ components/      ← Apresentação pura (props in, callbacks out)
       └─ types/      ← Interfaces TypeScript compartilhadas
```

## Fluxo de dados — mensagem REST (specs 001 + 002)

```
1. Usuário digita e aperta "Enviar" → MessageInput.onSend()
2. useConversation.sendMessage(content) é chamado
3. conversationApi.sendMessage(id, content) faz POST /conversations/{id}/messages
4. ConversationController recebe o request
5. ConversationService.post_user_message():
   a. ConversationRepository.add_message(id, {sender:"user", content})
   b. AIService.reply_to(conversation) → chama provedor com system_goal + histórico
   c. ConversationRepository.add_message(id, {sender:"ai", content: resposta})
   d. Retorna as duas mensagens
6. Controller serializa e retorna 200
7. useConversation atualiza estado → ConversationView re-renderiza
```

## Fluxo de dados — streaming WebSocket (spec 003, opcional)

```
1. useChatSocket.sendMessage(content) → ws.send({content})
2. FastAPI WS endpoint recebe, persiste msg user
3. AIService.stream_reply_to() (async generator) → chunks
4. Para cada chunk: ws.send_json({type:"ai_message_chunk", content})
5. Ao final: persiste msg IA completa, ws.send_json({type:"ai_message_done"})
6. useChatSocket.onChunk → acumula em streamingMessage
7. useChatSocket.onDone → atualiza lista definitiva de mensagens
```

## Decisões de arquitetura

| Decisão | Escolha | Motivo |
|---------|---------|--------|
| Mensagens embutidas na conversa | Embedding no documento MongoDB | Volume de mensagens por conversa é baixo na POC; evita joins |
| AIProvider como Protocol | Protocol + implementação injetável | Testabilidade com FakeAIProvider sem chamadas reais de API |
| WebSocket por conversa | Um socket por `conversation_id` | Simples para POC; multiplexing não é requisito |
| Sem autenticação | Sem auth na POC | Requisito não solicitado pelo arquiteto para esta fase |
| pydantic-settings | Centraliza toda config em `core/config.py` | Evita `os.environ` espalhado, facilita override em testes |

## Evolução futura (fora do escopo da POC)

- Autenticação (JWT / OAuth2)
- Múltiplos usuários por conversa (broadcast WS)
- Coleção separada de `messages` (se volume crescer)
- Cache de histórico (Redis) para conversas longas
- Monitoramento de telemetria das chamadas à IA
