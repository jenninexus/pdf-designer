---
name: lesson-hub-archive-not-found
description: Hub "not found" for jenni galleries / shade work-samples — scan walked _archive and *.template.html; stale /storage/ URLs missed resumes/
metadata:
  type: feedback
  date: 2026-08-17
---

**Design Hub must not list archived or template-only HTML, and must resolve stale
`storage/<user>/` preview URLs to live `resumes/<user>/` files.**

**Why:** The library scan walked `storage/_archive` and picked up `*.template.html`
cards that were not real working documents. HTTP served raw paths, so bookmarks and
deep-links still using `/storage/<user>/…` 404'd even when the same HTML lived under
`resumes/<user>/` after the root-noun move. Jenni title galleries and Shade work-samples
looked "not found" in the Hub while the files existed one noun over.

**How to apply:**

- Hub scan: `EXCLUDE_PARTS` includes `_archive`; skip `*.template.html`.
- Preview serve: route files through `resolve_preview_file` / `resolve_rel` so the
  dual-run alias maps `storage/<user>/…` → `resumes/<user>/…` when the live file exists.
- Do not recreate a `storage/` directory — the resolver is for old URLs and tests only.

Related: [[lesson-scaffold-readme-must-not-win-path-resolution]] · [[lesson-ssot-dashboard-must-name-live-paths]]
