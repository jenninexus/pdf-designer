# ROADMAP — pdf-designer

> **This is the durable product backlog and status map.**
>
> | Kind | File |
> |---|---|
> | **Active product slice** | [`Plans/_Active/9-27-2026-pdf-work.md`](../Plans/_Active/9-27-2026-pdf-work.md) — session protocol/docs cleanup plus the ordered remaining-work checklist |
> | **Completed history** | [`Plans/_Complete/2026-09-26-roadmap-completed-archive.md`](../Plans/_Complete/2026-09-26-roadmap-completed-archive.md) |
>
> `/jen:roadmap` resolves here. Plans index: [`Plans/README.md`](../Plans/README.md).
> `/pdf-start` and `/pdf-wrap` use the active plan plus this roadmap. Do not create or update
> `dev-log.yaml`, `dev-log-sego.yaml`, or `dev-chat.md`; the old YAML is frozen under
> [`Plans/_Complete/_archive/`](../Plans/_Complete/_archive/).
>
> Product UX target: [`WORKSPACE-LAYOUT.md`](WORKSPACE-LAYOUT.md) (root `users/` · `vaults/` · `_job-apps/` · …).  
> Live data today: those root nouns. [`STORAGE.md`](STORAGE.md) documents the layout + the `storage/` dual-run alias.

## Current execution

The exact checklist, blocker evidence, and next action live in
[`Plans/_Active/9-27-2026-pdf-work.md`](../Plans/_Active/9-27-2026-pdf-work.md). The current accepted
organization slice completed on 2026-09-27: `/pdf-start` and `/pdf-wrap` are self-contained, superseded
docs are archived, ignore rules are corrected, and generated command adapters match their sources.
The active plan remains open because the release and product queue below is not complete.

After that slice, priority remains:

1. Resolve the existing remote containment gate when a writable jenninexus credential is available;
   prove the intended remote mainline contains the local tip and close recovery item
   `203463379ec2b8182ebf6e4c5e26e695723ea1ba7d4680289274a53f039e35a5`.
2. Select one next product-evolution slice from the decision-gated work below.

The 2026-09-26 private-preview repair and stage filters are verified and archived in the
completed-history file linked above.

The completed workspace/export organization slice is archived at
[`Plans/_Complete/2026-09-26-roadmap-completed-archive.md#export-library-organization`](../Plans/_Complete/2026-09-26-roadmap-completed-archive.md#export-library-organization).
Its original centralized `_exports/` decision was superseded 2026-09-27: exports now live beside
their document family (`resumes/<user>/…`, `collages/<project>/`), with `_exports/` as the fallback.
See [`STORAGE.md`](STORAGE.md).

### Parked / decision-gated

- **PyWebView or Electron shell** — reopen only after enough local-first workflow evidence exists to
  choose the smallest maintainable shell. Historical PyWebView plan:
  [`Plans/_Complete/2026-07-11-design-hub-parked-phases.md`](../Plans/_Complete/2026-07-11-design-hub-parked-phases.md).
- **Signed binary channel** — only after a private channel decision; require valid Authenticode plus
  clean Windows 10/11 x64 VM proof before any binary listing. Unsigned listing stays off.
- **Production PyPI** — only after TestPyPI proof and an explicit channel decision; the GitHub clone
  remains the complete free product.

### Product evolution

- **Canvas editor** — drag/drop image tray, canvas presets, layout-family starts, hero selection, and
  text blocks over the same `collage-source.json` used by the CLI.
- **Collage books** — multi-page project manifest → render pages → `merge_pdfs`.
- **Desktop output-folder picker** — only in a packaged desktop shell; retain editable path text.

### Never

- Auto-submit · invent claims · fork the renderer · commit real vaults · reopen Netflix  
- Force-push history rewrite without explicit human OK + jenninexus auth  
- Recreate `storage/` as a second vault/listing store
