# `collages/` — image layouts (source)

One **project folder** per set (`collages/<project>/{images,_candidates,_raw,faves}`).
Run `python -m pdf_tool.collage <imagesDir> --recipe <id> --png`.

Working candidates stay beside the source project under `_candidates/`. Personal finished picks go to
**[`_exports/<user>/collages/<project>/`](../_exports/README.md)** when a personal command supplies
`--out`; public/example engine runs use [`output/collages/<project>/`](../output/README.md).

| Tracked | Gitignored |
|---|---|
| this README | real image sets, `_candidates/`, `_picker/`, `_raw/`, working PNGs |

Keep picker galleries **with the project** (`_picker/` / `_candidates/`) so the
Design Hub can still scan them. Do not dump finished renders at
`collages/layouts/` — that name collides with tracked `layouts/collage/` recipes.

Legacy alias: `storage/collages/`. Recipes live in tracked `layouts/collage/`.
Design: [`docs/COLLAGE-DESIGN.md`](../docs/COLLAGE-DESIGN.md).
