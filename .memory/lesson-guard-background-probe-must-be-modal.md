---
name: lesson-guard-background-probe-must-be-modal
description: footer-collision sampled ONE pixel as "background"; on a glyph it lit the whole sheet and failed a fitting résumé — sample a grid and take the modal colour
metadata:
  type: project
  date: 2026-09-27
---

A pixel guard must derive the page background from the **modal colour of a sparse grid**, never from
a single probe pixel.

**Why:** `check_footer_collision` read `bg = im.getpixel((inset, H // 2))`. On a résumé whose summary
text crossed that exact point, the probe returned the cream text colour, so every empty navy pixel
counted as "lit". The signature cluster then "extended" up to the search floor (rows 1108–1580) and a
page with ~1.5in of clear space under its last bullet failed with 61,894 "intruding" pixels. Cutting
content could never move the number — the classic guard-assumption trap.

**How to apply:** the guard now uses `Counter(...).most_common(1)` over a 31×23 px grid inside the
content box. Control tests: `tests/test_check_generation_footer.py` fails on the old probe and passes
on the new one (`tests/fixtures/known-good-probe-on-text.html`) while the known-bad overlap still fails.
If another render guard samples "the background", reuse the same modal approach.

Related: [[lesson-guard-assumptions-must-be-measured]] · [[lesson-work-samples-footer-row-false-collision]]
