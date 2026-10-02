# Gallery

Square tiles in a grid: `.h3-gallery` with `--cols: 1|2|3`, `space-4` gap, `radius-md`, `object-fit: cover`. Under the pointer a tile drains to `grayscale(1)` over 450ms.

## Markup

```html
<ul class="h3-gallery" style="--cols:3"><li><img src="…" alt="…"></li>…</ul>
<button class="h3-button" type="button">Show more (4)</button>
```

A single image is not cropped. No "Gallery" heading on screen — the name goes to the screen reader. Empty slots use Gridfield.

Source: `skills/h3nr7-design/assets/h3nr7.css` and `references/components.md` in h3nr7/h3nr7-design.
