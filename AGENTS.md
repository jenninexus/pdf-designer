# AGENTS.md — pdf-designer

**The single agent-facing SSOT for this repo.** Any AI assistant (Claude, Codex, Cursor, Copilot, a
local model) or a human with a terminal should be able to drive the whole toolkit from this one page.
It is **vendor-neutral on purpose** — [`CLAUDE.md`](CLAUDE.md) and
[`.claude/commands/README.md`](.claude/commands/README.md) are thin pointers back here.

Human-facing intro: [`README.md`](README.md). Deep design docs live under [`docs/`](docs/) and are linked
per section below.

> **Jenni's dev note (SEGOPC):** for cross-workspace doc organization / search, the go-to is the
> user-global **`/jen:docs`** (and `/jen:doc-organize`). Those are personal tools, not a repo dependency —
> **this repo's own SSOT is [`docs/SSOT.md`](docs/SSOT.md)** and a fresh clone needs nothing outside the repo.

---

## Session start (read in this order)

1. **This file** — capability map + the contracts that must not break.
2. [`docs/SSOT.md`](docs/SSOT.md) — the SSOT dashboard (what this repo owns vs. points elsewhere).
3. [`docs/VAULT.md`](docs/VAULT.md) — **the vault**: what may be claimed, how each person sounds
   (`characterVoice` + vault `voice`), the capability matrix, the role tracks.
4. [`docs/JOB-ASSESSMENT.md`](docs/JOB-ASSESSMENT.md) — how to assess a listing (apply URL is blocking;
   remote? pay vs. market?; the evidence map).
5. [`docs/STORAGE.md`](docs/STORAGE.md) — the four private layers and the `storage/` layout.
6. [`themes/PALETTE-RULES.md`](themes/PALETTE-RULES.md) — the color rule and its guard.
7. [`docs/LAYOUT-SYSTEM.md`](docs/LAYOUT-SYSTEM.md) — the page model (equal margins, header-flows /
   footer-pins, content-fit).
8. The command you're running — [`.claude/commands/`](.claude/commands/) (see the table below).

**Fire up the Design Hub:** `python -m pdf_tool.preview` → http://127.0.0.1:8787/ (on workspace open the
folder task runs `scripts/ensure-design-hub.ps1` — starts the hub if needed, opens the browser; accept the
"allow automatic tasks" prompt the first time). **One-time setup:** `pip install -e ".[dev]" && playwright install chromium`.

**Active plan (one):** [`Plans/_Active/2026-07-14-professional-product-roadmap.md`](Plans/_Active/2026-07-14-professional-product-roadmap.md) · index [`Plans/README.md`](Plans/README.md).

---

## What this repo does

Local-first PDF/document toolkit. Two layers:

1. **`pdf_tool`** — the engine. Render HTML → PDF via headless Chromium, merge PDFs, render PDF → PNG,
   guard the palette, validate a vault, build collages, serve a previewer. Deterministic: what a browser
   prints is what you get.
2. **The résumé layer** — a *protocol*, not a module. The job-application workflow lives in
   [`.claude/commands/`](.claude/commands/) (agent-agnostic markdown), backed by plain JSON in `storage/`
   and the guards (`check_vault`, `check_ats`, `check_palette`). The judgment can't be coded; the data is
   the product. See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

**Reads no environment variables. Makes no network calls.** Every knob is a CLI flag or a constant —
which is why there is no `.env` (one would be a fiction).

---

