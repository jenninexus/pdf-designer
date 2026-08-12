---
name: lesson-work-samples-footer-row-false-collision
description: A L/R work-samples footer (name left · links right) false-triggers footer-collision — pin bottom-RIGHT like the résumé and put portfolio URLs in a body panel
metadata:
  type: feedback
  date: 2026-08-08
---

Do **not** use a two-column footer row on work-samples (script left / links right). Put portfolio URLs in a **body** `.links-panel` and pin the signature **bottom-RIGHT** (`.footer.page-sig`), same family as the résumé.

**Why:** `check_footer_collision` finds the bottom-most lit cluster on the left *and* right, treats the lower side as the signature, then counts lit pixels in the **opposite** column as intrusion. A legitimate L/R footer paints both columns on the same rows (~160 "intruding" pixels every page) and fails forever no matter how much body content you cut.

**How to apply:**

1. Work-samples recipe: [`layouts/work-examples/work-examples.json`](../layouts/work-examples/work-examples.json).
2. Export go-to packs into `storage/<user>/defaults/` — never `_exports/defaults/`.
3. After editing the `.template.html`, re-inline images, then `check_generation` before export.

Related: [[lesson-guard-assumptions-must-be-measured]] · [[lesson-fixed-height-clips-content-silently]]
