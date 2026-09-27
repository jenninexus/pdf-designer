---
name: lesson-defaults-export-beside-html
description: SUPERSEDED — go-to PDFs now export flat into resumes/<profile>/ (fallback _exports/<profile>/resumes/ only when unmatched); HTML stays in resumes/<profile>/defaults/
metadata:
  type: feedback
  date: 2026-08-08
  superseded: 2026-08-22
---

**Superseded.** The 2026-08-08 rule (write go-to PDFs into `defaults/` beside
the HTML so the Hub picker could see them) mixed source and artifacts. The 2026-09-26 rule (repo-root
`_exports/<profile>/resumes/`) was itself superseded 2026-09-27: the engine default is now
`resumes/<profile>/` (flat), beside the document family; `_exports/<profile>/resumes/` is fallback
only for an unmatched source. Hub lists HTML under `resumes/<profile>/defaults/` and exported PDFs
under the friendly **Exports** filter (or directly in the profile's own `resumes/<profile>/` folder).

See [[lesson-exports-are-one-user-facing-root]] (historical) and `docs/STORAGE.md` (current).
