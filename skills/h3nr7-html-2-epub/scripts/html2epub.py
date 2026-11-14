#!/usr/bin/env python3
"""
Turn an h3nr7 HTML page into an EPUB 3 that keeps the h3nr7 look.

    python scripts/html2epub.py page.html -o book.epub
    python scripts/html2epub.py page.html -o book.epub --author "Henry YP Ho" --split h2
    python scripts/html2epub.py page.html -o book.epub --no-display-font   # to share it
    python scripts/html2epub.py page.html -o book.epub --keep-build build/  # for preview.py

What it does, in order:

1. Reads the page: inline <style>, local <link rel=stylesheet>, images (files or
   data: URIs) and inline SVG. Scripts, iframes, video and remote images are dropped.
2. Fonts come from the h3nr7-design skill (assets/fonts/fonts.json + the TTFs), never
   from the page: every @font-face in the page is removed and replaced by the
   bundled faces the page's font stacks ask for. Fonts are IDPF-obfuscated in the
   package unless --no-obfuscate (Mrs Eaves is licensed; see SKILL.md).
3. Makes the CSS e-reader safe: resolves var(--x) to literal light-theme values
   (SVG diagrams included), drops dark-mode and print blocks, replaces clamp(),
   color-mix(), :is()/:where() and viewport units, removes min-widths and fixed
   positioning. Then appends assets/epub.css (pagination, no hover, no motion).
4. Splits into chapters at --split (default h2): each h2 and what follows it, the
   wrappers around it kept, so every chapter carries the page's real classes.
   The opening (everything before the first h2) is chapter one.
5. Writes nav.xhtml + toc.ncx from the h2/h3 headings, an h3nr7 cover image
   (Mrs Eaves title, Inter label, ink rule) and the OPF, then zips it with the
   mimetype first and uncompressed. Then checks the package (--no-check to skip).

Needs: Python 3.10+, lxml, Pillow (cover). Optional: none. Standard EPUB 3.3 output.
"""

from __future__ import annotations

import argparse
import base64
import copy
import datetime as dt
import hashlib
import html as htmllib
import json
import mimetypes
import re
import shutil
import sys
import tempfile
import uuid
import zipfile
from html.entities import name2codepoint
from pathlib import Path

from lxml import etree
from lxml import html as lhtml

HERE = Path(__file__).resolve().parent.parent  # skills/h3nr7-html-2-epub
XHTML_NS = "http://www.w3.org/1999/xhtml"
SVG_NS = "http://www.w3.org/2000/svg"
EPUB_NS = "http://www.idpf.org/2007/ops"

mimetypes.add_type("image/svg+xml", ".svg")
mimetypes.add_type("image/webp", ".webp")
mimetypes.add_type("font/ttf", ".ttf")
mimetypes.add_type("font/otf", ".otf")
mimetypes.add_type("font/woff2", ".woff2")

IMG_EXT = {"image/png": ".png", "image/jpeg": ".jpg", "image/gif": ".gif",
           "image/svg+xml": ".svg", "image/webp": ".webp"}


def note(msg: str) -> None:
    print(f"  · {msg}", file=sys.stderr)


# ----------------------------------------------------------------- design skill

def find_design(explicit: str | None) -> Path:
    """Locate the h3nr7-design skill folder (the one with assets/h3nr7.css)."""
    cands = []
    if explicit:
        cands.append(Path(explicit).expanduser())
    cands += [HERE.parent / "h3nr7-design"]
    home = Path.home()
    for root in [home / ".claude" / "skills", Path("/home/claude"), Path.cwd()]:
        if root.is_dir():
            cands += sorted(root.glob("**/skills/h3nr7-design"))[:5]
            cands += sorted(root.glob("**/h3nr7-design/assets/h3nr7.css"))[:5]
    for c in cands:
        c = c.parent.parent if c.name == "h3nr7.css" else c
        if (c / "assets" / "h3nr7.css").is_file():
            return c.resolve()
    sys.exit("Cannot find the h3nr7-design skill (assets/h3nr7.css). Clone "
             "https://github.com/h3nr7/h3nr7-design and pass --design <repo>/skills/h3nr7-design")


def load_faces(design: Path) -> list[dict]:
    manifest = design / "assets" / "fonts" / "fonts.json"
    faces = []
    for f in json.loads(manifest.read_text())["faces"]:
        for key in ("desktop", "file"):  # prefer TTF: every reader takes it
            p = design / "assets" / "fonts" / (f.get(key) or "")
            if f.get(key) and p.is_file() and p.stat().st_size > 1024:
                faces.append({**f, "path": p})
                break
        else:
            note(f"font missing in the design skill, skipped: {f['family']} {f['subfamily']}")
    return faces


# ------------------------------------------------------------------- CSS tools

def strip_comments(css: str) -> str:
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def split_blocks(css: str):
    """Yield (prelude, body) for each top-level rule; at-rules without a block
    yield (statement, None). Brace-matched, string-aware enough for real CSS."""
    i, n = 0, len(css)
    while i < n:
        while i < n and css[i] in " \t\r\n;":
            i += 1
        if i >= n:
            break
        j = i
        quote = None
        while j < n:
            ch = css[j]
            if quote:
                if ch == quote and css[j - 1] != "\\":
                    quote = None
            elif ch in "'\"":
                quote = ch
            elif ch == "{" or ch == ";":
                break
            j += 1
        if j >= n:
            break
        prelude = css[i:j].strip()
        if css[j] == ";":
            yield prelude, None
            i = j + 1
            continue
        depth, k, quote = 1, j + 1, None
        while k < n and depth:
            ch = css[k]
            if quote:
                if ch == quote and css[k - 1] != "\\":
                    quote = None
            elif ch in "'\"":
                quote = ch
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
            k += 1
        yield prelude, css[j + 1:k - 1]
        i = k


