# Icons

The site's own icons, 24 viewBox, all single-ink `currentColor` — as `<img>` they draw black, so inline the SVG to take `colour-ink` and flip with the theme.

- Brand marks, filled, shown at 16px: `x`, `github`, `linkedin`, `youtube`, `instagram`.
- UI marks, 2px round stroke, shown at 14px: `arrow-left` (back), `arrow-right`, `external-link` (leaves the site), `link` (the other half of the same site), `chat` (book a meeting), `printer`.
- `sound-on`, `sound-off`: 1.6px stroke with a filled cone, 16–20px.

Always ink, never each platform's brand colour. `aria-hidden` on the SVG; the control (`.h3-icon-button`, `.h3-button-square`) carries the accessible name. No icon packs, no emoji.
