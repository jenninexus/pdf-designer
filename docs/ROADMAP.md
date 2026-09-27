# ROADMAP — pdf-designer

> **This is the durable product backlog and status map.**
>
> | Kind | File |
> |---|---|
> | **Active product slice** | _none accepted_ — `Plans/_Active/` holds only its README. Last carryover plan (closed 2026-09-27): [`Plans/_Complete/2026-09-26-private-preview-routing-and-product-carryover.md`](../Plans/_Complete/2026-09-26-private-preview-routing-and-product-carryover.md) |
> | **Completed history** | [`Plans/_Complete/2026-09-26-roadmap-completed-archive.md`](../Plans/_Complete/2026-09-26-roadmap-completed-archive.md) |
>
> `/jen:roadmap` resolves here. Plans index: [`Plans/README.md`](../Plans/README.md).
> Session narrative **does not** go in `dev-log-sego.yaml` (frozen 2026-09-08 → [`Plans/_Complete/_archive/`](../Plans/_Complete/_archive/)).
>
> Product UX target: [`WORKSPACE-LAYOUT.md`](WORKSPACE-LAYOUT.md) (root `users/` · `vaults/` · `_job-apps/` · …).  
> Live data today: those root nouns. [`STORAGE.md`](STORAGE.md) documents the layout + the `storage/` dual-run alias.

## Active carryover

- [ ] **Remote containment gate (human credential):** local `main` is verified and committed but cannot
  reach `origin/main`. The push URL is deliberately `github.invalid`, SSH has no jenninexus key, and the
  signed-in GitHub CLI account has **read-only** permission on `jenninexus/pdf-designer`
  (re-checked 2026-09-27). Next action: activate an existing jenninexus write credential, restore the
  real push URL, push `main`, fetch, and prove `origin/main` contains the local tip. Then close
  recovery-queue item `203463379ec2b8182ebf6e4c5e26e695723ea1ba7d4680289274a53f039e35a5`.
- [ ] Select the next accepted slice from the decision-gated and product-evolution work below, then
  give it its own dated, public-safe checklist in `Plans/_Active/`. Acceptance rule: product work
  starts only after one slice is explicitly accepted.

The 2026-09-26 private-preview repair and stage filters are verified and archived in the
completed-history file linked above.

The completed workspace/export organization slice is archived at
[`Plans/_Complete/2026-09-26-roadmap-completed-archive.md#export-library-organization`](../Plans/_Complete/2026-09-26-roadmap-completed-archive.md#export-library-organization):
`_exports/` was the only user-facing generated library at the time, `output/` is explicit automation
scratch, editable sources remain in their document roots, and `applications/` is only a runtime
compatibility alias. That export-library decision was itself superseded 2026-09-27: exports now live
beside their document family (`resumes/<user>/…`, `collages/<project>/`), with `_exports/` as the
fallback — see [`STORAGE.md`](STORAGE.md). The 2026-09-26 carryover plan was closed on 2026-09-27;
its open items are the carryover list above.

### Parked / decision-gated

- [ ] **pywebview shell** — [`Plans/_Complete/2026-07-11-design-hub-parked-phases.md`](../Plans/_Complete/2026-07-11-design-hub-parked-phases.md)
- [ ] **Signed binary channel** — only reopen after a private channel decision; require Valid
  Authenticode plus clean Win10/11 x64 VM proof before any binary listing. Unsigned listing stays off.

### Product evolution carryover

- [ ] **Canvas editor** — drag/drop image tray, canvas presets, layout-family starts, hero selection,
  and text blocks over the same `collage-source.json` used by the CLI.
- [ ] **Collage books** — multi-page project manifest → render pages → `merge_pdfs`.
- [ ] **Desktop output-folder picker** — only in the signed desktop shell; retain editable path text.
- [ ] **Production PyPI decision** — only after TestPyPI proof and an explicit channel decision; the
  GitHub clone remains the complete free product.

### Never

- Auto-submit · invent claims · fork the renderer · commit real vaults · reopen Netflix  
- Force-push history rewrite without explicit human OK + jenninexus auth  
- Recreate `storage/` as a second vault/listing store
