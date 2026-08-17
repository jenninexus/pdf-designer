---
name: lesson-flag-looking-output-dir
description: pdf_to_png treats leftover CLI flags as a folder name — refuse paths that start with -
metadata:
  type: feedback
  date: 2026-08-17
---

**Refuse an output path that starts with `-`.** `pdf_to_png` takes a *positional*
out-dir (`python -m pdf_tool.pdf_to_png doc.html out-dir`). If someone pastes
`html_to_pdf`'s `--output-dir` flag by mistake, Python happily creates a folder
named `--output-dir/` and writes PNGs into it.

**Why:** two CLIs, two shapes. `html_to_pdf` uses `--output-dir <dir>`.
`pdf_to_png` uses a second positional. A leftover flag is a valid Windows
folder name, so mkdir succeeds and the dump looks like a product directory.

**How to apply:** `paths.reject_flag_looking_path` runs in both CLIs. Default
exports already land beside the HTML (`resumes/<id>/_exports/` or `defaults/`).
Never invent a repo-root `--output-dir/` folder. `.gitignore` lists
`--output-dir/` as a belt-and-suspenders ignore.

Related: [[lesson-defaults-export-beside-html]]
