# SSOT Dashboard — pdf-designer

```
SSOT Dashboard — pdf-designer
─────────────────────────────
Config:    .config/mcp-pdf-designer.json ✓  (+ .example.json template ✓)
Env:       none by design (no .env) ✓
Protocol:  AGENTS.md → docs/{STORAGE,VAULT,JOB-ASSESSMENT,ARCHITECTURE}.md → /make-resume · /make-collage
Product:   docs/PRODUCT.md   ← ⭐ free GitHub core vs future paid app (WHITE-LABEL = public reuse only)
Theme:     themes/default-{resume,collage}.json + themes/presets/* + PALETTE-RULES.md   ← COLOR
Gen-rules: themes/GENERATION-RULES.md   ← ⭐ house rules for ALL generated docs (casing · overlays · framing · no-magenta)
QA gate:   docs/QA.md + python -m pdf_tool.check_generation   ← ⭐ 10 checks; judge the ARTIFACT (render), not the source
Layouts:   layouts/collage/* + layouts/*  (python -m pdf_tool.collage --list-recipes)  ← STRUCTURE
Private:   storage/brand-design, users, vaults, studio/resources/images/martiangames (shared MG gallery), collages (gitignored)
Hub:       python -m pdf_tool.preview → :8787 (workspace auto-starts via scripts/ensure-design-hub.ps1)
Smoke:     python scripts/smoke-white-label.py   ← ⭐ fresh-clone proof (examples/ only, no storage/)
Package:   docs/PACKAGING.md + scripts/check-wheel-assets.py  ← wheel must include themes/layouts
Engine:    python -m pdf_tool  (hub) / individual modules
Plans:     Plans/_Active/2026-07-21-next-agent-product-prompt.md
```

Compact map of what this repo owns vs what it only points at. Agents: start here, then
[`AGENTS.md`](../AGENTS.md). Humans shipping without private vaults:
[`WHITE-LABEL.md`](WHITE-LABEL.md).

---

## Owns here

| Surface | Path | Role |
|---|---|---|
| Engine | `src/pdf_tool/` | HTML→PDF, guards, collage, Design Hub, tracker |
| Public themes | `themes/default-resume.{json,css}`, `themes/presets/*` | ⭐ **COLOR** — token SSOT + audition palettes |
| Collage theme | `themes/default-collage.json` | Canvas presets + `backgrounds` (gradients) + per-background `frame` colors |
| **Layouts** | `layouts/*.json` (docs) + `layouts/collage/*` | ⭐ **STRUCTURE** — cover=`one-page-letter` · résumé=`two-page-standard` · samples=`work-examples` · collage recipes under `collage/` |
| Page layout | `docs/LAYOUT-SYSTEM.md` + `themes/default-resume.{json,css}#document` | ⭐ Equal margins (0.65in default) + header-flows/footer-pins; one knob `--resume-page-margin`; content-fit rule |
| Page signature | `themes/default-resume.json#document.signature` | Bottom-right page-footer pin (`.page` / `.page-main` / `.page-sig`) |
| Previewer | `src/pdf_tool/preview.py` (`docs/PREVIEWER.md`) | Design Hub; `/recipes` · `/vault`; **auto-refreshes** via `/api/version` on new exports |
| Palette rule | `themes/PALETTE-RULES.md` | No brown / mustard / lime — enforced by `check_palette` |
| **Generation rules** | `themes/GENERATION-RULES.md` | ⭐ House rules for ALL generated docs: **name/company never all-lowercase**, no neon over images (dark scrim only), 16:9 no-crop framing, no-magenta pointer |
| **QA gate** | `docs/QA.md` + `pdf_tool.check_generation` | ⭐ ONE command · **10 checks** (palette·rgba-magenta·casing·overlay·signature·margins·page-bg·rendered-color·overflow·footer-collision). Per-user + per-doc aware. **Judge the artifact.** Run before shipping. |
| Protocol docs | `docs/{STORAGE,VAULT,JOB-ASSESSMENT,ARCHITECTURE}.md` | Claim rules + workflow |
| **Work-samples SSOT** | `profiles/<user>-resume.json#workSamples` + `users/<user>.json#portfolio` | ⭐ **PER-USER** page structure + personal assets — never copy another person's page ([VAULT.md](VAULT.md) § Work-samples) |
| **Shared MG gallery** | `storage/studio/resources/images/martiangames/` | ⭐ Title stills + MG logo used by **both** applicants; per-user `…/images/martiangames/` junctions here ([STORAGE.md](STORAGE.md)) |
| Agent map | `AGENTS.md` | Capability / command SSOT for assistants |
| **Product / business** | [`PRODUCT.md`](PRODUCT.md) | ⭐ Free GitHub toolkit vs future paid app; shell-over-Hub; privacy split |
| Packaging / PyPI | [`PACKAGING.md`](PACKAGING.md) | Wheel must ship public `themes/` + `layouts/` via `pdf_tool/share/` |
| White-label how-to | [`WHITE-LABEL.md`](WHITE-LABEL.md) | Clone without vaults (not the business plan) |
| Make-resume | `.claude/commands/make-resume.example.md` | Job-application routine (public seed; personal `make-resume.md` is gitignored) |
| Make-collage | `.claude/commands/make-collage.md` | Multi-image collage routine |
| Public examples | `examples/profiles/`, `examples/brand-design/`, `examples/_job-listings/` | Clone-safe templates |
| Project config | `.config/mcp-pdf-designer.json` | Breakpoint pointer, hub, voice/external pointers |
| Active plan | `Plans/_Active/2026-07-21-next-agent-product-prompt.md` | What to build next (+ paste-ready handoff) |