def collect_vars(css: str) -> dict[str, str]:
    """Custom properties from plain `:root {}` rules (light theme, no media)."""
    out: dict[str, str] = {}
    for prelude, body in split_blocks(strip_comments(css)):
        if body is None or prelude.startswith("@"):
            continue
        if any(s.strip() == ":root" for s in prelude.split(",")):
            for m in re.finditer(r"(--[\w-]+)\s*:\s*([^;]+)", body):
                out[m.group(1)] = m.group(2).strip()
    return out


def _split_args(s: str) -> list[str]:
    parts, depth, cur = [], 0, ""
    for ch in s:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append(cur.strip())
            cur = ""
        else:
            cur += ch
    parts.append(cur.strip())
    return parts


def _replace_func(value: str, name: str, fn) -> str:
    """Replace every name(...) in value (innermost-safe) using fn(args)->str."""
    out, i = "", 0
    pat = re.compile(r"(?<![\w-])" + re.escape(name) + r"\(")
    while True:
        m = pat.search(value, i)
        if not m:
            return out + value[i:]
        depth, k = 1, m.end()
        while k < len(value) and depth:
            depth += {"(": 1, ")": -1}.get(value[k], 0)
            k += 1
        inner = value[m.end():k - 1]
        out += value[i:m.start()] + fn(inner)
        i = k


def resolve_value(value: str, vars_: dict[str, str], depth: int = 0) -> str | None:
    if depth > 12:
        return None
    missing = False

    def var_fn(inner: str) -> str:
        nonlocal missing
        args = _split_args(inner)
        name, fb = args[0], (", ".join(args[1:]) if len(args) > 1 else None)
        if name in vars_:
            r = resolve_value(vars_[name], vars_, depth + 1)
            if r is not None:
                return r
        if fb is not None:
            r = resolve_value(fb, vars_, depth + 1)
            if r is not None:
                return r
        missing = True
        return ""

    value = _replace_func(value, "var", var_fn)
    if missing:
        return None
    value = _replace_func(value, "clamp", lambda a: _split_args(a)[0])
    for f in ("min", "max"):
        value = _replace_func(value, f, lambda a: next(
            (x for x in _split_args(a) if not re.search(r"\d(dv|sv|lv)?(vw|vh|vmin|vmax)\b", x)),
            _split_args(a)[0]))
    value = _replace_func(value, "color-mix", _color_mix)
    value = _replace_func(value, "env", lambda a: _split_args(a)[-1] if len(_split_args(a)) > 1 else "0")
    return value


def _hex_rgb(h: str):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) if len(h) == 6 else None


def _color_mix(inner: str) -> str:
    """color-mix(in srgb, A p%, B q%?) for hex/transparent/currentColor."""
    args = _split_args(inner)[1:]
    if len(args) != 2:
        return "currentColor"

    def part(s):
        m = re.match(r"(.+?)\s+([\d.]+)%$", s.strip())
        return (m.group(1).strip(), float(m.group(2)) / 100) if m else (s.strip(), None)

    (a, pa), (b, pb) = part(args[0]), part(args[1])
    if pa is None and pb is None:
        pa = 0.5
    pa = pa if pa is not None else 1 - pb
    if b == "transparent" and a.startswith("#") and _hex_rgb(a):
        r, g, bl = _hex_rgb(a)
        return f"rgba({r}, {g}, {bl}, {pa:.2f})"
    if a.startswith("#") and b.startswith("#") and _hex_rgb(a) and _hex_rgb(b):
        ca, cb = _hex_rgb(a), _hex_rgb(b)
        return "#" + "".join(f"{round(x * pa + y * (1 - pa)):02x}" for x, y in zip(ca, cb))
    return a if a != "transparent" else b


def expand_is(selector: str) -> list[str]:
    """`.a > :is(p, ul) b` -> ['.a > p b', '.a > ul b']; :where() the same."""
    m = re.search(r":(is|where)\(", selector)
    if not m:
        return [selector]
    depth, k = 1, m.end()
    while k < len(selector) and depth:
        depth += {"(": 1, ")": -1}.get(selector[k], 0)
        k += 1
    head, inner, tail = selector[:m.start()], selector[m.end():k - 1], selector[k:]
    out = []
    for alt in _split_args(inner):
        out += expand_is(head + alt + tail)
    return out


DROP_DECL = re.compile(
    r"^\s*(min-width|min-height|position\s*:\s*(fixed|sticky)|backdrop-filter|"
    r"cursor|pointer-events|user-select|scroll-[\w-]+|overscroll[\w-]*|touch-action|"
    r"-webkit-text-size-adjust|content-visibility|container[\w-]*)", re.I)


