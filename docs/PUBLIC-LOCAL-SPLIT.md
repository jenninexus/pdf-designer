# Public vs local split — pdf-designer

This repository **is public MIT**:
[github.com/jenninexus/pdf-designer](https://github.com/jenninexus/pdf-designer).

Treat every **tracked** file as product + engine material a stranger can clone
without inheriting machine paths, private vaults, real job applications, brand
hex maps, or SEGO session ritual.

The **free product** is that clone. A possible paid app is a thin installer/wizard
over the same engine later — not a second feature set, and not a reason to delay
clone-safe fixes. Boundary audit: [`PUBLIC-RELEASE-AUDIT.md`](PUBLIC-RELEASE-AUDIT.md).
Thesis: [`PRODUCT.md`](PRODUCT.md).

Sibling pattern: [`agency/docs/PUBLIC-LOCAL-SPLIT.md`](../../agency/docs/PUBLIC-LOCAL-SPLIT.md)
(framework agents). Same idea here for a **résumé / PDF toolkit**.

| Layer | On GitHub | Local only |
|---|---|---|
| Engine | `src/pdf_tool/`, `themes/` (including licensed `themes/fonts/`), `layouts/`, QA guards | — |
| Product story | [`PRODUCT.md`](PRODUCT.md) · [`examples/resume-studio/`](../examples/resume-studio/) | [`MARKETING.md`](MARKETING.md) (gitignored) |
| Folder UX | [`WORKSPACE-LAYOUT.md`](WORKSPACE-LAYOUT.md) · [`STORAGE.md`](STORAGE.md) (alias notes) | Real data under root nouns; leftover `storage/` |
| Generated files | [`../output/README.md`](../output/README.md) (layout only) | `output/**/*.pdf` · `output/**/*.png` |
| Clone path | [`GETTING-STARTED.md`](GETTING-STARTED.md) | — |
| Protocol (rules) | [`VAULT.md`](VAULT.md) · [`JOB-ASSESSMENT.md`](JOB-ASSESSMENT.md) | Real vaults / listings / PII |
| Commands | `.claude/commands/*.example.md` only | Bare `start` / `wrap` / `make-*` / commands `README` + generated `.codex/` adapters |
| Config | `.config/mcp-pdf-designer.example.json` | `mcp-pdf-designer.json` (absolute paths) |
| Theme kit | Public default themes in-repo | `www-theme-kit` profiles + `brands/` (private kits) |
| Docs | This folder (public `*.md`) | `MARKETING.md` · `WORKSPACE.md` · `HISTORY-SCRUB.md` · `CHANNELS.local.md` · `WINDOWS-ELECTRON.local.md` · other `*.local.md` · `Plans/` |
| Lessons | `.memory/README.md` · `.memory/lesson-*.md` | Other `.memory/` notes · `dev-log-sego.yaml` |

## Track public files

Commit when they are clone-safe and reusable:

- `src/pdf_tool/` — HTML→PDF, Design Hub, guards, collage
- `themes/` · `layouts/` · `examples/` (incl. `resume-studio/`)
- `docs/*.md` — engine, product, protocol **except** gitignored private notes listed below
- `README.md` · `LICENSE` · contributor map `AGENTS.md` (keep it clone-safe; no vault bodies)
- `.claude/commands/*.example.md` — generalized protocol seeds; placeholders only
- `.config/*.example.json` · `.vscode/mcp.json.example`
- `.memory/lesson-*.md` — durable traps (no vault bodies)
- `output/README.md` — where generated PDFs go; never the PDFs themselves
- `users/examples.json` · `vaults/examples.json` · `profiles/examples.json` — fictional Jane Example so the Hub Vault and profile dropdown have a clone-safe card. Copy-me seeds stay `*.example.json`.
- `_job-apps/_template/README.md` — generic folder-shape pointer only. Real listings, provider-specific material, employer notes, submission evidence, phone numbers, and real names never belong in this tracked tree.

## Keep local files untracked

Never commit from a personal machine:

| Path | Why |
|---|---|
| Root nouns (`users/` · `vaults/` · `resumes/` · …) real files; leftover `storage/` | Vaults, contacts, source HTML, exports |
| `output/*` except `output/README.md` | Generated PDFs/PNGs |
| `docs/MARKETING.md` · `WORKSPACE.md` · `HISTORY-SCRUB.md` · `docs/*.local.md` | SEGO marketing, channel/signing ops, machine paths, rewrite runbooks |
| `Plans/` | Local engineering checklists |
| `.claude/commands/{start,wrap,pdf-start,pdf-wrap,README,make-*}.md` | Dev ritual + personal specifics |
| `.codex/` | Generated local adapters for the bare commands |
| `.config/mcp-pdf-designer.json` | Absolute machine paths |
| `dev-log-sego.yaml` | Session narrative with private paths |
| `*.pdf` / `*.png` (except deliberate example fixtures under `docs/images/`) | Exports / captures |

### Named public seeds, not broad private-root exceptions

The smoke gate permits the fictional Jane cards and `*.example.json` copy-me shapes by name and
suffix; it does **not** exempt a whole private-shaped directory. Add a public example under
`examples/` whenever possible. If a root-noun seed is truly needed, keep it fictional, list its
reason here, and add a narrow allowlist/test in the same change. This protects real applicants,
their contact details, and every real application from an accidental public push.

## Product surfaces (do not blur)

```
┌──────────────────────────────────────────────────────────────┐
│  PUBLIC — free GitHub (live) / optional TestPyPI later       │
│  pdf_tool + themes + layouts + Design Hub + *.example.md     │
│  docs: PRODUCT · GETTING-STARTED · VAULT shape · QA          │
│  output/README.md (layout) · examples/resume-studio/         │
│  demo: python scripts/smoke-white-label.py                   │
└──────────────────────────┬───────────────────────────────────┘
                           │ optional local data
┌──────────────────────────▼───────────────────────────────────┐
│  PRIVATE — your machine                                      │
│  vaults · jobs · brands · collages · output/*.pdf            │
│  MARKETING.md · bare /make-resume · /start · /wrap           │
└──────────────────────────┬───────────────────────────────────┘
                           │ future (hypothesis)
┌──────────────────────────▼───────────────────────────────────┐
│  PAID APP — thin shell over the same engine                  │
│  installer → Design Hub · guided vault/export wizard         │
│  never requires cloud vaults; never ships someone else's PII │
└──────────────────────────────────────────────────────────────┘
```

Thesis: [`PRODUCT.md`](PRODUCT.md). Clone without vaults: [`GETTING-STARTED.md`](GETTING-STARTED.md).
Private marketing detail: `docs/MARKETING.md` (gitignored).

## Theme kits (private — not the public product)

`www-theme-kit` / `syna-theme-kit` are **dev-only** brand registries on this network.
They are **not** published with the free GitHub résumé product.

| Kit profile | Owns | Public pdf-designer counterpart |
|---|---|---|
| `www-theme-kit/profiles/pdf-designer.json` | Design Hub chrome pointers | `src/pdf_tool/static/hub.css` + `themes/` |
| `www-theme-kit/profiles/resume.json` | Private studio résumé layout notes | `layouts/` + public `themes/default-resume.*` |
| `www-theme-kit/palettes/resume-palettes.json` | Audition / brand palette registry | `themes/presets/*.json` (public subset) |

Document tokens that strangers need live in **`themes/`**. Real studio hex stays in
`brands/`.

## Sibling repos (same split idea)

| Repo | Public | Private / local |
|---|---|---|
| **pdf-designer** (this) | Engine + product docs + examples + `output/` layout | Root-noun payload, bare commands, `Plans/` |
| **agency** | `agents/`, `docs/`, media masters | `projects/`, `mcp.json`, audits |
| **socials** | Generic `docs/` + MCP tools | `storage/docs/*` IDs, `.env`, brand YAMLs |
| **dashboard** | Seed profiles + fictional sample data | `my-dashboard/`, `.env` |
| **www-theme-kit** | *(network private kit — not a public app)* | Whole kit is SEGO/BEE brand infra |

## History hygiene

Files that once lived on `main` (bare commands, machine MCP config) can still exist in
**old SHAs**. Working-tree ignore is not enough — clones of those commits still see them.

- Runbook (local): `docs/HISTORY-SCRUB.md` (gitignored)
- Do **not** force-push until GitHub auth is confirmed and a human OK’s the rewrite
- Fast-forward of clone-safe `main` commits **is** how the public product stays current

## Related

- [`README.md`](README.md) — docs hub
- [`PUBLIC-RELEASE-AUDIT.md`](PUBLIC-RELEASE-AUDIT.md) — free vs paid vs local checklist
- [`STORAGE.md`](STORAGE.md) — layout protocol + `storage/` alias
- [`../output/README.md`](../output/README.md) — generated-file layout
- [`../AGENTS.md`](../AGENTS.md) — agent contracts (keep clone-safe)
