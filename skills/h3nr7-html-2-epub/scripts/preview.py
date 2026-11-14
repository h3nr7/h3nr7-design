#!/usr/bin/env python3
"""
Screenshot an unpacked EPUB (html2epub.py --keep-build DIR) the way a reader
shows it: a narrow page, reader margins, the book's own CSS and fonts.

    python scripts/preview.py build/ -o shots/            # every chapter + the cover
    python scripts/preview.py build/ -o shots/ --width 600 --height 960 --dark

Needs a headless Chrome or Chromium on PATH. Writes one PNG per chapter
(the top --height pixels of it) and prints their paths. Look at them.
--dark previews a reader's night mode by inverting, which is roughly what
Apple Books and Kobo do to a page that sets its own colours.
"""

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def chrome() -> str:
    for c in ("google-chrome", "chromium", "chromium-browser", "chrome", "google-chrome-stable"):
        if shutil.which(c):
            return shutil.which(c)
    sys.exit("No headless Chrome/Chromium found: open the .epub in Apple Books or Thorium instead.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("build", help="folder written by html2epub.py --keep-build")
    ap.add_argument("-o", "--out", default="epub-preview")
    ap.add_argument("--width", type=int, default=600)
    ap.add_argument("--height", type=int, default=960)
    ap.add_argument("--margin", type=int, default=36, help="reader margin in CSS px")
    ap.add_argument("--dark", action="store_true")
    a = ap.parse_args()
    oebps = Path(a.build).resolve() / "OEBPS"
    out = Path(a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    exe = chrome()
    tmp = Path(tempfile.mkdtemp(prefix="h3prev-", dir=oebps))
    shots = []
    for xf in sorted(oebps.glob("chapter-*.xhtml")):
        src = xf.read_text(encoding="utf-8")
        inject = (f"<style>html{{background:#f6f6f7}} body{{padding:{a.margin}px {a.margin}px !important}}"
                  + ("html{filter:invert(1) hue-rotate(180deg)} img{filter:invert(1) hue-rotate(180deg)}" if a.dark else "")
                  + "</style>")
        page = tmp / xf.name
        page.write_text(src.replace('href="css/', 'href="../css/').replace('src="images/', 'src="../images/')
                        .replace("</head>", inject + "</head>"), encoding="utf-8")
        png = out / (xf.stem + (".dark" if a.dark else "") + ".png")
        subprocess.run([exe, "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
                        "--allow-file-access-from-files", f"--window-size={a.width},{a.height}",
                        f"--screenshot={png}", "--virtual-time-budget=3000", page.as_uri()],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        shots.append(png)
    cover = oebps / "images" / "cover.jpg"
    if cover.is_file():
        shutil.copy(cover, out / "cover.jpg")
        shots.append(out / "cover.jpg")
    shutil.rmtree(tmp, ignore_errors=True)
    print("\n".join(str(s) for s in shots))


if __name__ == "__main__":
    main()
