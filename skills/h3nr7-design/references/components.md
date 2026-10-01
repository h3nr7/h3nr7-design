# Components

All classes are in `assets/h3nr7.css` and mirror h3nr7.com's own (`h3-` prefix). Rules of the
whole set: flat (no shadows), ink and greys only, the ground moves on hover and the label
never does, every link and button has a `:focus-visible` treatment paired with its `:hover`.

## Contents
Page layouts · Masthead · Rule · Section label · Prose · CV entry · Links · Buttons ·
Icon button · Chrome · Cards and panel · Person · Notice · Field · Dialog · Hover card ·
Placeholder grid · Gallery · Loading bar · Soft titles and split-flap

---

## Page layouts

| Class | What |
|---|---|
| `.h3-page` | Reading column: `max-width: 68ch`, centred, padding `3rem 1rem 6rem`. Articles, documents, the CV on a phone. |
| `.h3-page.h3-page-wide` | From 48rem up, widens to `--measure-page` (64rem+) for two-column layouts. |
| `.h3-home` + `.h3-landing` | Billboard: page column, then a landing block `--measure-landing` wide, centred on itself, padding `3rem 0 4rem`. |
| `.h3-cols` + `.h3-span-{2,3,4,6}` | From 48rem: 6 tracks, 3rem gutter, `align-items: start`. Below: stacked with a 2rem seam. |

