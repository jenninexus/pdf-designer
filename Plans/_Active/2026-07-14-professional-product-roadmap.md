# Product roadmap — pdf-designer (ACTIVE)

**Single active plan.** Started 2026-07-14 · consolidated 2026-07-14.

| Pointer | Role |
|---|---|
| **This file** | Working checklist — what to build next |
| [`docs/SSOT.md`](../../docs/SSOT.md) | SSOT dashboard (owns vs points elsewhere) |
| [`docs/WHITE-LABEL.md`](../../docs/WHITE-LABEL.md) | Public-only reusable path |
| [`docs/PREVIEWER.md`](../../docs/PREVIEWER.md) | Design Hub how-to |
| [`docs/STORAGE.md`](../../docs/STORAGE.md) · [`VAULT.md`](../../docs/VAULT.md) · [`JOB-ASSESSMENT.md`](../../docs/JOB-ASSESSMENT.md) | Protocol SSOT |
| [`../_Archive/`](../_Archive/) | Completed / parked plans (hub Phase 1, character voice, pywebview) |

---

## Product thesis

**Local-first career document studio.** Vault-backed claims → tailored HTML →
print-perfect PDF/PNG. Design Hub is the interactive shell; the Python engine is
the only renderer. No MCP / always-on server required for core value.

## Layers (do not blur)

| Layer | Owns | Ships? |
|---|---|---|
| Engine (`pdf_tool`) | export, guards, collage, preview | yes — MIT |
| Public themes | `themes/default-*`, `themes/presets/*` | yes |
| Protocol docs | `docs/*`, `/make-resume` | yes |
| Private workspace | `storage/` vaults, brands, applications | no — gitignored |
| Kit registries | www `resume-palettes`, profiles | yes (pointers) |

---

## Shipped (do not re-open unless regressing)

- [x] Design Hub Phase 1 — preview, filters, palette swap, export
- [x] Compact ~44px toolbar (Syqo/Synagen density)
- [x] Protocol docs in tracked `docs/`; `storage/` private + stubs
- [x] Brand SSOT = `storage/brands/brand-*.json`; users only point
- [x] Public presets (6) + polished `default-resume` + kit catalog
- [x] Breakpoint pointer: `.config/mcp-pdf-designer.json#breakpoints`
- [x] Character voice layers (`users#characterVoice` + vault `#voice`) — see archive
- [x] Guards: `check_palette` on export, `check_vault`, `doNotClaim` ledger
- [x] Wire `check_vault` into `/make-resume` (step 0 blocks on schema / thin track)
- [x] `check_vault --explain` — ranked claims, blocks on schema + thin target track
- [x] `check_vault --coverage` — mechanical listing gap-check (ASK BEFORE GAPS)
- [x] `check_ats` — ATS text-layer guard on light PDF exports
- [x] YouTube-poster / linked portfolio pattern in example resume
- [x] pytest for `check_palette.classify()` + vault ranking + coverage helpers
- [x] Canvas-preset tables reconciled (SSOT: `COLLAGE-DESIGN.md` + `default-collage.json`)
- [x] License decided: MIT (see `LICENSING-NOTES.md`)
- [x] Application tracker CLI (scan `storage/applications/**/application.json`) — `python -m pdf_tool.tracker list|status` (UI stays later / Jobright-inspired)
- [x] Match / coverage report against listing — CLI: `check_vault --coverage` (UI stays with tracker)
- [x] `--variants` palette shopping → `_variants/` (`python -m pdf_tool.variants` / `html_to_pdf --variants`)
- [x] Optional WCAG gate (`node scripts/wcag-resume-palettes.mjs` — document in README/AGENTS; no package.json yet)
- [x] White-label docs path — [`docs/WHITE-LABEL.md`](../../docs/WHITE-LABEL.md)
- [x] SSOT map — [`docs/SSOT.md`](../../docs/SSOT.md) + `.config/mcp-pdf-designer.json` pointers
- [x] CLI hub + console_scripts — `python -m pdf_tool` / `pdf-designer*` entry points

---

## Shipped recently (2026-07-15 → 07-16) — private collage workspace

- [x] **meet-jenni-bot collage pack** under `storage/collages/meet-jenni-bot/` (same family pattern as syn-themes): uniform-grid HD fave + hero-mosaic / filmstrip / square / masonry alts
- [x] Source frames from jenni-bot `storage/screenshots/` (socials `:8777` previewer captures) + exported into JN blog gallery assets
- [x] Collage SSOT unchanged: `docs/COLLAGE-DESIGN.md` + canvas presets — engine already owns layout families

