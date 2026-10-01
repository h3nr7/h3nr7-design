"""
Regenerate skills/h3nr7-design/assets/specimen.html — every token and component on one page.

    python scripts/build_specimen.py

A generator rather than a hand-kept file so the icon row and the mark are always the files
in assets/, inlined (an <img> of an SVG cannot take currentColor, so it would not invert in
dark mode). Standard library only.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "skills" / "h3nr7-design" / "assets"


def inline_svg(path: Path, size: str = "") -> str:
    svg = path.read_text(encoding="utf-8").strip()
    svg = re.sub(r"<title>.*?</title>\s*", "", svg, flags=re.S)
    svg = svg.replace("<svg ", '<svg aria-hidden="true" focusable="false" ', 1)
    if size:
        svg = re.sub(r'\swidth="[^"]*"\s+height="[^"]*"', f" {size}", svg, count=1)
    return svg


def main() -> None:
    tokens = json.loads((ASSETS / "tokens.json").read_text(encoding="utf-8"))
    mark = inline_svg(ASSETS / "logo" / "h3nr7-mark.svg", 'width="150" height="201"')
    glyph = inline_svg(ASSETS / "logo" / "h3nr7-glyph.svg", 'width="32" height="32"')

    swatches = "\n".join(
        f'<div class="sw"><span class="sw-chip" style="background:var(--colour-{name})"></span>'
        f'<span class="sw-name">--colour-{name}</span>'
        f'<span class="sw-hex">{v["light"]} · {v["dark"]}</span><span class="sw-role">{v["role"]}</span></div>'
        for name, v in tokens["colour"].items()
        if name != "focus"
    )
    scale = "\n".join(
        f'<div class="sc"><span class="sc-k">{k}</span><span class="sc-v" style="font-size:var(--text-{k})">'
        f"Tinkering things</span><span class=\"sc-n\">{v}</span></div>"
        for k, v in tokens["text"].items()
        if not k.startswith("landing")
    )
    spaces = "\n".join(
        f'<div class="sp"><span class="sp-bar" style="width:var(--space-{k})"></span><span>{k} · {v}</span></div>'
        for k, v in tokens["space"].items()
    )
    radii = "\n".join(
        f'<div class="rd"><span class="rd-box" style="border-radius:var(--radius-{k})"></span><span>{k} · {v}</span></div>'
        for k, v in tokens["radius"].items()
    )
    icons = "\n".join(
        f'<figure class="ic"><span>{inline_svg(p)}</span><figcaption>{p.stem}</figcaption></figure>'
        for p in sorted((ASSETS / "icons").glob("*.svg"))
    )
    chat = inline_svg(ASSETS / "icons" / "chat.svg")
    link = inline_svg(ASSETS / "icons" / "link.svg")
    social = "".join(
        f'<a class="h3-icon-button" href="#" aria-label="{n}">{inline_svg(ASSETS / "icons" / f"{n}.svg")}</a>'
        for n in ("x", "github", "linkedin", "youtube")
    )

    html = TEMPLATE
    for key, value in {
        "MARK": mark, "GLYPH": glyph, "SWATCHES": swatches, "SCALE": scale, "SPACES": spaces,
        "RADII": radii, "ICONS": icons, "CHAT": chat, "LINK": link, "SOCIAL": social,
    }.items():
        html = html.replace(f"{{{{{key}}}}}", value)
    out = ASSETS / "specimen.html"
    out.write_text(html, encoding="utf-8", newline="\n")
    print(f"wrote {out} ({out.stat().st_size // 1024} KB)")


TEMPLATE = """<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>h3nr7 design system</title>
<link rel="icon" href="logo/h3nr7-glyph.png">
<link rel="stylesheet" href="h3nr7.css">
<style>
  /* Specimen-only layout. Everything else on this page is h3nr7.css. */
  .spec section { margin-top: var(--space-16); }
  .row { display: flex; flex-wrap: wrap; gap: var(--space-8); align-items: flex-end; }
  .cap { font-size: var(--text-xs); color: var(--colour-ink-faint); margin-top: var(--space-2); }
  .tile { width: 160px; height: 160px; border-radius: var(--radius-lg); overflow: hidden; }
  .tile img { width: 100%; height: 100%; }
  .grid-2 { display: grid; gap: var(--space-4); grid-template-columns: repeat(auto-fill, minmax(15rem, 1fr)); }
  .sw { display: grid; grid-template-columns: 2.5rem 1fr; column-gap: var(--space-3); align-items: center; }
  .sw-chip { grid-row: span 3; width: 2.5rem; height: 2.5rem; border-radius: var(--radius-md); border: 1px solid var(--colour-line); }
  .sw-name { font-size: var(--text-sm); font-weight: var(--weight-semibold); }
  .sw-hex, .sw-role { font-size: var(--text-xs); color: var(--colour-ink-faint); }
  .sc { display: grid; grid-template-columns: 3rem 1fr 5rem; align-items: baseline; gap: var(--space-4); padding: var(--space-2) 0; border-bottom: 1px solid var(--colour-line); }
  .sc-k, .sc-n { font-size: var(--text-xs); color: var(--colour-ink-faint); }
  .sp { display: flex; align-items: center; gap: var(--space-3); font-size: var(--text-xs); color: var(--colour-ink-faint); margin-bottom: var(--space-1); }
  .sp-bar { display: inline-block; height: 0.5rem; background: var(--colour-ink); }
  .rd { display: inline-flex; flex-direction: column; gap: var(--space-2); font-size: var(--text-xs); color: var(--colour-ink-faint); margin-right: var(--space-6); }
  .rd-box { width: 4rem; height: 4rem; background: var(--colour-surface); border: 1px solid var(--colour-ink); }
  .ic { display: inline-flex; flex-direction: column; align-items: center; gap: var(--space-2); width: 6rem; margin: 0 0 var(--space-4); }
  .ic > span { display: grid; place-items: center; width: 2.5rem; height: 2.5rem; border-radius: var(--radius-md); background: var(--colour-surface); }
  .ic figcaption { margin: 0; }
  .demo-ground { padding: var(--space-6); border-radius: var(--radius-xl); background: var(--colour-hover); }
