---
name: h3nr7-design
description: Henry YP Ho's personal design system, as built for h3nr7.com and iam.h3nr7.com - a monochrome ink-on-paper palette, Mrs Eaves italic display type over an Inter body, hairline rules, no shadows, quiet motion - with the h3nr7 logo files, portrait, icons, bundled fonts, CSS tokens and ready-made page, CV, landing, slide and social-card templates. Use this skill whenever Henry (h3nr7) wants something that should look like his own brand or site - web pages, HTML artifacts, portfolio or article pages, a CV or bio, slide decks, documents, social or OG images, posters, README or email headers, diagrams - or says on-brand, my style, my site, h3nr7 style, iam h3nr7, or asks for his logo, colours, fonts or brand rules, or wants something restyled to match h3nr7.com. Do not use it for Lumina or Kyoso work, which has its own brand.
---

# h3nr7 design system

h3nr7 is Henry YP Ho's site and identity: "a techie journal of tinkering things". It looks like
a well-set page rather than an app — black ink on off-white paper, one literary serif italic
for the voice, one neutral sans for everything practical, hairlines where other systems use
boxes, and motion that behaves like a gesture (a rule drawing itself on, a blurred title coming
into focus, letters rolling like a split-flap board) rather than decoration.

Paths below are relative to this skill's folder. Values come from the live site's
`tokens.css`/`app.css`; the reasoning behind them is in `references/`.

## Look before you build

If you can view images, open two or three files in `assets/reference/` first —
`billboard-hover-light.jpg`, `article-light.jpg`, `contact-panel-light.png`, and
`ligatures.png` for what the display type must look like. They calibrate the look faster
than any description. Then start from the closest template in
`assets/templates/` rather than a blank page.

## What makes it h3nr7 — the essentials

1. **Monochrome, always.** Ink `#17171a` on page `#f6f6f7`, raised surfaces in white, four
   greys. There is no accent colour and no brand blue; the only colour on the site comes from
   photographs. Dark mode is a full inversion (page `#0e0e10`, ink `#f2f2f3`), never an
   afterthought — every colour is a role token that flips.
2. **Two faces, two jobs.** Display = **Mrs Eaves OT Italic** — the only cut in use, regular
   weight, **ligatures always on** — for the name, titles, statements and entry headings.
   Body = Inter for prose and *all* UI: buttons,
   labels, captions, navigation. Section labels are Inter, uppercase, tracked 0.08em, small
   and faint — the smallest thing in a section, while the entry titles under them are the
   largest. That inverted hierarchy is deliberate.
3. **Hairlines, not boxes.** 1px rules and borders; no `box-shadow` anywhere; flat surfaces.
   Radii double: 4px controls, 8px cards and avatars, 16px panels and dialogs.
4. **Space on a 4px scale, text on a measure.** Running text sits on a 68ch column; wider
   layouts use a 6-track grid with a 3rem gutter, split 4+2 (record beside an index) or 3+3
   (two of the same kind). Left-aligned, ragged right. Air is asymmetric: more below a rule
   than above it.
5. **Quiet motion.** Only the ground changes on hover — labels never fade or shift. Rules
   sweep in left to right; links grow an ink underline over a grey rail; titles can rest
   blurred and sharpen under the pointer. Everything has a `prefers-reduced-motion` answer.

## Core tokens

| Role | Light | Dark | Use |
|---|---|---|---|
| `--colour-page` | `#f6f6f7` | `#0e0e10` | the ground |
| `--colour-surface` | `#ffffff` | `#17171a` | cards, buttons at rest, dialogs |
| `--colour-hover` | `#e8e8ea` | `#24242a` | hover ground, skeletons |
| `--colour-ink` | `#17171a` | `#f2f2f3` | text, rules, filled controls |
| `--colour-ink-muted` | `#595a5f` | `#a6a7ac` | standfirsts, roles, secondary lines |
| `--colour-ink-faint` | `#8a8b90` | `#6f7076` | labels, dates, captions, keywords |
| `--colour-line` | `#e2e2e5` | `#2a2a2f` | borders nobody should notice |
| `--colour-accent` / `-ink` | `#17171a` / `#fff` | `#f2f2f3` / `#0e0e10` | the filled state: CTA, pressed button |

