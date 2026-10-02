# IconButton

A 1.75rem square around a 14–16px icon inside a card — link-outs and social marks. The mark never changes; the ground goes to `colour-hover`.

## Markup

```html
<div class="h3-social">
  <a class="h3-icon-button" href="https://github.com/h3nr7" aria-label="GitHub">…16px github icon…</a>
</div>
```

- `.h3-social` lays a row with a 4px gap and a `-0.375rem` start margin so the glyphs align optically with the text above.
- Icons always ink (inline SVG, `currentColor`), never platform colours. Platform names alone as accessible names ("GitHub").

Source: `skills/h3nr7-design/assets/h3nr7.css` and `references/components.md` in h3nr7/h3nr7-design.
