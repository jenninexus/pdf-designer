---
name: lesson-defaults-export-beside-html
description: Export reusable go-to résumé/cover/work-samples PDFs into storage/<user>/defaults/ beside the HTML — never into _exports/defaults/
metadata:
  type: feedback
  date: 2026-08-08
---

When refreshing a user's **defaults** pack, write PDFs with `--output-dir storage/<user>/defaults` (or an explicit path under that folder). Do **not** use `_exports/defaults/`.

**Why:** Design Hub lists HTML under `storage/<user>/defaults/`. PDFs that land in `_exports/defaults/` are invisible next to the picker path the human uses (`/?doc=storage/jenni/defaults/…`). Vault `goToPacks.*.exportDir` must match.

**How to apply:**

```bash
python -m pdf_tool.check_generation storage/<user>/defaults/<doc>.html
python -m pdf_tool.html_to_pdf storage/<user>/defaults/<doc>.html --pdf-theme dark --output-dir storage/<user>/defaults --force
```

Related: [[lesson-work-samples-footer-row-false-collision]]
