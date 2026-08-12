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
2. ⭐ [`.memory/README.md`](.memory/) — **the traps already hit here, and why.** Tracked, so it
   travels with every clone. Read it before your first substantive change: each `lesson-*.md` is a
   mistake someone already paid for (a guard whose assumption was wrong, a true claim that went
   invisible, a "gap" nobody had asked about). Cheapest file in the repo.
3. [`docs/SSOT.md`](docs/SSOT.md) — the SSOT dashboard (what this repo owns vs. points elsewhere).
4. [`docs/VAULT.md`](docs/VAULT.md) — **the vault**: what may be claimed, how each person sounds
   (`characterVoice` + vault `voice`), the capability matrix, the role tracks.
5. [`docs/JOB-ASSESSMENT.md`](docs/JOB-ASSESSMENT.md) — how to assess a listing (apply URL is blocking;
   remote? pay vs. market?; the evidence map).
6. [`docs/STORAGE.md`](docs/STORAGE.md) — the four private layers and the `storage/` layout.
7. [`themes/PALETTE-RULES.md`](themes/PALETTE-RULES.md) — the color rule and its guard.
8. [`docs/LAYOUT-SYSTEM.md`](docs/LAYOUT-SYSTEM.md) — the page model (equal margins, header-flows /
   footer-pins, content-fit).
9. The command you're running — [`.claude/commands/`](.claude/commands/) (see the table below).

**Fire up the Design Hub:** `python -m pdf_tool.preview` → http://127.0.0.1:8787/ (on workspace open the
folder task runs `scripts/ensure-design-hub.ps1` — starts the hub if needed, opens the browser; accept the
"allow automatic tasks" prompt the first time). **One-time setup:** `pip install -e ".[dev]" && playwright install chromium`.

**Public-path smoke (no `storage/`):** `python scripts/smoke-white-label.py` — QA + light/dark PDF + ATS on
`examples/profiles/default-resume/`. Checklist: [`docs/WHITE-LABEL.md`](docs/WHITE-LABEL.md). Product
direction (free GitHub vs paid app): [`docs/PRODUCT.md`](docs/PRODUCT.md). Packaging / wheel gate:
[`docs/PACKAGING.md`](docs/PACKAGING.md) · `python scripts/check-wheel-assets.py` ·
`python scripts/testpypi-dry-run.py` (local wheel proof; `--upload` needs `TESTPYPI_TOKEN`).

**Active plan (one):** [`Plans/_Active/2026-08-12-product-privacy-packaging.md`](Plans/_Active/2026-08-12-product-privacy-packaging.md) · index [`Plans/README.md`](Plans/README.md). Completed waves: [`Plans/_Complete/`](Plans/_Complete/).

**Session start / wrap:** `/start` → local [`.claude/commands/start.md`](.claude/commands/start.md)
(gitignored). `/wrap` → local [`.claude/commands/wrap.md`](.claude/commands/wrap.md) — **requires
`/reflect`** + next-agent handoff (`/jen:wrap` routes here too). Public protocol seeds:
`.claude/commands/*.example.md`. Palette prefs: [`docs/SSOT.md`](docs/SSOT.md) § Personal palette prefs ·
private maps in `storage/brand-design/`. Product front door: [`examples/resume-studio/`](examples/resume-studio/).

**Where learnings go — two surfaces, do not confuse them.** `dev-log-sego.yaml` is **gitignored**, so
a lesson recorded only there is invisible to every other clone and to the next agent. Durable
lessons — a trap, its root cause, and the guard that now prevents it — go to **tracked**
[`.memory/lesson-*.md`](.memory/) with a row in [`.memory/README.md`](.memory/README.md). Session
narrative (what happened today, next steps) stays in the dev-log. If the lesson changes a standing
rule, edit the owning `docs/` page **as well**.

