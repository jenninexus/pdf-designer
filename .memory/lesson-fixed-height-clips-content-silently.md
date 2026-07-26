---
name: lesson-fixed-height-clips-content-silently
description: A print `height` + `overflow: hidden` on a cover letter silently CLIPS the sign-off — every guard passes because the DOM reports no overflow
metadata:
  type: feedback
  date: 2026-07-25
---

**Never put a fixed print `height` + `overflow: hidden` on a COVER LETTER.** That pattern belongs
to the résumé and work-samples, where a *fixed page count* means the box must hold the bottom edge.
On a one-page letter it destroys content instead of protecting it.

**Why:** the Sony letter shipped with **"Founder & CEO, Martian Games LLC" sliced through the
middle and the email line gone entirely.** `@page { margin }` already insets the printable area, so
a `.page` *also* declaring a near-full height overflows the sheet — and `overflow: hidden` then
**clips the tail** rather than letting it flow to where it would be visible.

**It is invisible to every guard we have:**

| Check | Verdict | Why it missed |
|---|---|---|
| `check_overflow` | **PASS** | DOM measured content at 7.29in inside a 9.6in box — `overflowBy: 0`. The clip does not exist in the DOM. |
| `check_generation` (all 10) | **PASS** | Same DOM basis, plus the signature *was* present — just cut in half. |
| Page-count check | **PASS** | Exactly 1 page, as required. |
| Text-layer / `check_ats` | **PASS-looking** | The clipped line still exists in the text layer, so a grep for it succeeds even though no human can read it. |

Only **rasterising the PDF and looking at the bottom of the page** caught it — and only because the
owner opened the file. The document was otherwise "verified" by four passing checks.

**A second trap sits right next to it:** when the height is removed the letter may flow to **two**
pages, which is also wrong (a cover letter is fixed at 1). The instinct is to put the height back.
Don't — that just re-hides the overflow. **Cut prose until it fits at its natural height.**

**How to apply:**

- **Cover letter:** `@page { margin: <equal> }` controls the frame; `.page` gets `height: auto` and
  **no** `overflow: hidden` in print. The letter that always rendered correctly
  (`shade-ai-cover-letter`) sets no print height at all — copy that, not the Netflix letter.
- **Résumé / work-samples:** keep the fixed height + `overflow: hidden` — there the guarantee that
  the page count cannot silently grow is worth more, and `check_generation`'s footer-collision rule
  covers the collision case.
- **Doesn't fit? Cut prose.** Never raise the height, never shrink the margin, never drop
  line-height to buy a line. See [[lesson-overflow-fix-is-move-not-shrink]].
- **Verify the BOTTOM of every exported letter by eye**, not by guard. Crop the last ~15% of the
  rendered page and look at it. A guard that reads the DOM cannot see a rasteriser clip.
- **⚠ A PIXEL GUARD CANNOT CATCH THIS — measured, do not re-attempt.** Two detectors were built
  and both failed: (a) *ink at the sheet edge* — a clipped and a clean export gave an **identical**
  bottom-ink row (y=1438 of 1584), because the cut happens at the `.page` BOX boundary ~100px
  inside the paper margin; (b) *a short final ink band* (a sliced line keeps its top, loses its
  body) — both files ended with a **13px** band against a **16px** median. A rasteriser cannot
  distinguish "the line ended here" from "the line was cut here".
  **So the rule is enforced at the SOURCE:** `check_generation` check 11 (`letter-geometry`,
  implemented in `check_pagefit.check_source_geometry`) refuses the CSS combination outright on any
  file whose name contains `letter`. Contract: `layouts/resume/one-page-letter.json`.
- **Fix order when a letter runs long** (never restore the height): cut prose → tighten the closing
  → font-size 11.5→11.0→10.75px (floor 10.5) → line-height 1.55→1.5→1.45 (floor 1.4) → margin
  0.75–0.8in, equal on all edges.
- **Watch for the ORPHAN TAIL too** — a sign-off stranded alone on page 2 is unprofessional even
  though nothing is clipped. `check_pagefit <doc>.pdf` flags it.
- Note the diagnostic order that actually worked: measure where the ink ends in the PDF → compare
  to the DOM's reported content height → when they disagree, the *renderer* is clipping, not the
  layout. Same discipline as [[lesson-guard-assumptions-must-be-measured]].

Related: [[lesson-overflow-fix-is-move-not-shrink]] · [[lesson-guard-assumptions-must-be-measured]] ·
`docs/LAYOUT-SYSTEM.md`