</style>
</head>
<body>
<nav class="h3-chrome" aria-label="Specimen">
  <button class="h3-button" type="button" aria-pressed="false" id="theme">Dark</button>
</nav>
<main class="h3-page h3-page-wide spec">
  <header class="h3-masthead">
    <p class="h3-wordmark"><span data-scramble>h3nr7</span></p>
    <h1><span data-scramble>Design system</span></h1>
    <p class="h3-standfirst">Ink on paper, Mrs Eaves for the voice, Inter for the rest, hairlines for structure.</p>
    <p class="h3-date">Source: h3nr7.com v4 · tokens.css and app.css</p>
  </header>
  <span class="h3-rule h3-rule-soft" role="presentation"></span>

  <section style="margin-top:0">
    <h2 class="h3-label" style="margin-top:0">Mark</h2>
    <div class="row">
      <div>{{MARK}}<p class="cap">h3nr7-mark.svg · currentColor</p></div>
      <div><div class="tile"><img src="logo/h3nr7-tile-dark.svg" alt="h3nr7, white on black"></div><p class="cap">tile-dark</p></div>
      <div><div class="tile" style="outline:1px solid var(--colour-line)"><img src="logo/h3nr7-tile-light.svg" alt="h3nr7, black on white"></div><p class="cap">tile-light</p></div>
      <div>{{GLYPH}}<p class="cap">glyph · ≤ 32px</p></div>
      <div><p class="h3-landing-name" style="margin:0">h3nr7</p><p class="cap">text wordmark</p></div>
    </div>
  </section>

  <section>
    <h2 class="h3-label">Colour</h2>
    <div class="grid-2">{{SWATCHES}}</div>
  </section>

  <section>
    <h2 class="h3-label">Type</h2>
    <p class="h3-landing-lede">A techie journal of tinkering things.</p>
    <p class="cap">Statement · Mrs Eaves OT Italic · --text-landing (48–64px) · leading 0.95</p>
    <p class="h3-display" style="font-size:var(--text-3xl);line-height:var(--leading-tight);margin-top:var(--space-8)">first office coffee aesthetic street act spy kitty THE</p>
    <p class="cap">Ligatures, always on · liga: fi ff ffi fl ft · dlig: st ct sp ee ae it tt ty Th THE TT AV · never tracked</p>
    <div class="h3-cols" style="margin-top:var(--space-8)">
      <div class="h3-span-3">
        <p class="h3-landing-name" style="margin:0">WebGl terrain mesh</p>
        <p class="cap">Title · italic · --text-landing-name</p>
        <h3 style="font-style:italic;font-size:var(--text-xl);line-height:var(--leading-tight);margin-top:var(--space-6)">Platform &amp; Product Engineer — Company</h3>
        <p class="cap">Entry title · italic · --text-xl · the ct in Product is a ligature</p>
        <p class="h3-label" style="margin-top:var(--space-6)">Experience</p>
        <p class="cap">Label · Inter · sm · uppercase · 0.08em · faint</p>
      </div>
      <div class="h3-span-3">
        <p>Body is Inter at 16px on a 1.5 leading, set on a 68ch measure. It carries everything practical: prose, buttons, captions, navigation.</p>
        <p class="h3-standfirst">Standfirst · muted · base</p>
        <p class="h3-date">Date · faint · xs · 18 May 2020</p>
        <p class="h3-keywords">Keywords · TypeScript · React · WebGL</p>
      </div>
    </div>
    <div style="margin-top:var(--space-8)">{{SCALE}}</div>
  </section>

  <section>
    <h2 class="h3-label">Space and radius</h2>
    <div class="h3-cols"><div class="h3-span-3">{{SPACES}}</div><div class="h3-span-3">{{RADII}}</div></div>
  </section>

  <section>
    <h2 class="h3-label">Controls and links</h2>
    <div class="row" style="align-items:center">
      <button class="h3-button" type="button">Contact</button>
      <button class="h3-button" type="button" aria-pressed="true">Pressed</button>
      <button class="h3-button h3-button-square" type="button" aria-label="Link">{{LINK}}</button>
      <a class="h3-cta" href="#">Back to home</a>
      <span>A <a class="h3-link" href="#">link in a sentence</a>, swept on hover.</span>
    </div>
    <nav class="h3-landing-links"><a href="#">Articles</a><a href="#">GitHub</a><a href="#">Contact</a></nav>
  </section>

  <section>
    <h2 class="h3-label">Cards, panel, person</h2>
    <div class="h3-cols">
      <div class="h3-span-3 demo-ground">
        <div class="h3-panel" style="width:auto">
          <div class="h3-card h3-card-row"><span class="h3-card-title">Let's have a chat</span><a class="h3-icon-button" href="#" aria-label="Book a meeting">{{CHAT}}</a></div>
          <div class="h3-card">
            <div class="h3-person">
              <span class="h3-person-avatar">HH<img src="images/portrait-600.jpg" alt=""></span>
              <div class="h3-person-detail">
                <div class="h3-card-row"><span class="h3-person-name">Henry YP Ho</span><a class="h3-icon-button" href="#" aria-label="Open the profile site">{{LINK}}</a></div>
                <span class="h3-person-title">Platform &amp; Product Engineer</span>
                <span class="h3-person-url">iam.h3nr7.com</span>
              </div>
            </div>
            <span class="h3-card-rule"></span>
            <div class="h3-social">{{SOCIAL}}</div>
          </div>
        </div>
      </div>
      <div class="h3-span-3">
        <p class="h3-notice">GitHub and Medium are unavailable, so this list is incomplete.</p>
        <div class="h3-field" style="margin-top:var(--space-6)">
          <label for="pp">Passphrase</label>
          <input id="pp" placeholder="three words">
          <p class="h3-field-hint">It is in the email that sent you here.</p>
        </div>
        <div class="h3-dialog" style="margin-top:var(--space-6)">A dialog: surface, 1px line, 16px radius, no shadow.</div>
      </div>
    </div>
  </section>

  <section>
    <h2 class="h3-label">Imagery</h2>
    <div class="row">
      <div><span class="h3-hovercard"><span class="h3-gridfield" style="width:220px;height:124px"><span class="h3-monogram">R3</span></span></span><p class="cap">Hover card · square corner = point of contact</p></div>
      <div style="width:22rem"><ul class="h3-gallery" style="--cols:3">
        <li class="h3-gridfield"><span class="h3-monogram">A</span></li><li class="h3-gridfield"><span class="h3-monogram">B</span></li><li class="h3-gridfield"><span class="h3-monogram">C</span></li>
      </ul><p class="cap">Gallery · placeholder grid · drains to grey on hover</p></div>
    </div>
  </section>

  <section>
    <h2 class="h3-label">Motion</h2>
    <p class="h3-landing-lede" style="font-size:var(--text-3xl)">
      <a href="#"><span class="h3-soft" data-breathe data-scramble>Soft at rest</span></a>, <a href="#"><span class="h3-soft" data-breathe data-scramble>sharp under the pointer</span></a>.
    </p>
    <p class="cap">.h3-soft + data-breathe + data-scramble · the rule above drew itself on from the left</p>
  </section>

  <section>
    <h2 class="h3-label">Icons</h2>
    <div>{{ICONS}}</div>
  </section>

  <span class="h3-rule h3-rule-close" role="presentation"></span>
  <footer class="h3-footer"><p>Otherwise I am always up for a coffee and/or a <a href="#">chat</a>.</p></footer>
</main>
<script src="h3-scramble.js"></script>
<script>
  const b = document.getElementById('theme');
  const dark = () => document.documentElement.dataset.theme === 'dark' ||
    (!document.documentElement.dataset.theme && matchMedia('(prefers-color-scheme: dark)').matches);
  const label = () => { b.textContent = dark() ? 'Light' : 'Dark'; b.setAttribute('aria-pressed', String(dark())); };
  b.addEventListener('click', () => { document.documentElement.dataset.theme = dark() ? 'light' : 'dark'; label(); });
  label();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
