# `_exports/` — the export library

This is the single user-facing destination for deliberate PDFs, PNG previews, collages, and other generated deliverables. It is used by public examples and local profiles alike:

```text
_exports/<profile>/resumes/<application>/
_exports/<profile>/collages/<project>/
_exports/examples/
_exports/unfiled/
```

Only this README is tracked. Export payloads stay ignored. Keep editable source in `examples/`, `resumes/`, `collages/`, or `_job-apps/`; never treat an exported PDF as the source of truth.

The engine defaults here so every export appears in the Design Hub. `output/` is separate disposable automation/test scratch and is never the user's document library.

Do not create `docs/_exports/` or other nested export roots. Documentation images intended for publication belong in `docs/images/`; generated documentation previews belong here.

To browse these files without exposing them, run the Design Hub, select the matching profile, then
choose **Exports** in the folder picker. The UI uses that friendly label while the physical folder remains `_exports/`. PDF/image cards are read-only. Use the per-card comparison
checkboxes and **Focus N** when comparing a smaller set.
