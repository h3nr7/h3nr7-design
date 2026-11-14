---
name: h3nr7-logo
description: How Henry YP Ho's stacked h3nr7 logo mark is built from type, so it can be drawn in code at any size or colour instead of relying on the SVG. Use when Henry wants the h3nr7 mark generated or redrawn in SVG, canvas, a script, a PDF or an image, asks how the logo is constructed or aligned, or wants a variant of it. For the finished logo files, tiles, colours and general brand rules use h3nr7-design.
---

# h3nr7 logo: building the mark from type

The mark is **five lowercase glyphs set in Mrs Eaves OT Bold Italic**: `h 3 r` on the top row, `n 7` on the
row below, at one font size, placed by hand so the two rows lock together. There is no drawing
behind it beyond that placement, which means it can be rebuilt exactly from the font plus the
numbers below.

The finished files (`h3nr7-mark.svg`, `-black`, `-white`, the tiles, the favicon glyph) live in the
**h3nr7-design** skill (its logo folder); copies of the three mark SVGs sit in `assets/` here as
the fallback. Prefer those whenever an SVG will do. Build from type only when the mark has to be
generated: another size, colour or format drawn by code, a variant, or a check against the original.

## The one thing to know first: the font

The mark uses **Mrs Eaves OT Bold Italic**. That file is **not bundled** with h3nr7-design, which carries
only the regular Italic, and the site's Adobe kit serves only the italic 400. The regular Italic cannot
stand in: its outlines are narrower (the `h` is 0.07 em narrower) and adding a stroke or faux bold only
reaches about 0.73 overlap with the real mark in a pixel comparison. Faux bold from the browser is no
better. So:

| You have | Do this |
|---|---|
| The Bold Italic file | Build outlines with `scripts/build_mark.py`, or load it with `@font-face` (weight 700, italic) and use live text. |
| No Bold Italic file | Use the SVGs in `assets/`. Do not approximate the mark with the regular Italic, and say why. |

Mrs Eaves is a licensed Emigre face: build outlines into a logo file, and never publish or send the font
file itself.

## The layout

Origin is the baseline start of the `h`; units are **em of the font size**; y points down. The
machine-readable copy is `assets/mark-layout.json`.

| Glyph | Row | x (em) | y (em) | Note |
|---|---|---|---|---|
| `h` | 1 | 0 | 0 | the origin |
| `3` | 1 | 0.380 | 0 | old-style figure, descends 0.187 below its baseline |
| `r` | 1 | 0.824 | 0 | |
| `n` | 2 | 0.099 | 0.608 | row 2 starts 0.099 right of the `h` and 0.608 below |
| `7` | 2 | 0.541 | 0.713 | 0.105 below the `n`'s baseline; old-style, descends 0.196 |

Ink box (what the viewBox hugs): x 0.028, y -0.6172, width 1.1391, height 1.5262. At the shipped
size (483.2744) that gives the shipped `viewBox="271.50 203.00 550.75 737.75"` to within a quarter of a
unit.

What the numbers mean:

- **Rows overlap.** Row 2 sits 0.608 em below row 1, less than one em. The `7`'s top (0.511 above its
  baseline) lands 0.202 em below the top row's baseline, about 0.016 em under the bottom of the `3`.
  That near-touch is the lock-up; keep it when scaling and do not add spacing.
- **The `7` is dropped.** It sits 0.105 em lower than the `n`, so the pair does not share a baseline.
- **Plain digits.** `3` and `7` are the font's default old-style figures. Do not turn on lining figures
  (`lnum`), ligatures or discretionary ligatures, and set kerning off: each glyph is placed alone.
- **Offsets are measured, not typed.** They were read from the shipped SVG, so reproduce them as given
  rather than recomputing from advance widths.

## Build it

### Outlines (a logo file that needs no font)

```
pip install fonttools
python scripts/build_mark.py --font MrsEavesOT-BoldItalic.otf --size 100 --color "#17171a" --out mark.svg
python scripts/build_mark.py --font MrsEavesOT-BoldItalic.otf --check
```

`--check` compares each glyph's outline box with the one recorded from the shipped mark and exits non-zero
if a glyph or weight is wrong. Run it first with any font you are unsure of. (The regular Italic fails it by
0.014 to 0.056 em per glyph, which is the point.) `--color currentColor` is the default so the mark follows
the text colour.

### Live text in a page

Load the Bold Italic yourself, then place five `<text>` elements. `scripts/build_mark.py --text --size 100`
writes this; it needs no fontTools:

```html
<svg viewBox="2.8 -61.72 113.91 152.62" role="img" aria-label="h3nr7" fill="currentColor"
     font-family="'Mrs Eaves OT'" font-style="italic" font-weight="700" font-size="100"
     style="font-synthesis:none;font-kerning:none;font-variant-ligatures:none">
  <text x="0"    y="0">h</text>
  <text x="38"   y="0">3</text>
  <text x="82.4" y="0">r</text>
  <text x="9.9"  y="60.8">n</text>
  <text x="54.1" y="71.3">7</text>
</svg>
```

`font-synthesis:none` matters: if the page has only the regular Italic, the browser would otherwise fake a
bold and the mark would look wrong without any error.

### In JavaScript

```js
// Rebuilds the mark at any size. Needs Mrs Eaves OT Bold Italic loaded as weight 700, italic.
function h3nr7Mark(size = 100, fill = 'currentColor') {
  const glyphs = [['h', 0, 0], ['3', 0.38, 0], ['r', 0.824, 0], ['n', 0.099, 0.608], ['7', 0.541, 0.713]];
  const u = (v) => +(v * size).toFixed(2);
  const view = [0.028, -0.61719, 1.13911, 1.52615].map(u).join(' ');
  const text = glyphs.map(([c, x, y]) => `<text x="${u(x)}" y="${u(y)}">${c}</text>`).join('');
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${view}" role="img" aria-label="h3nr7" fill="${fill}"` +
    ` font-family="'Mrs Eaves OT'" font-style="italic" font-weight="700" font-size="${size}"` +
    ` style="font-synthesis:none;font-kerning:none;font-variant-ligatures:none">${text}</svg>`;
}
```

For canvas, call `ctx.font = 'italic 700 ' + size + 'px "Mrs Eaves OT"'` and `ctx.fillText(c, x * size, y * size)` for
each row of the table, with `ctx.textBaseline = 'alphabetic'`.

## Rules

- Same colours as the finished marks: ink `#17171a`, black, white, or `currentColor`. Never a gradient,
  outline, shadow or tint.
- Same clear space as h3nr7-design says: at least the width of the `n` on every side. Below about 48px
  tall, use the favicon glyph in h3nr7-design instead.
- In running headers the signature is the text wordmark (`h3nr7` in display italic, linked to
  h3nr7.com), not this stacked mark. See h3nr7-design.
- If a rebuilt mark and `assets/h3nr7-mark.svg` disagree by more than a pixel at 200px tall, the font or
  the layout is wrong. Trust the SVG and re-check.

## Not verified here

`scripts/build_mark.py` and `assets/mark-layout.json` were built against the shipped SVG and tested
for the regular Italic (which they correctly reject) and for the live-text output. They have **not** been run
against the real Mrs Eaves OT Bold Italic file, which was not available. The first run with it should be
`--check`, then a visual comparison with `assets/h3nr7-mark-black.svg`.
