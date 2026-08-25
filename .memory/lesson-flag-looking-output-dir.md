---
name: lesson-flag-looking-output-dir
description: pdf_to_png treats leftover CLI flags as a folder name — refuse paths that start with -
metadata:
  type: feedback
  date: 2026-08-17
---

**Refuse an output path that starts with `-`.** `pdf_to_png` takes a *positional*
out-dir (`python -m pdf_tool.pdf_to_png doc.html out-dir`). `html_to_pdf` takes an
optional positional PDF path after the HTML. If someone pastes `check_generation`'s
`--user shade` (or `html_to_pdf`'s `--output-dir`) into the wrong CLI, Python will
happily write `C:\Github\pdf-designer\--user` (a 2 MB PDF named like a flag).

**Why:** three CLIs, three shapes. `html_to_pdf` uses `--output-dir <dir>` and an
optional positional PDF. `pdf_to_png` uses a second positional. `check_generation`
uses `--user`. A leftover flag is a valid Windows file name.

**How to apply:** `paths.reject_flag_looking_path` runs on `--output-dir` **and**
on `html_to_pdf`'s positional output. Default exports already land under repo-root
`output/<user>/<kind>/` (see [[lesson-output-is-repo-root]]). Never invent a
repo-root `--user` or `--output-dir` file. `html_to_pdf` has no `--user` flag —
user is inferred from the HTML path.
