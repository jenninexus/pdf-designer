# AGENTS.md — pdf-designer capability map for AI assistants

This file is the machine/agent-facing overview of the repo. It is
**vendor-neutral**: any AI coding assistant (Claude, Codex, Cursor, Copilot,
local models, none at all) should be able to drive this toolkit from this one
page. Human-facing docs: [`README.md`](README.md). Deep design docs are linked
per section.

## What this repo does

Local-first PDF/document toolkit. Two layers:

1. **`pdf_tool`** — render HTML → PDF via headless Chromium, merge PDFs,
   render PDF → PNG. Deterministic; what a browser prints is what you get.
2. **`application_assistant`** (partly planned) — job-application workflow on
   top: claim vault, job-listing capture, per-application folders, tailored
   resumes that never invent a claim.

## Commands an agent can run

```bash
pip install playwright && playwright install chromium   # one-time setup

python -m pdf_tool.html_to_pdf <doc>.html                       # light/ATS PDF (default)
python -m pdf_tool.html_to_pdf <doc>.html --pdf-theme dark      # dark branded PDF, same pagination
python -m pdf_tool.html_to_pdf <doc>.html --output-dir <dir>    # control export location
python -m pdf_tool.merge_pdfs out.pdf a.pdf b.pdf --require-letter   # bundle, validate 8.5x11
python -m pdf_tool.pdf_to_png <doc>.pdf                         # one PNG per page (visual verify)
python -m pdf_tool.collage <imagesDir> --layout auto --png      # collage candidates + picker gallery
```

Run from `src/` (or with `src/` on `PYTHONPATH`). Exports default to
`_exports/` beside the source HTML and never overwrite (auto `-v2`, `-v3`).
**Verification without a screen:** export, then `pdf_to_png.py` and read the
PNGs — that is the intended agent feedback loop.

## Repo map

| Path | What it is |
|---|---|
| `src/pdf_tool/` | the engine (html_to_pdf, merge_pdfs, pdf_to_png; more planned) |
| `themes/default-resume.{json,css}` | public default theme — JSON is the token SSOT, CSS is its mirror |
| `themes/default-collage.json` | collage canvas presets + tokens ([`docs/COLLAGE-DESIGN.md`](docs/COLLAGE-DESIGN.md)) |
| `examples/profiles/<id>/` | one profile per document type: `profile.json` + reference `.html` render + example data |
| `examples/applications/` | one-folder-per-job-application workflow + copyable template |
| `examples/job-listing-capture.example.md` | job-listing capture template |
| `docs/` | ARCHITECTURE, THEME-DESIGN, EXPORTS, COLLAGE-DESIGN, LICENSING-NOTES |
| `storage/` | **gitignored** local workspace: real profiles, real applications, real image sets |

## Contracts (do not break)

- **Geometry is locked.** Resumes/letters are US Letter 8.5×11 with
  `@page { size: Letter; margin: 0.5in 0.55in 0.78in; }`. Palette changes
  never change paper size, margins, or page-break strategy.
- **Dual mode is intentional.** Every document supports light print
  (`@media print` default, ATS-safe) AND dark branded
  (`html[data-pdf-theme="dark"]` overrides). Keep both working when editing
  a template.
- **Token names.** `--bg, --surface, --elevated, --text, --dim, --dim2,
  --border, --border2, --primary, --secondary, --accent, --support`.
  External palettes get *mapped into* these names ([`docs/THEME-DESIGN.md`](docs/THEME-DESIGN.md)).
- **Source-backed only.** Never write a resume claim that isn't in the
  user's resume-source vault (`resume-source.json`). Unverified stays marked
  unverified. Employer-specific framing goes in the cover letter, never the
  resume body.
- **No auto-submission.** Prepare materials; the human submits.
- **Privacy split.** `storage/`, `*.pdf`, `*.png`, `_exports/`,
  non-`.example` source/capture files are gitignored. Never move real
  personal data into tracked paths; never put private brand palettes into
  the tracked default themes.

## Common tasks → recipes

- **New job application:** create
  `storage/applications/<yyyy-mm-dd>-<company>-<role>/`, copy
  `examples/applications/example-application/`, follow
  [`examples/applications/README.md`](examples/applications/README.md).
- **New document type / profile:** copy `examples/profiles/default-resume/`
  (or `default-collage/`) to a new `examples/profiles/<id>/` (public example)
  or under `storage/` (real/private), point `profile.json` at the right theme.
- **Tailor a resume:** read the application folder's
  `job-listing-capture.md`, adjust the resume HTML emphasis using only vault
  claims, export light PDF, verify via PNG.
- **Collage:** put images in `storage/collages/<project>/`, run
  `python -m pdf_tool.collage <dir> --layout auto --png`, open
  `<dir>/_candidates/index.html` to compare all six layout families, then
  export the winner (PNG for social canvases, `html_to_pdf.py` for print).
  Design + families: [`docs/COLLAGE-DESIGN.md`](docs/COLLAGE-DESIGN.md).
