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
| Installable Python package | **Locally proved** | Wheel assets and fresh-venv dry-run passed 2026-08-21; TestPyPI upload needs a human token. |
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
- [ ] Visual-regression check the Hub (`/`, `/recipes`, `/vault`) at 390, 576, 768, 992, 1200, 1400,
  and 1920px against `www-theme-kit/profiles/pdf-designer.json`; add a browser-level test if a
  recurring layout regression appears.

## Distribution — optional, not a blocker for the clone product

- [x] Public-source smoke and local wheel gates exist.
- [ ] Human: create a TestPyPI token, run `python scripts/testpypi-dry-run.py --upload`, and prove a fresh install from TestPyPI.
- [ ] Only after TestPyPI passes: decide whether to publish production PyPI and update the README install path.

## Paid desktop shell — first real implementation phase

- [ ] Owner decision: define the supported first OS and delivery mechanism for the paid shell.
- [ ] Write a small acceptance spec for the first installer: installs/launches the existing Hub on localhost, opens the browser, and leaves all vault data local.
- [ ] Build and test that launcher/installer spike without forking the renderer or introducing a cloud account.
- [ ] Add the guided vault → skills → palette → light/dark export wizard only after the launcher is proven.
- [ ] Keep Gumroad and any paid listing blocked until the installer/wizard has a real, tested user path.
- [ ] After the launcher is proven, choose the paid checkout path: Gumroad as merchant-of-record
  convenience, or a Jenninexus product card with a PayPal checkout button plus owned fulfilment,
  tax, receipt, refund, and download-delivery responsibilities.
- [ ] Define an optional Voice Seed handoff for the wizard: create/import a user's own public-safe
  voice card only after local `characterVoice` + vault `voice` are set. It must remain optional,
  never copy private vault claims or contacts, and never add Voice Seed as a renderer dependency.

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
