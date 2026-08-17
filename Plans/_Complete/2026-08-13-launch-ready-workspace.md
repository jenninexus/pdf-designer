# pdf-designer — launch-ready workspace + product board

**Date:** 2026-08-13 · **Host:** SEGOPC · **Mode:** `/auto-goal`  
**Prior (complete this morning):** Hub profile-scope + sticky filters (`8d79911`).  
**Hub repair plan archived:** [`../_Complete/2026-08-13-previewer-path-header-repair.md`](../_Complete/2026-08-13-previewer-path-header-repair.md)

Product-design hub: `C:\Github\product-design` (renamed from `Products`). Command SSOT: `.claude/commands/products.md`. Global pointer: `~/.claude/commands/jen/products.md`.

---

## Done when

- [x] Root-noun folders hold a **copy** of SEGO live data; `storage/` remains as read-only alias.
- [x] `iter_application_json` dedupes by **path relative to the applications root**, not leaf folder name.
- [x] `python -m pdf_tool.tracker list` still reports **7** applications (not 14).
- [x] `python -m pytest tests/test_workspace_paths.py tests/test_preview_workspace.py -q` passes.
- [x] Hub `http://127.0.0.1:8787/` returns 200 after the copy.
- [x] `pytest-of-Owner/` is gitignored and removed from the working tree.
- [x] product-design registry board lists **stage + price + free/paid diffs** for every SKU.
- [x] `/jen:products` is a ⛔ pointer; repo `products.md` is the ⭐ SSOT (relative paths).
- [x] Completed Hub-repair plan sits in `_Complete/`.
- [x] Launch **copy** for Patreon → Gumroad → JN exists in the hub (not posted — Hard Stop).

---

## Task checklist

- [x] Orient: start ritual, tracker (7 SUBMITTED), Hub :8787, sys-admin running, TestPyPI token absent
- [x] Fix application identity (relative path) + nested-leaf test
- [x] Write + run `scripts/migrate-workspace.py` (copy, remap MG junctions, keep `storage/`)
- [x] Gitignore + delete `pytest-of-Owner/`
- [x] Move Hub repair plan → `_Complete`; refresh this plan + `Plans/README.md` + ROADMAP
- [x] product-design: rename paths, SSOT command, registry board, launch sequence, active plan
- [x] `~/.claude/commands/jen/products.md` pointer + jen README + JN ROADMAP hub path
- [x] Dual-run smoke (tracker, pytest, Hub)
- [x] Wrap (`/reflect` + dev-log + tracked commit)

### Release assets addendum — 2026-08-13

- [x] Refresh the public README around the clone-safe product loop and public/private boundary.
- [x] Create a public-safe browser/PDF overview using only documented claims; render and inspect both pages.
- [x] Link the browser source and PDF from the README and record their local-only status on the product board.
- [x] Re-run fresh-clone smoke and relevant tests; commit only safe tracked release assets locally.

### Release-content alignment — 2026-08-13

- [x] Normalize the local JenniNexus Patreon and blog sister drafts to dated, platform-owned paths.
- [x] Correct the Socials JN content protocol: each platform has sibling `drafts/` and `published/` folders; no generated/published artifacts live inside a devlog draft topic directory.
- [x] Link the product card to the actual local drafts and retain every human publication gate.

## Assumptions

- **Do not delete `storage/` this run.** Dual-run alias stays until a human confirms Hub/tracker/vault after living on root nouns. Flip signal: a full workday on root nouns with zero `storage/` reads.
- **Do not post Patreon, publish Gumroad, push GitHub, or history-scrub.** Consent + `jenninexus` auth + `TESTPYPI_TOKEN` (none in credential DB). Launch copy is the deliverable.
- **Gumroad $5 today would sell a shell that does not exist.** Early release = Patreon announcement of the **free** GitHub seed (after public push). Gumroad waits for installer / extra kit.
- **`.memory/` stays tracked.** Session start reads the **index**, not 19 files. Protocol lessons already live in `docs/`; Hub traps stay as lesson files until PREVIEWER absorbs them. Archiving the directory would hide clone-traveling traps (same failure as gitignored-only dev-log).
- CRLF-only dirty diffs in `.config/mcp-pdf-designer.example.json` and `scripts/testpypi-dry-run.py` are noise — restore, do not commit.
- The browser/PDF overview is a **release asset**, not a launch event: it may be tracked because it contains
  only public examples and product documentation. It does not authorize public GitHub, Patreon, blog,
  Gumroad, or JN-store publication.
- The target date `2026-08-14` names the planned sister draft files, not an authorization to publish.

## Evidence

- VERIFIED: `python scripts/migrate-workspace.py` → copy=538; MG galleries under `resumes/{jenni,shade}/resources/images/martiangames` are **junctions** to `resumes/studio/...` (Python 3.10 `is_symlink()` misses junctions — script now uses `st_file_attributes`).
- VERIFIED: resolver prefers new nouns (`applications/`, `vaults/jenni.json`, `users/jenni.json`, `resumes/jenni`).
- VERIFIED: `python -m pdf_tool.tracker list` → **7** applications (not 14).
- VERIFIED: `pytest tests/test_workspace_paths.py tests/test_preview_workspace.py -q` → 19 passed (includes nested Sony leaf test).
- VERIFIED: Hub `GET /api/version` → 200.
- VERIFIED: sys-admin MCP ready; no TestPyPI credential in userdata.db.
- UNVERIFIED: GitHub push, history scrub, Patreon/Gumroad/blog publish, TestPyPI upload (Hard Stops / missing token).
- VERIFIED (release assets addendum): browser-openable `docs/pdf-designer-overview.html` rendered by
  PDF Designer to `docs/pdf-designer-overview.pdf`; palette and print-overflow checks pass, and both
  pages were visually inspected. README and docs index link them.
- VERIFIED (release assets addendum): `python -m pytest tests/test_workspace_paths.py
  tests/test_preview_workspace.py -q` → 19 passed; `python scripts/smoke-white-label.py` → PASS,
  including rendered QA and contiguous ATS section cues.
- VERIFIED (release-content alignment): local JenniNexus content protocol and product card now point to
  dated Patreon/blog drafts with the shared `pdf-designer` slug; every platform archives only to its
  own sibling `published/` directory. Publication remains unperformed.

## Deferred

- History scrub + force-push (explicit OK)
- `origin/main` push (`jenninexus` auth)
- TestPyPI upload (create account + token)
- Delete `storage/` alias after a workday on root nouns
- JN `/products` page implementation (site repo)
- Patreon / Gumroad / blog **publish** (human) — drafts in socials; card `C:\Github\product-design\docs\PDF-DESIGNER.md`
- Paid-shell installer spike
- Archiving `.memory/` — **rejected**; index-only session start instead
