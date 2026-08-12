# Public vs local split — pdf-designer

This repository is (or will be) **public MIT**. Treat tracked files as product +
engine material that a stranger can clone without inheriting machine paths,
private vaults, real job applications, brand hex maps, or SEGO session ritual.

Sibling pattern: [`agency/docs/PUBLIC-LOCAL-SPLIT.md`](../../agency/docs/PUBLIC-LOCAL-SPLIT.md)
(framework agents). Same idea here for a **résumé / PDF toolkit**.

| Layer | On GitHub | Local only (`storage/` + gitignored ritual) |
|---|---|---|
| Engine | `src/pdf_tool/`, `themes/`, `layouts/`, QA guards | — |
| Product story | [`PRODUCT.md`](PRODUCT.md) · [`examples/resume-studio/`](../examples/resume-studio/) | [`../storage/docs/MARKETING.md`](../storage/docs/MARKETING.md) |
| Clone path | [`GETTING-STARTED.md`](GETTING-STARTED.md) | — |
| Protocol (rules) | [`VAULT.md`](VAULT.md) · [`STORAGE.md`](STORAGE.md) · [`JOB-ASSESSMENT.md`](JOB-ASSESSMENT.md) | Real vaults / listings / PII |
| Commands | `.claude/commands/*.example.md` only | Bare `start` / `wrap` / `make-*` / commands `README` |
| Config | `.config/mcp-pdf-designer.example.json` | `mcp-pdf-designer.json` (absolute paths) |
| Theme kit | Public default themes in-repo | `www-theme-kit` profiles + `storage/brand-design/` (private kits) |
| Docs index | This folder + tracked [`../storage/docs/README.md`](../storage/docs/README.md) placeholder | Full private notes under `storage/docs/` |

## Track public files

Commit when they are clone-safe and reusable:

- `src/pdf_tool/` — HTML→PDF, Design Hub, guards, collage
- `themes/` · `layouts/` · `examples/` (incl. `resume-studio/`)
- `docs/*.md` — engine, product, protocol **without** real employer/PII
- `AGENTS.md` · `README.md` · `Plans/` (engineering checklists)
- `.claude/commands/*.example.md` — generalized protocol seeds
- `.config/*.example.json` · `.vscode/mcp.json.example`
- `.memory/lesson-*.md` — durable traps (no vault bodies)
- Tracked placeholder: `storage/docs/README.md` (index only)

## Keep local files untracked

Never commit from a personal machine:

| Path | Why |
|---|---|
| `storage/users/`, `storage/<user>/`, `storage/profiles/` | Vaults, contacts, `characterVoice` |
| `storage/_job-listings/` | Real listings, pay, apply URLs |
| `storage/brand-design/` | Studio / personal palettes + chrome CSS |
| `storage/collages/`, `*_exports/` | Real image sets + PDFs |
| `storage/docs/MARKETING.md`, `WORKSPACE.md`, `HISTORY-SCRUB.md`, … | SEGO marketing, machine paths, rewrite runbooks |
| `.claude/commands/{start,wrap,pdf-wrap,README,make-*}.md` | Dev ritual + personal specifics |
| `.config/mcp-pdf-designer.json` | Absolute machine paths |
| `dev-log-sego.yaml` | Session narrative with private paths |
| `*.pdf` / `*.png` (except deliberate example fixtures) | Exports / captures |

## Product surfaces (do not blur)

```
┌──────────────────────────────────────────────────────────────┐
│  PUBLIC — free GitHub / future PyPI                          │
│  pdf_tool + themes + layouts + Design Hub + *.example.md     │
│  docs: PRODUCT · GETTING-STARTED · VAULT shape · QA          │
│  demo: examples/resume-studio/ + smoke-white-label.py        │
└──────────────────────────┬───────────────────────────────────┘
                           │ optional local data
┌──────────────────────────▼───────────────────────────────────┐
│  PRIVATE — your machine                                      │
│  storage/ vaults · jobs · brands · collages · MARKETING.md   │
│  bare /make-resume · /start · /wrap                          │
└──────────────────────────┬───────────────────────────────────┘
                           │ future (hypothesis)
┌──────────────────────────▼───────────────────────────────────┐
│  PAID APP — thin shell over the same engine                  │
│  installer → Design Hub · guided vault/export wizard         │
│  never requires cloud vaults; never ships someone else's PII │
└──────────────────────────────────────────────────────────────┘
```

Thesis: [`PRODUCT.md`](PRODUCT.md). Clone without vaults: [`GETTING-STARTED.md`](GETTING-STARTED.md).
Private marketing detail: `storage/docs/MARKETING.md`.

## Theme kits (private — not the public product)

`www-theme-kit` / `syna-theme-kit` are **dev-only** brand registries on this network.
They are **not** published with the free GitHub résumé product.

| Kit profile | Owns | Public pdf-designer counterpart |
|---|---|---|
| `www-theme-kit/profiles/pdf-designer.json` | Design Hub chrome pointers | `src/pdf_tool/static/hub.css` + `themes/` |
| `www-theme-kit/profiles/resume.json` | Private MG/Shade résumé layout notes | `layouts/` + public `themes/default-resume.*` |
| `www-theme-kit/palettes/resume-palettes.json` | Audition / brand palette registry | `themes/presets/*.json` (public subset) |

Document tokens that strangers need live in **`themes/`**. Real studio hex stays in
`storage/brand-design/`.

## Sibling repos (same split idea)

| Repo | Public | Private / local |
|---|---|---|
| **pdf-designer** (this) | Engine + product docs + examples | `storage/`, bare commands |
| **agency** | `agents/`, `docs/`, media masters | `projects/`, `mcp.json`, audits |
| **socials** | Generic `docs/` + MCP tools | `storage/docs/*` IDs, `.env`, brand YAMLs |
| **dashboard** | Seed profiles + fictional sample data | `my-dashboard/`, `.env` |
| **www-theme-kit** | *(network private kit — not a public app)* | Whole kit is SEGO/BEE brand infra |

## History hygiene

Files that once lived on `main` (bare commands, machine MCP config) must be
**removed from git history** before a wide public launch. Working tree ignore is
not enough — clones of old SHAs still see them.

- Runbook (local): `storage/docs/HISTORY-SCRUB.md`
- Do **not** force-push until `jenninexus` GitHub auth is confirmed and a human OK’s the rewrite

## Related

- [`README.md`](README.md) — docs hub
- [`STORAGE.md`](STORAGE.md) — layout protocol for the private tree
- [`../AGENTS.md`](../AGENTS.md) — agent contracts
- [`../storage/docs/README.md`](../storage/docs/README.md) — private index placeholder
