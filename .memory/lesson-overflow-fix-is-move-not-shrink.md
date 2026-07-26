---
name: lesson-overflow-fix-is-move-not-shrink
description: Page overflow is fixed by moving or cutting content, never by shrinking the equal margins or line-height
metadata:
  type: feedback
  date: 2026-07-25
---

**When a page overflows its print box, MOVE a section to the next page or CUT content. Never shrink
the margins, the line-height, or the font size to make it fit.**

**Why:** equal margins are the professional frame — every document uses one margin value on all four
edges (`0.65in` résumé, `0.75in` cover letter). A page that is 0.5in on top and 0.78in on the bottom
looks lopsided, and the three doc types stop reading as a matched set. Shrinking type to win 40px
degrades every page to rescue one.

The failure this prevents is concrete: content overflowing its box **collides with the pinned
signature**, so the last lines render *through* the script name. `overflow: hidden` guarantees the
PDF is not taller, which means the collision is silent unless a guard catches it.

Observed on the Sony build (2026-07-25): adding a **Leading & Mentoring** section pushed page 1 to
**1010px against a 931px box**. What looked like free space at the bottom of the page was the
signature's reserved band, not slack. Fixed by moving "Why this maps to teamLFG" to page 2, then
trimming three page-2 bullets that restated page 1 — no margin was touched.

**How to apply:**

- Content box at the 0.65in default is **9.7in ≈ 931px tall · 7.2in ≈ 691px wide**. Cover letter at
  0.75in is ~912px.
- **Page counts are fixed:** résumé exactly 2 · cover letter 1 · work-samples 3 · merged bundle 3.
  So on a 1-page letter "move to the next page" is unavailable — **cut instead**, and cut the
  paragraph that *duplicates* something already on the page.
- **Prefer cutting duplication over cutting substance.** The Sony page-2 bullets removed were
  restatements of the page-1 flagship block; nothing unique was lost.
- Run `check_overflow <doc>.html --pdf-theme <theme you ship>` — and note it is a **DOM pre-flight**.
  The exported PDF is ground truth; `check_generation`'s `footer-collision` renders the real PDF.
- **A trailing loose `<p>` just before a pinned footer drifts to the bottom and collides** even when
  totals fit. Put that line *inside* the pinned footer block (`.page-foot--stacked`).
- If trims stop changing the reported numbers, suspect the guard —
  see [[lesson-guard-assumptions-must-be-measured]].

Related: [[lesson-guard-assumptions-must-be-measured]] · `docs/LAYOUT-SYSTEM.md`
