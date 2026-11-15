#!/usr/bin/env python3
"""
Check a tech doc's body against the rules in SKILL.md ("Tech docs"), so a page
that would be refused for publishing is caught while it is still being built.

    python scripts/check_techdoc.py page.html
    python scripts/check_techdoc.py page.html --css path/to/techdoc.css

The body is the element with class h3-doc-content. Exit 0: it passes (warnings
may be printed). Exit 1: it does not, and every problem is named. Exit 2: the
file could not be read. Works on a page written against the skill's files and
on one already inlined by inline.py. Standard library only.

The rules. h3nr7.com's push script applies the same list to the same body; the
two are separate implementations of one list, so a change to one is a change
to both. Kept side by side:

    rule                                      here    push script
    a .h3-doc-content element                 error   error
    classes: only those techdoc.css defines   error   error (the site's copy)
    <style>, style="…"                        error   error
    script iframe foreignObject use           error   error
    any other element outside the allowlist   error   error
    on…= attributes                           error   error
    attributes outside the allowlist          error   error
    fill stroke opacity font-* attributes     error   error
    a href: http https mailto # or /path      error   error
    marker-*: url(#id) only                   error   error
    h1                                        error   error
    root svg without viewBox / aria-label     error   error
    img not a child of figure.h3-doc-figure   error   error
    img without alt text                      error   error
    img from http(s)                          error   error
    img not PNG JPEG WebP GIF                 error   error
    img over 2 MB                             warning warning
    body over 45,000 characters               warning warning
    body over 50,000 characters               error   error
    (an image's tag counts as 400 characters: the length of the tag the push
    script writes in its place, so image data never counts)
"""

from __future__ import annotations

import argparse
import base64
import re
import sys
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
TECHDOC_CSS = SKILL / "assets" / "techdoc.css"

HTML_ELEMENTS = set(
    "div section p h2 h3 h4 ul ol li dl dt dd blockquote figure figcaption table thead "
    "tbody tr th td pre code strong em a br hr span img".split())
SVG_ELEMENTS = set(
    "svg g defs marker path rect circle ellipse line polyline polygon text tspan title "
    "desc".split())
ALWAYS_ERROR = {"script", "style", "iframe", "foreignobject", "use", "h1"}

COMMON_ATTRS = {"class", "id"}
SVG_ATTRS = {
    "viewbox", "role", "aria-label", "aria-hidden", "xmlns",
    "x", "y", "x1", "y1", "x2", "y2", "cx", "cy", "r", "rx", "ry", "width", "height", "d",
    "points", "transform", "dx", "dy", "text-anchor", "dominant-baseline",
    "markerwidth", "markerheight", "markerunits", "refx", "refy", "orient",
    "marker-start", "marker-mid", "marker-end",
}
CELL_ATTRS = {"colspan", "rowspan", "scope"}
IMG_ATTRS = {"src", "srcset", "sizes", "width", "height", "alt", "loading", "decoding"}
PRESENTATION = re.compile(r"^(fill|stroke|opacity|font|color$)")
RASTER = {"image/png", "image/jpeg", "image/webp", "image/gif"}
RASTER_EXT = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
              ".webp": "image/webp", ".gif": "image/gif"}
IMG_STAND_IN = 400
LIMIT, WARN_AT = 50_000, 45_000
VOID = {"br", "hr", "img", "meta", "link", "input", "source", "area", "base", "col",
        "embed", "param", "track", "wbr"}


def css_classes(css: str) -> set[str]:
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\{[^{}]*\}", "{}", css)  # selectors only: no '.6' from a declaration
    return set(re.findall(r"\.(-?[A-Za-z_][\w-]*)", css))


