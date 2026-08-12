---
description: Build a standalone tailored cover letter for a job application — REMOTE + PAY, company theme, honest-gap paragraph, export per exportPrefs. Accepts natural phrasing. Public seed — copy to make-cover-letter.md for personal specifics.
argument-hint: "[for] <user> [application-dir] [dark]"
---

# /make-cover-letter — Standalone Cover Letter Builder (public seed)

Generalized command. **No real employer names or private paths.** Copy to
`make-cover-letter.md` (gitignored) for your specifics.

> **`/make-resume` does NOT auto-build a cover letter.** Use this command when you want a letter.

### Page geometry

**Recipe:** [`layouts/cover-letter/one-page-letter.json`](../../layouts/cover-letter/one-page-letter.json) ·
[`docs/LAYOUT-SYSTEM.md`](../../docs/LAYOUT-SYSTEM.md).

| | Do this | Never |
|---|---|---|
| Structure | `.page` flex column · `.letter-main` grows · `.signoff { margin-top: auto }` | Sign-off floating mid-page |
| Placement | **Bottom-LEFT** | Résumé bottom-RIGHT |
| Print | `min-height` · `height: auto` · **no** `overflow: hidden` | Fixed height that clips |
| Margins | Equal (band ~0.65–0.8in; default **0.75in**) | Asymmetric edges |

Ship gate: `python -m pdf_tool.check_generation <doc>.html`.

### Voice (blocking)

| Layer | Path |
|---|---|
| Application prose | `storage/<user>/resume-source.json#voice` |
| Personality | `storage/users/<user>.json#characterVoice` |

Edit via `/voice application <user>` · `/voice character <user>`. No Discord emoji on ATS PDFs.
Never studio “we” on a solo application.

### Checklist

0. Voice layers loaded  
1. Listing + apply URL + theme  
2. Gap check — ask before writing gaps  
3. Write letter (company-specific content lives HERE)  
4. Export per `exportPrefs` → `storage/<user>/_exports/<Job>/`  
5. Verify 1 page US Letter  
6. Log paths in `application.json`

Contracts: [`AGENTS.md`](../../AGENTS.md) · sibling [`make-resume.example.md`](make-resume.example.md).
