# AGENTS.md — pdf-designer capability map for AI assistants

This file is the machine/agent-facing overview of the repo. It is
**vendor-neutral**: any AI coding assistant (Claude, Codex, Cursor, Copilot,
local models, none at all) should be able to drive this toolkit from this one
page. Human-facing docs: [`README.md`](README.md). **SSOT dashboard:**
[`docs/SSOT.md`](docs/SSOT.md). White-label (public-only) path:
[`docs/WHITE-LABEL.md`](docs/WHITE-LABEL.md). Deep design docs are linked
per section. Voice map/public cards: `C:\Github\voice-seed` (deep edit stays in `storage/`).

## Session start (read this first)

1. Read [`docs/SSOT.md`](docs/SSOT.md).
2. Design Hub: `python -m pdf_tool.preview` on :8787 (workspace folder-open task runs
   `scripts/ensure-design-hub.ps1` — starts the hub if needed, then opens the browser).
   First open may ask to allow automatic tasks — accept it.
3. Before resume work: `check_vault --explain`, `check_palette` before export, `check_ats` after light PDF.
4. Private data lives in `storage/` only — never promote it into tracked paths.

## What this repo does

Local-first PDF/document toolkit. Two layers:

1. **`pdf_tool`** — the engine. Render HTML → PDF via headless Chromium, merge
   PDFs, render PDF → PNG, guard the palette, validate a vault, build collages,
   serve a previewer. Deterministic: what a browser prints is what you get.
