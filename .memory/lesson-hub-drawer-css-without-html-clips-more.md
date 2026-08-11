---
name: hub-drawer-css-without-html-clips-more
description: Design Hub drawer CSS shipped without HTML/JS; hub-more popover was clipped by overflow:hidden
metadata:
  type: project
---

# Hub drawer CSS without HTML · ⋯ panel clipped

## Trap

`hub.css` documented a full offcanvas drawer + search overlay (commit `2b75b79`), and the
toolbar had a `⋯` `<details class="hub-more">` for the export output folder — but:

1. **No matching HTML/JS ever landed in `preview.py`**, so ≤767.98px filters vanished with
   nowhere to go.
2. `.hub-bar { overflow: hidden }` + `.hub-bar-scroll { overflow-y: hidden }` **clipped** the
   absolute `hub-more-panel`, so the ⋯ control looked inert.

Separately, moving document recipes into `layouts/{cover-letter,letter,resume,work-examples}/`
without updating `recipe_gallery._resume_layouts` made `/recipes` report **0** document layouts.

## Guard

- Wire drawer + search overlay markup/JS in the same change as the CSS contract.
- Keep `hub-more` in `.hub-bar-pin` with `overflow: visible` on the bar/pin.
- `recipe_gallery` must scan category folders (not only top-level `layouts/*.json`).
- Exclude `build/` / `dist` / `*.egg-info` from the Design Hub library scan.

## See also

- [[lesson-fixed-height-clips-content-silently]] — another "invisible clip" class of bug
- `docs/PREVIEWER.md` · `www-theme-kit/profiles/pdf-designer.json`
