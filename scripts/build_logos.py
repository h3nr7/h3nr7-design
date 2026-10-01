"""
Rebuild the logo set in skills/h3nr7-design/assets/logo from the Illustrator master.

    python scripts/build_logos.py ../h3nr7-design.ai

The master (`h3nr7-design.ai`, kept beside the h3nr7 repos rather than in this
one) is PDF-compatible and carries two 1080 x 1080 artboards: the stacked
"h3r / n7" wordmark in Mrs Eaves OT Bold Italic, black on white and white on
black. Its text is still live type, so PyMuPDF is asked to emit glyph OUTLINES
(`text_as_path=True`) — the SVGs produced here need no font to render, which is
the whole point of a logo file and also why shipping them is not shipping the
face.

Everything is derived from the first artboard's glyph geometry; the second only
confirms the colours. Requires: pymupdf, pillow.
"""

import re
import sys
from io import BytesIO
from pathlib import Path

import pymupdf
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "skills" / "h3nr7-design" / "assets" / "logo"
ART = 1080  # artboard size in points, and so in SVG user units
SCALE = 4  # raster oversampling used only to measure the ink's tight box

# The site's ink and page tokens. The master is pure #000/#fff; the PNG/SVG
# "black"/"white" files keep the master's values, and `currentColor` is the
# variant meant for anything that should follow the theme instead.
BLACK, WHITE = "#000000", "#ffffff"


def glyphs(svg: str) -> list[str]:
    """`<use>` + `<defs>` flattened to one `<path transform d>` per glyph."""
    defs = dict(re.findall(r'<path id="([^"]+)" d="([^"]+)"/>', svg))
    uses = re.findall(r'<use data-text="[^"]*" xlink:href="#([^"]+)" transform="([^"]+)"', svg)
    return [f'<path transform="{t}" d="{defs[ref]}"/>' for ref, t in uses]


def ink_box(page: pymupdf.Page) -> tuple[float, float, float, float]:
    """Tight box of the glyphs in artboard units, measured from a transparent render."""
    pix = page.get_pixmap(matrix=pymupdf.Matrix(SCALE, SCALE), alpha=True)
    alpha = Image.open(BytesIO(pix.tobytes("png"))).getchannel("A")
    l, t, r, b = alpha.getbbox()
    return l / SCALE, t / SCALE, r / SCALE, b / SCALE


def svg_doc(view: str, body: str, w: float, h: float, title: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view}" '
        f'width="{w:g}" height="{h:g}" role="img" aria-label="{title}">\n'
        f"<title>{title}</title>\n{body}\n</svg>\n"
    )


def main(ai_path: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    doc = pymupdf.open(ai_path)
    page = doc[0]
    paths = "\n".join(glyphs(page.get_svg_image(text_as_path=True)))

    l, t, r, b = ink_box(page)
    w, h = r - l, b - t
    tight = f"{l:.2f} {t:.2f} {w:.2f} {h:.2f}"
    print(f"ink box {tight}  ({w / ART:.1%} x {h / ART:.1%} of the artboard)")

    files = {
        # Tight to the ink: the caller supplies clear space.
        "h3nr7-mark.svg": svg_doc(tight, f'<g fill="currentColor">\n{paths}\n</g>', round(w), round(h), "h3nr7"),
        "h3nr7-mark-black.svg": svg_doc(tight, f'<g fill="{BLACK}">\n{paths}\n</g>', round(w), round(h), "h3nr7"),
        "h3nr7-mark-white.svg": svg_doc(tight, f'<g fill="{WHITE}">\n{paths}\n</g>', round(w), round(h), "h3nr7"),
        # The master artboards, margins and all.
        "h3nr7-tile-dark.svg": svg_doc(
            f"0 0 {ART} {ART}",
            f'<rect width="{ART}" height="{ART}" fill="{BLACK}"/>\n<g fill="{WHITE}">\n{paths}\n</g>',
            ART, ART, "h3nr7",
        ),
        "h3nr7-tile-light.svg": svg_doc(
            f"0 0 {ART} {ART}",
            f'<rect width="{ART}" height="{ART}" fill="{WHITE}"/>\n<g fill="{BLACK}">\n{paths}\n</g>',
            ART, ART, "h3nr7",
        ),
        # The favicon's diagonal: the bottom-right half of a square. Drawn
        # rather than traced — it is one triangle, and the 32px PNG it comes
        # from is anti-aliased along exactly the edge that matters.
        "h3nr7-glyph.svg": svg_doc("0 0 32 32", '<path fill="currentColor" d="M32 0V32H0Z"/>', 32, 32, "h3nr7"),
    }
    for name, text in files.items():
        (OUT / name).write_text(text, encoding="utf-8", newline="\n")

    # Rasters, for the places SVG cannot go: Office files, social cards, avatars.
    for idx, name, colour in ((1, "h3nr7-tile-dark", WHITE), (0, "h3nr7-tile-light", BLACK)):
        doc[idx].get_pixmap(matrix=pymupdf.Matrix(1, 1), alpha=False).save(OUT / f"{name}.png")

    # Transparent, tight, 1200px tall: black from the render, white by recolouring it.
    zoom = 1200 / h
    clip = pymupdf.Rect(l, t, r, b)
    pix = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), clip=clip, alpha=True)
    black = Image.open(BytesIO(pix.tobytes("png"))).convert("RGBA")
    black.save(OUT / "h3nr7-mark-black.png", optimize=True)
    white = Image.new("RGBA", black.size, (255, 255, 255, 0))
    white.putalpha(black.getchannel("A"))
    white.save(OUT / "h3nr7-mark-white.png", optimize=True)

    glyph = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    tri = Image.new("L", (512, 512), 0)
    from PIL import ImageDraw  # local: only this raster needs it

    ImageDraw.Draw(tri).polygon([(512, 0), (512, 512), (0, 512)], fill=255)
    glyph.paste((23, 23, 26, 255), mask=tri)
    glyph.save(OUT / "h3nr7-glyph.png", optimize=True)

    for f in sorted(OUT.iterdir()):
        print(f"  {f.name:28} {f.stat().st_size:>8} bytes")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
