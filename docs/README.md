# Docs — pdf-designer

Index for product users and contributors. The root [`README.md`](../README.md) stays
a short GitHub postcard; **setup and product detail live here** (start at
[`GETTING-STARTED.md`](GETTING-STARTED.md)).

## Public vs private

⭐ Start with the [`public app vs personal workspace diagram`](WORKSPACE-LAYOUT.md#two-journeys-one-engine),
then use [`PUBLIC-LOCAL-SPLIT.md`](PUBLIC-LOCAL-SPLIT.md) for the tracking/privacy rules.

| On GitHub (clone-safe) | Local only (gitignored) |
|---|---|
| Public product docs · `themes/` · `layouts/` · `examples/` | Live vaults / brands / jobs / collages / exports (`_job-apps/` + `storage/` alias) |
| `.config/mcp-pdf-designer.example.json` | `mcp-pdf-designer.json` (machine paths) |
| `*.example.md` command seeds only | Bare `start`/`wrap`/`README`/`make-*.md` |
| [`PRODUCT.md`](PRODUCT.md) · [`GETTING-STARTED.md`](GETTING-STARTED.md) · `resume-studio/` · optional public-safe product plan | Personal/session plans, agent notes, application records, and local marketing / workspace / history notes |

## Start here

| Doc | Owns |
|---|---|
| [`PUBLIC-LOCAL-SPLIT.md`](PUBLIC-LOCAL-SPLIT.md) | ⭐ Public vs local vs paid architecture |
| [`WORKSPACE-LAYOUT.md`](WORKSPACE-LAYOUT.md) | ⭐ Target root folders (`users/` · `vaults/` · …) for the free product |
| [`PRODUCT.md`](PRODUCT.md) | ⭐ Business / product direction (free GitHub + optional tip; installer is a later shell) |
| [`GETTING-STARTED.md`](GETTING-STARTED.md) | ⭐ Clone path without vaults |
| [`../examples/resume-studio/`](../examples/resume-studio/) | Public product front door |
| [`pdf-designer-overview.html`](pdf-designer-overview.html) · [`PDF`](pdf-designer-overview.pdf) | Browser-openable product overview + PDF rendered by this engine |
| [`images/README.md`](images/README.md) | Current public-only Hub screenshot set; prior captures are dated archives |
| [`PACKAGING.md`](PACKAGING.md) | PyPI / wheel spike |
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

## Workflow & local data

These remain separate because each owns a different decision boundary; they are not alternate getting-started guides.

| Doc | Owns |
|---|---|
| [`SSOT.md`](SSOT.md) | One-screen ownership map and authoritative-file lookup |
| [`STORAGE.md`](STORAGE.md) | Public/private folders, root nouns, aliases, and brand paths |
| [`VAULT.md`](VAULT.md) | Claim provenance, voice, role tracks, and vault schema |
| [`APPLICATIONS.md`](APPLICATIONS.md) | One-folder-per-job workflow and where application artifacts live |
| [`JOB-ASSESSMENT.md`](JOB-ASSESSMENT.md) | Apply-link, remote/pay, evidence, gap-check, and ATS assessment protocol |
| [`ROADMAP.md`](ROADMAP.md) | Durable product backlog plus the optional current execution-plan pointer |

## Compatibility pointer

[`WHITE-LABEL.md`](WHITE-LABEL.md) is intentionally only a redirect for older links. Its maintained
content lives in [`GETTING-STARTED.md`](GETTING-STARTED.md); do not grow a second white-label guide there.

## Historical records

Completed audits and superseded spikes live under [`_archive/`](_archive/). They preserve evidence but
are not current instructions. The maintained authorities remain the docs listed above.

## Local operating records

Personal/session plans, agent runbooks, working vault payload, and application records stay
gitignored. All of `Plans/` is local-only working context; the public backlog is
[`ROADMAP.md`](ROADMAP.md). The public walkthrough is the fictional
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

The local Design Hub can still browse ignored `_exports/` PDFs and images: select **Exports** in
Library. Those artifact cards are read-only and exist only on loopback; the
public repository continues to track the folder README, never the payload.