class Checker(HTMLParser):
    def __init__(self, allowed: set[str], base: Path, root=lambda tag, classes: "h3-doc-content" in classes):
        super().__init__(convert_charrefs=True)
        self.allowed, self.base, self.root = allowed, base, root
        self.stack: list[tuple[str, set[str]]] = []   # open elements: (tag, classes)
        self.depth = None                              # stack depth of the body, when inside
        self.found = False
        self.errors: dict[str, list[int]] = defaultdict(list)
        self.warnings: dict[str, list[int]] = defaultdict(list)
        self.span = [None, None]                       # body (start, end) as (line, col)
        self.img_tags: list[tuple[tuple[int, int], str]] = []

    def err(self, msg):
        self.errors[msg].append(self.getpos()[0])

    def warn(self, msg):
        self.warnings[msg].append(self.getpos()[0])

    def handle_starttag(self, tag, attrs):
        self._start(tag, attrs, self.get_starttag_text() or "")
        if tag in VOID:
            self.handle_endtag(tag)

    def handle_startendtag(self, tag, attrs):
        self._start(tag, attrs, self.get_starttag_text() or "")
        self.handle_endtag(tag)

    def _start(self, tag, attrs, raw):
        a = {k.lower(): (v or "") for k, v in attrs}
        classes = set(a.get("class", "").split())
        if self.depth is None:
            if self.root(tag, classes) and not self.found:
                self.found = True
                self.depth = len(self.stack)
                self.span[0] = self.getpos()
            self.stack.append((tag, classes))
            return
        self._check(tag, a, classes, raw)
        self.stack.append((tag, classes))

    def handle_endtag(self, tag):
        # pop to the matching open element; HTML lets some end tags be left out
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break
        if self.depth is not None and len(self.stack) <= self.depth:
            self.depth = None
            self.span[1] = self.getpos()

    def _check(self, tag, a, classes, raw):
        in_svg = any(t == "svg" for t, _ in self.stack[self.depth:])
        if tag in ALWAYS_ERROR:
            self.err(f"<{tag}> is not allowed in the body")
        elif tag not in (SVG_ELEMENTS if in_svg or tag == "svg" else HTML_ELEMENTS):
            self.err(f"<{tag}> is not in the allowed elements")

        for c in sorted(classes - self.allowed):
            self.err(f"class '{c}' is not defined in techdoc.css")

        allowed_attrs = set(COMMON_ATTRS)
        if tag == "svg" or in_svg:
            allowed_attrs |= SVG_ATTRS
        if tag in ("th", "td"):
            allowed_attrs |= CELL_ATTRS
        if tag == "a":
            allowed_attrs |= {"href", "target", "rel"}
        if tag == "img":
            allowed_attrs |= IMG_ATTRS
        for k, v in a.items():
            if k == "style":
                self.err("style attribute: use techdoc.css classes")
            elif k.startswith("on"):
                self.err(f"{k}= event attribute")
            elif PRESENTATION.match(k):
                self.err(f"{k}= presentation attribute on <{tag}>: draw with the .h3-d-* classes")
            elif k not in allowed_attrs:
                self.err(f"{k}= is not an allowed attribute on <{tag}>")
            elif k.startswith("marker-") and not re.fullmatch(r"url\(#[\w-]+\)", v.strip()):
                self.err(f"{k}= must be url(#id)")
        if tag == "a" and "href" in a:
            href = a["href"].strip()
            if not (re.match(r"(?i)(https?:|mailto:)", href) or href.startswith("#")
                    or (href.startswith("/") and not href.startswith("//"))):
                self.err(f"link href '{href[:40]}' is not http, https, mailto, # or a site path")

        if tag == "svg" and not in_svg:
            if not a.get("viewbox"):
                self.err("root <svg> has no viewBox")
            if not a.get("aria-label", "").strip():
                self.err("root <svg> has no aria-label")

        if tag == "img":
            self.img_tags.append((self.getpos(), raw))
            parent_tag, parent_classes = self.stack[-1]
            if not (parent_tag == "figure" and "h3-doc-figure" in parent_classes):
                self.err("<img> outside a figure.h3-doc-figure")
            if not a.get("alt", "").strip():
                self.err("<img> without alt text")
            self._check_src(a.get("src", ""))

    def _check_src(self, src):
        src = src.strip()
        if not src:
            self.err("<img> without src")
        elif re.match(r"(?i)(https?:)?//", src):
            self.err(f"<img> from the web ({src[:50]}): use a local file, embedded by inline.py")
        elif src.lower().startswith("data:"):
            m = re.match(r"(?i)data:([\w/+.-]+)?(;base64)?,", src)
            mime = (m.group(1) or "").lower() if m else ""
            if mime not in RASTER:
                self.err(f"<img> of type '{mime or '?'}': PNG, JPEG, WebP or GIF only")
            elif m and m.group(2):
                size = len(base64.b64decode(src[m.end():] + "==", validate=False))
                if size > 2 * 1024 * 1024:
                    self.warn(f"<img> is {size / 1048576:.1f} MB: over 2 MB")
        else:
            path = (self.base / src.split("?")[0]).resolve()
            mime = RASTER_EXT.get(path.suffix.lower())
            if not mime:
                self.err(f"<img> '{src}': PNG, JPEG, WebP or GIF only")
            elif not path.is_file():
                self.err(f"<img> '{src}' not found")
            elif path.stat().st_size > 2 * 1024 * 1024:
                self.warn(f"<img> '{src}' is over 2 MB")


