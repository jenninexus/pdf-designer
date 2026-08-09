---
name: lesson-ats-section-cues-must-be-contiguous
description: Jobright/Indeed miss Job Title · Work Experience · Education when headings are creative, mashed, buried, or split in the PDF text layer (e.g. Montserrat W → "W ORK")
metadata:
  type: feedback
  date: 2026-08-09
---

Board parsers (Jobright, Indeed, LinkedIn) need **contiguous** section cues in the PDF text layer —
not just a nice-looking page. A résumé can *look* perfect and still warn “missing Job Title / Work
Experience / Education.”

**Why:**

1. Creative or short headings (`Experience`, `My Journey`) are not the field names parsers map.
2. `COMPANY — ROLE` on one line often fails to extract a Job Title.
3. Education buried as an `h3` inside a two-column grid may never register as an Education section.
4. **Font metrics:** Montserrat’s `W` glyph advances made pypdf extract `WORK EXPERIENCE` as
   `W ORK EXPERIENCE` even at `letter-spacing: 0` — Jobright then treated the cue as missing.
5. Extreme `letter-spacing` on brand words (`0.18em` on `jenninexus`) similarly splits the text layer.

**How to apply:**

1. Use exact `h2` labels: **Work Experience**, **Education**, **Skills**; header line **Job Title**.
2. Job blocks: title → company → dates (separate lines).
3. Section `h2` on a system font (`Segoe UI` / Arial / Helvetica) for ATS-critical cues.
4. Export **light** for board upload; keep dark for humans (same HTML — dark is not “unparseable”).
5. Gate: `python -m pdf_tool.check_ats <resume-light.pdf>` — exit 0 requires contiguous
   `job title` · `work experience` · `education`. Read the dump; if *you* cannot find the phrases,
   the board will not either.

SSOT: [`docs/JOB-ASSESSMENT.md`](../docs/JOB-ASSESSMENT.md) § Tier 4.5 · [`docs/SSOT.md`](../docs/SSOT.md)
§ ATS parseability · `examples/profiles/default-resume/profile.json#verify.atsParse`.

Related: [[lesson-defaults-export-beside-html]] · [[lesson-work-samples-footer-row-false-collision]]
