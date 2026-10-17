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

## Brand SSOT (pdf-designer)

| Who / what | Single file to edit | Pointed at by |
|---|---|---|
| **Jenni** personal | `brands/brand-jenninexus.json` | `users/jenni.json` → `brandTheme.ssot`, `profiles/jenni-resume.json` |
| **Shade** personal (Synagen) | `brands/brand-synagen.json` | `users/shade.json` → `brandTheme.ssot`, `profiles/shade-resume.json` |
| **Martian Games** studio | `brands/brand-martian.json` | `profiles/martian-resume.json`, `profiles/studio-resume.json` |

Do **not** keep a second hex map in `users/*.json`. Upstream website profiles are
**inspiration / sync source**, not a second résumé SSOT.

**MG dark role lockstep** (do not swap secondary/accent): primary `#FF6B00` · secondary `#8B5CF6` ·
accent `#FF4500` · support `#42F4C8` — mirrors `www-theme-kit/profiles/martiangames.json` and
`www-theme-kit/palettes/resume-palettes.json#martian-resume`. Path is `brands/` (was
`storage/brand-design/`).

**Cross-PC:** root nouns are gitignored. After editing brand maps on example-host, copy
`brands/` → BEE `C:\p\pdf-designer\brands\` over SMB
(`\\example-builder\p\…`). Tracked docs sync via `git pull` on BEE (pdf-designer uses a deploy key —
see `/jen/pdf` · `/jen/bee` §11b). Prefs chain: [`SSOT.md`](SSOT.md) § Personal palette prefs.

Tracked template for new users: [`../examples/brand-design/`](../examples/brand-design/).

---

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
                       (+ martian-resume / studio-resume for studio voice)
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

### Company grouping (multi-application companies)

A company micro1/Meta-style — several near-identical postings at once — gets **its own folder** under the
person, so the role folders do not pile up flat:

```text
resumes/shade/Micro1/Research-Engineering/          ← company group + role
resumes/shade/Micro1/Art-Related-Professional/
resumes/shade/Meta/Technical-Game-Designer/
resumes/shade/Sony-3D-Characters/                   ← single-application company stays flat
```

Group a company only when it has **two or more applications** for that person; a one-off stays flat so
the tree does not grow a level for nothing. The company group is a **browsing** convenience — the
`_job-apps/<App>/` record stays flat and keeps its company-prefixed name
(`_job-apps/Micro1-Research-Engineering/`).

> ⚠️ **Exports for a grouped company need an explicit `--output-dir`.** The engine infers the export
> folder from the flat `_job-apps/<App>/` name, so it would write
> `resumes/shade/Micro1-Research-Engineering/` next to the group instead of inside it. Pass
> `--output-dir resumes/shade/Micro1/Research-Engineering` for those. Single-application companies need
> no flag. (`src/pdf_tool/paths.py` `default_output_dir`.)

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

### Shared studio assets vs per-user assets (⭐ read before hunting images)

Both founders ship Martian Games title art in work-samples. That gallery is **shared**, not copied
twice. Personal / brand-identity art stays per-user.

| Asset class | SSOT path | Who |
|---|---|---|
| **MG title stills + MG logo** | `resumes/studio/resources/images/martiangames/` | Jenni **and** Shade |
| Agency banner + agent faces | `resumes/jenni/resources/images/agency/` | **Jenni only** |
| Synagen logo / engine shots | `resumes/shade/resources/logos/` (+ `images/synagen/` when present) | **Shade lead** (Jenni may reference the logo file under her own `logos/` copy) |
| Source CVs / owner quotes | `resumes/<user>/resources/references/` | That person |

```
resumes/studio/resources/images/
  martiangames/             ⭐ SHARED MG gallery (WebP). README inside.
  README.md                 what belongs here vs per-user

resumes/<user>/resources/images/martiangames/   → Windows JUNCTION → studio/.../martiangames/
```

**Keep both current:** edit files only under `studio/…/martiangames/`. The junctions mean
`jenni/.../martiangames/` and `shade/.../martiangames/` always resolve to the same bytes.
Person files point at the studio path via `users/<user>.json#portfolio.workSampleAssets.mgGallerySsot`.
Work-samples templates should reference these files by **relative `<img src>` path** (not `{{img:…}}`
placeholders): the template then previews correctly as-is, and `inline_images` inlines every relative
source automatically, failing loudly on a missing file.
Prefer **WebP** for new drops (PNG inlined in HTML balloons PDF size past upload caps).

Refresh MG atlas from the local website checkout: `<mg-repo>/html/resources/images/atlas/`.
Air Wars preferred hero source: `<mg-repo>/src/assets/images/airwars/gallery/11b.png` →
`game-air-wars-sunset.webp`.

### Per-user directory layout (`resumes/jenni/`, `resumes/shade/`)

Each person's résumé folder holds their **go-to source documents** + reusable assets and
finished-run history. Identity and claims live separately in `users/` and `vaults/`; generated
deliverables live beside this folder, under `resumes/<user>/…` (fallback `_exports/` only for an
unmatched source). Updated architecture 2026-07-20 / root-noun split 2026-08-17 / export-beside-family 2026-09-27:

