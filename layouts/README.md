# Layouts — reusable structure recipes

**Structure lives here; color lives in [`../themes/`](../themes/).** A *layout* answers
"where does everything sit on the page" (family, canvas, fit, sizing, safety rules). A
*theme* answers "what color is it" (tokens, palettes, gradients). They compose: any
layout renders in any theme.

> **Nothing private lives here.** Real image sets, vaults, and finished exports stay in
> `storage/` (gitignored). This directory is tracked so layouts survive, get reused, and
> ship with a fresh clone — the same way `themes/presets/` does.

| Dir | Owns | Consumed by |
|---|---|---|
| [`collage/`](collage/) | Collage layout recipes — family + canvas + fit + background | `python -m pdf_tool.collage --recipe <id>` · `/make-collage` |
| [`resume/`](resume/) | Document page models — margins, header/footer, page rhythm | [`../docs/LAYOUT-SYSTEM.md`](../docs/LAYOUT-SYSTEM.md) · `/make-resume` |

Machine-readable pointers: [`../.config/mcp-pdf-designer.json#layouts`](../.config/mcp-pdf-designer.json).
Map of every SSOT surface: [`../docs/SSOT.md`](../docs/SSOT.md).

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

The PNGs themselves are per-project output and stay in gitignored `storage/`. To collect a
project's finished picks onto the cross-project shelf:

```bash
python -m pdf_tool.collage <dir> --recipe <id> --png --shelve
```

`--shelve` copies every render to `storage/collages/layouts/`, prefixed `<project>__`, in
one flat directory. The **recipe** is the reusable artifact; the PNG is just a picture of
one project's images.
