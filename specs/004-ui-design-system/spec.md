# Spec 004 — Design System UI

Define a identidade visual transversal do ChatterBox Web. Aplica-se a todas
as páginas e componentes do frontend.

## Contexto

O frontend precisa de uma base visual consistente antes da implementação das
features de chat (spec 001). Esta spec cobre apenas tokens, layout global e
convenções de estilo — não funcionalidade de negócio.

## Objetivo

Estabelecer uma linguagem visual coesa: tipografia Roboto, paleta azul/verde,
bordas suavemente arredondadas, Tailwind CSS e Heroicons (outline).

## Requisitos

1. Fonte principal: **Roboto** (Regular 400, Medium 500, Bold 700).
2. Paleta de cores (tokens):
   - `brand` — `#2b9eb3` (primária: header, botões, destaques)
   - `accent` — `#85cc9c` (secundária: badges, estados positivos)
   - `surface` — `#bcd9a0` (fundos suaves, cards, áreas de conteúdo)
   - `ink` — `#484848` (texto principal, ícones escuros)
3. Bordas arredondadas de forma suave (`rounded-xl` a `rounded-3xl` como
   padrão; evitar cantos retos em containers principais).
4. Estilização exclusivamente via **Tailwind CSS** (sem CSS modules ou styled-
   components nesta POC).
5. Ícones via **Heroicons** (`@heroicons/react`), preferindo a variante
   **outline** (`/24/outline`).
6. Layout global (`AppLayout`) envolve todas as páginas: header com marca,
   área de conteúdo centralizada com card arredondado.

## Fora de escopo

- Temas dark/light alternáveis.
- Componentes de chat (MessageBubble, MessageInput) — specs 001/002.
- Animações complexas ou bibliotecas de UI (MUI, Chakra, etc.).

## Critérios de aceite

- [ ] Roboto carregada e aplicada como `font-sans` global.
- [ ] Tokens de cor disponíveis no `tailwind.config` (`brand`, `accent`,
      `surface`, `ink`).
- [ ] `AppLayout` renderiza header + main com paleta e bordas arredondadas.
- [ ] Pelo menos um ícone Heroicons outline visível no layout global.
- [ ] Rules, skills e plan documentam as convenções acima.