Type scale (1.25 ratio): 2xs .694 · xs .833 · sm .9 · base 1 · lg 1.25 · xl 1.563 · 2xl 1.953 ·
3xl 2.441 · 4xl 3.052rem. Plus two off-scale display sizes: **name** `clamp(1.5rem → 2rem)` and
**statement** `clamp(3rem → 4rem)` (48pt). Leading: display 0.95, tight 1.15, normal 1.5.
Spacing: 4 · 8 · 12 · 16 · 24 · 32 · 48 · 64 · 96px. Everything else: `references/tokens.md`,
machine-readable in `assets/tokens.json`, drop-in CSS in `assets/h3nr7.css`.

## Type rules that are easy to get wrong

- **Ligatures on, always — this matters more than anything else about the type.** Display
  text gets `font-variant-ligatures: common-ligatures discretionary-ligatures contextual`
  (OpenType `liga` + `dlig` + `calt`). In this italic that fuses **fi ff fl ft fr ffi ffl**
  (liga) and **st ct sp ee ae oe it tt ty tw ky gi gy gg py ip fy Th THE TT AV** and more
  capital pairs (dlig). "coffee", "aesthetic", "street", "act" must show their ligatures —
  compare `assets/reference/ligatures.png`. Full list in `references/typography.md`.
- **Never letter-space the display face.** Any tracking, even 0.005em, silently switches the
  ligatures off. Tighten size or measure instead. No `font` shorthand on display type either
  (it resets ligatures).
- **Italic only, never bold.** Mrs Eaves OT Italic is the one cut: never ask for roman, bold or
  small caps (they would be faked). Emphasis comes from size and colour. The logo is the one
  Bold Italic object, and it is a drawing, not type.
- **Labels are never Mrs Eaves.** Anything uppercase-and-tracked is Inter.
- Mrs Eaves has a small x-height: set it a step larger than Inter to look the same size
  (entry titles are `xl` over `base` body).
- Figures are oldstyle by default in the display face; use lining figures for tables,
  monograms and numbers set against capitals.
- Sentence case for everything a person reads; uppercase comes only from CSS on labels.
- Em dash with spaces for a role and its company ("Engineer — Company"); middot with spaces
  for a run of short items ("React · WebGL · AWS").

Detail, per element: `references/typography.md`.

## Fonts outside h3nr7.com — read this before any output

The display face is **Mrs Eaves** — never substitute another serif for it. The site loads it
and Inter from an Adobe Fonts kit that only serves h3nr7.com, so this skill carries the font
files itself: `assets/fonts/fonts.json` lists every bundled face — "Mrs Eaves OT" Italic
(`MrsEavesOT-Italic.ttf` for desktop tools, `.woff2` repaired so browsers accept it) and
Inter at the site's 18pt optical size. Mrs Eaves is a licensed commercial face whose
embedding permission is *Preview & Print*: a self-contained HTML file is for Henry's own
viewing and presenting, **anything going to other people goes as PDF**, and the font files
themselves are never sent or published.

| Output | Do this |
|---|---|
| HTML artifact shown in chat | Paste `assets/h3nr7.css` into a `<style>`. Do not paste base64 fonts — far too many tokens. Mrs Eaves renders only where it is installed; tell Henry the preview's display type is a fallback, and offer a standalone file for the real thing. |
| HTML file (page, deck, one-pager) | Write it linking the skill's CSS/JS/images by path, then run `python scripts/inline.py page.html` — it inlines everything and embeds Mrs Eaves + Inter. For Henry to view or present. |
| PDF | The HTML file above, printed (see `references/outputs.md`). **The format for anything that goes to someone else.** |
| Word | Fonts by name ("Mrs Eaves OT" italic, "Inter") with ligatures set to *All* — see `outputs.md`. The opening machine needs the fonts installed. |
| PowerPoint | Cannot switch on discretionary ligatures, so Mrs Eaves loses st/ct/ee/ae there. Prefer `templates/slides.html` → PDF; if a .pptx is required, say what it loses. |
| Raster image (Pillow) | The Mrs Eaves file named in `fonts.json` + `Inter-*.ttf`. Ligatures need Pillow with libraqm and `features=["liga","dlig"]`; without it, render HTML instead. |

If `fonts.json` lists no Mrs Eaves face (a build made without the files), say so instead of
quietly substituting; the fallback stack is a last resort, not a choice.

## Logo and imagery

