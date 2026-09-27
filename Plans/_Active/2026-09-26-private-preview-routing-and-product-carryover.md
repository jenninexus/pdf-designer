# Private preview routing and product carryover

**Status:** Active — canonical workspace/output organization review accepted 2026-09-26; remote
containment still awaits write access
**Public safety:** no names, employers, vault claims, machine paths, or private media are recorded here.

## Current task contract — canonical workspace and output map

- **Outcome:** one professional public/local/private folder model, with one canonical destination for
  personal deliverables and matching Design Hub filters, docs, ignore rules, commands, and profile data.
- **Scope:** repository folder ownership; `output/` versus `_exports/`; private source roots; application
  records; Design Hub discovery/filter labels; public examples; tracked/local commands and generated
  adapters; the pdf-designer theme-kit profile. Existing private payload content is not rewritten.
- **Source authority:** `C:\Github\pdf-designer` `main` at `2d35f01`, plus
  `C:\Github\www-theme-kit\profiles\pdf-designer.json` for the consumer profile.
- **Acceptance evidence:** path/reference inventory; ignore-boundary probes; focused preview tests;
  documentation/link checks; command-adapter parity; browser verification of root/profile/kind filters.
- **Irreversible effects:** none planned. No private payload deletion, destructive Git operation,
  submission, deployment, or publication is authorized by this slice.
- **Observable handoff:** the running Design Hub library at `http://127.0.0.1:8787/` and the canonical
  map in `docs/PUBLIC-LOCAL-SPLIT.md` / `docs/STORAGE.md`.

### Organization refinement outcome — completed 2026-09-26

- [x] Make `_exports/` the one user-facing generated-deliverables library for public examples and
  private profiles: `_exports/<profile>/<kind>/<project-or-application>/`.
- [x] Reserve `output/` for explicit automation, smoke-test, and disposable build scratch; it is no
  longer the engine default and is not a Design Hub library root.
- [x] Keep editable sources in `examples/`, `resumes/`, `collages/`, and `_job-apps/`; keep identity,
  claims, presentation, and brand data in `users/`, `vaults/`, `profiles/`, and `brands/`.
- [x] Retire tracked `applications/` scaffolding; retain it only as a runtime compatibility alias to
  `_job-apps/`, with the entire alias ignored.
- [x] Show the friendly label **Exports** in the Design Hub while preserving the physical `_exports`
  path in file controls and nested locations.
- [x] Align public docs/examples, local commands, generated Codex/Agents adapters, ignore boundaries,
  desktop seed, and `www-theme-kit/profiles/pdf-designer.json`.
- [x] Verify the decision through the full Python suite, clone-safe smoke, wheel gate, desktop seed,
  JSON parsing, adapter parity, and live mobile/desktop browser checks.

## Accepted slice

- [x] Keep local profiles, vaults, résumés, job applications, collages, brands, and exports gitignored.
- [x] Restore private collage source images beside the HTML that references them; retain `_exports` as
  deliverables rather than the only copy of source media.
- [x] Correct the two private favorite-page paths that traversed above their project image folders.
- [x] Turn the selected-document kind, profile, and root-folder pills into accessible library filters.
- [x] Complete automated, HTTP, and browser-level verification.
- [ ] Push verified local `main` to `origin/main` after an authorized `jenninexus` credential becomes
  active; fetch and prove the remote contains the wrap commit before closing this gate.
- [ ] Select the next accepted carryover slice before implementation; do not start a decision-gated
  item without its named decision.

## Session wrap — 2026-09-26

| Phase | Outcome | Artifact |
|---|---|---|
| 1 — repair private sources | Restored nine ignored Martian PNG source copies and corrected two favorite-page relative-path sets. | local/private |
| 2 — make stage chips useful | Kind, profile, and root-folder pills now scope the left library and retain the selected preview. | `3ab3034` |
| 3 — consolidate plans/docs | Completed roadmap history moved out of the live backlog; one carryover plan remains. | tracked |
| 4 — verify | 119 tests, white-label smoke, wheel gate, 21 HTTP assets, browser dimensions, and three filter transitions passed. | local evidence |
| 5 — deliver | Commit created; push correctly failed because `MonoFinity` has `READ` permission on `jenninexus/pdf-designer`. | recovery queue |

