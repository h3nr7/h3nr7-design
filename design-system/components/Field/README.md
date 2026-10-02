# Field

A labelled input: `.h3-field` (grid, 4px gap, max `measure-form`) → `label`, `input`, `.h3-field-hint`, `.h3-field-error`.

## Markup

```html
<div class="h3-field">
  <label for="pp">Passphrase</label>
  <input id="pp" placeholder="three words">
  <p class="h3-field-hint">It is in the email that sent you here.</p>
</div>
```

- Input: padding `space-2 space-3`, 1px `colour-line` border, `radius-md`, `colour-page` ground; keeps the 2px `colour-focus` ring, offset 2px.
- Hint: `colour-ink-faint`, `text-sm`. Error (`.h3-field-error`): **ink** `text-sm` — said plainly, never coloured red.

Source: `skills/h3nr7-design/assets/h3nr7.css` and `references/components.md` in h3nr7/h3nr7-design.
