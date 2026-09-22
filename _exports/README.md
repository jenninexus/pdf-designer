# `_exports/` — private personal deliverables

This root is the local, gitignored workspace for real applicant/studio PDFs, PNG previews, and other generated deliverables:

```text
_exports/<user>/resumes/<application>/
_exports/<user>/collages/<project>/
```

Only this README is tracked. Personal payloads stay ignored. Keep source HTML in the corresponding private root noun (`resumes/`, `collages/`, or `_job-apps/`).

The public engine and white-label examples still default to `output/`; `output/README.md` remains the tracked public anchor. Personal command copies and private profiles pass `--output-dir _exports/...` explicitly.

Do not create `docs/_exports/` or other nested export roots. Documentation images intended for publication belong in `docs/images/`; generated documentation previews belong here.

To browse these files without exposing them, run the Design Hub, select the matching profile, then
choose the virtual **`_exports`** folder. PDF/image cards are read-only. Use the per-card comparison
checkboxes and **Focus N** when comparing a smaller set.
