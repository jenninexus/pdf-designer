---
name: lesson-utf8-json-roundtrip-on-windows
description: Never round-trip UTF-8 JSON configs through PowerShell/cp1252 — prefer surgical Edit patches; restore with git checkout if bytes corrupt
metadata:
  type: feedback
  date: 2026-08-08
---

When patching tracked UTF-8 JSON that contains emoji / fancy punctuation (⭐, —), **do not** rewrite the
whole file via a PowerShell one-liner that shells `python -c "json.dumps(...)"` and writes back.

**Why:** On SEGOPC the console/default codec is often **cp1252**. A full round-trip can emit a corrupt
byte (`0x90`) for characters that were valid UTF-8. The next `json.load` fails with
`UnicodeDecodeError: 'charmap' codec can't decode byte 0x90` — and a large `git diff` can look like
"everything changed" even when only one key was intended.

**How to apply:**

1. Prefer the editor **Edit** tool for a one-key change (e.g. `layouts.resume` → `layouts.documents`).
2. If using Python, open/write with `encoding="utf-8"` from a `.py` file — never rely on the console codec.
3. If corruption is already on disk: `git checkout -- <file>`, then re-apply the minimal patch.
4. Verify: `json.load` + assert `"\u2b50" in data["layouts"]["_role"]`.

Hit while updating `.config/mcp-pdf-designer.json` for the `layouts/resume/` → `layouts/` flatten
(2026-08-08). Recovered with checkout + surgical patch; no intentional keys were lost.

Related: [[lesson-defaults-export-beside-html]]
