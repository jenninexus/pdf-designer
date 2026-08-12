<div align="center">

# 🖨️ pdf-designer

## Design it in HTML.
## Print it like a browser.

![MIT](https://img.shields.io/badge/license-MIT-9b5cf6?style=flat-square&labelColor=1a1a2e)
![Runtime](https://img.shields.io/badge/runtime-python%20%2B%20playwright-63b3ed?style=flat-square&labelColor=1a1a2e)
![Engine](https://img.shields.io/badge/engine-headless%20chromium-42f4c8?style=flat-square&labelColor=1a1a2e)
![Local](https://img.shields.io/badge/local--first-no%20SaaS-ff6ec4?style=flat-square&labelColor=1a1a2e)

Local-first **résumé studio for a broken job market** — HTML → print-perfect PDFs, optional
vault-backed claims, skills tags, and palette prefs. Never invents a claim. No SaaS vault.

**Zero network calls. Zero environment variables. Zero telemetry.**

</div>

- 📄 **HTML → PDF** via real headless Chromium — what the browser prints is what you get
- 🌗 **Light + dark** from one source — ATS-safe light PDF and branded dark, same pagination
- 🗄 **Per-user vaults** — skills / board tags / claims you control (`docs/VAULT.md`)
- 🎨 **Themeable** palettes with a guard that rejects colors that print badly
- 🔍 **Design Hub** — local preview, palette swap, one-click export (`python -m pdf_tool.preview`)

> **Status:** private for now; docs shaped for a public release. **Start here:**
> [`examples/resume-studio/`](examples/resume-studio/) · product: [`docs/PRODUCT.md`](docs/PRODUCT.md) ·
> white-label: [`docs/WHITE-LABEL.md`](docs/WHITE-LABEL.md) · packaging: [`docs/PACKAGING.md`](docs/PACKAGING.md) ·
> agents: [`AGENTS.md`](AGENTS.md). Protocol seeds on GitHub are `*.example.md` only
> (bare `start`/`wrap`/`make-*` stay local). Palette prefs (private): `storage/brand-design/` —
> [`docs/SSOT.md`](docs/SSOT.md).

---

## 🚀 5-minute path (fresh clone, no private data)

Works from **tracked files only** — `examples/` + `themes/`. No `storage/` required.

```bash
pip install -e ".[dev]"
playwright install chromium

# Prove the public path (QA + light/dark PDF + ATS text layer)
python scripts/smoke-white-label.py

# Design Hub — browse the example resume, swap palettes, export
python -m pdf_tool.preview         # → http://127.0.0.1:8787/
```

Or export by hand:

```bash
python -m pdf_tool.html_to_pdf examples/profiles/default-resume/default-resume.html
python -m pdf_tool.html_to_pdf examples/profiles/default-resume/default-resume.html --pdf-theme dark
```

Exports land in `_exports/` as `<stem>-light.pdf` / `<stem>-dark.pdf` and **never
overwrite** (`-v2`, `-v3`). Full command list → [`docs/EXPORTS.md`](docs/EXPORTS.md).
Ship gate → [`docs/QA.md`](docs/QA.md) (`python -m pdf_tool.check_generation …`).

---

## 📚 Docs

| Start here | |
|---|---|
| [`docs/README.md`](docs/README.md) | **Docs index** — where every topic lives |
| [`docs/PRODUCT.md`](docs/PRODUCT.md) | Free GitHub core vs future paid app |
| [`docs/PACKAGING.md`](docs/PACKAGING.md) | PyPI / wheel (must ship themes + layouts) |
| [`docs/SSOT.md`](docs/SSOT.md) | What this repo owns vs pointers elsewhere |
| [`docs/WHITE-LABEL.md`](docs/WHITE-LABEL.md) | Public-only path (no private vaults) |
| [`AGENTS.md`](AGENTS.md) | Agent capability map + contracts |

---

## 🧭 Principles

- **Local-first** — no SaaS, no upload, no telemetry; `storage/` is gitignored
- **Source-backed** — generated copy never outruns verified claims
- **No auto-submission** — the tool prepares; the human submits
- **Geometry is locked** — palettes change color, never paper size or pagination
- **Consistent, professional frame** — every document uses **equal margins on all four edges**
  (default `0.65in`), the header flows at the top, and the footer/signature pins to the bottom.
  One shared layout system → [`docs/LAYOUT-SYSTEM.md`](docs/LAYOUT-SYSTEM.md)
- **The Design Hub auto-refreshes** — export a new resume and the previewer updates itself, no restart

---

## 📄 License

MIT — use, fork, customize. See [`LICENSE`](LICENSE). © 2026 Jenni Nexus.

Honest MIT: every dependency is permissive (playwright, pypdf, Pillow). AGPL history →
[`docs/LICENSING-NOTES.md`](docs/LICENSING-NOTES.md).

<div align="center">

Published by [Jenni](https://github.com/jenninexus) at [Monofinity Studio](https://github.com/monofinitystudio).

</div>
