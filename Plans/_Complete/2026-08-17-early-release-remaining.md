# Complete / superseded plan — Early release remaining (human publication)

> **Superseded 2026-08-21.** Its remaining release, distribution, and desktop-shell work now lives in
> [`../_Active/2026-08-21-standalone-app-remaining.md`](../_Active/2026-08-21-standalone-app-remaining.md).
> X composer completion was recorded at the human's direction; the live URL and `x:notify:jn` remain
> separate follow-up work. This file is historical context, not a working checklist.

**Date:** 2026-08-17 · **Updated:** 2026-08-20 · **Host:** SEGOPC

Engine waves for this SKU are **complete.** Last parked:
[`../_Complete/2026-08-17-hub-examples-storage-retire/Plan.md`](../_Complete/2026-08-17-hub-examples-storage-retire/Plan.md).

Product hub card: `C:\Github\product-design\docs\PDF-DESIGNER.md`.  
Launch copy lives in **Socials** (do not post from this repo unless asked).

---

## Product (locked — already shipped in-repo)

- **One live job folder:** `_job-apps/`. `applications/` is a tracked README redirect.
- **Exports:** `resumes/<id>/_exports/<Track>/` and `resumes/<id>/defaults/`. `--output-dir` is a CLI flag.
- **Clone path:** `examples/` + `themes/` + Jane Example (`users/examples.json`). Personal vaults gitignored.
- **Screenshot pack:** local `jenni-nexus` (Jennifer Nexus, public email, no phone). Keepers in `docs/images/`.

---

## Remaining — human gates only

- [x] **README / stills** — approved 2026-08-19.
- [x] **Blog** — live [`/blog/pdf-designer`](https://jenninexus.com/blog/pdf-designer) (2026-08-19). Clone URL added in local PHP 2026-08-20 (`github.com/jenninexus/pdf-designer`); deploy JN if prod copy still says private.
- [x] **Public GitHub** — [`github.com/jenninexus/pdf-designer`](https://github.com/jenninexus/pdf-designer) flipped **public** 2026-08-19.
- [x] **Patreon paste body** — [live post](https://www.patreon.com/posts/pdf-designer-com-167093475) 2026-08-20. Local [`socials/.../patreon/published/2026-08-14-pdf-designer.md`](../../../socials/content/jenninexus/patreon/published/2026-08-14-pdf-designer.md). Archive refreshed (`npm run patreon:archive:jn`, 616 posts).
- [x] **Discord `#announcements📢`** — SENT 2026-08-20 (landscape promo card). Patreon webhook already fanned `#social-feed` / patrons / supporters — do not re-`--post` those.
- [x] **X composer** — marked complete at the human’s direction 2026-08-21. Capture the live URL and run `x:notify:jn` only with explicit authorization; see the active plan.
- [ ] **Meta composer** — API blocked 2026-08-20 (`FB_PAGE_ACCESS_TOKEN` expired 2026-06-07). Human composer: attach `docs/images/promo-card-landscape.png` (also HTTPS on jenninexus.com). Preflight next time: `npx tsx scripts/auth/fb-auth.ts`.
- [ ] **Short-form** — TikTok + YouTube sisters dated 2026-08-17. Use `docs/images/` (Jennifer Nexus pack + Jane Example). Never real vaults or `_job-apps`.

### Already done (do not re-open)

- [x] HISTORY-SCRUB + force-push (`docs/HISTORY-SCRUB.md`) — BEE must re-clone, not us.
- [x] Private `origin/main` push of clone-safe Hub + launch stills (`3f5ebe8`).
- [x] Public Hub examples, `_job-apps/` sole listing noun, `storage/` directory retired.

### Not launch-blocking (later)

- Gumroad $5 — blocked until installer/wizard exists (`docs/PACKAGING.md`).
- JN.com `/products` store row for this SKU.
- Optional TestPyPI upload.
- Next AI-trainer application: confirm the provider and permitted company line with the user before use.

### Never

- Auto-submit · invent claims · commit vaults · reopen Netflix
- Force-push without HISTORY-SCRUB OK
- Recreate `storage/` as a second vault/listing store
- Post / deploy / `--write` without an explicit human yes
- Show a real résumé, listing, or `brands/` hex in launch media
