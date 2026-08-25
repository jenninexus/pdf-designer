---
name: lesson-layout-recipe-vs-inline-html
description: Layout JSON recipes are not applied automatically — default résumé HTML inlines CSS and can pack tighter than LAYOUT-SYSTEM
metadata:
  type: project
  date: 2026-08-25
---

`layouts/resume/two-page-standard.json` (and cover / work-examples siblings) document
spacing. They do **not** inject CSS. Jenni/Shade/Jane HTML often duplicates `@page`
and section gaps inline. Those values can drift (résumé `section` ~12px vs recipe
16–19px) while `check_generation` still PASSes.

**Why:** the engine prints whatever is in the HTML. Recipe JSON is the authoring
contract; overflow/page-count guards do not enforce vertical rhythm.

**How to apply:** when changing spacing, edit the HTML (or `@import` theme geometry)
to match [`docs/LAYOUT-SYSTEM.md`](../docs/LAYOUT-SYSTEM.md). Never shrink equal
margins to fit. Rasterize (`pdf_to_png`) after `check_generation`. Plan:
`Plans/_Active/2026-08-25-remaining-release-and-document-layout.md`.

Related: [[lesson-output-is-repo-root]]
