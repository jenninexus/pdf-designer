<div align="center">

# 🖨️ PDF Designer

## Design in HTML. Print with confidence.
## A local-first résumé studio that keeps your career data yours.

![MIT](https://img.shields.io/badge/license-MIT-9b5cf6?style=flat-square&labelColor=1a1a2e)
![Runtime](https://img.shields.io/badge/runtime-python%20%2B%20playwright-63b3ed?style=flat-square&labelColor=1a1a2e)
![Engine](https://img.shields.io/badge/engine-headless%20chromium-42f4c8?style=flat-square&labelColor=1a1a2e)
![Local](https://img.shields.io/badge/local--first-no%20SaaS-ff6ec4?style=flat-square&labelColor=1a1a2e)

`pdf-designer` turns HTML into print-perfect PDFs with the same Chromium engine your browser uses.
Build ATS-honest light résumés, branded dark versions, letters, and collages — without giving a SaaS
your work history.

**Zero network calls. Zero environment variables. Zero telemetry.**

</div>

| Create | Verify | Keep control |
|---|---|---|
| **Light + dark PDFs** from one HTML source | **QA guards** for palette, overflow, and ATS text | **Private vaults** stay local and gitignored |
| Résumés, letters, work samples, and collages | `check_generation` judges the rendered artifact | No telemetry, account, environment file, or network call |

> **Status:** private for now; docs shaped for a public release. **Start here:**
> [`examples/resume-studio/`](examples/resume-studio/) · product: [`docs/PRODUCT.md`](docs/PRODUCT.md) ·
> split: [`docs/PUBLIC-LOCAL-SPLIT.md`](docs/PUBLIC-LOCAL-SPLIT.md) ·
> clone path: [`docs/GETTING-STARTED.md`](docs/GETTING-STARTED.md) · packaging: [`docs/PACKAGING.md`](docs/PACKAGING.md) ·
> [`Browser overview`](docs/pdf-designer-overview.html) · [`printable PDF`](docs/pdf-designer-overview.pdf) · agents: [`AGENTS.md`](AGENTS.md).
> Protocol seeds on GitHub are `*.example.md` only; bare `start`/`wrap`/`make-*` stay local.

---

## 🚀 Prove the public path in five minutes

Works from **tracked files only** — `examples/` + `themes/`. No `storage/` required.

```bash
pip install -e ".[dev]"
playwright install chromium

# Prove the public path: QA + light/dark PDFs + ATS text-layer check
python scripts/smoke-white-label.py

# Design Hub — browse the example resume, swap palettes, export
python -m pdf_tool.preview         # → http://127.0.0.1:8787/
```

The smoke script is the release proof. To use the engine directly:

```bash
python -m pdf_tool.html_to_pdf examples/profiles/default-resume/default-resume.html
python -m pdf_tool.html_to_pdf examples/profiles/default-resume/default-resume.html --pdf-theme dark
```

Exports land in `_exports/` as `<stem>-light.pdf` / `<stem>-dark.pdf` and **never
overwrite** (`-v2`, `-v3`). Full command list → [`docs/EXPORTS.md`](docs/EXPORTS.md).
Ship gate → [`docs/QA.md`](docs/QA.md) (`python -m pdf_tool.check_generation …`).

---

## ✨ The product loop

1. **Start with the public example.** Browse `examples/resume-studio/`, or make a copy of the profile
   and theme that fit your work.
2. **Design once.** Render a light board-upload PDF and a dark human-facing PDF from the same HTML.
3. **Verify before you ship.** Run `check_generation`; for board uploads, run `check_ats` on the light PDF.

The optional vault workflow makes claims source-backed. It never auto-submits an application, and it
asks before treating a missing claim as a skill gap.

## 📚 Navigate the studio

| Start here | |
|---|---|
| [`docs/README.md`](docs/README.md) | **Docs index** — where every topic lives |
| [`docs/PRODUCT.md`](docs/PRODUCT.md) | Free GitHub core vs future paid app |
| [`docs/PUBLIC-LOCAL-SPLIT.md`](docs/PUBLIC-LOCAL-SPLIT.md) | Public vs private vs paid architecture |
| [`docs/GETTING-STARTED.md`](docs/GETTING-STARTED.md) | Clone path without vaults |
| [`docs/PACKAGING.md`](docs/PACKAGING.md) | PyPI / wheel (must ship themes + layouts) |
| [`docs/SSOT.md`](docs/SSOT.md) | What this repo owns vs pointers elsewhere |
| [`AGENTS.md`](AGENTS.md) | Agent capability map + contracts |

For the full command index, see [`docs/EXPORTS.md`](docs/EXPORTS.md). For a visual tour of the product
story, open [`docs/pdf-designer-overview.html`](docs/pdf-designer-overview.html) in any browser, or read
the [`printable PDF`](docs/pdf-designer-overview.pdf) rendered by PDF Designer.

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
