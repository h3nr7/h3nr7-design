# Panel

The contact panel: a stack of cards with no ground of its own — the cards are the surfaces, separated by a 4px gap rather than a divider because they are unrelated offers.

## Markup

```html
<div class="h3-panel">
  <div class="h3-card h3-card-row">
    <span class="h3-card-title">Let's have a chat</span>
    <a class="h3-icon-button" href="…" aria-label="Book a meeting — opens the booking page">…chat…</a>
  </div>
  <div class="h3-card">…Person…<span class="h3-card-rule"></span><div class="h3-social">…</div></div>
</div>
```

- `.h3-card` — `space-3` padding, `radius-lg`, `colour-surface`, `text-sm`; no border, no shadow.
- `.h3-panel` — 20rem wide, anchored under the "Contact" button; scales in from 0.96 and −0.25rem in 160ms, out in 120ms.
- `.h3-card-rule` — the quick ink rule inside a card.

## Consumer provides

The cards' content. A card grid with borders and shadows is not this.

Source: `skills/h3nr7-design/assets/h3nr7.css` and `references/components.md` in h3nr7/h3nr7-design.
