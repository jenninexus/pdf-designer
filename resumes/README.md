# `resumes/` — working HTML *and* this person's PDFs

Per-person **source** tree: `resumes/<id>/{html,defaults,resources,templates}`.
Personal generated PDFs and PNGs now live **beside their document family, in this same
`resumes/<id>/` tree** — `_exports/<id>/resumes/` (see [`../_exports/README.md`](../_exports/README.md))
is fallback only, for a source the engine can't match here.
Public examples and direct engine runs still use [`output/`](../output/README.md).

| Tracked | Gitignored |
|---|---|
| this README | HTML, private resources, job-letter HTML, generated PDFs/PNGs |

**Vault SSOT is [`vaults/<id>.json`](../vaults/), not a `resume-source.json` in this folder.**

| What | Where |
|---|---|
| Go-to HTML | `resumes/<id>/defaults/` |
| Go-to personal PDFs | `resumes/<id>/` (flat) |
| Per-job personal PDFs | `resumes/<id>/<App>/` |
| Public/example PDFs | `output/examples/` |
| Shared MG gallery | `resumes/studio/resources/images/martiangames/` (junctions from jenni/shade) |

There is no repo-root `--output-dir/` folder — that name is a CLI flag
(`html_to_pdf --output-dir <dir>`). Omit the flag and the engine infers
`resumes/<id>/` (plus the job folder when the source is under `_job-apps/<App>/`).

Legacy alias: `storage/<id>/`. See [`docs/STORAGE.md`](../docs/STORAGE.md) ·
[`docs/EXPORTS.md`](../docs/EXPORTS.md).
