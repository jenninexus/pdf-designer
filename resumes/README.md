# `resumes/` — working HTML (not the PDFs)

Per-person **source** tree: `resumes/<id>/{html,defaults,resources,templates}`.
Personal generated PDFs and PNGs live in **[`_exports/<id>/resumes/`](../_exports/README.md)**.
Public examples and direct engine runs still use [`output/`](../output/README.md).

| Tracked | Gitignored |
|---|---|
| this README | HTML, private resources, job-letter HTML |

**Vault SSOT is [`vaults/<id>.json`](../vaults/), not a `resume-source.json` in this folder.**

| What | Where |
|---|---|
| Go-to HTML | `resumes/<id>/defaults/` |
| Go-to personal PDFs | `_exports/<id>/resumes/` (flat) |
| Per-job personal PDFs | `_exports/<id>/resumes/<App>/` |
| Public/example PDFs | `output/examples/` |
| Shared MG gallery | `resumes/studio/resources/images/martiangames/` (junctions from jenni/shade) |

There is no repo-root `--output-dir/` folder — that name is a CLI flag
(`html_to_pdf --output-dir <dir>`). Omit the flag and the engine infers
`output/<user>/resumes/`.

Legacy alias: `storage/<id>/`. See [`docs/STORAGE.md`](../docs/STORAGE.md) ·
[`docs/EXPORTS.md`](../docs/EXPORTS.md).