2. **The résumé layer** — a *protocol*, not a module. The job-application
   workflow lives in [`.claude/commands/make-resume.md`](.claude/commands/make-resume.md)
   (agent-agnostic markdown), backed by plain JSON in `storage/` and guards
   (`check_vault`, `check_ats`, `check_palette`). The judgment can't be coded; the data is the product. See
   [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

**Reads no environment variables. Makes no network calls.** Every knob is a CLI
flag or a constant — which is why there is no `.env` (one would be a fiction).

## Commands an agent can run

```bash
pip install -e . && playwright install chromium                 # one-time setup

python -m pdf_tool                                              # engine hub — list commands
python -m pdf_tool.html_to_pdf <doc>.html                       # light/ATS PDF (default)
python -m pdf_tool.html_to_pdf <doc>.html --pdf-theme dark      # dark branded PDF, same pagination
python -m pdf_tool.html_to_pdf <doc>.html --output-dir <dir>    # control export location
python -m pdf_tool.html_to_pdf <doc>.html --variants            # light PDF per public palette → _variants/<stem>/
python -m pdf_tool.variants <doc>.html                          # same as --variants
python -m pdf_tool.merge_pdfs out.pdf a.pdf b.pdf --require-letter   # bundle, validate 8.5x11
python -m pdf_tool.pdf_to_png <doc>.pdf                         # one PNG per page (visual verify)
python -m pdf_tool.check_palette <doc>.html                     # ⭐ palette guard — run before EVERY export
python -m pdf_tool.check_palette --scan storage/                #    sweep a whole tree
python -m pdf_tool.check_overflow <doc>.html --pdf-theme dark   # ⭐ overflow guard — page fits its box (pinned footer won't collide); auto-warns on export
python -m pdf_tool.check_vault --all                            # vault schema — catches invisible claims
python -m pdf_tool.check_vault --explain <user> <track>         # ranked claims preview (blocks on schema/thin)
python -m pdf_tool.check_vault --coverage <user> <track> <listing.md>  # listing gap-check
python -m pdf_tool.check_ats <resume-light.pdf>                 # ATS text-layer guard
python -m pdf_tool.tracker list                                 # scan storage/applications/**/application.json
python -m pdf_tool.tracker status                               # status breakdown (optional filter arg)
python -m pdf_tool.collage <imagesDir> --layout auto --png      # collage candidates + picker gallery
#   → writes to <imagesDir>/_candidates/<canvas>-<W>x<H>/ (never overwrites other sizes)
#   --canvas <preset> --px WxH --hero <file> --title "..." --theme light|dark
python -m pdf_tool.preview --no-open --port 8787                # Design Hub server (127.0.0.1; docs/PREVIEWER.md)
node scripts/wcag-resume-palettes.mjs                           # optional WCAG contrast spot-check (add --strict to fail)
```

`pip install -e .` makes `pdf_tool` importable **from the repo root**. (Without it you must run from
`src/` or set `PYTHONPATH=src` — the older docs' failure mode.)

Exports default to `_exports/` beside the source HTML and **never overwrite** (auto `-v2`, `-v3`).
Default dual-mode names: `<stem>-light.pdf` (ATS) and `<stem>-dark.pdf` (branded) when you
pass `--output-dir` / omit an explicit path — `--pdf-theme dark` selects the dark file.
**Verification without a screen:** export, then `pdf_to_png` and *read* the PNGs — that is the
intended agent feedback loop.

## Repo map

| Path | What it is |
|---|---|
| `src/pdf_tool/` | the engine (html_to_pdf, variants, tracker, merge_pdfs, pdf_to_png, check_palette, check_vault, check_ats, collage, preview) |
| `themes/default-resume.{json,css}` | public default theme — JSON is the token SSOT, CSS is its mirror |
| `themes/presets/*.json` | public audition palettes (Design Hub swapper) |
| `themes/PALETTE-RULES.md` | ⭐ **the color rule** (no brown/mustard/lime) + how the guard enforces it |
| `examples/brands/` | tracked **template** for private brand maps (copy → `storage/brands/`) |
| `storage/brands/*.json` | ⛔ PRIVATE **pdf-designer color SSOT** per person/studio (gitignored). One file each — see [`docs/STORAGE.md`](docs/STORAGE.md). Website kits inspire; do not keep a second hex map in `users/*.json`. |
| `docs/README.md` | Docs index — humans start at root README, detail lives under `docs/` |
| `docs/SSOT.md` · `WHITE-LABEL.md` · `EXPORTS.md` | SSOT dashboard · public-only path · command/export recipes |
| `docs/LAYOUT-SYSTEM.md` | ⭐ Shared page model — equal margins, pinned footer, per-doc spec, work-samples build |
| `docs/STORAGE.md` · `VAULT.md` · `JOB-ASSESSMENT.md` | Tracked protocol (fresh clones). `storage/*.md` stubs only point here. |
| `.config/mcp-pdf-designer.json` | Project config — **breakpoint SSOT pointer** + Design Hub / palette / voice pointers |
| `Plans/_Active/` | ⭐ Working roadmap (one file) — see [`Plans/README.md`](Plans/README.md) |
| `themes/default-collage.json` | collage canvas presets + tokens ([`docs/COLLAGE-DESIGN.md`](docs/COLLAGE-DESIGN.md)) |
| `examples/profiles/<id>/` | one profile per document type: `profile.json` + reference `.html` render + example data |
| `examples/applications/` | one-folder-per-job-application workflow + copyable template |
| `docs/` | ARCHITECTURE, SSOT, WHITE-LABEL, STORAGE, VAULT, JOB-ASSESSMENT, THEME-DESIGN, EXPORTS, COLLAGE-DESIGN, PREVIEWER, LICENSING-NOTES |
| `storage/` | **gitignored** local workspace: vaults, real applications, real image sets, private brands |

### Privacy split (do not blur this)

| Public / tracked (safe to clone) | Private / gitignored (`storage/`) |
|---|---|
| `src/pdf_tool/`, `themes/`, `examples/`, `docs/`, `AGENTS.md` | `users/`, `*/resume-source.json`, `profiles/*-resume.json`, `applications/`, `brands/`, `_exports/` |
| Brand-neutral default theme | Real brand maps (`brand-jenninexus`, `brand-martian`, `brand-synagen`) |
| Example brand shape (`examples/brands/`) | Real vault claims, contacts, employer research |

Website kits own **live site** colors. For résumé exports, the mapped file under
`storage/brands/brand-*.json` is the **only** pdf-designer color SSOT — `users/*.json`
points via `brandTheme.ssot`; never duplicate hex there.

### The application workflow lives in `storage/` (gitignored)

Four layers, each answering one question. **The vault is the brain.**

| Layer | File | Answers |
|---|---|---|
| Person | `storage/users/<user>.json` | **who** — contact, `brandTheme.ssot`, **`characterVoice`**, `hardFacts` |
| **Vault** ⭐ | `storage/<user>/resume-source.json` | **what may be truthfully claimed** · application `voice` · roleTracks |
| Profile | `storage/profiles/<user>-resume.json` | **how** it renders (one per person — no per-track files) |
| Application | `storage/applications/<Track>/` | **the job** — listing, apply link, pay, company palette |

Read [`docs/VAULT.md`](docs/VAULT.md) before authoring any resume claim.  
Next engineering work: [`Plans/_Active/2026-07-14-professional-product-roadmap.md`](Plans/_Active/2026-07-14-professional-product-roadmap.md).

## Contracts (do not break)

- **Geometry is locked.** Resumes/letters are US Letter 8.5×11 with **equal margins on all four
  edges** — the default is `@page { size: Letter; margin: 0.65in; }` (a doc may open it wider, e.g.
  0.75in for a formal cover letter, but it must stay equal). Palette changes never change paper size,
  margins, or page-break strategy. **Layout model** (equal frame + header-flows/footer-pins):
  [`docs/LAYOUT-SYSTEM.md`](docs/LAYOUT-SYSTEM.md).
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
  [`docs/JOB-ASSESSMENT.md`](docs/JOB-ASSESSMENT.md).
- **Tailor a resume by hand:** read the listing → pick the role track → read the vault's
  `roleTracks.<track>.angle` → select claims whose `tracks` match, ordered by `strength` → cut to two
  pages → export light PDF → **verify by reading the PNG**.
- **New document type / profile:** copy `examples/profiles/default-resume/`
  (or `default-collage/`) to a new `examples/profiles/<id>/` (public example)
  or under `storage/` (real/private), point `profile.json` at the right theme.
- **Add a person:** `storage/users/<name>.json` + `storage/<name>/resume-source.json` +
  `storage/profiles/<name>-resume.json`. See [`docs/STORAGE.md`](docs/STORAGE.md).
- **Collage:** put images in `storage/collages/<project>/`, run
  `python -m pdf_tool.collage <dir> --layout auto --png`, open
  `<dir>/_candidates/index.html` to compare all six layout families, then
  export the winner (PNG for social canvases, `html_to_pdf.py` for print).
  Design + families: [`docs/COLLAGE-DESIGN.md`](docs/COLLAGE-DESIGN.md).
