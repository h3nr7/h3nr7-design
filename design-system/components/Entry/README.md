# Entry

A CV or record entry: a display-italic title, a faint period, a line of remit, outcomes and a keyword run.

## Markup

```html
<article class="h3-entry">
  <h3>[Role] — [Company]</h3>
  <p class="h3-period">[Jan 2024] — Present</p>
  <p>One line on the remit.</p>
  <ul class="h3-points"><li>Outcome, with the number.</li></ul>
  <p class="h3-keywords">TypeScript · React · WebGPU</p>
</article>
<div class="h3-entry"><h3>Frontend</h3><ul class="h3-skills"><li>React</li><li>Three.js</li></ul></div>
```

- Entries are `space-12` apart — the gap between entries must beat the gap inside one.
- Title `text-xl` display italic, leading 1.15; the period closes up under it and pushes the description `space-4` away.
- `.h3-skills` joins its items with " · ". Every entry title in every section (roles, skill groups, qualifications, referees) is display italic — one document, not two. Entry titles are never links.

## Consumer provides

Role — Company (em dash with spaces), period, one remit line, outcomes not duties, a middot-separated keyword run.

Source: `skills/h3nr7-design/assets/h3nr7.css` and `references/components.md` in h3nr7/h3nr7-design.
