# Layouts — reusable structure recipes

**Structure lives here; color lives in [`../themes/`](../themes/).** A *layout* answers
"where does everything sit on the page" (family, canvas, fit, sizing, safety rules). A
*theme* answers "what color is it" (tokens, palettes, gradients). They compose: any
layout renders in any theme.

The reusable recipes here ship with a fresh clone. For a shared workspace customization, copy
[`application-packet.example.json`](application-packet.example.json) to the ignored
`layouts/application-packet.json`, then point the profiles that should use it at that copy.
Keep each person's preferences in their [render profile](../profiles/README.md).

| Path | Owns | Consumed by |
|---|---|---|
| [`cover-letter/`](cover-letter/) | Professional cover letters (1 page, bottom-LEFT sign-off) | `/make-cover-letter` · LAYOUT-SYSTEM |
| [`letter/`](letter/) | Personal letterhead (date top-right, optional cursive sign-off) | personal notes |
| [`resume/`](resume/) | Résumé page model (2 pages, bottom-RIGHT signature) | `/make-resume` |
| [`work-examples/`](work-examples/) | Work-samples / Additional Documents (3 pages) | `/make-work-examples` |
| [`collage/`](collage/) | Collage layout recipes — family + canvas + fit + background | `python -m pdf_tool.collage --recipe <id>` · `/make-collage` |

Machine-readable pointers: [project config seed](../.config/mcp-pdf-designer.example.json).
Map of every SSOT surface: [`../docs/SSOT.md`](../docs/SSOT.md).

> **Path note (2026-08-10):** document recipes live in **category folders**
> (`cover-letter` · `letter` · `resume` · `work-examples`). Older flat
> `layouts/*.json` and the brief `layouts/`-only note (2026-08-08) are retired.

---

## Document page models — start here

**Protocol (every `/make-resume` · `/make-cover-letter` · `/make-work-examples` · personal letter):**

| Doc | Open this recipe | Signature | Pages |
|---|---|---|---|
| **Cover letter** | [`cover-letter/one-page-letter.json`](cover-letter/one-page-letter.json) ⭐ | **Bottom-LEFT**, flex-pinned (`margin-top: auto`, `padding-top: 30px`). Print = `min-height` only — **never** fixed `height` + `overflow: hidden` | **1** |
| **Personal letter** | [`letter/personal-letter.json`](letter/personal-letter.json) | Date **top-RIGHT**; closing + optional cursive first name **bottom-LEFT**; soft footer | **1** |
| **Résumé** | [`resume/two-page-standard.json`](resume/two-page-standard.json) | **Bottom-RIGHT**, flex-pinned. Print = fixed `height` + `overflow: hidden` | **2** |
| **Work samples** | [`work-examples/work-examples.json`](work-examples/work-examples.json) | Footer row (name L / links R). Portfolio URLs in a **body** section — not an extra footer line | **3** |

Full narrative + bands: [`../docs/LAYOUT-SYSTEM.md`](../docs/LAYOUT-SYSTEM.md).  
Use the visible rhythm as a starting point: roughly 20px between major sections and 14px between
consecutive roles or subsections, checked in both PDF themes. Fit content without shrinking the
equal page margins. Game-art thumbnails may cover their frame if the subject survives the crop;
screenshots whose complete content matters use contain. See the work-samples recipe for the
print-safe glass-like card treatment.
See the [cover-letter example](../examples/profiles/default-cover-letter/default-cover-letter.html)
for sign-off placement and padding and the [personal-letter example](../examples/profiles/default-letter/personal-letter.html)
for personal letterhead.

| Recipe | Doc types | Page model |
|---|---|---|
| [`resume/two-page-standard.json`](resume/two-page-standard.json) | résumé | Flex column · fixed print `height` + `overflow: hidden` · signature **bottom-RIGHT** |
| [`work-examples/work-examples.json`](work-examples/work-examples.json) | work-samples / Additional Documents | Flex column · fixed print `height` · signature bottom-right · **full-row** stats/link grids |
| [`cover-letter/one-page-letter.json`](cover-letter/one-page-letter.json) ⭐ | **cover letter** | Flex column · print `min-height` · sign-off **bottom-LEFT** |
| [`letter/personal-letter.json`](letter/personal-letter.json) | family / friend letter | Letterhead · date top-RIGHT · optional cursive closing · soft footer · letter print model |

