# Spec 002 — IA Responde com Objetivo

Cobre os requisitos mínimos **(c)** e **(d)** da POC.

Depende de: `001-iniciar-conversa`.

## Contexto

Depois que o usuário envia uma mensagem, o sistema deve processá-la usando um
modelo de IA e armazenar a resposta como uma mensagem de `sender=ai` na mesma
conversa. A IA nesta POC tem um objetivo de conversação fixo e explícito:
**"Convencer o usuário que a Terra é plana."**

## Objetivo

Toda mensagem do usuário gera, de forma automática, uma resposta da IA
persistida e devolvida ao cliente, respeitando o objetivo configurado e o
histórico da conversa.

## Requisitos funcionais

1. Ao receber `POST /conversations/{id}/messages` com uma mensagem do
   usuário, o sistema deve:
   a. Persistir a mensagem do usuário (spec 001).
   b. Montar o contexto da conversa (histórico de mensagens).
   c. Chamar o provedor de IA com um *system prompt* que injeta o objetivo
      configurado (`AI_SYSTEM_GOAL`).
   d. Persistir a resposta da IA como mensagem `sender=ai`.
   e. Retornar ambas as mensagens (ou ao menos a da IA) na resposta HTTP.
2. O objetivo da IA é lido de configuração (variável de ambiente
   `AI_SYSTEM_GOAL`), nunca escrito diretamente dentro da lógica de negócio.
3. Falhas do provedor de IA (timeout, erro de API) não podem corromper a
   conversa: a mensagem do usuário já persistida permanece; o erro é
   reportado de forma tratada (ex: mensagem de erro amigável, sem quebrar a
   aplicação).
4. O serviço de IA deve ser abstraído por uma interface (`AIProvider` /
   `AIService`) que permita trocar o provedor (ex: Anthropic, OpenAI, mock)
   sem alterar o restante do sistema — importante para testabilidade (TDD).

## Fora de escopo (nesta spec)

- Streaming da resposta em tempo real (spec 003).
- Ajuste fino de "quão convincente" a IA deve ser — objetivo é qualitativo,
  não há critério de sucesso de persuasão nesta POC.

## Critérios de aceite

- [ ] Enviar uma mensagem de usuário para uma conversa gera, na sequência,
      uma mensagem de `sender=ai` persistida no Mongo.
- [ ] O *system prompt* usado na chamada de IA contém literalmente o valor de
      `AI_SYSTEM_GOAL`.
- [ ] Existe um `AIService`/`AIProvider` mockável, testado com um provedor
      fake nos testes unitários (sem chamar API externa real em testes).
- [ ] Se o provedor de IA falhar, o endpoint retorna erro tratado (ex: 503)
      sem perder a mensagem do usuário já salva.
