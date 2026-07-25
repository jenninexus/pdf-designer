# Active plan + next-agent handoff — pdf-designer

**Single active plan** (2026-07-21). Supersedes the archived
[`../_Archive/2026-07-14-professional-product-roadmap.md`](../_Archive/2026-07-14-professional-product-roadmap.md)
wave (public path · QA · packaging spike · paid-app design — all shipped).

| Pointer | Role |
|---|---|
| **This file** | Working checklist + paste-ready next-agent prompt |
| [`docs/ROADMAP.md`](../../docs/ROADMAP.md) | Thin pointer here (`/jen:roadmap`) |
| [`docs/PRODUCT.md`](../../docs/PRODUCT.md) | Free GitHub vs paid app · shell-over-Hub |
| [`docs/PACKAGING.md`](../../docs/PACKAGING.md) | Wheel must ship `themes/` + `layouts/` |
| [`docs/WHITE-LABEL.md`](../../docs/WHITE-LABEL.md) | Public clone how-to (not the business plan) |
| [`docs/QA.md`](../../docs/QA.md) | Ship gate — judge the artifact |
| [`docs/PREVIEWER.md`](../../docs/PREVIEWER.md) | Design Hub |
| [`../README.md`](../README.md) | Plans index |

---

## Remaining checklist

- [ ] **TestPyPI dry-run** — bump version if needed → `python scripts/check-wheel-assets.py` PASS → upload TestPyPI → fresh-venv install proof. Do **not** claim production PyPI until that works.
- [ ] **Hub recipe-gallery UX** — browse `layouts/` + `themes/presets/` inside Design Hub (paid-shell precursor; still one renderer)
- [x] **Hub vault overview** (2026-07-24) — `/vault` + `GET /api/vault-overview` reads users / profiles / `boardSkills` / `goToPacks` (see `2026-07-24-jenni-vault-hub-handoff.md`)
- [ ] Keep **SSOT + QA docs** honest as the engine evolves
- [ ] Optional: document meet-jenni-bot / syn-themes collage recipes in `docs/COLLAGE-DESIGN.md` (paths stay private under `storage/`)
- [ ] Optional: Synagen engine promo screenshots → `storage/shade/resources/images/synagen/`

### Parked

- [ ] **pywebview shell** — parked; shell-over-Hub first ([archived](../_Archive/2026-07-11-design-hub-parked-phases.md))

### Never

- Auto-submit applications · cloud-only PII · invent claims · fork the renderer

---

## Shipped in prior wave (do not redo)

Full history: [`../_Archive/2026-07-14-professional-product-roadmap.md`](../_Archive/2026-07-14-professional-product-roadmap.md).

Highlights: `check_generation` (10 checks) · white-label smoke · dark-PDF specificity fix ·
`paths.repo_root` + wheel share pipeline · shell-over-Hub design in PRODUCT.md.

### Also landed (2026-07-22…24) — docs / ops

- Personal palette prefs: `storage/brand-design/brand-*.json` + `docs/SSOT.md` § Personal palette prefs
  (MG dark roles lockstep with live site — primary `#FF6B00` · secondary `#8B5CF6` · accent `#FF4500`)
- Project wrap: `.claude/commands/pdf-wrap.md` (`/jen:wrap` routes here)
- BEE `C:\p\pdf-designer` GitHub sync via deploy key; private brand maps via SEGO→BEE SMB

### Netflix — CLOSED (do not touch)

Both founders' Netflix applications are **SUBMITTED**. Keep any `storage/_job-listings/Netflix*`
folders / schemas / templates in place for history — **do not delete**. Do **not** reopen,
rebuild, re-export, re-theme, gap-check, or re-apply Netflix work unless the human **explicitly**
asks in this session. Default: ignore Netflix entirely.

---

## Prompt (copy into a new chat)

