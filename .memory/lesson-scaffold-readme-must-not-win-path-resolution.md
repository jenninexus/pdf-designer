---
name: lesson-scaffold-readme-must-not-win-path-resolution
description: A tracked README in users/ or applications/ must not steal live storage/ paths during dual-run
metadata:
  type: feedback
  date: 2026-08-13
---

**Path resolution must require payload, not directory existence.** A tracked
`applications/README.md` (or `users/README.md`) makes that folder *exist*. If
`resolve_rel` treats “directory exists” as a hit, Hub / tracker / vault skip
the live `storage/` tree and look empty.

**Why:** The free GitHub product needs those folders visible in the clone file
tree (`WORKSPACE-LAYOUT.md`). Live SEGO data still lives under `storage/` until
the copy. Dual-run therefore has **README-only new nouns + full legacy tree**
at the same time. `.exists()` on the directory is true for a scaffold; that is
not “the jobs moved.”

**How to apply:** In `pdf_tool.paths`, `_has_payload` ignores `README.md`,
`.gitkeep`, and `*.example.json`. File lookups (`vault_path`, `user_path`) still
prefer an existing **file** on the new noun. Directory helpers (`applications_dir`)
keep `storage/_job-listings` while the new tree is README-only. Tests:
`tests/test_workspace_paths.py` (`test_scaffold_dir_does_not_steal_legacy_jobs`).
Do **not** delete `storage/` until a copy has real files under the new nouns and
dual-run smoke is green.

Related: [[lesson-public-clone-path-stays-tracked]]
