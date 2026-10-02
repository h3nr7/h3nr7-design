# HoverCard

A picture that follows the pointer over a title: 1px ink border, ink ground, radius `radius-xl` on three corners and **square on the corner that touches the cursor** — the point of contact.

## Markup

`<span class="h3-hovercard"><img src="…" alt="…" width="220"></span>` — `data-flip-x` / `data-flip-y` move the square corner when the card flips near an edge.

It starts as a 75px placeholder square and grows to the image's ratio in 260ms `cubic-bezier(0.2, 0, 0, 1)`. Static use (a thumbnail beside a title) keeps the shape. Pointer tracking is the consumer's script.

Source: `skills/h3nr7-design/assets/h3nr7.css` and `references/components.md` in h3nr7/h3nr7-design.
