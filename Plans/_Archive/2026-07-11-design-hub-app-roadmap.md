# Roadmap (ARCHIVED 2026-07-14)

> **Superseded by** [`../_Active/2026-07-14-professional-product-roadmap.md`](../_Active/2026-07-14-professional-product-roadmap.md).
> Phase 1 Design Hub shipped; remaining pipeline items live on the active product roadmap.
> Parked pywebview/canvas: [`2026-07-11-design-hub-parked-phases.md`](2026-07-11-design-hub-parked-phases.md).

---

Design SSOT: [`../../docs/PREVIEWER.md`](../../docs/PREVIEWER.md). Protocol SSOT:
[`../../docs/STORAGE.md`](../../docs/STORAGE.md) · [`../../docs/VAULT.md`](../../docs/VAULT.md) ·
[`../../docs/JOB-ASSESSMENT.md`](../../docs/JOB-ASSESSMENT.md).

This file is the working checklist — check items off as they land.

---

## Where this stands

**Phase 1 shipped.** Phases 2–5 as originally written are **unbuilt and de-prioritized** —
verified against the source (no `--variants`, no `pdf_tool/app.py`, no canvas drag-and-drop, no
multi-page collage book).

**2026-07-14 housekeeping done**

- [x] Protocol docs moved to tracked `docs/` (`STORAGE`, `VAULT`, `JOB-ASSESSMENT`); `storage/` keeps stubs + private data only
- [x] Brand color SSOT = one file each under `storage/brands/`; `users/*.json` only pointers
- [x] Previewer reads `storage/brands/` (not the never-existed `storage/themes/`)
- [x] React-vs-pywebview conflict already resolved in `THEME-DESIGN.md`

**Why the re-prioritization.** The résumé pipeline is the product. Collage app work stays parked.

| | Built | Used |
|---|---|---|
| **Résumé / application pipeline** | vault, profiles, guards, `/make-resume` | active (both applicants) |
| **Collage** | CLI + candidates gallery | rare |

---

## ✅ Phase 1 — local previewer (2026-07-11 · hub UX 2026-07-14)

- [x] `src/pdf_tool.preview` — Design Hub (thumbnails, palette swapper, export)
- [x] `css_vars` injection — palette-swapped exports are WYSIWYG
- [x] Verified against real résumé + collage candidates
- [x] **Hub chrome tokens** — `static/hub.css` (dashboard-token lineage); www profile `pdf-designer.json`
- [x] **Library filters** — kind · folder · person · search (Jobright-style; each HTML = one template)
- [x] **Compact toolbar** — single ~44px bar (Syqo/Synagen density); output path under ⋯ menu

## ✅ Guards (2026-07-13)

- [x] `check_palette` wired into `html_to_pdf`
- [x] `check_vault` — claim schema + track existence
- [x] `doNotClaim` verification ledger

---

## Next — the résumé pipeline

### 🔜 A. Wire `check_vault` into `/make-resume`
- [ ] Auto-run at top of `/make-resume`
- [ ] `--explain <track>` — print ranked claims for a track

### 🔜 B. `--variants` (original Phase 2)
- [ ] N palette variants → `_variants/` for side-by-side hub shopping

### 🔜 C. Close the ATS loop
- [ ] `pdf_tool.check_ats <resume.pdf>` — show the text layer a parser sees

### 🔜 D. Vault ergonomics
- [ ] `check_vault --coverage <listing.md>` — mechanical gap-check

---

## Parked — app shell (Phases 3–5)

Not cancelled. Detail archived for history: see
[`../_Archive/2026-07-11-design-hub-parked-phases.md`](../_Archive/2026-07-11-design-hub-parked-phases.md).

- Phase 3: pywebview window around the preview server — polish only
- Phases 4–5: canvas editor & collage books — blocked on demand

---

## Still worth doing (cheap)

- [ ] Reconcile canvas-preset tables across README / COLLAGE-DESIGN / PREVIEWER
- [ ] Decide license on purpose (MIT vs `LICENSING-NOTES.md`)
- [ ] Minimal tests for `check_palette.classify()` + vault ranking

## Does this need MCP / always-on localhost?

**No.** Best path = offline CLI. Design Hub is optional: `python -m pdf_tool.preview` →
`http://127.0.0.1:8787` (temporary process). No MCP server required.