---

## The two axes: color vs structure

Design lives in **two tracked, composable registries**. Any layout renders in any theme.

| Axis | Owns | Where | Discover |
|---|---|---|---|
| **Color** | tokens, palettes, gradients, frame colors | `themes/` + `themes/presets/` | `themes/default-collage.json#backgrounds` |
| **Structure** | family, canvas, fit, margins, page model | `layouts/collage/` + `layouts/` | `python -m pdf_tool.collage --list-recipes` |

> **Neither belongs in `storage/`.** `storage/` is *private content* — real images, vaults,
> finished exports. A layout or palette you'd reuse is **tracked**, so it survives, is
> discoverable, and ships with a fresh clone. Content is private; design is shared.

Both are reachable from one machine-readable file:
[`.config/mcp-pdf-designer.json`](../.config/mcp-pdf-designer.json) → `layouts`, `collage`,
`palette_registry`. Clone-safe template: `.config/mcp-pdf-designer.example.json`.

---

## Personal palette prefs (Jenni / Shade)

**One hex map each. Person files only point.**

```
users/<user>.json#brandTheme.ssot
        │
        ▼
storage/brand-design/brand-*.json   ← ⭐ pdf-designer COLOR SSOT (Design Hub + exports)
        ▲
        │  map / sync from (never a second résumé SSOT)
www-theme-kit/profiles/{jenninexus,martiangames}.json
```

| Who | Edit this file | Pointed by |
|---|---|---|
| Jenni | `storage/brand-design/brand-jenninexus.json` | `users/jenni.json` · `profiles/jenni-resume.json` |
| Shade (Synagen) | `storage/brand-design/brand-synagen.json` | `users/shade.json` · `profiles/shade-resume.json` |
| Martian studio | `storage/brand-design/brand-martian.json` | Shade studio/games profiles + kit `#martian-resume` |

Design Hub loads `themes/` + `themes/presets/` + `storage/brand-design/` (`preview.load_palettes`).
The person filter is library-only — it does **not** auto-select a palette. Full contract:
[`THEME-DESIGN.md`](THEME-DESIGN.md) · [`STORAGE.md`](STORAGE.md) · [`../themes/PALETTE-RULES.md`](../themes/PALETTE-RULES.md).

---

## Points elsewhere (never duplicate)

| Concern | Owning SSOT |
|---|---|
| Breakpoints numbers | `C:\mcp\.config\mcp-breakpoints.json` + www-theme-kit SCSS |
| Resume palette kit catalog | `www-theme-kit/palettes/resume-palettes.json` |
| Hub chrome profile ⭐ | `www-theme-kit/profiles/pdf-designer.json` |
| Live-site brand hex (JN / MG) | `www-theme-kit/profiles/{jenninexus,martiangames}.json` — map into `storage/brand-design/` for résumés |
| Preset lineage (history only) | Some `themes/presets/*` note syna-theme-kit origins — **runtime kit is www-theme-kit**; do not open syna/syn-themes for hub work |
| Human voice map / public cards | `C:\Github\voice-seed` (registry + `characters/humans/*.md`) |
| Application `characterVoice` + vault `voice` | **THIS** repo `storage/` (private) — voice-seed only points |
| Agency fiction voices | `agency` — **NOT** applicants |
| Social / marketing registers | `socials` |

---

## Engine CLI map

| Module | One-liner |
|---|---|
| `html_to_pdf` | Render HTML → print-perfect PDF (light/dark; optional `--variants`) |
| `variants` | Light PDF per public palette → `_variants/<stem>/` |
| `merge_pdfs` | Bundle PDFs; optional US Letter size check |
| `pdf_to_png` | Screenshot each `.page` (agent visual verify) |
| `check_generation` | ⭐ ONE QA pass — 10 checks incl. rendered-color + footer-collision (per-user/doc aware) |
| `check_palette` | Reject brown / mustard / lime (source hex) before export |
| `check_rendered_color` | Reject brown that only appears after the browser composites |
| `check_overflow` | Page-fit at 816px paper width (also auto-warns on export) |
| `check_vault` | Vault schema / `--explain` / `--coverage` |
| `check_ats` | ATS text-layer sanity on light PDF |
| `audit_resume` | Diff rendered HTML vs vault (lead omissions) |
| `tracker` | List / status over `storage/_job-listings/**/application.json` |
| `collage` | Layout candidates + picker gallery from an image folder |
| `preview` | Design Hub — localhost library + palette swap + export |

```bash
python -m pdf_tool                  # hub help
python -m pdf_tool.<command> ...    # run a module
```

Also after `pip install -e .`: `pdf-designer`, `pdf-designer-preview`,
`pdf-designer-check-palette`, `pdf-designer-check-vault`, `pdf-designer-check-ats`,
`pdf-designer-tracker`, `pdf-designer-variants`.

---

## Related docs

Full index: [`README.md`](README.md) (docs hub). Root [`../README.md`](../README.md) is the
short public-facing entry.

| Doc | Role |
|---|---|
| [`EXPORTS.md`](EXPORTS.md) | Commands + export / pagination SSOT |
| [`WHITE-LABEL.md`](WHITE-LABEL.md) | Public-only reusable path (no private vaults) |
| [`VAULT.md`](VAULT.md) | Claim + voice rules |
| [`PREVIEWER.md`](PREVIEWER.md) | Design Hub how-to |
| [`STORAGE.md`](STORAGE.md) | Private workspace layout |
| [`Plans/_Active/…`](../Plans/_Active/2026-07-21-next-agent-product-prompt.md) | Working checklist + handoff |
