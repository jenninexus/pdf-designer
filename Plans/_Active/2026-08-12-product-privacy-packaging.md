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
- [x] **Privatize bare `.claude/commands/`** — track **only** `*.example.md` (start/wrap/README/make-* local)
- [x] Add `make-collage.example.md`
- [x] Wire `/reflect` into project wrap + mandatory next-agent handoff
- [x] Public product entry: `examples/resume-studio/` + job-market résumé pitch in PRODUCT
- [ ] **TestPyPI upload** — needs `TESTPYPI_TOKEN` → `python scripts/testpypi-dry-run.py --upload`
- [ ] **Push origin/main** — needs `jenninexus` GitHub auth (MonoFinity gh fails “repo not found”)
- [ ] Optional: deepen `examples/resume-studio/` (sample vault walkthrough HTML / Hub deep-link card)
- [ ] Optional: PyPI production after TestPyPI succeeds
- [ ] Optional: paid-shell spike (installer → Design Hub) — still shell-over-Hub, no second renderer

### Never

- Auto-submit · invent claims · fork the renderer · commit `storage/` · reopen Netflix  
- Force-add bare `.claude/commands/{start,wrap,README,make-*}.md` to GitHub

---

## Public vs private (decision)

| Surface | GitHub (free) | Local only | Future paid app |
|---|---|---|---|
| `pdf_tool` + themes + layouts + QA | ✅ | — | Same engine |
| Design Hub | ✅ | — | Shell launches Hub |
| `examples/resume-studio/` + protocol `*.example.md` | ✅ | — | Guided wizard UX |
| Protocol docs (VAULT shape, JOB-ASSESSMENT) | ✅ generic | Real vaults / listings | Guided wizard UX |
| Bare start/wrap/make-*/commands README | ❌ | ✅ SEGO ritual + `/reflect` | N/A |
| `mcp-pdf-designer.json` | ❌ `.example` only | ✅ | N/A |
| Brand maps · collages · exports · applicants | ❌ | ✅ `storage/` | User’s own local data |
| Marketing strategy with personal brands | High-level in [`docs/PRODUCT.md`](../../docs/PRODUCT.md) | Detail in `storage/docs/MARKETING.md` | Paid features list |

SSOT for free-vs-paid: [`docs/PRODUCT.md`](../../docs/PRODUCT.md).  
Clone how-to: [`docs/WHITE-LABEL.md`](../../docs/WHITE-LABEL.md) · [`examples/resume-studio/`](../../examples/resume-studio/).  
Private notes: [`storage/docs/`](../../storage/docs/) (gitignored with `storage/`).

---

## Marketing (summary — detail private)

1. **Free GitHub** — résumé creator for a broken market: vaults + skills + palettes; smoke + Hub.
2. **Audience** — agents + power users who refuse invented claims; paid shell later for seekers.
3. **Paid later** — installer + vault/export wizard; sell *time saved*, not vaults.
4. **Do not** market personal career data, founder names, or private brand maps as the product.

Full narrative: `storage/docs/MARKETING.md` (local).
