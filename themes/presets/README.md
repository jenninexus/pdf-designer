# Public resume color presets

These are **brand-neutral** audition palettes for the Design Hub palette swapper.
Personal/studio brands stay in gitignored `storage/brand-design/`.

| File | Aesthetic | Lineage |
|---|---|---|
| `../default-resume.json` | Cool teal / gold / violet (engine default) | pdf-designer |
| `slate-ink.json` | Classic navy professional | original |
| `ocean-breeze.json` | Calm blues/teals | syna `#ocean` |
| `synagentic.json` | Teal + violet glass | syna synagentic / synabrain |
| `void-circuit.json` | Violet circuits | syna `#void-circuit` |
| `cinematic-studio.json` | Muted cinematic cool | syna `#cinematic-studio` |
| `midnight-chrome.json` | Midnight blue chrome | syna midnight-chrome skin |

**Private brands (also loaded by Design Hub):** `storage/brand-design/brand-synagen.json` (Shade Default/AI — orchid-**violet** + iridescent-**cyan**, ⛔ no magenta), `brand-martian.json` (studio), `brand-jenninexus.json` (Jenni).

**User prefs are pointers only** — `storage/users/{jenni,shade}.json#brandTheme.ssot` → the matching `brand-*.json` above. Hex lives in brand maps, never in the person file. Design Hub person filter only filters the library; it does not auto-pick a palette.

Registry mirror (kit): `www-theme-kit/palettes/resume-palettes.json` (7 public presets + default-resume + martian-resume).  
Rules: [`../PALETTE-RULES.md`](../PALETTE-RULES.md)  
Breakpoints SSOT: [`.config/mcp-pdf-designer.json#breakpoints`](../../.config/mcp-pdf-designer.json)
