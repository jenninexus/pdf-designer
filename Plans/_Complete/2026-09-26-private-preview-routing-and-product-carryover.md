# Product carryover and remote containment

**Status:** Closed 2026-09-27 — moved to `_Complete` at owner direction. Nothing was dropped: every open
item below is carried verbatim in [`docs/ROADMAP.md`](../../docs/ROADMAP.md) (remote containment gate with
the recovery-queue id; decision-gated and product-evolution slices). No product slice was accepted, so
`Plans/_Active/` holds only its README until one is.
**Public safety:** no names, employers, vault claims, machine paths, or private media belong here.

## Completed context

- Workspace/export organization:
  [`2026-09-26-roadmap-completed-archive.md#export-library-organization`](2026-09-26-roadmap-completed-archive.md#export-library-organization)
- Earlier roadmap, private-preview repair, and stage-filter history:
  [`2026-09-26-roadmap-completed-archive.md`](2026-09-26-roadmap-completed-archive.md)
- Canonical current map: [`../../docs/PUBLIC-LOCAL-SPLIT.md`](../../docs/PUBLIC-LOCAL-SPLIT.md) and
  [`../../docs/STORAGE.md`](../../docs/STORAGE.md)

## Remaining gate — publish verified local main

- [ ] Activate an existing credential with write access to `jenninexus/pdf-designer`.
- [ ] Restore the real `origin` push URL, push local `main`, fetch, and prove `origin/main` contains the
  current local-main tip recorded in the recovery item below.
- [ ] Close recovery-queue item
  `203463379ec2b8182ebf6e4c5e26e695723ea1ba7d4680289274a53f039e35a5` only after that containment
  proof. The clean checkout remains ahead of `origin/main`; the configured push URL is intentionally
  blocked at `github.invalid`.

This is an external credential gate, not unfinished engineering in the completed organization slice.

## Next accepted slice — choose before implementation

### Decision-gated

- [ ] **pywebview shell** — remains parked; see
  [`2026-07-11-design-hub-parked-phases.md`](2026-07-11-design-hub-parked-phases.md).
- [ ] **Signed binary channel** — reopen only after a private-channel decision; require valid
  Authenticode and clean Windows 10/11 x64 VM evidence. Do not list an unsigned executable.
- [ ] **Production PyPI** — proceed only after TestPyPI proof and an explicit channel decision; the
  GitHub clone remains the complete free product.

### Product evolution

- [ ] **Canvas editor** over the existing `collage-source.json`: drag/drop tray, presets,
  layout-family starts, hero selection, text blocks, and the existing export endpoint.
- [ ] **Collage books:** multi-page manifest → render pages → `merge_pdfs`.
- [ ] **Desktop export-folder picker:** only inside the signed shell; retain editable path text.

## Acceptance for this active plan

- Remote gate closes only with fresh destination containment evidence for the exact intended mainline.
- Product work starts only after one slice is explicitly accepted and receives its own bounded plan.
- ~~Keep exactly this one non-README file in `Plans/_Active/`~~ — superseded 2026-09-27: the open items live in ROADMAP; `_Active` is empty until a slice is accepted.
