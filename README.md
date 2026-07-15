<div align="center">

# 🖨️ pdf-designer

## Design it in HTML.
## Print it like a browser.

![MIT](https://img.shields.io/badge/license-MIT-9b5cf6?style=flat-square&labelColor=1a1a2e)
![Runtime](https://img.shields.io/badge/runtime-python%20%2B%20playwright-63b3ed?style=flat-square&labelColor=1a1a2e)
![Engine](https://img.shields.io/badge/engine-headless%20chromium-42f4c8?style=flat-square&labelColor=1a1a2e)
![Local](https://img.shields.io/badge/local--first-no%20SaaS-ff6ec4?style=flat-square&labelColor=1a1a2e)

Local-first toolkit that turns HTML into **print-perfect PDFs** — résumés, cover letters,
collages — with an optional vault-backed job-application layer that never invents a claim.

**Zero network calls. Zero environment variables. Zero telemetry.**

</div>

- 📄 **HTML → PDF** via real headless Chromium — what the browser prints is what you get
- 🌗 **Light + dark** from one source — ATS-safe light PDF and branded dark, same pagination
- 🎨 **Themeable** palettes with a guard that rejects colors that print badly
- 🔍 **Design Hub** — local preview, palette swap, one-click export (`python -m pdf_tool.preview`)

> **Status:** private for now. Structure and docs are shaped for a future public release
> (MIT engine + public themes; private vaults stay gitignored). See [`docs/WHITE-LABEL.md`](docs/WHITE-LABEL.md).

---

## 🚀 Quick start

```bash
pip install -e .
playwright install chromium

python -m pdf_tool                 # list every command
python -m pdf_tool.preview         # Design Hub → http://127.0.0.1:8787/
python -m pdf_tool.html_to_pdf doc.html
python -m pdf_tool.html_to_pdf doc.html --pdf-theme dark
```

Exports land in `_exports/` as `<stem>-light.pdf` / `<stem>-dark.pdf` and **never
overwrite** (`-v2`, `-v3`). Full command list, guards, pagination traps →
[`docs/EXPORTS.md`](docs/EXPORTS.md).

---

## 📚 Docs

| Start here | |
|---|---|
| [`docs/README.md`](docs/README.md) | **Docs index** — where every topic lives |
| [`docs/SSOT.md`](docs/SSOT.md) | What this repo owns vs pointers elsewhere |
| [`docs/WHITE-LABEL.md`](docs/WHITE-LABEL.md) | Public-only path (no private vaults) |
| [`AGENTS.md`](AGENTS.md) | Agent capability map + contracts |

---

## 🧭 Principles

- **Local-first** — no SaaS, no upload, no telemetry; `storage/` is gitignored
- **Source-backed** — generated copy never outruns verified claims
- **No auto-submission** — the tool prepares; the human submits
- **Geometry is locked** — palettes change color, never paper size or pagination

---

## 📄 License

MIT — use, fork, customize. See [`LICENSE`](LICENSE). © 2026 Jenni Nexus.

Honest MIT: every dependency is permissive (playwright, pypdf, Pillow). AGPL history →
[`docs/LICENSING-NOTES.md`](docs/LICENSING-NOTES.md).

<div align="center">

Published by [Jenni](https://github.com/jenninexus) at [Monofinity Studio](https://github.com/monofinitystudio).

</div>
