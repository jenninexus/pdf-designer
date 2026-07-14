# Design Hub — Previewer & the App Roadmap

How you preview styles and pick winners in pdf-designer — today as a local
web app, eventually as a windowed desktop app. Design principle first, then
what exists, then the phased roadmap.

## The one rule that makes previews trustworthy

**The Python engine is the only renderer.** Every preview is the *same HTML
file* the exporter prints, shown in the same browser engine. The app layers
(gallery, palette swapper, future canvas editor) are thin shells that never
re-implement rendering — so the preview you pick is byte-for-byte what
exports, this year and in five years. UI layers may come and go; documents
and the CLI keep working without them (headless parity).

## What exists now: `pdf_tool.preview`

```powershell
pip install -e .                          # one-time: makes pdf_tool importable from the repo root
python -m pdf_tool.preview                # scan the repo, open http://127.0.0.1:8787
python -m pdf_tool.preview path/to/dir    # scan any directory (e.g. one application folder)
python -m pdf_tool.preview --port 9000 --no-open
```

The PowerPoint-style picker, generalized to the whole repo:

- **Sidebar of live thumbnails** for every `.html` document found (resume
  renders, collage candidates, cover letters), grouped by folder — like
  PowerPoint Designer's side column, but for all your documents.
- **Click a thumbnail** → full-size preview in the main pane.
- **Palette swapper**: audition color combos live. Palettes are read from
  `themes/*.json` (public) and `storage/themes/*.json` (private) — drop in
  another theme file to get more options. Works on any template that uses
  the token contract (`--bg`, `--primary`, …).
- **Export selected** → PDF (light/dark) or PNG pages, to any output folder
  (default `_exports` next to the doc). A swapped palette is *included* in
  the export via `html_to_pdf`'s `css_vars` injection — preview is WYSIWYG.
- Zero new dependencies (stdlib server; exports reuse Playwright).
  Binds to 127.0.0.1 only.

Typical flows:

- **"Which resume style?"** — copy your resume HTML into 2–3 variants (or
  keep one HTML and audition palettes with the swapper), open the hub,
  compare side by side, export the winner.
- **"Which collage?"** — run `pdf_tool.collage`, open the hub (or the
  generated `_candidates/index.html`), pick, export.

## Roadmap

### Phase 2 — variant generation (`--variants`)

One command that renders N palette/layout variants of the same document into
`_variants/` so the hub can show true side-by-side alternatives without
hand-copying files. Resume color-combo shopping becomes: generate variants →
open hub → pick → export.

### Phase 3 — windowed app (pywebview first, Electron if outgrown)

Recommendation: **pywebview**, not Electron, as the first app shell.

| | pywebview | Electron | Tauri |
|---|---|---|---|
| Fits this stack | ✅ engine is Python; one `pip install pywebview` | ❌ adds Node/Chromium bundle + IPC to Python | ❌ adds Rust toolchain |
| App size | ~1 MB (uses OS webview) | ~150 MB+ | small |
| Native file dialogs, drag-drop | ✅ | ✅ | ✅ |
| Distribution to non-Python users | weaker | ✅ strongest | ✅ |

The hub is already a localhost web app, so the shell is trivial: pywebview
window pointed at the same server = same UI, native window, real file-picker
dialogs for "export to…". Revisit Electron/Tauri only when distributing to
users who won't install Python — the UI code carries over unchanged either
way, because everything speaks HTTP to the same engine.

### Phase 4 — canvas editor (drag & drop)

The interactive collage/composition surface, still engine-backed:

- **Canvas with size presets** (the README table: Letter, 16:9, 9:16, 4:3,
  4:5, 1:1) — pick a size, get a live canvas at that geometry.
- **Add images** by dragging files onto the canvas *or* pointing at a
  directory (the current `collage.py` input), thumbnails appear in a tray.
- **Arrange**: apply any layout family as the starting point, then drag to
  reorder, pick the hero, drop a text block in.
- **Persistence**: the editor reads/writes `collage-source.json` — the same
  file the CLI uses. Close the app, re-run the CLI, nothing is lost; the
  GUI is an editor for the data file, not a separate world.
- **Export panel**: format (PDF/PNG), light/dark, output folder — same
  `/api/export` endpoint.

### Phase 5 — collage books / multi-page projects

A project file listing multiple collage pages (each its own
`collage-source.json`) → render each page → `merge_pdfs.py` into one PDF
book. Same pattern as cover-letter + resume bundles.

## See also

- [`COLLAGE-DESIGN.md`](COLLAGE-DESIGN.md) — layout families + canvas presets
- [`THEME-DESIGN.md`](THEME-DESIGN.md) — token contract the palette swapper relies on
- [`EXPORTS.md`](EXPORTS.md) — export command reference
- `Plans/_Active/` — the live phase checklist