```
resumes/<user>/
  <user>-resume.html / shade-default-resume.html   the favorite/default source HTML (root)
  defaults/                 ⭐ GO-TO reusable HTML — the generic "best-of" resume, cover letter,
                            and work-examples sources (company-agnostic). PDFs live in
                            resumes/<user>/ (flat), not in this folder.
  resources/                reusable career-document sources (NOT job-specific; not résumé-only)
      images/
        martiangames/       JUNCTION → resumes/studio/resources/images/martiangames/ (shared)
        agency/             (jenni only) Agency showcase
        synagen/            (shade — when engine screenshots arrive)
      logos/                brand marks — synagen-logo-16-9.png, etc. (per-user)
      videos/               reusable clips; keep job-specific captures with that application instead
      references/           source CVs + owner quote docs (mg_cv_2025.pdf, Self-Described.md, …)
  (PDFs)                    resumes/<user>/<Track>/  — private generated files (per-job subfolder)
                            resumes/<user>/<Track>/submitted-<company>-<slug>-<date>/
                              the exact files sent for one posting + their README and hash
                              (never edited; where the sent artifact lives — APPLICATIONS.md)
  _archive/                 ⛔ retired/superseded material — DO NOT DELETE on a "clean stale" pass
```

> **⛔ `_archive/` and any `submitted-*` folder are protected.** Never delete their contents during
> a "clean stale" / dangling-reference sweep — they are history the owner keeps on
> purpose. A `submitted-*` folder is the only copy of what an employer received: treat it as a
> permanent record (`docs/APPLICATIONS.md` § And freeze what you actually sent).
> Private finished PDFs also live under **`resumes/<user>/`** itself (protected too;
> `_exports/<user>/resumes/` is fallback only, for a source the engine can't match here).
> Stale-cleaning applies to broken *pointers*, not to these directories.
>
> **Legacy note:** an older revision of this page described a single top-level `resumes/<user>/_submitted/`
> folder. **No such folder was ever created**, and `src/pdf_tool/paths.py` keeps `_submitted` only in its
> reserved-name list so an old path shape can never be mistaken for a job folder. The live convention is
> the per-track `submitted-*` folder above.
>
> **`defaults/` vs the per-job folder.** `resumes/<user>/<Track>/` is per-job output;
> **`defaults/` is HTML only** — the generic "best-of" résumé / cover / work-examples
> sources. Grab the matching go-to PDFs from `resumes/<user>/` (flat).
> Vault `goToPacks.*.exportDir` must point at `resumes/<user>/`. After editing
> a default HTML, re-export **light + dark** (no `--output-dir` needed), run
> `python -m pdf_tool.check_generation` on the source, and `python -m pdf_tool.check_ats` on the light
> PDF (see [`QA.md`](QA.md) · [`JOB-ASSESSMENT.md`](JOB-ASSESSMENT.md) § Tier 4.5).
> Work-examples must also pass `--max-mb 5` (Indeed-class additional-documents cap) —
> re-inline with `python -m pdf_tool.inline_images --board` first; see [`EXPORTS.md`](EXPORTS.md).
### Voice SSOT (hybrid)

| Layer | Path | Edit when… |
|---|---|---|
| **Network map / public cards** | `C:\Github\voice-seed\` (`registry.json`, `characters/`) | New character, register map changes, public overview refresh |
| **Character / personality** | `users/<user>.json#characterVoice` | Traits, partner contrast, emoji prefs, pointers to socials/bots |
| **Application prose** | `<user>/resume-source.json#voice` | How résumés and cover letters sound (tone, signatureMoves, leadIdentity) |
| **Marketing (not applications)** | `socials/content/*/format-manifest.json` + bot STYLE-SPECs | Post format + Discord emoji — inspire only |
| **Agency loft (fiction)** | `agency/docs/STUDIO-VOICE.md` + `agents/*.md` | Site-audit / Discord agent characters — never applicant voice |

Protocol deep-dives (tracked):

| Doc | For |
|---|---|
| [`VAULT.md`](VAULT.md) | What may be claimed; voice; capability matrix |
| [`JOB-ASSESSMENT.md`](JOB-ASSESSMENT.md) | Capture → verify → gap-check before writing |
| [`.claude/commands/make-resume.md`](../.claude/commands/make-resume.example.md) | End-to-end build routine |

---

## Does pdf-designer need MCP or a always-on server?

**No.** The engine is offline CLI + optional local Design Hub:

```bash
python -m pdf_tool.preview          # local http://127.0.0.1:8787 — optional convenience
python -m pdf_tool.html_to_pdf …    # works with zero server running
```

- **No MCP server required** for best results.
- **No cloud / env / telemetry.**
- The previewer is a **temporary localhost** process (stdlib HTTP on 127.0.0.1). Stop it when you’re done. Playwright launches Chromium only for export/preview rendering.
