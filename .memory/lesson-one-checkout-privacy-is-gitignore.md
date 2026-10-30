---
name: lesson-one-checkout-privacy-is-gitignore
description: One engine for you and strangers — gitignore + *.example.json, not a second app or .env.local
metadata:
  type: project
  date: 2026-08-13
---

Use **one pdf-designer engine** with ignored personal trees (`users/` · `vaults/` · `_job-apps/` · `resumes/` · `brands/` · `storage/` alias) and tracked `*.example.json` / `examples/`. Ignore rules protect new additions only: they do not remove tracked files, historical blobs or private pixels from screenshots. Audit the exact staged paths, content and images; use the public-push guard and review historical exposure separately. Do not add `.env` / `.env.local` unless a tool actually reads it.

**Why:** Personal workspace data and a public engine need distinct storage boundaries, not duplicate engines. An old image archive contained real career-document pixels even though text scans and current ignores passed. Public captures must use a clone-safe workspace; `scripts/capture-hub-stills.py` no longer opens a personal screenshot pack.

**How to apply:** Clone-safe teaching files live at `users/you.example.json`, `vaults/you.example.json`, and `profiles/you-resume.example.json`; Hub demos use `examples/resume-studio/`. Real payload stays ignored in the same checkout, with verified private backup. Exports live beside their document family; `_exports/` is the public/unfiled fallback. Future paid-source isolation is a separate implementation slice in `docs/DEVELOPMENT-FLOW.md`; an ignored directory alone does not implement a premium loader.

Tracker is **who × job** (`_job-apps/applied-index.md` + `python -m pdf_tool.tracker list`). Do not daily-count submissions.

Related: [[lesson-public-clone-path-stays-tracked]] · [[lesson-scaffold-readme-must-not-win-path-resolution]]
