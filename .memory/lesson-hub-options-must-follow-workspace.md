---
name: lesson-hub-options-must-follow-workspace
description: Design Hub filter and palette options must derive from the previewed workspace, not a hard-coded local roster or the package checkout root
metadata:
  type: project
  date: 2026-08-13
---

**Make Design Hub options data-driven from the workspace it is serving.** Profile selectors must be
built from `users/` + `profiles/` (including their `storage/` aliases) and document ownership; private
brand palettes must be discovered from that same requested root. Rebuild the profile controls whenever
the live index refreshes.

**Why:** the first dual-path resolver correctly made the document scan understand `resumes/` and
`storage/<user>/`, but the desktop and drawer headers still carried a four-name hard-coded profile
roster. `python -m pdf_tool.preview <other-root>` also scanned the requested documents while its
palette dropdown silently read `brands/` from the package checkout. New or migrated workspace options
therefore disappeared from the UI even when the library could render their files.

**How to apply:**

- Use `workspace_profile_ids()` / `available_profile_ids()` for every profile selector, and retain
  document-derived IDs for legacy content without a card.
- Pass the `serve(root)` root to `load_palettes(root)`; public themes remain package-owned, private
  `brands/` and `storage/brand-design/` are workspace-owned.
- Keep `.json` in the watcher signature so a new profile card refreshes the header choices without a
  server restart.
- Prove both desktop and drawer options with a handler HTTP smoke, plus a custom-root palette test.

Related: [[lesson-scaffold-readme-must-not-win-path-resolution]]