def clean_declarations(body: str, vars_: dict[str, str]) -> str:
    out = []
    for decl in _split_decls(body):
        if ":" not in decl:
            continue
        prop, val = decl.split(":", 1)
        prop = prop.strip()
        if prop.startswith("--"):
            continue  # values already resolved below; old parsers choke on them
        if DROP_DECL.match(f"{prop}:{val}"):
            continue
        val2 = resolve_value(val.strip(), vars_)
        if val2 is None or not val2.strip():
            continue
        if re.search(r"\d(dv|sv|lv)?(vw|vh|vmin|vmax)\b", val2):
            continue
        out.append(f"{prop}: {val2}")
    return "; ".join(out)


def _split_decls(body: str) -> list[str]:
    parts, depth, cur, quote = [], 0, "", None
    for ch in body:
        if quote:
            if ch == quote:
                quote = None
        elif ch in "'\"":
            quote = ch
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        elif ch == ";" and depth == 0:
            parts.append(cur)
            cur = ""
            continue
        cur += ch
    parts.append(cur)
    return [p.strip() for p in parts if p.strip()]


def is_dark_or_screen_only(prelude: str) -> bool:
    p = prelude.lower()
    return any(k in p for k in ("prefers-color-scheme: dark", "prefers-color-scheme:dark",
                                "print", "hover: hover", "hover:hover", "pointer:",
                                "prefers-reduced-motion"))


def transform_css(css: str, vars_: dict[str, str], url_fn) -> str:
    """Rewrite one stylesheet for e-readers. url_fn(url) -> new url or None."""
    out = []
    for prelude, body in split_blocks(strip_comments(css)):
        if body is None:
            if prelude.lower().startswith(("@import", "@charset")):
                continue
            out.append(prelude + ";")
            continue
        low = prelude.lower()
        if low.startswith("@font-face"):
            continue  # fonts come from the design skill
        if low.startswith(("@keyframes", "@-webkit-keyframes", "@property", "@layer", "@container", "@page")):
            continue
        if low.startswith("@media"):
            if is_dark_or_screen_only(prelude):
                continue
            inner = transform_css(body, vars_, url_fn)
            if inner.strip():
                out.append(f"{prelude} {{\n{inner}\n}}")
            continue
        if low.startswith("@supports"):
            inner = transform_css(body, vars_, url_fn)
            if inner.strip():
                out.append(f"{prelude} {{\n{inner}\n}}")
            continue
        if low.startswith("@"):
            continue
        sels = []
        for s in _split_args(prelude):
            if re.search(r"data-theme\s*=\s*['\"]?dark|:hover|:focus|:active|::selection|"
                         r"::-webkit-scrollbar|::backdrop|:root:not", s):
                continue
            sels += expand_is(s)
        if not sels:
            continue
        decls = clean_declarations(body, vars_)
        decls = re.sub(r"url\(\s*(['\"]?)(.*?)\1\s*\)",
                       lambda m: f"url('{url_fn(m.group(2)) or ''}')", decls)
        decls = re.sub(r"[^;]*url\(''\)[^;]*;?", "", decls)
        if decls.strip():
            out.append(f"{', '.join(sels)} {{ {decls} }}")
    return "\n".join(out)


def font_families_used(css: str) -> set[str]:
    fams = set()
    for m in re.finditer(r"font-family\s*:\s*([^;}]+)", css):
        for f in m.group(1).split(","):
            fams.add(f.strip().strip("'\"").lower())
    return fams


# --------------------------------------------------------------- HTML helpers

SVG_RE = re.compile(r"<svg\b.*?</svg\s*>", re.S | re.I)


def protect_svg(src: str) -> tuple[str, list[str]]:
    """Cut outermost <svg>…</svg> blocks out before the HTML parser (which would
    lower-case viewBox and friends). Nested <svg> inside an svg is kept whole."""
    blocks: list[str] = []
    out, i = "", 0
    lower = src.lower()
    while True:
        s = lower.find("<svg", i)
        if s < 0:
            return out + src[i:], blocks
        depth, k = 0, s
        while True:
            o = lower.find("<svg", k)
            c = lower.find("</svg", k)
            if c < 0:
                return out + src[i:], blocks
            if 0 <= o < c:
                depth += 1
                k = o + 4
            else:
                depth -= 1
                k = lower.find(">", c) + 1
                if depth == 0:
                    break
        blocks.append(src[s:k])
        out += src[i:s] + f'<h3svg data-i="{len(blocks) - 1}"></h3svg>'
        i = k


def svg_element(text: str, vars_: dict[str, str]) -> etree._Element:
    def ent(m):
        name = m.group(1)
        if name in ("amp", "lt", "gt", "quot", "apos"):
            return m.group(0)
        cp = name2codepoint.get(name)
        return f"&#{cp};" if cp else ""
    text = re.sub(r"&([A-Za-z][A-Za-z0-9]*);", ent, text)
    if "xmlns=" not in text[:400]:
        text = text.replace("<svg", f'<svg xmlns="{SVG_NS}"', 1)
    if "xlink:" in text and "xmlns:xlink" not in text[:600]:
        text = text.replace("<svg", '<svg xmlns:xlink="http://www.w3.org/1999/xlink"', 1)
    try:
        el = etree.fromstring(text.encode("utf-8"))
    except etree.XMLSyntaxError:
        el = etree.fromstring(text.encode("utf-8"), etree.XMLParser(recover=True))
    # var() inside presentation attributes and style="" too
    for node in el.iter():
        if not isinstance(node.tag, str):
            continue
        for k, v in list(node.attrib.items()):
            if "var(" in v or "clamp(" in v:
                if k == "style":
                    node.set(k, clean_declarations(v, vars_))
                else:
                    r = resolve_value(v, vars_)
                    if r:
                        node.set(k, r)
                    else:
                        del node.attrib[k]
        if node.tag in (f"{{{SVG_NS}}}style", "style") and node.text:
            node.text = transform_css(node.text, vars_, lambda u: None)
        if node.tag in (f"{{{SVG_NS}}}script", "script"):
            node.getparent().remove(node)
    for k in list(el.attrib):
        if k.startswith("on"):
            del el.attrib[k]
    return el


