h3nr7 is Henry YP Ho's site and identity — "a techie journal of tinkering things". It should look like a well-set page, not an app: black ink on off-white paper, one literary serif italic for the voice, one neutral sans for everything practical, hairlines where other systems use boxes, and motion that behaves like a gesture rather than decoration.

## The essentials

1. **Monochrome, always.** `colour-ink` on `colour-page`, raised planes in `colour-surface`, and the greys `colour-ink-muted`, `colour-ink-faint`, `colour-line`, `colour-hover`. There is no accent hue and no brand blue: `colour-accent` *is* ink. Photographs are the only source of colour. Dark mode is a full inversion — every colour is a role token that flips, so never hard-code a hex.
2. **Two faces, two jobs.** `display` (Mrs Eaves OT Italic) for the name, titles, statements and entry headings. `body` (Inter) for prose and *all* UI — buttons, labels, captions, navigation.
3. **Hairlines, not boxes.** 1px rules and borders, flat surfaces, no `box-shadow` anywhere. Radii double: `radius-md` controls, `radius-lg` cards and avatars, `radius-xl` panels and dialogs.
4. **Space on a 4px scale, text on a measure.** Running text sits on `measure` (68ch). Wider layouts use a 6-track grid with a `space-12` gutter, split 4+2 (a record beside an index) or 3+3 (two of the same kind). Left-aligned, ragged right. Air is asymmetric: more below a rule than above it.
5. **Quiet motion.** Only the ground changes on hover — labels never fade or shift. Rules sweep in left to right; links grow an ink underline over a grey rail; titles can rest blurred and sharpen under the pointer. Everything has a `prefers-reduced-motion` answer.

## Colour

- Text is `colour-ink` on `colour-page` or `colour-surface`. Secondary lines (standfirst, role, quotes) are `colour-ink-muted`.
- `colour-ink-faint` is for metadata only — labels, dates, captions, keywords, one closing footer line. It is 3.2:1 on the light page and 3.9:1 on the dark one: below AA for body copy, so never use it for sentences a reader must read.
- `colour-line` is for borders nobody should notice and the link rail. It is decorative (1.2–1.35:1); a control needs its focus ring or its ground, not the line, to be found.
- The filled state — the one CTA, a pressed or expanded button — is `colour-accent` with `colour-accent-ink` text.
- Focus is `colour-focus`: 2px solid, offset 2px. It follows ink.
- Charts and diagrams use the grey ramp `chart-1` … `chart-4`, plus direct labels; never hues.
- Fixed values that never flip: `gridfield`, `gridfield-line`, `monogram` (the image placeholder) and `logo-black`, `logo-white`.
- Modal scrim: `color-mix(in srgb, var(--colour-page) 75%, transparent)` with `backdrop-filter: blur(3px)` — a wash toward the paper, never a black overlay.

## Type

- Set the name, titles, statements and entry titles in `display` italic, regular weight. Use the `statement`, `name` and `entry-title` styles.
- **Ligatures on, always.** Display text gets `font-variant-ligatures: common-ligatures discretionary-ligatures contextual`. In this italic that fuses fi ff fl ft fr ffi ffl (liga) and st ct sp ee ae oe it tt ty tw ky gi gy py Th THE TT AV and more (dlig). "coffee", "aesthetic", "street", "act" must show them — compare `assets/Reference/ligatures.png`.
- **Never letter-space the display face.** Any tracking, even 0.005em, switches the ligatures off. No `font` shorthand on display type either (it resets them). Prefer `font-variant-*` over `font-feature-settings`.
- **Italic only, never bold, never roman, no small caps.** Emphasis comes from size and colour.
- Section labels are `label`: Inter, UPPERCASE from CSS, tracked 0.08em, `colour-ink-faint`. The label is the smallest thing in its section and the entry title under it the largest — that inverted hierarchy is deliberate. Never set a label in Mrs Eaves.
- Mrs Eaves has a small x-height: set it a step larger than Inter to look the same size (entry titles are `text-xl` over `text-base` body).
- Figures are oldstyle in the display face; add `font-variant-numeric: lining-nums` for tables, monograms and numbers against capitals.
- Sentence case for everything a person reads; uppercase comes only from CSS on labels.
- Bulleted lists use the `⁌ ` marker (U+204C), inside, flush with the text. Em dash with spaces for role and company ("Engineer — Company"); middot with spaces for a run ("React · WebGL · AWS").

**Fonts.** Both faces are carried here: Mrs Eaves OT Italic (the one cut in use, as a WOFF2 with its CFF table repaired so browsers accept it) and Inter (OFL) at the site's 18pt optical size in Regular, SemiBold and Italic. Mrs Eaves is a licensed Emigre face whose embedding permission is *Preview & Print*: use it to preview and to make Henry's own documents, never send or republish the font file, and send anything going to other people as PDF. If a surface cannot load it, the `display` stack falls back to Baskerville / Times italic — say so, and never present the fallback as the brand.

