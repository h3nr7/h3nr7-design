# Columns

The page column and its six-track grid: `.h3-page` holds running text on `measure` (68ch); `.h3-page-wide` + `.h3-cols` lays out two columns from `breakpoint-md` (48rem).

## Use

- `.h3-page` — reading column: `max-width: var(--measure)`, centred, padding `space-12 space-4 space-24`. Articles, documents, the CV on a phone.
- `.h3-page.h3-page-wide` — from 48rem widens to `measure-page` (64rem, 76rem at 96rem, 94rem at 120rem).
- `.h3-cols` with children `.h3-span-2|3|4|6` — six tracks, `space-12` gutter, `align-items: start`. Below 48rem they stack with a `space-8` seam.
- **4 + 2** when the left is a record and the right a short index (CV: experience | skills, education). **3 + 3** when both hold the same kind of thing.

## Consumer provides

The column children, in reading order. Never reorder the DOM for the grid — the order is the same at every width.

Source: `skills/h3nr7-design/assets/h3nr7.css` and `references/components.md` in h3nr7/h3nr7-design.
