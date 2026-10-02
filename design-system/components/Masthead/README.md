# Masthead

The top of an article or document: the muted text wordmark, the title in display italic at the same size, a standfirst and a date, closed by a soft rule.

## Markup

```html
<header class="h3-masthead">
  <p class="h3-wordmark"><a href="/">h3nr7</a></p>
  <h1>WebGl terrain mesh</h1>
  <p class="h3-standfirst">Create terrain mesh from NASA satellite data</p>
  <p class="h3-date">18 May 2020</p>
</header>
<span class="h3-rule h3-rule-soft" role="presentation"></span>
```

- Wordmark and title are the same size (`text-landing-name`); colour alone separates them — wordmark `colour-ink-muted` (the site, not the piece), title `colour-ink`. `space-6` from wordmark down to title.
- Standfirst sits 4px under the title (`colour-ink-muted`, base); the date closes up under it (`colour-ink-faint`, xs).
- On a CV the `h1` *is* the wordmark ("iam h3nr7", ink), followed by "Name · Title" and a contact row.

## Consumer provides

Title, one-line standfirst, an en-GB date ("1 October 2026"). Sentence case; no tracking on the title.

Source: `skills/h3nr7-design/assets/h3nr7.css` and `references/components.md` in h3nr7/h3nr7-design.
