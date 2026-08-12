# White-label path — public-only reuse

Shippable story for anyone cloning this repo **without** private vaults, PII, or
studio brand maps. No new themes invented here — the public defaults and presets
are the product.

> **Not the business plan.** Free-vs-paid / GitHub-vs-app direction lives in
> [`PRODUCT.md`](PRODUCT.md). This page is only *how to use the public surface*.

---

## What you need

| Piece | Path | Notes |
|---|---|---|
| **Product entry** | [`examples/resume-studio/`](../examples/resume-studio/) | Marketed résumé-creator front door |
| Example profile + HTML | `examples/profiles/default-resume/` | Reference render + `profile.json` |
| Default theme | `themes/default-resume.{json,css}` | Token SSOT + CSS mirror |
| Audition palettes | `themes/presets/*.json` | Design Hub / `--variants` shopping |
| Palette rule | [`themes/PALETTE-RULES.md`](../themes/PALETTE-RULES.md) | No brown / mustard / lime |
| Brand template (optional) | `examples/brand-design/` | Copy shape only — not real hex maps |
| Protocol seeds | `.claude/commands/*.example.md` | Bare start/wrap/make-* are **not** on GitHub |

You do **not** need `storage/users`, vaults, or `storage/brand-design` to export PDFs.

---

## 5-minute checklist (stranger / fresh clone)

Do this in order. Every step uses **tracked** paths only.

| Step | Command | Pass means |
|---|---|---|
| 1. Install | `pip install -e ".[dev]" && playwright install chromium` | `python -m pdf_tool` prints the hub |
| 2. Smoke | `python scripts/smoke-white-label.py` | exit 0 — QA + light/dark PDF + ATS |
| 3. Hub | `python -m pdf_tool.preview` | http://127.0.0.1:8787/ opens the example |
| 4. (Optional) variants | `python -m pdf_tool.variants examples/profiles/default-resume/default-resume.html` | one light PDF per public palette |

The smoke script:

- runs `check_generation` on `examples/profiles/default-resume/default-resume.html`
- exports light + dark PDFs (2 pages each)
- runs `check_ats` on the light PDF
- copies PDFs into `examples/profiles/default-resume/_exports/` (gitignored)

**If smoke fails on a clean clone, the public product path is broken — fix before anything else.**

---

## Commands

```bash
pip install -e ".[dev]" && playwright install chromium

# One-shot proof (preferred)
python scripts/smoke-white-label.py

# Or step-by-step:
python -m pdf_tool.check_generation examples/profiles/default-resume/default-resume.html
python -m pdf_tool.html_to_pdf examples/profiles/default-resume/default-resume.html
python -m pdf_tool.html_to_pdf examples/profiles/default-resume/default-resume.html --pdf-theme dark

# Palette shopping — one light PDF per public palette
python -m pdf_tool.variants examples/profiles/default-resume/default-resume.html

# Design Hub — browse, swap presets, export
python -m pdf_tool.preview

# Collages from a folder of images
python -m pdf_tool.collage path/to/images --layout auto --png
```

Hub help: `python -m pdf_tool`. Full recipes: [`EXPORTS.md`](EXPORTS.md).
Docs index: [`README.md`](README.md). Agent map: [`AGENTS.md`](../AGENTS.md).
SSOT dashboard: [`SSOT.md`](SSOT.md). Product direction: [`PRODUCT.md`](PRODUCT.md).

---

## Brand maps

- **Stay public:** use `themes/default-resume.json` + `themes/presets/*` (and the Hub swapper).
- **Go private later:** copy `examples/brand-design/` → your local `storage/brand-design/brand-*.json`
  (gitignored). That file becomes the color SSOT for that person/studio — see
  [`STORAGE.md`](STORAGE.md).

Do not put real brand hex into tracked `themes/` or `examples/` unless you intend
them to be public.

---

## What stays private forever

| Surface | Why |
|---|---|
| `storage/users/*.json` | Contact, hard facts, `characterVoice` |
| `storage/<user>/resume-source.json` | Claim vault + application voice |
| `storage/_job-listings/` | Real listings, pay, apply links |
| `storage/brand-design/brand-*.json` | Studio / personal palettes |
| `storage/collages/`, `storage/docs/` | Real image sets + SEGO-only notes |
| `.config/mcp-pdf-designer.json` | Absolute machine paths (use `.example.json`) |
| Bare `make-resume.md` / `make-cover-letter.md` / `make-work-examples.md` | Personal command copies |
| Real PII in any form | Never commit; never move into `examples/` |

The résumé *protocol* (vault → tailor → export) is documented and optional. The
**engine + public themes** are the white-label deliverable.

---

## Related

- [`PREVIEWER.md`](PREVIEWER.md) — Design Hub
- [`THEME-DESIGN.md`](THEME-DESIGN.md) — token contract
- [`VAULT.md`](VAULT.md) — only if you adopt the private claim layer
