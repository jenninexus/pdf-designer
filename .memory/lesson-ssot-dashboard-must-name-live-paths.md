---
name: lesson-ssot-dashboard-must-name-live-paths
description: After a folder rename, SSOT.md and wrap checklists must name the live path — engine dual-run is not enough
metadata:
  type: feedback
  date: 2026-08-17
---

**When live data moves, update the session-start dashboard in the same wrap.** `pdf_tool.paths`
dual-run plus a correct `STORAGE.md` do not stop the next agent from writing into the old
folder if `docs/SSOT.md` (session start #3), `AGENTS.md` privacy rows, or `/pdf-wrap` still
name the legacy path.

**Why:** The 2026-08-13 root-noun copy put palettes in `brands/`. The engine already prefers
that folder and aliases `storage/brand-design/`. After the 2026-08-16 archive, the live
payload left `storage/brand-design/`. `STORAGE.md` was updated; `SSOT.md`, THEME-DESIGN
prefs tables, the wrap checklist, and Step 6 SMB copy still said `storage/brand-design/`.
A wrap that only touches the engine + STORAGE leaves the first file agents read stale.

**How to apply:** After any path migration, grep `docs/SSOT.md`, `AGENTS.md`,
`.claude/commands/pdf-wrap.md`, and `THEME-DESIGN.md` for the **old** folder name and
retarget them in the same wrap. Keep the old name only as “(was …)” / dual-run alias.
Do not treat “the resolver still finds it” as “the docs are honest.”

Related: [[lesson-scaffold-readme-must-not-win-path-resolution]]
