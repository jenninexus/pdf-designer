# Collage Design — Multi-Image Layout Generator

pdf-designer's second document type after resumes: give it a **directory of
images** and get back a set of **collage layout options** to compare and pick
from — the same experience as dropping photos into PowerPoint and having it
offer a handful of arrangement candidates.

Consumers:
- Print / PDF / social collage pages (this repo)
- Live web: Martian Games `/news/{slug}` collage CSS mirrors these family names
  (`filmstrip`, `hero-mosaic`, …) — see `mg/storage/docs/NEWS.md` → Collage layouts.
  Optional `collage_image:` on a news post accepts a `--png` export from this tool.

Status: **v1 built** — `src/pdf_tool/collage.py` implements all six layout
families, the candidates output, the `index.html` picker gallery, and `--png`
rendering. This doc remains the design SSOT; the example profile lives at
[`../examples/profiles/default-collage/`](../examples/profiles/default-collage/).
Canvas presets below are mirrored in the root
[`README.md`](../README.md#-canvas-sizes) and defined in
[`themes/default-collage.json`](../themes/default-collage.json).

## The feature in one flow

1. Point the tool at a directory of images (typically under
   `storage/collages/<project>/images/`).
2. It reads each image's dimensions/orientation and generates **several
   candidate layouts** (different layout families, see below) as HTML pages.
3. You open the candidates side by side (or render them all to PNG contact
   sheets), pick one, and optionally add text blocks (title, captions).
4. Export the chosen layout to PDF (print) or PNG (social) at any of the
   canvas presets.

Like everything in this repo: deterministic HTML/CSS rendered through the
same `html_to_pdf.py` / `pdf_to_png.py` pipeline — no new render engine.

## Default canvas sizes

| Preset id | Ratio | Pixels | Use |
|---|---|---|---|
| `letter-portrait` | 8.5 × 11 in | 2550 × 3300 @300dpi | Print page, PDF one-sheet |
| `letter-landscape` | 11 × 8.5 in | 3300 × 2550 @300dpi | Print landscape |
| `hd-landscape` | 16:9 | 1920 × 1080 (or 1280 × 720) | YouTube thumbnail, slides, banners |
| `hd-portrait` | 9:16 | 1080 × 1920 (or 720 × 1280) | Stories, Reels, TikTok, Shorts |
| `standard-landscape` | 4:3 | 1440 × 1080 | Classic photo layout |
| `standard-portrait` | 3:4 | 1080 × 1440 | Portrait photo layout |
| `ig-portrait` | 4:5 | 1080 × 1350 | Instagram portrait post (their max-height feed size) |
| `square` | 1:1 | 1024 × 1024 (or 1000 × 1000, 512 × 512) | Instagram square, avatars, thumbnails |

Print presets are physical (inches + `@page`); social presets are pixel
canvases rendered 1:1 via PNG export. One collage layout should be able to
re-target another preset — the layout adapts, the image set stays.

## Layout families (the "PowerPoint options" study)

PowerPoint's Designer offers a handful of *layout families* per image count
rather than one grid. We mirror that. Each family is a deterministic
algorithm parameterized by image count, image orientations, and canvas ratio:

### 1. Uniform grid
Equal cells, R×C chosen from the image count and canvas ratio
(e.g. 12 images on Letter portrait → 3×4; on 16:9 → 4×3). Images
center-cropped to the cell (`object-fit: cover`). The safe default for any
count. Best for consistent same-subject sets.

### 2. Hero mosaic (featured + supporting)
One image gets a large cell (~40–60% of canvas), the rest tile around it.
PowerPoint leans on this heavily — it reads as *designed* instead of
*gridded*. Variants: hero top-left / hero centered / hero full-bleed with a
strip. Pick the hero by largest resolution, or explicitly in the source file.

### 3. Masonry / packed columns
Columns of equal width, images keep their native aspect ratio and stack to
balanced column heights. No cropping — best for mixed portrait/landscape
sets where cropping would hurt.

### 4. Filmstrip / rows
1–3 full-width rows, each row's images scaled to a common height (justified
layout, like Google Photos). Great on landscape canvases and for
chronological sequences.

### 5. Spotlight + caption (image/text mix)
A layout that reserves a text region: title block, caption list, or one text
card occupying a grid cell. This is the "sometimes images/text" requirement —
text blocks are first-class cells, declared in the collage source file, not
overlaid ad hoc.

### 6. Frame scatter (polaroid)
Slight rotations, borders, and overlaps on a background color/texture.
Decorative option for personal/scrapbook use; off by default for
professional documents.

### Capacity guidance (Letter portrait)

| Images | Recommended families |
|---|---|
| 2–4 | Hero mosaic, filmstrip |
| 5–8 | Hero mosaic, uniform grid (2×3/2×4), masonry |
| 9–12 | Uniform grid (3×3/3×4), hero mosaic with 3×3 support tiles |
| 13–15 | Uniform grid (3×5/4×4 with one spanning cell), masonry — beyond ~15 per page, split pages |

Rules of thumb baked into every family:
- Consistent gutters (one gap token, default 8–16px screen / 0.08–0.12in print).
- Center-crop, never stretch; masonry when cropping is unacceptable.
- Respect orientation: portrait images prefer tall cells, landscape wide
  cells — the generator scores candidate cell assignments by fit.
