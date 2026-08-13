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
- [ ] Wrap (`/reflect` + dev-log + tracked commit)

## Assumptions

- **Do not delete `storage/` this run.** Dual-run alias stays until a human confirms Hub/tracker/vault after living on root nouns. Flip signal: a full workday on root nouns with zero `storage/` reads.
- **Do not post Patreon, publish Gumroad, push GitHub, or history-scrub.** Consent + `jenninexus` auth + `TESTPYPI_TOKEN` (none in credential DB). Launch copy is the deliverable.
- **Gumroad $5 today would sell a shell that does not exist.** Early release = Patreon announcement of the **free** GitHub seed (after public push). Gumroad waits for installer / extra kit.
- **`.memory/` stays tracked.** Session start reads the **index**, not 19 files. Protocol lessons already live in `docs/`; Hub traps stay as lesson files until PREVIEWER absorbs them. Archiving the directory would hide clone-traveling traps (same failure as gitignored-only dev-log).
- CRLF-only dirty diffs in `.config/mcp-pdf-designer.example.json` and `scripts/testpypi-dry-run.py` are noise — restore, do not commit.

## Evidence

- VERIFIED: `python scripts/migrate-workspace.py` → copy=538; MG galleries under `resumes/{jenni,shade}/resources/images/martiangames` are **junctions** to `resumes/studio/...` (Python 3.10 `is_symlink()` misses junctions — script now uses `st_file_attributes`).
- VERIFIED: resolver prefers new nouns (`applications/`, `vaults/jenni.json`, `users/jenni.json`, `resumes/jenni`).
- VERIFIED: `python -m pdf_tool.tracker list` → **7** applications (not 14).
- VERIFIED: `pytest tests/test_workspace_paths.py tests/test_preview_workspace.py -q` → 19 passed (includes nested Sony leaf test).
- VERIFIED: Hub `GET /api/version` → 200.
- VERIFIED: sys-admin MCP ready; no TestPyPI credential in userdata.db.
- UNVERIFIED: GitHub push, history scrub, Patreon/Gumroad/blog publish, TestPyPI upload (Hard Stops / missing token).

## Deferred

- History scrub + force-push (explicit OK)
- `origin/main` push (`jenninexus` auth)
- TestPyPI upload (create account + token)
- Delete `storage/` alias after a workday on root nouns
- JN `/products` page implementation (site repo)
- Patreon / Gumroad / blog **publish** (human) — copy in product-design `docs/LAUNCH-PDF-DESIGNER.md`
- Paid-shell installer spike
- Archiving `.memory/` — **rejected**; index-only session start instead
