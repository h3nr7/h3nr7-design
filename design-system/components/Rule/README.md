# Rule

A 1px line that draws itself on from the left: it closes an introduction and opens the record.

## Variants

- `<span class="h3-rule" role="presentation"></span>` — ink, `scaleX(0→1)` over 1000ms `--ease-out` after a 1000ms delay. Margins asymmetric: `space-12` above, `space-16` below.
- `.h3-rule-soft` — `colour-ink-muted`, under an article masthead (a black bar would compete with the title).
- `.h3-rule-close` — sits down on a footer: `space-12` above, `space-6` below, 2000ms delay.
- `.h3-card-rule` — the quick version inside a panel card: 420ms after 160ms, margin `space-3 0`.

## Rules

An element, not a `border` — borders cannot sweep. Ink (or muted), never `colour-line`: a line that draws attention to its own arrival and then turns out pale reads as a mistake. Under reduced motion it is simply there.

Source: `skills/h3nr7-design/assets/h3nr7.css` and `references/components.md` in h3nr7/h3nr7-design.
