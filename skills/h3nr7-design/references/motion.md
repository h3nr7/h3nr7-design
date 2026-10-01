# Motion

Motion on h3nr7 is a gesture the page makes, not decoration on top of it. One direction
runs through all of it — **left to right, the way the words are read** — and one rule: the
ground moves, the content does not (no lifts, slides or scale on hover).

| Effect | Spec | Where |
|---|---|---|
| Ground change | `background-color` 120ms ease | Buttons, icon buttons, cards' controls |
| Underline sweep | `background-size` 0→100% of an ink 1px line over a grey rail, 200ms `--ease-out`, anchored left | Every in-text link |
| Rule draw-on | `scaleX(0→1)`, origin left, 1000ms `--ease-out`, 1000ms delay (`both` fill) | Under the masthead; 2000ms delay on the closing rule |
| Panel rule | same keyframes, 420ms after 160ms | Inside the contact panel |
| Popover in / out | `opacity 0, scale(0.96) translateY(-0.25rem)` → rest in 160ms `cubic-bezier(0.16,1,0.3,1)`; out to `scale(0.98)` in 120ms `cubic-bezier(0.4,0,1,1)` | Contact panel |
| Dialog in / out | fade + `scale(0.96)` 200ms; out 140ms | Modals (keyframes, not transitions) |
| Soft title | rest `blur(3.8px)` + `opacity .55`; sharpen in 184ms, return in 230ms | Landing titles |
| Breath | the rest blur ×(1+0.18) and opacity ×(1−0.18) on a ~5.2s `ease-in-out` `alternate` loop, each title with its own period and phase | Landing titles at rest |
| Random reveal | one title at a time surfaces by itself (sharpen + roll), holds ~1.6s, a few seconds apart | Landing |
| Split-flap roll | per character: 460ms, 26ms stagger, a new card every 55ms, a 0.08em drop as each card lands; 0.6× speed on leave | Wordmark, titles, display headings |
| Hover card | follows the pointer with an eased frame loop; grows from 75px square to the image ratio in 260ms `cubic-bezier(0.2,0,0,1)` | Titles with a hero image |
| Gallery drain | `filter: grayscale(1)` 450ms `--ease-out` | Image tiles under the pointer |
| Image in | `opacity 0, scale(0.94)` → rest, 380ms | Lightbox once decoded |
| Reveal skeleton | each block covered by a `--colour-hover` slab that pulses to `--colour-line` (1600ms ×2) and fades out (600ms) starting 1500ms in — the rule's midpoint — 120ms per block, record first, index second | CV and article body, over real server-rendered text |
| Loading bar | 40% ink segment sweeping a 2px track, 1100ms infinite | While something actually loads |
| Canvas loader | 3px ink bar, `scaleX` 0→1 from the left then 1→0 to the right, 1400ms | Before the WebGL scene mounts |

Durations outside the two tokens (120/200ms) are deliberate and belong to their effect:
chrome acknowledges a pointer without being noticed; draining a photograph or drawing a rule
*is* the effect, and at 200ms it reads as a flicker.

## Reduced motion

A blanket clamp — every animation and transition to 0.01ms, one iteration — so anything new
is covered by default. Then the cases where the clamp is the wrong answer:

- Infinite animations (loading bar, breath) become still, not a strobe.
- Anything whose resting state is hidden (lightbox image, reveal skeleton) is shown whole —
  "no animation" must mean visible.
- The reveal skeleton is removed entirely; delays are not motion, but 1.5s of grey slab over
  text is not an acceptable reduced form.
- The split-flap does not run. The hover card still appears and tracks; only its easing goes.
- Colour changes (gallery grey) stay, instantly: a colour change is feedback, not motion.

## Translating to other media

- Slides: no transitions beyond a plain fade or none; never fly-ins. A rule can draw on as a
  wipe from the left if the tool supports it.
- Video or animated social posts: the rule draw-on and the split-flap roll are the two
  signature moves; keep the timings above.
- Static media: show the end state. A soft title in print is sharp.