## Commands the agent runs (the engine)

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
python -m pdf_tool.check_overflow <doc>.html --pdf-theme dark   # ⭐ overflow guard — page fits its box; auto-warns on export
python -m pdf_tool.check_vault --all                            # vault schema — catches invisible claims
python -m pdf_tool.check_vault --explain <user> <track>         # ranked claims preview (blocks on schema/thin)
python -m pdf_tool.check_vault --coverage <user> <track> <listing.md>  # listing gap-check
python -m pdf_tool.check_ats <resume-light.pdf>                 # ATS text-layer guard
python -m pdf_tool.tracker list                                 # scan storage/applications/**/application.json
python -m pdf_tool.tracker status                               # status breakdown (optional filter arg)
python -m pdf_tool.collage --list-recipes                       # named layout recipes (layouts/collage/)
python -m pdf_tool.collage <imagesDir> --recipe <id> --png      # render a named recipe
python -m pdf_tool.collage <imagesDir> --layout auto --png      # every family + picker gallery (--fit contain for screenshots)
python -m pdf_tool.preview --no-open --port 8787                # Design Hub server (127.0.0.1; docs/PREVIEWER.md)
node scripts/wcag-resume-palettes.mjs                           # optional WCAG contrast spot-check (add --strict to fail)
```

`pip install -e .` makes `pdf_tool` importable **from the repo root** (else run from `src/` or set
`PYTHONPATH=src`). Exports default to `_exports/` beside the source HTML and **never overwrite** (auto
`-v2`, `-v3`). Default dual-mode names: `<stem>-light.pdf` (ATS) and `<stem>-dark.pdf` (branded).
**Verification without a screen:** export, then `pdf_to_png` and *read* the PNGs — the intended agent loop.

Full command/export recipes: [`docs/EXPORTS.md`](docs/EXPORTS.md).

---

## Slash commands (the protocol)

Project-scoped commands live in [`.claude/commands/`](.claude/commands/) and travel **with the repo** —
any agent working here picks them up; no global install. Each is plain markdown (no vendor APIs, no
`SKILL.md` folders) — **Codex/Cursor/Copilot/a local model can all just read and follow the file.** If your
agent doesn't auto-load them: *"read `.claude/commands/make-resume.md` and follow it."*

| Command | Tracked? | What it does |
|---|---|---|
| `make-resume.example.md` | ✅ public seed | The generalized application builder — résumé + (opt-in) cover letter + work-samples. Company research, **REMOTE + PAY verification**, **gap-check (ask, don't assume)**, a company-derived theme, light+dark PDFs. |
| `make-collage.md` | ✅ public | General collage / layout builder over the `layouts/` + `themes/` recipes. No private data. |
| `README.md` | ✅ public | Points here. |
| `make-resume.md` | 🔒 personal | Your copy of the builder with the real specifics. |
| `make-cover-letter.md` | 🔒 personal | Standalone cover-letter build (reuses make-resume). |
| `make-work-examples.md` | 🔒 personal | Standalone work-samples / portfolio build. |

### 📎 Public seed vs. personal copy — the `.example` split

| File | Tracked? | Contains |
|---|---|---|
| `<name>.example.md` | ✅ yes | The **generalized** command. No real client names, employers, emails. Safe to clone/share — the public seed. |
| `<name>.md` (bare) | ❌ gitignored | **Your** copy with the concrete specifics (the real company that burned you, the real contacts). |

You type `/make-<name>`; the assistant runs the bare `<name>.md` when it exists, else the tracked
`.example.md`. Same idea as the repo's `*.example` data files: the shareable shape is tracked, the real
content stays in the gitignored `storage/` vault. (This replaced the older `.local.md` convention.)

---

## Repo map

| Path | What it is |
|---|---|
| `src/pdf_tool/` | the engine (html_to_pdf, variants, tracker, merge_pdfs, pdf_to_png, check_palette, check_overflow, check_vault, check_ats, collage, preview) |
| `themes/default-resume.{json,css}` | public default theme — JSON is the token SSOT, CSS its mirror |
| `themes/presets/*.json` | public audition palettes (Design Hub swapper) |
| `themes/PALETTE-RULES.md` | ⭐ **the color rule** (no brown/mustard/lime) + how the guard enforces it |
| `themes/default-collage.json` | collage canvas presets + `backgrounds` (gradients) + per-bg `frame` colors ([`docs/COLLAGE-DESIGN.md`](docs/COLLAGE-DESIGN.md)) |
| `layouts/` | ⭐ **STRUCTURE registry** — reusable layout recipes (`collage/`, `resume/`); counterpart to `themes/` (color). See [`layouts/README.md`](layouts/README.md). |
| `examples/brands/` | tracked **template** for private brand maps (copy → `storage/brands/`) |
| `examples/profiles/<id>/` | one profile per document type: `profile.json` + reference `.html` + example data |
| `examples/applications/` | one-folder-per-job-application workflow + copyable template |
| `docs/` | ARCHITECTURE · SSOT · WHITE-LABEL · STORAGE · VAULT · JOB-ASSESSMENT · THEME-DESIGN · LAYOUT-SYSTEM · EXPORTS · COLLAGE-DESIGN · PREVIEWER · APPLICATIONS · LICENSING-NOTES ([`docs/README.md`](docs/README.md) is the index) |
| `.config/mcp-pdf-designer.json` | project config — **breakpoint SSOT pointer** + hub/palette/layout/collage/voice pointers. Clone-safe: `.config/mcp-pdf-designer.example.json` |
| `Plans/_Active/` | ⭐ the working roadmap (one file) — see [`Plans/README.md`](Plans/README.md) |
| `storage/` | ⛔ **gitignored** local workspace: vaults, real applications, real image sets, private brands |

### Privacy split (do not blur this)

| Public / tracked (safe to clone) | Private / gitignored (`storage/`) |
|---|---|
| `src/pdf_tool/`, `themes/`, `examples/`, `docs/`, `AGENTS.md`, `*.example.md` | `users/`, `*/resume-source.json`, `profiles/*-resume.json`, `applications/`, `brands/`, `_exports/` |
| Brand-neutral default theme | Real brand maps (`brand-jenninexus`, `brand-martian`, `brand-synagen`) |
| Example brand shape (`examples/brands/`) | Real vault claims, contacts, employer research |
| Public seed commands (`*.example.md`, `make-collage.md`) | Personal commands (bare `make-resume.md` / `make-cover-letter.md` / `make-work-examples.md`), `.codex/`, `dev-log-*.yaml` |

`themes/` is deliberately **public** — it's the engine's default theme + palette rule a fresh clone needs
to render. Private brand palettes live in `storage/brands/`, read by the previewer alongside `themes/`.
Website kits own **live-site** colors; for résumé exports the mapped `storage/brands/brand-*.json` is the
**only** pdf-designer color SSOT — `users/*.json` points via `brandTheme.ssot`; never duplicate hex there.

### The application workflow lives in `storage/` (gitignored)

Four layers, each answering one question. **The vault is the brain.**

| Layer | File | Answers |
|---|---|---|
| Person | `storage/users/<user>.json` | **who** — contact, `brandTheme.ssot`, **`characterVoice`**, `hardFacts` |
| **Vault** ⭐ | `storage/<user>/resume-source.json` | **what may be truthfully claimed** · application `voice` · roleTracks |
| Profile | `storage/profiles/<user>-resume.json` | **how** it renders (one per person) · `workSamples` |
| Application | `storage/applications/<Track>/` | **the job** — listing, apply link, pay, company palette |

Read [`docs/VAULT.md`](docs/VAULT.md) before authoring any resume claim.

---

## Contracts (do not break)

- **Geometry is locked.** Résumés/letters are US Letter 8.5×11 with **equal margins on all four edges** —
  default `@page { size: Letter; margin: 0.65in; }` (a doc may open it wider, e.g. 0.75in for a formal
  cover letter, but it must stay equal). Palette changes never change paper size, margins, or pagination.
  Layout model: [`docs/LAYOUT-SYSTEM.md`](docs/LAYOUT-SYSTEM.md).
- **Content must FIT its box.** Each page's content fits (~9.7in at the default) or the pinned signature
  collides with the last lines. `check_overflow` enforces this (auto-warns on export). Fix by **moving a
  section to the next page**, never by shrinking the margin.
- **Dual mode is intentional.** Every document supports light print (`@media print` default, ATS-safe)
  AND dark branded (`html[data-pdf-theme="dark"]`). Keep both working when editing a template.
- **Token names.** `--bg, --surface, --elevated, --text, --dim, --dim2, --border, --border2, --primary,
  --secondary, --accent, --support`. External palettes get *mapped into* these
  ([`docs/THEME-DESIGN.md`](docs/THEME-DESIGN.md)).
- **Palette rule.** **No brown, no mustard, no puke/lime green.** Amber has no readable dark form on white
  (darkening turns it brown); hand that role to another hue on the light palette. Enforced by
  `check_palette` — **run before every export.** Full rule: [`themes/PALETTE-RULES.md`](themes/PALETTE-RULES.md).
- **Source-backed only.** Never write a résumé claim not in the user's vault. Employer-specific framing
  goes in the **cover letter**, never the résumé body.
- **🛑 Ask before calling something a gap.** The vault records what the user *told* you — not the limit of
  what they can do. If a listing needs something the vault lacks, **ask first**; if they have it, write it
  into the vault, then use it. (`doNotClaim` = *"not yet confirmed"*, not *"can't do it"* — Maya and ZBrush
  sat there for months while both founders had years with each.)
- **Emails — the default is the default.** Each person file has one `contact.emailRules.default`. Use it,
  every time, automatically. A personal gmail on record is **recognition, not authorization**.
- **No auto-submission.** Prepare materials; the human submits.
- **Privacy split.** `storage/`, `*.pdf`, `*.png`, `_exports/`, non-`.example` source/capture files, and
  the personal `.md` commands are gitignored. Never move real personal data into tracked paths.

---

## Common tasks → recipes

- **Full job application:** run **`/make-resume <user> <application-dir>`** — the whole routine (capture
  the apply link → verify remote/pay → **gap-check and ask** → derive the theme → write → export résumé +
  cover letter + work samples, light+dark → log it). Folders are keyed by **role track**
  (`storage/applications/3D-Visualizer/`), not by date. Protocol:
  [`docs/JOB-ASSESSMENT.md`](docs/JOB-ASSESSMENT.md).
- **Just one document:** `/make-cover-letter` or `/make-work-examples` (personal) rebuild a single
  deliverable when the résumé already exists.
- **New document type / profile:** copy `examples/profiles/default-resume/` (or `default-collage/`) to a
  new `examples/profiles/<id>/` (public example) or under `storage/` (real/private).
- **Add a person:** `storage/users/<name>.json` + `storage/<name>/resume-source.json` +
  `storage/profiles/<name>-resume.json`. See [`docs/STORAGE.md`](docs/STORAGE.md).
- **Collage:** images in `storage/collages/<project>/images/`, then `--recipe <id>` or `--layout auto
  --png`. **Screenshots need `--fit contain`.** Serve the picker via the Design Hub. Routine:
  [`/make-collage`](.claude/commands/make-collage.md); families: [`docs/COLLAGE-DESIGN.md`](docs/COLLAGE-DESIGN.md).