## Space, layout, radius

- Spacing is `space-1` … `space-24` (4, 8, 12, 16, 24, 32, 48, 64, 96px). There is no 5, 7 or 10.
- Reading column: `.h3-page` — `measure` wide, centred, padding `space-12 space-4 space-24`.
- From `breakpoint-md` (48rem): `.h3-cols` with `.h3-span-{2,3,4,6}` — six tracks, `space-12` gutter. 4+2 for a record and its index, 3+3 for two of a kind. Never reorder the DOM for the grid.
- Page widths step at `breakpoint-2xl` and `breakpoint-3xl` (`measure-page` 64 → 76 → 94rem; `measure-landing` always 4rem narrower). Nothing is fluid between them except `text-landing` and `text-landing-name`.
- Radii: `radius-md` controls, inputs, images; `radius-lg` cards, the avatar square; `radius-xl` panels, dialogs, the hover card.

## Motion

One direction — left to right, the way the words are read — and one rule: the ground moves, the content does not. Ground changes 120ms; link underline sweep 200ms `cubic-bezier(0.16, 1, 0.3, 1)`; the rule draws on over 1000ms after a 1000ms delay. Under reduced motion everything clamps, infinite loops become still, and anything whose resting state is hidden is shown whole. Full table in the Motion section.

## Logo and imagery

- The mark is the stacked **h3r / n7** in Mrs Eaves Bold Italic, outlined. Place the files in `assets/Logos/`; never retype, redraw, stretch, rotate, outline, shadow or recolour it beyond black/ink and white.
- In running headers the signature is the **text wordmark** — `h3nr7`, lowercase, display italic (`.h3-wordmark`, `.h3-landing-name`) — not the stacked mark. Never "H3NR7" or "H3nr7".
- Squares (avatar, social card, og:image, closing slide) take `h3nr7-tile-dark`. Below ~48px tall use `h3nr7-glyph`.
- Clear space: at least the width of the mark's "n" on every side.
- The portrait (`assets/Images/`) only where the context is Henry himself: square, `radius-lg`, never a circle, initials "HH" as the fallback.
- No stock imagery. An empty image slot is `.h3-gridfield` with the piece's initials — the WebGL wireframe seen head-on.

## Iconography

The site's own icons, in `assets/Icons/`, all `currentColor` on a 24 viewBox: filled brand marks (x, github, linkedin, youtube, instagram) at 16px; stroked UI marks (arrows, external-link, link, chat, printer) at 14px with a 2px round stroke; sound-on/off at 16–20px. Always ink, never the platforms' brand colours. `aria-hidden` on the SVG; the control carries the name. No icon packs, no emoji.

## Voice

First person, plain and a little dry; British spelling; en-GB dates ("1 October 2026"). Controls name what they do in the fewest words ("Back to home", "Print this CV", "Show more (4)"). Friendly closers rather than calls to action: "Let's have a chat", "Otherwise I am always up for a coffee and/or a chat." Errors own up lightly: "Oops! Looks like the feed is unavailable right now." No exclamation marks except that "Oops!". Never "Get started", "Unlock", "Supercharge".

## What it is not

Anything that would look at home on a SaaS landing page: gradients, drop shadows, glass, coloured accents, pill buttons, circular avatars, emoji as icons, icon fonts, stock photos, centred body text, bold or all-caps serif headings, tracked serif, card grids with borders and shadows, hero banners with a button stack. When unsure, take something away.

## Using this system

- The components are HTML + CSS: `components/bundle.css` is the site's portable stylesheet (`h3nr7.css`) verbatim — tokens, base type, a reset and every `h3-` class. There is no JavaScript component library; each component's README gives its markup. `components/bundle.js` only carries the split-flap script (`h3-scramble.js`) so `data-scramble` works wherever the bundle is loaded.
- `templates/` holds the source's starting points — `page.html`, `cv.html`, `landing.html`, `slides.html`, `social-card.html` — and `h3-scramble.js`, the vanilla split-flap roll for `data-scramble`. The templates link `../h3nr7.css`; here that file is `components/bundle.css`.
- Check every output in light and dark (`data-theme="dark"` on `<html>`), at 390px wide, and with reduced motion. Nothing should scroll sideways.

## Not synced

From `h3nr7/h3nr7-design` at `main@795edce`: the `.ttf` desktop copies of Mrs Eaves and Inter (the `.woff2` files are here, with `licenses/OFL-Inter.txt`); `specimen.html`, `scripts/inline.py` and the repo's build scripts. Motion durations and easings live in prose, not tokens. Components are the stylesheet's `h3-` classes with static HTML previews — no React bundle exists to build.
