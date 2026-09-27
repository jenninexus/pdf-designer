---
name: lesson-output-is-repo-root
description: SUPERSEDED 2026-09-26 — deliberate exports now use repo-root _exports/; output/ is explicit automation scratch
metadata:
  type: project
  date: 2026-08-22
  superseded: 2026-09-26
---

**Superseded.** The useful part of this lesson remains: keep generated deliverables out of editable
source folders. Its destination decision no longer holds. The engine and Hub now use one repo-root
`_exports/` library for every deliberate export; `output/` is explicit disposable automation/test
scratch.

See [[lesson-exports-are-one-user-facing-root]].
