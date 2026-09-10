---
name: lesson-default-light-must-override-dark-source
description: A default light export must override a dark theme already declared in the source HTML
metadata:
  type: feedback
  date: 2026-09-10
---

Treat the renderer's default as an explicit `light` theme assignment, not merely a `-light.pdf` filename.

**Why:** The export path once defaulted to `-light.pdf` while the DOM theme was changed only when `--pdf-theme` was supplied. An HTML document whose root already declared `data-pdf-theme="dark"` therefore produced a dark artifact with a light filename.

**How to apply:** Resolve an omitted or blank theme to `light` and always write that resolved value to the document root before PDF printing or PNG verification. Keep tests that start from a dark-root HTML source and assert the default PDF and PNG paths actively set `light`.
