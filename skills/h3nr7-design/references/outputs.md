# Outputs, medium by medium

The system is the same everywhere — ink and greys, Mrs Eaves italic with its ligatures on for
the voice, Inter for the rest, hairlines, generous asymmetric space. What changes is how the
fonts and assets get there. `assets/fonts/fonts.json` names the bundled faces ("Mrs Eaves OT"
Italic, Inter) and their files.

**Who receives it decides the format.** Mrs Eaves' own embedding permission (OS/2 `fsType` 4)
is *Preview & Print*: a PDF fits that; an HTML file carrying the whole font as WOFF2 does not.
So a self-contained HTML file is for Henry's own viewing and presenting; anything going to
other people goes as **PDF**. Never send or publish the font files themselves.

## Contents
HTML artifact · Standalone HTML · PDF · Slides (HTML, PowerPoint) · Word · Images (Pillow) ·
Charts and diagrams · Markdown, README, email

---

## HTML artifact (shown in the chat)

- Paste `assets/h3nr7.css` into one `<style>` (trim sections you do not use if size matters).
  Paste the contents of `assets/h3-scramble.js` into a `<script>` only if the page uses
  `data-scramble`.
- Never paste base64 fonts or images into an artifact — tens of thousands of tokens. The
  stack renders Mrs Eaves wherever it is installed (Henry's machine) and falls back to a system
  Baskerville elsewhere; tell Henry if the preview will not show the real face.
- Inline the mark as SVG markup (from `assets/logo/h3nr7-mark.svg`, ~4 KB) rather than an
  `<img>`, so it takes `currentColor` and inverts in dark mode.
- Start from a template's markup; keep its classes.

## Standalone HTML file

1. Write the page linking the skill's files by absolute path:
   `<link rel="stylesheet" href="<skill>/assets/h3nr7.css">`,
   `<script src="<skill>/assets/h3-scramble.js"></script>`, `<img src="<skill>/assets/logo/…">`.
2. Run `python <skill>/scripts/inline.py page.html`. It inlines CSS, JS and images and embeds
   every face in `fonts.json` as WOFF2. `--family Inter --family "Mrs Eaves OT"` limits the
   fonts; `--no-fonts` skips them.
3. The result is one file that renders identically anywhere — for Henry's own use. To give it
   to someone else, make the PDF below from it.

## PDF

Prefer HTML → PDF: write the page (templates print cleanly; `@media print` drops chrome and
animation and collapses page grids to one column), inline it, then print with a headless
Chromium if one is available (Playwright:
`page.pdf({ preferCSSPageSize: true, printBackground: true })`). Page size follows the
medium: documents and CVs A4 portrait with 18–25mm margins (`@page { size: A4; margin: 20mm }`);
slides use the template's own `@page { size: 1280px 720px }`, one slide per page; a social
card is an image, not a PDF. Then check the fonts (`pymupdf`: `page.get_fonts()`, or
`pdffonts`): Chrome embeds Mrs Eaves as unnamed **Type 3** outlines (the font program itself
is not embedded) beside a named `Inter-18pt` subset — that is correct. A *named* serif such as
`TimesNewRoman` or `Georgia` means the display face fell back: fix it before handing over.
If no browser exists, use ReportLab: register `MrsEavesOT-Italic.ttf` and the Inter TTFs from
`assets/fonts/` and apply the Word settings below — but ReportLab does not apply OpenType
ligatures, so say so, or prefer any route that goes through a browser.

## Slides

**HTML deck — the default** — `assets/templates/slides.html`: 1280×720 slides, one
`<section class="slide">` each; pins `data-theme="light"` so dark slides stay the accent;
zooms to fit narrow windows; **P** or **F** presents full screen (arrows, space, click; Esc
leaves); printing gives one slide per PDF page. Kinds: title, section, content, statement
(dark), image, close (dark, the white mark). Present from the inlined HTML; send the PDF.

**PowerPoint (python-pptx)** — only when a .pptx is explicitly needed. PowerPoint has no
switch for OpenType discretionary ligatures, so Mrs Eaves loses st/ct/sp/ee/ae there (standard
fi/ff may still form); tell Henry that, and offer the HTML/PDF deck instead.

| Setting | Value |
|---|---|
| Size | 13.333 × 7.5 in (16:9) |
| Background | `F6F6F7`; statement and closing slides `0E0E10` |
| Margins | 0.75 in top/bottom, 1 in left/right; everything left-aligned to the left margin |
| Statement / title | Mrs Eaves family from `fonts.json`, italic, regular, 44–54 pt, line spacing 0.95, `17171A` (or `F2F2F3` on dark) |
| Slide title | Mrs Eaves italic 32–40 pt |
| Label | Inter 11 pt, all caps (`font.all_caps`), character spacing +0.9 pt, `8A8B90` |
| Body | Inter 16–20 pt, `17171A`; secondary `595A5F` |
| Footer | the text wordmark "h3nr7" in Mrs Eaves italic 14 pt `595A5F` left, slide number Inter 10 pt `8A8B90` right |
| Rule | a 1 pt line shape in `17171A`, full content width |
| Logo | `assets/logo/h3nr7-mark-white.png` on the dark close slide, ~2.7 in tall, centred |

Turn off what PowerPoint adds by default: no shape fills, outlines or shadows
(`shape.shadow.inherit = False`, `line.fill.background()`), no theme colours, no gradients, no
transitions beyond none/fade, no bullets other than the brand marker or plain text. One idea per
slide. Henry has both fonts installed; for anyone else, export a PDF.

## Word documents (python-docx)

| Style | Setting |
|---|---|
| Page | A4, margins 22 mm; no headers/footers except a faint page number |
| Ligatures | **All**, on every Mrs Eaves run — Word's Font › Advanced › Ligatures. In python-docx, add `<w14:ligatures w14:val="all"/>` to the run's `rPr` (namespace `http://schemas.microsoft.com/office/word/2010/wordml`); set it in the Title and Heading 2 styles so every display run inherits it |
| Normal | Inter 10.5 pt, `17171A`, line spacing 1.3, 8 pt after |
| Title | Mrs Eaves italic 24 pt, `17171A`, 0 after; a standfirst paragraph in Inter 11 pt `595A5F` under it; date Inter 9 pt `8A8B90` |
| Rule after the masthead | an empty paragraph with a 1 pt bottom border in `17171A` (or `595A5F` for an article), 24 pt before, 32 pt after |
| Heading 1 (section label) | Inter 9 pt, all caps, character spacing +0.7 pt (`w:spacing w:val="14"`), `8A8B90`, 24 pt before, 8 pt after |
| Heading 2 (entry / subhead) | Mrs Eaves italic 15 pt, `17171A`, 16 pt before, 2 pt after |
| Metadata line (dates, keywords) | Inter 9 pt `8A8B90` |
| Quote | Inter italic 10.5 pt `595A5F`, left border 0.75 pt `E2E2E5`, 8 pt indent |
| Lists | flush left; marker "⁌" where the font has it, else an en dash; numbered lists keep numbers |
| Tables | no vertical lines; 0.5 pt `E2E2E5` horizontals; header row in the label style |
| Links | ink `17171A` with a plain underline — never Word's default blue |

Never: coloured headings, Word's default blue, bold display type, centred body text, shaded
boxes. A CV is `assets/templates/cv.html` turned into a PDF; build a .docx only when asked.

## Images (Pillow)

Load fonts from `assets/fonts/` — the Mrs Eaves italic file named in `fonts.json`, and
`Inter-Regular.ttf`, `Inter-SemiBold.ttf`. Paste logo PNGs with their alpha as the mask.

```python
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, features

skill = Path("<skill>")
fonts = skill / "assets/fonts"
faces = json.loads((fonts / "fonts.json").read_text())["faces"]
italic = next(f for f in faces if f["family"] != "Inter" and f["style"] == "italic" and f["weight"] == 400)
display = ImageFont.truetype(str(fonts / italic["desktop"]), 64)
body = ImageFont.truetype(str(fonts / "Inter-Regular.ttf"), 22)

card = Image.new("RGB", (1200, 630), "#f6f6f7")
d = ImageDraw.Draw(card)
d.rectangle([570, 0, 1200, 630], fill="#000000")
mark = Image.open(skill / "assets/logo/h3nr7-mark-white.png")
mark = mark.resize((328, round(mark.height * 328 / mark.width)))
card.paste(mark, (885 - 164, 315 - mark.height // 2), mark)
lig = {"features": ["liga", "dlig"]} if features.check("raqm") else {}  # ligatures need libraqm
d.text((64, 150), "WebGl terrain mesh", font=display, fill="#17171a", **lig)
d.text((64, 250), "Create terrain mesh from NASA satellite data", font=body, fill="#595a5f")
card.save("card.png")
```

Pillow only shapes OpenType features when it is built with libraqm (`features.check("raqm")`).
Without it Mrs Eaves' ligatures cannot show — and they always matter for display type — so
in that case render the card as HTML (`templates/social-card.html`) and screenshot it with a
headless browser, or tell Henry the image lacks them. Sizes: og/LinkedIn post 1200×630; square
1080×1080 (the dark tile is the default avatar); LinkedIn banner 1584×396; X header 1500×500;
YouTube banner 2560×1440 (keep text in the central 1546×423).

## Charts and diagrams

Monochrome, like everything else.

- Series: ink `#17171a` for the one that matters, then `#595a5f`, `#8a8b90`, `#c4c5c9`; four at
  most. Separate by grey *and* by form (solid/dashed line, filled/hollow mark) and label lines
  directly at their ends instead of using a legend.
- Axes and ticks Inter xs `#8a8b90`; gridlines `#e2e2e5`, horizontal only; no chart border, no
  background fill, no shadows, no 3D, no gradients.
- Title as a section label (Inter caps, tracked, faint); a one-line takeaway in Mrs Eaves
  italic above it if the chart needs a headline.
- Numbers in lining, tabular figures. Dark mode: swap to the dark ramp (`#f2f2f3`, `#a6a7ac`,
  `#6f7076`, `#2a2a2f`).
- Diagrams (SVG, Mermaid): white `#ffffff` nodes with a 1px `#17171a` or `#e2e2e5` stroke and
  4–8px radius on the `#f6f6f7` page; 1px ink connectors with open chevron arrowheads; labels
  Inter 13–14px; emphasis by filling one node ink with white text. Mermaid: `theme: 'base'`
  with `primaryColor #ffffff`, `primaryBorderColor #17171a`, `lineColor #17171a`,
  `primaryTextColor #17171a`, `fontFamily Inter`.

## Markdown, README, email

- Header image: `assets/logo/h3nr7-tile-dark.png` at 96–128px, or the text "h3nr7" alone.
- No emoji, no badges wall, no coloured shields. Headings in sentence case.
- Email signature: "Henry YP Ho · Platform & Product Engineer", then `h3nr7.com`, in the
  client's default sans in dark grey; optionally the 48px dark tile. No quotes, no banners.
