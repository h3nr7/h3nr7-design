#!/usr/bin/env python3
"""
Turn a Claude Docs export into an h3nr7 tech-doc HTML page, ready for html2epub.py.

    python scripts/docs2page.py "My doc.docx" -o page.html          # preferred input
    python scripts/docs2page.py "My doc.html" -o page.html          # the HTML export
    python scripts/docs2page.py doc.docx -o page.html --kind "Learning note" --owner "Henry YP Ho"

Why a converter: a Claude doc's exports carry no styling at all. The HTML export
is a bare fragment (no <head>, no CSS, no fonts) and leaves every diagram out,
keeping only its caption. The Word export keeps the diagrams as PNGs and names
the people mentioned, but pandoc reads its code blocks as plain text unless
told which Word styles are code. So this script:

  * .docx: renames the Docs code styles (Code, CodeChar) to the names pandoc
    knows (Source Code, Verbatim Char), converts with pandoc, keeps the images.
  * .html: turns <time data-atom> into a written date, mention chips into the
    owner's name, and empty diagram embeds into a one-line note.

Then it lays the content out as an h3nr7 tech doc, linking the design skill's
own h3nr7.css and techdoc.css: the opening (mark, label, title, ink rule, meta
columns), h2s as display-italic takeaways, hairline tables, figures on a
surface panel, the closing rule and footer. Needs pandoc for .docx; lxml.
"""

import argparse
import datetime as dt
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

from lxml import etree
from lxml import html as lhtml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from html2epub import find_design  # noqa: E402


def fix_docx(src: Path, dst: Path) -> None:
    """Give the Docs code styles the names pandoc maps to code."""
    names = {"Code": "Source Code", "CodeChar": "Verbatim Char"}
    with zipfile.ZipFile(src) as zin, zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "word/styles.xml":
                x = data.decode("utf-8")
                for sid, name in names.items():
                    x = re.sub(r'(<w:style\b[^>]*w:styleId="%s"[^>]*>\s*<w:name w:val=")[^"]*(")' % sid,
                               r"\g<1>%s\g<2>" % name, x)
                data = x.encode("utf-8")
            zout.writestr(item, data)


def from_docx(path: Path, media_dir: Path) -> str:
    if not shutil.which("pandoc"):
        sys.exit("pandoc is needed for .docx input")
    tmp = Path(tempfile.mkdtemp()) / "fixed.docx"
    fix_docx(path, tmp)
    out = subprocess.run(["pandoc", str(tmp), "-f", "docx", "-t", "html5", "--wrap=none",
                          f"--extract-media={media_dir}"], check=True, capture_output=True, text=True)
    return out.stdout


def nice_date(s: str) -> str:
    for fmt in ("%Y-%m-%d", "%b %d, %Y", "%B %d, %Y", "%d %B %Y"):
        try:
            d = dt.datetime.strptime(s.strip(), fmt)
            return f"{d.day} {d.strftime('%B %Y')}"
        except ValueError:
            pass
    return s.strip()


