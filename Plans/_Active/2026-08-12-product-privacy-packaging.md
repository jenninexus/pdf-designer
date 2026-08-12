# Active plan — Product privacy · packaging · marketing

**Date:** 2026-08-12 · **Host:** SEGOPC  
**Prior hub wave (complete):** [`../_Complete/2026-08-10-hub-layouts-letterhead.md`](../_Complete/2026-08-10-hub-layouts-letterhead.md)  
**Prior product wave (complete):** [`../_Complete/2026-07-21-next-agent-product-prompt.md`](../_Complete/2026-07-21-next-agent-product-prompt.md)

---

## Session checklist (2026-08-12)

- [x] Confirm `storage/` never tracked (gitignore + `git ls-files` empty)
- [x] Untrack `.config/mcp-pdf-designer.json` — keep `.example.json` only on GitHub
- [x] Archive completed Plans (`07-21`, `08-10`) → `_Complete/`
- [x] Add private `storage/docs/` index (dev-only / personal workspace notes)
- [x] Refresh public PRODUCT / WHITE-LABEL / STORAGE / docs README / ROADMAP
- [x] Public seeds: `make-cover-letter.example.md` · `make-work-examples.example.md`
- [x] Durable lesson: Hub Collages + Profiles filter hides untagged projects
- [ ] **TestPyPI upload** — needs `TESTPYPI_TOKEN` → `python scripts/testpypi-dry-run.py --upload`
- [ ] Optional: PyPI production after TestPyPI succeeds
- [ ] Optional: paid-shell spike (installer → Design Hub) — still shell-over-Hub, no second renderer

### Never

- Auto-submit · invent claims · fork the renderer · commit `storage/` · reopen Netflix

---

## Public vs private (decision)

| Surface | GitHub (free) | Local only (`storage/`) | Future paid app |
|---|---|---|---|
| `pdf_tool` + themes + layouts + QA | ✅ | — | Same engine |
| Design Hub | ✅ | — | Shell launches Hub |
| Protocol docs (VAULT shape, JOB-ASSESSMENT) | ✅ generic | Real vaults / listings | Guided wizard UX |
| Personal make-*.md · mcp-pdf-designer.json | ❌ `.example` only | ✅ | N/A |
| Brand maps · collages · exports · applicants | ❌ | ✅ | User’s own local data |
| Marketing strategy with personal brands | High-level in [`docs/PRODUCT.md`](../../docs/PRODUCT.md) | Detail in `storage/docs/MARKETING.md` | Paid features list |

SSOT for free-vs-paid: [`docs/PRODUCT.md`](../../docs/PRODUCT.md).  
Clone how-to: [`docs/WHITE-LABEL.md`](../../docs/WHITE-LABEL.md).  
Private notes: [`storage/docs/`](../../storage/docs/) (gitignored with `storage/`).

---

## Marketing (summary — detail private)

1. **Free GitHub** — “local-first PDF / collage studio for agents + power users”; smoke script + Hub demo.
2. **Audience** — people who already write HTML/CSS or drive agents; not Canva beginners (yet).
3. **Paid later** — installer + recipe gallery chrome + guided export; sell *time saved*, not vaults.
4. **Do not** market personal career data, founder names, or private brand maps as the product.

Full narrative: `storage/docs/MARKETING.md` (local).
