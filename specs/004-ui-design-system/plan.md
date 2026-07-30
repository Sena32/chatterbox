# Plan 004 — Design System UI

## Stack de estilo

| Ferramenta | Uso |
|---|---|
| Tailwind CSS v3 | Utility classes; tokens customizados no `theme.extend` |
| Google Fonts (Roboto) | Tipografia via `<link>` em `index.html` |
| `@heroicons/react` | Ícones outline (`/24/outline`) |

## Tokens de cor (Tailwind)

```js
// tailwind.config.js → theme.extend.colors
brand:   '#2b9eb3'   // primária
accent:  '#85cc9c'   // secundária
surface: '#bcd9a0'   // fundos
ink:     '#484848'   // texto
```

Uso semântico sugerido:

- **Fundo da página:** gradiente ou tom claro derivado de `surface` (`bg-surface/20`).
- **Header:** `bg-brand` com texto branco.
- **Card principal:** `bg-white` com `border-surface`, `rounded-2xl`, sombra suave.
- **Texto:** `text-ink`; secundário com `text-ink/70`.

## Bordas arredondadas

| Elemento | Classe Tailwind |
|---|---|
| Card principal | `rounded-2xl` |
| Header / footer internos | `rounded-xl` |
| Botões / inputs (futuro) | `rounded-xl` |
| Pills / badges | `rounded-full` |

Evitar `rounded-none` e `rounded-sm` em containers visíveis.

## Estrutura de arquivos

```
apps/web/
  index.html              ← link Google Fonts Roboto
  tailwind.config.js      ← tokens de cor + fontFamily
  postcss.config.js
  src/
    index.css             ← @tailwind directives + base styles
    components/
      Layout/
        AppLayout.tsx     ← shell global (header + main)
    pages/
      ChatPage.tsx        ← compõe AppLayout + conteúdo futuro
```

## AppLayout — contrato

Componente de apresentação pura. Recebe `children` via props.

```tsx
interface AppLayoutProps {
  children: React.ReactNode
}
```

Estrutura visual:

1. `<div>` raiz — `min-h-screen`, fundo claro com tom `surface`.
2. `<header>` — barra superior `brand`, logo + título, ícone outline.
3. `<main>` — container centralizado (`max-w-3xl`), card branco arredondado
   com padding generoso, recebe `children`.

## Ícones Heroicons

```tsx
import { ChatBubbleLeftRightIcon } from "@heroicons/react/24/outline"
```

Regra: usar sempre `/24/outline`. Só usar `/24/solid` se o outline não existir
para o ícone necessário.

## Documentação do projeto

Atualizar antes de codificar:

- `specs/constitution.md` — seção Web, referência ao design system.
- `.cursor/rules/020-frontend-react.mdc` — seção Estilo / Tailwind.
- `.cursor/skills/react-hooks-separation/SKILL.md` — exemplos com Tailwind.
- `.cursor/skills/frontend-design-system/SKILL.md` — playbook de tokens e layout.
- `.cursor/rules/030-sdd-workflow.mdc` — listar spec 004.
