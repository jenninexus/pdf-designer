# AGENTS.md — pdf-designer capability map for AI assistants

This file is the machine/agent-facing overview of the repo. It is
**vendor-neutral**: any AI coding assistant (Claude, Codex, Cursor, Copilot,
local models, none at all) should be able to drive this toolkit from this one
page. Human-facing docs: [`README.md`](README.md). Deep design docs are linked
per section.

## What this repo does

Local-first PDF/document toolkit. Two layers:

1. **`pdf_tool`** — the engine. Render HTML → PDF via headless Chromium, merge
   PDFs, render PDF → PNG, guard the palette, validate a vault, build collages,
   serve a previewer. Deterministic: what a browser prints is what you get.
2. **The résumé layer** — a *protocol*, not a module. The job-application
   workflow lives in [`.claude/commands/make-resume.md`](.claude/commands/make-resume.md)
   (agent-agnostic markdown), backed by plain JSON in `storage/` and two guards.
   The judgment can't be coded; the data is the product. See
   [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

**Reads no environment variables. Makes no network calls.** Every knob is a CLI
flag or a constant — which is why there is no `.env` (one would be a fiction).

## Commands an agent can run

```bash
pip install -e . && playwright install chromium                 # one-time setup

python -m pdf_tool.html_to_pdf <doc>.html                       # light/ATS PDF (default)
python -m pdf_tool.html_to_pdf <doc>.html --pdf-theme dark      # dark branded PDF, same pagination
python -m pdf_tool.html_to_pdf <doc>.html --output-dir <dir>    # control export location
python -m pdf_tool.merge_pdfs out.pdf a.pdf b.pdf --require-letter   # bundle, validate 8.5x11
python -m pdf_tool.pdf_to_png <doc>.pdf                         # one PNG per page (visual verify)
python -m pdf_tool.check_palette <doc>.html                     # ⭐ palette guard — run before EVERY export
python -m pdf_tool.check_palette --scan storage/                #    sweep a whole tree
python -m pdf_tool.collage <imagesDir> --layout auto --png      # collage candidates + picker gallery
#   → writes to <imagesDir>/_candidates/<canvas>-<W>x<H>/ (never overwrites other sizes)
#   --canvas <preset> --px WxH --hero <file> --title "..." --theme light|dark
python -m pdf_tool.preview --no-open --port 8787                # Design Hub server (127.0.0.1; docs/PREVIEWER.md)
```

`pip install -e .` makes `pdf_tool` importable **from the repo root**. (Without it you must run from
`src/` or set `PYTHONPATH=src` — the older docs' failure mode.)

Exports default to `_exports/` beside the source HTML and **never overwrite** (auto `-v2`, `-v3`).
**Verification without a screen:** export, then `pdf_to_png` and *read* the PNGs — that is the
intended agent feedback loop.

## Repo map

| Path | What it is |
|---|---|
| `src/pdf_tool/` | the engine (html_to_pdf, merge_pdfs, pdf_to_png, check_palette, collage, preview) |
| `themes/default-resume.{json,css}` | public default theme — JSON is the token SSOT, CSS is its mirror |
| `themes/PALETTE-RULES.md` | ⭐ **the color rule** (no brown/mustard/lime) + how the guard enforces it |
| `storage/brands/*.json` | ⛔ PRIVATE brand palettes (gitignored). The previewer reads them alongside `themes/`. |
| `themes/default-collage.json` | collage canvas presets + tokens ([`docs/COLLAGE-DESIGN.md`](docs/COLLAGE-DESIGN.md)) |
| `examples/profiles/<id>/` | one profile per document type: `profile.json` + reference `.html` render + example data |
| `examples/applications/` | one-folder-per-job-application workflow + copyable template |
| `docs/` | ARCHITECTURE, THEME-DESIGN, EXPORTS, COLLAGE-DESIGN, PREVIEWER, LICENSING-NOTES |
| `storage/` | **gitignored** local workspace: the vaults, real applications, real image sets |

### The application workflow lives in `storage/` (gitignored)

Four layers, each answering one question. **The vault is the brain.**

| Layer | File | Answers |
|---|---|---|
| Person | `storage/users/<user>.json` | **who** is applying |
| **Vault** ⭐ | `storage/<user>/resume-source.json` | **what may be truthfully claimed** · how they sound · the angle per role track |
| Profile | `storage/profiles/<user>-resume.json` | **how** it renders (one per person — no per-track files) |
| Application | `storage/applications/<Track>/` | **the job** — listing, apply link, pay, company palette |

Read [`storage/VAULT.md`](storage/VAULT.md) before authoring any resume claim.

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
- **Palette rule.** **No brown, no mustard, no puke/lime green.** Amber has no
  readable dark form on white — darkening it turns it brown; on the light
  palette hand that role to another hue. Enforced by
  `python -m pdf_tool.check_palette` — **run it before every export.**
  Full rule: [`themes/PALETTE-RULES.md`](themes/PALETTE-RULES.md).
- **Source-backed only.** Never write a resume claim that isn't in the
  user's vault (`storage/<user>/resume-source.json`). Employer-specific framing
  goes in the cover letter, never the resume body.
- **🛑 Ask before calling something a gap.** The vault records what the user has
  *told* you — it is **not** the limit of what they can do. If a listing needs
  something the vault lacks, **ask them first**; if they have it, write it into
  the vault, then use it. (`doNotClaim` means *"not yet confirmed"*, not
  *"can't do it"* — Maya and ZBrush sat there for months while both founders had
  years of experience with each.)
- **No auto-submission.** Prepare materials; the human submits.
- **Privacy split.** `storage/`, `*.pdf`, `*.png`, `_exports/`,
  non-`.example` source/capture files are gitignored. Never move real
  personal data into tracked paths; never put private brand palettes into
  the tracked default themes.

## Common tasks → recipes

- **New job application:** run **`/make-resume <user> <application-dir>`** — it runs the whole
  routine (capture the apply link → verify remote/pay → **gap-check and ask** → derive the theme →
  write → export light+dark → merge the bundle → log it). Folders are keyed by **role track**
  (`storage/applications/3D-Visualizer/`), not by date. Protocol:
  [`storage/JOB-ASSESSMENT.md`](storage/JOB-ASSESSMENT.md).
- **Tailor a resume by hand:** read the listing → pick the role track → read the vault's
  `roleTracks.<track>.angle` → select claims whose `tracks` match, ordered by `strength` → cut to two
  pages → export light PDF → **verify by reading the PNG**.
- **New document type / profile:** copy `examples/profiles/default-resume/`
  (or `default-collage/`) to a new `examples/profiles/<id>/` (public example)
  or under `storage/` (real/private), point `profile.json` at the right theme.
- **Add a person:** `storage/users/<name>.json` + `storage/<name>/resume-source.json` +
  `storage/profiles/<name>-resume.json`. See [`storage/README.md`](storage/README.md).
- **Collage:** put images in `storage/collages/<project>/`, run
  `python -m pdf_tool.collage <dir> --layout auto --png`, open
  `<dir>/_candidates/index.html` to compare all six layout families, then
  export the winner (PNG for social canvases, `html_to_pdf.py` for print).
  Design + families: [`docs/COLLAGE-DESIGN.md`](docs/COLLAGE-DESIGN.md).
