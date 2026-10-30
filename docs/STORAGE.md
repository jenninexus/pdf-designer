# `storage/` — retired dual-run alias

> **Retired 2026-08-17.** Live personal data is only at the root nouns in
> [`WORKSPACE-LAYOUT.md`](WORKSPACE-LAYOUT.md): `users/` · `vaults/` · `profiles/` ·
> `resumes/` · `_job-apps/` · `collages/` · `brands/`.
> The engine (`pdf_tool.paths`) still *accepts* `storage/…` paths as aliases so old
> scripts and Hub URLs keep working. Existing backups/collage/video/PyPI residue may
> remain there; do **not** add new live listings or current application sources under it.
>
> `_job-apps/_template/` is a tracked folder-shape pointer only. Keep real application material local.
> Private font: `brands/fonts/alienleaguebold.woff2` (gitignored).
>
> **Tracked protocol SSOT:** this page lives in `docs/` so a fresh clone can learn the flow.

Everything under `storage/` is **local-only legacy residue**. Keep it for recovery/history, but
route live career data through the root nouns; deliberate generated deliverables now export
beside their document family (`resumes/<user>/…`, `collages/<project>/`), with `_exports/`
as the fallback for unmatched sources.
Private *notes* (`MARKETING` · `WORKSPACE` · history scrub) now live under **`docs/`** (gitignored)
— not a second docs tree here.

---

## Public vs private (one glance)

| Tracked in the repo (safe to clone) | Private at repo root (gitignored) | Lives in theme kits (website SSOT) |
|---|---|---|
| `src/`, `themes/`, `examples/`, `docs/`, `AGENTS.md`, `output/README.md`, `_exports/README.md` | `users/`, `vaults/`, `profiles/`, `_job-apps/`, `brands/`, `collages/`, `resumes/`, `_exports/*` payload, `output/*` scratch, legacy `storage/` | `www-theme-kit/profiles/…` (official kit) |
| Brand-neutral default theme + `examples/brand-design/` | Real brand maps + vaults + contacts + private notes | Live site primary/secondary/accent |
| `.config/mcp-pdf-designer.example.json` | Local `mcp-pdf-designer.json` (absolute paths) | — |

**Website kits own live site colors.** pdf-designer stores a **mapped copy** under
`brands/brand-*.json` for exports and the Design Hub. That mapped file is the
**pdf-designer SSOT** for personal/studio résumé colors — edit it here, point everything else at it.

---

## Brand SSOT

Each private `brands/brand-*.json` owns the document palette. User and profile records point to it; do not duplicate token values there. Public defaults are independent of private brand maps.

## The four layers

Each layer answers exactly one question.

```
  ① WHO ─────────────  users/<user>.json
                       contact · emails · brandTheme.ssot → brands/brand-*.json
                       characterVoice  ← personality · contrast · register map
                                    │
                                    ▼
  ② WHAT ────────────  vaults/<user>.json          ◀── ⭐ THE VAULT
     every claim (source · strength · tracks) + voice (application prose)
     + roleTracks.<track>.angle
                                    │
                                    ▼
  ③ HOW ─────────────  profiles/<user>-resume.json
                       layout · exports · cover-letter policy
                       voice = pointer only (vault + characterVoice)
                       (+ a studio profile when needed)
                                    │
                                    ▼
  ④ THE JOB ─────────  _job-apps/<Track>/
                       <Company>.md · application.json · theme.json · *.html
                                    │
                                    ▼
  → OUT ─────────────  resumes/<profile>/<Track>/  (or collages/<project>/; _exports/ fallback)
```

## The generated-file rule

Exports live **with their document family**, not in one central library. Per-job résumé/cover-letter/
work-sample PDFs and PNGs go to `resumes/<profile>/<Track>/` (HTML sources stay in `_job-apps/<Track>/`).
Go-to/default packs export flat into `resumes/<profile>/` (HTML stays in `resumes/<profile>/defaults/`).
Studio exports live under `resumes/studio/…`. Collage exports land at the collage project root,
`collages/<project>/`. The Hub labels the union of these **Exports**.

### Which folder is which (the four surfaces, settle it once)

These have been mistaken for each other. They are not alternatives; each has exactly one job.

| Folder | Job | Tracked? | Never put here |
|---|---|---|---|
| **`resumes/<user>/…`** | ⭐ **where finished résumé/letter/work-sample files go** — beside the person who sends them | 🔒 no | HTML sources, job research, scratch |
| **`_job-apps/<App>/`** | the **job** — listing, `application.json`, `theme.json`, the HTML sources | 🔒 no (README only) | PDFs |
| **`output/…`** | **disposable scratch only** — a QA staging dir, a smoke test, a bundle you are about to throw away. Reached only by an explicit `--output-dir output/…` | 🔒 payload (README yes) | anything you want to keep, and anything the Hub should show |
| **`_exports/…`** | **fallback only** — a source the engine cannot match to a person/project (public `examples/`, or an unfiled source). A fresh clone lands here because it has no `resumes/<profile>/` yet | 🔒 payload (README yes) |

**So: `output/` is not "the old output folder" and it is not the destination for a real résumé.** It is
deliberate, disposable automation scratch, it is excluded from the Hub's document library, and the smoke
test writes there on purpose. The user-facing answer to *"where does my PDF go?"* is
**`resumes/<user>/…`** for a personal document, `collages/<project>/` for a collage, and `_exports/…` only
when nothing else can be inferred.

### Company grouping

Group multiple roles for one company under `resumes/<user>/ExampleCo/<role>/`. The engine currently infers a flat application path; pass an explicit `--output-dir` when exporting to the grouped folder.

### Sent artifacts

A submitted file moves into `resumes/<user>/<Track-or-company>/submitted-<company>-<slug>-<date>/` and is
never edited again. If an already-frozen document is **reused verbatim** for another posting, point at
that frozen original and record its hash — do not make a second copy. Protocol:
[`APPLICATIONS.md`](APPLICATIONS.md) § And freeze what you actually sent.

`_exports/` is now the **fallback only**, used when a source can't be matched to a document family:

```text
_exports/examples/                         public/example exports
_exports/unfiled/                          source with no inferred profile or kind
```

A fresh public clone (before any `resumes/<profile>/` or `collages/<project>/` exists) still exports
here by default.

`output/` is not a second library. It is explicit, disposable automation/test scratch and is not
scanned by the Hub. Editable HTML and image sources remain in `examples/`, `resumes/`, `collages/`,
or `_job-apps/`; identity, claims, and render configuration remain in `users/`, `vaults/`, and
`profiles/`.

### Shared and per-user assets

Keep each person’s resources under `resumes/<user>/resources/`. A shared studio gallery may be referenced from multiple profiles, while attribution and portfolio selection remain person-specific. Preserve supported links and verify their targets before moving assets.

### Voice sources

Application voice is sourced from the person record and private vault; keep external voice maps separate from claim evidence.

## Does pdf-designer need MCP or a always-on server?

**No.** The engine is offline CLI + optional local Design Hub:

```bash
python -m pdf_tool.preview          # local http://127.0.0.1:8787 — optional convenience
python -m pdf_tool.html_to_pdf …    # works with zero server running
```

- **No MCP server required** for best results.
- **No cloud / env / telemetry.**
- The previewer is a **temporary localhost** process (stdlib HTTP on 127.0.0.1). Stop it when you’re done. Playwright launches Chromium only for export/preview rendering.
