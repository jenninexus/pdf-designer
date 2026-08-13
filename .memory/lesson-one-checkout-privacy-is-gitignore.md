---
name: lesson-one-checkout-privacy-is-gitignore
description: One engine for you and strangers — gitignore + *.example.json, not a second app or .env.local
metadata:
  type: project
  date: 2026-08-13
---

Use **one pdf-designer checkout**. Privacy is gitignore of personal trees (`users/` · `vaults/` · `_job-apps/` · `resumes/` · `brands/` · `storage/` alias) plus tracked `*.example.json` and `examples/`. Do not invent a second app, and do not add `.env` / `.env.local` unless a tool actually reads env vars — this engine does not.

**Why:** Asking “do I need two versions?” usually means mixing SEGO vaults with the public seed. A `.env` would document a fiction (`AGENTS.md`: reads no environment variables). Machine paths already live in `.config/mcp-pdf-designer.json`.

**How to apply:** Clone-safe teaching files at `users/you.example.json`, `vaults/you.example.json`, `profiles/you-resume.example.json`. Hub demos use `examples/resume-studio/`. After the 2026-08-13 copy, `_exports` live under `resumes/<user>/_exports/` — deleting `storage/` later does not delete those copies, but wait until dual-run smoke has lived.

Tracker is **who × job** (`_job-apps/applied-index.md` + `python -m pdf_tool.tracker list`). Do not daily-count submissions.

Related: [[lesson-public-clone-path-stays-tracked]] · [[lesson-scaffold-readme-must-not-win-path-resolution]]
