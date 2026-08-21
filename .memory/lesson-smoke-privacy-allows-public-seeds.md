---
name: lesson-smoke-privacy-allows-public-seeds
description: The public smoke guard must reject real private payloads while explicitly allowing only the tracked Jane Example cards and application template.
metadata:
  type: project
  date: 2026-08-21
---

Keep `scripts/smoke-white-label.py`'s tracked-private-path allowlist narrow and explicit.
`users/examples.json`, `vaults/examples.json`, `profiles/examples.json`, and
`_job-apps/_template/` are intentional clone-safe teaching assets; they do not weaken the privacy
boundary. Every other tracked payload under a private root remains a smoke failure.

**Why:** the guard classified its allowed source roots by directory name alone. Once the public Jane
Example Hub cards and private provider template became tracked, the fresh-clone gate failed before rendering
anything — blocking a healthy public release with a false privacy alarm.

**How to apply:** when adding a public seed under a private-shaped root, add only its exact path (or the
smallest template prefix) to the smoke allowlist, then run `python scripts/smoke-white-label.py`. Never
allow an entire private root.

Related: [[lesson-public-examples-cannot-reference-private-assets]]
