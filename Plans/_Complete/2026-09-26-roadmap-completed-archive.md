# Roadmap completed archive — through 2026-09-26

This public-safe archive removes finished work from the live backlog. Detailed implementation evidence
remains in Git history, the linked completed plans, and the owning docs.

## Workspace and privacy model

- Root duplicates were archived and legacy `storage/` was retired; the dual-run URL resolver remains.
- `_job-apps/` became the one live application noun; only generalized seeds are public.
- Repository history was scrubbed, the clone-safe Hub was published, and the GitHub product became public.
- Deliberate exports were consolidated under `_exports/<profile>/<kind>/`; `output/` is explicit
  automation/test scratch, and source HTML stays under its public/private authoring roots. Full
  evidence: [Export library organization](#export-library-organization) below.
- Personal commands stay local; only `.example.md` protocol seeds ship.

## Public product and Design Hub

- Clone-safe Resume Studio, fresh-clone smoke, wheel gates, and the browser/PDF overview landed.
- Jane Example covers the public document kinds; profile and folder filters discover live private roots
  only when those ignored files exist locally.
- Drawer, layout, letterhead, compact/off-canvas chrome, mobile sheet behavior, and vault-import wizard
  landed. See [`2026-08-26-hub-compact-offcanvas.md`](2026-08-26-hub-compact-offcanvas.md).
- Workspace layout, public/local architecture, and docs ownership were consolidated under `docs/`.
- Private collage source routing was repaired without weakening git privacy, and the selected-document
  kind/profile/root pills became working library filters (2026-09-26). Browser verification covered all
  21 affected images plus the three filter transitions.

## Document quality and distribution decisions

- Jenni and Shade résumé, cover-letter, and work-example layouts were checked against the layout system.
- Azure signing and paid fulfilment were explicitly held. The supported public channel remains the free
  GitHub product with an optional tip; unsigned executable listings remain prohibited.
- The previous release/layout closeout remains at
  [`2026-08-25-remaining-release-and-document-layout.md`](2026-08-25-remaining-release-and-document-layout.md).

## Export library organization

Completed 2026-09-26:

- `_exports/` is the one user-facing generated-deliverables library. Private output uses
  `_exports/<profile>/<kind>/<project-or-application>/`; public example output uses
  `_exports/examples/`; unknown one-offs use `_exports/unfiled/`.
- `output/` is explicit disposable automation, smoke-test, and build scratch. It is not the engine
  default and is not indexed as a Design Hub document library.
- Editable source stays in `examples/`, `resumes/`, `collages/`, and `_job-apps/`. Person, claim,
  presentation, and brand data stays in `users/`, `vaults/`, `profiles/`, and `brands/`.
- `applications/` is a runtime compatibility alias only; its tracked scaffold and the obsolete reverse
  migration script were removed.
- The Hub shows **Exports** while physical paths remain `_exports/...`; both label-update paths have
  interaction coverage.
- Public docs/examples, local commands, 8 Codex + 8 Agents adapters, ignore rules, desktop seed, and
  `www-theme-kit/profiles/pdf-designer.json` now agree on the map.
- Verification: 120 full-suite tests; 22 focused preview tests after the client-disconnect log fix;
  white-label light/dark + 10/10 generation + ATS smoke; 89-file wheel gate; 66-file desktop seed;
  mobile/desktop live browser checks and repeated clean reloads.
- Theme-kit commits `6465819` and `d836cab` landed on its `origin/main`. PDF Designer commits
  `a39eda8`, `6c639a3`, and the plan-closeout successors remain preserved on clean local `main`; the
  active plan owns the external credential/publication gate.

Reflection: the former engine-default `output/` versus Hub-indexed `_exports/` split caused successful
exports to disappear from the working library. `export_root()`, routing/UI tests, and
`.memory/lesson-exports-are-one-user-facing-root.md` now guard the decision. A stale local command-sync
entry point was corrected and both adapter trees were regenerated. Synabrain's required request audit
and review write timed out during wrap; no false request or review ID was recorded.
