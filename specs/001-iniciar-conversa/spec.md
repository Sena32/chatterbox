# Spec 001 — Iniciar Conversa

Cobre os requisitos mínimos **(a)** e **(b)** da POC.

## Contexto

O usuário acessa o ChatterBox Web e precisa conseguir iniciar uma conversa com
a IA sem nenhuma configuração prévia. Cada conversa é composta por mensagens,
e cada mensagem pertence a um remetente: `user` ou `ai`.

## Objetivo

Permitir que qualquer usuário inicie uma nova conversa e visualize as
mensagens trocadas, claramente separadas por quem enviou.

## Requisitos funcionais

1. Ao acessar a aplicação, o usuário pode criar uma nova conversa com um
   clique/ação simples (não precisa de login nesta POC).
2. Uma conversa possui: identificador único, data de criação, lista de
   mensagens.
3. Uma mensagem possui: identificador único, `conversation_id`, `sender`
   (`user` | `ai`), `content` (texto), `created_at`.
4. O usuário pode enviar mensagens de texto dentro de uma conversa existente.
5. A interface exibe as mensagens em ordem cronológica, com identificação
   visual clara de quem enviou cada uma (ex: alinhamento diferente, cor, ou
   rótulo).
6. Conversas e mensagens são persistidas (não se perdem ao atualizar a
   página).

## Fora de escopo (nesta spec)

- Autenticação/autorização de usuários.
- Resposta da IA em si (coberto pela spec `002-ia-responde-com-objetivo`).
- Streaming via WebSocket (coberto pela spec `003-stream-mensagens-websocket`).

## Critérios de aceite

- [ ] `POST /conversations` cria uma conversa vazia e retorna seu `id`.
- [ ] `GET /conversations/{id}` retorna a conversa com suas mensagens
      ordenadas por `created_at`.
- [ ] `POST /conversations/{id}/messages` adiciona uma mensagem com
      `sender=user` à conversa.
- [ ] No Web, ao carregar uma conversa existente, mensagens de `user` e `ai`
      são visualmente distinguíveis.
- [ ] Recarregar a página mantém o histórico da conversa (dado vem do Mongo).
