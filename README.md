# h3nr7-design

The h3nr7.com design system, packaged as a **Claude skill** so Claude Desktop (and claude.ai,
and Claude Code) can make things that look like h3nr7: pages, artifacts, CVs, slides,
documents, social cards, charts.

Everything here is derived from the site itself — `h3nr7/packages/ui/src/styles/tokens.css`,
`h3nr7/apps/web/app/app.css`, the copy in `apps/web/app/lib/copy/`, the icons in
`apps/web/app/components/icons.tsx` — and the logo master `../h3nr7-design.ai`. When the site
changes, this follows it, not the other way round.

```
skills/h3nr7-design/        the skill — this folder is what gets zipped and uploaded
  SKILL.md                  entry point: essentials, tokens, fonts, logo rules, workflow
  references/               tokens · typography · components · motion · brand-assets · voice · outputs
  assets/h3nr7.css          portable stylesheet: tokens, base type, every h3- component
  assets/h3-scramble.js     the split-flap hover roll, vanilla JS
  assets/tokens.json        the same tokens as data
  assets/specimen.html      every token and component on one page (open it in a browser)
  assets/templates/         page · cv · landing · slides · social-card
  assets/logo/              the mark (SVG outlines + PNG), tiles, favicon glyph
  assets/icons/             the site's icons, currentColor
  assets/images/            portrait
  assets/fonts/             Mrs Eaves (local only, see below) + Inter, with fonts.json
  assets/reference/         screenshots of the v4 site
  scripts/inline.py         make an HTML file self-contained, fonts embedded
scripts/                    build tooling for this repo
source/fonts/               drop the Mrs Eaves files here (gitignored)
```

## Install in Claude Desktop

1. Make sure the Mrs Eaves files are in `source/fonts/` and built (see Fonts below).
2. `python scripts/package.py` → `dist/h3nr7-design.zip`.
3. In Claude Desktop: **Settings → Capabilities**, turn on *Code execution and file creation*.
4. **Customize → Skills → + → Create skill → Upload a skill**, choose the ZIP.
5. Try it: *"Make me a one-page write-up of the WebGL terrain project in my h3nr7 style."*

Re-upload the ZIP after any change. Uploaded skills are private to your account; keep it that
way — the ZIP contains Mrs Eaves.

**Claude Code** (optional): link the folder into your user skills instead of uploading —
From cmd: `mklink /J "%USERPROFILE%\.claude\skills\h3nr7-design" "<this repo>\skills\h3nr7-design"`
(Windows) or `ln -s "$PWD/skills/h3nr7-design" ~/.claude/skills/h3nr7-design`.

## Fonts

h3nr7.com sets **Mrs Eaves** (display) and **Inter** (body) from Adobe Fonts kit `jik4pcx`,
which only serves the site's own domains — so the skill carries the files.

- **Mrs Eaves** is commercial (Emigre). Only **Mrs Eaves OT Italic** is used, always with
  `liga` + `dlig` on. Put the licensed file in `source/fonts/` (any depth — the foundry folder
  as downloaded is fine). It and the copies the build places in the skill are **gitignored**:
  this repository never contains them, the ZIP built on your machine does. The build writes
  the desktop file unchanged plus a WOFF2 with the CFF table rewritten, because Chrome rejects
  the 1996 original — including the foundry's own web kit — with
  `OTS parsing error: CFF : Failed to parse Top DICT Data`.
- **Inter** (OFL) is committed: static, Latin-subset instances at the 18pt optical size the
  kit serves, plus WOFF2 copies.

```bash
python scripts/build_fonts.py                       # after adding/changing Mrs Eaves files
python scripts/build_fonts.py --inter <google-fonts-inter-dir>   # to rebuild Inter as well
```

`build_fonts.py` writes `assets/fonts/fonts.json`, which `inline.py` and the skill read to
find each face. `package.py` refuses to build a ZIP with no Mrs Eaves in it.

## Rebuilding the other assets

```bash
pip install -r scripts/requirements.txt
python scripts/build_logos.py ../h3nr7-design.ai   # SVG outlines + PNGs from the Illustrator master
python scripts/build_specimen.py                   # regenerate assets/specimen.html
python scripts/package.py                          # validate + zip
```

`package.py`, `build_specimen.py` and the skill's `inline.py` need only the standard library;
`build_logos.py` needs PyMuPDF + Pillow, `build_fonts.py` needs fontTools + brotli.

The reference screenshots were taken from the local v4 site (`pnpm local --dev` in the h3nr7
repo) with Playwright; the canvas layer was hidden on the hover shot because the billboard's
blob plays third-party footage.

## Deliberately left out

- The v3 identity in `h3nr7/legacy/`: Akkurat, Rift and Roboto fonts (commercial or off-brand),
  the pastel infographic artboards, the old 200px diagonal logo (the favicon glyph replaces it).
- The CV's real content — the CV template uses placeholders.
- The `correspondents.mp4` clip the billboard plays inside its blob.
