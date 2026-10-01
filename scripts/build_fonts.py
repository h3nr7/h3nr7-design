"""
Rebuild the bundled fonts in skills/h3nr7-design/assets/fonts and their manifest.

    python scripts/build_fonts.py                 # Mrs Eaves from source/fonts, Inter as already built
    python scripts/build_fonts.py --inter DIR     # also rebuild Inter from google/fonts variable TTFs

The two faces of h3nr7.com, which the site itself loads from an Adobe Fonts kit that only
serves its own domains:

- **Mrs Eaves** (Emigre, commercial). Henry's own files, dropped into `source/fonts/`.
  Copied unmodified — no subsetting, no renaming inside the font — plus a WOFF2 of each for
  `scripts/inline.py`, which is a format change only. Every Mrs Eaves file, here and in the
  skill, is .gitignored: the skill ZIP built on this machine carries them, the repo does not.
- **Inter** (OFL), pinned to the 18pt optical size the kit serves as `inter-18pt`, as static
  Latin-subset instances: Pillow and python-pptx/docx want one file per style, and a base64
  @font-face should cost tens of KB, not a megabyte. Expects, from github.com/google/fonts
  (ofl/inter): `Inter[opsz,wght].ttf`, `Inter-Italic[opsz,wght].ttf`, `OFL.txt`
  (or `inter-OFL.txt`).

`fonts.json` lists every face with the CSS family, style and weight it should be registered
under; `inline.py` reads it and skips any file that is missing. Requires: fonttools, brotli.
"""

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "skills" / "h3nr7-design" / "assets" / "fonts"
SOURCE = ROOT / "source" / "fonts"

# Basic Latin, Latin-1, Latin Extended-A, general punctuation, euro, trademark, arrows, minus.
UNICODES = "U+0020-007E,U+00A0-017F,U+2000-206F,U+20AC,U+2122,U+2190-2193,U+2212"

INTER = [
    ("Inter[opsz,wght].ttf", "Inter-Regular.ttf", {"opsz": 18, "wght": 400}, "normal", 400),
    ("Inter[opsz,wght].ttf", "Inter-SemiBold.ttf", {"opsz": 18, "wght": 600}, "normal", 600),
    ("Inter-Italic[opsz,wght].ttf", "Inter-Italic.ttf", {"opsz": 18, "wght": 400}, "italic", 400),
]


def woff2(src: Path, dst: Path) -> None:
    font = TTFont(src)
    font.flavor = "woff2"
    font.save(dst)


def web_woff2(src: Path, dst: Path) -> None:
    """A WOFF2 that browsers will actually load, for a CFF-flavoured (OTTO) face.

    Measured, not assumed: Chrome's font sanitiser (OTS) rejects the 1996 Emigre Mrs Eaves OT
    Italic with "CFF : Failed to parse Top DICT Data" — both the foundry's own Web Fonts WOFF2
    and a plain re-wrap of the desktop file — and a rejected @font-face fails silently, so the
    page just falls back to Times. Decompiling the CFF and letting fontTools write it back, and
    dropping DSIG (a signature over bytes that no longer exist), produces a file OTS accepts.
    Outlines stay CFF and GSUB/GPOS are untouched, so every glyph and ligature is preserved.
    """
    font = TTFont(src)
    if "CFF " in font:
        cff = font["CFF "].cff
        for top in cff.topDictIndex:
            for name in top.CharStrings.keys():
                top.CharStrings[name].decompile()
    if "DSIG" in font:
        del font["DSIG"]
    font.flavor = "woff2"
    font.save(dst)


def build_inter(src: Path) -> None:
    for source, output, location, _, _ in INTER:
        # A suffix match, not a glob: the `[wght]` in these names IS glob syntax.
        found = [p for p in src.iterdir() if p.name.endswith(source)]
        if not found:
            sys.exit(f"missing {source} in {src}")
        font = instancer.instantiateVariableFont(TTFont(found[0]), location, updateFontNames=True)
        opts = subset.Options()
        opts.layout_features = ["*"]
        opts.name_IDs = ["*"]
        opts.name_languages = ["*"]
        opts.notdef_outline = True
        sub = subset.Subsetter(opts)
        sub.populate(unicodes=subset.parse_unicodes(UNICODES))
        sub.subset(font)
        font.save(OUT / output)
        woff2(OUT / output, (OUT / output).with_suffix(".woff2"))
        print(f"  {output:34} {location}")
    licence = next((p for p in src.iterdir() if p.name.lower() in ("ofl.txt", "inter-ofl.txt")), None)
    if licence:
        shutil.copyfile(licence, OUT / "OFL-Inter.txt")


def names(font: TTFont) -> tuple[str, str, str]:
    """(family, subfamily, postscript) — typographic names first, legacy ones as fallback."""
    n = font["name"]
    family = n.getDebugName(16) or n.getDebugName(1)
    sub = n.getDebugName(17) or n.getDebugName(2) or "Regular"
    ps = n.getDebugName(6) or re.sub(r"\W", "", f"{family}-{sub}")
    return family, sub, ps


def build_mrs_eaves() -> list[dict]:
    faces = []
    for old in OUT.glob("MrsEaves*"):
        old.unlink()
    # Any depth: a foundry download arrives as a folder with a "Web Fonts" kit inside it.
    found = sorted(p for p in SOURCE.rglob("*") if p.suffix.lower() in (".otf", ".ttf")) if SOURCE.is_dir() else []
    files, seen = [], set()
    for p in found:  # the same face often ships twice (desktop + web kit): keep one per PostScript name
        ps = names(TTFont(p))[2]
        if ps not in seen:
            seen.add(ps)
            files.append(p)
    if not files:
        print(f"  (no Mrs Eaves files in {SOURCE}; display falls back to the system stack)")
    for src in files:
        font = TTFont(src)
        family, sub, ps = names(font)
        italic = "italic" in sub.lower() or bool(font["OS/2"].fsSelection & 1) or font["post"].italicAngle != 0
        weight = font["OS/2"].usWeightClass
        stem = ps if ps.startswith("MrsEaves") else f"MrsEaves-{ps}"
        dst = OUT / f"{stem}{src.suffix.lower()}"
        shutil.copyfile(src, dst)  # unmodified, for Office and Pillow (FreeType is lenient)
        web_woff2(src, dst.with_suffix(".woff2"))  # not the foundry's web kit: see web_woff2
        faces.append({
            "family": family, "subfamily": sub, "style": "italic" if italic else "normal",
            "weight": weight, "file": dst.with_suffix(".woff2").name, "desktop": dst.name,
        })
        print(f"  {dst.name:34} family={family!r} sub={sub!r} {('italic' if italic else 'normal')} {weight}")
    return faces


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--inter", type=Path, help="dir holding the google/fonts Inter variable TTFs")
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)

    if args.inter:
        build_inter(args.inter)
    faces = build_mrs_eaves()
    for _, output, _, style, weight in INTER:
        if (OUT / output).exists():
            faces.append({"family": "Inter", "subfamily": output[6:-4], "style": style, "weight": weight,
                          "file": output.replace(".ttf", ".woff2"), "desktop": output})
    manifest = {
        "_note": "Generated by scripts/build_fonts.py. inline.py registers each face under `family`.",
        "faces": faces,
    }
    (OUT / "fonts.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"wrote {OUT / 'fonts.json'} ({len(faces)} faces)")


if __name__ == "__main__":
    main()