def offset(lines_start: list[int], pos) -> int:
    line, col = pos
    return lines_start[line - 1] + col


def body_length(src: str, ch: Checker) -> int:
    starts = [0]
    for line in src.splitlines(keepends=True):
        starts.append(starts[-1] + len(line))
    a = offset(starts, ch.span[0])
    if ch.span[1] is None:
        b = len(src)
    else:
        b = offset(starts, ch.span[1])
        b = src.index(">", b) + 1  # through the end tag
    n = b - a
    for pos, raw in ch.img_tags:
        n += IMG_STAND_IN - len(raw)
    return n


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[1].strip())
    ap.add_argument("page", type=Path)
    ap.add_argument("--css", type=Path, default=TECHDOC_CSS,
                    help="the techdoc.css whose classes are allowed (default: the skill's)")
    a = ap.parse_args()
    try:
        src = a.page.read_text(encoding="utf-8")
        allowed = css_classes(a.css.read_text(encoding="utf-8"))
    except OSError as e:
        print(f"check_techdoc: {e}", file=sys.stderr)
        return 2

    base = a.page.resolve().parent
    ch = Checker(allowed, base)
    ch.feed(src)
    ch.close()
    if not ch.found:
        # Still say what else would be refused: check <main>, else <body>, as if it were
        # the body. Its opening is reported too, since it has nowhere else to go.
        for tag in ("main", "body"):
            fb = Checker(allowed, base, root=lambda t, _c, tag=tag: t == tag)
            fb.feed(src)
            fb.close()
            if fb.found:
                print(f"no .h3-doc-content: checked <{tag}> instead")
                ch = fb
                break
        ch.found = False
        ch.errors["no element with class h3-doc-content: wrap the body in "
                  "<div class=\"h3-doc-content\">"].append(1)
    else:
        n = body_length(src, ch)
        if n > LIMIT:
            ch.errors[f"body is {n:,} characters: the limit is {LIMIT:,}"].append(ch.span[0][0])
        elif n > WARN_AT:
            ch.warnings[f"body is {n:,} characters: close to the {LIMIT:,} limit"].append(ch.span[0][0])

    def report(kind, items):
        for msg, lines in sorted(items.items(), key=lambda kv: kv[1][0]):
            where = f"line {lines[0]}" + (f", {len(lines)} times" if len(lines) > 1 else "")
            print(f"{kind}: {msg} ({where})")

    report("error", ch.errors)
    report("warning", ch.warnings)
    if ch.found:
        print(f"body: {body_length(src, ch):,} characters, {len(ch.img_tags)} image(s)")
    print(f"{a.page.name}: " + ("refused" if ch.errors else "passes"))
    return 1 if ch.errors else 0


if __name__ == "__main__":
    sys.exit(main())
