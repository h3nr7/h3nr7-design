# Mrs Eaves source files (not in git)

Drop the Mrs Eaves OT Italic `.otf` / `.ttf` here (the foundry folder as downloaded is fine —
the italic is the only cut the system uses). Then run:

    python scripts/build_fonts.py

which copies them into `skills/h3nr7-design/assets/fonts/` (plus a WOFF2 of each for
`scripts/inline.py`) and rewrites `fonts.json`.

Mrs Eaves is a commercial Emigre face. Everything in this folder, and the copies the build
makes inside the skill, are `.gitignore`d — the skill ZIP built from this machine carries
them; the repository never does. Keep the ZIP to your own Claude account.
