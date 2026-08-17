# `collages/` — image layouts

One **project folder** per set (`collages/<project>/{images,_candidates,_raw}`).
Run `python -m pdf_tool.collage <imagesDir> --recipe <id> --png`.

| Tracked | Gitignored |
|---|---|
| this README | real image sets, `_candidates/`, `_picker/`, `_raw/`, PNGs |

Do not dump picker galleries at `collages/layouts/` — that name collides with
tracked `layouts/collage/` recipes. Auto-layout PNGs live under the project as
`_picker/` or `_candidates/`.

Legacy alias: `storage/collages/`. Recipes live in tracked `layouts/collage/`. Design: [`docs/COLLAGE-DESIGN.md`](../docs/COLLAGE-DESIGN.md).
