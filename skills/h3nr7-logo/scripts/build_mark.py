"""
Build the stacked h3r / n7 mark from Mrs Eaves OT Bold Italic, in code.

    python scripts/build_mark.py --font MrsEavesOT-BoldItalic.otf --out mark.svg
    python scripts/build_mark.py --font MrsEavesOT-BoldItalic.otf --check
    python scripts/build_mark.py --text --size 100            # live <text>, needs the font in the page

The mark is five lowercase glyphs - h 3 r over n 7 - set in Mrs Eaves OT Bold Italic at one
size and placed by hand. `assets/mark-layout.json` holds where each one goes, in em, so this
script (or any other code) can rebuild it at any size without the shipped SVG.

Outline mode (default) turns the glyphs into a path, so the result needs no font to display -
the right form for a logo file. It needs fontTools and the Bold Italic font file, which is NOT
bundled (only the regular Italic is, and its outlines are too narrow to reproduce the mark).
Text mode needs neither; it writes <text> elements and the page must load the font itself.

Requires: fonttools (outline mode only).
"""

import argparse
import json
import sys
from pathlib import Path

LAYOUT = Path(__file__).resolve().parent.parent / "assets" / "mark-layout.json"
TOLERANCE_EM = 0.003  # how far a glyph's outline box may drift from the recorded one in --check


def load_layout() -> dict:
    return json.loads(LAYOUT.read_text(encoding="utf-8"))


def n(v: float) -> str:
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def svg_doc(view: tuple[float, float, float, float], body: str, color: str, attrs: str = "") -> str:
    x, y, w, h = view
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{n(x)} {n(y)} {n(w)} {n(h)}" '
        f'width="{n(w)}" height="{n(h)}" role="img" aria-label="h3nr7"{attrs}>\n'
        f'<title>h3nr7</title>\n<g fill="{color}">\n{body}\n</g>\n</svg>\n'
    )


def text_svg(layout: dict, size: float, color: str) -> str:
    """Live <text>: exact placement, but the page must supply Mrs Eaves OT Bold Italic."""
    f = layout["font"]
    ink = layout["ink_em"]
    view = (ink["x"] * size, ink["y"] * size, ink["w"] * size, ink["h"] * size)
    style = (f' font-family="\'{f["family"]}\'" font-style="{f["style"]}" font-weight="{f["weight"]}"'
             f' font-size="{n(size)}" style="font-synthesis:none;font-kerning:none;font-variant-ligatures:none"')
    rows = "\n".join(
        f'<text x="{n(g["x"] * size)}" y="{n(g["y"] * size)}">{g["char"]}</text>' for g in layout["glyphs"]
    )
    return svg_doc(view, rows, color, style)


def open_font(path: str):
    from fontTools.ttLib import TTFont  # imported here so --text works without fontTools

    font = TTFont(path)
    names = {r.nameID: r.toUnicode() for r in font["name"].names if r.nameID in (1, 2, 4, 16, 17)}
    label = names.get(4) or f"{names.get(1, '?')} {names.get(2, '')}"
    mac = font["head"].macStyle
    if not (mac & 1 and mac & 2):
        print(f"warning: {label!r} is not flagged Bold Italic; the mark will not match.", file=sys.stderr)
    return font, label


def outlines(font, layout: dict, size: float):
    """Yield (char, path data, (xmin, ymin, xmax, ymax)) per glyph, in SVG space (y down), origin at the h."""
    from fontTools.pens.boundsPen import BoundsPen
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen

    gs, cmap = font.getGlyphSet(), font.getBestCmap()
    s = size / font["head"].unitsPerEm
    for g in layout["glyphs"]:
        name = cmap[ord(g["char"])]
        m = (s, 0, 0, -s, g["x"] * size, g["y"] * size)  # flip y, scale to size, move to this glyph's origin
        path = SVGPathPen(gs, ntos=lambda v: f"{v:.2f}".rstrip("0").rstrip("."))
        gs[name].draw(TransformPen(path, m))
        box = BoundsPen(gs)
        gs[name].draw(TransformPen(box, m))
        yield g["char"], path.getCommands(), box.bounds


def outline_svg(font, layout: dict, size: float, color: str) -> str:
    parts, boxes = [], []
    for _, d, b in outlines(font, layout, size):
        parts.append(f'<path d="{d}"/>')
        boxes.append(b)
    x0, y0 = min(b[0] for b in boxes), min(b[1] for b in boxes)
    x1, y1 = max(b[2] for b in boxes), max(b[3] for b in boxes)
    return svg_doc((x0, y0, x1 - x0, y1 - y0), "\n".join(parts), color)


def check(font, layout: dict) -> bool:
    """Compare each glyph's own outline box with the one recorded from the shipped mark."""
    from fontTools.pens.boundsPen import BoundsPen

    gs, cmap, upm = font.getGlyphSet(), font.getBestCmap(), font["head"].unitsPerEm
    ok = True
    for g in layout["glyphs"]:
        bp = BoundsPen(gs)
        gs[cmap[ord(g["char"])]].draw(bp)
        got = [v / upm for v in bp.bounds]
        worst = max(abs(a - b) for a, b in zip(got, g["bbox_em"]))
        flag = "ok " if worst <= TOLERANCE_EM else "BAD"
        ok &= worst <= TOLERANCE_EM
        print(f"  {flag} {g['char']}  worst edge drift {worst:.4f} em")
    return ok


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--font", help="Mrs Eaves OT Bold Italic (.otf/.ttf); needed for outlines and --check")
    ap.add_argument("--size", type=float, default=100, help="font size in SVG units (default 100)")
    ap.add_argument("--color", default="currentColor", help="fill (default currentColor)")
    ap.add_argument("--text", action="store_true", help="write live <text> instead of outlines")
    ap.add_argument("--check", action="store_true", help="verify the font against the recorded glyph boxes")
    ap.add_argument("--out", help="write here instead of stdout")
    args = ap.parse_args()

    layout = load_layout()
    if args.text and not args.check:
        svg = text_svg(layout, args.size, args.color)
    else:
        if not args.font:
            sys.exit("--font is required (Mrs Eaves OT Bold Italic). Use --text for a live-text version.")
        font, label = open_font(args.font)
        if args.check:
            print(f"{label}:")
            sys.exit(0 if check(font, layout) else 1)
        svg = outline_svg(font, layout, args.size, args.color)

    if args.out:
        Path(args.out).write_text(svg, encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        sys.stdout.write(svg)


if __name__ == "__main__":
    main()