def text_of(el) -> str:
    return re.sub(r"\s+", " ", el.text_content()).strip()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", help="the doc's Word (.docx) or HTML export")
    ap.add_argument("-o", "--output", required=True, help="the h3nr7 page to write (.html)")
    ap.add_argument("--design", help="path to skills/h3nr7-design")
    ap.add_argument("--kind", default="Note", help="first part of the opening label, e.g. 'Learning note'")
    ap.add_argument("--owner", default="Henry YP Ho")
    ap.add_argument("--website", default="h3nr7.com")
    ap.add_argument("--source", default="Claude doc", help="third meta column")
    ap.add_argument("--footer", default="Otherwise I am always up for a coffee and/or a chat.")
    a = ap.parse_args()

    src = Path(a.input).resolve()
    out = Path(a.output).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    design = find_design(a.design)
    media = out.parent / (out.stem + "-media")

    if src.suffix.lower() == ".docx":
        frag = from_docx(src, media)
    else:
        frag = src.read_text(encoding="utf-8")
    root = lhtml.fragment_fromstring(frag, create_parent="div")

    # HTML-export chips
    for t in root.xpath(".//time[@data-atom='date']"):
        t.text = nice_date(t.get("datetime") or t.text_content())
        for c in list(t):
            t.remove(c)
    for m in root.xpath(".//span[@data-atom='mention']"):
        m.text = a.owner
        for c in list(m):
            m.remove(c)
    for fig in root.xpath(".//figure[@data-embed]"):
        if fig.find(".//img") is None:
            cap = fig.find("figcaption")
            p = lhtml.Element("p", {"class": "h3-doc-sub"})
            p.text = f"Diagram: {text_of(cap) if cap is not None else 'see the doc'} (not in the HTML export; use the Word export to keep it)."
            fig.getparent().replace(fig, p)

    # title and byline
    h1 = root.find(".//h1")
    title = text_of(h1) if h1 is not None else src.stem
    date = owner = None
    if h1 is not None:
        nxt = h1.getnext()
        h1.drop_tree()
        if nxt is not None and nxt.tag == "p" and "·" in text_of(nxt) and len(text_of(nxt)) < 80:
            left, _, right = text_of(nxt).partition("·")
            date, owner = nice_date(left), right.strip().lstrip("@") or None
            nxt.drop_tree()
    owner = a.owner  # the doc's mention is a short display name; the meta wants the full one
    label = " · ".join(x for x in (a.kind, date) if x)

    # images: lone image paragraphs become figures; the caption paragraph after joins them
    for img in list(root.iter("img")):
        if img.get("style"):
            del img.attrib["style"]
        p = img.getparent()
        if p.tag == "p" and len(p) == 1 and not (p.text or "").strip():
            fig = lhtml.Element("figure", {"class": "h3-doc-figure"})
            fig.append(lhtml.Element("img", {k: v for k, v in img.attrib.items()}))
            cap = p.getnext()
            if cap is not None and cap.tag == "p" and text_of(cap) and text_of(cap) == (img.get("alt") or "").strip():
                fc = lhtml.Element("figcaption")
                fc.text = text_of(cap)
                fig.append(fc)
                cap.drop_tree()
            p.getparent().replace(p, fig)

    for t in root.iter("table"):
        t.set("class", "h3-doc-table")
        for attr in ("style", "border", "width"):
            t.attrib.pop(attr, None)
        wrap = lhtml.Element("div", {"class": "h3-doc-scroll"})
        t.getparent().replace(t, wrap)
        wrap.append(t)
    for h in root.iter("h2"):
        h.set("class", "h3-doc-takeaway")
    for c in root.xpath(".//colgroup"):
        c.drop_tree()

    # a "References"/"Sources" section's lists use the hairline refs style
    for h in root.iter("h2"):
        if re.match(r"(references|sources)\b", text_of(h), re.I):
            for sib in h.itersiblings():
                if sib.tag == "h2":
                    break
                if sib.tag == "ul":
                    sib.set("class", "h3-doc-refs")

    body_html = "".join(lhtml.tostring(c, encoding="unicode") for c in root)
    if root.text and root.text.strip():
        body_html = f"<p>{root.text.strip()}</p>" + body_html
    mark = (design / "assets" / "logo" / "h3nr7-mark.svg").read_text(encoding="utf-8")
    mark = re.sub(r"<\?xml.*?\?>", "", mark).strip()
    css = [design / "assets" / "h3nr7.css", design / "assets" / "techdoc.css"]
    esc = lambda s: (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    page = f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} — h3nr7</title>
{''.join(f'<link rel="stylesheet" href="{p.as_uri()[7:]}">' for p in css)}
<style>
.h3-doc-body-prose {{ margin-top: var(--space-16); }}
.h3-doc-body-prose h2.h3-doc-takeaway {{ font-family: var(--font-display); font-style: italic; font-weight: var(--weight-regular);
  font-size: var(--text-2xl); line-height: var(--leading-tight); font-variant-ligatures: common-ligatures discretionary-ligatures contextual;
  margin: var(--space-16) 0 var(--space-4); text-transform: none; letter-spacing: normal; color: var(--colour-ink); max-width: 28ch; }}
.h3-doc-body-prose h3 {{ font-family: var(--font-display); }}
.h3-doc-body-prose pre {{ background: var(--colour-surface); border-radius: var(--radius-lg); padding: var(--space-4); font-size: var(--text-xs); margin: 0 0 var(--space-6); overflow-x: auto; }}
.h3-doc-body-prose :not(pre) > code {{ font-size: 0.86em; }}
.h3-doc-body-prose .h3-doc-figure img {{ display: block; width: 100%; height: auto; border-radius: 0; }}
.h3-doc-body-prose .h3-doc-table td:first-child {{ color: var(--colour-ink); }}
.h3-doc-body-prose .h3-doc-table td {{ color: var(--colour-ink-muted); }}
</style>
</head>
<body>
<main class="h3-page h3-page-wide">
  <header class="h3-doc-opening">
    <a class="h3-doc-mark" href="https://h3nr7.com/" aria-label="h3nr7 — home">{mark}</a>
    <p class="h3-label">{esc(label)}</p>
    <h1 class="h3-doc-title">{esc(title)}</h1>
    <span class="h3-rule" role="presentation"></span>
    <div class="h3-doc-meta">
      <div><p class="h3-label">Owner</p><p>{esc(owner)}</p></div>
      <div><p class="h3-label">Website</p><p><a class="h3-link" href="https://{esc(a.website)}/">{esc(a.website)}</a></p></div>
      <div><p class="h3-label">Source</p><p>{esc(a.source)}</p></div>
    </div>
  </header>
  <div class="h3-prose h3-doc-body-prose">
{body_html}
  </div>
  <span class="h3-rule h3-rule-close" role="presentation"></span>
  <footer class="h3-footer"><p>{esc(a.footer)}</p></footer>
</main>
</body>
</html>
"""
    out.write_text(page, encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
