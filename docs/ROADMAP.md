# ROADMAP — pdf-designer

> **This is a pointer, not the roadmap.** The single active working checklist is
> [`Plans/_Active/2026-08-13-intuitive-workspace-product.md`](../Plans/_Active/2026-08-13-intuitive-workspace-product.md).
> `/jen:roadmap` resolves here. Plans index: [`Plans/README.md`](../Plans/README.md).
>
> Product UX target: [`WORKSPACE-LAYOUT.md`](WORKSPACE-LAYOUT.md) (root `users/` · `vaults/` · …).  
> Live tree today: still [`STORAGE.md`](STORAGE.md) under `storage/`.

## Remaining (open items)

- [ ] **Root workspace migration** — data move + drop `storage/` (resolver + README scaffolds landed)
- [ ] **History scrub** — `docs/HISTORY-SCRUB.md` (gitignored) then human-authorized force-push
- [ ] **TestPyPI upload** — `TESTPYPI_TOKEN` → `python scripts/testpypi-dry-run.py --upload`
- [ ] **Push origin/main** — `jenninexus` GitHub auth
- [ ] Keep **SSOT + QA docs** honest as the engine evolves
- [ ] Optional: production PyPI · paid-shell · collage recipe docs

### Recently landed

- [x] **Docs-only private notes** (2026-08-13) — `MARKETING` / `WORKSPACE` / `HISTORY-SCRUB` under `docs/` + gitignore; no `storage/docs/` dual tree
- [x] **WORKSPACE-LAYOUT recommendation** — root nouns for future users
- [x] **Public vs local architecture** (2026-08-12) — `PUBLIC-LOCAL-SPLIT` · `GETTING-STARTED`
- [x] **Clone-safe Resume Studio walkthrough** + smoke / wheel gates
- [x] **Commands privacy** — `*.example.md` only on GitHub
- [x] **Hub drawer / layouts / letterhead** (2026-08-10)

### Parked

- [ ] **pywebview shell** — [`Plans/_Complete/2026-07-11-design-hub-parked-phases.md`](../Plans/_Complete/2026-07-11-design-hub-parked-phases.md)

### Never

- Auto-submit · invent claims · fork the renderer · commit real vaults · reopen Netflix  
- Force-push history rewrite without explicit human OK + jenninexus auth  
- Delete `storage/` before dual-path resolver is green
