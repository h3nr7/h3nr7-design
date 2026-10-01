#!/usr/bin/env python3
"""
Make an HTML file self-contained: inline its local stylesheets, scripts and
images, and embed the bundled fonts as base64 @font-face rules.

    python scripts/inline.py page.html            # rewrites page.html in place
    python scripts/inline.py page.html -o out.html
    python scripts/inline.py page.html --no-fonts
    python scripts/inline.py page.html --family 'Mrs Eaves OT' --family Inter

Write the page against the skill's files by path, e.g.

    <link rel="stylesheet" href="/path/to/h3nr7-design/assets/h3nr7.css">
    <script src="/path/to/h3nr7-design/assets/h3-scramble.js"></script>
    <img src="/path/to/h3nr7-design/assets/logo/h3nr7-mark.svg" alt="h3nr7">

then run this. Relative paths resolve against the HTML file; absolute paths
are used as they are; http(s) and data: URLs are left alone.

Why it exists: Claude artifacts and most document viewers block external
fonts, and h3nr7.com's Adobe Fonts kit only serves h3nr7.com. So the brand
faces travel inside the file instead: every face listed in assets/fonts/
fonts.json (Mrs Eaves, Inter at its 18pt optical size) is embedded under the
family name the h3nr7.css stacks already ask for, and nothing else in the
page changes. Faces whose files are absent are skipped with a note.
Standard library only.
"""

import argparse
import base64
import json
import mimetypes
import re
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
FONTS = SKILL / "assets" / "fonts"

MANIFEST = FONTS / "fonts.json"  # written by the repo's scripts/build_fonts.py

mimetypes.add_type("image/svg+xml", ".svg")
mimetypes.add_type("image/webp", ".webp")
mimetypes.add_type("font/woff2", ".woff2")


def resolve(ref: str, base: Path) -> Path | None:
    if re.match(r"^(https?:|data:|//|#|mailto:)", ref):
        return None
    p = Path(ref)
    if not p.is_absolute():
        p = (base / ref).resolve()
    return p if p.is_file() else None


def data_uri(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"


def font_faces(families: set[str] | None) -> tuple[str, int]:
    """One @font-face per face in the manifest, under the family name the CSS stacks ask for."""
    faces = json.loads(MANIFEST.read_text(encoding="utf-8"))["faces"] if MANIFEST.is_file() else []
    rules = []
    for f in faces:
        if families and f["family"] not in families:
            continue
        path = FONTS / f["file"]
        if not path.is_file():
            print(f"  font missing, skipped: {f['file']}", file=sys.stderr)
            continue
        rules.append(
            f"@font-face{{font-family:'{f['family']}';font-style:{f['style']};font-weight:{f['weight']};"
            f"font-display:swap;src:url({data_uri(path)}) format('woff2');}}"
        )
    return "<style>/* h3nr7-design fonts, see SKILL.md */\n" + "\n".join(rules) + "\n</style>", len(rules)


def inline(html: str, base: Path, fonts: bool, families: set[str] | None = None) -> tuple[str, list[str]]:
    done: list[str] = []

    def css(m: re.Match) -> str:
        p = resolve(m.group("href"), base)
        if not p:
            return m.group(0)
        done.append(f"css    {p.name}")
        return f"<style>\n{p.read_text(encoding='utf-8')}\n</style>"

    def js(m: re.Match) -> str:
        p = resolve(m.group("src"), base)
        if not p:
            return m.group(0)
        done.append(f"js     {p.name}")
        return f"<script>\n{p.read_text(encoding='utf-8')}\n</script>"

    def asset(m: re.Match) -> str:
        p = resolve(m.group("url"), base)
        if not p:
            return m.group(0)
        done.append(f"asset  {p.name}")
        return f'{m.group("attr")}="{data_uri(p)}"'

    html = re.sub(r'<link\b[^>]*\brel=["\']stylesheet["\'][^>]*\bhref=["\'](?P<href>[^"\']+)["\'][^>]*>', css, html)
    html = re.sub(r'<link\b[^>]*\bhref=["\'](?P<href>[^"\']+\.css)["\'][^>]*\brel=["\']stylesheet["\'][^>]*>', css, html)
    html = re.sub(r'<script\b[^>]*\bsrc=["\'](?P<src>[^"\']+)["\'][^>]*>\s*</script>', js, html)
    # `src`/`poster` anywhere; `href` only on an icon <link> — an <a href> to a
    # picture is a link to it, not a picture, and must stay a URL.
    pattern = r'(?P<attr>\b(?:src|poster))=["\'](?P<url>[^"\']+\.(?:svg|png|jpe?g|webp|gif|ico))["\']'
    html = re.sub(pattern, asset, html)
    html = re.sub(
        r'<link\b[^>]*\brel=["\'][^"\']*icon[^"\']*["\'][^>]*>',
        lambda m: re.sub(r'(?P<attr>\bhref)=["\'](?P<url>[^"\']+)["\']', asset, m.group(0)),
        html,
    )

    if fonts:
        faces, count = font_faces(families)
        if re.search(r"<head[^>]*>", html):
            html = re.sub(r"(<head[^>]*>)", lambda m: m.group(1) + "\n" + faces, html, count=1)
        else:
            html = faces + "\n" + html
        done.append(f"fonts  {count} faces")
    return html, done


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("html", type=Path)
    ap.add_argument("-o", "--out", type=Path)
    ap.add_argument("--no-fonts", action="store_true", help="skip the base64 @font-face block")
    ap.add_argument("--family", action="append", help="embed only this family (repeatable), e.g. --family Inter")
    args = ap.parse_args()

    src = args.html.resolve()
    families = set(args.family) if args.family else None
    out_html, done = inline(src.read_text(encoding="utf-8"), src.parent, not args.no_fonts, families)
    dst = (args.out or src).resolve()
    dst.write_text(out_html, encoding="utf-8")
    for line in done:
        print("  " + line)
    print(f"wrote {dst} ({dst.stat().st_size // 1024} KB)")
    leftovers = re.findall(r'\bsrc=["\'](?!https?:|data:|//)([^"\']+)["\']', out_html)
    leftovers += re.findall(r'<link\b[^>]*\bhref=["\'](?!https?:|data:|//)([^"\']+\.css)["\']', out_html)
    if leftovers:
        print("not found, left as-is: " + ", ".join(sorted(set(leftovers))), file=sys.stderr)


if __name__ == "__main__":
    main()
