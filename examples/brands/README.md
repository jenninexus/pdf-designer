# `examples/brands/` — public brand-map pattern (no personal data)

Private brand palettes for real projects live in **`storage/brands/`** (gitignored).
This folder is the **tracked template** so a future user (or a fresh clone) knows the shape.

## Where colors live

| Layer | Path | Tracked? | Owns |
|---|---|---|---|
| Live website brand | `www-theme-kit/profiles/<site>.json` (or syna-theme-kit) | yes (kit repo) | Production site primary/secondary/accent |
| Resume kit mirror | `www-theme-kit/palettes/resume-palettes.json` | yes (kit repo) | Print-safe light+dark maps for résumé surfaces |
| pdf-designer private map | `storage/brands/brand-<name>.json` | **no** | Token map the Design Hub / exports actually load |
| pdf-designer public default | `themes/default-resume.{json,css}` | **yes** | Brand-neutral engine default |

**Rule:** personal contact, vaults, applications, and private brand files stay under `storage/`.
Never put real emails, employers, or private paths into `themes/` or `examples/`.

## How to add your brand

1. Copy [`brand-example.json`](brand-example.json) → `storage/brands/brand-<yours>.json`.
2. Map from your website profile (`www-theme-kit/profiles/...`) into the pdf-designer token names (`--primary`, `--secondary`, `--accent`, `--support`, surfaces, text).
3. Derive a **light** print map that obeys [`../../themes/PALETTE-RULES.md`](../../themes/PALETTE-RULES.md) — never darken amber/gold into brown; hand that role to another hue already in the palette.
4. Point your `storage/profiles/<you>-resume.json` → `theme.default` at that brand file.
5. Run `python -m pdf_tool.check_palette --scan storage/` before export.

## Worked MG example (structure only)

Live site: molten orange `FF6B00` + hot secondary `FF4500` + violet `8B5CF6` + cyan `42F4C8`.
Private map name: `storage/brands/brand-martian.json`.
Kit mirror: `resume-palettes.json#martian-resume`.
