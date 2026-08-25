# Docs — pdf-designer

Index for product users and contributors. The root [`README.md`](../README.md) stays
short and public-facing; **public product detail lives here**.

## Public vs private

⭐ Full map: [`PUBLIC-LOCAL-SPLIT.md`](PUBLIC-LOCAL-SPLIT.md) · folder UX target: [`WORKSPACE-LAYOUT.md`](WORKSPACE-LAYOUT.md)

| On GitHub (clone-safe) | Local only (gitignored) |
|---|---|
| Public product docs · `themes/` · `layouts/` · `examples/` | Live vaults / brands / jobs / collages / exports (`_job-apps/` + `storage/` alias) |
| `.config/mcp-pdf-designer.example.json` | `mcp-pdf-designer.json` (machine paths) |
| `*.example.md` command seeds only | Bare `start`/`wrap`/`README`/`make-*.md` |
| [`PRODUCT.md`](PRODUCT.md) · [`GETTING-STARTED.md`](GETTING-STARTED.md) · `resume-studio/` | Operating plans, agent notes, application protocol records, and local marketing / workspace / history notes |

## Start here

| Doc | Owns |
|---|---|
| [`PUBLIC-LOCAL-SPLIT.md`](PUBLIC-LOCAL-SPLIT.md) | ⭐ Public vs local vs paid architecture |
| [`WORKSPACE-LAYOUT.md`](WORKSPACE-LAYOUT.md) | ⭐ Target root folders (`users/` · `vaults/` · …) for the free product |
| [`PRODUCT.md`](PRODUCT.md) | ⭐ Business / product direction (free GitHub + optional tip; installer is a later shell) |
| [`GETTING-STARTED.md`](GETTING-STARTED.md) | ⭐ Clone path without vaults |
| [`PUBLIC-RELEASE-AUDIT.md`](PUBLIC-RELEASE-AUDIT.md) | Free GitHub product vs local vs paid; clone-safety on public `main` |
| [`../examples/resume-studio/`](../examples/resume-studio/) | Public product front door |
| [`pdf-designer-overview.html`](pdf-designer-overview.html) · [`PDF`](pdf-designer-overview.pdf) | Browser-openable product overview + PDF rendered by this engine |
| [`images/README.md`](images/README.md) | Current public-only Hub screenshot set; prior captures are dated archives |
| [`PACKAGING.md`](PACKAGING.md) | PyPI / wheel spike |
| [`WINDOWS-LAUNCHER.md`](WINDOWS-LAUNCHER.md) | Windows-first local Design Hub launcher spike + acceptance checks |
| [`WINDOWS-ELECTRON.md`](WINDOWS-ELECTRON.md) | Pre-release Windows shell: unsigned packaging, Documents/OneDrive, clean-machine harness |
| [`VOICE-SEED-HANDOFF.md`](VOICE-SEED-HANDOFF.md) | Optional, public-safe voice-card boundary |
| [`QA.md`](QA.md) | Ship gate — `check_generation` |

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

## Local operating records

The active plan, agent runbook, working vault protocol, and application records stay
gitignored. They may contain local paths or personal working context and are not part
of the public product. The public walkthrough is the fictional
[`../examples/resume-studio/`](../examples/resume-studio/) example plus
[`GETTING-STARTED.md`](GETTING-STARTED.md).

### Also (tracked, outside `docs/`)

| Path | Owns |
|---|---|
| [`../themes/PALETTE-RULES.md`](../themes/PALETTE-RULES.md) | No brown / mustard / lime + guard |
| [`../layouts/README.md`](../layouts/README.md) | Layout recipes — structure (themes own color) |
| [`../.claude/commands/*.example.md`](../.claude/commands/) | Public protocol seeds only |

### Privacy

Root workspace nouns (`users/` · `vaults/` · `_job-apps/` · …) are **gitignored** except for
tracked `README` scaffolds and `*.example.json`; real JSON/HTML stay ignored. `storage/` is
retired and accepted only as an old-path alias. Public docs must not include machine pointers,
personal data, or operational history. One checkout; no `.env` (the engine reads none).
