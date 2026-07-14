<div align="center">

# 🖨️ pdf-designer

**Design it in HTML. Print it like a browser. Never invent a claim.**

![MIT](https://img.shields.io/badge/license-MIT-9b5cf6?style=flat-square&labelColor=1a1a2e)
![Runtime](https://img.shields.io/badge/runtime-python%20%2B%20playwright-63b3ed?style=flat-square&labelColor=1a1a2e)
![Engine](https://img.shields.io/badge/engine-headless%20chromium-42f4c8?style=flat-square&labelColor=1a1a2e)
![Local](https://img.shields.io/badge/local--first-no%20SaaS-ff6ec4?style=flat-square&labelColor=1a1a2e)

A local-first toolkit for turning HTML into **print-perfect PDFs** — résumés, cover letters, collages —
with an optional job-application layer that tailors every document from *your own verified facts*.

**Zero network calls. Zero environment variables. Zero telemetry.**
Not a promise — a property of the code. There's nothing to configure and nowhere for your data to go.

</div>

---

## ✨ What it does

| | |
|---|---|
| 📄 **HTML → PDF** | Real headless Chromium. CSS grid, flex, and `@media print` render exactly like a browser's own *Print → Save as PDF*. |
| 🌗 **Light + dark, one source** | Every document exports an ATS-safe light PDF **and** a branded dark one — same geometry, same pagination. |
| 🎨 **Themeable** | Palettes are data. Swap a token map, keep the layout. A guard rejects colors that print badly. |
| 🖼️ **Collages** | Point it at a folder of images → six layout families + a picker gallery, PowerPoint-Designer style. |
| 🔍 **Design Hub** | A local previewer with live thumbnails, a palette swapper, and one-click export. |
| 🔐 **Source-backed** | The résumé layer can only claim what's in your vault. It elaborates; it never fabricates. |

## 🚀 Quick start

```bash
pip install -e .            # makes `pdf_tool` importable from the repo root
playwright install chromium
```

```bash
python -m pdf_tool.preview                        # 🎨 Design Hub — browse, theme, export
python -m pdf_tool.html_to_pdf doc.html           # 📄 light / ATS PDF   (palette guard runs automatically)
python -m pdf_tool.html_to_pdf doc.html --pdf-theme dark   # 🌙 branded dark PDF
python -m pdf_tool.merge_pdfs out.pdf a.pdf b.pdf --require-letter
python -m pdf_tool.pdf_to_png doc.pdf             # 👀 verify by eye
python -m pdf_tool.collage ./images --layout auto --png
```

**The guards** — they fail loudly, so nothing quietly ships broken:

```bash
python -m pdf_tool.check_palette --scan .   # 🚦 no brown / mustard / lime  (also BLOCKS every export)
python -m pdf_tool.check_vault --all        # 🧠 vault schema — catches claims that would be invisible
```

Exports land in `_exports/` beside the source and **never overwrite** (auto `-v2`, `-v3`).

## 📚 Docs

| Doc | What's in it |
|---|---|
| [`AGENTS.md`](AGENTS.md) | **Agent capability map** — every command, the repo map, and the contracts that must not break. Vendor-neutral. |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | How the pieces fit; the roadmap. |
| [`docs/THEME-DESIGN.md`](docs/THEME-DESIGN.md) | The theme/profile contract and the token names. |
| [`docs/EXPORTS.md`](docs/EXPORTS.md) | Export paths, the palette guard, pagination traps. |
| [`docs/PREVIEWER.md`](docs/PREVIEWER.md) | The Design Hub + its app roadmap. |
| [`docs/COLLAGE-DESIGN.md`](docs/COLLAGE-DESIGN.md) | The six collage families and the canvas presets. |
| [`themes/PALETTE-RULES.md`](themes/PALETTE-RULES.md) | 🚦 **The color rule** — no brown, no mustard, no lime — and the guard that enforces it. |

## 🧠 The résumé layer *(optional)*

The interesting part. A résumé is a **query against a vault**, not a document you rewrite each time.

```
storage/                        ← gitignored; your real data never ships
  users/<you>.json              WHO is applying — contact, brand, naming
  <you>/resume-source.json      ⭐ THE VAULT — every fact you may truthfully claim,
                                   each with a source, a strength, and its role tracks
  profiles/<you>-resume.json    HOW it renders — layout, exports, cover-letter policy
  applications/<Role>/          THE JOB — the listing, the apply link, the company palette
```

**The rule:** never write a claim that isn't in the vault. But *do* elaborate persuasively on what
genuinely matches — take a real skill and show precisely why it's valuable *to this employer*.
That's not spin, it's translation.

**The other rule:** if a listing asks for something the vault doesn't have — **ask the human before
calling it a gap.** The vault records what they've *told* you; it is not the limit of what they can do.

Then one command runs the whole routine — capture the apply link, verify remote status and pay,
research the company, derive a theme from their real brand CSS, write, export light + dark, merge the
bundle:

```
/make-resume <user> storage/applications/<Role>
```

📖 [`.claude/commands/make-resume.md`](.claude/commands/make-resume.md) — and it's **agent-agnostic**:
plain markdown, no vendor APIs. Any assistant (or human) can follow it.

## 🎨 Canvas sizes

Print defaults to **US Letter (8.5 × 11in)**. Collages also target the standard social canvases:

| Ratio | Pixels | Use |
|---|---|---|
| 8.5 × 11in | 2550 × 3300 @300dpi | Print / PDF one-sheet |
| 16:9 | 1920 × 1080 | YouTube, slides, banners |
| 9:16 | 1080 × 1920 | Stories, Reels, Shorts |
| 4:5 | 1080 × 1350 | Instagram portrait |
| 1:1 | 1024 × 1024 | Square posts, avatars |

Presets: [`themes/default-collage.json`](themes/default-collage.json)

## 🧭 Principles

- **Local-first.** No SaaS, no upload, no telemetry. `storage/` is gitignored and stays home.
- **Source-backed.** Generated content never outruns verified claims.
- **No auto-submission.** The tool prepares; the human submits.
- **Geometry is locked.** Palettes change color — never paper size, margins, or pagination.

## 📄 License

**MIT** — see [`LICENSE`](LICENSE). © 2026 Jenni Nexus.

And it's an *honest* MIT: **every dependency is permissive**, so there's no copyleft hiding in the
tree and nothing you have to disclose downstream.

| Dependency | License |
|---|---|
| playwright | Apache-2.0 |
| pypdf | BSD-3-Clause |
| Pillow | MIT-CMU |

> PyMuPDF (**AGPL-3.0**) was removed in July 2026 — a mandatory AGPL dependency makes an MIT claim
> incoherent, because you can't grant rights you don't hold. It only rasterized PDF pages, and
> Chromium (already shipping) does that better. The full story:
> [`docs/LICENSING-NOTES.md`](docs/LICENSING-NOTES.md).
