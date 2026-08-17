# `resumes/` — working HTML + exports

Per-person working tree: `resumes/<id>/{html,defaults,_exports,resources}`.

| Tracked | Gitignored |
|---|---|
| this README | HTML, PDFs, `_exports/`, private resources |

**Vault SSOT is [`vaults/<id>.json`](../vaults/), not a `resume-source.json` in this folder.**
Exports: per-job PDFs in `_exports/<Track>/`; the reusable go-to pack in `defaults/`
(same folder as the HTML). There is no repo-root `--output-dir/` folder — that name
is a CLI flag (`html_to_pdf --output-dir <dir>`).

Legacy alias: `storage/<id>/`. Shared studio assets stay under `resumes/studio/resources/`
(or `brands/`) with the same junction rule as today — see [`docs/STORAGE.md`](../docs/STORAGE.md).
