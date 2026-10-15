---
name: lesson-required-render-failure-must-fail
description: A missing browser or renderer is incomplete QA, never a successful shipping gate.
metadata:
  type: feedback
  date: 2026-10-15
---

When full document QA is requested, a renderer/dependency failure must fail the composed gate.
Only an explicit source-only run may skip render checks, and its report must identify that mode.

**Why:** render helpers returned `ok=True` with `(skipped render — ...)` on exceptions. The composed
gate trusted the boolean, so an unavailable browser could produce a green report without checking
the artifact. `run_file` now rejects those unavailable-check messages in rendered mode. Non-applicable
checks (for example résumé-only text checks on a letter) remain a distinct valid case.

**Guard:** `tests/test_check_generation_verification.py` covers required-render failure, deliberate
source-only mode and a non-applicable check. Actual document QA also exercises working Chromium.
The owning protocol is [docs/QA.md](../docs/QA.md); do not treat a source-only PASS as acceptance.