## Shipped recently (2026-07-19) — layout system + live previewer

- [x] **Shared page layout system** — [`docs/LAYOUT-SYSTEM.md`](../../docs/LAYOUT-SYSTEM.md). **Equal margins on all four edges** (default `@page { margin: 0.65in }`); header flows at the top, footer/signature pins to the bottom (`margin-top:auto`). Codified in `themes/default-resume.{json,css}` (one knob `--resume-page-margin`) + the public example resume; applied to the Netflix templates.
- [x] **Content-fit rule + `check_overflow` guard** — each page's content must fit its box (9.7in default) or the pinned signature collides with the last lines. New `pdf_tool.check_overflow` measures every `.page`'s rendered height vs its print box in headless Chromium and fails on overflow; it also auto-warns on every `html_to_pdf` export. Caught a real latent overflow in the public example resume. (Fixed the 2026-07-19 signature-overlap bug so it can never ship again.)
- [x] **Design Hub auto-refresh** — `GET /api/version` (tree signature over HTML + `_exports/**`) + client poller; the previewer re-renders + reloads the open doc when you export a new resume. No restart. (`docs/PREVIEWER.md`.)
- [x] **GitHub-readiness** — `examples/README.md` first-run guide; `.vscode/mcp.json` → gitignored + `.vscode/mcp.json.example`; `ensure-design-hub.ps1` launches hidden + agnostic (`python` from PATH); `.vscode/tasks.json` uses `${workspaceFolder}` (no hardcoded paths).
- [x] **Work-samples doc type** — visual portfolio PDF (self-contained base64 images) for "Additional Documents" uploads; profile contract in `profiles/<user>-resume.json#workSamples`.

## Shipped recently (2026-07-20) — repo org for public seed

- [x] **Command surface split for GitHub.** Public seed = `*.example.md` (tracked); personal copies =
  bare `<name>.md` (gitignored). Retired the `.local.md` convention. `make-resume.md` untracked
  (`git rm --cached`); added personal `/make-cover-letter` + `/make-work-examples` (reuse make-resume).
  `/make-resume` default is now the full application (résumé + cover letter + work samples), owner directive.
- [x] **Single agent SSOT.** Consolidated `AGENTS.md` + `CLAUDE.md` + `.claude/commands/README.md` into one
  `AGENTS.md`; the other two are thin pointers. Fixes the "root files go stale" problem — one file to edit.
- [x] **`.codex/` retired.** Stale generated `SKILL.md` mirrors removed; `.codex/` gitignored — no more
  dual-maintenance of Codex + Claude copies. Codex reads `.claude/commands/*.md` directly.
- [x] **`/jen:roadmap` wired** — `docs/ROADMAP.md` pointer resolves to this plan (no duplicate roadmap).
- [x] **gitignore hardened** — `dev-log-*.yaml` (per-machine private log) now ignored.

## Next — maintenance / PyPI when going public ← **priority**

- [ ] PyPI / installer for non-dev users (when going public)
- [ ] Keep SSOT + white-label docs honest as the engine evolves
- [ ] Optional: document meet-jenni-bot / syn-themes collage recipes in `docs/COLLAGE-DESIGN.md` examples (paths stay private under `storage/`)

## Later / parked

- [ ] pywebview shell — **parked.** Design Hub browser (`python -m pdf_tool.preview`) is the interactive SSOT; revive only on demand ([archived detail](../_Archive/2026-07-11-design-hub-parked-phases.md))

## Never

- **Never:** auto-submit applications; cloud-only PII; invent claims

---

## Contracts (quick)

| Concern | SSOT |
|---|---|
| Breakpoints | `.config/mcp-pdf-designer.json#breakpoints` → mcp-breakpoints → www SCSS |
| Public palettes | `themes/` + `themes/presets/` |
| Private brands | `storage/brands/` |
| Claims + app voice | `storage/<user>/resume-source.json` |
| Personality / registers | `storage/users/<user>.json#characterVoice` |
| Voice map / public cards | `C:\Github\voice-seed` (deep edit stays in storage/) |
| Palette rule | `themes/PALETTE-RULES.md` |
| Repo SSOT dashboard | `docs/SSOT.md` |
