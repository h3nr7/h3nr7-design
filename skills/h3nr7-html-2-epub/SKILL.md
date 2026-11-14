---
name: h3nr7-html-2-epub
description: Convert an h3nr7-styled HTML page, a Claude artifact page or a Claude doc into an EPUB 3 ebook that keeps the h3nr7 look - Mrs Eaves italic display over Inter, the monochrome palette, hairline tables, the tech-doc opening and panels, inline SVG diagrams - with the real CSS and fonts from the h3nr7-design skill, chapters, a table of contents and an h3nr7 cover. Use whenever Henry (h3nr7) asks for an epub, ebook, Kindle, Apple Books or Kobo version of a page, cheat sheet, learning note, tech doc, artifact or Claude doc, or says html to epub, doc to epub, make this readable on my e-reader. Not for Lumina or Kyoso work.
---

# h3nr7 HTML → EPUB

Turns an h3nr7 page into an ebook that still looks like h3nr7. Everything a page's design
depends on travels with it: the page's own classes and layout CSS, made e-reader safe; the
brand faces from the h3nr7-design skill (TTF, never the page's inline copies); inline SVG
diagrams; images. What a reader cannot do (hover, motion, sideways scrolling, a fixed page
width) is resolved into the finished, resting state.

Paths below are relative to this skill's folder. The design skill sits beside it in the same
repository: `../h3nr7-design/` (assets/h3nr7.css, techdoc.css, fonts/, logo/).

## 0. Get the current skill and the design assets

Source of truth is the public repository, as for h3nr7-design:

```bash
GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 https://github.com/h3nr7/h3nr7-design   # or git pull
cd h3nr7-design/skills/h3nr7-html-2-epub
```

The scripts find `../h3nr7-design` on their own; pass `--design <path>` if it lives elsewhere.
Needs Python 3.10+, lxml and Pillow (all usually present), pandoc for Word input, and a
headless Chrome only for the preview step. Nothing is installed from the network.

## 1. Get the HTML onto disk

**An HTML file** (attached, or built with h3nr7-design): use it as it is. Local stylesheets,
images and `data:` URIs are all picked up.

### From Claude: an artifact page or a Claude doc

This is the usual case, and how the HTML gets to disk matters, because base64 copied by hand
out of a tool result comes out a character off.

**A Claude artifact page** (a hand-built HTML artifact, such as an h3nr7 tech doc or cheat
sheet: a `claude.ai/artifact/…` link that is not a Docs-type doc). This is the best source:
it carries the real classes, the SVG diagrams and the layout.

1. `get_artifact` with the link → its `slug` (the link's short id is not the slug).
2. `list_files` with the slug → usually just `index.html`.
3. `read_file` with `slug` and **`paths: ["index.html"]`** (the plural). The file comes back
   *saved to a local path*, not printed into the conversation. Copy it into the work folder:
   `cp /tmp/claude-tool-results/*/mcp-claude-artifacts-blob-*.html work/page.html`
   (take the newest if there are several). Never use `read_artifact` for this: it prints the
   whole page, embedded fonts and all, into the context.
4. Go to step 2 with `work/page.html`. Its inline fonts are ignored; the design skill's are used.

**A Claude doc** (a Docs-type artifact: editable, commentable, tabs). Its exports carry no
styling at all, so the h3nr7 layout is applied by `scripts/docs2page.py`:

- The **HTML export** is a bare fragment: no `<head>`, no CSS, no fonts, mentions as raw ids,
  and every diagram reduced to its caption. Use it only when there are no diagrams.
- The **Word export** keeps diagrams as PNGs and names the people mentioned. Prefer it.

1. Read the doc (`read` with the link) to get its tab id (`files[].id`).
2. `export` with `format: "docx"`, `file: <tab id>`, `pictures: "fit"`. A doc with a diagram
   or two is large enough that the result is **saved to a file** (the tool says where).
   Decode it:
   ```bash
   python3 -c "import json,base64,sys; d=json.load(open(sys.argv[1]))['data']; open('work/doc.docx','wb').write(base64.b64decode(d['bytes_b64']))" /tmp/claude-tool-results/<…>/mcp-Claude_Docs-export-<…>.txt
   ```
   If it comes back **inline** instead (a small doc), do not retype the base64. Ask Henry to
   click the doc's name → Export → Word and attach the file (or pick it from his Downloads
   through the desktop app), then use that.
3. `python scripts/docs2page.py work/doc.docx -o work/page.html --kind "Learning note"`
   This renames the Docs code styles so pandoc keeps code blocks, then lays the content out as
   an h3nr7 tech doc linked to the design skill's `h3nr7.css` + `techdoc.css`: the opening
   (mark, label "Kind · date", title, ink rule, Owner / Website / Source), h2s as
   display-italic takeaways, hairline tables, figures on a surface panel, references in the
   refs style, closing rule and footer. `--owner`, `--website`, `--source`, `--footer` adjust it.
4. Open `work/page.html` in a browser if one is to hand: it is a normal h3nr7 page, and
   whatever looks wrong there will look wrong in the book. Then go to step 2.

## 2. Build the EPUB

```bash
python scripts/html2epub.py work/page.html -o "out/Title.epub" --keep-build work/build
```

Useful options: `--author` (default Henry YP Ho), `--title`, `--label` (cover label line),
`--split h2|h3|none` (chapter boundary, default h2), `--cover image.jpg`, `--no-cover`,
`--no-display-font` (leave Mrs Eaves out, for a copy others will read), `--no-obfuscate`.

What the converter does to the CSS, so nothing surprises you:

| In the page | In the book | Why |
|---|---|---|
| `var(--colour-ink)` and every other token, in CSS, `style=""` and SVG | the literal light-theme value | many readers have no custom properties |
| `@media (prefers-color-scheme: dark)`, `[data-theme=dark]`, print, hover blocks | dropped | the reader owns night mode |
| `clamp(a, b, c)`, `min()/max()` with vw | `a` / the non-viewport term | no viewport in a reader |
| `color-mix(in srgb, #x p%, transparent)` | `rgba(…)` | wide support |
| `:is(…)`, `:where(…)` | expanded selector lists | old engines drop the whole rule |
| `min-width`, `position: fixed/sticky`, vw/vh values | removed | a page cannot scroll sideways |
| animations, transitions, `.h3-soft` blur, scramble | resting state | no motion, no hover |
| tables, `pre` | wrap inside the page | same reason |
| page `@font-face` (inline woff2) | the design skill's TTFs, only the families used | the real files, every reader takes TTF |

`assets/epub.css` is appended last: reader margins, pagination (headings stay with what
follows; figures, cells, panels and table rows stay whole), wrapping, and a fix for
techdoc.css's narrow-screen meta spacing. Edit it rather than the page when the book alone
needs a change.

Chapters: chapter one is the opening (everything before the first h2: the cover header and
the statement panel). Then one chapter per h2 with what follows it, its wrappers kept so the
page's classes still apply. The contents list is built from h2s, with h3s nested.

The cover is drawn from the page: the mark PNG from the design skill, the opening label
(tracked Inter caps), the title in Mrs Eaves with its ligatures, an ink rule, the author.

## 3. Check it

The build ends with a structural check (zip layout, well-formed XHTML, manifest against
files, SVG properties, images and links). It is not epubcheck; run epubcheck too if it is
installed. Then look at it:

```bash
python scripts/preview.py work/build -o work/shots          # add --dark for night mode
```

Open the cover, chapter one, a chapter with a diagram, one with a table and one with code.
Check that headings are Mrs Eaves italic (not a Times fallback), labels are tracked Inter caps,
tables have no mid-word breaks, code wraps inside its surface block, diagrams are legible.
No Chrome here: say so, and suggest Apple Books, Thorium or calibre's viewer on Henry's machine.

## 4. Deliver

Send the `.epub` (SendUserFile). One line on what it is, plus the font note below if Mrs Eaves
is in it. If he wants it on his computer and the desktop app is connected, write it there too.

## Fonts and sharing

Mrs Eaves is a licensed Emigre face (Preview and Print embedding). An EPUB embeds the font
file, so a book with Mrs Eaves in it is **for Henry's own reading**. The converter obfuscates
embedded fonts the standard IDPF way (readers undo it; the file inside is not a usable font),
which is what the format offers for licensed faces, but it does not change the licence. For a
copy that goes to anyone else, build with `--no-display-font` (display type falls back to the
Baskerville stack) or send a PDF. Never send the font files themselves. Inter is OFL and fine.

## What a reader changes, whatever we do

- Text reflows to the screen and the reader's font size. Layouts stay; fixed positions do not.
- Grids (numbered cells, meta columns, panels' three-up lines) collapse to one column on
  narrow screens, as on a phone.
- Wide SVG diagrams shrink to the page width; on a phone their 11–13px labels get small.
  For diagram-heavy books, mention that a tablet or landscape reads better.
- Readers may override fonts (Kindle and Apple Books let the reader choose) and invert
  colours in night mode. The ink panel inverts with it.
- Kindle: Send to Kindle takes EPUB and converts it. If the brand faces do not show there,
  rebuild with `--no-obfuscate` for his own device.

## Troubleshooting

- *Headings in Times*: the face did not load. Check `OEBPS/fonts/` has MrsEavesOT-Italic.ttf
  and that `../h3nr7-design/assets/fonts/` holds the real file, not an LFS pointer.
- *A section missing from the contents*: its heading is not an h2 at the same depth as the
  others; use `--split h3` or `--split none`.
- *Code arrived as plain paragraphs from a Claude doc*: the doc used a code style other than
  Code / CodeChar. Look at `word/styles.xml` and add the id to `fix_docx` in docs2page.py.
- *A diagram missing from a Claude doc*: it came from the HTML export. Use the Word export.
