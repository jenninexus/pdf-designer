---
name: lesson-ask-before-calling-it-a-gap
description: doNotClaim means "not yet confirmed", never "cannot do" — ask the applicant before writing any requirement off as a gap
metadata:
  type: feedback
  date: 2026-07-25
---

**Never write off a listing requirement as a gap without asking the applicant first.** The vault
records what they have *told* us; it is not the boundary of what they can do.

**Why:** this has now cost real opportunities three separate times.

| When | What went wrong |
|---|---|
| Colour X, 2026-07-13 | 3ds Max, V-Ray, Unreal, and CC4 apparel authoring were all missing from the vault — and *all four* turned out to be central to the role. A résumé claiming only Blender and Unity was nearly submitted for a job requiring 3ds Max. |
| Maya + ZBrush, 2026-07-13 | Both sat in `doNotClaim` for months while both founders had **years** of experience. Forbidden on résumés purely because nobody had asked. |
| **Substance Painter, 2026-07-25** | Sat `unverified` in both ledgers. The Sony listing named Substance as a core tool. One question established **5 years of production use** for both founders. Had it not been asked, the strongest tool match on the listing would have been silently absent. |

The mechanism is that a flat blocklist cannot distinguish *"we asked and they don't have it"* from
*"nobody ever checked."* Absence of a claim reads identically to absence of the skill.

**How to apply:**

- `doNotClaim.tools[].status` is the whole point: **`unverified` is not a gap.** Only
  `confirmed-absent` may be treated as one, and it must carry an `askedOn` date.
- Before building, list every unbacked requirement **in one message** and ask plainly: *"Do you have
  experience with any of these?"* One question up front costs nothing; not asking costs the job.
- If they have it → **write it into the vault first** (`source: "owner directive <date>"`, move the
  ledger entry to `resolved` as `confirmed-have`), *then* use it. The vault gets permanently richer
  and every later application in that track benefits.
- If they genuinely don't → *then* it is a gap: honest equivalent on the résumé, named once plainly
  in the cover letter. That candour has won credibility; hiding a gap has not.
- **Assume broad competence.** Check `docs/VAULT.md`'s capability matrix before concluding anything
  is missing.
- When the user answers with scope limits ("keep it non-specific"), **record that constraint in the
  claim's `note`** so a later agent does not "helpfully" invent supporting detail.

Related: [[lesson-track-tags-hide-true-claims]] · [[lesson-applicant-fit-before-polish]]