Use **4 + 2** when the left is a record and the right a short index (CV: experience | skills,
education, references). Use **3 + 3** when both columns hold the same kind of thing (an
article's content | more content). Never reorder the DOM for the grid — reading order is the
same at every width.

## Masthead

```html
<header class="h3-masthead">
  <p class="h3-wordmark"><a href="/">h3nr7</a></p>   <!-- muted: the site, not the piece -->
  <h1>WebGl terrain mesh</h1>                         <!-- display italic, name size -->
  <p class="h3-standfirst">Create terrain mesh from NASA satellite data</p>
  <p class="h3-date">18 May 2020</p>
</header>
<span class="h3-rule h3-rule-soft" role="presentation"></span>
```

Wordmark and title are the same size; colour alone separates them. 24px from wordmark down
to title; standfirst sits on the title (4px); the date sits on the standfirst with no gap. On
the CV the `h1` *is* the wordmark ("iam h3nr7", ink), followed by a role line
"Name · Title" and a contact row, with a display-italic summary under it.

## Rule

`<span class="h3-rule" role="presentation"></span>` — a 1px ink line that draws itself on
from the left: `scaleX(0→1)`, 1000ms, `--ease-out`, after a 1000ms delay. Margins are
asymmetric, `3rem` above and `4rem` below: it closes the introduction and opens the record.

- `.h3-rule-soft` — muted instead of ink, under an article masthead (a black bar would
  compete with the title).
- `.h3-rule-close` — the rule that sits down on a footer: `3rem` above, `1.5rem` below, 2s
  delay.
- `.h3-card-rule` — the quick version inside a panel: 420ms after 160ms, margin `0.75rem 0`.

It is an element and not a `border` because borders cannot sweep. Ink, not `--colour-line`:
a line that draws attention to its own arrival and then turns out pale reads as a mistake.

## Section label

`<h2 class="h3-label">Experience</h2>` — Inter, `--text-sm`, uppercase, `0.08em`, faint,
`3rem` above and `1rem` below. Structurally a heading, typographically a signpost. In `.h3-prose`
every `h2` takes this automatically. Never Mrs Eaves.

## Prose (`.h3-prose`)

For rich text with bare tags. Paragraphs `0 0 1rem` at 1.5 leading (paragraph spacing, not
loose leading, does the separating). `h1` → display italic at name size; `h2` → label;
`h3` → display italic `xl`, 1.15 leading, `2rem 0 4px`; `h4`/`h5` → Inter faint (base / xs);
`h6` → display italic base, faint. Lists flush with the text, `⁌` markers inside, `0.5rem`
between items. Quotes: muted italic Inter, 1px `--colour-line` rule on the left — no quote
marks. Images 4px radius; captions xs faint. Links ink with the sweep underline.

## CV entry (`.h3-entry`)

```html
<article class="h3-entry">
  <h3>[Role] — [Company]</h3>
  <p class="h3-period">[Jan 2024] — Present</p>
  <p>One line on the remit.</p>
  <ul class="h3-points"><li>Outcome, with the number.</li></ul>
  <p class="h3-keywords">TypeScript · React · WebGPU</p>
</article>
<div class="h3-entry"><h3>Frontend</h3><ul class="h3-skills"><li>React</li><li>Three.js</li></ul></div>
```

Entries `3rem` apart — the gap between entries must beat the gap inside one. Title display
italic `xl`; the period closes up under it and pushes the description `1rem` away. Every
entry title in every section (roles, skill groups, qualifications, referees) is display
italic — one document, not two. Entry titles are never links.

## Links

Every in-text link: `.h3-link` (or any `a` inside `.h3-prose`, `.h3-landing-links`,
`.h3-footer`). Two hairlines painted as backgrounds: a full-width `--colour-line` rail at rest,
and an ink line that grows from 0 to 100% width, left to right, over 200ms on hover/focus.
`padding-bottom: 2px` keeps it clear of descenders; `box-decoration-break: clone` underlines
every line of a wrapped link. Colour by context: ink in prose; muted → ink on the landing
links (they are the content, so they step back); ink inside a faint footer (the actionable
words are the darkest in the sentence).

**Hollow letters** (`.h3-hollow`, opt-in): on display-size text that opens elsewhere, hover
drains the fill to transparent and leaves a 0.6px ink `-webkit-text-stroke` contour. Only on
large type; on small text the counters collapse and it reads as damaged. Never on links that
contain an icon.

## Buttons

| Class | Spec |
|---|---|
| `.h3-button` | Quiet chrome. `min-height: 1.75rem` (28px), padding `2px 0.5rem`, 4px radius, surface ground, ink text, Inter xs medium, `line-height: 1`. Hover/focus → `--colour-hover`. `aria-pressed="true"` / `aria-expanded="true"` → accent ground, accent-ink text (state read from ARIA, not a class). |
| `.h3-button-square` | Add to `.h3-button` for an icon-only control: 1.75rem square, padding 2px. |
| `.h3-cta` | The one filled action on a page (e.g. "Back to home" on an error page). Padding `0.5rem 1rem`, accent ground, accent-ink. Hover inverts to the hover ground *and* ink text. As wide as its label (`inline-flex`). |

No pill shapes, no outlines-as-buttons, no icon+label buttons in prose, no movement on hover.
28px is below the 44px touch target — fine for chrome, reconsider for a primary action.

## Icon button

`.h3-icon-button` — a 1.75rem square around a 14–16px icon inside a card (link-outs, social
marks). The mark never changes; the ground goes to `--colour-hover`. Ink, never brand colours.
A row of them: `.h3-social`, 4px gap, `-0.375rem` start margin so the glyphs align optically
with the text above.

## Chrome

`.h3-chrome` — a fixed row top-right (`1rem` in, safe-area aware), 4px gap, `z-index: 20`:
back arrow (square button), "Contact" (button), sound toggle (square). Nothing else floats.

## Cards and panel

```html
<div class="h3-panel">                      <!-- no ground of its own: the cards are the surfaces -->
  <div class="h3-card h3-card-row">
    <span class="h3-card-title">Let's have a chat</span>
    <a class="h3-icon-button" href="…" aria-label="Book a meeting">…chat icon…</a>
  </div>
  <div class="h3-card">…person…<span class="h3-card-rule"></span><div class="h3-social">…</div></div>
</div>
```

Card: `0.75rem` padding, 8px radius, surface ground, `--text-sm`, no border, no shadow.
Cards in a panel are separated by a 4px gap, not a divider — they are unrelated offers. Panel
20rem wide, anchored under the "Contact" button; it scales in from `0.96` and `-0.25rem` in
160ms (`h3-popover-in`), out in 120ms.

## Person

`.h3-person` → `.h3-person-avatar` (4rem square, 8px radius, photo `object-fit: cover` over
the initials) + `.h3-person-detail` (`.h3-person-name` semibold ink, `.h3-person-title` and
`.h3-person-url` muted). The photo square uses the card's radius so it reads as part of the
card, not a badge stuck on it.

## Notice

`.h3-notice` — status text in a box: 1px line border, 4px radius, padding `0.75rem 1rem`, muted
sm. For "feed unavailable" or "this list is incomplete", not for marketing.

## Field

`.h3-field` (grid, 4px gap, max 24rem) → `label`, `input` (padding `0.5rem 0.75rem`, 1px line
border, 4px radius, page ground), `.h3-field-hint` (faint sm), `.h3-field-error` (**ink** sm —
errors are said plainly, not coloured red). Inputs keep the 2px ink focus ring, offset 2px.

## Dialog

`.h3-scrim` (page colour at 75% + 3px backdrop blur — a wash toward the paper, never a black
overlay) + `.h3-dialog` (centred, 1.5rem padding, 1px line border, 16px radius, surface).
In: fade + `scale(0.96→1)` over 200ms; out: 140ms. A lightbox drops the panel entirely: the
photo sits full screen on the scrim with `object-fit: contain`.

## Hover card

`.h3-hovercard` — a picture that follows the pointer over a title: 1px ink border, ink ground,
`overflow: hidden`, radius `16px 16px 16px 0`. **The square corner is the point of contact**
(it sits at the cursor); `data-flip-x` / `data-flip-y` move the square corner when the card
flips near an edge. It starts as a 75px placeholder square and grows to the image's ratio in
260ms `cubic-bezier(0.2, 0, 0, 1)`. Static use (e.g. a thumbnail beside a title) keeps the
shape.

## Placeholder grid

`.h3-gridfield` + `.h3-monogram` — near-black `#0d0d0f` with white 1px lines at 13% every
14px, and the piece's initials centred (Mrs Eaves italic, lining figures, ligatures on — "TT" or "AV" fuse — 30px, white 82%).
This is the only acceptable empty-image state: it is the WebGL wireframe seen head-on.

## Gallery

`.h3-gallery` with `--cols: 1|2|3` — square tiles, 1rem gap, 4px radius, `object-fit: cover`;
under the pointer a tile drains to `grayscale(1)` over 450ms. A single image is not cropped.
"Show more (n)" is a `.h3-button` under the grid.

## Loading bar

`.h3-loading-bar` — fixed 2px line across the top: a `--colour-line` track with a 40% ink
segment sweeping across in 1100ms. Under reduced motion it becomes a still full bar.

## Soft titles and split-flap

- `.h3-soft` — text resting at `blur(3.8px)` and `opacity: 0.55`, sharp under hover/focus of its
  link (184ms in, 230ms back). Add `data-breathe` for a slow 5.2s blur "breath". Only under
  `(hover: hover)`: on touch it renders plain. Use for a run of titles that should invite
  pointing — never for body text or anything a phone reader needs.
- `data-scramble` + `assets/h3-scramble.js` — on hover/focus each character rolls through
  A–Z a–z 0–9 and lands on itself, staggered 26ms left to right, 460ms each (0.6× on leave);
  ligature pairs roll as one cell; widths are pinned so the line never jitters. Used on the
  wordmark, the landing titles and display headings. No colour or opacity change — movement
  only. Off under reduced motion.
