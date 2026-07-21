# Handoff prompt — next agent (copy into a new chat)

> **Status:** ready to paste (refreshed 2026-07-21 wrap). Workstreams **A + B shipped**.
> Pick **C** (paid-app spike) and/or **PyPI/installer**; optional **D** (recipe polish).
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
3. docs/PRODUCT.md          ← business direction SSOT (free GitHub vs paid app)
4. docs/WHITE-LABEL.md      ← public clone path ONLY (not the business plan)
5. docs/QA.md               ← judge the ARTIFACT; check_generation is the ship gate
6. docs/ROADMAP.md → Plans/_Active/2026-07-14-professional-product-roadmap.md
7. docs/STORAGE.md          ← shared MG gallery under storage/studio/resources/images/martiangames/
8. docs/THEME-DESIGN.md     ← trap: prefers-color-scheme must be screen-scoped

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

## Prove public path still green (30s)
python scripts/smoke-white-label.py

## Suggested workstream (pick 1–2, finish, verify)
C. Paid-app spike (design only or thin prototype): installer + recipe gallery over Design Hub —
   document in PRODUCT.md / active plan; do not ship secrets. pywebview shell is parked —
   prefer documenting the shell-over-Hub approach first.
P. PyPI / installer spike for non-dev users (remaining public-readiness item).
D. Collage/resume recipe polish that strengthens the “layout studio” story for both free + paid.

## Verification
- python -m pdf_tool.check_generation on any doc you touch
- For public path: python scripts/smoke-white-label.py (tracked files only)
- Commit tracked docs/code only; never commit storage/
- Windows consoles are often cp1252 — keep script print() ASCII

## Out of scope this session
- Rebuilding Netflix materials
- Moving real PII into tracked paths
- Auto-applying to jobs
```

---

## Context for humans

| Clarification | Truth |
|---|---|
| Is WHITE-LABEL the business plan? | **No.** It’s the public reuse how-to. Business direction = `docs/PRODUCT.md`. |
| Where are applications logged? | `storage/_job-listings/applied-index.md` + each `application.json` + `pdf_tool.tracker` |
| Active engineering plan | `Plans/_Active/2026-07-14-professional-product-roadmap.md` |
| Observable public proof | `python scripts/smoke-white-label.py` → PASS; Hub at http://127.0.0.1:8787/ |
