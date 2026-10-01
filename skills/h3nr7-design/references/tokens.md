# Tokens

Every value on h3nr7.com is a CSS custom property, named by **role**, never by appearance —
`--colour-ink`, not `--black` — so a theme flip or a redesign changes values, not names.
British spelling (`colour`) is part of the names. The same set is in `assets/h3nr7.css`
(CSS) and `assets/tokens.json` (data).

## Colour

| Token | Light | Dark | Role |
|---|---|---|---|
| `--colour-page` | `#f6f6f7` | `#0e0e10` | The ground. Off-white, not white, so white surfaces read as raised. |
| `--colour-surface` | `#ffffff` | `#17171a` | A plane above the page: cards, buttons at rest, dialogs. Lighter than the page in both themes. |
| `--colour-hover` | `#e8e8ea` | `#24242a` | A control under the pointer; skeleton placeholders. Darker than the page in light ("pressed into the paper"). |
| `--colour-ink` | `#17171a` | `#f2f2f3` | Text, deliberate rules, filled controls, focus rings. |
| `--colour-ink-muted` | `#595a5f` | `#a6a7ac` | Secondary lines: standfirst, role, person title, quotes, muted links. |
| `--colour-ink-faint` | `#8a8b90` | `#6f7076` | Metadata: labels, dates, captions, keywords, footer prose. |
| `--colour-line` | `#e2e2e5` | `#2a2a2f` | Borders a reader is not meant to notice; the link rail. |
| `--colour-accent` | `#17171a` | `#f2f2f3` | The filled state (CTA, pressed/expanded button). Same as ink — there is no accent hue. |
| `--colour-accent-ink` | `#ffffff` | `#0e0e10` | Text on the accent. |
| `--colour-focus` | `var(--colour-ink)` | (follows ink) | Focus ring. Was blue once; removed because it was the only colour on the site. |

Fixed values outside the theme (they never flip):

| Value | Where |
|---|---|
| `#000000` / `#ffffff` | The logo master and its tiles. |
| `#0d0d0f` + `rgb(255 255 255 / .13)` 1px lines every 14px | `.h3-gridfield`, the image placeholder. |
| `rgb(255 255 255 / .82)` | Initials on the placeholder. |
| `color-mix(in srgb, var(--colour-page) 75%, transparent)` + `blur(3px)` | Modal scrim — a wash toward the page, never a black scrim. |
| `opacity: .19` | Filler text that is not information (e.g. lorem around a status line). |

Contrast against the page (WCAG, computed): ink 16.6:1 light / 17.2:1 dark; muted 6.4:1 /
8.0:1 (AA for body text); faint 3.2:1 / 3.9:1 — below AA for body, so faint is for metadata
(dates, labels, captions) and the one short closing line of a footer — never for body copy.
The hover ground moves
only ~1.1–1.3:1 from the page, a known trade the site accepts for chrome; the focus ring
(2px ink) is what keyboard users rely on for inputs.

**No other colours.** Charts, diagrams and states are built from these greys plus ink (see
`outputs.md` → charts). Photographs are the only source of hue.

## Type

| Token | Value |
|---|---|
| `--font-display` | `mrs-eaves, 'Mrs Eaves OT', 'Mrs Eaves', Baskerville, 'Libre Baskerville', 'Times New Roman', Times, serif` — the kit name, then the desktop/bundled family (Mrs Eaves OT Italic), then system serifs with real italics as a last resort only |
| `--font-body` | `inter-18pt, Inter, 'Inter 18pt', ui-sans-serif, system-ui, -apple-system, 'Segoe UI', sans-serif` |
| `--font-mono` | `ui-monospace, 'SF Mono', 'Cascadia Mono', Menlo, Consolas, monospace` (no brand mono) |

Scale, 1.25 modular, named by step:

