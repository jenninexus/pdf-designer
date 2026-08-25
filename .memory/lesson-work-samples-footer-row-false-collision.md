---
name: lesson-work-samples-footer-row-false-collision
description: A L/R work-samples footer (name left · links right) false-triggers footer-collision — pin bottom-RIGHT like the résumé and put portfolio URLs in a body panel
metadata:
  type: feedback
  date: 2026-08-08
---

Do **not** use a two-column footer row on work-samples (script left / links right). Put portfolio URLs in a **body** `.links-panel` and pin the signature **bottom-RIGHT** (`.footer.page-sig`), same family as the résumé.

Keep the signature email **inside the right 28% of the sheet**. `check_footer_collision` splits at `x = 0.72W`. Uppercase `12px` + `letter-spacing: 0.08em` on a long address (`shade@martiangames.com`) paints into the “body” column and fails both pages at ~70 px — cutting content does not move that number. Drop tracking to ~`0.03em` and keep ≥11px / `font-weight: 600` / `--text`.

A **full-bleed collage mosaic** named `work-examples` (Jane Hub demo) will also fail this check: colored tiles light the bottom 30% in both columns. That file is collage-family geometry (`0.6in` / `9.8in`), not the 3-page work-examples pack. Do not “fix” it by shrinking `@page` margins.

**Why:** `check_footer_collision` finds the bottom-most lit cluster on the left *and* right, treats the lower side as the signature, then counts lit pixels in the **opposite** column as intrusion. A legitimate L/R footer paints both columns on the same rows (~160 "intruding" pixels every page) and fails forever no matter how much body content you cut. A wide right-aligned email is the same class of false-looking failure: the “intrusion” *is* the signature.

**How to apply:**

1. Work-samples recipe: [`layouts/work-examples/work-examples.json`](../layouts/work-examples/work-examples.json).
2. Export go-to packs into `output/<user>/resumes/` — HTML stays in `resumes/<user>/defaults/`.
3. After editing the `.template.html`, re-inline images, then `check_generation` before export.

Related: [[lesson-guard-assumptions-must-be-measured]] · [[lesson-fixed-height-clips-content-silently]]
