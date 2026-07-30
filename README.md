# ChatterBox - Monorepo

## Objetivo

Provar que é possível: iniciar uma conversa, trocar mensagens entre Usuário e IA,
persistir tudo em MongoDB, e ter a IA perseguindo um objetivo definido
("Convencer o usuário que a Terra é plana"), com bônus de streaming via WebSocket.

## Estrutura do monorepo

```
chatterbox/
├── .cursor/                 # Configuração do Cursor (agente de IA no editor)
│   ├── rules/                # Regras de projeto (.mdc) aplicadas automaticamente
│   └── skills/                # Skills específicas (playbooks) para tarefas recorrentes
├── specs/                   # Spec-Driven Development (SDD) — fonte da verdade do "o quê" e "como"
│   ├── constitution.md       # Princípios inegociáveis do projeto
│   ├── 001-iniciar-conversa/
│   ├── 002-ia-responde-com-objetivo/
│   └── 003-stream-mensagens-websocket/
├── apps/
│   ├── api/                  # ChatterBox API — Python + FastAPI + MongoDB
│   └── web/                  # ChatterBox Web — ReactJS
├── infra/                   # Scripts/seed de infraestrutura (ex: init do Mongo)
├── docs/                    # Documentação complementar (arquitetura, decisões)
├── docker-compose.yml
├── .env.example
└── .gitignore
```

## Stack

| Camada     | Tecnologia                          |
|------------|--------------------------------------|
| API        | Python 3.12, FastAPI, Motor (MongoDB async driver) |
| Banco      | MongoDB 7                            |
| Web        | ReactJS 18 + Vite + TypeScript        |
| IA         | Provedor configurável via `.env` (ver `apps/api/src/services`) |
| Realtime   | WebSocket nativo do FastAPI (opcional/requisito e) |
| Infra local| Docker Compose                       |

## Arquitetura da API (camadas)

```
controllers  →  services  →  repositories  →  models
 (HTTP/WS)      (regras de     (acesso a       (schemas /
                 negócio)       dados/Mongo)     entidades)
```

Cada camada só conhece a camada imediatamente abaixo. Ver
`.cursor/rules/010-backend-python-tdd.mdc` para as regras que o Cursor deve seguir
ao gerar código nessa pasta.

## Arquitetura do Web (componentes x lógica)

```
pages       → orquestram componentes + hooks
components  → apenas apresentação (recebem props, disparam callbacks)
hooks       → toda lógica de estado, efeitos e chamadas a serviços
services    → chamadas HTTP/WS isoladas (sem JSX, sem estado de UI)
```

Ver `.cursor/rules/020-frontend-react.mdc`.

## Como este repo deve ser usado (fluxo SDD)

1. Toda funcionalidade nasce como uma pasta em `specs/NNN-nome-da-feature/`
   contendo `spec.md` (o quê/por quê), `plan.md` (como, tecnicamente) e
   `tasks.md` (checklist executável).
2. O Cursor (ou qualquer agente) **deve ler a spec correspondente antes de
   escrever código** — ver `.cursor/rules/030-sdd-workflow.mdc`.
3. Implementação segue TDD: teste primeiro (red), implementação mínima (green),
   refatoração (refactor).
4. Specs já criadas nesta POC cobrem os requisitos mínimos (a, b, c, d) e o
   requisito opcional (e).

## Subindo a infraestrutura local

```bash
cp .env.example .env
docker compose up --build
```

Serviços esperados (definidos em `docker-compose.yml`):

- `mongo` — MongoDB 7, porta `27017`
- `api` — FastAPI, porta `8000` (docs em `/docs`)
- `web` — React (Vite dev server), porta `5173`