> ### ⛔ Never put the résumé's *print* model on a cover letter or personal letter
>
> Both letter types use flex + `margin-top: auto` to pin the sign-off. The difference is **print geometry**:
>
> | | Résumé / samples | Cover / personal letter (CZI-safe) |
> |---|---|---|
> | Print `.page` | fixed `height` + `overflow: hidden` | `height: auto` · `min-height` · **no** `overflow: hidden` |
> | Why | Fixed page count must hold the bottom edge | `@page { margin }` already insets; a near-full fixed height + clip **slices the sign-off** |
>
> **Enforced** by `check_generation` → `letter-geometry`.
>
> **If a letter runs long:** cut prose → tighten close → font steps → line-height → margin 0.75→0.8in.
> **Never** restore fixed height. Bands: [`cover-letter/one-page-letter.json#fitToOnePage`](cover-letter/one-page-letter.json).

---

## Collage recipes

A recipe is a named, versioned bundle of the flags you'd otherwise retype. Instead of

```bash
python -m pdf_tool.collage <dir> --canvas hd-landscape --px 1920x1080 \
  --layout frame-scatter --fit contain --bg discord-slate
```

you name the intent:

```bash
python -m pdf_tool.collage <dir> --recipe scatter-showcase-16x9
```

Recipe fields (all optional except `id`, `family`, `canvas`):

| Field | Meaning |
|---|---|
| `id` | Recipe name used on the CLI (matches the filename stem) |
| `family` | A layout family from [`../docs/COLLAGE-DESIGN.md`](../docs/COLLAGE-DESIGN.md) |
| `canvas` / `px` | Canvas preset id, plus an optional explicit pixel size |
| `fit` | `cover` (crop to fill, for photos) or `contain` (whole image, for screenshots) |
| `background` | A preset id from `themes/default-collage.json#backgrounds`, or raw CSS |
| `bestFor` / `notes` | Human guidance — when to reach for this one |

CLI flags always win over the recipe, so a recipe is a starting point, never a cage.

## The lifecycle — promote, reuse, archive

**Never hand-copy a layout you liked.** Save it from the render that produced it:

```bash
# 1. Render something you like
python -m pdf_tool.collage <dir> --layout frame-scatter --fit contain --bg discord-slate --png

# 2. Promote those exact settings into a reusable recipe
python -m pdf_tool.collage <dir> --layout frame-scatter --fit contain --bg discord-slate \
  --promote my-layout-16x9 --best-for "When to reach for this." --png

# 3. Any future project just names it
python -m pdf_tool.collage <other-project>/images --recipe my-layout-16x9 --png

# 4. Retire it when it stops earning its place (the file survives)
python -m pdf_tool.collage --archive my-layout-16x9
```

`--promote` validates **before** rendering (needs one `--layout`, not `auto`; refuses to
overwrite an existing name) and writes the recipe **after** a successful render — so a
saved recipe is always a combination that actually worked. It omits `px` when the size is
just the canvas preset's default, keeping recipes minimal.

### What earns a recipe

A recipe must be **distinguishable by structure** — family, canvas, or fit. Those can't be
recovered from a flag later.

> **Color is not structure.** Backgrounds compose at render time (`--bg <preset>`), so
> "the same layout in orange" is a flag, not a recipe. Adding one anyway is how a registry
> turns into noise — see [`collage/_archive/README.md`](collage/_archive/README.md).

Archiving is preferred over deleting: retired recipes leave `--list-recipes` but stay on
disk in `collage/_archive/`, so nothing is lost to a snap judgment.

### Finished renders (not recipes)

The PNGs themselves are per-project output and stay in the gitignored collage project. To collect a
project's finished picks onto the project's own shelf:

```bash
python -m pdf_tool.collage <dir> --recipe <id> --png --shelve
```

`--shelve` copies every render to the collage project root, `collages/<project>/`, prefixed
`<project>__`, in one flat directory (falls back to `_exports/<profile>/collages/` when the source
can't be matched to a project). The **recipe** is the reusable artifact; the PNG is just a picture of
one project's images.

## Application packets

The [example packet recipe](application-packet.example.json) defines the part order, Letter
geometry and applicant-first hierarchy. It allows up to one cover-letter page, two résumé
pages and two work-example pages. The cover letter is optional and goes first when included.
A finished packet has at most five pages in each requested print theme.

Resolve values in this order: the request for the current document, the selected profile's
`layoutPrefs`, then the selected packet or document recipe. Use heading case as written when
the profile has no preference. Keep names and project titles in their official casing in
body text and use the profile's case for headings. Use the actual rendered page counts to
check the individual caps and the combined cap. Edit the content to fit the available space
within the standard equal margins.
