# ROADMAP — pdf-designer

> **This is a pointer, not the roadmap.** The single active working checklist is
> [`Plans/_Active/2026-08-12-product-privacy-packaging.md`](../Plans/_Active/2026-08-12-product-privacy-packaging.md)
> (+ run [`…/2026-08-12-public-private-split/Plan.md`](../Plans/_Active/2026-08-12-public-private-split/Plan.md)).
> This file exists so `/jen:roadmap` (which looks for `docs/ROADMAP.md`) resolves to the real plan
> without a second copy that could drift. Plans index: [`Plans/README.md`](../Plans/README.md).
>
> Completed waves: [`Plans/_Complete/`](../Plans/_Complete/) (includes hub layouts 2026-08-10 and
> product prompt 2026-07-21).

## Remaining (open items)

Pulled from the active plan — keep in sync there, this is a quick view:

- [ ] **History scrub** — `storage/docs/HISTORY-SCRUB.md` then human-authorized force-push
- [ ] **TestPyPI upload** — create account/token → `python scripts/testpypi-dry-run.py --upload`
- [ ] **Push origin/main** — use `jenninexus` GitHub auth (MonoFinity `gh` cannot see the private repo)
- [ ] Keep **SSOT + QA docs** honest as the engine evolves ([`SSOT.md`](SSOT.md) · [`QA.md`](QA.md))
- [ ] Optional: production PyPI after TestPyPI · paid-shell
- [ ] Optional: document meet-jenni-bot / syn-themes **collage recipes** in [`COLLAGE-DESIGN.md`](COLLAGE-DESIGN.md)
- [ ] Optional: Synagen **engine** promo screenshots → `storage/shade/resources/images/synagen/`

### Recently landed

- [x] **Public vs local architecture** (2026-08-12) — `PUBLIC-LOCAL-SPLIT` · `GETTING-STARTED` · tracked `storage/docs/README` · siblings + theme-kit pointers
- [x] **Clone-safe Resume Studio walkthrough** (2026-08-12) — tracked vault → profile → palette → HTML → QA/export/ATS path + direct Hub example link
- [x] **Codex/public-command reconciliation** (2026-08-12) — generated local adapters; anonymized public résumé seed; public smoke + wheel artifact gates green
- [x] **Commands privacy** (2026-08-12) — GitHub = `*.example.md` only; wrap requires `/reflect` + handoff
- [x] **Resume Studio product frame** — `examples/resume-studio/` + job-market pitch in PRODUCT
- [x] **Privacy packaging** (2026-08-12) — untrack local MCP config; `storage/docs/`; public command seeds
- [x] **Hub drawer / icons / letterhead / split restore** (2026-08-10.11)
- [x] **TestPyPI local-wheel dry-run** (2026-07-25)
- [x] **Hub vault/recipes + recipe-gallery UX** (2026-07-25)

### Parked

- [ ] **pywebview shell** — parked ([`Plans/_Complete/2026-07-11-design-hub-parked-phases.md`](../Plans/_Complete/2026-07-11-design-hub-parked-phases.md))

### Never

- Auto-submit applications · invent claims · fork the renderer · commit `storage/` · reopen Netflix
- Force-push history rewrite without explicit human OK + jenninexus auth