**Netflix — CLOSED:** both founders submitted. Keep any `storage/_job-listings/Netflix*` schemas —
do not delete. Do not reopen/rebuild/re-apply unless the human explicitly asks.

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
python -m pdf_tool.pdf_to_png <doc>.html                        # one PNG per page (visual verify; HTML source)
python -m pdf_tool.check_generation <doc>.html                  # ⭐ ONE QA gate — 10 checks; run before EVERY ship
python -m pdf_tool.check_generation --scan storage/<user>/defaults  #    sweep go-to set
python -m pdf_tool.check_palette <doc>.html                     # palette only (also inside check_generation)
python -m pdf_tool.check_palette --scan storage/                #    sweep a whole tree
python -m pdf_tool.check_overflow <doc>.html --pdf-theme dark   # overflow only (also inside check_generation)
python -m pdf_tool.check_vault --all                            # vault schema — catches invisible claims
python -m pdf_tool.check_vault --explain <user> <track>         # ranked claims preview (blocks on schema/thin)
python -m pdf_tool.check_vault --coverage <user> <track> <listing.md>  # listing gap-check
python -m pdf_tool.check_ats <resume-light.pdf>                 # ATS text-layer guard
python -m pdf_tool.tracker list                                 # scan storage/_job-listings/**/application.json
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

Project-scoped commands live in [`.claude/commands/`](.claude/commands/). **GitHub tracks only
`*.example.md`** — session ritual (`start` / `wrap` / `README`) and bare `make-*.md` stay
**local / gitignored** (SEGO workspace). Any agent on this machine reads the bare file when
present; a fresh public clone uses the `.example.md` seeds. Plain markdown — no vendor APIs.
If an agent doesn't auto-load them: *"read `.claude/commands/make-resume.md` (or the `.example`)
and follow it."*

| Command | Tracked? | What it does |
|---|---|---|
| `make-resume.example.md` | ✅ public seed | Résumé builder — vault + skills + palette; REMOTE + PAY + gap-check + company theme |
| `make-cover-letter.example.md` | ✅ public seed | Standalone cover letter (not auto-bundled with resume) |
| `make-work-examples.example.md` | ✅ public seed | Standalone work-samples / portfolio |
| `make-collage.example.md` | ✅ public seed | Collage / layout builder over `layouts/` + `themes/` |
| `start.md` · `wrap.md` · `pdf-wrap.md` · `README.md` | 🔒 **dev-only** (gitignored) | Session start/wrap + local index — include `/reflect`; never push |
| `make-resume.md` · `make-cover-letter.md` · `make-work-examples.md` · `make-collage.md` | 🔒 personal (gitignored) | Your copies with real specifics |

**Applicant shorthand** (local `README.md` when present; else `/jen:pdf` applicant table).
`/shade` · `/jenni` · `/studio` · `/martian` · `both` resolve vault + profile + export dir.

**Global commands in scope here** (personal, `~/.claude/commands/`, not in this repo): **`/pdf`**
· **`/voice`** · **`/reflect`** (`jen/reflect-universal` — required at wrap) · `/roadmap` →
[`docs/ROADMAP.md`](docs/ROADMAP.md).

### 📎 Public seed vs. personal / dev copy — the `.example` split

| File | Tracked? | Contains |
|---|---|---|
| `<name>.example.md` | ✅ yes | Generalized protocol. No real clients, employers, emails, machine paths. |
| `<name>.md` (bare) | ❌ gitignored | Personal specifics **or** SEGO session ritual (`start`/`wrap`). |

You type `/make-<name>`; the assistant runs the bare `<name>.md` when it exists, else the tracked
`.example.md`. Same idea as `*.example` data files and `.config/*.example.json`.

**Public product entry (examples only):** [`examples/resume-studio/`](examples/resume-studio/) —
marketed résumé-creator demo path (vault shape + palettes + smoke), not private vaults.

---

## Repo map

