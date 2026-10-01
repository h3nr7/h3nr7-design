# Typography

## The two faces

**Mrs Eaves OT Italic** (Zuzana Licko, Emigre, 1996) — a Baskerville revival with a famously
small x-height, open counters and a large set of ligatures. The **italic is the only cut in
use**, at regular weight, and always with its ligatures on. It is the voice: the name, page
titles, the landing statement, entry titles, subheads, the monogram.

**Inter**, at its 18pt optical size (`inter-18pt` in the kit) — cut for reading at text
sizes. Everything practical: prose, buttons, labels, captions, navigation, form fields.

Chrome is navigation, not part of the statement, so it is never set in the display face —
including tiny UI text, where a discretionary ligature ("ct" in "Contact") would be a bug.

### Where the faces come from

| Context | Display | Body |
|---|---|---|
| h3nr7.com | Adobe kit `jik4pcx` (`mrs-eaves`, `inter-18pt`) | same kit |
| Desktop apps | "Mrs Eaves OT" Italic, where installed | Inter |
| Files this skill makes | bundled `MrsEavesOT-Italic`, embedded by `scripts/inline.py` | bundled Inter |

**Mrs Eaves is the display face — there is no substitute.** The CSS stack ends in system
Baskervilles only so a page never collapses to a sans; if a build of this skill has no Mrs
Eaves file (`assets/fonts/fonts.json` lists none), say so rather than presenting the
fallback as the brand. Mrs Eaves is licensed to Henry: embed it in his own documents, never
send or publish the font files. The kit is domain-locked; never try to fetch it for a page
that will live elsewhere. Akkurat and Rift, from the old v3 site, are retired.

The bundled web font is the desktop file with its CFF table rewritten: Chrome's sanitiser
rejects the 1996 original ("CFF: Failed to parse Top DICT Data") — the foundry's own web kit
included — and a rejected `@font-face` fails silently. Outlines and features are unchanged.

## Feature settings

Exactly what h3nr7.com sets (`packages/ui/src/styles/fonts.css`):

```css
:root { font-kerning: normal; font-variant-ligatures: common-ligatures contextual; }
h1, h2, h3, h4, .h3-display, .h3-landing-name, .h3-landing-lede {
  font-family: var(--font-display);
  font-variant-ligatures: common-ligatures discretionary-ligatures contextual;  /* liga+clig, dlig, calt */
  letter-spacing: normal;            /* a requirement, not a default */
  text-rendering: optimizeLegibility;
}
```

`assets/h3nr7.css` adds `font-style: italic` and `font-synthesis: style` (one cut, so never a
faux bold). Body text and UI keep `common-ligatures contextual` only: a discretionary ligature
in a label ("ct" in "Contact") is a bug.

**The ligature set of the bundled Mrs Eaves OT Italic** — shaped with HarfBuzz, every pair of
letters plus the three-letter candidates, comparing glyphs with the features off and on.
`assets/reference/ligatures.png` shows them rendered.

| Feature | CSS keyword | Ligatures |
|---|---|---|
| `liga` | `common-ligatures` | ff fi fl fb fh fj fr ft · ffi ffl ffb ffh ffj ffr fft |
| `dlig` | `discretionary-ligatures` | ae ct ee fy gg gi gy ip it ky oe py sp st tt tw ty · cky ggy tty ffy |
| `dlig` capitals | `discretionary-ligatures` | AA AV FF FI FL HE LA MB MD ME MP NK NT OC OG OO TE TR TT TW TY UB UD UL UP UR VA · Th · THE |

So "office" is 6 letters in 4 glyphs, "coffee" 6 in 4 (ff + ee), "aesthetic" 9 in 7
(ae + st), "street" 6 in 4, "THE" one glyph. Write display copy knowing this — the
ligatures are the reason for the face.

- **Any non-zero `letter-spacing` disables them** (Chrome drops optional ligatures once
  tracking is applied; `-0.005em` is enough). So display type is never tracked, never set
  with a `font` shorthand (which resets ligatures), and `font-feature-settings` is avoided in
  favour of `font-variant-*` (it replaces rather than adds).
- The kit h3nr7.com serves is a different build: the site's own notes measured its italic
  as having no fi/ffi and a smaller set. That measurement compared text *widths*, which cannot
  see a ligature drawn to the same advance as its letters (fi, ee, ae, ct here are exactly
  that), so trust shaping, not width, when checking a face.
