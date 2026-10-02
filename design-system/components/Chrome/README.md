# Chrome

The only thing that floats: `.h3-chrome`, a fixed row top-right (`space-4` in, safe-area aware), 4px gap, `z-chrome`.

## Markup

```html
<nav class="h3-chrome" aria-label="Site">
  <a class="h3-button h3-button-square" href="/" aria-label="Back">…arrow-left…</a>
  <button class="h3-button" type="button" aria-expanded="false">Contact</button>
  <button class="h3-button h3-button-square" type="button" aria-pressed="false" aria-label="Sound">…sound-off…</button>
</nav>
```

Back arrow, "Contact" (opens the Panel; `aria-expanded` fills it), sound toggle. Nothing else floats. Chrome is Inter, never the display face. Hidden in print.

Source: `skills/h3nr7-design/assets/h3nr7.css` and `references/components.md` in h3nr7/h3nr7-design.
