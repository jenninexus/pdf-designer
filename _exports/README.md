# `_exports/` — fallback export folder

**Personal exports no longer live here.** Finished files live with their document family, so
a job's PDFs sit next to everything else about that person (owner directive 2026-09-27):

```text
resumes/<profile>/<application>/   per-job résumé · cover letter · work samples (+ <stem>-png/)
resumes/<profile>/                 go-to packs (sources stay in resumes/<profile>/defaults/)
collages/<project>/                finished collage PNGs (inputs in images/, renders in _candidates/)
```

This folder is only the **fallback** the engine uses when a source has no family:

```text
_exports/examples/   renders of the public examples/ documents (a fresh clone lands here)
_exports/unfiled/    anything the engine cannot place
```

Only this README is tracked; payloads stay ignored. Keep editable sources in `examples/`,
`resumes/`, `collages/`, or `_job-apps/`, and never treat an exported PDF as the source of truth.
`output/` is separate disposable automation/test scratch.

`python -m pdf_tool.html_to_pdf <doc>.html` picks the destination for you:
`_job-apps/<App>/<user>-….html` → `resumes/<user>/<App>/`, `resumes/<user>/…` → `resumes/<user>/`,
`collages/<project>/…` → `collages/<project>/`, everything else → here. Pass `--output-dir` to override.

**Design Hub:** choose **Exports (all finished files)** in the folder picker to see every exported
PDF and image in one view wherever it lives; `_exports (fallback)` shows only this folder. Cards are
read-only; use the comparison checkboxes and **Focus N** to compare a smaller set.

Do not create `docs/_exports/` or other nested export roots. Documentation images intended for
publication belong in `docs/images/`.
