# Dialog

A modal on a paper-coloured scrim: `.h3-scrim` (`colour-page` at 75% + 3px backdrop blur — never a black overlay) under `.h3-dialog` (centred, `space-6` padding, 1px `colour-line` border, `radius-xl`, `colour-surface`, no shadow).

## Markup

```html
<div class="h3-scrim"></div>
<div class="h3-dialog" role="dialog" aria-modal="true" aria-labelledby="t">…</div>
```

In: fade + `scale(0.96→1)` over 200ms; out 140ms. A lightbox drops the panel entirely: the photo sits full screen on the scrim with `object-fit: contain`. The consumer supplies focus management and the close control (a `.h3-button`).

Source: `skills/h3nr7-design/assets/h3nr7.css` and `references/components.md` in h3nr7/h3nr7-design.