def slug(text: str) -> str:
    s = re.sub(r"[^\w\s-]", "", text.lower()).strip()
    return re.sub(r"[\s_]+", "-", s)[:60] or "s"


# ------------------------------------------------------------------- the build

class Book:
    def __init__(self, args):
        self.a = args
        self.src = Path(args.input).resolve()
        self.base = self.src.parent
        self.design = find_design(args.design)
        self.build = Path(args.keep_build or tempfile.mkdtemp(prefix="h3epub-")).resolve()
        if self.build.exists():
            shutil.rmtree(self.build)
        (self.build / "OEBPS" / "css").mkdir(parents=True)
        (self.build / "OEBPS" / "fonts").mkdir()
        (self.build / "OEBPS" / "images").mkdir()
        (self.build / "META-INF").mkdir()
        self.images: dict[str, str] = {}   # key -> OEBPS-relative href
        self.fonts: list[str] = []

    # -- resources
    def add_image_bytes(self, data: bytes, mime: str, hint: str = "img") -> str:
        key = hashlib.sha1(data).hexdigest()[:12]
        if key not in self.images:
            ext = IMG_EXT.get(mime, mimetypes.guess_extension(mime) or ".bin")
            name = f"images/{slug(hint)[:24]}-{key}{ext}"
            (self.build / "OEBPS" / name).write_bytes(data)
            self.images[key] = name
        return self.images[key]

    def resolve_ref(self, ref: str, base: Path) -> str | None:
        """Return an OEBPS-relative href for an image reference, or None."""
        ref = ref.strip()
        if ref.startswith("data:"):
            m = re.match(r"data:([\w/+.-]+)?(;base64)?,(.*)", ref, re.S)
            if not m:
                return None
            mime = m.group(1) or "application/octet-stream"
            if not mime.startswith("image/"):
                return None
            raw = m.group(3)
            data = base64.b64decode(raw) if m.group(2) else htmllib.unescape(
                __import__("urllib.parse").parse.unquote(raw)).encode()
            return self.add_image_bytes(data, mime)
        if re.match(r"^(https?:)?//", ref):
            note(f"remote image dropped (readers block remote files): {ref[:80]}")
            return None
        p = Path(ref.split("#")[0].split("?")[0])
        p = p if p.is_absolute() else (base / p)
        if p.is_file():
            mime = mimetypes.guess_type(p.name)[0] or "application/octet-stream"
            if mime.startswith("image/"):
                return self.add_image_bytes(p.read_bytes(), mime, p.stem)
        note(f"image not found, dropped: {ref[:80]}")
        return None

    # -- main
    def run(self) -> Path:
        raw = self.src.read_text(encoding="utf-8", errors="replace")
        raw, svgs = protect_svg(raw)
        doc = lhtml.document_fromstring(raw)

        # metadata before we strip anything
        title_el = doc.find(".//title")
        h1 = doc.find(".//h1")
        page_title = (title_el.text_content().strip() if title_el is not None else "")
        h1_text = h1.text_content().strip() if h1 is not None else ""
        self.title = self.a.title or h1_text or re.sub(r"\s+[—-]\s+h3nr7$", "", page_title) or self.src.stem
        self.lang = self.a.lang or doc.get("lang") or "en-GB"
        cls = lambda c: f"contains(concat(' ', normalize-space(@class), ' '), ' {c} ')"
        label = doc.xpath(f"//*[{cls('k-cover-label')}] | //header//*[{cls('h3-label')}]")
        self.label = self.a.label or (label[0].text_content().strip() if label else "")

        # stylesheets, in document order
        css_parts = []
        for el in doc.iter("style", "link"):
            if el.tag == "style":
                css_parts.append((el.text or "", self.base))
            elif (el.get("rel") or "").lower() == "stylesheet":
                href = el.get("href") or ""
                p = Path(href) if Path(href).is_absolute() else (self.base / href)
                if p.is_file():
                    css_parts.append((p.read_text(encoding="utf-8"), p.parent))
                else:
                    note(f"stylesheet not found, skipped: {href}")
        if not css_parts:
            note("page has no CSS: using the design skill's h3nr7.css + techdoc.css")
            for f in ("h3nr7.css", "techdoc.css"):
                p = self.design / "assets" / f
                css_parts.append((p.read_text(encoding="utf-8"), p.parent))
        all_css = "\n".join(c for c, _ in css_parts)
        vars_ = collect_vars(all_css)
        if not vars_:
            vars_ = collect_vars((self.design / "assets" / "h3nr7.css").read_text())

        css_out = []
        for css, base in css_parts:
            css_out.append(transform_css(css, vars_, lambda u, b=base: (
                "../" + r if (r := self.resolve_ref(u, b)) else None)))
        page_css = "\n\n".join(c for c in css_out if c.strip())

        # fonts from the design skill, only the families the CSS asks for
        used = font_families_used(page_css)
        faces = load_faces(self.design)
        if self.a.no_display_font:
            faces = [f for f in faces if "eaves" not in f["family"].lower()]
            note("Mrs Eaves left out (--no-display-font): display falls back to the Baskerville stack")
        font_css = []
        for f in faces:
            if f["family"].lower() not in used:
                continue
            name = f"fonts/{f['path'].name}"
            shutil.copy(f["path"], self.build / "OEBPS" / name)
            self.fonts.append(name)
            fmt = {"ttf": "truetype", "otf": "opentype", "woff2": "woff2"}[f["path"].suffix[1:]]
            font_css.append(
                "@font-face { font-family: '%s'; font-style: %s; font-weight: %s; src: url('../%s') format('%s'); }"
                % (f["family"], f["style"], f["weight"], name, fmt))
        if any("eaves" in f.lower() for f in self.fonts):
            note("Mrs Eaves is embedded: this EPUB is for Henry's own reading. Share with --no-display-font, or as PDF.")
        epub_css = (HERE / "assets" / "epub.css").read_text(encoding="utf-8")
        (self.build / "OEBPS" / "css" / "book.css").write_text(
            "/* fonts: h3nr7-design */\n" + "\n".join(font_css) +
            "\n\n/* the page's own CSS, made e-reader safe */\n" + page_css +
            "\n\n/* e-reader overrides: h3nr7-html-2-epub/assets/epub.css */\n" + epub_css,
            encoding="utf-8")

        # clean the body
        body = doc.find("body")
        for bad in body.xpath(".//script|.//noscript|.//iframe|.//video|.//audio|.//canvas|"
                              ".//object|.//embed|.//template|.//form|.//input|.//select|.//textarea"):
            if bad.tag in ("video", "iframe", "canvas", "audio", "object", "embed"):
                note(f"<{bad.tag}> dropped: readers cannot play or run it")
            bad.drop_tree()
        for el in body.iter():
            if not isinstance(el.tag, str):
                continue
            for k in list(el.attrib):
                if k.startswith("on") or k in ("contenteditable", "draggable", "tabindex", "loading",
                                               "decoding", "fetchpriority", "srcset", "sizes",
                                               "data-scramble", "data-breathe", "data-awake"):
                    del el.attrib[k]
            st = el.get("style")
            if st:
                st2 = clean_declarations(st, vars_)
                if st2:
                    el.set("style", st2)
                else:
                    del el.attrib["style"]
        for img in body.iter("img"):
            href = self.resolve_ref(img.get("src") or "", self.base)
            if href:
                img.set("src", href)
                img.set("alt", img.get("alt") or "")
            else:
                img.drop_tree()

        # ids for headings (TOC + links)
        seen = set(x.get("id") for x in body.iter() if isinstance(x.tag, str) and x.get("id"))
        for h in body.iter("h2", "h3"):
            if not h.get("id"):
                base_id, i = slug(h.text_content()), 2
                hid = base_id
                while hid in seen:
                    hid = f"{base_id}-{i}"
                    i += 1
                h.set("id", hid)
                seen.add(hid)

        chunks = self.split(doc)
        self.write_chapters(chunks, svgs, vars_)
        self.write_cover()
        self.write_nav()
        self.write_opf()
        out = self.package()
        if not self.a.no_check:
            check_epub(out)
        return out

    # -- chapters
    def split(self, doc) -> list:
        body = doc.find("body")
        if self.a.split == "none":
            return [copy.deepcopy(body)]
        heads = [h for h in body.iter(self.a.split)]
        if len(heads) < 2:
            return [copy.deepcopy(body)]
        units = []
        for h in heads:  # climb while the parent holds only this heading
            u = h
            while u.getparent() is not body and len(list(u.getparent().iter(self.a.split))) == 1:
                u = u.getparent()
            units.append(u)
        parent = units[0].getparent()
        if any(u.getparent() is not parent for u in units):
            # mixed nesting: keep the units that share the most common parent
            from collections import Counter
            parent = Counter(u.getparent() for u in units).most_common(1)[0][0]
            units = [u for u in units if u.getparent() is parent]
            note(f"split at {len(units)} of {len(heads)} {self.a.split} headings (others are nested deeper)")
        tree = body.getroottree()
        ppath = tree.getpath(parent)
        kids = list(parent)
        idx = [kids.index(u) for u in units]
        bounds = [(0, idx[0])] + [(idx[i], idx[i + 1] if i + 1 < len(idx) else len(kids)) for i in range(len(idx))]
        chunks = []
        for n, (a, b) in enumerate(bounds):
            first, last = n == 0, n == len(bounds) - 1
            cdoc = copy.deepcopy(doc)
            ctree = cdoc.getroottree()
            cpar = ctree.xpath(ppath)[0]
            for i, kid in reversed(list(enumerate(list(cpar)))):
                if not (a <= i < b):
                    cpar.remove(kid)
            node = cpar
            cbody = cdoc.find("body")
            while node is not cbody:  # trim the wrappers' other children
                up = node.getparent()
                sibs = list(up)
                pos = sibs.index(node)
                for i, s in reversed(list(enumerate(sibs))):
                    if (i < pos and not first) or (i > pos and not last):
                        up.remove(s)
                node = up
            if len(cpar) and not first:
                head = cpar[0]
                head.set("class", ((head.get("class") or "") + " h3-epub-chapter-start").strip())
            if cbody.text_content().strip() or cbody.find(".//img") is not None or cbody.find(".//h3svg") is not None:
                chunks.append(cbody)
        return chunks

    def write_chapters(self, chunks, svgs, vars_):
        self.chapters = []  # (file, title, [(id, text, level)], has_svg)
        id_file = {}
        for n, body in enumerate(chunks, 1):
            fname = f"chapter-{n:02d}.xhtml"
            heads = [(h.get("id"), re.sub(r"\s+", " ", h.text_content()).strip(), int(h.tag[1]))
                     for h in body.iter("h1", "h2", "h3") if h.get("id") or h.tag != "h1"]
            for x in body.iter():
                if isinstance(x.tag, str) and x.get("id"):
                    id_file.setdefault(x.get("id"), fname)
            title = next((t for _, t, lvl in heads if lvl == 2), None) or (self.title if n == 1 else f"Part {n}")
            self.chapters.append([fname, title, [h for h in heads if h[0] and h[2] in (2, 3)], body])
        for ch in self.chapters:
            fname, title, heads, body = ch
            for a in body.iter("a"):
                href = a.get("href") or ""
                if href.startswith("#") and id_file.get(href[1:], fname) != fname:
                    a.set("href", id_file[href[1:]] + href)
            ch[3] = self.to_xhtml(body, title, svgs, vars_, fname)

    def to_xhtml(self, body, title, svgs, vars_, fname) -> bool:
        html_el = etree.Element(f"{{{XHTML_NS}}}html", nsmap={None: XHTML_NS, "epub": EPUB_NS})
        html_el.set("lang", self.lang)
        html_el.set("{http://www.w3.org/XML/1998/namespace}lang", self.lang)
        head = etree.SubElement(html_el, f"{{{XHTML_NS}}}head")
        etree.SubElement(head, f"{{{XHTML_NS}}}meta", charset="utf-8")
        t = etree.SubElement(head, f"{{{XHTML_NS}}}title")
        t.text = title
        etree.SubElement(head, f"{{{XHTML_NS}}}link", rel="stylesheet", type="text/css", href="css/book.css")
        b = copy.deepcopy(body)
        lhtml.html_to_xhtml(b)
        b.tag = f"{{{XHTML_NS}}}body"
        if body.get("class"):
            b.set("class", body.get("class"))
        html_el.append(b)
        has_svg = False
        for ph in list(html_el.iter(f"{{{XHTML_NS}}}h3svg")):
            el = svg_element(svgs[int(ph.get("data-i"))], vars_)
            el.tail = ph.tail
            ph.getparent().replace(ph, el)
            has_svg = True
        # attributes XHTML/EPUB reject
        for el in html_el.iter():
            if not isinstance(el.tag, str):
                continue
            for k in list(el.attrib):
                if ":" in k and not k.startswith("{"):
                    del el.attrib[k]
            if el.tag == f"{{{XHTML_NS}}}a" and el.get("target"):
                del el.attrib["target"]
        data = etree.tostring(html_el, encoding="utf-8", xml_declaration=True,
                              doctype="<!DOCTYPE html>", pretty_print=False)
        (self.build / "OEBPS" / fname).write_bytes(data)
        return has_svg

    # -- cover
    def write_cover(self):
        self.cover = None
        if self.a.cover:
            p = Path(self.a.cover)
            mime = mimetypes.guess_type(p.name)[0]
            self.cover = self.add_image_bytes(p.read_bytes(), mime, "cover")
            return
        if self.a.no_cover:
            return
        try:
            from PIL import Image, ImageDraw, ImageFont, features
        except ImportError:
            note("Pillow missing: no cover image")
            return
        W, H = 1600, 2560
        page, ink, muted, faint = (246, 246, 247), (23, 23, 26), (89, 90, 95), (138, 139, 144)
        img = Image.new("RGB", (W, H), page)
        d = ImageDraw.Draw(img)
        fonts = {f["family"].lower() + f["style"]: f["path"] for f in load_faces(self.design)
                 if f["path"].suffix == ".ttf"}
        disp = None if self.a.no_display_font else fonts.get("mrs eaves otitalic")
        body = fonts.get("internormal")
        raqm = features.check("raqm")
        feats = ["liga", "dlig", "calt"] if raqm else None
        layout = ImageFont.Layout.RAQM if raqm else ImageFont.Layout.BASIC

        def font(path, size):
            if path:
                return ImageFont.truetype(str(path), size, layout_engine=layout)
            for fb in ("DejaVuSerif-Italic.ttf", "DejaVuSans.ttf"):
                try:
                    return ImageFont.truetype(fb, size)
                except OSError:
                    pass
            return ImageFont.load_default()

        x = 150
        # mark: the PNG from the design skill when there is one
        mark = self.design / "assets" / "logo" / "h3nr7-mark-black.png"
        y = 170
        if mark.is_file():
            m = Image.open(mark).convert("RGBA")
            m.thumbnail((210, 260))
            img.paste(m, (x, y), m)
            y += m.size[1]
        else:
            d.text((x, y), "h3nr7", font=font(disp, 110), fill=muted, features=feats)
            y += 140
        y += 520
        lab = font(body, 34)
        label = (self.label or "Learning note").upper()
        cx = x
        for ch in label:  # tracked 0.08em by hand
            d.text((cx, y), ch, font=lab, fill=faint)
            cx += d.textlength(ch, font=lab) + 34 * 0.08
        y += 110
        size = 190
        tf = font(disp, size)
        words, lines, cur = self.title.split(), [], ""
        for w in words:
            t = (cur + " " + w).strip()
            if d.textlength(t, font=tf, features=feats) > W - 2 * x and cur:
                lines.append(cur)
                cur = w
            else:
                cur = t
        lines.append(cur)
        while len(lines) > 5 and size > 110:
            size -= 20
            tf = font(disp, size)
            lines, cur = [], ""
            for w in words:
                t = (cur + " " + w).strip()
                if d.textlength(t, font=tf, features=feats) > W - 2 * x and cur:
                    lines.append(cur)
                    cur = w
                else:
                    cur = t
            lines.append(cur)
        for line in lines:
            d.text((x, y), line, font=tf, fill=ink, features=feats)
            y += int(size * 0.98)
        y += 60
        d.rectangle([x, y, W - x, y + 2], fill=ink)
        y += 50
        d.text((x, y), self.a.author, font=font(body, 40), fill=muted)
        d.text((x, H - 200), "h3nr7.com", font=font(body, 34), fill=faint)
        name = "images/cover.jpg"
        img.save(self.build / "OEBPS" / name, quality=92)
        self.cover = name

    # -- navigation
    def write_nav(self):
        items = []
        for fname, title, heads, _ in self.chapters:
            subs = [h for h in heads if h[2] == 3]
            top = next((h for h in heads if h[2] == 2), None)
            link = f"{fname}#{top[0]}" if top else fname
            inner = "".join(f'<li><a href="{fname}#{i}">{htmllib.escape(t)}</a></li>' for i, t, _ in subs)
            items.append(f'<li><a href="{link}">{htmllib.escape(title)}</a>'
                         + (f"<ol>{inner}</ol>" if inner and self.a.toc_depth > 1 else "") + "</li>")
        nav = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="{XHTML_NS}" xmlns:epub="{EPUB_NS}" lang="{self.lang}" xml:lang="{self.lang}">
