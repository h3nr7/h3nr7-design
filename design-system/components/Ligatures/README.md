# Ligatures

A specimen of the display face's ligatures: Mrs Eaves OT Italic with `liga`, `dlig` and `calt` on (the brand), off, and broken by tracking. Use it to check that a surface is really showing Mrs Eaves with its ligatures.

## The rule

Display text always carries `font-variant-ligatures: common-ligatures discretionary-ligatures contextual`. Every display class in `components/bundle.css` (`h1`–`h4`, `.h3-display`, `.h3-landing-name`, `.h3-landing-lede`, `.h3-wordmark`, `.h3-monogram`) sets it; text set in the `display` family any other way must add it by hand, or only fi ff fl appear.

- `liga`: ff fi fl fb fh fj fr ft · ffi ffl ffb ffh ffj ffr fft
- `dlig`: ae ct ee fy gg gi gy ip it ky oe py sp st tt tw ty · cky ggy tty ffy · capitals AA AV FF FI FL HE LA … Th THE
- Any non-zero `letter-spacing` switches the optional ligatures off; so does a `font` shorthand placed after the ligature rule.

## Consumer provides

Nothing: `<p class="h3-display">…</p>` is enough. The status line in the preview says whether the Mrs Eaves file loaded; if it did not, the serif shown is a fallback and has none of these ligatures.

Source: `skills/h3nr7-design/references/typography.md` and `assets/reference/ligatures.png` in h3nr7/h3nr7-design.
