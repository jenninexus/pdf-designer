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

**No MCP / always-on server.** Optional temporary localhost only. CLI export works without it.

### Auto-refresh (no restart when you export)

The hub **refreshes itself** when documents change — you don't restart it after exporting a new resume
or editing a source. A client poller hits **`GET /api/version`** (~every 1.5s), which returns a cheap
tree *signature* (count + newest mtime + total size over `*.html` sources **and** `_exports/**` outputs)
plus a fresh document list. When the signature changes, the sidebar re-renders, the open preview reloads
(cache-busted), and a small toast flashes (`＋1 document`). So the loop is simply: **export or edit → the
hub updates on its own.** The signature is coarse and content-free (never reads file bytes), so it stays
fast on a large tree. If the server is briefly down mid-poll, the client just retries the next tick.

### Chrome vs document tokens

| Layer | Where | Purpose |
|---|---|---|
| **Hub chrome** | `src/pdf_tool/static/hub.css` | App shell (filters, library, stage). Vendored `--dash-*` from www-theme-kit dashboard tokens + glass. Profile: `www-theme-kit/profiles/pdf-designer.json`. |
| **Document brands** | `themes/*.json` + `themes/presets/*.json` + `storage/brand-design/brand-*.json` | Palette swapper / WYSIWYG export. Personal SSOT — see [`STORAGE.md`](STORAGE.md). |

### Breakpoints (one project reference)

| Pointer | Role |
|---|---|
| [`.config/mcp-pdf-designer.json#breakpoints`](../.config/mcp-pdf-designer.json) | ⭐ **THE** pdf-designer breakpoint SSOT (set name + paths — not duplicate numbers) |
| `C:\mcp\.config\mcp-breakpoints.json` | Global cross-PC cache → `bootstrap_5_3_8_extended_390_4k` |
| `www-theme-kit/scss/_breakpoint-tokens.scss` | Shared numeric tokens / mixins (syna mirror identical) |
| `hub.css` `@media` | Hard-codes the same `.98px` maxes (CSS cannot `var()` inside `@media`) |

Hub layout: stacks below **991.98px** (md-max); comfortable from **1200px** (xl); widescreen from **1400px** (xxl).

Each `.html` file is its **own template** in the library (one card = one file).

### Filters (Jobright-style library)

Adapted from `D:\Resume\Jobright\jobright-feature-review.md` — local-first library + filters, not cloud match scores:

- **Kind chips:** All · Resumes · Cover letters · Collages · Galleries · Examples
- **Folder:** e.g. `storage/_job-listings/3D-Artist`, `examples/profiles/default-resume`
- **Person:** jenni / shade (from filename prefix)
- **Search:** name or path substring

Sidebar groups stay collapsible by folder. Stage bar shows kind · person · bucket · path.

### Features

- **Live thumbnails** for every renderable `.html` (excludes `_exports/`, etc.)
- **Palette swapper** → injects CSS vars into the previewed document (and into export)
- **Export selected** → PDF light/dark or PNG pages
- **Vault overview** → [http://127.0.0.1:8787/vault](http://127.0.0.1:8787/vault) · `GET /api/vault-overview`
  — human-readable `storage/users`, profiles (joined under each person), `boardSkills` tags, and `goToPacks`
  (which default résumé targets which job family). Read-only; no second renderer.
  Pack **Open in library** links use `/?doc=<html-path>` to select that file in the Hub
  library (filters cleared, person chip set, card scrolled into view). Selecting a
  library card also writes `?doc=` into the URL for shareable deep-links.
- Zero new deps (stdlib server; Playwright only for export/render)
  Binds to 127.0.0.1 only.

Typical flows:

- **"Hide old cover letters"** — click **Resumes** (or filter folder to one application track).
- **"Only collages"** — click **Collages**.
- **"Which resume style?"** — filter Examples / vault renders, audition palettes, export.
- **"Which collage?"** — Collages filter, or open `_candidates/index.html` (gallery kind).

## Lineage (D:\Resume → pdf-designer)

| Keep / adapt in pdf-designer | Leave private on D:\Resume |
|---|---|
| Engine, Design Hub, protocol docs, examples | Disney finals, personal vaults, Jobright screenshots |
| Jobright *library + filter* UX ideas | Jobright match scores / autofill / extension |
| Brand maps under `storage/brand-design/` | Historical prompt logs |

## Roadmap

### Phase 2 — variant generation (`--variants`)

One command that renders N palette/layout variants of the same document into
`_variants/` so the hub can show true side-by-side alternatives without
hand-copying files. Resume color-combo shopping becomes: generate variants →
open hub → pick → export.

### Phase 3 — paid shell (shell-over-Hub first; pywebview optional)

**Product decision (2026-07-21):** the paid app is a thin installer / launcher
around **this** Design Hub — not a second renderer. See [`PRODUCT.md`](PRODUCT.md)
§ shell-over-Hub. Native window (pywebview) stays **parked** until a non-browser
shell is actually needed.

| | shell-over-Hub (chosen) | pywebview (parked) | Electron / Tauri |
|---|---|---|---|
| Fits this stack | ✅ Hub already ships | ✅ ~1 MB OS webview | ❌ heavy / new toolchain |
| First milestone | installer + recipe gallery chrome | native window polish | only if Python install is a blocker |
| Engine | same `pdf_tool.preview` HTTP | same | same |

Recipe gallery = Hub UI over tracked `layouts/` + `themes/presets/`. Packaging
precursor: [`PACKAGING.md`](PACKAGING.md).

### Phase 4 — canvas editor (drag & drop)

The interactive collage/composition surface, still engine-backed:

- **Canvas with size presets** — full table in
  [`COLLAGE-DESIGN.md`](COLLAGE-DESIGN.md#default-canvas-sizes) (`letter-portrait`,
  `hd-landscape`, `hd-portrait`, `standard-landscape`, `standard-portrait`, `ig-portrait`,
  `square`, …) — pick a size, get a live canvas at that geometry.
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
- [`Plans/_Active/2026-07-21-next-agent-product-prompt.md`](../Plans/_Active/2026-07-21-next-agent-product-prompt.md) — ⭐ live product checklist
- [`Plans/README.md`](../Plans/README.md) — active vs archive index