<head><meta charset="utf-8"/><title>Contents</title><link rel="stylesheet" type="text/css" href="css/book.css"/></head>
<body>
<nav epub:type="toc" id="toc"><p class="h3-label">Contents</p><ol>{''.join(items)}</ol></nav>
<nav epub:type="landmarks" hidden="hidden"><ol>
<li><a epub:type="bodymatter" href="{self.chapters[0][0]}">Start</a></li>
</ol></nav>
</body></html>"""
        (self.build / "OEBPS" / "nav.xhtml").write_text(nav, encoding="utf-8")
        points = "".join(
            f'<navPoint id="np{i}" playOrder="{i}"><navLabel><text>{htmllib.escape(t)}</text></navLabel>'
            f'<content src="{f}"/></navPoint>'
            for i, (f, t, _, _) in enumerate(self.chapters, 1))
        self.uid = "urn:uuid:" + str(uuid.uuid5(uuid.NAMESPACE_URL, f"h3nr7:{self.title}:{self.a.author}"))
        ncx = f"""<?xml version="1.0" encoding="utf-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
<head><meta name="dtb:uid" content="{self.uid}"/></head>
<docTitle><text>{htmllib.escape(self.title)}</text></docTitle>
<navMap>{points}</navMap></ncx>"""
        (self.build / "OEBPS" / "toc.ncx").write_text(ncx, encoding="utf-8")

    def write_opf(self):
        now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        man = ['<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>',
               '<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>',
               '<item id="css" href="css/book.css" media-type="text/css"/>']
        for i, f in enumerate(self.fonts):
            man.append(f'<item id="font{i}" href="{f}" media-type="{mimetypes.guess_type(f)[0]}"/>')
        for i, href in enumerate(sorted(set(self.images.values()) | ({self.cover} if self.cover else set()))):
            props = ' properties="cover-image"' if href == self.cover else ""
            man.append(f'<item id="img{i}" href="{href}" media-type="{mimetypes.guess_type(href)[0]}"{props}/>')
        spine = []
        for i, (f, _, _, has_svg) in enumerate(self.chapters, 1):
            man.append(f'<item id="c{i}" href="{f}" media-type="application/xhtml+xml"'
                       + (' properties="svg"' if has_svg else "") + "/>")
            spine.append(f'<itemref idref="c{i}"/>')
        cover_meta = ""
        if self.cover:
            cid = next(m.split('"')[1] for m in man if f'href="{self.cover}"' in m)
            cover_meta = f'<meta name="cover" content="{cid}"/>'
        opf = f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="uid" xml:lang="{self.lang}">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:identifier id="uid">{self.uid}</dc:identifier>
<dc:title>{htmllib.escape(self.title)}</dc:title>
<dc:creator>{htmllib.escape(self.a.author)}</dc:creator>
<dc:language>{self.lang}</dc:language>
<dc:publisher>h3nr7.com</dc:publisher>
<dc:date>{now[:10]}</dc:date>
<meta property="dcterms:modified">{now}</meta>
{cover_meta}
</metadata>
<manifest>
{chr(10).join(man)}
</manifest>
<spine toc="ncx">
{chr(10).join(spine)}
</spine>
</package>"""
        (self.build / "OEBPS" / "content.opf").write_text(opf, encoding="utf-8")
        (self.build / "META-INF" / "container.xml").write_text(
            '<?xml version="1.0" encoding="utf-8"?>\n<container version="1.0" '
            'xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles>'
            '<rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>'
            '</rootfiles></container>', encoding="utf-8")

    # -- zip
    def package(self) -> Path:
        out = Path(self.a.output or self.src.with_suffix(".epub")).resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
        obfuscate = self.fonts and not self.a.no_obfuscate
        key = hashlib.sha1(re.sub(r"[\x20\x09\x0d\x0a]", "", self.uid).encode()).digest()
        with zipfile.ZipFile(out, "w") as z:
            z.writestr(zipfile.ZipInfo("mimetype"), "application/epub+zip", compress_type=zipfile.ZIP_STORED)
            for p in sorted(self.build.rglob("*")):
                if p.is_dir():
                    continue
                rel = p.relative_to(self.build).as_posix()
                data = p.read_bytes()
                if obfuscate and rel.startswith("OEBPS/fonts/"):
                    data = bytes(b ^ key[i % 20] if i < 1040 else b for i, b in enumerate(data))
                z.writestr(rel, data, compress_type=zipfile.ZIP_DEFLATED)
            if obfuscate:
                refs = "".join(
                    '<enc:EncryptedData><enc:EncryptionMethod Algorithm="http://www.idpf.org/2008/embedding"/>'
                    f'<enc:CipherData><enc:CipherReference URI="OEBPS/{f}"/></enc:CipherData></enc:EncryptedData>'
                    for f in self.fonts)
                z.writestr("META-INF/encryption.xml",
                           '<?xml version="1.0" encoding="utf-8"?>\n<encryption '
                           'xmlns="urn:oasis:names:tc:opendocument:xmlns:container" '
                           f'xmlns:enc="http://www.w3.org/2001/04/xmlenc#">{refs}</encryption>',
                           compress_type=zipfile.ZIP_DEFLATED)
        return out


