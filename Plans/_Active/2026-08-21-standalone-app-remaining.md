# Active plan — Standalone app release path

**Date:** 2026-08-21 · **Host:** SEGOPC · **Status:** core toolkit shipped; distribution and desktop shell remain.

This is the one active plan. It replaces the completed launch handoffs in
[`../_Complete/2026-08-17-early-release-remaining.md`](../_Complete/2026-08-17-early-release-remaining.md)
and
[`../_Complete/2026-08-20-pdf-designer-remaining-sisters/Plan.md`](../_Complete/2026-08-20-pdf-designer-remaining-sisters/Plan.md).

## Honest completion picture

| Surface | Status | Evidence / boundary |
|---|---|---|
| Local-first engine + Design Hub | **Shipped** | HTML→PDF, variants, collage, vault/ATS/palette/overflow guards, public examples, and the localhost Hub are in `main`. |
| Public GitHub clone experience | **Shipped, regression-gated** | `scripts/smoke-white-label.py` passed 2026-08-21: public-only QA, light/dark export, and ATS parsing. |
| Installable Python package | **TestPyPI proved** | Wheel assets, upload, fresh TestPyPI install, and packaged `check_generation` passed 2026-08-21. |
| Public product record | **Shipped** | Public GitHub clone, clone-safe Hub examples, and the blog walkthrough exist. Social publication records are owned by `C:\Github\socials\Plans\_ACTIVE\2026-08-10-jn-agency-socials-sequence\Plan.md`, not this engineering plan. |
| Paid standalone desktop app | **Not implemented** | The product decision is a thin installer/launcher + guided wizard over the same engine, never a second renderer. No installer or wizard code exists yet. |

Do not turn these rows into invented percentages. The core can be used standalone from a clone today;
the non-developer desktop product is a separate, unstarted implementation phase.

## Public examples and privacy boundary

- [x] Keep the fictional Jane Example cards (`users/examples.json`, `vaults/examples.json`,
  `profiles/examples.json`) tracked so a fresh clone and the Hub demonstrate every document kind.
- [x] Replace the broad `_job-apps/_template/` smoke exception with named public seeds; remove the
  provider-specific material from the public tree. Real listings, provider records, names, phone numbers,
  and submission evidence remain local only.
- [x] Make `users/<you>.json#characterVoice` the one person-level voice-design area in the public
  seed; the vault is the sole application-prose layer and profiles only point at it.
- [ ] When adding a new public Hub feature, add a fictional Jane Example artifact (or a clearly
  labelled generic template) and extend the public-example coverage test in the same change.

## Responsive Hub contract

- [x] Confirm the shared numeric scale comes from `www-theme-kit/scss/_breakpoint-tokens.scss`,
  while `src/pdf_tool/static/hub.css` owns this app's breakpoint and nav-switch behavior. The MCP
  breakpoint file is a cache/index only.
- [x] At the drawer switch, hide empty desktop groups and their divider borders; keep refresh/close
  compact; make drawer and search dismiss on outside click as well as Escape.
- [x] Visual/regression check the Hub (`/`, `/recipes`, `/vault`) at 390, 576, 768, 992, 1200, 1400,
  and 1920px against `www-theme-kit/profiles/pdf-designer.json` (2026-08-21). Fixed document-root
  overflow from the closed drawer and restored the 768px desktop hamburger boundary.
- [x] Replace the compact top-right menu glyph with Font Awesome Free 6.7.2 `bars-staggered` across
  Library, Recipes, and Vault (2026-08-21). The local SVG keeps the control offline and visually
  distinct from the drawer's close action.

## Distribution — optional, not a blocker for the clone product

- [x] Public-source smoke and local wheel gates exist.
- [x] TestPyPI: `pdf-designer 0.4.0` uploaded and passed the fresh-install + packaged `check_generation` proof on 2026-08-21.
- [ ] Only after TestPyPI passes: decide whether to publish production PyPI and update the README install path.

