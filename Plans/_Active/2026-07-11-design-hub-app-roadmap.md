# Design Hub → Desktop App Roadmap (started 2026-07-11)

Design SSOT: [`../../docs/PREVIEWER.md`](../../docs/PREVIEWER.md). This file
is the working checklist; check items off as phases land.

> **Status 2026-07-13: STILL ACTIVE.** Phase 1 shipped. Phases 2–5 are unstarted —
> verified against the source (no `--variants` flag, no `pdf_tool/app.py`, no canvas
> drag-and-drop, no multi-page collage book). **Do not archive this plan.**
>
> Unrelated work that landed since (2026-07-13, not part of this roadmap): the résumé
> vault restructure, `themes/PALETTE-RULES.md` + the `check_palette` guard, brand token
> maps, and `pyproject.toml` (so `python -m pdf_tool.*` runs from the repo root).

## Phase 1 — local previewer ✅ (2026-07-11)

- [x] `src/pdf_tool/preview.py` — Design Hub server (sidebar thumbnails,
      main preview, palette swapper, export panel)
- [x] `css_vars` injection in `html_to_pdf.py` (palette-swapped exports are WYSIWYG)
- [x] Verified against jenni-resume + martian-collage candidates

## Phase 2 — variant generation

- [ ] `--variants` mode: render N palette variants of one document into `_variants/`
- [ ] Hub groups variants under the source document
- [ ] Optional: custom palette editor in the hub (color pickers → save as storage/themes/*.json)

## Phase 3 — windowed app (pywebview)

- [ ] `pdf_tool.app` — pywebview window wrapping the preview server
- [ ] Native file dialogs for "export to…" and "open directory"
- [ ] Decide later: Electron/Tauri only if distributing to non-Python users

## Phase 4 — canvas editor

- [ ] Canvas-size preset picker (README table presets)
- [ ] Drag & drop images onto canvas / directory input → image tray
- [ ] Layout family as starting arrangement; drag to reorder; hero pick; text blocks
- [ ] Reads/writes `collage-source.json` (CLI and GUI share the same data file)

## Phase 5 — collage books

- [ ] Multi-page project file (list of collage-source pages)
- [ ] Render all pages → `merge_pdfs.py` → one PDF book
