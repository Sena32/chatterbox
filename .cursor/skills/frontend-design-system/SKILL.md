---
name: frontend-design-system
description: Use esta skill ao criar ou modificar estilos, layout global ou componentes visuais em apps/web/. Cobre Tailwind CSS, tokens de cor, fonte Roboto, bordas arredondadas e Heroicons outline conforme specs/004-ui-design-system/.
---

# Frontend — Design System (Tailwind + Roboto + Heroicons)

## Quando usar

Sempre que a tarefa envolver: layout global, cores, tipografia, ícones,
bordas, ou qualquer estilização visual em `apps/web/`.

Spec de referência: `specs/004-ui-design-system/`.

## Tokens de cor

Use os nomes semânticos do Tailwind — **nunca** hex inline no JSX:

| Token | Hex | Uso |
|---|---|---|
| `brand` | `#2b9eb3` | Header, botões primários, links |
| `accent` | `#85cc9c` | Destaques secundários, badges |
| `surface` | `#bcd9a0` | Fundos suaves, bordas de card |
| `ink` | `#484848` | Texto principal |

Exemplos:

```tsx
<header className="bg-brand text-white">...</header>
<main className="bg-white text-ink border border-surface/40 rounded-2xl">...</main>
<p className="text-ink/70">Texto secundário</p>
```

## Tipografia

- Fonte: **Roboto** (`font-sans`), pesos 400/500/700.
- Carregada em `index.html` via Google Fonts.
- Títulos: `font-bold text-ink`; corpo: `font-normal text-ink`.

## Bordas arredondadas

| Elemento | Classe |
|---|---|
| Card / painel principal | `rounded-2xl` |
| Sub-seções | `rounded-xl` |
| Botões / inputs | `rounded-xl` |
| Badges / avatares | `rounded-full` |

Evitar `rounded-none` e `rounded-sm` em containers visíveis.

## Ícones — Heroicons outline

```tsx
import { PaperAirplaneIcon } from "@heroicons/react/24/outline"

<PaperAirplaneIcon className="h-5 w-5" aria-hidden="true" />
```

Regras:

- Importar sempre de `@heroicons/react/24/outline`.
- Usar `/24/solid` **somente** se o ícone não existir em outline.
- Tamanho padrão: `h-5 w-5` (20px); header: `h-6 w-6`.

## Layout global — AppLayout

Todas as páginas usam `AppLayout`:

```tsx
// src/pages/ChatPage.tsx
import { AppLayout } from "../components/Layout/AppLayout"

export function ChatPage() {
  return (
    <AppLayout>
      {/* conteúdo da página */}
    </AppLayout>
  )
}
```

`AppLayout` é componente de apresentação puro — recebe `children`, sem hooks
de negócio, sem fetch.

## Estrutura de arquivos de estilo

```
apps/web/
  tailwind.config.js    ← tokens (colors, fontFamily, borderRadius)
  postcss.config.js
  src/index.css         ← @tailwind base/components/utilities
  index.html            ← <link> Google Fonts Roboto
```

## Checklist antes de concluir

- [ ] Cores via tokens Tailwind (`brand`, `accent`, `surface`, `ink`).
- [ ] `font-sans` (Roboto) aplicada globalmente.
- [ ] Ícones Heroicons outline.
- [ ] Bordas suavemente arredondadas nos containers.
- [ ] Nenhum CSS ad-hoc fora de `index.css` e classes Tailwind.
- [ ] `AppLayout` usado como shell das páginas.