```
You are continuing work on C:\Github\pdf-designer (local-first PDF/document toolkit).

## Mission
Improve this repo as both (1) a polished free/open GitHub product and (2) a foundation for a
future paid desktop app (PowerPoint / collage-maker class UX), without breaking the privacy
split or inventing a second renderer.

## Read first (in order)
1. AGENTS.md
2. docs/SSOT.md
3. docs/PRODUCT.md          ← business direction + shell-over-Hub
4. docs/PACKAGING.md        ← PyPI/wheel rules (themes+layouts must ship in the wheel)
5. docs/WHITE-LABEL.md      ← public clone path ONLY (not the business plan)
6. docs/QA.md               ← judge the ARTIFACT; check_generation is the ship gate
7. docs/ROADMAP.md → Plans/_Active/2026-07-21-next-agent-product-prompt.md  ← ⭐ active plan
8. docs/PREVIEWER.md        ← Design Hub (recipe gallery lands here)
9. docs/THEME-DESIGN.md     ← trap: prefers-color-scheme must be screen-scoped

## Product constraints (do not violate)
- MIT engine stays free; storage/ vaults + real applications stay gitignored forever.
- No auto-submit applications; no cloud-only PII as default.
- One renderer: pdf_tool (Playwright/Chromium). A paid app = thin shell + recipes, not a fork.
- Palette rule + generation QA stay mandatory (docs/QA.md, themes/PALETTE-RULES.md).
- Prior wave archived: Plans/_Archive/2026-07-14-professional-product-roadmap.md — history only.

## What already shipped (don't redo)
- check_generation (10 checks) + rendered-color + footer-collision known-bad fixture
- Shared studio MG gallery (WebP) + junctions from jenni/shade
- Public 5-minute path: README + docs/WHITE-LABEL.md + scripts/smoke-white-label.py
- Dark-PDF fix: @media screen and (prefers-color-scheme: light)
- Paid-app DESIGN spike: shell-over-Hub in docs/PRODUCT.md (pywebview stays parked)
- PyPI/wheel SPIKE: pdf_tool.paths.repo_root + scripts/sync-wheel-share.py +
  scripts/check-wheel-assets.py + docs/PACKAGING.md

## Netflix — CLOSED (ignore unless human explicitly asks)
- Jenni + Shade Netflix apps already SUBMITTED (separate accounts).
- Keep storage/_job-listings/Netflix* schemas/templates — do NOT delete.
- Do NOT rebuild, re-export, re-theme, gap-check, or re-apply. Default: ignore Netflix.

## Prove public path still green (30s)
python scripts/smoke-white-label.py
# When touching install/wheel:
python scripts/check-wheel-assets.py

## Suggested workstream (pick 1–2, finish, verify)
T. TestPyPI dry-run — version bump if needed, check-wheel-assets PASS, upload TestPyPI,
   fresh-venv install proof. No production PyPI claim until that works.
G. Design Hub recipe-gallery UX — browse layouts/ + themes/presets/ inside the Hub
   (paid-shell precursor; still one renderer).
D. Optional: collage/resume recipe polish or COLLAGE-DESIGN private-path examples.

## Verification
- python -m pdf_tool.check_generation on any doc you touch
- python scripts/smoke-white-label.py (tracked files only)
- python scripts/check-wheel-assets.py when packaging changes
- Commit tracked docs/code only; never commit storage/ or generated
  src/pdf_tool/share/{themes,layouts,examples}/
- Windows consoles are often cp1252 — keep script print() ASCII

## Out of scope
- Netflix (CLOSED — both submitted; keep files, ignore unless human asks)
- Moving real PII into tracked paths
- Auto-applying to jobs
- Re-opening pywebview vs Electron (decision: shell-over-Hub first)
```

---

## Context for humans

| Clarification | Truth |
|---|---|
| Is WHITE-LABEL the business plan? | **No.** Public reuse how-to. Business = `docs/PRODUCT.md`. |
| Where is the active checklist? | **This file** (`Plans/_Active/2026-07-21-…`) |
| Where did the old roadmap go? | `Plans/_Archive/2026-07-14-professional-product-roadmap.md` |
| Netflix? | **Closed.** Both submitted. Keep schemas; agents ignore unless you ask. |
| Packaging SSOT | `docs/PACKAGING.md` |
| Observable proof | `python scripts/smoke-white-label.py` → PASS · Hub http://127.0.0.1:8787/ |
