# Docs — pdf-designer

Index for humans and agents. The root [`README.md`](../README.md) stays short and
public-facing; **detail lives here**. Agent contracts: [`../AGENTS.md`](../AGENTS.md).

## Public vs private

| On GitHub (clone-safe) | Local only (`storage/` — never pushed) |
|---|---|
| This folder · `AGENTS.md` · `themes/` · `layouts/` · `examples/` | Vaults, brands, jobs, collages, exports |
| `.config/mcp-pdf-designer.example.json` | `mcp-pdf-designer.json` (machine paths) |
| `*.example.md` command seeds | Bare `make-resume.md` / `make-cover-letter.md` / `make-work-examples.md` |
| [`PRODUCT.md`](PRODUCT.md) thesis | `storage/docs/MARKETING.md` · `WORKSPACE.md` |

## Start here

| Doc | Owns |
|---|---|
| [`SSOT.md`](SSOT.md) | ⭐ Dashboard — owns vs points elsewhere; engine CLI map |
| [`PRODUCT.md`](PRODUCT.md) | ⭐ **Business / product direction** — free GitHub core vs future paid app |
| [`WHITE-LABEL.md`](WHITE-LABEL.md) | Public-only reuse (examples + themes, **no** vaults) — *not* the business plan |
| [`PACKAGING.md`](PACKAGING.md) | PyPI / wheel spike — must ship `themes/` + `layouts/` (not just `pdf_tool/*.py`) |
| [`../layouts/cover-letter/one-page-letter.json`](../layouts/cover-letter/one-page-letter.json) | ⭐ **Cover-letter page model** — flowing sign-off, fit-to-one-page bands |
| [`QA.md`](QA.md) | ⭐ Ship gate — `check_generation` (judge the artifact) |
| [`ROADMAP.md`](ROADMAP.md) | Pointer to the active plan (`/jen:roadmap` entry point) |

## Engine & design

| Doc | Owns |
|---|---|
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | How the engine fits; guards; planned vs built |
| [`EXPORTS.md`](EXPORTS.md) | Commands, export paths, light/dark, guards, pagination traps |
| [`THEME-DESIGN.md`](THEME-DESIGN.md) | Token names, dual mode, page signature pin |
| [`LAYOUT-SYSTEM.md`](LAYOUT-SYSTEM.md) | Shared page model — pinned footer, margins, content-fit |
| [`PREVIEWER.md`](PREVIEWER.md) | Design Hub how-to |
| [`COLLAGE-DESIGN.md`](COLLAGE-DESIGN.md) | Layout families, canvas presets, backgrounds, fit |
| [`LICENSING-NOTES.md`](LICENSING-NOTES.md) | MIT honesty + AGPL removal story |

## Career protocol (private *data* lives in `storage/`)

These pages document the **protocol** (clone-safe). Real vaults and listings stay gitignored.

| Doc | Owns |
|---|---|
| [`STORAGE.md`](STORAGE.md) | Private workspace layout, brand SSOT, **shared MG gallery** |
| [`VAULT.md`](VAULT.md) | Claim rules, voice layers, role tracks, work-samples per-user rule |
| [`JOB-ASSESSMENT.md`](JOB-ASSESSMENT.md) | Listing capture / pay / gap-check protocol |
| [`APPLICATIONS.md`](APPLICATIONS.md) | One-folder-per-job workflow |

### Also (tracked, outside `docs/`)

| Path | Owns |
|---|---|
| [`../themes/PALETTE-RULES.md`](../themes/PALETTE-RULES.md) | No brown / mustard / lime + guard |
| [`../themes/GENERATION-RULES.md`](../themes/GENERATION-RULES.md) | House rules for all generated docs |
| [`../layouts/README.md`](../layouts/README.md) | Layout recipes — structure (themes own color) |
| [`../Plans/`](../Plans/) | Working roadmap (one active file) |
| [`../AGENTS.md`](../AGENTS.md) | ⭐ Single agent SSOT — capability map + contracts |
| [`../.claude/commands/make-resume.example.md`](../.claude/commands/make-resume.example.md) | `/make-resume` public seed |
| [`../.claude/commands/make-cover-letter.example.md`](../.claude/commands/make-cover-letter.example.md) | `/make-cover-letter` public seed |
| [`../.claude/commands/make-work-examples.example.md`](../.claude/commands/make-work-examples.example.md) | `/make-work-examples` public seed |
| [`../.claude/commands/make-collage.md`](../.claude/commands/make-collage.md) | `/make-collage` routine |

### Privacy

`storage/` is **gitignored** — vaults, real brands, applications, fonts, images, and
`storage/docs/` (personal notes). Tracked docs stay clone-safe; machine pointers belong in
local `.config/mcp-pdf-designer.json` (seed: [`.example.json`](../.config/mcp-pdf-designer.example.json)).
