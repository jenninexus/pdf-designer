# Hub examples, listing pointers, storage retire

## Done when
- [x] `_job-apps/` is the only live listing noun; workspace + READMEs no longer tell people to store copies under `storage/_job-listings/`
- [x] Public Hub (`python -m pdf_tool.preview examples`) shows a working example for resume, cover letter, letter, work samples, collage, and gallery, sorted first in each kind
- [x] Design Hub no longer lists `_archive/` or `*.template.html`; live `resumes/` / `_job-apps/` / `collages/` HTML for jenni, shade, studio, martian still appears
- [x] `/storage/<user>/…` preview URLs resolve to `resumes/<user>/…` when the live file exists
- [x] Hub chrome + preview iframes use the same cyan scrollbar treatment
- [x] Unique `storage/` leftovers relocated; `storage/` directory removed; dual-run resolver still accepts the alias in tests
- [ ] HISTORY-SCRUB backup exists; rewrite + force-push only with the already-given human OK (BEE re-clone parked, not surprised)

## Task checklist
- [x] Archive listing pointers (workspace + examples/docs copy recipes)
- [x] Exclude `_archive` + `.template.html` from Hub scan
- [x] Serve files through `resolve_rel` so moved HTML is not 404
- [x] Public cover-letter, work-samples, gallery examples; sort `examples/` first
- [x] Header chip colors + themed scrollbars (chrome + iframe inject)
- [x] Relocate private provider.md + private font; dual-run smoke; delete `storage/`
- [ ] HISTORY-SCRUB backup; execute rewrite if tools/auth allow
- [x] Update STORAGE / ROADMAP / remaining plan / product card

## Assumptions
- User OK for history scrub + deleting `storage/` is this prompt. Patreon/blog/Discord stay unposted (consent not granted for public posts).
- JN `/products` in the remaining plan means the **site** page. The product-design hub card already exists.
- `socialMarketing` is a register (format-manifest), not a second voice-seed card; Jenni’s posting-face prefs are a section of `jenni.md` / `characterVoice.socialPostingPrefs`.
- BEE clone is not force-reset from this machine (Hard Stop: other people’s live state).

## Evidence
- (filled as we go)

## Deferred
- Patreon / blog / Discord / short-form posting
- Gumroad installer/wizard
- JN.com `/products` store page
- BEE re-clone after history scrub
- TestPyPI upload
