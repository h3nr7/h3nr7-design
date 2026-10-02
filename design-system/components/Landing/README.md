# Landing

The billboard home page: the name in display italic, then every recent title run together as one statement, then a row of plain links.

## Markup

```html
<main class="h3-home">
  <header class="h3-landing">
    <h1 class="h3-landing-name"><span data-scramble>h3nr7</span></h1>
    <div class="h3-landing-lede">
      <ol class="h3-run" aria-label="Recent work">
        <li><a href="…"><span class="h3-soft" data-breathe data-scramble>WebGl terrain mesh</span></a><span class="h3-run-stop">.</span> </li>
      </ol>
    </div>
    <nav class="h3-landing-links" aria-label="Elsewhere"><a href="…">Articles</a><a href="…">GitHub</a></nav>
  </header>
</main>
```

- `.h3-landing-name` — `text-landing-name` (24→32px), leading 0.95, ink.
- `.h3-landing-lede` — `text-landing` (48→64px), leading 0.95, `text-wrap: pretty`. A list of titles set as one sentence: a full stop and a space between them (`.h3-run`, `.h3-run-stop`).
- `.h3-landing-links` — Inter, uppercase, 0.08em, `text-sm`; `colour-ink-muted` → ink on hover with the underline sweep; `space-6` apart, `space-12` above.
- The block is `measure-landing` wide, centred on itself.

## Consumer provides

The titles and their links; optional `data-scramble` (needs `templates/h3-scramble.js`) and `.h3-soft` (see SoftTitle). Do not add a hero image, a button stack or a tagline above the name.

Source: `skills/h3nr7-design/assets/h3nr7.css` and `references/components.md` in h3nr7/h3nr7-design.
