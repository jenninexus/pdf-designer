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

## Adding one

Copy the closest existing file, change `id` to match the new filename, and record
`bestFor` honestly — a recipe nobody can tell apart from its neighbour is noise. Delete
recipes that stop earning their place; they are cheap to recreate from a render you liked.
