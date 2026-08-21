# Getting started — public clone path

Use this repo **without** private vaults, PII, or studio brand maps.

```bash
git clone https://github.com/jenninexus/pdf-designer.git
```

Public defaults and presets *are* the product.

> **Architecture:** [`PUBLIC-LOCAL-SPLIT.md`](PUBLIC-LOCAL-SPLIT.md) ·
> **Business thesis:** [`PRODUCT.md`](PRODUCT.md) ·
> **Front door:** [`../examples/resume-studio/`](../examples/resume-studio/)

*(Formerly titled “WHITE-LABEL” — same checklist, clearer name for a public README.)*

---

## What you need

| Piece | Path | Notes |
|---|---|---|
| **Product entry** | [`examples/resume-studio/`](../examples/resume-studio/) | Résumé-creator pitch + demo path |
| Example profile + HTML | `examples/profiles/default-resume/` | Reference render + `profile.json` |
| Default theme | `themes/default-resume.{json,css}` | Token SSOT + CSS mirror |
| Audition palettes | `themes/presets/*.json` | Design Hub / `--variants` shopping |
| Palette rule | [`themes/PALETTE-RULES.md`](../themes/PALETTE-RULES.md) | No brown / mustard / lime |
| Brand template (optional) | `examples/brand-design/` | Copy shape only — not real hex maps |
| Protocol seeds | `.claude/commands/*.example.md` | Bare start/wrap/make-* are **not** on GitHub |

You do **not** need `users/`, vaults, or `brands/` to export PDFs.
The clone also shows **README stubs** at `users/` · `vaults/` · `profiles/` · `resumes/` ·
`_job-apps/` · `collages/` · `brands/` so the product folders are visible — copy from
`examples/` (or the in-folder `*.example.json`) into those names when you add your own data. Layout: [`WORKSPACE-LAYOUT.md`](WORKSPACE-LAYOUT.md).

---

## One checkout — not two apps, not `.env`

You and a stranger use the **same engine**. Privacy is gitignore, not a second install:

| Layer | What |
|---|---|
| **Tracked (clone)** | Engine, `themes/`, `layouts/`, `examples/`, README stubs, `users/you.example.json`, `vaults/you.example.json` |
| **Local (you)** | Real `users/*.json`, vaults, `_job-apps/`, `resumes/**/_exports/`, `brands/` |
| **Optional pointers** | `.config/mcp-pdf-designer.json` (copy the `.example`) |

The engine **reads no environment variables**. Do not add `.env` / `.env.local` unless a new tool actually reads them — it would document a fiction. `storage/` was retired after the root-noun migration; the resolver only accepts old URLs when a live root-noun file exists. Exports live under `resumes/<user>/_exports/`.

---

## 5-minute checklist (stranger / fresh clone)

Every step uses **tracked** paths only.

| Step | Command | Pass means |
|---|---|---|
| 1. Install | `pip install -e ".[dev]" && playwright install chromium` | `python -m pdf_tool` prints the hub |
| 2. Smoke | `python scripts/smoke-white-label.py` | exit 0 — QA + light/dark PDF + ATS |
| 3. Hub | `python -m pdf_tool.preview` | http://127.0.0.1:8787/ |
| 4. (Optional) variants | `python -m pdf_tool.variants examples/profiles/default-resume/default-resume.html` | one light PDF per public palette |

The smoke script runs `check_generation`, exports light + dark PDFs, runs `check_ats` on
the light file, and writes under `examples/profiles/default-resume/_exports/` (gitignored).

**If smoke fails on a clean clone, the public product path is broken — fix before anything else.**

---

## Commands

```bash
pip install -e ".[dev]" && playwright install chromium

python scripts/smoke-white-label.py

python -m pdf_tool.check_generation examples/profiles/default-resume/default-resume.html
python -m pdf_tool.html_to_pdf examples/profiles/default-resume/default-resume.html
python -m pdf_tool.html_to_pdf examples/profiles/default-resume/default-resume.html --pdf-theme dark

python -m pdf_tool.variants examples/profiles/default-resume/default-resume.html
python -m pdf_tool.preview
python -m pdf_tool.collage path/to/images --layout auto --png
```

More: [`EXPORTS.md`](EXPORTS.md) · [`PREVIEWER.md`](PREVIEWER.md) · [`../AGENTS.md`](../AGENTS.md).

---

## Brand maps

- **Public:** `themes/default-resume.json` + `themes/presets/*` (Hub swapper).
- **Private later:** copy `examples/brand-design/` → local `brands/brand-*.json`
  (gitignored). See [`STORAGE.md`](STORAGE.md).

Do not put real brand hex into tracked `themes/` or `examples/` unless you intend them public.

---

## What stays private forever

| Surface | Why |
|---|---|
| `users/*.json` | Contact, hard facts, `characterVoice` |
| `vaults/<user>.json` | Claim vault + application voice |
| `_job-apps/` | Real listings, pay, apply links |
| `brands/` | Studio / personal palettes |
| `collages/` | Real images |
| `.config/mcp-pdf-designer.json` | Absolute machine paths (use `.example.json`) |
| Bare `make-*.md` / `start.md` / `wrap.md` | Personal / SEGO ritual |
| Real PII | Never commit; never move into `examples/` |

The résumé *protocol* is documented and optional. The **engine + public themes** are the
clone-safe deliverable.

---

## Related

- [`PUBLIC-LOCAL-SPLIT.md`](PUBLIC-LOCAL-SPLIT.md) — public vs local architecture
- [`PRODUCT.md`](PRODUCT.md) — free GitHub vs future paid app
- [`VAULT.md`](VAULT.md) — only if you adopt the private claim layer
- [`WHITE-LABEL.md`](WHITE-LABEL.md) — stub alias → this page
