# Archived recipes

Retired layouts. They no longer appear in `--list-recipes` and can't be rendered by name,
but the files survive here so a layout is never lost to a snap judgment.

```bash
python -m pdf_tool.collage --archive <id>              # retire (moves the file here)
mv _archive/<id>.json ..                               # un-retire
```

## What gets archived

A recipe earns its place by being **distinguishable**. Archive it when:

- **It's the same layout in a different color.** Backgrounds compose at render time
  (`--bg <preset>`), so a recipe differing only by background is noise. This is the most
  common reason — `scatter-ember-16x9` was archived for exactly this: identical family,
  canvas, and fit to `scatter-showcase-16x9`, differing only by `discord-ember`.
- Nobody could tell from `bestFor` when to pick it over its neighbour.
- The layout it captures stopped producing good results.

Keep a recipe when it differs in **family, canvas, or fit** — those are structural and
can't be recovered from a flag at render time.