- Figures are **oldstyle by default** — no `onum` needed. For lining figures (tables, numbers
  against capitals, a two-letter monogram like "R3") use `font-variant-numeric: lining-nums`;
  the italic has `lnum` (and `tnum`).
- There are no small caps in this cut (no `smcp`). Do not use `font-variant-caps`; it would be
  synthesised. A caps label is Inter.
- Body text may track freely; it has no discretionary ligatures to lose.

## Hierarchy, element by element

| Element | Face / cut | Size | Leading | Colour | Air |
|---|---|---|---|---|---|
| Landing name `h3nr7` | display italic 400 | `--text-landing-name` (24→32) | 0.95 | ink | 0 0 0.8rem |
| Landing statement | display italic 400 | `--text-landing` (48→64) | 0.95 | ink | — ; `text-wrap: pretty` |
| Page wordmark (above a title) | display italic 400 | landing-name | 0.95 | **muted** | 0 0 1.5rem |
| Page / article title `h1` | display italic 400 | landing-name | 0.95 | ink | 0 |
| CV summary | display italic 400 | landing-name, full width | 0.95 | ink | 0 0 1.5rem |
| Standfirst / role line | Inter 400 | base | 1.5 | muted | 4px above |
| Date | Inter 400 | xs | 1.5 | faint | 0 |
| Section label `h2` | **Inter**, UPPERCASE, 0.08em | sm | 1.5 | faint | 3rem above, 1rem below |
| Entry title / subhead `h3` | display italic 400 | xl (25) | 1.15 | ink | 0 0 4px (closes to 0 over a date) |
| Entry period | Inter | xs | 1.5 | faint | 0 0 1rem |
| Body paragraph | Inter 400 | base | 1.5 | ink | 0 0 1rem |
| Keywords / skills run | Inter | xs | 1.5 | faint | 0.5rem 0; skills joined by " · " |
| `h4` in prose | Inter | base | 1.5 | faint | 0 0 4px |
| `h5` in prose | Inter | xs | 1.5 | faint | 0 |
| `h6` in prose | display italic | base (optically = h5) | 1.5 | faint | 0 |
| Quote | Inter italic | base | 1.5 | muted | 2rem 0; 1px line rule left, 1rem pad |
| Caption | Inter | xs | 1.5 | faint | 0.5rem above |
| Buttons, chrome | Inter 500(→400) | xs | 1 | ink | — |
| Card text | Inter | sm | 1.5 | ink / muted | — |
| Landing links | Inter, UPPERCASE, 0.08em | sm | — | muted → ink | gap 1.5rem, 3rem above |
| Footer / closing line | Inter | sm | 1.5 | faint, links ink | — |

Two consequences worth internalising:

- **The section label is the smallest thing in its section**, and the entry title under it the
  largest. The label says where you are; the title is what you are reading.
- **A display title at 2rem outranks body at 2.4rem**, because face and cut carry presence.
  A heading's presence is its size *and* its measure: a one-line title can stay at the name
  size where a long summary would look bigger at the same size.

## Lists and marks

- Bulleted lists: marker `⁌ ` (U+204C, black leftwards bullet) with a trailing space,
  `list-style-position: inside`, flush with the prose (no indent). Declare `disc` first as a
  parser fallback. Neither face has the glyph; a system font draws it.
- Numbered lists keep decimal numbers.
- Inline runs of short items (skills): middot with spaces, `' · '`.
- Role and company: em dash with spaces, "Platform Engineer — Company".
- Name and title in one line: middot, "Henry YP Ho · Platform & Product Engineer".
- A list of titles set as one sentence (landing): full stop and a space between titles.

## Sizes in other media

| Medium | Display | Body | Label |
|---|---|---|---|
| Web page | 24–32px titles, 48–64px statement, 25px subheads | 16px | 14.4px caps |
| Slides 1280×720 | 52–72px statement, 40–52px slide title | 20px | 14px caps |
| Social card 1200×630 | 64px title, 32px wordmark | 22px standfirst | — |
| A4 document | 20–24pt title, 14pt subheads | 10–11pt | 8pt caps, 0.08em |
| Print CV | same as web, single column | 10.5–11pt | 8pt caps |
