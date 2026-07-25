# ROADMAP — pdf-designer

> **This is a pointer, not the roadmap.** The single active working checklist is
> [`Plans/_Active/2026-07-21-next-agent-product-prompt.md`](../Plans/_Active/2026-07-21-next-agent-product-prompt.md).
> This file exists so `/jen:roadmap` (which looks for `docs/ROADMAP.md`) resolves to the real plan
> without a second copy that could drift. Plans index: [`Plans/README.md`](../Plans/README.md).
>
> Prior wave (archived): [`Plans/_Archive/2026-07-14-professional-product-roadmap.md`](../Plans/_Archive/2026-07-14-professional-product-roadmap.md).

## Remaining (open items)

Pulled from the active plan — keep in sync there, this is a quick view:

- [x] **TestPyPI local-wheel dry-run** (2026-07-25) — `scripts/testpypi-dry-run.py` fresh-venv + bundled `share/` + `check_generation` PASS ([`PACKAGING.md`](PACKAGING.md))
- [ ] **TestPyPI upload** — create account/token → `python scripts/testpypi-dry-run.py --upload`
- [ ] Keep **SSOT + QA docs** honest as the engine evolves ([`SSOT.md`](SSOT.md) · [`QA.md`](QA.md))
- [ ] Optional: document meet-jenni-bot / syn-themes **collage recipes** in [`COLLAGE-DESIGN.md`](COLLAGE-DESIGN.md) (paths stay private under `storage/`)
- [ ] Optional: Synagen **engine** promo screenshots → `storage/shade/resources/images/synagen/`

### Recently landed (ops / docs — 2026-07-22…25)

- [x] **Hub vault/recipes responsive chrome** (2026-07-25) — shared `Library | Recipes | Vault` nav; `hub-shell` / `hub-page`; same `991.98`/`1200`/`1400` switches ([`PREVIEWER.md`](PREVIEWER.md) · www-theme-kit `profiles/pdf-designer.json`)
- [x] **Hub recipe-gallery UX** (2026-07-25) — `/recipes` + `GET /api/recipe-gallery` over `layouts/` + `themes/presets/` ([`PREVIEWER.md`](PREVIEWER.md) · [`PRODUCT.md`](PRODUCT.md) shell-over-Hub)

- [x] **Personal palette prefs** — `storage/brand-design/brand-*.json` SSOT + docs chain ([`SSOT.md`](SSOT.md) · [`STORAGE.md`](STORAGE.md) · [`THEME-DESIGN.md`](THEME-DESIGN.md)); MG dark roles lockstep with live site
- [x] **Project wrap** — [`.claude/commands/wrap.md`](../.claude/commands/wrap.md) (`/wrap` · `/jen:wrap`); wrap must refresh agent docs + `dev-log-sego.yaml`
- [x] **BEE clone sync** — `C:\p\pdf-designer` pull via deploy key; private `brand-design/` via SEGO→BEE SMB (`/jen/bee` §11b · `/jen/pdf`)

### Parked

- [ ] **pywebview shell** — parked; shell-over-Hub (browser → Design Hub) is the paid-app plan.
  Revive native window on demand ([archived detail](../Plans/_Archive/2026-07-11-design-hub-parked-phases.md)).

### Never

- Auto-submit applications · cloud-only PII · invent claims.

---

**Shipped** history lives in the archived 2026-07-14 plan — read it there rather than duplicating here.
