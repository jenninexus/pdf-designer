# Design Hub path and header repair

## Done when

- [x] The recent dual-path resolver and Products-hub work has an evidence-backed review.
- [x] The Design Hub discovers live workspace documents and exposes their actual profiles/folders in both header and drawer controls.
- [x] A legacy-only `storage/` workspace remains visible during the migration, while README-only root scaffolds do not displace live payloads.
- [x] Focused automated checks and an HTTP/API smoke test demonstrate the repaired behavior.
- [ ] The session wrap records the outcome and any durable lesson.

## Task checklist

- [x] Read workspace/layout/previewer doctrine, durable lessons, plan, status, and recent local log.
- [x] Trace the document-index and UI-filter data path against the current private workspace.
- [x] Implement the smallest path/header correction.
- [x] Verify the API/index and rendered header controls.
- [ ] Review the resulting diff, wrap, and report.

## Assumptions

- The requested "options" are the Design Hub's profile and folder selectors, which currently need to reflect live private workspace paths during the storage-to-root-nouns migration. This will be reconsidered if the data trace identifies a different control.
- Existing unrelated changes in `.config/mcp-pdf-designer.example.json`, `scripts/testpypi-dry-run.py`, and `pytest-of-Owner/` are another agent's work and remain untouched.

## Evidence

- VERIFIED: independent read-only review identified profile selectors hard-coded to four names and custom preview roots loading palette choices from the repository root instead of the requested root. It also confirmed root-noun folders are scaffolds while the live SEGO documents remain correctly under `storage/`.
- VERIFIED: `python -m pytest tests/test_workspace_paths.py tests/test_preview_workspace.py -q` → 13 passed.
- VERIFIED: `python -m pytest -q` → 56 passed.
- VERIFIED: in-process HTTP smoke of `make_handler()` returned `/api/version` (43,787 bytes) and injected each live workspace profile (`jenni`, `shade`, `studio`, `martian`) twice — desktop header and mobile drawer.
- VERIFIED: direct scan reports workspace profiles `jenni, martian, shade, studio`; documents continue to scan from the legacy path (129 documents) until data migration.

## Deferred

- Private-data migration from `storage/` to root nouns is outside this request's safe code repair; retain the read-only alias.
- Push remains blocked by the user's stated jenninexus authentication gate.
- The reviewer noted application deduplication is based only on a leaf folder name. It is unrelated to the header/path symptom and is intentionally not changed here.
