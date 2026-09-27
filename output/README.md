# `output/` — automation and test scratch

Repo-root scratch space for smoke tests, packaging checks, benchmarks, and other disposable automation. It is not the default export destination and the Design Hub does not present it as the user's library.

```text
output/smoke/
output/test-runs/
output/<tool-specific-scratch>/
```

| Tracked | Gitignored |
|---|---|
| this README | every PDF, PNG, and job folder |

Callers must opt in with `--output-dir output/...`; routine CLI and Hub exports default to beside
their document family (`resumes/<user>/`, `collages/<project>/`), falling back to
[`../_exports/`](../_exports/) for public examples or an unmatched source. Scratch files may be
deleted and must never be referenced as a submitted or final deliverable.

A stranger's first export from `examples/profiles/default-resume/` lands in `_exports/examples/` and is immediately visible under **Exports** in the Hub.
