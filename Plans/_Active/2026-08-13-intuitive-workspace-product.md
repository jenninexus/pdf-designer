# Active plan — Intuitive root workspace · product UX

**Date:** 2026-08-13 · **Host:** SEGOPC  
**Prior waves (complete):**  
[`../_Complete/2026-08-12-product-privacy-packaging.md`](../_Complete/2026-08-12-product-privacy-packaging.md) ·  
[`../_Complete/2026-08-12-public-private-split/`](../_Complete/2026-08-12-public-private-split/)

---

## Product decision (locked)

**Move personal workspace out of opaque `storage/` into root nouns** so GitHub clones
read like a product, not a dump:

`users/` · `vaults/` · `profiles/` · `resumes/` · `applications/` · `collages/` · `brands/`

- Real data stays **gitignored**; tracked **README + `*.example.*` + `examples/`** teach the shape.
- **All docs live under `docs/`** — private notes (`MARKETING` · `WORKSPACE` · `HISTORY-SCRUB`)
  sit beside public docs and are gitignored (no `storage/docs/` dual tree).
- Engine still uses `storage/` **until** a path resolver + migration land (do not move vaults tonight).

SSOT: [`docs/WORKSPACE-LAYOUT.md`](../../docs/WORKSPACE-LAYOUT.md).

---

## Session checklist

### Docs / ignore (this wave)

- [x] Write [`docs/WORKSPACE-LAYOUT.md`](../../docs/WORKSPACE-LAYOUT.md) recommendation
- [x] Move private notes → `docs/{MARKETING,WORKSPACE,HISTORY-SCRUB}.md` + gitignore
- [x] Retire tracked `storage/docs/README.md`; leave local redirect stub
- [x] Archive 2026-08-12 active plans → `_Complete/`
- [x] Refresh [`docs/README.md`](../../docs/README.md) · [`PUBLIC-LOCAL-SPLIT.md`](../../docs/PUBLIC-LOCAL-SPLIT.md) · [`PRODUCT.md`](../../docs/PRODUCT.md) · [`STORAGE.md`](../../docs/STORAGE.md) pointers
- [x] Update [`docs/ROADMAP.md`](../../docs/ROADMAP.md) · [`Plans/README.md`](../README.md) · `/jen/roadmap` pdf-designer row
- [x] Dev-log `#pdf-designer-s021` + optional `C:\Github\Products\docs\PDF-DESIGNER.md` hub

### Migration (next engineering)

- [ ] Add `workspace` path resolver (accept `storage/` **and** root nouns during cutover)
- [ ] Scaffold root dirs with README + example stubs (tracked)
- [ ] Migrate SEGO `storage/{users,profiles,jenni,shade,studio,collages,brand-design,_job-listings}` → new nouns
- [ ] Update Hub / vault / tracker / collage / AGENTS / make-* examples
- [ ] Dual-run smoke; then remove `storage/` alias

### Still human-gated (carry forward)

- [ ] Push `origin/main` — `jenninexus` GitHub auth
- [ ] History scrub — `docs/HISTORY-SCRUB.md` + explicit OK + force-push
- [ ] TestPyPI upload — `TESTPYPI_TOKEN`
- [ ] Optional: production PyPI · paid-shell spike

### Never

- Auto-submit · invent claims · fork the renderer · commit real vaults · reopen Netflix  
- Force-add bare `.claude/commands/{start,wrap,README,make-*}.md`  
- Big-bang delete `storage/` before path resolver is green

---

## Skills / plugins to lean on (product design)

From `C:\mcp\.claude\plugins.yaml` — use these when shaping the free→paid story:

| Plugin / skill | Use for pdf-designer |
|---|---|
| **product-management** (`/write-spec`, `/metrics-review`) | Spec the root-workspace migration + paid-shell MVP acceptance criteria |
| **marketing** (`/campaign-plan`, `/draft-content`) | GitHub launch / Product Hunt drafts — after layout looks clone-friendly |
| **frontend-design** + `/theme` | Design Hub / future installer chrome (pair with www-theme-kit tokens) |
| **feature-dev** | Architect the path-resolver cutover against live `preview.py` / vault code |
| **superpowers** `/brainstorm` | Only if folder nouns still feel wrong before Phase 2 |
| **engineering** `/architecture` | Optional second opinion on alias vs hard cutover |

Do **not** invent a parallel product process — Plans + PRODUCT.md stay the SSOT; plugins assist.

---

## Carry-forward evidence (already VERIFIED last wave)

- Resume Studio walkthrough + smoke + local wheel dry-run green
- Commands = `*.example.md` only on GitHub
- PUBLIC-LOCAL-SPLIT + GETTING-STARTED shipped

## Deferred / UNVERIFIED

- Push · history scrub · TestPyPI upload (credentials / consent)
- Physical `storage/` → root move (this plan’s engineering track)
