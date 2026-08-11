# Active plan — Hub fix · layout categories · personal letterhead

**Date:** 2026-08-10 · **Host:** SEGOPC  
**Supersedes working queue from:** [`2026-07-21-next-agent-product-prompt.md`](2026-07-21-next-agent-product-prompt.md) (incomplete leftovers folded below).  
**Completed prior plans:** moved to [`../_Complete/`](../_Complete/) (renamed from `_Archive`).

---

## Session checklist

- [x] **Hub previewer fix** — wire missing drawer HTML/JS; unclip `⋯` output-folder popover (`overflow:hidden` on `.hub-bar`); exclude `build/` from library scan
- [x] **Icon-only toolbar** — Export = FA download; Refresh = FA arrows-rotate; More = FA ellipsis (inline SVG from Font Awesome Free 6.7.2, offline)
- [x] **Responsive audit** — drawer holds nav/chips/selects/`outdir` ≤767.98px; pin keeps refresh + export; search overlay/magnifier
- [x] **Layouts category tree** — `cover-letter/` · `letter/` · `resume/` · `work-examples/` (+ `collage/`); update all docs/commands/kit refs
- [x] **Personal letterhead** — `layouts/letter/personal-letter.json` + example HTML (date top-right, Dear…, Parisienne sign-off, soft footer)
- [x] **recipe_gallery** — scan nested document recipes (not flat `layouts/*.json`)
- [x] **www-theme-kit** — refresh `profiles/pdf-designer.json` · `profiles/resume.json` · `palettes/resume-palettes.json` pointers to new layout paths
- [x] **Commands** — `.claude/commands` + `/jen/wrap` handoff includes `/jen:reflect` section
- [ ] **Milestone wrap** — commit + `/wrap` when hub+layouts land

### Folded from prior active plan (still open)

- [ ] **TestPyPI upload** — needs `TESTPYPI_TOKEN` then `python scripts/testpypi-dry-run.py --upload`
- [ ] Keep **SSOT + QA docs** honest as the engine evolves
- [ ] Optional: document meet-jenni-bot / syn-themes collage recipes in `docs/COLLAGE-DESIGN.md`
- [ ] Optional: Synagen engine promo screenshots → `storage/shade/resources/images/synagen/`
- [ ] **pywebview shell** — parked ([`../_Complete/2026-07-11-design-hub-parked-phases.md`](../_Complete/2026-07-11-design-hub-parked-phases.md))

### Never

- Auto-submit applications · cloud-only PII · invent claims · fork the renderer · reopen Netflix

---

## Diagnosis (2026-08-10)

| Symptom | Root cause |
|---|---|
| `⋯` looks dead | Panel is `position:absolute` under `.hub-bar` / `.hub-bar-scroll` with `overflow:hidden` — open state is clipped |
| Narrow widths lose filters | `hub.css` drawer contract shipped in `2b75b79`; **HTML/JS never landed** in `preview.py` |
| `/recipes` document count = 0 | Layouts moved into category folders; `recipe_gallery._resume_layouts` still globs top-level `layouts/*.json` only |

Observable: [http://127.0.0.1:8787/](http://127.0.0.1:8787/) · [http://127.0.0.1:8787/recipes](http://127.0.0.1:8787/recipes)
