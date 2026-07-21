# Handoff prompt — next agent (copy into a new chat)

> **Status:** ready to paste. Private Netflix/application records are in gitignored `storage/`;
> product docs were clarified 2026-07-21 (`docs/PRODUCT.md`). Do not re-apply Netflix.

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

## Product constraints (do not violate)
- MIT engine stays free; storage/ vaults + real applications stay gitignored forever.
- No auto-submit applications; no cloud-only PII as default.
- One renderer: pdf_tool (Playwright/Chromium). A paid app = thin shell + recipes, not a fork.
- Palette rule + generation QA stay mandatory (docs/QA.md, themes/PALETTE-RULES.md).

## What already shipped (don't redo)
- check_generation (10 checks) + rendered-color + footer-collision known-bad fixture
- Shared studio MG gallery (WebP) + junctions from jenni/shade
- Shade + Jenni Netflix applications SUBMITTED (separate accounts) — see
  storage/_job-listings/applied-index.md and Netflix-App/application.json
- Shade Netflix work-samples-dark under 5MB

## Suggested workstream (pick 1–2, finish, verify)
A. Public-repo readiness: fresh-clone demo from examples/ only; README “5-minute path”;
   PyPI/installer spike when ready.
B. White-label smoke script or doc checklist that a stranger can run without storage/.
C. Paid-app spike (design only or thin prototype): installer + recipe gallery over Design Hub —
   document in PRODUCT.md / active plan; do not ship secrets.
D. Collage/resume recipe polish that strengthens the “layout studio” story for both free + paid.

## Verification
- python -m pdf_tool.check_generation on any doc you touch
- For public path: prove it works with only tracked files (no storage/ dependency)
- Commit tracked docs/code only; never commit storage/

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
