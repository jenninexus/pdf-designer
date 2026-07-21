# ROADMAP — pdf-designer

> **This is a pointer, not the roadmap.** The single active working checklist is
> [`Plans/_Active/2026-07-14-professional-product-roadmap.md`](../Plans/_Active/2026-07-14-professional-product-roadmap.md).
> This file exists so `/jen:roadmap` (which looks for `docs/ROADMAP.md`) resolves to the real plan
> without a second copy that could drift. Plans index: [`Plans/README.md`](../Plans/README.md).

## Remaining (open items)

Pulled from the active plan — keep in sync there, this is a quick view:

- [x] **White-label demo path** — README 5-minute path + `scripts/smoke-white-label.py` ([`WHITE-LABEL.md`](WHITE-LABEL.md))
- [x] **PyPI / wheel spike** — `paths.repo_root` + `share/` sync + `check-wheel-assets.py` ([`PACKAGING.md`](PACKAGING.md)); TestPyPI upload still open
- [x] **Paid-app spike (design)** — shell-over-Hub in [`PRODUCT.md`](PRODUCT.md); next = Hub recipe-gallery UX (not a second renderer)
- [ ] **TestPyPI dry-run** — publish + fresh-venv install after version bump
- [ ] Keep **SSOT + QA docs** honest as the engine evolves ([`SSOT.md`](SSOT.md) · [`QA.md`](QA.md))
- [ ] Optional: document meet-jenni-bot / syn-themes **collage recipes** in [`docs/COLLAGE-DESIGN.md`](COLLAGE-DESIGN.md) examples (paths stay private under `storage/`)
- [ ] Optional: Synagen **engine** promo screenshots → `storage/shade/resources/images/synagen/`
- [ ] Optional: Design Hub **recipe gallery** chrome over `layouts/` + `themes/presets/` (paid-shell precursor)

### Parked

- [ ] **pywebview shell** — parked; shell-over-Hub (browser → Design Hub) is the paid-app plan.
  Revive native window on demand ([archived detail](../Plans/_Archive/2026-07-11-design-hub-parked-phases.md)).

### Never

- Auto-submit applications · cloud-only PII · invent claims.

---

**Shipped** history and the full product thesis / layer breakdown / contracts table live in the active
plan — read it there rather than duplicating here.
