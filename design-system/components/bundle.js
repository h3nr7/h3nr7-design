/* @ds-bundle: {"format":4,"namespace":"h3nr7","components":[]} */
/* h3nr7 has no JavaScript component library: the components are the h3- classes in bundle.css.
   This bundle carries the one script the system has, the split-flap roll for [data-scramble]
   (templates/h3-scramble.js, verbatim below), and lets the component previews run live. */
/*
 * h3-scramble: the split-flap roll h3nr7.com plays on hover. Vanilla port of
 * ScrambleText (packages/ui/src/components/ScrambleText.tsx), same timings.
 *
 *   <a href="…"><span data-scramble>WebGl terrain mesh</span></a>
 *   <h1 class="h3-landing-name"><span data-scramble>h3nr7</span></h1>
 *
 * Add class "h3-soft" (and data-breathe) to the span for the blurred-at-rest
 * look; that half is pure CSS in h3nr7.css. Each character rolls through
 * A–Z a–z 0–9 and lands on itself, staggered left to right; ligature pairs
 * (the full liga + dlig set of Mrs Eaves OT Italic: st, ct, ee, fi, ffi, Th, TT, …) roll as one cell so the
 * fused glyph keeps its width.
 * Does nothing under prefers-reduced-motion. Screen readers get the text once.
 */
(() => {
  const GLYPHS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  // Every ligature in the bundled Mrs Eaves OT Italic (liga + dlig, shaped with HarfBuzz),
  // longest first so 'ffi' is tried before 'ff' and 'fi'. A pair split across two cells
  // lands twice and the settled letter visibly changes shape — the "jump".
  const LIGATURES = [
    'ffb', 'ffh', 'ffi', 'ffj', 'ffl', 'ffr', 'fft', 'ffy', 'cky', 'ggy', 'tty', 'THE',
    'AA', 'AV', 'FF', 'FI', 'FL', 'HE', 'LA', 'MB', 'MD', 'ME', 'MP', 'NK', 'NT', 'OC', 'OG', 'OO',
    'TE', 'TR', 'TT', 'TW', 'TY', 'Th', 'UB', 'UD', 'UL', 'UP', 'UR', 'VA',
    'ae', 'ct', 'ee', 'fb', 'ff', 'fh', 'fi', 'fj', 'fl', 'fr', 'ft', 'fy', 'gg', 'gi', 'gy',
    'ip', 'it', 'ky', 'oe', 'py', 'sp', 'st', 'tt', 'tw', 'ty',
  ];
  const FLAP_MS = 55;
  const DURATION = 460;
  const STAGGER = 26;
  const EXIT = 0.6;
  const reduced = () => window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function cellsOf(word) {
    const chars = Array.from(word);
    const out = [];
    for (let i = 0; i < chars.length; ) {
      const lig = LIGATURES.find((l) => chars.slice(i, i + l.length).join('') === l);
      const cell = lig || chars[i];
      out.push(cell);
      i += Array.from(cell).length;
    }
    return out;
  }

  function wire(host) {
    const text = host.textContent;
    const trigger = host.closest('a, button') || host;
    let frame = 0;
    let running = false;

    const stop = () => {
      cancelAnimationFrame(frame);
      running = false;
      host.textContent = text;
      host.removeAttribute('data-flapping');
    };

    const start = (scale = 1) => {
      if (running || reduced()) return;
      running = true;
      host.setAttribute('data-flapping', '');
      const dur = DURATION * scale;
      const stg = STAGGER * scale;
      const flaps = Math.max(1, Math.round(dur / FLAP_MS));
      const label = Object.assign(document.createElement('span'), { className: 'h3-visually-hidden', textContent: text });
      const stage = document.createElement('span');
      stage.setAttribute('aria-hidden', 'true');
      const cells = [];
      let offset = 0;
      text.split(/(\s+)/).forEach((word, i) => {
        if (!word) return;
        if (i % 2) return void stage.append(word);
        const w = Object.assign(document.createElement('span'), { className: 'h3-scramble-word' });
        for (const group of cellsOf(word)) {
          const el = Object.assign(document.createElement('span'), { className: 'h3-scramble-char', textContent: group });
          w.append(el);
          const parts = Array.from(group).map((c) => {
            const at = GLYPHS.indexOf(c);
            return { real: c, rolls: at >= 0, from: at >= 0 ? at - flaps : 0 };
          });
          cells.push({ el, real: group, parts, offset });
          offset += parts.length;
        }
        stage.append(w);
      });
      host.replaceChildren(label, stage);
      // Pin each cell to its real width so the line never jitters.
      cells.forEach((c) => { c.el.style.width = `${c.el.getBoundingClientRect().width}px`; });
      const total = offset * stg + dur;
      const began = performance.now();
      const tick = (now) => {
        const t = now - began;
        for (const c of cells) {
          const p = (t - c.offset * stg) / dur;
          if (p <= 0 || p >= 1) {
            if (c.el.textContent !== c.real) c.el.textContent = c.real;
            c.el.style.removeProperty('--flap');
            continue;
          }
          const pos = p * flaps;
          const card = Math.floor(pos);
          c.el.textContent = c.parts
            .map((x) => (x.rolls ? GLYPHS[(((x.from + card) % GLYPHS.length) + GLYPHS.length) % GLYPHS.length] : x.real))
            .join('');
          c.el.style.setProperty('--flap', String(pos - card));
        }
        if (t < total) frame = requestAnimationFrame(tick);
        else stop();
      };
      frame = requestAnimationFrame(tick);
    };

    trigger.addEventListener('pointerenter', () => start());
    trigger.addEventListener('focusin', () => start());
    trigger.addEventListener('pointerleave', () => start(EXIT));
    trigger.addEventListener('focusout', () => start(EXIT));
  }

  const init = () => document.querySelectorAll('[data-scramble]').forEach(wire);
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();

window.h3nr7 = window.h3nr7 || {};
