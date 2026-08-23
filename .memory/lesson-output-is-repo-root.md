---
name: lesson-output-is-repo-root
description: Generated PDFs/PNGs go to repo-root output/<user>/<kind>/ — never beside the HTML, never into storage/, never into a retired _exports/ folder
metadata:
  type: project
  date: 2026-08-22
---

**How to apply:** omit `--output-dir`. `pdf_tool.paths.default_output_dir` writes
`output/<user>/resumes/` (or `…/collages/`, `output/examples/`, `output/` when
no profile). HTML stays in `resumes/<user>/defaults/` and collage sources stay
in `collages/<project>/`. Vault `goToPacks.*.exportDir` must match the PDF
folder.

**Why:** Mixing generated files with source HTML hid personal docs from the
Design Hub (which skips `_exports/` and now `output/`) and made "where did my
PDF go?" unanswerable. Putting source trees under `_exports/resumes/` also
broke the MG gallery junction (`resumes/studio/…` must exist first).

**Do not** restore the old "export go-to packs into `defaults/` beside the HTML"
rule — that lesson is superseded. Hub previews HTML from `resumes/`; humans
grab PDFs from `output/<user>/resumes/`.

Related: [[lesson-defaults-export-beside-html]] (superseded) ·
[[lesson-flag-looking-output-dir]] · [[lesson-hub-archive-not-found]]
