---
description: Build a multi-image collage from a folder of screenshots or photos — picks a layout recipe, renders candidates at any canvas size (16:9, 9:16, square, print), and serves a picker gallery to compare them. Use for "/make-collage", "make a collage", "combine these screenshots", "put these images together", "collage for Discord/Twitter/a news post", "layout options for these images", or whenever several images need to become one shareable graphic.
argument-hint: <images-dir-or-project> [recipe] [--bg <background>]
---

# /make-collage — Multi-Image Layout Builder

> **Public seed (`*.example.md`).** Copy to bare `make-collage.md` locally if you add personal
> paths or recipes. Bare command files are gitignored — only this `.example` ships on GitHub.

Repo-local command for **pdf-designer**. Real image sets live under `storage/collages/`
(gitignored); **reusable layouts live in tracked [`layouts/collage/`](../../layouts/collage/)**.

## Usage

```
/make-collage storage/collages/<project>/images                          # all families + picker
/make-collage storage/collages/<project>/images scatter-showcase-16x9    # one named recipe
/make-collage storage/collages/<project>/images --bg discord-ember       # override the background
/make-collage <project> --canvas hd-portrait --px 1080x1920              # re-target another size
```

Only the images directory is required. **`python -m pdf_tool.collage --list-recipes`** prints every
layout with what it's best for — run it before inventing flags.

---

## ✅ THE CHECKLIST

- [ ] **1. 🔎 LOOK AT THE IMAGES FIRST — before choosing anything.** Read their real dimensions:
      ```bash
      python -c "import sys; sys.path.insert(0,'src')
      from pdf_tool.collage import scan_images; from pathlib import Path
      for im in scan_images(Path('<images-dir>')):
          print(f\"{im['w']:>5}x{im['h']:<5} ratio {im['w']/im['h']:.2f}  {im['file']}\")"
      ```
      **Image count and shape decide the layout — not taste.** A set with one wide image and three
      tall ones wants a different family than four uniform screenshots. Open a couple and see what
      they actually show; the images often tell a story (same feature on three surfaces, a
      before/after) and that story picks the layout.
- [ ] **2. 🖼 IS IT CONTENT OR IS IT A PHOTO? — this decides `--fit`, and it is the #1 mistake.**
      | Images are… | Use | Why |
      |---|---|---|
      | Screenshots, UI, diagrams, anything with **text** | **`--fit contain`** | Cropping cuts off the very content the collage exists to show |
      | Photos, art, textures | `--fit cover` (default) | Center-crop fills the cell cleanly; nothing is lost |
      **When in doubt on a screenshot set, use `contain`.** A cropped screenshot is a wasted render.
- [ ] **3. Pick a recipe** (`--list-recipes`), or `--layout auto` to generate every family and compare.
      Recipes carry the fit/canvas/background that already worked — prefer one over loose flags.
- [ ] **4. Set the hero if one image leads.** `--hero <filename>`. Hero defaults to the largest by
      resolution, which is often **not** the most important one.
- [ ] **5. Render with `--png`**, then **LOOK AT EVERY PNG YOU PRODUCED.** Read them back. Do not
      report a collage you have not seen — see the failure table below for what to look for.
- [ ] **6. Serve the picker, don't hand over a file path.** The Design Hub serves `storage/`:
      <http://127.0.0.1:8787/storage/collages/<project>/_candidates/index.html>
      A `C:\...` path is **not** a clickable link and fails the task-completion rule.
- [ ] **7. Verify the links resolve** (200) before saying it's ready.
- [ ] **8. 📌 PROMOTE OR ARCHIVE — never leave a good layout as a one-off.**
      ```bash
      # a layout worth reusing → save the settings that made it
      python -m pdf_tool.collage <dir> --layout <family> --fit contain --bg <preset> \
        --promote <id> --best-for "When to reach for this." --png
      # collect this run's renders onto the cross-project shelf
      python -m pdf_tool.collage <dir> --recipe <id> --png --shelve
      # retire one that stopped earning its place (the file survives)
      python -m pdf_tool.collage --archive <id>
      ```
      **Only structure earns a recipe** — family, canvas, or fit. "The same layout in
      orange" is `--bg`, not a new recipe; adding it anyway turns the registry into noise.
      **Never hand-copy files** to promote or shelve — use the flags, or the next project
      won't know the layout exists.

