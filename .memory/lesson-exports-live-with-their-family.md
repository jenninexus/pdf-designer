---
name: lesson-exports-live-with-their-family
description: Exports live beside their document family (resumes/<user>/<App>/, collages/<project>/); _exports/ is only the examples/unfiled fallback — and the Hub must discover every family root or cards "fail to load"
metadata:
  type: project
  date: 2026-09-27
---

**Rule:** finished PDFs/PNGs live WITH their family — `resumes/<user>/<App>/` for a job,
`resumes/<user>/` for go-to packs, `collages/<project>/` for collages. `_exports/` only catches public
`examples/` renders and unfiled sources, so a fresh clone still works. Owner directive 2026-09-27,
reversing the 2026-09-26 single-library model ([[lesson-exports-are-one-user-facing-root]]).

**Why:** people look for a job's PDFs next to that person's other work, not in a parallel tree that
mirrors `resumes/`. The single library made every lookup a two-tree hunt. The earlier trap still
applies in the other direction: the Hub listed artifacts ONLY from `_exports/`, so once files moved,
its cards pointed at missing paths ("failed to load") and the relocated PDFs were invisible.

**How to apply:** omit `--output-dir`; `pdf_tool.paths.default_output_dir` maps
`_job-apps/<App>/<user>-….html` → `resumes/<user>/<App>/` (user = longest filename prefix matching
`users/<id>.json` or `resumes/<id>/`), `resumes/<user>/…` → `resumes/<user>/`, `collages/<project>/…`
→ `collages/<project>/`, else `_exports/`. `preview.iter_export_artifacts` discovers every family root
(PDFs under `resumes/`, images outside `resources/`, collage project-root files, all of `_exports/`) and
the folder picker's **Exports (all finished files)** shows them in one view. If you move exports by
hand, click the Hub's refresh so stale cards drop. Tests: `tests/test_paths.py`,
`tests/test_preview_workspace.py::test_scan_finds_exports_beside_their_family`.

Related: [[lesson-exports-are-one-user-facing-root]] (superseded) · [[lesson-private-collage-source-assets]]