| Asset | Use it for |
|---|---|
| `assets/logo/h3nr7-mark.svg` | The stacked "h3r / n7" mark, tight to the ink, `currentColor`. Inline in HTML. |
| `h3nr7-mark-black.svg/.png`, `h3nr7-mark-white.svg/.png` | Same mark, fixed colour, transparent. PNG for Office. |
| `h3nr7-tile-dark.svg/.png` (+ `-1280.png`) | White mark on a black square — the avatar, social card and og:image. |
| `h3nr7-tile-light.svg/.png` | Black on white, for light contexts that need a square. |
| `h3nr7-glyph.svg/.png` | The favicon: a square's bottom-right half. For 32px and below only. |
| `assets/images/portrait-600.jpg`, `-1200.jpg` | Henry's portrait. Only where it is his profile. |
| `assets/icons/*.svg` | The site's icons, `currentColor`. |

- The mark is a drawing in Mrs Eaves Bold Italic. Use the files; never re-typeset it, stretch,
  rotate, outline, shadow or recolour it beyond ink/black/white.
- Clear space: at least the width of the mark's "n" on every side; the tiles show the intended
  margins (the mark fills about 51% of the width). Below about 48px tall, use the glyph instead.
- In running headers the signature is the **text wordmark** — `h3nr7` set lowercase in display
  italic (`.h3-wordmark` / `.h3-landing-name`) — not the stacked mark.
- Portrait: square, 8px radius (never a circle), 64px in a card; the initials "HH" underneath
  as the fallback.
- No stock imagery. An empty image slot is `.h3-gridfield` — a near-black square grid with the
  piece's initials in lining figures — which echoes the WebGL wireframe behind the site.
- Icons: filled brand marks at 16px, stroked UI icons at 14px with a 2px round stroke; always
  ink, never the platforms' brand colours.

More, including the backdrop and reference screenshots: `references/brand-assets.md`.

## Voice

First person, plain and a little dry; British spelling. Short labels that say what a thing
does ("Back to home", "Print this CV", "Show more (4)"). Friendly closers rather than calls to
action: "Let's have a chat", "Drop me an email for the full CV.", "Otherwise I am always up for
a coffee and/or a chat." Errors own up simply: "Oops! Looks like the feed is unavailable right
now." More in `references/voice.md`.

## Building something

1. **Pick the template** in `assets/templates/`:
   `page.html` (article, report, write-up, one-pager) · `cv.html` (CV, bio, profile) ·
   `landing.html` (home, portfolio index, link page) · `slides.html` (16:9 deck, prints to PDF)
   · `social-card.html` (1200×630 og image, cover). `assets/specimen.html` shows every
   component at once.
2. **Use the `h3-` classes** from `assets/h3nr7.css` — catalogue in `references/components.md`.
   Add `assets/h3-scramble.js` and `data-scramble` for the split-flap roll on hover.
3. **Check** light and dark (`data-theme="dark"` on `<html>` forces it), a 390px-wide phone,
   and reduced motion. Nothing should scroll sideways.
4. Deliver: an artifact for a quick look; otherwise a file — run `scripts/inline.py` on any
   HTML file before handing it over. For PDF, Word, PowerPoint, images and charts, follow
   `references/outputs.md`.

Minimal page:

```html
<!doctype html>
<html lang="en-GB">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Title — h3nr7</title><style>/* contents of assets/h3nr7.css */</style></head>
<body>
<main class="h3-page">
  <header class="h3-masthead">
    <p class="h3-wordmark">h3nr7</p>
    <h1>Title in display italic</h1>
    <p class="h3-standfirst">What this is, in one line.</p>
    <p class="h3-date">1 October 2026</p>
  </header>
  <span class="h3-rule h3-rule-soft" role="presentation"></span>
  <div class="h3-prose">
    <h2>Section label</h2>
    <p>Body text in Inter, on a 68ch measure.</p>
  </div>
</main>
</body>
</html>
```

## What it is not

Anything that would look at home on a SaaS landing page is wrong here: gradients, drop
shadows, glass, coloured accents, pill buttons, circular avatars, emoji as icons, icon fonts,
stock photos, centred body text, bold or all-caps serif headings, tracked serif, card grids
with borders and shadows, hero banners with a button stack. When unsure, take something away.

## Files

```
SKILL.md
references/  tokens.md · typography.md · components.md · motion.md · brand-assets.md · voice.md · outputs.md
assets/      h3nr7.css · h3-scramble.js · tokens.json · specimen.html
             logo/ · icons/ · images/ · fonts/ · reference/ · templates/
scripts/     inline.py   (make an HTML file self-contained, fonts embedded)
```