---

## 🔍 Step 5 — WHAT TO LOOK FOR (every one of these shipped as a bug first)

| Symptom | Cause | Fix |
|---|---|---|
| Text sliced off the edge of a cell | `cover` cropping a screenshot | `--fit contain` |
| Visibly **empty cells** in the grid | Image count doesn't divide into the columns | Add/drop an image, or pick a count with an exact divisor (2, 4, 6, 8, 9) |
| A tall image **towering** over the others | Sizing by width instead of area | Fixed in `frame-scatter`; on other families prefer `uniform-grid` |
| An image **buried** under a neighbour | Scatter overlap too aggressive | Narrow tiles auto-stack on top now; reduce the image count if it persists |
| Grey **letterbox slabs** around a screenshot | Frame ratio ≠ image ratio | Fixed in `frame-scatter`; elsewhere it's the `contain` backing (expected) |
| Big empty bands top and bottom | `filmstrip` on a 16:9 canvas | Use `uniform-grid` or `hero-mosaic` |
| Gradient missing in a **PDF** export | Chromium drops backgrounds when printing | Already handled via `print-color-adjust: exact` — don't remove it |

---

## 🎨 Backgrounds and frames — use the palette, never hardcode

Backgrounds are **named presets**, not ad-hoc CSS:
[`themes/default-collage.json#backgrounds`](../../themes/default-collage.json) is the SSOT.

```bash
--bg discord-slate     # Discord grey, the safe default
--bg discord-ember     # warm orange lean
--bg "linear-gradient(...)"   # raw CSS also accepted, passed through verbatim
```

Each background also declares a **`frame`** color, used for the polaroid borders in
`frame-scatter`. **Never hardcode white** — it fights every dark palette. A background with no
declared frame falls back to the theme mode's border color.

> The house palette rule from [`themes/PALETTE-RULES.md`](../../themes/PALETTE-RULES.md)
> (no brown / mustard / lime) applies to collage backgrounds too.

---

## Where things live

```
layouts/collage/<recipe>.json        ⭐ TRACKED — reusable layout recipes
themes/default-collage.json          ⭐ TRACKED — canvas presets, backgrounds, frames
storage/collages/<project>/
  images/                              your source images (+ optional collage-source.json)
  _candidates/                         ⭐ ALL renders — ONE FLAT DIR, no subfolders
storage/collages/layouts/            finished picks across every project, <project>__ prefixed
```

**Output is flat.** Variants never nest into subfolders — canvas, background, and fit are encoded
in the filename (`<family>__<canvas>-<W>x<H>[__<bg>][__contain].png`), so nothing collides and
everything for a project sits in one place.

**Reusable layouts do NOT belong in `storage/`.** `storage/` is private content (real images,
finished exports). A layout you'd use again is tracked in `layouts/collage/` so it survives, is
discoverable, and ships with a clone.

---

## Contracts (do not break)

- **Never crop content.** Screenshots, UI, and diagrams render with `contain`. Always.
- **One flat output dir per project.** No per-canvas or per-background subfolders.
- **Promote with `--promote`, shelve with `--shelve`, retire with `--archive`.** Copying
  files by hand is how a reusable layout becomes a one-off nobody finds again.
- **Serve, don't hand over a path.** Observable = an `http://127.0.0.1:8787/...` link.
- **Look at what you rendered** before reporting it. Every failure in the table above was
  shipped once by not looking.
- **Privacy:** `storage/` is gitignored. Real images never move into tracked paths.

## Related

[`docs/COLLAGE-DESIGN.md`](../../docs/COLLAGE-DESIGN.md) — layout families, canvas presets, backgrounds, fit ·
[`layouts/README.md`](../../layouts/README.md) — recipe schema + how to add one ·
[`themes/PALETTE-RULES.md`](../../themes/PALETTE-RULES.md) — color guard ·
[`docs/PREVIEWER.md`](../../docs/PREVIEWER.md) — Design Hub ·
[`docs/SSOT.md`](../../docs/SSOT.md) — full surface map ·
[`.claude/commands/make-resume.example.md`](make-resume.example.md) — the sibling document routine
