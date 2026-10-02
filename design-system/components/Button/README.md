# Button

Quiet chrome: a 28px control on `colour-surface` with ink text; only the ground moves on hover (`colour-hover`), and the pressed state comes from ARIA.

## Markup

```html
<button class="h3-button" type="button">Contact</button>
<button class="h3-button" type="button" aria-pressed="true">Pressed</button>
<button class="h3-button h3-button-square" type="button" aria-label="Back">…14px icon…</button>
```

- `min-height: 1.75rem`, padding `2px space-2`, `radius-md`, Inter `text-xs` medium, `line-height: 1`.
- `aria-pressed="true"` / `aria-expanded="true"` → `colour-accent` ground, `colour-accent-ink` text (state read from ARIA, not a class).
- `.h3-button-square` — icon-only, 1.75rem square, padding 2px; the button carries the accessible name.

## Rules

No pill shapes, no outline buttons, no icon + label buttons in prose, no movement on hover. 28px is below the 44px touch target — fine for chrome; for a primary action use Cta.

Source: `skills/h3nr7-design/assets/h3nr7.css` and `references/components.md` in h3nr7/h3nr7-design.
