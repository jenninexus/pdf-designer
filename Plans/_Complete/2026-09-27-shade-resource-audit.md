# Shade shared-resource audit

## Scope

- Inventory Shade and studio media, including ignored private files.
- Map each asset to its actual HTML/JSON consumers.
- Keep document-local assets local; consolidate only genuinely person-wide assets under
  `users/shade/resources/`; retain studio-wide Martian Games assets in their shared studio home.
- Verify affected documents, privacy ignores, and the latest TDX Lodge Concepts résumé.

## Changed-files ledger

- `AGENTS.md` — advertise the per-person reusable resource contract.
- `docs/GETTING-STARTED.md` · `docs/STORAGE.md` · `docs/EXPORTS.md` · `resumes/README.md` — document ownership tiers and all four resource lanes.
- `src/pdf_tool/starter_workspace.py` · `src/pdf_tool/static/wizard.html` — create and surface `images/`, `logos/`, `videos/`, and `references/` for every new person.
- `tests/test_starter_workspace.py` — cover the expanded starter contract.
- Private ignored workspace: migrated live `refrence/` trees to `references/`, updated user/vault/profile pointers, and preserved the old trees under `storage/_archive/resource-spelling-migration-2026-09-27/`.
- `Plans/_Complete/2026-09-27-shade-resource-audit.md` — task evidence and closeout.

## Acceptance evidence

- [x] Every moved or retained media asset has an identified ownership tier and consumer.
- [x] No private media becomes tracked (`git check-ignore` confirms `resumes/*`).
- [x] All affected local media references resolve; TDX résumé, cover letter, and work examples pass `check_generation`; the light résumé passes ATS.
- [x] The exact recent Shade card-company résumé is identified as the TDX Lodge Concepts Graphic Artist light/dark pair; the light PDF was queued in Codex.
- [x] Public documentation/tests now cover the previously missing `videos/` and `references/` lanes.

## Notes

- Source authority: current `main` at `d4ad2bb` plus private ignored workspace data.
- Rollback boundary: text changes are ledgered; private media is copied and verified before any exact
  source-file removal.

## Verification

- `python -m pytest tests/test_starter_workspace.py -q` — 4 passed.
- `python -m pytest tests/test_wizard.py tests/test_preview_workspace.py -q` — 25 passed.
- `python -m pdf_tool.check_vault --all` — PASS (existing unverified-tool warnings only).
- `python -m pdf_tool.check_generation <TDX resume|cover letter|work examples>` — 3/3 PASS.
- `python -m pdf_tool.check_ats resumes/shade/TDX-Lodge-Concepts-Graphic-Artist/shade-tdx-graphic-artist-resume-light.pdf` — PASS, zero mid-word splits.
- Copied reference files matched their originals by SHA-256 before the legacy trees were archived.
- `git -c core.whitespace=cr-at-eol diff --check` — clean for this CRLF-native repository.

## Friction

- Observation: the starter created only image/logo lanes while live data used the misspelled `refrence/` lane.
- Cause (high confidence): the resource feature was initially scoped to visual work samples and inherited an older private-folder typo.
- Effect: videos and source evidence had no generated home, and future agents could perpetuate two spellings.
- Remedy: one four-lane per-person contract, live pointer migration, focused tests, and recoverable archival of the old folders. Verified by path scans, hashes, vault validation, and document generation gates.

## Synabrain

- Request `ctxreq_e8795ff1aff04f0ea485ea4ece969859`: `grounded`, useful — it identified the TDX Lodge Concepts application and distinguished it from the earlier Santa Barbara Games application.
- Review: 1 useful, 0 suboptimal; activity healthy; no performance review required.
- Durable link: `ctxlink_0130d475ac944f37bb913ff2a7def92b` associates the request with this completed plan.
