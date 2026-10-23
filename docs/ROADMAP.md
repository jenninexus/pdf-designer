# ROADMAP — pdf-designer

> **Durable product backlog and status map.** Completed work is archived, not restated here.
>
> | Kind | File |
> |---|---|
> | **Active product slice** | `Plans/README.md` → the one dated checklist (local-only) |
> | **Completed history** | `Plans/_Complete/2026-09-26-roadmap-completed-archive.md` (local-only) |
>
> `/jen:roadmap` resolves here. `Plans/` is local-only working context (gitignored, public repo
> rule 2026-09-30); this file is the public backlog.
> `/pdf-start` and `/pdf-wrap` use the active plan plus this roadmap. Do not create or update
> `dev-log.yaml`, `dev-log-sego.yaml`, or `dev-chat.md`; the old YAML is frozen under
> `Plans/_Complete/_archive/` (local-only).
>
> Product UX target: [`WORKSPACE-LAYOUT.md`](WORKSPACE-LAYOUT.md) (root `users/` · `vaults/` · `_job-apps/` · …).  
> Live data today: those root nouns. [`STORAGE.md`](STORAGE.md) documents the layout + the `storage/` dual-run alias.

## Current execution

The exact checklist, blocker evidence, and next action live in the dated checklist named in the
local-only `Plans/README.md`. This file is the durable backlog; completed slices are archived
in `Plans/_Complete/2026-09-26-roadmap-completed-archive.md` (local-only) and are **not** restated here.

**Priority: select one next product-evolution slice from the decision-gated work below.**

**Landed context — do not re-open:**

- **Exports beside their document family** (2026-09-27) — a personal document lands under
  `resumes/<user>/…`, a collage under `collages/<project>/`; `_exports/` is the public/unfiled
  **fallback** only and `output/` is disposable automation scratch. This supersedes the earlier
  centralized `_exports/` decision. Four-surface table: [`STORAGE.md`](STORAGE.md).
- **Reusable specialist packs + local-first QA** (2026-10-15) — per-person specialist claim selections,
  the system-font document policy, deterministic local QA with hash-based receipt reuse, and a
  fail-closed gate for required render errors ([`QA.md`](QA.md)).
- **One workspace across clones** (2026-10-18) — `scripts/private-sync.py` shares the personal roots
  *and* the bare personal commands through a remote you own; `scripts/local-state.py` reports every
  local-only surface (private-sync, command wrappers per runtime, `.config` vs its seeds).
  The portal form-fill contract is in [`APPLICATIONS.md`](APPLICATIONS.md) § *Fill the portal form*.
- **Brand-collab tracking + local mirror** (2026-10-21) — a private `_collabs/` root noun, the
  creator-collab counterpart to `_job-apps/` (deal detail lives in the operator's own hub); and a `lan`
  git remote that mirrors this repo's public history to a machine you own, kept current by
  `.githooks/post-commit`. Machine-local runbook stays out of the repo.

### Parked / decision-gated

- **Commercial desktop shell** — Electron/NSIS has a pre-release implementation; signing, clean-machine
  proof and fulfilment remain release gates, not a live sale. Historical PyWebView exploration:
  `Plans/_Complete/2026-07-11-design-hub-parked-phases.md` (local-only).
- **Signed binary channel** — only after a private channel decision; require valid Authenticode plus
  clean Windows 10/11 x64 VM proof before any binary listing. Unsigned listing stays off.
- **Production PyPI** — only after TestPyPI proof and an explicit channel decision; the GitHub clone
  remains the complete free product.

### Product evolution

- **Canvas editor** — drag/drop image tray, canvas presets, layout-family starts, hero selection, and
  text blocks over the same `collage-source.json` used by the CLI.
- **Collage books** — multi-page project manifest → render pages → `merge_pdfs`.
- **Desktop output-folder picker** — only in a packaged desktop shell; retain editable path text.

### Decks, publishing and vector editing — reference review (2026-10-22)

Planning direction; these features are not yet implemented. The detailed priorities and acceptance
criteria live in the dated checklist named by `Plans/README.md` (local-only).

| Order | Product slice | Completion signal |
|---|---|---|
| 1 | Readable title/header, original compact app icon, accessible mode switcher, New/Open/Recent/Templates/Samples startup options | Legible chrome at Windows scaling; working modes; current templates retained |
| 2 | Presentation recipes/masters and business story starters: pitch, proposal, kickoff, status, case study, training; slide/page sorter | Editable source, reorder/undo, correct slide dimensions, multiple palettes and deck-specific fit QA |
| 3 | Persistent editor with undo/autosave, true side-by-side page editing, publishing masters/guides/styles/text flow, SVG and line-art editing | Edit both pages and actual vector geometry; save/reopen and export without data loss |
| 4 | PDF organization/review; speaker notes, presentation and handouts afterward | Real PDF persistence and text/link/annotation preservation |

References: [DeckCraft](https://getartcraft.com/apps/deckcraft),
[its repository](https://github.com/storytold/deckcraft),
[PdfCraft](https://getartcraft.com/apps/pdfcraft),
[its repository](https://github.com/storytold/pdfcraft), and Serif Affinity Designer/Publisher.
The supplied screenshots and source documentation inspire concepts; competitor runtime behavior was
not tested. Two-up reading is distinct from editable spreads. PowerPoint-style layouts are distinct
from editable PPTX exchange, which needs separate round-trip fixtures and compatibility decisions.
Keep the existing HTML/Chromium renderer, templates, palette system, private workspace split and
Letter career-document contracts. Use original visuals and check code/brand licenses before reuse.
OCR, signing, secure redaction, animation/media and press-ready color need separately accepted scopes.

### Never

- Auto-submit · invent claims · fork the renderer · commit real vaults · reopen closed applications without an explicit request
- Force-push history rewrite without explicit human OK + jenninexus auth  
- Recreate `storage/` as a second vault/listing store
