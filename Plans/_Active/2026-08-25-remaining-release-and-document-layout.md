# Remaining — release gates + document layout / spacing

**Date:** 2026-08-25  
**Status:** Active — the only working checklist  
**Closed parents:**  
[`../_Complete/2026-08-22-product-polish-and-release-readiness.md`](../_Complete/2026-08-22-product-polish-and-release-readiness.md) ·  
[`../_Complete/2026-08-22-root-output-folder.md`](../_Complete/2026-08-22-root-output-folder.md) ·  
[`../_Complete/2026-08-23-start-vault-import.md`](../_Complete/2026-08-23-start-vault-import.md)

Hub polish, LIVPHI **source** mirror, `/wizard` vault import, `output/<user>/<kind>/`, and
unsigned BundledRuntimeProof are done. This file is only what is left.

Public GitHub must stay clone-safe. Azure / Store / Partner Center / live `/products`
rewrite notes live in `docs/CHANNELS.local.md` (gitignored), not `docs/PRODUCT.md`.

---

## Where we are (cross-surface)

| Surface | State |
|---|---|
| **pdf-designer GitHub** | Public MIT clone. Suggested tip $3/$5 on README. No Setup.exe download. |
| **Design Hub** | http://127.0.0.1:8787/ — recipes at `/recipes` |
| **JN `/products`** | Local catalog already **free card + tip** (`jenninexus/public_html/includes/products.json`, 2026-08-25). Confirm live [jenninexus.com/products](https://jenninexus.com/products)#pdf-designer if not deployed this machine. Checkout stays off. |
| **product-design hub** | Local-only. Card: `C:\Github\product-design\docs\PDF-DESIGNER.md`. Money board: `product-registry.md`. Command: `/products`. |
| **Jenni defaults** | HTML `resumes/jenni/defaults/` · PDFs `output/jenni/resumes/` (work-examples ~1.18 MB, 2026-08-22). |
| **Shade defaults** | Same recipes. Work-examples PDF still ~12 MB (board follow-up). |

---

## Done when

- [x] Jenni + Shade résumé / cover / work-examples match [`docs/LAYOUT-SYSTEM.md`](../../docs/LAYOUT-SYSTEM.md) rhythm. `check_generation` PASS 2026-08-25. Jane résumé + cover PASS. Jane Hub mosaic is collage-family (`0.6in` / `9.8in`) — `footer-collision` still FAILs (colored tiles vs résumé signature scan); not the 3-page pack.
- [x] Shade work-examples PDFs ≤ 5 MB — `output/shade/resumes/shade-default-work-examples-{light,dark}-v2.pdf` ≈ **2.05 MB** (`html_to_pdf --max-mb 5`). Older `*-light.pdf` / `*-dark.pdf` (~11.8 MB) are pre-inline leftovers.
- [ ] Signed NSIS exists **or** Azure remains explicitly held (no unsigned listing).
- [ ] Clean Win10/11 x64 VM proof with `-RequireAuthenticode` **or** documented LAN substitute only after a Valid signature.

---

## 1. Document layout / spacing (engineering — next)

Recipes (shared by Jenni and Shade — not per-person files):

| Doc | Recipe | Theme geometry |
|---|---|---|
| Résumé | `layouts/resume/two-page-standard.json` | `themes/default-resume.css` `--resume-page-margin` |
| Cover letter | `layouts/cover-letter/one-page-letter.json` | 0.75in equal; **no** print `height` + `overflow: hidden` |
| Work examples | `layouts/work-examples/work-examples.json` | 0.6in; 3 pages; links in body `.links-panel` |

**Observed drift (2026-08-25):** Jenni default HTML **inlines** CSS instead of importing the theme. The résumé is packed tighter than LAYOUT-SYSTEM (header ~10px vs ~20; `section` ~12px vs 16–19; `li` ~1px vs ~4). Cover letter is already closest to spec. Work-examples `.page-main` gap is ~22px vs recipe ~18px; `section:last-of-type { margin-top: auto }` fights the footer-pin rule.

**Recommended pass (do not shrink margins to “fit”):**

1. **Résumé** — restore section/list air to the recipe. If page 2 overflows, cut a bullet or move a block — never `--resume-page-margin`. Keep page-1 and page-2 gaps even. Studio Capabilities stays demoted, not crammed at 10.5px as a second résumé.
2. **Cover letter** — keep CZI geometry (`min-height`, 13px paras, 30px above sign-off). Eyeball the bottom 15% of the PDF. Fit-to-one-page order is already in LAYOUT-SYSTEM.
3. **Work examples** — set `.page-main` gap to ~18px; drop `margin-top: auto` on the last section. Keep full-width grids (`repeat(N, 1fr)`). Caption below hero. Then `check_generation` + raster.
4. **Jane Example** — same rhythm so the public clone matches what we print.
5. **Verify** — `python -m pdf_tool.check_generation` then `pdf_to_png`. Optional later: `/human-sim-qa` on Syqo’s **designated QA machine** (never SEGOPC pointer). Write `human-sim-qa-pdf-designer.md` before that run.

**Landed 2026-08-25 (layout HTML pass):** Jenni defaults + Shade go-to restored to equal margins and recipe air. Shade cover is CZI flex (`.letter-main` / `.signoff`); work-examples re-inlined JPEG ≤960 via `resumes/shade/defaults/_inline_work_examples.py`. Footer email tracking dropped to ~`0.03em` so `footer-collision` does not treat the mailto as body. `html_to_pdf` has no `--user` — that flag is `check_generation` only.

## 2. Carryover (human / later — not this layout session)

From the closed 2026-08-22 polish plan. Detail: `docs/CHANNELS.local.md` + `docs/WINDOWS-ELECTRON.local.md`.

- [ ] **Hold Azure Artifact Signing** until a signing month is budgeted. Then `npm run dist:signed` + `verify-authenticode.ps1 -RequireSigned`. Detail stays in `docs/CHANNELS.local.md`.
- [ ] Clean VM (or `-BundledRuntimeProof -RequireAuthenticode` after Valid). Not a daily-driver PC as listing proof.
- [ ] Do not enable live checkout, Gumroad overlay, or Microsoft Store on `/products`.
- [x] Shade work-examples ≤ 5 MB.
- [ ] Production PyPI still out of scope.

---

## Assumptions

- One active plan. Closed files in `_Complete/` are history.
- `/jen/www` wrap is for the **website** if `/products` still needs a live deploy; this plan does not own jennidrop rsync.
- `/jenni` is identity/web ops, not the applicant vault (`/pdf` + `/jenni` applicant router).

## Evidence

- VERIFIED — wizard import tests exist; `output/` engine default landed (`190963f` / later).
- VERIFIED — JN local `products.json` sku `pdf-designer` is `status: free` + tip CTA (2026-08-25).
- UNVERIFIED — live droplet `/products` if deploy has not run since that catalog edit.
- UNVERIFIED — résumé/cover/work-examples raster vs LAYOUT-SYSTEM rhythm (layout pass not started).
