# SSOT Dashboard — pdf-designer

```
SSOT Dashboard — pdf-designer
─────────────────────────────
Config:    .config/mcp-pdf-designer.json ✓  (+ .example.json template ✓)
Env:       none by design (no .env) ✓
Protocol:  AGENTS.md → docs/{STORAGE,VAULT,JOB-ASSESSMENT,ARCHITECTURE}.md → /make-resume · /make-collage
Product:   docs/PRODUCT.md + docs/PUBLIC-LOCAL-SPLIT.md   ← ⭐ free core vs private vs paid
Clone:     docs/GETTING-STARTED.md   ← public reuse (ex-WHITE-LABEL stub)
Theme:     themes/default-{resume,collage}.json + themes/presets/* + PALETTE-RULES.md   ← COLOR
Gen-rules: themes/GENERATION-RULES.md   ← ⭐ house rules for ALL generated docs (casing · overlays · framing · no-magenta)
QA gate:   docs/QA.md + python -m pdf_tool.check_generation   ← ⭐ 10 checks; judge the ARTIFACT (render), not the source
Layouts:   layouts/{cover-letter,letter,resume,work-examples,collage}/*  (python -m pdf_tool.collage --list-recipes)  ← STRUCTURE
Private:   root nouns (users/vaults/profiles/resumes/_job-apps/collages/brands) + storage/ alias (gitignored)
Hub:       python -m pdf_tool.preview → :8787 (workspace auto-starts via scripts/ensure-design-hub.ps1)
Smoke:     python scripts/smoke-white-label.py   ← ⭐ fresh-clone proof (examples/ only, no storage/)
Package:   docs/PACKAGING.md + scripts/check-wheel-assets.py  ← wheel must include themes/layouts
Engine:    python -m pdf_tool  (hub) / individual modules
Plans:     Plans/_Active/2026-08-21-standalone-app-remaining.md
Product hub: C:\Github\product-design  (local; /jen:products)
```

Compact map of what this repo owns vs what it only points at. Agents: start here, then
[`AGENTS.md`](../AGENTS.md). Humans shipping without private vaults:
[`GETTING-STARTED.md`](GETTING-STARTED.md). Architecture: [`PUBLIC-LOCAL-SPLIT.md`](PUBLIC-LOCAL-SPLIT.md).

---

## Owns here

| Surface | Path | Role |
|---|---|---|
| Engine | `src/pdf_tool/` | HTML→PDF, guards, collage, Design Hub, tracker |
| Public themes | `themes/default-resume.{json,css}`, `themes/presets/*` | ⭐ **COLOR** — token SSOT + audition palettes |
| Collage theme | `themes/default-collage.json` | Canvas presets + `backgrounds` (gradients) + per-background `frame` colors |
| **Layouts** | `layouts/{cover-letter,letter,resume,work-examples}/*` + `layouts/collage/*` | ⭐ **STRUCTURE** — cover=`one-page-letter` · résumé=`two-page-standard` · samples=`work-examples` · collage recipes under `collage/` |
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
| **Product / business** | [`PRODUCT.md`](PRODUCT.md) | ⭐ Free GitHub toolkit vs future paid app; shell-over-Hub |
| **Public vs local** | [`PUBLIC-LOCAL-SPLIT.md`](PUBLIC-LOCAL-SPLIT.md) | ⭐ Tracked vs gitignored; sibling-repo map |
| Packaging / PyPI | [`PACKAGING.md`](PACKAGING.md) | Wheel must ship public `themes/` + `layouts/` via `pdf_tool/share/` |
| Clone how-to | [`GETTING-STARTED.md`](GETTING-STARTED.md) | Public path without vaults (`WHITE-LABEL.md` is a stub alias) |
| Make-resume | `.claude/commands/make-resume.example.md` | Job-application routine (public seed; personal `make-resume.md` is gitignored) |
| Make-collage | `.claude/commands/make-collage.example.md` | Multi-image collage routine (public seed) |
| Public examples | `examples/resume-studio/`, `examples/profiles/`, `examples/brand-design/` | Clone-safe templates |
| Project config | `.config/mcp-pdf-designer.example.json` | Seed only — local `mcp-pdf-designer.json` is gitignored |
| Active plan | `Plans/_Active/2026-08-21-standalone-app-remaining.md` | Current release record, optional distribution, and desktop-shell checklist |

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

## ATS parseability (every profile)

**How you know a résumé is parseable:** export the **light** PDF → run
`python -m pdf_tool.check_ats <file.pdf>` → required cues must show `[OK] job title` ·
`[OK] work experience` · `[OK] education`, **mid-word splits must be ≤ 2**, and the text dump
must contain those phrases as **contiguous words**. If *you* cannot find them, Jobright / Indeed will
not either. Full checklist: [`JOB-ASSESSMENT.md`](JOB-ASSESSMENT.md) § Tier 4.5 · inherited contract:
`examples/profiles/default-resume/profile.json#verify.atsParse`.

