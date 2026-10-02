# Person

A name block: a 4rem square avatar with `radius-lg` (the card's own corner, never a circle) beside the name and its captions.

## Markup

```html
<div class="h3-person">
  <span class="h3-person-avatar">HH<img src="portrait-600.jpg" alt=""></span>
  <div class="h3-person-detail">
    <span class="h3-person-name">Henry YP Ho</span>
    <span class="h3-person-title">Platform &amp; Product Engineer</span>
    <span class="h3-person-url">iam.h3nr7.com</span>
  </div>
</div>
```

The photo covers the initials ("HH"), which show if it fails. Name semibold ink; title and URL `colour-ink-muted`. Usually inside a `.h3-card`.

Source: `skills/h3nr7-design/assets/h3nr7.css` and `references/components.md` in h3nr7/h3nr7-design.
