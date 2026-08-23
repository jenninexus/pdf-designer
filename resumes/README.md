# `resumes/` — working HTML (not the PDFs)

Per-person **source** tree: `resumes/<id>/{html,defaults,resources,templates}`.
Generated PDFs and PNGs live in **[`output/<id>/resumes/`](../output/README.md)**.

| Tracked | Gitignored |
|---|---|
| this README | HTML, private resources, job-letter HTML |

**Vault SSOT is [`vaults/<id>.json`](../vaults/), not a `resume-source.json` in this folder.**

| What | Where |
|---|---|
| Go-to HTML | `resumes/<id>/defaults/` |
| Go-to PDFs | `output/<id>/resumes/` (flat) |
| Per-job PDFs | `output/<id>/resumes/<App>/` |
| Shared MG gallery | `resumes/studio/resources/images/martiangames/` (junctions from jenni/shade) |

There is no repo-root `--output-dir/` folder — that name is a CLI flag
(`html_to_pdf --output-dir <dir>`). Omit the flag and the engine infers
`output/<user>/resumes/`.

Legacy alias: `storage/<id>/`. See [`docs/STORAGE.md`](../docs/STORAGE.md) ·
[`docs/EXPORTS.md`](../docs/EXPORTS.md).