### Reflection

- **Mode:** friction + leverage.
- **Observation:** ignored private HTML remained discoverable while the media it referenced existed only
  in `_exports`; two shallower favorite pages also inherited deeper candidate-page relative paths.
- **Root cause (high):** source and deliverable lifecycles were treated as interchangeable, and path
  depth was not verified from the generated page's directory.
- **Landed now:** `.memory/lesson-private-collage-source-assets.md` defines source placement, copy-not-move
  export behavior, and the HTTP plus `naturalWidth` closeout guard.
- **Validated by:** 21/21 HTTP responses and 21/21 nonzero browser image dimensions. The
  [W3C button pattern](https://www.w3.org/WAI/ARIA/apg/patterns/button/) also confirms `aria-pressed`
  is the appropriate exposed state for these persistent filter buttons.
- **Expected signal:** a comparable collage wrap finds source media beside its HTML and fails verification
  before any broken card is accepted.

### Synabrain review

- `ctxreq_c509e490a84b44bdb8bbef6fc01b5d21`: grounded and useful for recovering the prior Design Hub
  public/private routing decisions.
- Delegated review `ctxrev_4e10c624050c464bb9291b4113548f52` was resolved without indexing ignored
  application data; replay `ctxreq_e0cb8c9084eb45198b46fde945f79782` was grounded and its focused
  privacy/scoping tests passed 6/6. Synabrain containment: `37d8492f` on its `origin/main`.
- This project intentionally has no live `dev-log-sego.yaml`; the roadmap plus this plan are the handoff.

## Carryover — next accepted slices

### Decision-gated (do not start without the named decision)

- [ ] pywebview shell — remains parked; see
  [`../_Complete/2026-07-11-design-hub-parked-phases.md`](../_Complete/2026-07-11-design-hub-parked-phases.md).
- [ ] Signed binary channel — reopen only after a private-channel decision; require valid Authenticode
  and clean Windows 10/11 x64 VM evidence. Do not list an unsigned executable.
- [ ] Production PyPI — proceed only after TestPyPI proof and an explicit channel decision; the GitHub
  clone remains the complete free product.

### Product evolution

- [ ] Canvas editor over the existing `collage-source.json`: drag/drop tray, presets, layout-family
  starts, hero selection, text blocks, and the existing export endpoint.
- [ ] Collage books: multi-page manifest → render pages → `merge_pdfs`.
- [ ] Desktop output-folder picker only inside the signed shell; retain editable path text.

## Changed-files ledger

Tracked/public-safe:

- `.gitignore`
- `.memory/README.md`
- `.memory/lesson-private-collage-source-assets.md`
- `docs/PREVIEWER.md`
- `docs/ROADMAP.md`
- `Plans/README.md`
- `Plans/_Active/2026-09-26-private-preview-routing-and-product-carryover.md`
- `Plans/_Complete/2026-09-26-roadmap-completed-archive.md`
- `src/pdf_tool/preview.py`
- `src/pdf_tool/static/hub.css`
- `tests/test_preview_workspace.py`

Personal/local and intentionally ignored:

- restored private image payload under `collages/martian-collage/`
- corrected private HTML under `collages/meet-jenni-bot/faves/` and `collages/syn-themes/faves/`
- canonical personal `/jen:roadmap` command and its generated user-level adapter

## Acceptance evidence

- Every referenced local image on the affected Martian, Meet Jenni Bot, and Syn Themes pages resolves.
- Browser inspection shows nonzero image dimensions and no broken-image placeholders.
- Clicking each stage pill updates the matching header control and scopes the left library without
  replacing the selected preview.
- Private paths remain ignored; public tests and clone-safe smoke pass.
- Verification: 21/21 affected image requests returned HTTP 200; browser dimensions were nonzero for
  all 21; 119 tests passed; public white-label smoke and wheel-asset gate passed.

## Friction record

- **Observation:** gallery layouts rendered filenames instead of images.
- **Cause / confidence:** high — nine source PNGs existed only in `_exports`; two favorite pages used
  `../../` where their assets live under `../images/`.
- **Effect:** private documents were discoverable but visually broken in the Hub.
- **Remedy / verification:** restore source placement, correct relative paths, test direct HTTP routes,
  and inspect image `naturalWidth` in the running Hub before closeout.

## Organization refinement wrap — 2026-09-26

| Phase | Outcome | Artifact |
|---|---|---|
| 1 — decide ownership | `_exports/` now owns deliberate deliverables; `output/` owns disposable automation scratch. | `docs/PUBLIC-LOCAL-SPLIT.md` · `docs/STORAGE.md` |
| 2 — wire the engine and Hub | Default export routing and every visible root label now agree on **Exports**. | `src/pdf_tool/paths.py` · `src/pdf_tool/preview.py` |
| 3 — remove duplicate concepts | Tracked `applications/` scaffolding and the obsolete reverse-migration script were removed. | `.gitignore` · `_job-apps/README.md` |
| 4 — align every surface | Public examples, commands/adapters, desktop seed, docs, AGENTS, memory, and theme-kit profile use the same map. | tracked + local surfaces |
| 5 — verify | 120 tests, smoke, wheel, seed, JSON, adapter, and responsive browser gates passed. | local evidence |

### Changed-files ledger — organization refinement

Tracked in `pdf-designer`:

- `.claude/commands/make-resume.example.md`
- `.config/mcp-pdf-designer.example.json`
- `.gitignore`
- `.memory/README.md`
- `.memory/lesson-defaults-export-beside-html.md`
- `.memory/lesson-exports-are-one-user-facing-root.md`
- `.memory/lesson-flag-looking-output-dir.md`
- `.memory/lesson-one-checkout-privacy-is-gitignore.md`
- `.memory/lesson-output-is-repo-root.md`
- `.memory/lesson-scaffold-readme-must-not-win-path-resolution.md`
- `.memory/lesson-work-samples-footer-row-false-collision.md`
- `AGENTS.md`
- `Plans/_Active/2026-09-26-private-preview-routing-and-product-carryover.md`
- `README.md`
- `_exports/README.md`
- `_job-apps/README.md`
- `applications/README.md` (removed)
- `docs/ARCHITECTURE.md`
- `docs/EXPORTS.md`
- `docs/GETTING-STARTED.md`
- `docs/LICENSING-NOTES.md`
- `docs/PACKAGING.md`
- `docs/PREVIEWER.md`
- `docs/PUBLIC-LOCAL-SPLIT.md`
- `docs/PUBLIC-RELEASE-AUDIT.md`
- `docs/QA.md`
- `docs/README.md`
- `docs/STORAGE.md`
- `docs/THEME-DESIGN.md`
- `docs/WORKSPACE-LAYOUT.md`
- `examples/_job-listings/example-application/Company.example.md`
- `examples/_job-listings/example-application/application.example.json`
- `examples/_job-listings/example-application/theme.example.json`
- `examples/_job-listings/tracker.example.json`
- `examples/brand-design/README.md`
- `examples/brand-design/brand-example.json`
- `examples/profiles/default-collage/collage-source.example.json`
- `examples/profiles/default-collage/profile.json`
- `examples/profiles/default-resume/profile.example.json`
- `examples/profiles/default-resume/profile.json`
- `examples/profiles/default-resume/resume-source.example.json`
- `examples/profiles/default-resume/user.example.json`
- `examples/resume-studio/README.md`
- `layouts/README.md`
- `output/README.md`
- `scripts/migrate-root-output.py` (removed)
- `scripts/smoke-white-label.py`
- `scripts/sync-desktop-seed.py`
- `src/pdf_tool/check_pagefit.py`
- `src/pdf_tool/collage.py`
- `src/pdf_tool/html_to_pdf.py`
- `src/pdf_tool/paths.py`
- `src/pdf_tool/preview.py`
- `src/pdf_tool/static/hub.css`
- `src/pdf_tool/variants.py`
- `tests/test_paths.py`
- `tests/test_preview_workspace.py`
- `themes/GENERATION-RULES.md`
- `themes/PALETTE-RULES.md`
- `themes/default-resume.json`
- `themes/presets/README.md`

Tracked in `www-theme-kit`:

- `profiles/pdf-designer.json`

Local and intentionally ignored:

- `.claude/commands/README.md`, `.claude/commands/make-resume.md`,
  `.claude/commands/make-work-examples.md`, `.claude/commands/pdf-wrap.md`
- `.codex/README.md`, generated `.codex/skills/` and `.agents/skills/` command adapters
- `.config/mcp-pdf-designer.json`
- `docs/CHANNELS.local.md`

### Acceptance evidence — organization refinement

- `pytest`: 120 passed.
- `python scripts/smoke-white-label.py`: public light/dark generation, 10/10 generation checks,
  and ATS guard passed; explicit scratch copies stayed under `output/examples/`.
- `python scripts/check-wheel-assets.py`: 89 wheel files, no PDF/image payloads.
- `python scripts/sync-desktop-seed.py --output output/desktop-seed-check`: 66 public files and no
  `applications/` scaffold; the disposable check directory was removed afterward.
- Command wrapper parity: 8 Codex adapters and 8 Agents adapters, zero problems.
- Live Design Hub: export cards, stage badges, and folder menu expose **Exports**; at 390×844 the
  drawer toggle is present and desktop folder control hidden, while at 1400×900 the inverse holds.
- `www-theme-kit/profiles/pdf-designer.json` parses as JSON and records the canonical library map.

### Reflection — organization refinement

- **Mode:** friction + leverage.
- **Observation:** the engine default wrote deliberate exports to `output/`, while the Hub indexed
  `_exports/`; a successful export could therefore disappear from the user's working library.
  **Cause / confidence:** high — output ownership was split across defaults, docs, and UI vocabulary.
  **Effect:** ambiguous filing, duplicate-folder temptation, and harder artifact discovery.
  **Remedy status:** enacted. **Action:** route defaults through `export_root()`, reserve `output/` for
  opt-in scratch, document one map, and add routing/UI regressions. **Verified:** full suite, smoke,
  seed, and browser checks above.
- **Observation:** the first UI pass changed one label path but a change handler restored raw
  `_exports`. **Cause / confidence:** high — two independent DOM update paths formatted the root.
  **Effect:** inconsistent terminology after interaction. **Remedy status:** enacted. **Action:** use
  `folderDisplayName()` in both paths and exercise the interaction live. **Verified:** the header and
  stage badge both remain **Exports** after selection.
- **Observation:** the command-adapter README referenced a stale sync-script location.
  **Cause / confidence:** high — local documentation lagged the shared generator move.
  **Effect:** one failed discovery path before the authoritative sync script was found.
  **Remedy status:** enacted. **Action:** correct the local README and regenerate both adapter trees.
  **Verified:** 8/8 parity for Codex and Agents.
- **Observation:** the required Synabrain wrap audit timed out twice, and the performance-review write
  timed out as well; service status was healthy but orchestrated restart failed with `cmd.exe ENOENT`.
  **Cause / confidence:** low — the API process is present, but either the activity query is stalled or
  the service-control launcher is broken. **Effect:** this session's request IDs could not be graded or
  linked. **Remedy status:** partial. **Action:** recorded the exact failure here after two bounded
  retries and one restart attempt. **Verified:** failures reproduced; PDF Designer verification was
  independent and remained green. **Why unresolved:** Synabrain activity/restart infrastructure is
  outside this repository and its own review endpoint was unavailable.
- **Observation:** responsive reloads could abandon an in-flight `/api/version` response and print a
  `ConnectionAbortedError` traceback even though the Hub stayed healthy. **Cause / confidence:** high —
  the stdlib handler wrote after the local browser closed the socket. **Effect:** noisy runtime logs
  obscured actionable errors. **Remedy status:** enacted. **Action:** `_send()` now ignores only the
  three normal client-disconnect exceptions. **Verified:** focused preview tests and repeated live
  reloads complete without a new traceback.

### Synabrain review — organization refinement

- The initial context gate returned useful project passages and reinforced the root-noun/privacy
  model; the strongest future-facing improvement was landed as
  `.memory/lesson-exports-are-one-user-facing-root.md` plus executable routing/UI tests.
- The mandatory request ledger became unavailable during wrap. Two
  `get_recent_context_requests` calls and one `submit_context_performance_review` call each timed out
  after 60 seconds, so `activity_health: unavailable`; no false review ID or link is recorded.
