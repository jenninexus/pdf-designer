---
name: lesson-guard-assumptions-must-be-measured
description: A QA guard that hard-codes one layout's assumption fails silently on the other layout — measure the actual pixels before believing a repeated failure
metadata:
  type: feedback
  date: 2026-07-25
---

When a QA guard keeps failing and your fixes do not move it, **stop editing the document and measure
what the guard is actually looking at.** A guard encodes assumptions about layout; if the document
uses a different-but-valid layout, the guard can fail forever on something that is not wrong.

**Why:** `check_generation`'s `footer-collision` rule hard-coded a **right-aligned** signature
(`sig_x0 = W * 0.72`) because that is the *résumé* pattern (`.page-sig` pins bottom-right). Cover
letters sign bottom-**left**. On a letter that scan window contained no signature at all, so the
check locked onto the last line of **body text** in the right column, called it the signature, and
flagged the rest of that same line as an intrusion.

The failure was self-camouflaging in three ways:

1. **Trimming appeared to do something.** Each cut moved the reported band up by exactly the height
   removed — but the intrusion count stayed ~1450px, because the "signature" being measured *was*
   the body text. Several passes of prose-trimming were wasted before measuring.
2. **A real prior document failed identically.** The already-**submitted** Netflix cover letter fails
   this same check, so the failure read as "known-bad document" rather than "broken check."
3. **A counter-example existed.** `shade-ai-cover-letter` passes — but only because its shorter body
   leaves no text in the right column near the bottom, not because it is structurally different.
   That near-miss briefly suggested "blanket false positive," which was also wrong.

Measuring settled it in one command: real signature at **y=1474 in the 8–40% band**, while the check
was reading body text ending at **y=1366 in the 72–100% band**.

**How to apply:**

- **Two or three failed fixes with an unchanged metric = suspect the guard, not the document.** A
  genuine overflow shrinks as you cut; a phantom does not.
- **Read the guard's source before the fourth attempt.** `src/pdf_tool/check_generation.py` is short
  and each check says what it samples.
- **Rasterize and measure** rather than reasoning from the DOM: render the real PDF and print where
  the lit pixels are per column band. `docs/LAYOUT-SYSTEM.md` already says the exported PDF is ground
  truth — that applies to diagnosing the *guard* too.
- **When you fix a guard, regression-test that it still catches the real defect.** Here: a
  deliberately overfilled résumé must still FAIL. Loosening a check until it passes is not a fix —
  it is deleting the check. (Fixed 2026-07-25; the rule now detects signature alignment by taking
  whichever bottom-most lit cluster sits lower, and scans the opposite column for intrusion.)

Related: [[lesson-overflow-fix-is-move-not-shrink]] · [[lesson-twin-files-always-fork]]
