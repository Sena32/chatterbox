# Constituição do Projeto — ChatterBox 2.0

Este documento define os princípios inegociáveis do projeto. Toda spec, plano,
tarefa ou código gerado (por humano ou agente) deve respeitá-los. Em caso de
conflito entre uma spec e a constituição, a constituição vence.

## 1. Spec-Driven Development (SDD)

- Nenhuma funcionalidade é implementada sem antes existir uma pasta em
  `specs/NNN-nome-da-feature/` com `spec.md`, `plan.md` e `tasks.md`.
- `spec.md` descreve **o quê** e **por quê** (comportamento observável,
  critérios de aceite), nunca detalhes de implementação.
- `plan.md` descreve **como**: decisões técnicas, contratos de API, schema de
  dados, camadas afetadas.
- `tasks.md` quebra o plano em tarefas pequenas, sequenciais e testáveis.
- Specs são a fonte da verdade. Código que diverge da spec deve corrigir a
  spec ou o código — nunca deixar os dois divergentes silenciosamente.

## 2. TDD é obrigatório no backend

- Toda função/método de `service` e `repository` nasce de um teste que falha
  primeiro (red), depois a implementação mínima (green), depois refactor.
- Nenhum Pull Request é aceito sem testes cobrindo o comportamento novo.
- Testes de integração validam o fluxo completo `controller → service →
  repository → Mongo` usando um banco de teste (ex: `mongomock` ou container
  efêmero), nunca o banco de desenvolvimento.

## 3. Separação de camadas — API

```
controllers  →  services  →  repositories  →  models
```

- `controllers`: apenas tradução HTTP/WS ↔ chamadas de `service`. Sem regra de
  negócio, sem acesso direto ao Mongo.
- `services`: regra de negócio, orquestração, decisões (ex: quando chamar a
  IA, como montar o histórico de contexto).
- `repositories`: única camada que fala com o MongoDB (via Motor). Sem regra
  de negócio.
- `models`: schemas/entidades (Pydantic). Sem lógica de negócio.
- Nunca pular camada (ex: controller chamando repository diretamente).

## 4. Separação de lógica e visualização — Web

- `components`: apresentação pura. Recebem dados via props, emitem eventos via
  callbacks. Não fazem fetch, não têm `useState` de regra de negócio.
- `hooks`: toda lógica de estado, efeitos colaterais e orquestração de
  chamadas a `services`. Um hook por responsabilidade (ex: `useConversation`,
  `useChatSocket`).
- `services` (frontend): isolam chamadas HTTP/WebSocket. Não importam React.
- Nenhum componente deve importar diretamente `fetch`/`axios`/`WebSocket`.

## 5. Objetivo da IA nesta POC é explícito e configurável

- O objetivo ("Convencer o usuário que a Terra é plana") vive em uma
  configuração (`AI_SYSTEM_GOAL`), nunca hardcoded espalhado pelo código.
- Isso é uma POC de arquitetura, não uma validação da crença. O agente de IA
  que gerar código deve tratar isso como um parâmetro de sistema substituível,
  mantendo o texto exatamente como especificado nos requisitos.

## 6. Simplicidade sobre esperteza

- Esta é uma POC. Preferir a solução mais simples que atenda a spec.
  Otimização prematura, abstrações genéricas ou infraestrutura extra não
  solicitada pelo arquiteto devem ser evitadas.

## 7. Cursor / agentes de IA que trabalham neste repositório

- Devem ler `.cursor/rules/030-sdd-workflow.mdc` antes de qualquer alteração.
- Devem citar, no início da resposta/PR, qual spec está sendo implementada.
- Não devem inventar requisitos fora de `specs/`. Se algo não está
  especificado, devem propor uma atualização de spec antes de codificar.
