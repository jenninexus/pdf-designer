---
name: lesson-smoke-privacy-allows-public-seeds
description: The public smoke guard must reject real private payloads while explicitly allowing only the tracked Jane Example cards and copy-me seeds.
metadata:
  type: project
  date: 2026-08-21
---

Keep `scripts/smoke-white-label.py`'s tracked-private-path allowlist narrow and explicit.
`users/examples.json`, `vaults/examples.json`, `profiles/examples.json`, and `*.example.json`
copy-me shapes are intentional clone-safe teaching assets; they do not weaken the privacy boundary.
The generic `_job-apps/_template/README.md` is a folder pointer, not a listing template. Every
other tracked payload under a private root remains a smoke failure.

**Why:** the guard classified its allowed source roots too broadly. Jane Example cards need a narrow
exception so a fresh clone has a working Hub; a whole `_job-apps/_template/` exception would also
silently permit account-specific private provider material to ship.

**How to apply:** when adding a public seed under a private-shaped root, add only its exact path (or a
copy-me suffix that still excludes real payloads) to the smoke allowlist, then run
`python scripts/smoke-white-label.py`. Never allow an entire private root or template directory.

Related: [[lesson-public-examples-cannot-reference-private-assets]]
