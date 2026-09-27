# Product carryover and remote containment

**Status:** Active — verified local main awaits authorized publication; the next product slice requires
an explicit selection.
**Public safety:** no names, employers, vault claims, machine paths, or private media belong here.

## Completed context

- Workspace/export organization:
  [`../_Complete/2026-09-26-export-library-organization.md`](../_Complete/2026-09-26-export-library-organization.md)
- Earlier roadmap, private-preview repair, and stage-filter history:
  [`../_Complete/2026-09-26-roadmap-completed-archive.md`](../_Complete/2026-09-26-roadmap-completed-archive.md)
- Canonical current map: [`../../docs/PUBLIC-LOCAL-SPLIT.md`](../../docs/PUBLIC-LOCAL-SPLIT.md) and
  [`../../docs/STORAGE.md`](../../docs/STORAGE.md)

## Remaining gate — publish verified local main

- [ ] Activate an existing credential with write access to `jenninexus/pdf-designer`.
- [ ] Restore the real `origin` push URL, push local `main`, fetch, and prove `origin/main` contains
  `6c639a37b86320c5717a5825b8e8348029eff4ff`.
- [ ] Close recovery-queue item
  `203463379ec2b8182ebf6e4c5e26e695723ea1ba7d4680289274a53f039e35a5` only after that containment
  proof. The clean checkout is currently 14 commits ahead of `origin/main`; the configured push URL is
  intentionally blocked at `github.invalid`.

This is an external credential gate, not unfinished engineering in the completed organization slice.

## Next accepted slice — choose before implementation

### Decision-gated

- [ ] **pywebview shell** — remains parked; see
  [`../_Complete/2026-07-11-design-hub-parked-phases.md`](../_Complete/2026-07-11-design-hub-parked-phases.md).
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
- Keep exactly this one non-README file in `Plans/_Active/` until one of those conditions changes.

