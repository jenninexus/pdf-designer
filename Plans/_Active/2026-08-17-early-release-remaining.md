# Active plan — Early release remaining (Patreon → public GitHub → blog / Discord / short-form)

**Date:** 2026-08-17 · **Host:** SEGOPC  
**Prior waves (complete):**  
[`../_Complete/2026-08-13-intuitive-workspace-product.md`](../_Complete/2026-08-13-intuitive-workspace-product.md) ·  
[`../_Complete/2026-08-13-launch-ready-workspace.md`](../_Complete/2026-08-13-launch-ready-workspace.md)

Product hub card: `C:\Github\product-design\docs\PDF-DESIGNER.md`.  
Launch copy lives in **Socials** (do not post from this repo).

---

## Product decision (locked)

**One live job folder:** `_job-apps/`. `applications/` is a tracked README redirect
only. Personal listings stay gitignored. Public clones see the noun +
`_job-apps/_template/README.md` pointing at `examples/_job-listings/`.

**Exports:** `resumes/<id>/_exports/<Track>/` (per job) and `resumes/<id>/defaults/`
(go-to pack). `--output-dir` is a **CLI flag**, not a repo folder.

---

## Remaining (this file)

### Human gates (do not skip)

- [x] **HISTORY-SCRUB** — executed 2026-08-18; force-push `8c1c631` on origin/main. BEE must re-clone. (`docs/HISTORY-SCRUB.md`.)
- [ ] **Patreon early** — paste [`socials/content/jenninexus/patreon/drafts/2026-08-14-pdf-designer.md`](../../../socials/content/jenninexus/patreon/drafts/2026-08-14-pdf-designer.md). Honest while GitHub is still private. Do not claim the repo is public.
- [ ] **Public GitHub** — only after scrub (or an explicit "private-repo Patreon is enough for now"). Then add the clone URL to Patreon / README tip footer.
- [ ] **Blog** — [`socials/content/jenninexus/devlogs/drafts/2026-08-14-pdf-designer.md`](../../../socials/content/jenninexus/devlogs/drafts/2026-08-14-pdf-designer.md). `site:publish` dry-run first; `--write` / SSH / deploy need a separate yes.
- [ ] **Discord `#announcements??`** — [`socials/content/jenninexus/discord/drafts/2026-08-17-announcements-pdf-designer.json`](../../../socials/content/jenninexus/discord/drafts/2026-08-17-announcements-pdf-designer.json). Manual. Patreon Publish already fans `#social-feed` / patrons / supporters — do not double-post there.
- [ ] **Short-form (after public-safe Hub stills)** — TikTok + YouTube sisters dated 2026-08-17. Capture only `python -m pdf_tool.preview examples` + `docs/pdf-designer-overview.html`. Never vaults or `_job-apps`.

### Later engineering (not launch-blocking)

- [x] Dual-run smoke on root nouns only, then retire the `storage/` **directory** (private provider template → `_job-apps/_template/private provider-ai-fellowship.md`; private font → `brands/fonts/`).
- [x] **`_job-apps/` sole listing noun** — `applications/` is a tracked README redirect only; workspace + docs no longer point at `storage/_job-listings/`.
- [x] **Public Hub examples** — `python -m pdf_tool.preview examples` shows resume, cover letter, letter, work samples, collage, and gallery; `examples/` sorts first in each kind.
- [x] **Hub not-found** — scan excludes `_archive` + `*.template.html`; `resolve_preview_file` maps stale `/storage/<user>/…` to `resumes/<user>/…`.
- [ ] Gumroad $5 — blocked until installer/wizard exists. Wheel + `testpypi-dry-run.py` exist; the paid SKU is a **desktop installer that launches Design Hub** (not started — see PACKAGING.md). Listing brief stays draft.
- [ ] JN.com `/products` store page (site repo). **Hub card already exists:** `C:\Github\product-design\docs\PDF-DESIGNER.md`.
- [ ] Optional TestPyPI upload — not required for clone launch.
- [ ] Next AI-trainer application: include `emp-private provider-ai`; company line exactly **private provider AI Fellowship**.

### Never

- Auto-submit · invent claims · commit vaults · reopen Netflix  
- Force-push without HISTORY-SCRUB OK  
- Recreate `storage/` as a second vault/listing store  
- Post / deploy / `--write` without an explicit human yes  
- Show a real résumé, listing, or `brands/` hex in launch media
