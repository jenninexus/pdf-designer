# `resumes/` — this person's sources *and* their finished PDFs

Per-person tree: `resumes/<id>/{defaults,resources,templates}` plus the generated files themselves.
**A personal résumé/letter/work-sample PDF lands under `resumes/<id>/` — that is the destination, not a
fallback.** `_exports/<id>/resumes/` exists only for a source the engine cannot match to a person here.

| Tracked | Gitignored |
|---|---|
| this README | HTML, private resources, job-letter HTML, generated PDFs/PNGs |

**Vault SSOT is [`vaults/<id>.json`](../vaults/), not a `resume-source.json` in this folder.**

| What | Where |
|---|---|
| Go-to HTML | `resumes/<id>/defaults/` |
| Go-to personal PDFs | `resumes/<id>/` (flat) |
| Per-job personal PDFs | `resumes/<id>/<App>/` |
| **Multi-application company** (`micro1`, `Meta`) | `resumes/<id>/<Company>/<Role>/` — see below |
| The exact file a posting received | `resumes/<id>/…/submitted-<company>-<slug>-<date>/` |
| Reusable person resources | `resumes/<id>/resources/{images,logos,videos,references}/` |
| Shared MG gallery | `resumes/studio/resources/images/martiangames/` (junctions from jenni/shade) |
| Public/example fallback | `_exports/examples/` |
| Disposable smoke/QA scratch | `output/examples/` (not a library; not scanned by the Hub) |

### Multi-application companies get a folder

When one company posts several near-identical roles at once, group them so the role folders don't pile up
flat — and drop the company prefix inside the group:

```text
resumes/shade/Micro1/Research-Engineering/
resumes/shade/Micro1/Art-Related-Professional/
resumes/shade/Meta/Technical-Game-Designer/
resumes/shade/Sony-3D-Characters/        ← single-application company stays flat
```

Group at two-or-more applications for that person. The `_job-apps/<App>/` record stays **flat** and keeps
its company-prefixed name. ⚠️ Exports into a company group need an explicit
`--output-dir resumes/<id>/<Company>/<Role>` — the engine infers a flat path from the `_job-apps/<App>/`
name. [`docs/STORAGE.md`](../docs/STORAGE.md) § Company grouping.

### `output/` and `_exports/` are not where a real document goes

There is no repo-root "output folder" step in the workflow. `--output-dir` is a **CLI flag**: omit it and
the engine infers `resumes/<id>/` (plus the job folder when the source is under `_job-apps/<App>/`).
`output/` is chosen *explicitly* for disposable automation and smoke-test scratch — the public smoke test
writes `output/examples/` on purpose, and the Hub ignores that tree. `_exports/` is the public/unfiled
fallback for a source with no `resumes/<id>/` to land in yet.[^1]

Legacy alias: `storage/<id>/` (retired tree; see [`docs/STORAGE.md`](../docs/STORAGE.md) ·
[`docs/EXPORTS.md`](../docs/EXPORTS.md)).

[^1]: This README previously said "Public examples and direct engine runs still use `output/`", which read
as if `output/` were the user-facing destination. It is not: the smoke/QA script uses it as scratch, and
engine inference falls back to `_exports/examples/`. Corrected 2026-10-16.
