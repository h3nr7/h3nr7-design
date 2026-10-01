# Brand assets

## The mark

The stacked **h3r / n7** — "h3nr7" broken over two lines, set in Mrs Eaves OT **Bold Italic**,
the 3 and 7 as oldstyle figures that drop below the baseline, the 7 hanging furthest. Master:
`h3nr7-design.ai` (Illustrator, two 1080×1080 artboards, black-on-white and white-on-black),
kept beside the h3nr7 repos. Every file in `assets/logo/` is generated from it with the type
converted to outlines, so none of them needs the font.

| File | Size | Notes |
|---|---|---|
| `h3nr7-mark.svg` | 551×738 viewBox | Tight to the ink, `fill="currentColor"`. Inline it in HTML so it follows the theme. |
| `h3nr7-mark-black.svg` / `.png` | PNG 896×1200 | Transparent, `#000`. |
| `h3nr7-mark-white.svg` / `.png` | PNG 896×1200 | Transparent, `#fff`. |
| `h3nr7-tile-dark.svg` / `.png` | 1080² | White mark on `#000`, the master's margins. The avatar and social image. |
| `h3nr7-tile-dark-1280.png` | 1280² | The site's own copy (`bw@1x.png`): og:image, CV menu card. |
| `h3nr7-tile-light.svg` / `.png` | 1080² | Black on `#fff`. |
| `h3nr7-glyph.svg` / `.png` | 32 / 512 | The favicon: the bottom-right half of a square (a diagonal from bottom-left to top-right), `currentColor` / ink. |

Rules:

- The mark is artwork. Place the file; never retype it in a font, never redraw it, never
  rearrange the lines, never put "h3nr7" on one line in Bold Italic and call it the logo.
- Colour: black (or ink) on light grounds, white on dark. No greys, no colours, no gradients,
  no outlines, no shadows, no rotation, no distortion.
- Clear space: at least the width of the mark's "n" on every side. The tiles show the intended
  generosity — the mark fills ~51% of the width and ~68% of the height.
- Minimum size: about 48px (screen) or 12mm (print) tall. Smaller than that, use the glyph.
- On a photograph, only over a flat, quiet area with enough contrast; otherwise use a tile.
- Squares (avatars, app icons, social profile pictures, a closing slide) take the dark tile.

## The text wordmark

In running layouts the signature is not the mark but the name set as type: **h3nr7**,
lowercase, Mrs Eaves OT Italic, regular weight, ligatures on (`.h3-landing-name` on the home page, `.h3-wordmark`
muted above an article title). The CV host is **iam h3nr7**. Never capitalised ("H3NR7",
"H3nr7"), never spelled out ("Henry") in place of it, never tracked.

## The glyph

The diagonal half-square from the favicon (`#181a19`, effectively ink) — the one survivor of
the v3 identity. For favicons and anything at or below 32px. Not a bullet, not a divider.

## Portrait

`assets/images/portrait-600.jpg` (what the site serves) and `portrait-1200.jpg` (the original):
Henry, head and shoulders, black crew-neck, flat light-grey background. Square crop, shown at
64px in the contact card and 110px on the CV wordmark's hover card, 8px radius — the card's
own corner, never a circle. Only where the context is Henry himself (contact, bio, CV,
speaker slide). No filters, no duotone, no cut-outs, never as a background texture. Initials
**HH** sit under it as the fallback.

## Icons

`assets/icons/`, all `currentColor`, viewBox 24:

- Brand marks, filled, shown at 16px: `x`, `github`, `linkedin`, `youtube`, `instagram`.
- UI marks, 2px round stroke, shown at 14px: `arrow-left`, `arrow-right`, `external-link`
  (leaves the site), `link` (the other half of the same site), `chat` (book a meeting),
  `printer`.
- `sound-on`, `sound-off`: 1.6px stroke, filled cone, 16–20px.

Always ink, never each platform's colour — five logos in five colours is a row of stickers.
`aria-hidden` on the SVG; the control carries the name. No icon packs, no emoji.

## The backdrop

Behind h3nr7.com sits a WebGL scene drawn in `--colour-ink` (`@h3nr7/canvas`): on the home page
"blobby", a soft-edged black blob that slowly morphs and can carry a photograph or video
inside it; on articles a field of fine perspective lines like a wireframe seen from low down.
It is decoration with a static fallback. In other media, evoke it with `.h3-gridfield`
(the same grid seen head-on) or leave it out — never imitate it with gradients, glows or
blurred colour.

## Reference screenshots

`assets/reference/`, taken from the local v4 site:

| File | Shows |
|---|---|
| `billboard-rest-light.jpg`, `-dark.jpg` | The home page at rest: name, then every title blurred into one statement. |
| `billboard-hover-light.jpg` | One title sharp under the pointer, the hover card with its square corner at the cursor. |
| `billboard-mobile-light.jpg` | The same at 390px. |
| `article-light.jpg` (full page), `article-dark.jpg` | Masthead, soft rule, hero, labels, 3+3 columns, lists, the line-field backdrop. |
| `contact-panel-light.png`, `-dark.png` | The panel: two cards, person block, card rule, social marks, chrome buttons. |
| `ligatures.png` | Mrs Eaves OT Italic with ligatures on (the brand), off, and broken by 0.02em tracking. |

## Retired — do not use

From the v3 site in `legacy/`: Akkurat, Akkurat Mono, Rift and Roboto (commercial or off-brand);
the pastel "Artboard" infographics (`#e4f5fc`, `#fad7e7`, `#f0f5d8`, cyan `#00aeef`, magenta
`#ec008c`, green `#39b54a`, Myriad Pro); the 200px diagonal `logo-200x200.jpg` (the glyph
replaces it).
