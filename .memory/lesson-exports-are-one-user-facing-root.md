---
name: lesson-exports-are-one-user-facing-root
description: Deliberate PDFs/PNGs belong in repo-root _exports/ so CLI output and the Hub library cannot diverge; output/ is explicit automation scratch
metadata:
  type: project
  date: 2026-09-26
---

**How to apply:** omit `--output-dir` for a normal export. `pdf_tool.paths.default_output_dir`
writes `_exports/<profile>/<kind>/` (or `_exports/examples/`, `_exports/<kind>/`, or
`_exports/unfiled/`). The Hub displays the physical `_exports/` root as **Exports** and scans its
artifacts read-only. Scripts that need disposable proof files must opt into `output/<run>/`.

**Why:** splitting public/default exports into `output/` and private exports into `_exports/` created
two user journeys. Worse, the Hub only browsed `_exports/`, so a new user's successful default export
was absent from the app's library. Privacy does not require a second destination because payloads in
both roots are ignored.

**Keep source separate:** editable HTML/images stay in `examples/`, `resumes/`, `collages/`, or
`_job-apps/`. `_exports/` is a deliverable library, never the only copy of source media. `output/`
may be deleted and must never be referenced as a submitted/final artifact.

Related: [[lesson-output-is-repo-root]] (superseded) ·
[[lesson-defaults-export-beside-html]] (superseded) ·
[[lesson-private-collage-source-assets]]