- Optional page background from theme tokens (dark full-color or light print,
  same dual-mode contract as resumes) — see [Page backgrounds](#page-backgrounds)
  for the gradient presets.

## Page backgrounds

A collage does not have to sit on flat white or flat dark. `--bg` sets the page
background to a **named gradient preset** or any raw CSS color/gradient string,
which is passed through verbatim.

Presets are defined in
[`themes/default-collage.json#backgrounds`](../themes/default-collage.json) (the
SSOT; `collage.py` carries a matching fallback table). The Discord family is
sampled from the real client chrome — chat `#313338`, sidebar `#2b2d31`, embed
card `#1e1f22`, shell `#111214` — with the Martian orange `#f0561d` and embed
link blue `#00a8fc` as accents:

| Preset | Look |
|---|---|
| `discord-slate` | Default Discord grey, diagonal — safest choice |
| `discord-deep` | Darker vertical fade; keeps bright screenshots dominant |
| `discord-radial` | Center-top glow; suits hero-mosaic and spotlight |
| `discord-ember` | Grey warming into the Martian orange |
| `discord-signal` | Grey cooling into the embed link blue |
| `martian-ember` | Strongest brand lean |
| `flat-dark` / `flat-white` | The pre-gradient flat defaults |

```bash
python -m pdf_tool.collage <dir> --bg discord-slate
python -m pdf_tool.collage <dir> --bg "linear-gradient(180deg,#2b2d31,#111214)"
```

The gradient is painted on `.canvas` so it spans the page **once** rather than
repeating per cell, and print CSS sets `print-color-adjust: exact` so Chromium
keeps it when exporting to PDF (without it, gradients silently drop).

## Fit: cover vs contain

`--fit` controls how an image fills its cell:

- **`cover` (default)** — center-crop to fill. Right for photos.
- **`contain`** — fit the whole image, letterboxed. **Required for screenshots,
  diagrams, and UI captures**, where a crop cuts off content. When contain is
  active, cells get a subtle translucent backing so the gradient shows through
  the letterbox area instead of a flat block.

A tall screenshot in a wide 16:9 cell loses most of its text under `cover` —
reach for `contain` whenever the images carry readable content.

## Profile + theme structure (same contract as resumes)

```text
themes/default-collage.json        canvas presets + gutter/background/caption tokens
examples/profiles/default-collage/
  profile.json                     which theme/canvas/layout the profile uses
  default-collage.html             reference render (hero mosaic, 6 images, Letter)
  collage-source.example.json      the input schema: image list + text blocks + options
storage/collages/<project>/        your real image sets + generated candidates (gitignored)
```

`collage-source.json` schema (see the example file for a filled version):

- `imagesDir` — directory to scan, or an explicit `images: []` list
- `canvas` — a preset id from the table above (or explicit `{width, height, unit}`)
- `layout` — a family id, or `"auto"` to generate one candidate per family
- `hero` — optional filename to force as the featured image
- `text` — optional array of `{type: "title"|"caption"|"card", content, cell}`
- `theme` — `dark` (default full-color) or `light` (print counterpart)
- `background` — a preset id from [Page backgrounds](#page-backgrounds), or a
  raw CSS color/gradient string
- `fit` — `cover` (default, center-crop) or `contain` (fit whole image; use for
  screenshots) — see [Fit: cover vs contain](#fit-cover-vs-contain)

## The module

`src/pdf_tool/collage.py`:

```text
python -m pdf_tool.collage <imagesDir>                                      # all 6 candidates + picker
python -m pdf_tool.collage <imagesDir> --canvas square --layout hero-mosaic # one family, one canvas
python -m pdf_tool.collage <imagesDir> --canvas hd-landscape --px 1280x720 --png   # 16:9 at 720p
python -m pdf_tool.collage <imagesDir> --hero best.png --title "Showcase" --theme dark --png
```

- Default (`--layout auto`) writes one candidate HTML per family into
  **`<imagesDir>/_candidates/<canvas>-<W>x<H>/`** plus **`index.html` — the
  PowerPoint-Designer-style picker**: every candidate side by side as live
  scaled previews; click one to open it full size. Each canvas size gets its
  own subfolder, so a new size/ratio run never overwrites earlier candidates.
- `--px WIDTHxHEIGHT` overrides a preset's pixel size (e.g. `hd-landscape`
  at 1280×720 instead of the default 1920×1080).
- `--png` also screenshots each candidate at the canvas pixel size (that's how
  social-format exports work; print canvases export via `html_to_pdf.py`).
- If `<imagesDir>/collage-source.json` exists, its `canvas`/`layout`/`hero`/
  `text`/`theme` become the defaults; CLI flags win.
- Deterministic: images sorted by name, hero = largest image unless overridden,
  frame-scatter jitter hashed from filenames — same inputs, same layouts.
- Combining with other documents stays trivial: a collage page is just
  another HTML → PDF page, so `merge_pdfs.py` can append a photo-collage
  page to a resume or portfolio bundle.

## Non-goals

- No image editing (crop/rotate beyond CSS `object-fit`, no filters).
- No cloud upload; images never leave the machine.
- No AI-generated captions — text comes from the source file.