## Paid desktop shell — first real implementation phase

- [ ] Owner decision: define the supported first OS and delivery mechanism for the paid shell.
- [x] Write a small acceptance spec for the first launcher: starts the existing Hub on localhost, opens the browser, and leaves all vault data local. See [`docs/WINDOWS-LAUNCHER.md`](../../docs/WINDOWS-LAUNCHER.md).
- [x] Build and test the Windows launcher spike without forking the renderer or introducing a cloud account.
- [ ] Add the guided vault → skills → palette → light/dark export wizard only after the launcher is proven.
- [ ] Keep Gumroad and any paid listing blocked until the installer/wizard has a real, tested user path.
- [ ] After the launcher is proven, choose the paid checkout path: Gumroad as merchant-of-record
  convenience, or a Jenninexus product card with a PayPal checkout button plus owned fulfilment,
  tax, receipt, refund, and download-delivery responsibilities.
- [x] Define the optional Voice Seed handoff contract in [`docs/VOICE-SEED-HANDOFF.md`](../../docs/VOICE-SEED-HANDOFF.md): create/import a user's own public-safe voice card only after local `characterVoice` + vault `voice` are set. It remains optional, never copies private vault claims or contacts, and never adds Voice Seed as a renderer dependency.

## Guardrails

- Never post, deploy, or use `--post` without explicit human authorization.
- Never auto-submit applications or commit private vaults, job listings, brands, PDFs, or bare commands.
- Launch media uses only public Jennifer Nexus / Jane Example assets — never real vaults, résumés, listings, or brand hex.
- The desktop shell starts the existing `pdf_tool.preview`; it does not reimplement HTML/PDF rendering.

## Verification record

Run before declaring the public toolkit healthy after engine or packaging changes:

```powershell
python scripts/smoke-white-label.py
python scripts/check-wheel-assets.py
python scripts/testpypi-dry-run.py
```

Related: [`../../docs/PRODUCT.md`](../../docs/PRODUCT.md) ·
[`../../docs/PACKAGING.md`](../../docs/PACKAGING.md) ·
[`../../docs/PREVIEWER.md`](../../docs/PREVIEWER.md).

## Autonomous completion run — 2026-08-21

### Done when

- [ ] The production-PyPI decision is documented with its evidence and release boundary.
- [x] A Windows launcher starts the existing local Hub, opens the browser, and keeps all data local. Acceptance record: [`docs/WINDOWS-LAUNCHER.md`](../../docs/WINDOWS-LAUNCHER.md).
- [ ] A guided local wizard covers vault → skills → palette → dual export without a second renderer.
- [ ] The optional Voice Seed flow presents a redacted card for approval and never needs a network dependency.
- [ ] The changed surfaces have automated and observable verification, then are committed and pushed as authorized.

### Task checklist

- [ ] Audit existing launcher, installer, wizard, and release mechanisms.
- [x] Implement the smallest Windows distribution path around `pdf_tool.preview` (`scripts/launch-design-hub.ps1`).
- [ ] Implement the guided wizard and bounded Voice Seed handoff.
- [ ] Verify the distribution and wizard paths; update release docs and plan.
- [ ] Commit explicit in-scope paths and push the authorized branch.

### Assumptions

- The first paid-shell target is Windows, because this is the requested platform and the active work occurs on Windows.
- Production PyPI is deferred unless an existing production credential and public-release gate make publication independently verifiable; TestPyPI remains the proved distribution rehearsal.
- The wizard is a Design Hub surface over existing local data and renderer commands, never a new renderer or cloud account.

### Evidence

- VERIFIED — 2026-08-21 TestPyPI uploaded `pdf-designer 0.4.0`, fresh-installed it outside the checkout, and passed the packaged `check_generation` gate.
- UNVERIFIED — Windows distribution and guided-wizard implementation have not yet been inspected in this run.

### Deferred

- Production PyPI publication itself is outward-facing and remains separate from the reversible production-PyPI decision unless its release conditions are fully met.
