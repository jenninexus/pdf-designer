# Docs — pdf-designer

Index for humans and agents. The root [`README.md`](../README.md) stays short and
public-facing; **detail lives here**. Agent contracts: [`../AGENTS.md`](../AGENTS.md).

## Public vs private

⭐ Full map: [`PUBLIC-LOCAL-SPLIT.md`](PUBLIC-LOCAL-SPLIT.md) · folder UX target: [`WORKSPACE-LAYOUT.md`](WORKSPACE-LAYOUT.md)

| On GitHub (clone-safe) | Local only (gitignored) |
|---|---|
| This folder · `AGENTS.md` · `themes/` · `layouts/` · `examples/` | Live vaults / brands / jobs / collages / exports (`_job-apps/` + `storage/` alias) |
| `.config/mcp-pdf-designer.example.json` | `mcp-pdf-designer.json` (machine paths) |
| `*.example.md` command seeds only | Bare `start`/`wrap`/`README`/`make-*.md` |
| [`PRODUCT.md`](PRODUCT.md) · [`GETTING-STARTED.md`](GETTING-STARTED.md) · `resume-studio/` | [`MARKETING.md`](MARKETING.md) · [`WORKSPACE.md`](WORKSPACE.md) · [`HISTORY-SCRUB.md`](HISTORY-SCRUB.md) (same `docs/` folder) |

## Start here

| Doc | Owns |
|---|---|
| [`PUBLIC-LOCAL-SPLIT.md`](PUBLIC-LOCAL-SPLIT.md) | ⭐ Public vs local vs paid architecture |
| [`WORKSPACE-LAYOUT.md`](WORKSPACE-LAYOUT.md) | ⭐ Target root folders (`users/` · `vaults/` · …) for the free product |
| [`PRODUCT.md`](PRODUCT.md) | ⭐ Business / product direction — résumé creator for a broken job market |
| [`GETTING-STARTED.md`](GETTING-STARTED.md) | ⭐ Clone path without vaults |
| [`../examples/resume-studio/`](../examples/resume-studio/) | Public product front door |
| [`pdf-designer-overview.html`](pdf-designer-overview.html) · [`PDF`](pdf-designer-overview.pdf) | Browser-openable product overview + PDF rendered by this engine |
| [`SSOT.md`](SSOT.md) | Dashboard — owns vs points elsewhere |
| [`PACKAGING.md`](PACKAGING.md) | PyPI / wheel spike |
| [`QA.md`](QA.md) | Ship gate — `check_generation` |
| [`ROADMAP.md`](ROADMAP.md) | Pointer to `Plans/_Active/` |

## Engine & design

| Doc | Owns |
|---|---|
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | How the engine fits; guards; planned vs built |
| [`EXPORTS.md`](EXPORTS.md) | Commands, export paths, light/dark, guards |
| [`THEME-DESIGN.md`](THEME-DESIGN.md) | Token names, dual mode, page signature pin |
| [`LAYOUT-SYSTEM.md`](LAYOUT-SYSTEM.md) | Shared page model — pinned footer, margins, content-fit |
| [`PREVIEWER.md`](PREVIEWER.md) | Design Hub how-to |
| [`COLLAGE-DESIGN.md`](COLLAGE-DESIGN.md) | Layout families, canvas presets, backgrounds, fit |
| [`LICENSING-NOTES.md`](LICENSING-NOTES.md) | MIT honesty + AGPL removal story |

## Career protocol (private *data* — `_job-apps/` + root nouns; `storage/` alias)

These pages document the **protocol** (clone-safe). Real vaults and listings stay gitignored.

| Doc | Owns |
|---|---|
| [`WORKSPACE-LAYOUT.md`](WORKSPACE-LAYOUT.md) | ⭐ **Target** root workspace for the public product |
| [`STORAGE.md`](STORAGE.md) | **Live** root-noun layout; retired `storage/` URL aliases |
| [`VAULT.md`](VAULT.md) | Claim rules, voice layers, role tracks |
| [`JOB-ASSESSMENT.md`](JOB-ASSESSMENT.md) | Listing capture / pay / gap-check protocol |
| [`APPLICATIONS.md`](APPLICATIONS.md) | One-folder-per-job workflow |

### Also (tracked, outside `docs/`)

| Path | Owns |
|---|---|
| [`../themes/PALETTE-RULES.md`](../themes/PALETTE-RULES.md) | No brown / mustard / lime + guard |
| [`../layouts/README.md`](../layouts/README.md) | Layout recipes — structure (themes own color) |
| [`../Plans/`](../Plans/) | Working roadmap (one active file) |
| [`../AGENTS.md`](../AGENTS.md) | Single agent SSOT |
| [`../.claude/commands/*.example.md`](../.claude/commands/) | Public protocol seeds only |

### Privacy

Root workspace nouns (`users/` · `vaults/` · `_job-apps/` · …) are **gitignored** except for
tracked READMEs + `*.example.json`; real JSON/HTML stay ignored. `storage/` is retired and only
accepted as an old-path alias. Tracked docs stay clone-safe;
machine pointers belong in local `.config/mcp-pdf-designer.json`. **Do not** copy
`storage/docs/` leftovers into this public index — private notes already live as gitignored
[`MARKETING.md`](MARKETING.md) · [`WORKSPACE.md`](WORKSPACE.md) · [`HISTORY-SCRUB.md`](HISTORY-SCRUB.md).
One checkout; no `.env` (engine reads none).
