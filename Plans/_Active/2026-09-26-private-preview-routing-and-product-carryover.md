# Private preview routing and product carryover

**Status:** Active carryover; the 2026-09-26 preview-fidelity slice is verified
**Public safety:** no names, employers, vault claims, machine paths, or private media are recorded here.

## Accepted slice

- [x] Keep local profiles, vaults, résumés, job applications, collages, brands, and exports gitignored.
- [x] Restore private collage source images beside the HTML that references them; retain `_exports` as
  deliverables rather than the only copy of source media.
- [x] Correct the two private favorite-page paths that traversed above their project image folders.
- [x] Turn the selected-document kind, profile, and root-folder pills into accessible library filters.
- [x] Complete automated, HTTP, and browser-level verification.
- [ ] Select the next accepted carryover slice before implementation; do not start a decision-gated
  item without its named decision.

## Carryover — next accepted slices

### Decision-gated (do not start without the named decision)

- [ ] pywebview shell — remains parked; see
  [`../_Complete/2026-07-11-design-hub-parked-phases.md`](../_Complete/2026-07-11-design-hub-parked-phases.md).
- [ ] Signed binary channel — reopen only after a private-channel decision; require valid Authenticode
  and clean Windows 10/11 x64 VM evidence. Do not list an unsigned executable.
- [ ] Production PyPI — proceed only after TestPyPI proof and an explicit channel decision; the GitHub
  clone remains the complete free product.

### Product evolution

- [ ] Canvas editor over the existing `collage-source.json`: drag/drop tray, presets, layout-family
  starts, hero selection, text blocks, and the existing export endpoint.
- [ ] Collage books: multi-page manifest → render pages → `merge_pdfs`.
- [ ] Desktop output-folder picker only inside the signed shell; retain editable path text.

## Changed-files ledger

Tracked/public-safe:

- `.gitignore`
- `.memory/README.md`
- `.memory/lesson-private-collage-source-assets.md`
- `docs/PREVIEWER.md`
- `docs/ROADMAP.md`
- `Plans/README.md`
- `Plans/_Active/2026-09-26-private-preview-routing-and-product-carryover.md`
- `Plans/_Complete/2026-09-26-roadmap-completed-archive.md`
- `src/pdf_tool/preview.py`
- `src/pdf_tool/static/hub.css`
- `tests/test_preview_workspace.py`

Personal/local and intentionally ignored:

- restored private image payload under `collages/martian-collage/`
- corrected private HTML under `collages/meet-jenni-bot/faves/` and `collages/syn-themes/faves/`
- canonical personal `/jen:roadmap` command and its generated user-level adapter

## Acceptance evidence

- Every referenced local image on the affected Martian, Meet Jenni Bot, and Syn Themes pages resolves.
- Browser inspection shows nonzero image dimensions and no broken-image placeholders.
- Clicking each stage pill updates the matching header control and scopes the left library without
  replacing the selected preview.
- Private paths remain ignored; public tests and clone-safe smoke pass.
- Verification: 21/21 affected image requests returned HTTP 200; browser dimensions were nonzero for
  all 21; 119 tests passed; public white-label smoke and wheel-asset gate passed.

## Friction record

- **Observation:** gallery layouts rendered filenames instead of images.
- **Cause / confidence:** high — nine source PNGs existed only in `_exports`; two favorite pages used
  `../../` where their assets live under `../images/`.
- **Effect:** private documents were discoverable but visually broken in the Hub.
- **Remedy / verification:** restore source placement, correct relative paths, test direct HTTP routes,
  and inspect image `naturalWidth` in the running Hub before closeout.
