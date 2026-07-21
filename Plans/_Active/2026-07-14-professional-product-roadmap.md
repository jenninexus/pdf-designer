# Product roadmap — pdf-designer (ACTIVE)

**Single active plan.** Started 2026-07-14 · consolidated 2026-07-14.

| Pointer | Role |
|---|---|
| **This file** | Working checklist — what to build next |
| [`docs/SSOT.md`](../../docs/SSOT.md) | SSOT dashboard (owns vs points elsewhere) |
| [`docs/PRODUCT.md`](../../docs/PRODUCT.md) | ⭐ Free GitHub vs future paid app (business direction) |
| [`docs/WHITE-LABEL.md`](../../docs/WHITE-LABEL.md) | Public-only reuse how-to (not the business plan) |
| [`docs/QA.md`](../../docs/QA.md) | Ship gate — judge the artifact |
| [`docs/PREVIEWER.md`](../../docs/PREVIEWER.md) | Design Hub how-to |
| [`docs/STORAGE.md`](../../docs/STORAGE.md) · [`VAULT.md`](../../docs/VAULT.md) · [`JOB-ASSESSMENT.md`](../../docs/JOB-ASSESSMENT.md) | Protocol SSOT |
| [`2026-07-21-next-agent-product-prompt.md`](2026-07-21-next-agent-product-prompt.md) | ⭐ Paste-ready next-agent handoff (remaining: paid-app / PyPI) |
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
- [x] Brand SSOT = `storage/brand-design/brand-*.json`; users only point
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
- [x] Application tracker CLI (scan `storage/_job-listings/**/application.json`) — `python -m pdf_tool.tracker list|status` (UI stays later / Jobright-inspired)
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

## Shipped recently (2026-07-20) — Netflix apps (both founders) + magenta ban + guards