| Path | What it is |
|---|---|
| `.memory/` | ⭐ **tracked durable learnings** — one `lesson-*.md` per trap already hit here (root cause + the guard that now prevents it) + an index. Read at session start; written at wrap. Travels with every clone, unlike the gitignored dev-log. |
| `src/pdf_tool/` | the engine (html_to_pdf, variants, tracker, merge_pdfs, pdf_to_png, **check_generation**, check_palette, check_overflow, check_rendered_color, check_vault, check_ats, collage, preview) |
| `themes/default-resume.{json,css}` | public default theme — JSON is the token SSOT, CSS its mirror |
| `themes/presets/*.json` | public audition palettes (Design Hub swapper) |
| `themes/PALETTE-RULES.md` | ⭐ **the color rule** (no brown/mustard/lime) + how the guard enforces it |
| `themes/default-collage.json` | collage canvas presets + `backgrounds` (gradients) + per-bg `frame` colors ([`docs/COLLAGE-DESIGN.md`](docs/COLLAGE-DESIGN.md)) |
| `layouts/` | ⭐ **STRUCTURE registry** — document recipes under `layouts/{cover-letter,letter,resume,work-examples}/` + `layouts/collage/`; counterpart to `themes/` (color). See [`layouts/README.md`](layouts/README.md). |
| `examples/brand-design/` | tracked **template** for private brand maps (copy → `storage/brand-design/`) |
| `examples/profiles/<id>/` | one profile per document type: `profile.json` + reference `.html` + example data |
| `examples/resume-studio/` | ⭐ **public product entry** — marketed résumé-creator demo (links vault/palette/skills shapes) |
| `examples/_job-listings/` | one-folder-per-job-application workflow + copyable template |
| `docs/` | ARCHITECTURE · SSOT · PRODUCT · PACKAGING · WHITE-LABEL · STORAGE · VAULT · JOB-ASSESSMENT · THEME-DESIGN · LAYOUT-SYSTEM · EXPORTS · COLLAGE-DESIGN · PREVIEWER · APPLICATIONS · LICENSING-NOTES ([`docs/README.md`](docs/README.md) is the index) |
| `.config/mcp-pdf-designer.example.json` | ⭐ Tracked project config **seed** (breakpoints + hub/palette/layout pointers). Copy → local `mcp-pdf-designer.json` (gitignored — machine paths). |
| `Plans/_Active/` | ⭐ the working roadmap (one file) — see [`Plans/README.md`](Plans/README.md) |
| `storage/` | ⛔ **gitignored** local workspace: vaults, real applications, real image sets, private brands |
| `storage/studio/resources/images/martiangames/` | ⭐ **shared** MG title gallery (WebP) — both applicants; see [`docs/STORAGE.md`](docs/STORAGE.md) |

### Privacy split (do not blur this)

| Public / tracked (safe to clone) | Private / gitignored (`storage/`) |
|---|---|
| `src/pdf_tool/`, `themes/`, `examples/`, `docs/`, `AGENTS.md`, `*.example.md` | `users/`, `*/resume-source.json`, `profiles/*-resume.json`, `_job-listings/`, `brand-design/`, `studio/resources/`, `_exports/` |
| Brand-neutral default theme | Real brand maps (`brand-jenninexus`, `brand-martian`, `brand-synagen`) |
| Example brand shape (`examples/brand-design/`) | Real vault claims, contacts, employer research |
| Public seed commands (`*.example.md` only) | Bare commands (`start`/`wrap`/`make-*`/`README`), `.codex/`, `dev-log-*.yaml` |

`themes/` is deliberately **public** — it's the engine's default theme + palette rule a fresh clone needs
to render. Private brand palettes live in `storage/brand-design/`, read by the previewer alongside `themes/`.
Website kits own **live-site** colors; for résumé exports the mapped `storage/brand-design/brand-*.json` is the
**only** pdf-designer color SSOT — `users/*.json` points via `brandTheme.ssot`; never duplicate hex there.

### The application workflow lives in `storage/` (gitignored)

