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
| Example profile + HTML | `examples/profiles/default-resume/` | Reference render + `profile.json` |
| Default theme | `themes/default-resume.{json,css}` | Token SSOT + CSS mirror |
| Audition palettes | `themes/presets/*.json` | Design Hub / `--variants` shopping |
| Palette rule | [`themes/PALETTE-RULES.md`](../themes/PALETTE-RULES.md) | No brown / mustard / lime |
| Brand template (optional) | `examples/brand-design/` | Copy shape only — not real hex maps |

You do **not** need `storage/users`, vaults, or `storage/brand-design` to export PDFs.

---

## Commands

```bash
pip install -e . && playwright install chromium

# Guard colors before every export
python -m pdf_tool.check_palette examples/profiles/default-resume/*.html

# Light (ATS) + dark branded — same pagination
python -m pdf_tool.html_to_pdf path/to/doc.html
python -m pdf_tool.html_to_pdf path/to/doc.html --pdf-theme dark

# Palette shopping — one light PDF per public palette
python -m pdf_tool.variants path/to/doc.html
# or: python -m pdf_tool.html_to_pdf path/to/doc.html --variants

# Design Hub — browse, swap presets, export
python -m pdf_tool.preview

# Collages from a folder of images
python -m pdf_tool.collage path/to/images --layout auto --png
```

Hub help: `python -m pdf_tool`. Full recipes: [`EXPORTS.md`](EXPORTS.md).
Docs index: [`README.md`](README.md). Agent map: [`AGENTS.md`](../AGENTS.md).
SSOT dashboard: [`SSOT.md`](SSOT.md).

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
| Real PII in any form | Never commit; never move into `examples/` |

The résumé *protocol* (vault → tailor → export) is documented and optional. The
**engine + public themes** are the white-label deliverable.

---

## Related

- [`PREVIEWER.md`](PREVIEWER.md) — Design Hub
- [`THEME-DESIGN.md`](THEME-DESIGN.md) — token contract
- [`VAULT.md`](VAULT.md) — only if you adopt the private claim layer
