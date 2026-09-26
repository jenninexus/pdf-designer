# ROADMAP — pdf-designer

> **This is the durable product backlog and status map.**
>
> | Kind | File |
> |---|---|
> | **Active product slice** | [`Plans/_Active/2026-09-26-private-preview-routing-and-product-carryover.md`](../Plans/_Active/2026-09-26-private-preview-routing-and-product-carryover.md) |
> | **Completed history** | [`Plans/_Complete/2026-09-26-roadmap-completed-archive.md`](../Plans/_Complete/2026-09-26-roadmap-completed-archive.md) |
>
> `/jen:roadmap` resolves here. Plans index: [`Plans/README.md`](../Plans/README.md).
> Session narrative **does not** go in `dev-log-sego.yaml` (frozen 2026-09-08 → [`Plans/_Complete/_archive/`](../Plans/_Complete/_archive/)).
>
> Product UX target: [`WORKSPACE-LAYOUT.md`](WORKSPACE-LAYOUT.md) (root `users/` · `vaults/` · `_job-apps/` · …).  
> Live data today: those root nouns. [`STORAGE.md`](STORAGE.md) documents the layout + the `storage/` dual-run alias.

## Active carryover

- [ ] **Remote containment gate:** local `main` is verified and committed but cannot reach
  `origin/main` while the active GitHub account has read-only repository permission. The exact next
  action and commit evidence are in the active plan.
- [ ] Select the next accepted slice from the decision-gated and product-evolution work below. The
  active plan keeps the acceptance constraints and sequencing in one place.

The 2026-09-26 private-preview repair and stage filters are verified and archived in the
completed-history file linked above.

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