# ------------------------------------------------------------------- checking

def check_epub(path: Path) -> bool:
    """Structural check: zip layout, well-formed XML, manifest <-> files, links."""
    problems = []
    with zipfile.ZipFile(path) as z:
        infos = z.infolist()
        if infos[0].filename != "mimetype" or infos[0].compress_type != zipfile.ZIP_STORED:
            problems.append("mimetype must be the first entry, stored")
        names = set(z.namelist())
        for n in names:
            if n.endswith((".xhtml", ".opf", ".ncx", ".xml")):
                try:
                    etree.fromstring(z.read(n))
                except etree.XMLSyntaxError as e:
                    problems.append(f"{n}: not well-formed XML: {e}")
        opf = etree.fromstring(z.read("OEBPS/content.opf"))
        ns = {"o": "http://www.idpf.org/2007/opf"}
        hrefs = {i.get("href"): i for i in opf.findall(".//o:manifest/o:item", ns)}
        for h in hrefs:
            if f"OEBPS/{h}" not in names:
                problems.append(f"manifest lists a missing file: {h}")
        for n in names:
            if n.startswith("OEBPS/") and n not in ("OEBPS/content.opf",) and n[6:] not in hrefs:
                problems.append(f"file not in manifest: {n}")
        for h, item in hrefs.items():
            if not h.endswith(".xhtml"):
                continue
            x = etree.fromstring(z.read(f"OEBPS/{h}"))
            has_svg = x.find(f".//{{{SVG_NS}}}svg") is not None
            if has_svg != ("svg" in (item.get("properties") or "")) and h != "nav.xhtml":
                problems.append(f"{h}: svg property mismatch")
            for el in x.iter(f"{{{XHTML_NS}}}img"):
                if f"OEBPS/{el.get('src')}" not in names:
                    problems.append(f"{h}: missing image {el.get('src')}")
            for el in x.iter(f"{{{XHTML_NS}}}a"):
                href = el.get("href") or ""
                if href and not re.match(r"^(https?:|mailto:|#)", href):
                    if f"OEBPS/{href.split('#')[0]}" not in names:
                        problems.append(f"{h}: broken link {href}")
    if problems:
        print("EPUB check found problems:", file=sys.stderr)
        for p in problems:
            print(f"  ✗ {p}", file=sys.stderr)
        return False
    print(f"EPUB check passed: {path.name}", file=sys.stderr)
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", help="the HTML page (self-contained, or with local CSS/images)")
    ap.add_argument("-o", "--output", help="the .epub to write (default: next to the input)")
    ap.add_argument("--design", help="path to skills/h3nr7-design (found automatically when beside this skill)")
    ap.add_argument("--title", help="book title (default: the page's h1)")
    ap.add_argument("--author", default="Henry YP Ho")
    ap.add_argument("--lang", help="language tag (default: <html lang>, else en-GB)")
    ap.add_argument("--label", help="cover label line (default: the page's opening label)")
    ap.add_argument("--split", default="h2", choices=["h2", "h3", "none"], help="chapter boundary")
    ap.add_argument("--toc-depth", type=int, default=2, choices=[1, 2])
    ap.add_argument("--cover", help="use this image as the cover instead of drawing one")
    ap.add_argument("--no-cover", action="store_true")
    ap.add_argument("--no-display-font", action="store_true",
                    help="leave Mrs Eaves out (for a copy that goes to other people)")
    ap.add_argument("--no-obfuscate", action="store_true", help="store fonts unobfuscated")
    ap.add_argument("--keep-build", help="keep the unpacked book in this folder (for preview.py)")
    ap.add_argument("--no-check", action="store_true")
    a = ap.parse_args()
    out = Book(a).run()
    print(out)


if __name__ == "__main__":
    main()
