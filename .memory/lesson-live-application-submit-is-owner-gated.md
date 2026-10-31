---
name: lesson-live-application-submit-is-owner-gated
description: A real employer application cannot be auto-completed by the agent when the form carries a CAPTCHA, a legal attestation, custom widgets or uploads — the helper fills only native text inputs and the human submits.
metadata:
  type: project
  date: 2026-10-31
---

Do not promise (or attempt) a fully automated application submission on a live employer site.
On a real form, fill only the top-frame **native text inputs** the owner has authorized, and leave
the CAPTCHA, the legal acknowledgment, custom widgets, uploads, free text and the final **Submit**
to the human. Never attempt to solve, bypass or work around the CAPTCHA.

**Why:** the 2026-10-31 Lightfox Games "Integration Artist" form (S) is a JS-injected custom SPA
form. It carries a **Cloudflare Turnstile** (its `submitApplication` endpoint rejects a request with
no token), a brand-skinned **custom date picker**, required **acknowledgment checkboxes** including a
legal work-authorization attestation ("I am legally authorized to work in the United States and will
not now or in the future require visa sponsorship"), a **file upload**, and a free-text note. The
extension supports only top-frame native inputs, so at most Name/Email/Portfolio/LinkedIn can be
filled by it. An agent that tries to "completely fill and submit" either defeats a bot gate (never
acceptable) or asserts a legal fact on the applicant's behalf (never acceptable). The owner's
standing rule already reads "No auto-submission. Prepare materials; the human submits"; a CAPTCHA
makes that physical, not merely policy.

**How to apply:** (1) capture the live listing + form read-only first (`roles.json` / any JSON feed,
plus a rendered control dump) and record the effective controls and policies; (2) fill only the
authorized native fields; (3) hand the owner the exact remaining steps (upload, acknowledgments,
date, note, Turnstile, Submit) with a screenshot; (4) record the submission only after the owner
confirms it. A site whose feed shows `visible:false`/`status:"icebox"`, or whose `?id=` slug matches
no live role, is not an open posting.

Related: [[lesson-extension-action-targets-need-managed-attachment]]
