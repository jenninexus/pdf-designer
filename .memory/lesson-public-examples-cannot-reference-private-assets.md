---
name: lesson-public-examples-cannot-reference-private-assets
description: A tracked example must not depend on an ignored local font, image, stylesheet, or other `storage/` asset.
metadata:
  type: project
  date: 2026-08-13
---

Public HTML must render from public inputs alone. Do not reference `storage/`, `users/`, `vaults/`,
`profiles/`, `resumes/`, `_job-apps/`, or another ignored workspace location from a tracked example asset URL.

**Why:** a local checkout can hide the mistake because the private file exists. A fresh clone silently
falls back to another font or loses an image, so the advertised seed no longer matches the checked-in
example.

**How to apply:** keep example assets tracked beside the template or use a platform/system fallback.
Licensed shared typography belongs in `themes/fonts/` with its redistribution notice, not in a private
font cache. Keep examples identity-neutral as well as path-safe. Run
`python -m pytest tests/test_public_example_assets.py`, `python scripts/smoke-white-label.py`, and the
document's `python -m pdf_tool.check_generation <example>.html` gate before shipping a public example.

**2026-08-13 follow-through:** the original test caught only `storage/` URLs, while the public letter
used a local-name signature and the brand template named a private map. The test now guards every
private root noun; the smoke scan covers the complete `examples/` tree; Parisienne and Montserrat ship
as verified OFL assets under `themes/fonts/`. A local Hub can still show private documents by design,
so use `python -m pdf_tool.preview examples --no-open` to review the exact public-seed library.

Related: [[lesson-public-clone-path-stays-tracked]] · [[lesson-scaffold-readme-must-not-win-path-resolution]]
