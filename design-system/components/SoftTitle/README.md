# SoftTitle

Titles that rest blurred and sharpen under the pointer, with the split-flap roll: `.h3-soft` (rest `blur(3.8px)` + `opacity .55`, sharp in 184ms, back in 230ms) and `data-scramble` (`templates/h3-scramble.js`).

## Use

- `.h3-soft` inside a link; `data-breathe` adds a slow 5.2s blur "breath". Only under `(hover: hover)` — on touch it renders plain.
- `data-scramble` — on hover or focus each character rolls through A–Z a–z 0–9 and lands on itself, 26ms stagger, 460ms each (0.6× on leave); ligature pairs roll as one cell; widths are pinned so the line never jitters. Movement only, no colour change.
- For a run of titles that should invite pointing (the landing, the wordmark, display headings) — never body text or anything a phone reader needs. Off under reduced motion.

## Consumer provides

The titles and links, and the script (inline `templates/h3-scramble.js`; vanilla, no dependencies).

Source: `skills/h3nr7-design/assets/h3nr7.css` and `references/components.md` in h3nr7/h3nr7-design.
