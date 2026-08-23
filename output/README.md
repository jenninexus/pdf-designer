# `output/` — generated PDFs and PNGs

Repo-root folder for **finished renders**. Source HTML stays in `resumes/` and
`collages/` (and public examples stay in `examples/`). The engine default
(no `--output-dir`) is `pdf_tool.paths.default_output_dir`.

```text
output/<user>/resumes/             go-to packs (flat)
output/<user>/resumes/<App>/       this job
output/<user>/collages/<project>/  that person's collage renders
output/collages/<project>/         collage with no inferred profile
output/examples/                   public Jane Example / smoke PDFs
output/                            truly unknown source
```

| Tracked | Gitignored |
|---|---|
| this README | every PDF, PNG, and job folder |

`storage/` is a private leftover and is **not** the output SSOT. `_exports/` is a
retired alias (gitignored); do not write new files there.

Personal clone and the shipped product use the same layout. A stranger's first
export from `examples/profiles/default-resume/` lands in `output/examples/`.
