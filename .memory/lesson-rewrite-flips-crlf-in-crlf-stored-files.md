---
name: lesson-rewrite-flips-crlf-in-crlf-stored-files
description: Rewriting a tracked file with the Write tool normalizes CRLF to LF — in this repo Python files are stored CRLF, so a 19-line edit showed as a 247-line diff
metadata:
  type: feedback
  date: 2026-10-16
---

Before committing a file you rewrote **in full** (rather than edited in place), check that you did not
also change its line endings: `git diff --numstat <file>` next to
`git ls-files --eol <file>`.

**Why:** this repo has no `.gitattributes` and `core.autocrlf=false`, so a file's bytes are stored as
authored — and they are **not uniform**: `src/pdf_tool/*.py` is CRLF while `docs/*.md` and
`.gitignore` are LF. A full-file rewrite from an editor/agent that emits LF silently flips a CRLF file,
which makes every line differ and buries the real change. It happened here: a 19-line CLI fix reported
as `247 changed lines`, and `git diff --ignore-cr-at-eol` was the only way to see the truth.

**How to apply:** after any whole-file write to a **tracked** file, run
`git ls-files --eol <path>` and compare `i/` (index) with `w/` (worktree). If `i/crlf` and `w/lf`,
normalize the worktree file back to CRLF before staging:

```powershell
$t = [System.IO.File]::ReadAllText($p) -replace "`r`n","`n" -replace "`n","`r`n"
[System.IO.File]::WriteAllText($p, $t, (New-Object System.Text.UTF8Encoding($false)))
```

Prefer the Edit tool for tracked source files — it preserves the existing line endings. Reserve a full
rewrite for files whose whole content is genuinely being replaced.

Related: [[lesson-utf8-json-roundtrip-on-windows]]
