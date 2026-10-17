# `collages/` — image layouts (source)

One **project folder** per set (`collages/<project>/{images,_candidates,_raw,faves}`).
Run `python -m pdf_tool.collage <imagesDir> --recipe <id> --png`.

**Finished renders land at the collage project root** — `collages/<project>/` — beside the project that
produced them, which is what the Design Hub shows as an Export. Working material stays in the project's
subfolders (`_candidates/`, `_picker/`, `_raw/`), and `_exports/` is the **fallback only**, for a source
the engine cannot match to a project (a public example, or an unfiled source).

`output/` is **not** the destination for a collage: it is explicit, disposable automation/test scratch
(and is not scanned by the Hub). See [`docs/STORAGE.md`](../docs/STORAGE.md) § Which folder is which.

| Tracked | Gitignored |
|---|---|
| this README | real image sets, `_candidates/`, `_picker/`, `_raw/`, finished PDFs/PNGs |

Keep picker galleries **with the project** (`_picker/` / `_candidates/`) so the
Design Hub can still scan them. Do not dump finished renders at
`collages/layouts/` — that name collides with tracked `layouts/collage/` recipes.

**Legacy alias:** `storage/collages/` still *resolves* (the dual-run map in `src/pdf_tool/paths.py` keeps
old Hub URLs working) but it is no longer a live location — the retired `storage/` tree holds only
`_archive/` plus two items that are still referenced (`screenshots/`, and the vid-scroll project config).

Recipes live in tracked `layouts/collage/`. Design: [`docs/COLLAGE-DESIGN.md`](../docs/COLLAGE-DESIGN.md).
