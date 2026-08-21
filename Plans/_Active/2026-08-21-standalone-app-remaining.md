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
| Public launch | **Near-close** | GitHub, blog, Patreon, and Discord are live. X has been marked complete at the human’s direction; capture its URL and notify Discord. Meta and short-form remain human/content gates. |
| Paid standalone desktop app | **Not implemented** | The product decision is a thin installer/launcher + guided wizard over the same engine, never a second renderer. No installer or wizard code exists yet. |

Do not turn these rows into invented percentages. The core can be used standalone from a clone today;
the non-developer desktop product is a separate, unstarted implementation phase.

## Now — close the release record

- [x] Record Shade’s Color X application as submitted (owner instruction, 2026-08-21).
- [x] Mark the X composer post complete at the human’s direction (2026-08-21); do **not** invent its URL.
- [ ] Capture the live X URL, move/confirm its Socials published draft, then run `npm run x:notify:jn` from `C:\Github\socials` **only after explicit authorization for that command**.
- [ ] Human: publish the MostlyJenniNexus Meta composer post with `docs/images/promo-card-landscape.png`; record the live URL in Socials.
- [ ] Human/content: make TikTok and YouTube sisters only from the approved `examples` Hub and public Jennifer Nexus / Jane Example assets.

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
