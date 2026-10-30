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
QA gate:   docs/QA.md + python -m pdf_tool.check_generation   ← 12 deterministic checks; public users run locally; judge saved PDFs
Layouts:   layouts/{cover-letter,letter,resume,work-examples,collage}/*  (python -m pdf_tool.collage --list-recipes)  ← STRUCTURE
Private:   root nouns (users/vaults/profiles/resumes/_job-apps/collages/brands/_exports) + storage/ residue (gitignored)
Hub:       python -m pdf_tool.preview → :8787 (workspace auto-starts via scripts/ensure-design-hub.ps1)
Smoke:     python scripts/smoke-white-label.py   ← ⭐ fresh-clone proof (examples/ only, no storage/)
Package:   docs/PACKAGING.md + scripts/check-wheel-assets.py  ← wheel must include themes/layouts
Engine:    python -m pdf_tool  (hub) / individual modules
Plans:     docs/ROADMAP.md (durable backlog) · Plans/ (local-only, gitignored)
```

Compact map of what this repo owns vs what it only points at. Agents: start here, then
[`AGENTS.md`](../AGENTS.md). Humans shipping without private vaults:
[`GETTING-STARTED.md`](GETTING-STARTED.md). Architecture: [`PUBLIC-LOCAL-SPLIT.md`](PUBLIC-LOCAL-SPLIT.md).
Folder and optional agent-tooling overview: [`PROJECT-MAP.md`](PROJECT-MAP.md).

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
| Previewer | `src/pdf_tool/preview.py` (`docs/PREVIEWER.md`) | Design Hub; `/recipes` · `/vault`; **auto-refreshes** via `/api/version`; focused comparison checkboxes; dark real-PDF page preview |
| Palette rule | `themes/PALETTE-RULES.md` | No brown / mustard / lime — enforced by `check_palette` |
| **Generation rules** | `themes/GENERATION-RULES.md` | ⭐ House rules for ALL generated docs: **name/company never all-lowercase**, no neon over images (dark scrim only), 16:9 no-crop framing, no-magenta pointer |
| **QA gate** | `docs/QA.md` + `pdf_tool.check_generation` | One command, 12 checks including letter geometry and résumé text extraction. Required render errors fail; explicit source-only mode is not acceptance. Reuse unchanged source/dependency/PDF receipts. |
| Protocol docs | `docs/{STORAGE,VAULT,JOB-ASSESSMENT,ARCHITECTURE}.md` | Claim rules + workflow |
| **Work-samples SSOT** | `profiles/<user>-resume.json#workSamples` + `users/<user>.json#portfolio` | ⭐ **PER-USER** page structure + personal assets — never copy another person's page ([VAULT.md](VAULT.md) § Work-samples) |
| Agent map | `AGENTS.md` | Capability / command SSOT for assistants |
| **Product / business** | [`PRODUCT.md`](PRODUCT.md) | ⭐ Free GitHub toolkit vs future paid app; shell-over-Hub |
| **Public vs local** | [`PUBLIC-LOCAL-SPLIT.md`](PUBLIC-LOCAL-SPLIT.md) | ⭐ Tracked vs gitignored; sibling-repo map |
| Packaging / PyPI | [`PACKAGING.md`](PACKAGING.md) | Wheel must ship public `themes/` + `layouts/` via `pdf_tool/share/` |
| Clone how-to | [`GETTING-STARTED.md`](GETTING-STARTED.md) | Public path without vaults (`WHITE-LABEL.md` is a stub alias) |
| Make-resume | `.claude/commands/make-resume.example.md` | Job-application routine (public seed; personal `make-resume.md` is gitignored) |
| Make-collage | `.claude/commands/make-collage.example.md` | Multi-image collage routine (public seed) |
| Public examples | `examples/resume-studio/`, `examples/profiles/`, `examples/brand-design/` | Clone-safe templates |
| Project config | `.config/mcp-pdf-designer.example.json` | Seed only — local `mcp-pdf-designer.json` is gitignored |
| Product backlog | `docs/ROADMAP.md` | Remaining and parked product work; authoritative when `_active/` is empty |
| Session plans (local-only) | `Plans/` | Gitignored working context: `_active/` slice + `_complete/` history; never pushed |

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

**Personal defaults:** ship **both** light and dark for go-to résumés under `resumes/<user>/` (flat)
(HTML stays in `resumes/<user>/defaults/`) so the board
file and the branded file stay in sync. Per-job `exportPrefs` may still emphasize dark for email —
that does **not** remove the need for a light file when a board will parse the upload. Cover letters
and work-samples: `check_generation` always; boards still get the light **résumé**, not the portfolio.
---

## Personal palette preferences

Each person’s ignored `brands/brand-*.json` is the document color source; personal identity and profile files point to it. Keep actual mappings in private workspace notes.

## Points elsewhere (never duplicate)

| Concern | Owning SSOT |
|---|---|
| Breakpoint numbers | `www-theme-kit/scss/_breakpoint-tokens.scss` (shared numeric SSOT) |
| Hub breakpoint / nav behavior | `src/pdf_tool/static/hub.css` (implemented pdf-designer policy) |
| Project breakpoint pointer | `.config/mcp-pdf-designer.json` selects the named kit set/profile. Client MCP files launch servers only; the retired MCP cache is not a dependency. |
| Hub chrome profile ⭐ | `www-theme-kit/profiles/pdf-designer.json` |
| Aesyna visual adapter | `syna-theme-kit/adapters/pdf-designer.json` generates the vendored `src/pdf_tool/static/hub-aesyna.css`; no private kit dependency at runtime. |
| Application `characterVoice` + vault `voice` | **THIS** repo `users/` + `vaults/` (private) — voice-seed only points |
| Agency fiction voices | `agency` — **NOT** applicants |
| Social / marketing registers | `socials` |

---

## Engine CLI map

| Module | One-liner |
|---|---|
| `html_to_pdf` | Render HTML → print-perfect PDF (light/dark; optional `--variants` / `--max-mb 5`) |
| `inline_images` | Inline `{{img:name}}` placeholders (`--board` = JPEG ≤960px for 5 MB caps) |
| `variants` | Light PDF per public palette → `_variants/<stem>/` |
| `merge_pdfs` | Bundle PDFs; optional US Letter size check |
| `pdf_to_png` | Screenshot each `.page` (agent visual verify) |
| `check_generation` | 12 deterministic document checks; local-first public workflow; source/dependency hashes allow reuse |
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
| [`ROADMAP.md`](ROADMAP.md) | Product backlog and current plan pointer |
