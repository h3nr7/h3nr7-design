# Link

The in-text link: two hairlines painted as backgrounds — a full-width `colour-line` rail at rest and an ink line that grows 0→100% from the left over 200ms on hover or focus.

## Use

- `.h3-link`, or any `a` inside `.h3-prose`, `.h3-landing-links`, `.h3-footer`.
- `padding-bottom: 2px` keeps the line clear of descenders; `box-decoration-break: clone` underlines every line of a wrapped link.
- Colour by context: ink in prose; muted → ink on landing links; ink inside a faint footer.
- `.h3-hollow` (opt-in, display-size text that opens elsewhere): hover drains the fill and leaves a 0.6px ink contour. Large type only; never on links with an icon.

## Consumer provides

A link that is a word in the sentence ("Drop me an **email**"), not "click here". Accessible names say where it goes.

Source: `skills/h3nr7-design/assets/h3nr7.css` and `references/components.md` in h3nr7/h3nr7-design.
