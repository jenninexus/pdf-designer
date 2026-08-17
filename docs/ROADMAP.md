# ROADMAP — pdf-designer

> **This is a pointer, not the roadmap.** The single active working checklist is
> [`Plans/_Active/2026-08-17-early-release-remaining.md`](../Plans/_Active/2026-08-17-early-release-remaining.md).
> `/jen:roadmap` resolves here. Plans index: [`Plans/README.md`](../Plans/README.md).
>
> Product UX target: [`WORKSPACE-LAYOUT.md`](WORKSPACE-LAYOUT.md) (root `users/` · `vaults/` · `_job-apps/` · …).  
> Live data today: those root nouns. [`STORAGE.md`](STORAGE.md) documents the layout + the `storage/` dual-run alias.

## Remaining (open items)

- [x] Root workspace **duplicates archived** (2026-08-16) — live data at root nouns; `storage/` keeps private provider template + private font + `_archive/`. Do not delete the `storage/` directory until dual-run is retired.
- [x] **One job noun** (2026-08-17) — `_job-apps/` is live + public; `applications/` is README-only.
- [ ] **History scrub** — `docs/HISTORY-SCRUB.md` (gitignored) then human-authorized force-push
- [x] **Push origin/main** — `jenninexus` GitHub auth (normal HTTPS push 2026-08-14; follow-up docs 2026-08-16). Repo stays **private**.
- [ ] **Patreon / blog / Discord / short-form** — drafts in socials; do not post/deploy from an agent. Card: `C:\Github\product-design\docs\PDF-DESIGNER.md`
- [ ] Keep **SSOT + QA docs** honest as the engine evolves
- [ ] Optional: TestPyPI upload (not required for clone launch) · production PyPI · paid-shell

### Recently landed

- [x] **Public README + browser/PDF overview** (2026-08-13) — clone-safe product loop, browser-openable overview, and fresh-clone smoke evidence
- [x] **Hub path/header repair** (2026-08-13) — live profiles/folders; profile scopes library
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
