# Project and folder map

`pdf-designer` is a local-first Python document toolkit. Its engine renders HTML to PDF with
Chromium, creates collages and page images, validates document geometry, palettes and ATS text,
and serves the Design Hub. Start with [AGENTS.md](../AGENTS.md) and [SSOT.md](SSOT.md).

| Folder | Responsibility |
|---|---|
| `src/pdf_tool/` | Engine, preview server, export commands and QA guards |
| `docs/` | Public protocol, architecture, storage, applications, QA and roadmap |
| `themes/` | Public color tokens, presets and palette rules |
| `layouts/` | Document structure recipes; separate from color |
| `examples/` | Public sample profiles, vault shapes and résumé studio |
| `.memory/` | Tracked lessons; read its index before opening relevant lessons |
| `.claude/commands/` | Public `*.example.md` protocols; bare personal commands are ignored |
| `users/` | Private identity, contact rules and character voice |
| `vaults/` | Private source-backed claims and application prose voice |
| `profiles/` | Private rendering preferences and work-sample structure |
| `_job-apps/` | Private listings, apply URLs, application records, correspondence and source HTML |
| `resumes/` | Private finished documents and reusable per-person reference assets |
| `brands/`, `collages/` | Private mapped brand colors and collage families |
| `Plans/` | Private session checklists; `docs/ROADMAP.md` owns the public backlog |
| `_exports/` | Fallback exports for examples or unmatched sources |
| `output/` | Disposable automation scratch, excluded from the document library |
| `storage/` | Retired private residue; compatibility aliases only |

The résumé protocol uses four layers: person → vault → profile → application. Claims are
authored in the vault before use. Source HTML lives with the application; generated PDFs live
under `resumes/<person>/<application>/`. The human response/submission index is
`_job-apps/applied-index.md`; per-application `application.json` carries machine-readable status.
Private data, correspondence, generated files and plans must not enter public Git or general
knowledge indexing. See [STORAGE.md](STORAGE.md) and [APPLICATIONS.md](APPLICATIONS.md).

## Optional agent tooling

The engine and public examples run without private agent services. Personal service registrations,
startup checks and indexing procedures belong in ignored `storage/docs/`. Public documentation
and fictional examples may be indexed; personal data and operational notes must remain excluded.
