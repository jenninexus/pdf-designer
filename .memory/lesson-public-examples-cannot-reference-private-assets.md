---
name: lesson-public-examples-cannot-reference-private-assets
description: A tracked example must not depend on an ignored local font, image, stylesheet, or other `storage/` asset.
metadata:
  type: project
  date: 2026-08-13
---

Public HTML must render from public inputs alone. Do not reference `storage/`, `resumes/`, `_job-apps/`,
or another ignored workspace location from a tracked example asset URL.

**Why:** a local checkout can hide the mistake because the private file exists. A fresh clone silently
falls back to another font or loses an image, so the advertised seed no longer matches the checked-in
example.

**How to apply:** keep example assets tracked beside the template or use a platform/system fallback.
Run `python -m pytest tests/test_public_example_assets.py` and the document's
`python -m pdf_tool.check_generation <example>.html` gate before shipping a public example.

Related: [[lesson-public-clone-path-stays-tracked]] · [[lesson-scaffold-readme-must-not-win-path-resolution]]
