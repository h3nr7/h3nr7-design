"""
Validate the skill and zip it for upload to Claude (Desktop or claude.ai).

    python scripts/package.py                    # -> dist/h3nr7-design.zip
    python scripts/package.py --allow-no-display # build even without the Mrs Eaves files

Upload: Claude → Customize → Skills → + → Create skill → Upload a skill, and pick the ZIP.
Code execution must be on (Settings → Capabilities → "Code execution and file creation").

The ZIP holds one top-level folder named like the skill, with exactly one SKILL.md in it —
what the uploader requires. It carries the Mrs Eaves files from this machine (they are
.gitignored, never in the repo), so it is refused when they are missing: a skill whose
display face silently became a system Baskerville is the failure this guards against.
Standard library only.
"""

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "h3nr7-design"
DIST = ROOT / "dist"
SKIP_DIRS = {"__pycache__", "node_modules", ".git"}
SKIP_FILES = {".DS_Store", "Thumbs.db"}


def frontmatter(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        sys.exit("SKILL.md: no YAML frontmatter")
    fields = {}
    for line in m.group(1).splitlines():
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    return fields


def validate() -> list[str]:
    problems = []
    fm = frontmatter((SKILL / "SKILL.md").read_text(encoding="utf-8"))
    name, desc = fm.get("name", ""), fm.get("description", "")
    if name != SKILL.name:
        problems.append(f"name {name!r} must equal the folder name {SKILL.name!r}")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) or len(name) > 64:
        problems.append("name must be kebab-case, at most 64 characters")
    if not desc or len(desc) > 1024 or "<" in desc or ">" in desc:
        problems.append(f"description must be 1–1024 characters with no angle brackets (is {len(desc)})")
    extra = [p for p in SKILL.rglob("SKILL.md") if p.parent != SKILL]
    if extra:
        problems.append(f"only one SKILL.md allowed, also found: {extra}")
    for ref in re.findall(r"`((?:references|assets|scripts)/[\w./-]+)`", (SKILL / "SKILL.md").read_text(encoding="utf-8")):
        if not (SKILL / ref).exists() and "*" not in ref:
            problems.append(f"SKILL.md points at a missing file: {ref}")
    return problems


def display_faces() -> list[dict]:
    manifest = SKILL / "assets" / "fonts" / "fonts.json"
    faces = json.loads(manifest.read_text(encoding="utf-8"))["faces"] if manifest.exists() else []
    return [f for f in faces if f["family"] != "Inter" and (SKILL / "assets" / "fonts" / f["file"]).exists()]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--allow-no-display", action="store_true", help="package without the Mrs Eaves files")
    args = ap.parse_args()

    problems = validate()
    if problems:
        sys.exit("not packaged:\n  " + "\n  ".join(problems))
    faces = display_faces()
    if not faces and not args.allow_no_display:
        sys.exit("not packaged: no Mrs Eaves files in the skill. Put them in source/fonts/ and run "
                 "scripts/build_fonts.py first (or pass --allow-no-display).")

    DIST.mkdir(exist_ok=True)
    out = DIST / f"{SKILL.name}.zip"
    count, size = 0, 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(SKILL.rglob("*")):
            rel = p.relative_to(SKILL.parent)
            if p.is_dir() or p.name in SKIP_FILES or SKIP_DIRS & set(rel.parts):
                continue
            z.write(p, rel.as_posix())
            count += 1
            size += p.stat().st_size
    print(f"display faces: {', '.join(f['family'] + ' ' + f['subfamily'] for f in faces) or 'NONE'}")
    print(f"wrote {out}: {count} files, {size // 1024} KB raw, {out.stat().st_size // 1024} KB zipped")


if __name__ == "__main__":
    main()
