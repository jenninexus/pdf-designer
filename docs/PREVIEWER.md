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
python -m pdf_tool.preview examples        # exact public-seed library (no local workspace documents)
python -m pdf_tool.preview --port 9000 --no-open
```

### What a new user sees

`python -m pdf_tool.preview` scans the **current checkout** — root nouns (`resumes/`,
`_job-apps/`, `collages/`, `users/`, `vaults/`, `profiles/`, `brands/`) plus tracked
`examples/` and `layouts/`. The `storage/` directory was retired 2026-08-17; `pdf_tool.paths`
still maps old `storage/<user>/…` preview URLs to `resumes/<user>/…` when the live file exists.
A fresh clone contains only tracked files, so it has no personal cards to discover. To inspect
the release experience exactly, run `python -m pdf_tool.preview examples`: the library contains
only the tracked default resume, cover letter, letter, work samples, collage, and gallery examples.
`examples/resume-studio/` is the walkthrough data and docs, not a renderable document directory by itself.

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
| **Hub chrome** | `src/pdf_tool/static/hub.css` | App shell (filters, library, stage). Vendored `--dash-*` from **www-theme-kit** dashboard tokens + glass. Official profile: [`www-theme-kit/profiles/pdf-designer.json`](../../www-theme-kit/profiles/pdf-designer.json). |
| **Document brands** | `themes/*.json` + `themes/presets/*.json` + `brands/brand-*.json` | Palette swapper / WYSIWYG export. Personal SSOT — see [`STORAGE.md`](STORAGE.md). |

### Breakpoints (one project reference)

| Pointer | Role |
|---|---|
| [`.config/mcp-pdf-designer.example.json#breakpoints`](../.config/mcp-pdf-designer.example.json) | ⭐ Tracked seed — copy to local `mcp-pdf-designer.json` (gitignored) for machine paths |
| Global breakpoint cache (optional) | e.g. shared `mcp-breakpoints.json` → `bootstrap_5_3_8_extended_390_4k` |
| `www-theme-kit/scss/_breakpoint-tokens.scss` | Shared numeric tokens / mixins (www-theme-kit is the consumer SSOT for this repo) |
| `hub.css` `@media` | Hard-codes the same `.98px` maxes (CSS cannot `var()` inside `@media`) |

Hub layout: **library left + viewer right** from **576px** up (desktop / tablet). Stacks only below
**575.98px** (phones). Drawer (hamburger) from **≤767.98px**. Comfortable from **1200px** (xl);
widescreen from **1400px** (xxl). Compact bar is **~40px**.
**Vault + Recipes** use the same switch points (shared `hub.css` + `Library | Recipes | Vault` nav). Library is `body.hub-shell` (fixed panes); subpages are `body.hub-page` (document scroll). Tables get a horizontal scroll wrapper below md.

Each `.html` file is its **own template** in the library (one card = one file).

### Filters (Jobright-style library)

Local-first library + filters (Jobright-style UX inspiration — not cloud match scores):

- **Kind chips (leading, after Profiles):** All · Resumes · Cover Letters · Letters · Work Samples · **Collages** · Galleries — then Library / Recipes / Vault / search / folder / palette scroll horizontally. **Refresh (icon) + Export (download icon) stay pinned** on the right; **⋯** opens the output-folder popover (also pinned — not clipped). ≤767.98px: hamburger drawer holds filters + outdir; magnifier opens search overlay (Ctrl/Cmd+K). Mouse wheel over the header strip scrolls that row horizontally.
- **Folder:** custom picker (not a bare `<select>`). Open the list → hover a row for a **ghost ★**; click the star to pin / unpin. Pinned folders sort to the **top** and persist in `localStorage` (`pdf-designer.hub.pinnedFolders`) across Refresh and full reloads. No separate pin button in the toolbar. Menu is `position:fixed` (JS places it from the trigger rect) so `.hub-bar-scroll`’s `overflow-y:hidden` cannot clip it.
- **Profiles** (was “Who”): `all profiles` plus **`examples` first** (Jane Example, from tracked `profiles/examples.json`) then every workspace id from `users/` + `profiles/`. Path ownership (`resumes/<id>/` · legacy `storage/<id>/` URLs resolve to the same files) or a hyphen-bounded token (`jenni-…`, `meet-jenni-bot`) tags the card. Preference: `pdf-designer.hub.profileFilter`. First visit with no stored preference selects `examples`. **Design Hub** logo returns to the home landing (kind cards) and clears `?doc=`.
  - Choosing a profile **scopes** the folder picker and kind-chip counts to that profile. Kind chips click the first matching card. A leftover folder filter is **not** restored across reload (that hid the library behind one template dir).
  - Copy `profiles/you-resume.example.json` → `profiles/you-resume.json` for yourself; keep `profiles/examples.json` so the public cards stay in the dropdown.
  - **Trap:** collage projects **without** a profile token (`profile: null`) still disappear when Profiles ≠ `all profiles`. Search the folder name, or pick All. Lesson: `.memory/lesson-hub-collage-hidden-by-profile-filter.md`.
- **Search:** name or path substring

Sidebar is a **left column**; the stage / iframe viewer fills the rest of the viewport. Groups stay collapsible by folder. Stage bar shows kind · profile · bucket · path.

### Features

- **Live thumbnails** for every renderable `.html` (excludes `_exports/`, etc.)
- **Palette swapper** → injects CSS vars into the previewed document (and into export)
- **Export selected** → PDF light/dark or PNG pages
- **Vault overview** → [http://127.0.0.1:8787/vault](http://127.0.0.1:8787/vault) · `GET /api/vault-overview?profile=examples`
  — default card is public Jane Example (`users/examples.json`). Personal vaults (jenni / shade / studio) appear only when that profile is selected in the header. Pack **Open in library** links use `/?doc=<html-path>`.
- **Recipe gallery** → [http://127.0.0.1:8787/recipes](http://127.0.0.1:8787/recipes) · `GET /api/recipe-gallery`
  — browse tracked `layouts/{cover-letter,letter,resume,work-examples,collage}/` + `themes/presets/` (structure +
  public audition palettes). Copy collage CLI (`--recipe <id>`), open raw JSON, or
  **Try in Hub** via `/?palette=<id>&mode=dark|light` (selects the palette swapper).
  Discovery chrome only — still one renderer.
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
| Brand maps under `brands/` | Historical prompt logs |

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

Recipe gallery chrome: **shipped** at `/recipes` (see Features above). Packaging
precursor for installers: [`PACKAGING.md`](PACKAGING.md).

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

### Workspace filters (live private tree)

Selecting a **header profile** must list that profile's documents. Restore the
profile chip **before** rebuilding folder options; scope folder + kind counts
to the selected profile or the library goes empty. README-only root-noun
scaffolds must not win over live root-noun payloads — `pdf_tool.paths._has_payload`
is the rule. Application identity is the path relative to `_job-apps/` (or the tracked
`applications/` README redirect), not the leaf folder name. Hub scan excludes `_archive/`
and `*.template.html`; stale `/storage/<user>/…` links resolve via `resolve_preview_file`.

Durable *why*: `.memory/lesson-hub-profile-scopes-folder-and-kind.md` ·
`lesson-scaffold-readme-must-not-win-path-resolution.md` ·
`lesson-hub-archive-not-found.md`.

## See also

- [`COLLAGE-DESIGN.md`](COLLAGE-DESIGN.md) — layout families + canvas presets
- [`THEME-DESIGN.md`](THEME-DESIGN.md) — token contract the palette swapper relies on
- [`EXPORTS.md`](EXPORTS.md) — export command reference
- [`WORKSPACE-LAYOUT.md`](WORKSPACE-LAYOUT.md) — root nouns (`storage/` retired; URL resolver only)
- [`Plans/README.md`](../Plans/README.md) — active vs archive index
