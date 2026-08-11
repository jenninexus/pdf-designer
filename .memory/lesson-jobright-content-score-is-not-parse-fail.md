---
name: lesson-jobright-content-score-is-not-parse-fail
description: Jobright rank D / IMPROVABLE / skills-count is their content AI — not the same as missing Job Title/Work Experience/Education or a shredded text layer
metadata:
  type: feedback
  date: 2026-08-09
---

**Do not treat Jobright’s résumé “Analysis Report” as an ATS parse failure.**

| Jobright signal | Reality | Gate |
|---|---|---|
| Missing Job Title / Work Experience / Education | True parser miss | `check_ats` must fail until fixed |
| Rank D · IMPROVABLE · Insufficient skills · Lack of Accomplishment · short bullets | Content AI grading against a generic template | Optional vault-backed rewrite; not “unparseable” |
| Uploaded `*-resume-dark.pdf` | Boards expect light | Always upload `*-resume-light.pdf` |

**Why this bit:** On 2026-08-09 the Jenni default **passed** `check_ats` (cues OK) while Jobright scored it D —
and the file uploaded was the **dark** PDF. Agents/humans then “fixed parseability” by chasing content
scores, or assumed dark was broken. Separately, Montserrat as the **print body** font was shredding
words (`Martian Gam es`, `m aterials`) even when `h2` was already on Segoe — `check_ats` now fails
mid-word splits, and print CSS must use a system stack for body text.

**How to apply:**

1. Board upload = **light** résumé only. Dark for humans / email / portfolio.
2. Run `python -m pdf_tool.check_ats <resume-light.pdf>` — exit 0 + read the dump.
3. If cues pass and mid-word splits are 0, the file is **parseable**. Jobright content flags are a
   different conversation (expand `boardSkills`, method+result bullets — still vault-backed).
4. Cover letters / work-samples: `check_generation`; never substitute them for the board résumé upload.
5. Print: system font for **body + h2**; letter-spacing ≤ 0.04em on ATS labels.

SSOT: [`docs/JOB-ASSESSMENT.md`](../docs/JOB-ASSESSMENT.md) § Tier 4.5 · [`docs/SSOT.md`](../docs/SSOT.md)
§ ATS parseability.

Related: [[lesson-ats-section-cues-must-be-contiguous]]
