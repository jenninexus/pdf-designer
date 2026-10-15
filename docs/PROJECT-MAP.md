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

## Relationship to sys-admin and Synabrain

**sys-admin is optional agent tooling, not an engine dependency.** Its MCP adapter can enrich an
agent session with file operations, machine access, SSH transfers and coordination. Synabrain
provides retrieval and knowledge indexing. Neither is required to render documents or use the
public examples. The engine has no MCP, environment-variable or network-service requirement;
installation and browser provisioning are separate setup steps.

A standing MCP process and a chat's tool attachment are separate: verify callable tools in the
current chat. `get_context` must use the actual caller repository path. A useful retrieved passage
does not prove that the caller's private files or current dirty bytes were indexed. Remote QA
uses the live Syqo machine route and a verified source snapshot rather than an assumed host.

Index this public map and selected public protocol documents in `proj:pdf-designer`. Preserve
source paths and revision provenance; do not recursively learn the private root nouns. Network
roles, providers and credentials remain owned by their respective services, not this repository.
