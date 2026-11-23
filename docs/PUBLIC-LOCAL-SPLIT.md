# Public vs local split — pdf-designer

This repository **is public MIT**:
[github.com/jenninexus/pdf-designer](https://github.com/jenninexus/pdf-designer).

Treat every **tracked** file as product + engine material a stranger can clone
without inheriting machine paths, private vaults, real job applications, brand
hex maps, or a maintainer's session ritual.

The **free product** is the clone. The planned Windows app packages the same engine and Hub. Thesis: [`PRODUCT.md`](PRODUCT.md). The completed release-boundary audit is retained locally in `storage/docs/_archive/`.

| Layer | On GitHub | Local only |
|---|---|---|
| Engine | `src/pdf_tool/`, `themes/` (including licensed `themes/fonts/`), `layouts/`, QA guards | — |
| Product story | [`PRODUCT.md`](PRODUCT.md) · [`examples/resume-studio/`](../examples/resume-studio/) | `storage/docs/MARKETING.md` |
| Folder UX | [`WORKSPACE-LAYOUT.md`](WORKSPACE-LAYOUT.md) · [`STORAGE.md`](STORAGE.md) (alias notes) | Real data under root nouns; leftover `storage/` |
| Generated files | [`STORAGE.md`](STORAGE.md) (canonical export layout) · [`EXPORTS.md`](EXPORTS.md) (fallback export layout) · [`../output/README.md`](../output/README.md) (automation scratch contract) · [`APPLICATIONS.md`](APPLICATIONS.md) § freeze what you sent | Exports beside their document family (`resumes/`, `collages/`) — including every `submitted-*` sent-artifact folder, which is a permanent record — plus `_exports/` and `output/` payloads |
| Clone path | [`GETTING-STARTED.md`](GETTING-STARTED.md) | — |
| Protocol (rules) | [`VAULT.md`](VAULT.md) · [`JOB-ASSESSMENT.md`](JOB-ASSESSMENT.md) | Real vaults / listings / PII |
| Commands | `.claude/commands/*.example.md` only | Bare `start` / `wrap` / `make-*` / commands `README` + generated `.codex/` adapters |
| Config | `.config/mcp-pdf-designer.example.json` | `mcp-pdf-designer.json` (absolute paths) |
| Theme kit | Public default themes in-repo | `www-theme-kit` profiles + `brands/` (private kits) |
| Docs | This folder (public `*.md`) | `storage/docs/` for operations and history · all `Plans/` for local work |
| Lessons | `.memory/README.md` · `.memory/lesson-*.md` | Other `.memory/` notes · frozen `Plans/_complete/_archive/dev-log-sego.yaml` |

## Root files and ownership

| Path | Public or local | Purpose |
|---|---|---|
| [README.md](../README.md) | Public | Product introduction, setup, and the example gallery. |
| [LICENSE](../LICENSE) | Public | MIT license for this repository. Bundled fonts carry their notices in `themes/fonts/`. |
| [AGENTS.md](../AGENTS.md) and [CLAUDE.md](../CLAUDE.md) | Public | Contributor contract and its compatibility pointer. |
| [.gitignore](../.gitignore) and [.gitattributes](../.gitattributes) | Public | Private path exclusions and portable hook line endings. |
| `pdf-designer.code-workspace` | Local | Machine-specific editor setup and private extension folder. |
| `docs/` and `assets/public/` | Public | Product documentation and reviewed example screenshots or overview assets. |
| `storage/docs/` and `Plans/` | Local | Maintainer docs, recovery evidence, and session plans. Neither is tracked by public Git. |
| `.vscode/` | Mixed | Opt-in `tasks.json.example` and `mcp.json.example`. Active tasks, MCP wiring and editor settings stay local. |
| `.claude/` | Mixed | Only `commands/*.example.md`. Plugin preferences, bare commands and other runtime files stay local. |
| `.config/` | Mixed | Optional `*.example.json` seeds, including the capture manifest. Active settings and privacy markers stay local. |
| `.memory/` | Mixed | Public reviewed lessons and their index. Other personal notes stay local. |
| `private/`, `.agents/`, `.codex/`, and `.local-artifacts/` | Local | Private add-ons, generated command adapters, and retained local output. |

Keep [AGENTS.md](../AGENTS.md) public as the contributor contract and [CLAUDE.md](../CLAUDE.md) as its short compatibility pointer. Operator sessions and machine setup live in ignored files.

## Scripts

| Location | Ownership |
|---|---|
| `scripts/` | Clone-safe Hub and document tools, privacy and packaging gates, captures of public examples, and release QA. Generic workspace sync utilities use settings supplied by the operator. |
| `storage/scripts/` | Private MCP preflight, context refresh for the maintainer's installed services, and legacy studio workspace migration. Public clones and packages exclude these scripts. |
| `desktop/scripts/` | Source recipes for packaging the public desktop shell. Publisher settings, credentials, generated runtimes and release binaries stay local. |

## Local execution and applicant ownership

Public users run the renderer, deterministic QA and preview locally. They do not need another PC,
a private service, theme-kit checkout or agent subscription. A maintainer's optional network
routing belongs to private operating instructions. See [QA.md](QA.md) for one final gate and cheap
receipt reuse; document QA does not require an LLM call.

Every person owns their identity, vault and one rendering profile. Reusable specialist résumés
select that person's sourced claims; per-posting application records own actual sent files and
responses. Neither a sample profile nor another person's skill is an applicant default. The public
demo uses fictional data. A future commercial installer creates a customer's own local workspace;
it never ships the maintainers' vaults, correspondence, palettes or operational plans.

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
- `output/README.md` — explicit automation/test scratch layout; never the payload itself
- `users/examples.json` · `vaults/examples.json` · `profiles/examples.json` — fictional Jane Example so the Hub Vault and profile dropdown have a clone-safe card. Copy-me seeds stay `*.example.json`.
- `_job-apps/_template/README.md` — generic folder-shape pointer only. Real listings, provider-specific material, employer notes, submission evidence, phone numbers, and real names never belong in this tracked tree.

## Keep local files untracked

Never commit from a personal machine:

| Path | Why |
|---|---|
| Root nouns (`users/` · `vaults/` · `resumes/` · …) real files; leftover `storage/` | Vaults, contacts, source HTML, exports |
| `_exports/` | Public-example exports and any source the engine can't match to a document family |
| `output/*` except `output/README.md` | Disposable smoke-test, packaging, benchmark, and automation scratch |
| `storage/docs/` | Private product publishing, roadmap, signing operations and recovery evidence |
| All of `Plans/` (personal, application, and session plans) | Local working context; never pushed (public repo rule 2026-09-30). Maintainer backlog: `storage/docs/ROADMAP.local.md` |
| `.claude/commands/{start,wrap,pdf-start,pdf-wrap,README,make-*}.md` | Dev ritual + personal specifics |
| `.codex/` | Generated local adapters for the bare commands |
| `.config/mcp-pdf-designer.json` | Absolute machine paths |
| `Plans/_complete/_archive/dev-log-sego.yaml` | Frozen historical session log (do not append) |
| `*.pdf` / `*.png` (except the approved product assets under `assets/public/`) | Exports / captures |

## Ongoing clone-safety gate

Before a public push:

0. Enable the enforced gate once per clone: `git config core.hooksPath .githooks`. Its pre-push
   hook ([`PRIVATE-SYNC.md`](PRIVATE-SYNC.md) § What the push gate checks) refuses any push that
   would publish a private path or a real person's identifiers; the steps below remain the habit.
   Share personal files between your own machines with `scripts/private-sync.py`, never via GitHub.
1. Stage explicit clone-safe paths; never use `git add -A` and never force-add ignored payload.
2. Keep public docs free of machine paths, private names, vault bodies, and operational credentials.
3. Treat `*.example.*` as a naming convention, not proof of safety; inspect its contents.
4. Run `python scripts/smoke-white-label.py` and `python scripts/check-wheel-assets.py` when engine,
   examples, or packaged assets change.
5. Require explicit human approval for any history rewrite or force-push. Ordinary fast-forward
   clone-safe commits remain the normal public-product update path.

### Local visibility is not publication

The Design Hub discovers ignored finished files beside their document family — any PDF under
`resumes/`, images under `resumes/` (except `resources/`), files at a collage project root, plus
everything under `_exports/**/*.{pdf,png,jpg,jpeg,webp}` — and shows them as **read-only local
previews** under **Exports** at `127.0.0.1`. This does not weaken the privacy boundary: discovery is
runtime-only, the server remains loopback-only, `_archive` is skipped, and Git still tracks only
`resumes/README.md` for this part of the workspace. A public clone therefore shows the folder contract but
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
Private marketing detail: `storage/docs/MARKETING.md` (gitignored).

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
| **pdf-designer** (this) | Engine + product docs + fictional examples + `output/` layout guide | Root-noun payload, generated deliverables, bare commands, all `Plans/` |
| **agency** | `agents/`, `docs/`, media masters | `projects/`, `mcp.json`, audits |
| **socials** | Generic `docs/` + MCP tools | `storage/docs/*` IDs, `.env`, brand YAMLs |
| **dashboard** | Seed profiles + fictional sample data | `my-dashboard/`, `.env` |
| **www-theme-kit** | *(network private kit — not a public app)* | Private kit infrastructure |

## History hygiene

Files that once lived on `main` (bare commands, machine MCP config) can still exist in
**old SHAs**. Working-tree ignore protects the current tree only; old commits remain accessible. Audit reachable history separately before deciding whether a targeted scrub is needed.

- Runbook (local): `storage/docs/HISTORY-SCRUB.md` (gitignored)
- Do **not** force-push without the required explicit owner authorization and a reviewed history-rewrite plan
- Fast-forward of clone-safe `main` commits **is** how the public product stays current

## Related

- [`README.md`](README.md) — docs hub
- [`STORAGE.md`](STORAGE.md) — layout protocol + `storage/` alias
- [`EXPORTS.md`](EXPORTS.md) — fallback export layout (see `STORAGE.md` for the family-local default)
- [`../output/README.md`](../output/README.md) — automation/test scratch layout
- [`../AGENTS.md`](../AGENTS.md) — agent contracts (keep clone-safe)