Four layers, each answering one question. **The vault is the brain.**

| Layer | File | Answers |
|---|---|---|
| Person | `storage/users/<user>.json` | **who** — contact, `brandTheme.ssot`, **`characterVoice`**, `hardFacts` |
| **Vault** ⭐ | `storage/<user>/resume-source.json` | **what may be truthfully claimed** · application `voice` · roleTracks |
| Profile | `storage/profiles/<user>-resume.json` | **how** it renders (one per person) · `workSamples` |
| Application | `storage/_job-listings/<Track>/` | **the job** — listing, apply link, pay, company palette |

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
- **Board upload = light PDF (UNIVERSAL).** Every profile (`jenni` · `shade` · `studio` · `martian`)
  ships `*-resume-light.pdf` + `*-resume-dark.pdf`. Upload **light** to Jobright / Indeed / LinkedIn.
  Gate: `python -m pdf_tool.check_ats <light.pdf>` (contiguous cues + mid-word splits). Print body +
  `h2` on a system font. Jobright content rank ≠ parse fail. SSOT:
  [`docs/JOB-ASSESSMENT.md`](docs/JOB-ASSESSMENT.md) § Tier 4.5 ·
  `examples/profiles/default-resume/profile.json#verify.atsParse` · each
  `storage/profiles/<user>-resume.json#exports.exportPrefs`.
- **Token names.** `--bg, --surface, --elevated, --text, --dim, --dim2, --border, --border2, --primary,
  --secondary, --accent, --support`. External palettes get *mapped into* these
  ([`docs/THEME-DESIGN.md`](docs/THEME-DESIGN.md)).
- **Palette rule.** **No brown, no mustard, no puke/lime green.** Amber has no readable dark form on white
  (darkening turns it brown); hand that role to another hue on the light palette. Enforced by
  `check_palette` (and by `check_rendered_color` for brown that only appears after compositing).
  Full rule: [`themes/PALETTE-RULES.md`](themes/PALETTE-RULES.md).
- **QA gate.** **`python -m pdf_tool.check_generation <doc>.html` before every ship** — 10 checks
  including artifact-level rendered-color, overflow @ 816px, and footer-collision. Source-only
  greps are not "verified." SSOT: [`docs/QA.md`](docs/QA.md).
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

- **Job résumé:** run **`/make-resume <user> <application-dir|url>`** — capture apply link → verify
  remote/pay → **gap-check and ask** → derive theme → write → export per **`exportPrefs`** (**every**
  profile = **light + dark**; board upload = **light** only) → `check_ats` on the light file → log it.
  Pasted URL with no folder → create `storage/_job-listings/<App>/`.
  Protocol: [`docs/JOB-ASSESSMENT.md`](docs/JOB-ASSESSMENT.md) § Tier 4.5 (parse ≠ Jobright content grade).- **Cover letter / work samples:** `/make-cover-letter` or `/make-work-examples` (personal) — **not**
  auto-bundled with make-resume.
- **`boardSkills`:** when LinkedIn/board tags change → update vault `#boardSkills` (+ claims); preview
  on Design Hub `/vault`.
- **New document type / profile:** copy `examples/profiles/default-resume/` (or `default-collage/`) to a
  new `examples/profiles/<id>/` (public example) or under `storage/` (real/private).
- **Add a person:** `storage/users/<name>.json` + `storage/<name>/resume-source.json` +
  `storage/profiles/<name>-resume.json`. See [`docs/STORAGE.md`](docs/STORAGE.md).
- **Collage / recipes:** images in `storage/collages/<project>/images/`, then `--recipe <id>` or
  `--layout auto --png`. **Screenshots need `--fit contain`.** Browse recipes in the Hub at
  [`/recipes`](http://127.0.0.1:8787/recipes). Routine: [`/make-collage`](.claude/commands/make-collage.md);
  families: [`docs/COLLAGE-DESIGN.md`](docs/COLLAGE-DESIGN.md).