| Myth | Reality |
|---|---|
| “Dark is not parseable” | **False** when print fonts match — light and dark share the HTML. Still upload **light** to boards. |
| “Always upload dark” | **Wrong for boards.** Jobright / Indeed / LinkedIn expect `*-resume-light.pdf`. Dark = humans / email / portfolio. |
| “Section looks fine on screen” | Not enough. Montserrat can split `WORK EXPERIENCE` → `W ORK EXPERIENCE` and body words → `Gam es` / `m aterials` while the page looks perfect. **Print body + h2 use a system font.** |
| “Jobright rank D means unparseable” | **False.** Rank / IMPROVABLE / “Insufficient skills” / “Lack of Accomplishment” is their **content AI**. Missing Job Title / Work Experience / Education is the **parse** warning. Different gates. |

**Defaults:** ship **both** light and dark for go-to résumés under `resumes/<user>/defaults/` so the board
file and the branded file stay in sync. Per-job `exportPrefs` may still emphasize dark for email —
that does **not** remove the need for a light file when a board will parse the upload. Cover letters
and work-samples: `check_generation` always; boards still get the light **résumé**, not the portfolio.
---

## Personal palette prefs (Jenni / Shade)

**One hex map each. Person files only point.**

```
users/<user>.json#brandTheme.ssot
        │
        ▼
brands/brand-*.json   ← ⭐ pdf-designer COLOR SSOT (Design Hub + exports)
        ▲
        │  map / sync from (never a second résumé SSOT)
www-theme-kit/profiles/{jenninexus,martiangames}.json
```

| Who | Edit this file | Pointed by |
|---|---|---|
| Jenni | `brands/brand-jenninexus.json` | `users/jenni.json` · `profiles/jenni-resume.json` · defaults triad under `resumes/jenni/defaults/` (same footer-mail legibility: `--text` ≥11px) |
| Shade (Synagen) | `brands/brand-synagen.json` | `users/shade.json` · `profiles/shade-resume.json` |
| Martian studio | `brands/brand-martian.json` | Shade studio/games profiles + kit `#martian-resume` |

Design Hub loads `themes/` + `themes/presets/` + `brands/` (`preview.load_palettes`; alias `storage/brand-design/`).
The person filter is library-only — it does **not** auto-select a palette. Full contract:
[`THEME-DESIGN.md`](THEME-DESIGN.md) · [`STORAGE.md`](STORAGE.md) · [`../themes/PALETTE-RULES.md`](../themes/PALETTE-RULES.md).

---

## Points elsewhere (never duplicate)

| Concern | Owning SSOT |
|---|---|
| Breakpoint numbers | `www-theme-kit/scss/_breakpoint-tokens.scss` (shared numeric SSOT) |
| Hub breakpoint / nav behavior | `src/pdf_tool/static/hub.css` (implemented pdf-designer policy) |
| MCP breakpoint file | `C:\mcp\.config\mcp-breakpoints.json` (cross-project cache/index; verify it, never treat it as the owner) |
| Resume palette kit catalog | `www-theme-kit/palettes/resume-palettes.json` |
| Hub chrome profile ⭐ | `www-theme-kit/profiles/pdf-designer.json` |
| Live-site brand hex (JN / MG) | `www-theme-kit/profiles/{jenninexus,martiangames}.json` — map into `brands/` for résumés |
| Preset lineage (history only) | Some `themes/presets/*` note syna-theme-kit origins — **runtime kit is www-theme-kit**; do not open syna/syn-themes for hub work |
| Human voice map / public cards | `C:\Github\voice-seed` (registry + `characters/humans/*.md`) |
| Application `characterVoice` + vault `voice` | **THIS** repo `users/` + `vaults/` (private) — voice-seed only points |
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
| `check_ats` | ATS parse gate — see § ATS parseability below |
| `audit_resume` | Diff rendered HTML vs vault (lead omissions) |
| `tracker` | List / status over `_job-apps/**/application.json` |
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
| [`GETTING-STARTED.md`](GETTING-STARTED.md) | Public-only reusable path (no private vaults) |
| [`VAULT.md`](VAULT.md) | Claim + voice rules |
| [`PREVIEWER.md`](PREVIEWER.md) | Design Hub how-to |
| [`STORAGE.md`](STORAGE.md) | Private workspace layout |
| [`Plans/_Active/2026-08-21-standalone-app-remaining.md`](../Plans/_Active/2026-08-21-standalone-app-remaining.md) | Working checklist + standalone-app handoff |