| Token | rem | px @16 |
|---|---|---|
| `--text-2xs` | 0.694 | 11.1 |
| `--text-xs` | 0.833 | 13.3 |
| `--text-sm` | 0.9 | 14.4 |
| `--text-base` | 1 | 16 |
| `--text-lg` | 1.25 | 20 |
| `--text-xl` | 1.563 | 25 |
| `--text-2xl` | 1.953 | 31.2 |
| `--text-3xl` | 2.441 | 39 |
| `--text-4xl` | 3.052 | 48.8 |
| `--text-landing-name` | `clamp(1.5rem, 1.29rem + 0.88vw, 2rem)` | 24 → 32 |
| `--text-landing` | `clamp(3rem, 2.58rem + 1.76vw, 4rem)` | 48 → 64 (= 48pt at 1280px) |

The two `landing` sizes are off the scale on purpose: they were chosen, not derived.

| Leading | Value | For |
|---|---|---|
| `--leading-display` | 0.95 | Display statements and names only (Mrs Eaves' small x-height survives it). |
| `--leading-tight` | 1.15 | Display subheads (`xl`). |
| `--leading-normal` | 1.5 | Body, UI, small headings. The `html` default. |
| `--leading-loose` | 1.7 | Rarely; paragraph spacing does the separating instead. |

| Weight | Value | Note |
|---|---|---|
| `--weight-light` | 300 | Renders as 100 from the kit. Avoid. |
| `--weight-regular` | 400 | Default for both faces. |
| `--weight-medium` | 500 | Buttons, card titles. The kit has no 500, so it renders as 400 — don't rely on it as a step. |
| `--weight-semibold` | 600 | The one real step up: a name over its captions. |
| `--weight-bold` | 700 | Exists; almost never used. Bold at 13px is shouting. |

## Space, radius, width

Spacing (4px base): `--space-1` .25rem · `-2` .5 · `-3` .75 · `-4` 1 · `-6` 1.5 · `-8` 2 ·
`-12` 3 · `-16` 4 · `-24` 6rem. There is no 5, 7, 10 — a step up is always the next token.

Radius (doubling): `--radius-sm` 2px · `-md` 4px (controls, images) · `-lg` 8px (cards,
avatar) · `-xl` 16px (panels, dialogs, hover card).

| Width | Value | Holds |
|---|---|---|
| `--measure` | 68ch | Running text: articles, CV below md, forms' prose. |
| `--measure-page` | 64rem → 76rem (≥96rem) → 94rem (≥120rem) | Outer page column; two-column layouts. |
| `--measure-landing` | 60rem → 72rem → 90rem | The landing statement, centred on itself. Always 4rem narrower than the page. |
| `--measure-form` | 24rem | Inputs. |

`ch` only on the element that carries the type — on a wrapper it resolves against 16px body
text and strangles display type inside it.

Breakpoints (Tailwind's, in rem): `48rem` (md — grids switch on), `96rem` (2xl), `120rem`
(3xl, 1920px). Widths step at the last two; nothing is fluid between them except the two
`clamp()` sizes.

## Motion, layers

`--duration-fast` 120ms (ground changes) · `--duration-normal` 200ms (underline, dialog) ·
`--ease-out` `cubic-bezier(0.16, 1, 0.3, 1)`. Effect-specific durations live with their
effect (see `motion.md`).

z-index: canvas 0 · content 10 · chrome 20 · hover card 50 · overlay 100 (dialog +1, its
loading bar +2).

## shadcn / Tailwind mapping

The site aliases shadcn's names to its own so components paste in unedited:
`--background`→page, `--foreground`→ink, `--card`/`--popover`→page, `--primary`→ink,
`--primary-foreground`→page, `--secondary`/`--muted`/`--accent`→surface,
`--muted-foreground`→ink-muted, `--border`/`--input`→line, `--ring`→focus. Note shadcn's
`--accent` (a hover surface) is not `--colour-accent` (the filled state). Tailwind v4 reads
them via `@theme inline` as `bg-page`, `text-ink`, `text-ink-muted`, `border-line`,
`font-serif` (display), `font-sans` (body).
