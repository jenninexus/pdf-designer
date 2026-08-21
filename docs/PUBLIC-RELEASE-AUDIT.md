# Public release content boundary

This is the release checklist for a clone-safe PDF Designer repository. It describes
what belongs in a future public release; it does not change an already-published
remote by itself.

## Keep public

- The engine, layouts, public themes and font notices.
- Fictional examples and the white-label smoke test.
- Product-facing technical documentation: setup, exports, previewer, packaging,
  quality checks, licensing, theming, collage design, and the optional Voice Seed
  handoff contract.
- Deliberately approved promotional images under `docs/images/`.

## Keep local only

- Agent runbooks, session memory, active/completed plans, and history-rewrite
  notes.
- Live user, vault, profile, job, résumé, brand, export, and collage data.
- Application workflow notes that describe real people, real work, or local paths.
- Any secret, token, environment configuration, capture, or unpublished media.

## Required before any future external release

1. Remove local-only operating records from Git tracking while preserving the local
   working copies, then rely on `.gitignore` to keep them local.
2. Replace or remove public-document links that point to those records.
3. Review every tracked text file for local paths, private names, and operational
   history; keep only generic product guidance.
4. Run `python scripts/smoke-white-label.py`, `python scripts/check-wheel-assets.py`,
   and a clean-clone documentation-link check.
5. Obtain explicit human approval for any external release action. This project must
   never push automatically.

The present workspace has the ignore policy and public documentation index prepared;
the local-only files remain intact for current work. No GitHub action is implied.
