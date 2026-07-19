# SSOT Dashboard — pdf-designer

```
SSOT Dashboard — pdf-designer
─────────────────────────────
Config:    .config/mcp-pdf-designer.json ✓
Env:       none by design (no .env) ✓
Protocol:  AGENTS.md → docs/{STORAGE,VAULT,JOB-ASSESSMENT,ARCHITECTURE}.md → /make-resume
Theme:     themes/default-resume.{json,css} + themes/presets/* + PALETTE-RULES.md
Private:   storage/brands, users, vaults (gitignored)
Hub:       python -m pdf_tool.preview → :8787 (workspace auto-starts via scripts/ensure-design-hub.ps1)
Engine:    python -m pdf_tool  (hub) / individual modules
Plans:     Plans/_Active/2026-07-14-professional-product-roadmap.md
```

Compact map of what this repo owns vs what it only points at. Agents: start here, then
[`AGENTS.md`](../AGENTS.md). Humans shipping without private vaults:
[`WHITE-LABEL.md`](WHITE-LABEL.md).

---

## Owns here

| Surface | Path | Role |
|---|---|---|
| Engine | `src/pdf_tool/` | HTML→PDF, guards, collage, Design Hub, tracker |
| Public themes | `themes/default-resume.{json,css}`, `themes/presets/*` | Token SSOT + audition palettes |
| Page layout | `docs/LAYOUT-SYSTEM.md` + `themes/default-resume.{json,css}#document` | ⭐ Equal margins (0.65in default) + header-flows/footer-pins; one knob `--resume-page-margin`; content-fit rule |
| Page signature | `themes/default-resume.json#document.signature` | Bottom-right page-footer pin (`.page` / `.page-main` / `.page-sig`) |
| Previewer | `src/pdf_tool/preview.py` (`docs/PREVIEWER.md`) | Design Hub; **auto-refreshes** via `/api/version` on new exports |
| Palette rule | `themes/PALETTE-RULES.md` | No brown / mustard / lime — enforced by `check_palette` |
| Protocol docs | `docs/{STORAGE,VAULT,JOB-ASSESSMENT,ARCHITECTURE}.md` | Claim rules + workflow |
| Agent map | `AGENTS.md` | Capability / command SSOT for assistants |
| Make-resume | `.claude/commands/make-resume.md` | Job-application routine |
| Public examples | `examples/profiles/`, `examples/brands/`, `examples/applications/` | Clone-safe templates |
| Project config | `.config/mcp-pdf-designer.json` | Breakpoint pointer, hub, voice/external pointers |
| Active plan | `Plans/_Active/2026-07-14-professional-product-roadmap.md` | What to build next |

---

## Points elsewhere (never duplicate)

| Concern | Owning SSOT |
|---|---|
| Breakpoints numbers | `C:\mcp\.config\mcp-breakpoints.json` + www-theme-kit SCSS |
| Resume palette kit catalog | `www-theme-kit/palettes/resume-palettes.json` |
| Hub chrome profile | `www-theme-kit/profiles/pdf-designer.json` |
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
| `check_palette` | Reject brown / mustard / lime before export |
| `check_vault` | Vault schema / `--explain` / `--coverage` |
| `check_ats` | ATS text-layer sanity on light PDF |
| `audit_resume` | Diff rendered HTML vs vault (lead omissions) |
| `tracker` | List / status over `storage/applications/**/application.json` |
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
| [`Plans/_Active/…`](../Plans/_Active/2026-07-14-professional-product-roadmap.md) | Working checklist |
