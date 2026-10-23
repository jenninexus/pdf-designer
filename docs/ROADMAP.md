# ROADMAP — pdf-designer

> **This is the durable product backlog and status map.**
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

The exact checklist, blocker evidence, and next action live in
the dated checklist named in the local-only `Plans/README.md`. The current accepted
organization slice completed on 2026-09-27. The October15 slice adds reusable per-person specialist
selections, system-font document policy, local-first deterministic QA with receipt reuse, and a
fail-closed gate for required render errors. Private applicant data stays out of the public product.
Current local work, if any, is named by the plan index; the commercial release queue remains below.
The 2026-10-18 slice made two clones work as one workspace. `scripts/private-sync.py` now shares the
personal commands too, and `scripts/local-state.py` checks every local-only surface: private-sync,
command wrappers across agent runtimes, and `.config` against its seeds. `/pdf-start` and `/pdf-wrap`
run both. [`APPLICATIONS.md`](APPLICATIONS.md) § *Fill the portal form* sets the upload order and the
answer-sheet contract for agent-assisted portal applications.

After that slice, priority remains:

1. Select one next product-evolution slice from the decision-gated work below. The old public-push
   blocker is resolved: October15 mainline delivery was verified, and the historical tip has an
   identical-tree integrated replacement. Recovery details stay in the private recovery queue.

The 2026-09-26 private-preview repair and stage filters are verified and archived in the
completed-history file linked above.

The completed workspace/export organization slice is archived at
`Plans/_Complete/2026-09-26-roadmap-completed-archive.md` § Export library organization (local-only).
Its original centralized `_exports/` decision was superseded 2026-09-27: exports now live beside
their document family (`resumes/<user>/…`, `collages/<project>/`), with `_exports/` as the fallback.
See [`STORAGE.md`](STORAGE.md).

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
