# Parked — Design Hub Phases 3–5 (archived 2026-07-14)

Pulled out of the active roadmap so the résumé pipeline stays the focus.
Not cancelled — revive when there is real demand.

## Phase 3 — windowed app (pywebview)

- [ ] `pdf_tool.app` — pywebview window around the preview server
- [ ] Native file dialogs for "export to…" / "open directory"
- [ ] Electron/Tauri only if distributing to non-Python users

pywebview remains the right call (~1 MB, Python engine, hub already localhost).
A native window is polish — the browser works today.

## Phases 4–5 — canvas editor & collage books

- [ ] Canvas-size preset picker · drag-and-drop image tray · layout families
- [ ] Reads/writes `collage-source.json` (CLI and GUI share one data file)
- [ ] Multi-page project file → `merge_pdfs` → one PDF book

**Do not start until a real collage need shows up.** The CLI already produces six
layout families and a picker gallery.
