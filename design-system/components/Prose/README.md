# Prose

`.h3-prose` styles rich text written with bare tags — articles, write-ups, markdown output.

## What it does

- Paragraphs `0 0 space-4`, leading 1.5 (paragraph spacing, not loose leading, separates).
- `h1` display italic at name size; `h2` → SectionLabel; `h3` display italic `text-xl`, 1.15, `space-8 0 4px`; `h4` Inter base faint; `h5` Inter xs faint; `h6` display italic base, faint.
- Lists flush with the text, `⁌ ` markers inside, `space-2` between items; numbered lists keep decimals.
- Quotes: muted italic Inter, a 1px `colour-line` rule on the left, no quote marks.
- Images `radius-md`; captions xs faint. Links are ink with the sweep underline (see Link).

## Consumer provides

Semantic HTML inside a `.h3-prose` wrapper on a `measure` column. No inline colours, no bold display headings.

Source: `skills/h3nr7-design/assets/h3nr7.css` and `references/components.md` in h3nr7/h3nr7-design.
