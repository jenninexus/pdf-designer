# <Company> — <Role Title>

> **The research doc.** Copy to `storage/_job-listings/<Track>/<Company>.md`.
> Its sibling `application.json` is the *machine* record (apply URL, pay, status);
> this file is the *human* one — what they do, what they want, and whether we're a fit.
>
> Order matters: **status first, links second.** If someone opens this file in a hurry,
> the two things they need are "can I submit this?" and "where?"

**Status:** `BLOCKED — no apply link` · **Track:** `<track>` · **Generated:** `<date>`

---

## 🔗 Links

> **⚠ BLOCKING. Fill this in BEFORE building anything.**
> A perfectly tailored application you can't submit is worthless. If the listing was
> pasted with no URL — **ask for it.** Status stays `BLOCKED` until this table is real.

| Item | Value |
|---|---|
| **Apply URL** | *(the exact page you click "apply" on — canonical, tracking params stripped)* |
| **How to apply** | portal · email · job board *(if a board: upload the **light/ATS** PDF, never the bundle)* |
| **Job ID** | |
| **Posting still live?** | ⚠ not verified — *fetch the direct link and confirm* |
| **Company site** | |
| **Careers page** | *(or "none — no careers page")* |

> **Trap:** a company page showing *"no open jobs"* does **NOT** mean the posting is dead.
> Board postings often never appear on the employer's own page. **Only the direct job link
> is authoritative.** We nearly wrote off a live posting on exactly this evidence.

---

## ⚠ Routine checks

| Check | Finding |
|---|---|
| **Remote?** | |
| **Pay** | *(state it, then convert: $/hr AND $/yr)* |
| **Pay verdict** | *(compare to market for this role + region. **If it's below market, say so loudly.**)* |
| **W2 / 1099 / contract?** | |
| **Duration** | |
| **Portfolio or take-home test?** | |
| **Seniority match?** | |
| **Company legit?** | |

---

## What they actually do

*Two or three sentences. Not their marketing copy — what the business actually is, who pays
them, and what this role is really for. This is what the cover letter hooks into.*

**What the listing repeats** — *the words they use more than once are the words that matter.
They're also the ATS surface.*

---

## Requirement → evidence map

Every requirement in the listing, mapped to a real vault claim.

| They ask for | We have | Vault claim |
|---|---|---|
| *(their exact words)* | ✅ *(our honest match)* | `sk-…` |
| | ⚠ **UNVERIFIED — ASK FIRST** | *(not in the vault. **Not a gap yet.**)* |
| | ❌ confirmed gap | *(→ honest equivalent + one line in the cover letter)* |

> **🛑 The gap-check is BLOCKING.** For every ⚠ row: **ask the applicant before building.**
> The vault records what they've *told* you — it is **not** the limit of what they can do.
> On a real application, four "gaps" turned out to be long-standing strengths nobody had
> asked about. Only a **confirmed** absence is a gap.

---

## The angle

*Which track, and what leads. Pull this from the vault's `roleTracks.<track>.angle` —
don't reinvent it. If the person's lead identity changes by track, name it here.*

## Gaps & prep notes

*What to say if they ask about the confirmed gap. What to bring up in an interview.
Anything the next person to touch this application needs to know.*

## Materials

| | Path |
|---|---|
| Résumé (light / ATS) | `../../<user>/_exports/<Track>/…-resume-light.pdf` |
| Résumé (dark / branded) | `…-resume-dark.pdf` |
| Cover letter (light / dark) | `…-cover-letter-{light,dark}.pdf` |
| **Submission bundle** | `FINAL-<Name>-<Role>-Cover-Letter-and-Resume.pdf` |

---

## Requirements

- Experience with systems design and core development
- Shipped titles with proven delivery and source-backed credits
- Proficiency with FictionalToolXYZ (demo unbacked row for `--coverage`)

## The listing, verbatim

*Paste it below, unedited. Postings get taken down; this is the only copy that survives.*

```
Example Studio LLC — Lead Developer

We're looking for someone who can ship titles and write resume claims from verified facts.

Requirements:
- Strong systems design and core development skills
- Demonstrated experience shipping titles with proven delivery
- Comfortable presenting work via portfolio links and demo reels

Nice to have:
- Proficiency with FictionalToolXYZ
- Experience with ObscureFramework 9000
```
