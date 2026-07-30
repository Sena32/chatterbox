# Spec 003 — Stream de Mensagens via WebSocket (Opcional)

Cobre o requisito opcional **(e)** da POC.

Depende de: `001-iniciar-conversa`, `002-ia-responde-com-objetivo`.

## Contexto

Hoje (spec 002) a resposta da IA só chega ao cliente depois de pronta
(request/response HTTP tradicional). Este requisito opcional propõe exibir a
resposta da IA "ao vivo" (token a token / chunk a chunk) enquanto ela é
gerada, via WebSocket.

## Objetivo

O usuário vê a resposta da IA sendo "digitada" progressivamente, sem esperar
a resposta completa para começar a ler.

## Requisitos funcionais

1. O cliente Web abre uma conexão WebSocket por conversa:
   `ws://<host>/ws/conversations/{id}`.
2. Ao enviar uma mensagem do usuário (via WS ou via HTTP, a definir na
   implementação — recomendado: enviar via WS também, para simplificar),
   o servidor:
   a. Persiste a mensagem do usuário.
   b. Inicia a geração da resposta da IA em modo streaming (se o provedor
      suportar) ou emula chunking de uma resposta não-streaming.
   c. Envia eventos incrementais ao cliente conforme os chunks chegam.
   d. Ao final, persiste a mensagem completa da IA (mesma garantia da spec
      002) e envia um evento de "fim de mensagem".
3. Formato de evento sugerido (JSON):
   ```json
   { "type": "ai_message_chunk", "conversation_id": "...", "content": "..." }
   { "type": "ai_message_done", "conversation_id": "...", "message": { "...": "..." } }
   { "type": "error", "message": "..." }
   ```
4. Se a conexão WS cair, o histórico da conversa continua íntegro e acessível
   via os endpoints REST da spec 001 (o WS é um canal adicional, não o único
   meio de acesso aos dados).

## Fora de escopo

- Múltiplos usuários simultâneos na mesma conversa (broadcast/colaboração).
- Reconexão automática sofisticada (retry simples é suficiente na POC).

## Critérios de aceite

- [ ] Cliente Web consegue abrir uma conexão WS por conversa e receber
      eventos de chunk enquanto a IA "digita".
- [ ] Ao final do streaming, a mensagem completa está persistida no Mongo
      (idêntica ao que seria salvo no fluxo HTTP da spec 002).
- [ ] Fechar e reabrir a página, o histórico via REST continua correto.
- [ ] Hook dedicado no frontend (`useChatSocket`) encapsula toda a lógica de
      WebSocket, sem vazar para os componentes de apresentação.
