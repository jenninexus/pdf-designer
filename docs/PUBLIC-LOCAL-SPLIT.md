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
| Generated files | [`STORAGE.md`](STORAGE.md) (canonical export layout) · [`../_exports/README.md`](../_exports/README.md) (fallback export layout) · [`../output/README.md`](../output/README.md) (automation scratch contract) | Exports beside their document family (`resumes/`, `collages/`), plus `_exports/` and `output/` payloads |
| Clone path | [`GETTING-STARTED.md`](GETTING-STARTED.md) | — |
| Protocol (rules) | [`VAULT.md`](VAULT.md) · [`JOB-ASSESSMENT.md`](JOB-ASSESSMENT.md) | Real vaults / listings / PII |
| Commands | `.claude/commands/*.example.md` only | Bare `start` / `wrap` / `make-*` / commands `README` + generated `.codex/` adapters |
| Config | `.config/mcp-pdf-designer.example.json` | `mcp-pdf-designer.json` (absolute paths) |
| Theme kit | Public default themes in-repo | `www-theme-kit` profiles + `brands/` (private kits) |
| Docs | This folder (public `*.md`) · optional one-plan public-safe execution slice · reviewed product history | `MARKETING.md` · `WORKSPACE.md` · `HISTORY-SCRUB.md` · `CHANNELS.local.md` · `WINDOWS-ELECTRON.local.md` · other `*.local.md` / `*.private.md` · personal/session plans |
| Lessons | `.memory/README.md` · `.memory/lesson-*.md` | Other `.memory/` notes · frozen `Plans/_Complete/_archive/dev-log-sego.yaml` |

## Exports live with their document family, one scratch area

Exports live **beside their document family**, not in one central library. Per-job résumé/cover-
letter/work-sample PDFs and PNGs go to `resumes/<profile>/<Track>/`; go-to/default packs export
flat into `resumes/<profile>/`; studio exports live under `resumes/studio/…`; collage exports land
at the collage project root, `collages/<project>/`. `_exports/` is the **fallback only** — public
examples use `_exports/examples/`; sources with no inferred profile, kind, or project use
`_exports/unfiled/`. The Hub presents the union of these as **Exports** and scans them read-only.

`output/` is deliberately different: disposable smoke-test, packaging, benchmark, and automation
scratch chosen with an explicit `--output-dir output/...`. It is not scanned by the Hub and must not be
used as a final/submitted-document path. Public and private users therefore learn one export workflow
without tracking anyone's generated files.

## Track public files

Commit when they are clone-safe and reusable:

- `src/pdf_tool/` — HTML→PDF, Design Hub, guards, collage
- `themes/` · `layouts/` · `examples/` (incl. `resume-studio/`)
- `docs/*.md` — engine, product, protocol **except** gitignored private notes listed below
- `README.md` · `LICENSE` · contributor map `AGENTS.md` (keep it clone-safe; no vault bodies)
- `.claude/commands/*.example.md` — generalized protocol seeds; placeholders only
- `.config/*.example.json` · `.vscode/mcp.json.example`
- `.memory/lesson-*.md` — durable traps (no vault bodies)
- `_exports/README.md` — fallback export layout; never the payload itself
- `output/README.md` — explicit automation/test scratch layout; never the payload itself
- `users/examples.json` · `vaults/examples.json` · `profiles/examples.json` — fictional Jane Example so the Hub Vault and profile dropdown have a clone-safe card. Copy-me seeds stay `*.example.json`.
- `_job-apps/_template/README.md` — generic folder-shape pointer only. Real listings, provider-specific material, employer notes, submission evidence, phone numbers, and real names never belong in this tracked tree.

## Keep local files untracked

Never commit from a personal machine:

| Path | Why |
|---|---|
| Root nouns (`users/` · `vaults/` · `resumes/` · …) real files; leftover `storage/` | Vaults, contacts, source HTML, exports |
| `_exports/*` except `_exports/README.md` | Public-example exports and any source the engine can't match to a document family |
| `output/*` except `output/README.md` | Disposable smoke-test, packaging, benchmark, and automation scratch |
| `docs/MARKETING.md` · `WORKSPACE.md` · `HISTORY-SCRUB.md` · `docs/*.local.md` | SEGO marketing, channel/signing ops, machine paths, rewrite runbooks |
| Personal/application/session plans under `Plans/` | Local working context; only an explicitly unignored public-safe product slice and already-reviewed product history are public |
| `.claude/commands/{start,wrap,pdf-start,pdf-wrap,README,make-*}.md` | Dev ritual + personal specifics |
| `.codex/` | Generated local adapters for the bare commands |
| `.config/mcp-pdf-designer.json` | Absolute machine paths |
| `Plans/_Complete/_archive/dev-log-sego.yaml` | Frozen historical session log (do not append) |
| `*.pdf` / `*.png` (except deliberate example fixtures under `docs/images/`) | Exports / captures |

### Local visibility is not publication

The Design Hub discovers ignored finished files beside their document family — any PDF under
`resumes/`, images under `resumes/` (except `resources/`), files at a collage project root, plus
everything under `_exports/**/*.{pdf,png,jpg,jpeg,webp}` — and shows them as **read-only local
previews** under **Exports** at `127.0.0.1`. This does not weaken the privacy boundary: discovery is
runtime-only, the server remains loopback-only, `_archive` is skipped, and Git still tracks only
`resumes/README.md` / `_exports/README.md`. A public clone therefore shows the folder contract but
never another person's generated documents.

### Named public seeds, not broad private-root exceptions

The smoke gate permits the fictional Jane cards and `*.example.json` copy-me shapes by name and
suffix; it does **not** exempt a whole private-shaped directory. Add a public example under
`examples/` whenever possible. If a root-noun seed is truly needed, keep it fictional, list its
reason here, and add a narrow allowlist/test in the same change. This protects real applicants,
their contact details, and every real application from an accidental public push.

## Product surfaces (do not blur)

The authoritative public-app versus personal-workspace diagram and path lookup table live in
[`WORKSPACE-LAYOUT.md`](WORKSPACE-LAYOUT.md#two-journeys-one-engine). In short: the public clone provides
the engine, Wizard, examples, themes, layouts, and `*.example` seeds; local users add ignored root-noun
data and receive private deliverables beside their document family (`resumes/<profile>/…`,
`collages/<project>/`, `_exports/` as fallback); a future paid shell wraps the same Hub and
renderer rather than creating a second product.

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
| **pdf-designer** (this) | Engine + product docs + examples + public-safe product plan/history + `_exports/`/`output/` layout guides | Root-noun payload, generated deliverables, bare commands, personal/session plans |
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
- [`../_exports/README.md`](../_exports/README.md) — fallback export layout (see `STORAGE.md` for the family-local default)
- [`../output/README.md`](../output/README.md) — automation/test scratch layout
- [`../AGENTS.md`](../AGENTS.md) — agent contracts (keep clone-safe)
