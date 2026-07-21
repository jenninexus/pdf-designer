# Handoff prompt — next agent (copy into a new chat)

> **Status:** ready to paste (refreshed 2026-07-21 wrap #2). Workstreams **A + B + C(design) + P(spike)** shipped.
> Pick **TestPyPI dry-run** and/or **Hub recipe-gallery UX**; optional collage recipe polish (D).
> Private Netflix/application records stay in gitignored `storage/`. Do not re-apply Netflix.

---

## Prompt (copy below)

```
You are continuing work on C:\Github\pdf-designer (local-first PDF/document toolkit).

## Mission
Improve this repo as both (1) a polished free/open GitHub product and (2) a foundation for a
future paid desktop app (PowerPoint / collage-maker class UX), without breaking the privacy
split or inventing a second renderer.

## Read first (in order)
1. AGENTS.md
2. docs/SSOT.md
3. docs/PRODUCT.md          ← business direction + shell-over-Hub paid-app spike
4. docs/PACKAGING.md        ← PyPI/wheel rules (themes+layouts must ship in the wheel)
5. docs/WHITE-LABEL.md      ← public clone path ONLY (not the business plan)
6. docs/QA.md               ← judge the ARTIFACT; check_generation is the ship gate
7. docs/ROADMAP.md → Plans/_Active/2026-07-14-professional-product-roadmap.md
8. docs/STORAGE.md          ← shared MG gallery under storage/studio/resources/images/martiangames/
9. docs/THEME-DESIGN.md     ← trap: prefers-color-scheme must be screen-scoped

## Product constraints (do not violate)
- MIT engine stays free; storage/ vaults + real applications stay gitignored forever.
- No auto-submit applications; no cloud-only PII as default.
- One renderer: pdf_tool (Playwright/Chromium). A paid app = thin shell + recipes, not a fork.
- Palette rule + generation QA stay mandatory (docs/QA.md, themes/PALETTE-RULES.md).

## What already shipped (don't redo)
- check_generation (10 checks) + rendered-color + footer-collision known-bad fixture
- Shared studio MG gallery (WebP) + junctions from jenni/shade
- Shade + Jenni Netflix applications SUBMITTED (separate accounts)
- Public 5-minute path: README + docs/WHITE-LABEL.md + scripts/smoke-white-label.py
- Dark-PDF fix: @media screen and (prefers-color-scheme: light) so OS light preference
  cannot outrank html[data-pdf-theme="dark"] print tokens
- Public example resume is 2 pages and passes check_generation
- Paid-app DESIGN spike: shell-over-Hub in docs/PRODUCT.md (pywebview stays parked)
- PyPI/wheel SPIKE: pdf_tool.paths.repo_root + scripts/sync-wheel-share.py +
  scripts/check-wheel-assets.py + docs/PACKAGING.md (wheel must include share/themes+layouts)

## Prove public path still green (30s)
python scripts/smoke-white-label.py
# Packaging gate (when touching install/wheel):
python scripts/check-wheel-assets.py

## Suggested workstream (pick 1–2, finish, verify)
T. TestPyPI dry-run — bump version if needed, check-wheel-assets PASS, upload TestPyPI,
   fresh-venv install proof. Do not claim production PyPI until that works.
G. Design Hub recipe-gallery UX — browse layouts/ + themes/presets/ inside the Hub
   (paid-shell precursor; still one renderer).
D. Collage/resume recipe polish that strengthens the “layout studio” story for both free + paid.

## Verification
- python -m pdf_tool.check_generation on any doc you touch
- For public path: python scripts/smoke-white-label.py (tracked files only)
- For packaging: python scripts/check-wheel-assets.py
- Commit tracked docs/code only; never commit storage/ or generated src/pdf_tool/share/{themes,layouts,examples}/
- Windows consoles are often cp1252 — keep script print() ASCII

## Out of scope this session
- Rebuilding Netflix materials
- Moving real PII into tracked paths
- Auto-applying to jobs
- Re-opening pywebview vs Electron debates (decision: shell-over-Hub first)
```

---

## Context for humans

| Clarification | Truth |
|---|---|
| Is WHITE-LABEL the business plan? | **No.** It’s the public reuse how-to. Business direction = `docs/PRODUCT.md`. |
| Where are applications logged? | `storage/_job-listings/applied-index.md` + each `application.json` + `pdf_tool.tracker` |
| Active engineering plan | `Plans/_Active/2026-07-14-professional-product-roadmap.md` |
| Packaging SSOT | `docs/PACKAGING.md` — naive wheels without `themes/` are broken |
| Observable public proof | `python scripts/smoke-white-label.py` → PASS; Hub at http://127.0.0.1:8787/ |
