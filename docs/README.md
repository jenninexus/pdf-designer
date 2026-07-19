# Docs — pdf-designer

Index for humans and agents. The root [`README.md`](../README.md) stays short and
public-facing; **detail lives here**. Agent contracts: [`../AGENTS.md`](../AGENTS.md).

| Doc | Owns |
|---|---|
| [`SSOT.md`](SSOT.md) | ⭐ Dashboard — owns vs points elsewhere; engine CLI map |
| [`WHITE-LABEL.md`](WHITE-LABEL.md) | Public-only reuse (examples + themes, no vaults) |
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | How the engine fits; guards; planned vs built |
| [`EXPORTS.md`](EXPORTS.md) | Commands, export paths, light/dark, guards, pagination traps |
| [`THEME-DESIGN.md`](THEME-DESIGN.md) | Token names, dual mode, page signature pin |
| [`LAYOUT-SYSTEM.md`](LAYOUT-SYSTEM.md) | ⭐ Shared page model — pinned footer, per-doc margins/rhythm, work-samples build |
| [`PREVIEWER.md`](PREVIEWER.md) | Design Hub how-to |
| [`COLLAGE-DESIGN.md`](COLLAGE-DESIGN.md) | Layout families + canvas presets (SSOT table) |
| [`STORAGE.md`](STORAGE.md) | Private workspace layout + brand color SSOT |
| [`VAULT.md`](VAULT.md) | Claim rules, voice layers, role tracks |
| [`JOB-ASSESSMENT.md`](JOB-ASSESSMENT.md) | Listing capture / pay / gap-check protocol |
| [`APPLICATIONS.md`](APPLICATIONS.md) | One-folder-per-job workflow |
| [`LICENSING-NOTES.md`](LICENSING-NOTES.md) | MIT honesty + AGPL removal story |

### Also (tracked, outside `docs/`)

| Path | Owns |
|---|---|
| [`../themes/PALETTE-RULES.md`](../themes/PALETTE-RULES.md) | No brown / mustard / lime + guard |
| [`../Plans/`](../Plans/) | Working roadmap (one active file) |
| [`../.claude/commands/make-resume.md`](../.claude/commands/make-resume.md) | `/make-resume` routine (agent-agnostic) |

### Privacy

`storage/` is **gitignored** — vaults, real brands, applications, fonts, chrome CSS.
Tracked docs never need absolute machine paths for the public story; private pointers
(voice-seed, theme kits, mcp breakpoints) live in [`SSOT.md`](SSOT.md) and
[`.config/mcp-pdf-designer.json`](../.config/mcp-pdf-designer.json).