- [x] **`check_overflow` guard + `overflow:hidden` structural fix.** New `pdf_tool.check_overflow` (headless-Chromium page-fit check, auto-warns on export). The real fix for the pinned-footer overlap is `overflow:hidden` on the print `.page` (clips at the edge, can't bleed onto the next sheet). Ground truth = rasterize the real PDF (pypdfium2), not an HTML re-render. `docs/LAYOUT-SYSTEM.md` updated.
- [x] **Magenta/pink ban** — `check_palette --no-magenta` (opt-in, hue ~290–345°, scoped to Shade + Martian; Jenni's pink is legit). Rebuilt `brand-synagen.json` violet+cyan (was magenta). Tests added. `PALETTE-RULES.md` documents it.
- [x] **Netflix application for BOTH founders** — Jenni submitted 2026-07-19 (portal); Shade's full set built (resume + cover + work-samples, cool-cyan matched-pair run, magenta-free). Split accent runs in the app `theme.json`. `applied-index.md` submission log added.
- [x] **Netflix "spectrum curtain" accent** — magenta-free pure-CSS rainbow band on Shade's docs; ported to `www-theme-kit` `$brand-netflix-spectrum`.
- [x] **Design Hub ↻ Refresh button** — manual re-scan alongside the auto-poll (a tab opened pre-poll could miss new docs).
- [x] **`.page-foot--stacked`** shared theme pattern — a line above the footer lives INSIDE the pinned footer so it can't collide with the signature.

## Shipped recently (2026-07-21) — generation QA subsystem + the real brown fix + storage restructure

> **Governing lesson:** a guard that inspects the SOURCE only catches defects that exist in the source.
> Three defects shipped while every guard said PASS. The QA contract is now *judge the artifact* —
> see the principle box at the top of [`docs/QA.md`](../../docs/QA.md).

- [x] **`pdf_tool.check_generation` — ONE QA gate** for any generated doc: palette · rgba-magenta ·
      casing · image-overlay · signature-pin · equal-margins · page-bg · rendered-color · overflow ·
      footer-collision. Per-user aware (Shade ⇒ no-magenta) and per-doc-type aware (cover letters
      sign off in flow; resumes/work-samples pin bottom-right). CLI + console script; exit 1 on FAIL.
- [x] **`pdf_tool.check_rendered_color` — the brown that isn't in the source.** Renders the page and
      judges PIXELS plus the average of large FLAT background tiles. Ignores text antialiasing (2× +
      greyscale AA + neighbour clustering) and artwork interiors (game art is legitimately amber).
      Control-tested: FAILS the old background, PASSES the fixed one.
- [x] **Root-caused the recurring "it looks brown".** (1) A red-tinted dark-grey background averaged
      `2c2224`/`291c1d` over large areas — every pixel "neutral" to a hex guard, brown to the eye.
      (2) Alpha layers over warm gradients manufactured real brown pixels (`a08251`, `7f4c04`).
      Fix: strictly neutral backgrounds; red only as saturated small accents; **never** an overlay on
      a warm gradient. Documented in `GENERATION-RULES.md` §3b.
- [x] **`check_overflow` was measuring at the wrong page width.** Playwright's default 1280px viewport
      vs Letter's 816px made the same page measure 726px instead of 940px — the guard reported 205px
      of headroom on a page 9px OVER, and a footer overlap shipped. Now pinned to `_LETTER_PX = 816`.
- [x] **Storage restructure** — `applications/`→`_job-listings/`, `brands/`→`brand-design/` (code paths,
      docs, configs, public example fixtures); per-user `resources/images/{martiangames,agency}` +
      `logos/` so every used image travels with the vault; per-user `defaults/` holding a ready-to-send
      resume + cover letter + work-samples; `_archive`/`_exports`/`_submitted` marked never-clean.
- [x] **`themes/GENERATION-RULES.md`** — house rules for ALL generated docs: names/company never
      all-lowercase, no neon over images (dark scrim only), 16:9 no-crop framing, neutral backgrounds,
      one page-background per applicant set.
- [x] **Per-user work-samples SSOT** (`#workSamples` + `#portfolio`) documented in `docs/VAULT.md` — a
      portfolio is built from the applicant's OWN assets (this is what put Jenni's Agency grid on a
      Shade doc).
- [x] **Palette-preview approval gate** — `make-resume` / `make-work-examples` must show the swatch
      table and get a yes BEFORE generating, so a wrong-colour set is never built twice.
- [x] **jenni-resume overflow + signature overlap (816px)** — Studio Capabilities moved to page 2;
      `overflow: hidden` on print `.page`; defaults re-exported. Footer-collision hardened (signature
      = bottom-most right cluster, intrusion window to 0.72) + known-bad control at
      `tests/fixtures/known-bad-footer-overlap.html`. Shade defaults re-verified 10/10 PASS.
- [x] **SSOT sync** — `docs/QA.md` lists all 10 checks; `AGENTS.md` / `docs/SSOT.md` /
      `make-resume.example.md` lead with `check_generation` as the ship gate.
- [x] **Shared MG gallery SSOT** — `storage/studio/resources/images/martiangames/` (WebP);
      per-user `images/martiangames/` = junctions; `users/*/portfolio.workSampleAssets` +
      `docs/STORAGE.md` / `storage/README.md` document the protocol. Air Wars sunset → `.webp`.
- [x] **Shade Netflix work-samples under 5MB** — JPEG/WebP image pipeline for Chromium PDF
      (1.09 MB dark); resume already ~0.21 MB.

## Shipped recently (2026-07-21) — public 5-minute path + dark-PDF specificity fix

- [x] **White-label smoke** — `scripts/smoke-white-label.py` (QA + light/dark export + ATS; no `storage/` required)
- [x] **README 5-minute path** — fresh-clone demo from `examples/` only; [`WHITE-LABEL.md`](../../docs/WHITE-LABEL.md) checklist
- [x] **Public example resume** — 2-page fit (content-fit rule); was overflowing + false footer-collision
- [x] **Dark PDF on light OS preference** — `@media screen and (prefers-color-scheme: light)` so screen tokens cannot outrank `html[data-pdf-theme="dark"]` print tokens (`default-resume.html` + `themes/default-resume.css`)
- [x] **`check_footer_collision` hardened** — sample bg inside the content box; `prefer_css_page_size=True` to match `html_to_pdf`

## Next — public GitHub + product packaging ← **priority**

See [`docs/PRODUCT.md`](../../docs/PRODUCT.md) for free-vs-paid thesis. Engineering checklist:

- [x] **Public-repo readiness (demo path)** — README 5-minute path + smoke script from `examples/` only
- [ ] **PyPI / installer** — package for non-dev users (spike when ready)
- [x] **White-label smoke** — `scripts/smoke-white-label.py` + [`WHITE-LABEL.md`](../../docs/WHITE-LABEL.md) checklist
- [ ] **Paid-app spike (later)** — thin desktop shell over the same engine (installer + recipe gallery); do **not** fork the renderer; privacy split stays absolute
- [ ] Keep SSOT + QA docs honest as the engine evolves
- [ ] Optional: document meet-jenni-bot / syn-themes collage recipes in `docs/COLLAGE-DESIGN.md` examples (paths stay private under `storage/`)
- [ ] Optional: Synagen engine promo screenshots → `storage/shade/resources/images/synagen/` (Shade work-samples)

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
| Private brands | `storage/brand-design/` |
| Claims + app voice | `storage/<user>/resume-source.json` |
| Personality / registers | `storage/users/<user>.json#characterVoice` |
| Voice map / public cards | `C:\Github\voice-seed` (deep edit stays in storage/) |
| Palette rule | `themes/PALETTE-RULES.md` |
| Repo SSOT dashboard | `docs/SSOT.md` |
