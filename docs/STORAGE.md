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
route live career data through the root nouns and generated personal deliverables through `_exports/`.
Private *notes* (`MARKETING` · `WORKSPACE` · history scrub) now live under **`docs/`** (gitignored)
— not a second docs tree here.

---

## Public vs private (one glance)

| Tracked in the repo (safe to clone) | Private at repo root (gitignored) | Lives in theme kits (website SSOT) |
|---|---|---|
| `src/`, `themes/`, `examples/`, `docs/`, `AGENTS.md`, `output/README.md`, `_exports/README.md` | `users/`, `vaults/`, `profiles/`, `_job-apps/`, `brands/`, `collages/`, `resumes/`, `_exports/*` payload, legacy `storage/` | `www-theme-kit/profiles/…` (official kit) |
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

**Cross-PC:** root nouns are gitignored. After editing brand maps on SEGO, copy
`brands/` → BEE `C:\p\pdf-designer\brands\` over SMB
(`\\BEETHOVEN\p\…`). Tracked docs sync via `git pull` on BEE (pdf-designer uses a deploy key —
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
  → OUT ─────────────  _exports/<user>/resumes/<Track>/
```

### Shared studio assets vs per-user assets (⭐ read before hunting images)

Both founders ship Martian Games title art in work-samples. That gallery is **shared**, not copied
twice. Personal / brand-identity art stays per-user.

| Asset class | SSOT path | Who |
|---|---|---|
| **MG title stills + MG logo** | `resumes/studio/resources/images/martiangames/` | Jenni **and** Shade |
| Agency banner + agent faces | `resumes/jenni/resources/images/agency/` | **Jenni only** |
| Synagen logo / engine shots | `resumes/shade/resources/logos/` (+ `images/synagen/` when present) | **Shade lead** (Jenni may reference the logo file under her own `logos/` copy) |
| Source CVs / owner quotes | `resumes/<user>/resources/refrence/` | That person |

```
resumes/studio/resources/images/
  martiangames/             ⭐ SHARED MG gallery (WebP). README inside.
  README.md                 what belongs here vs per-user

resumes/<user>/resources/images/martiangames/   → Windows JUNCTION → studio/.../martiangames/
```

**Keep both current:** edit files only under `studio/…/martiangames/`. The junctions mean
`jenni/.../martiangames/` and `shade/.../martiangames/` always resolve to the same bytes.
Person files point at the studio path via `users/<user>.json#portfolio.workSampleAssets.mgGallerySsot`.
Prefer **WebP** for new drops (PNG inlined in HTML balloons PDF size past upload caps).

Refresh MG atlas from the local website checkout: `<mg-repo>/html/resources/images/atlas/`.
Air Wars preferred hero source: `<mg-repo>/src/assets/images/airwars/gallery/11b.png` →
`game-air-wars-sunset.webp`.

### Per-user directory layout (`resumes/jenni/`, `resumes/shade/`)

Each person's résumé folder holds their **go-to source documents** + reusable assets and
finished-run history. Identity and claims live separately in `users/` and `vaults/`; generated
deliverables live in `_exports/`. Updated architecture 2026-07-20 / root-noun split 2026-08-17:

```
resumes/<user>/
  <user>-resume.html / shade-default-resume.html   the favorite/default source HTML (root)
  defaults/                 ⭐ GO-TO reusable HTML — the generic "best-of" resume, cover letter,
                            and work-examples sources (company-agnostic). PDFs live in
                            _exports/<user>/resumes/ (flat), not in this folder.
  resources/                reusable user assets (NOT job-specific)
      images/
        martiangames/       JUNCTION → resumes/studio/resources/images/martiangames/ (shared)
        agency/             (jenni only) Agency showcase
        synagen/            (shade — when engine screenshots arrive)
      logos/                brand marks — synagen-logo-16-9.png, etc. (per-user)
      refrence/             source CVs + owner quote docs (mg_cv_2025.pdf, Self-Described.md, …)
  (PDFs)                    _exports/<user>/resumes/<Track>/  — private generated files, not this folder
  _archive/                 ⛔ retired/superseded material — DO NOT DELETE on a "clean stale" pass
  _submitted/               (shade) sent-application record — DO NOT DELETE on a "clean stale" pass
```

> **⛔ `_archive/` and `_submitted/` are protected.** Never delete their contents during
> a "clean stale" / dangling-reference sweep — they are history the owner keeps on
> purpose. Private finished PDFs now live under **`_exports/<user>/resumes/`** (also protected).
> Stale-cleaning applies to broken *pointers*, not to these directories.
>
> **`defaults/` vs `_exports/`.** `_exports/<user>/resumes/<Track>/` is per-job output;
> **`defaults/` is HTML only** — the generic "best-of" résumé / cover / work-examples
> sources. Grab the matching PDFs from `_exports/<user>/resumes/` (flat go-to files).
> Vault `goToPacks.*.exportDir` must point at `_exports/<user>/resumes/`. After editing
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
