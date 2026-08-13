# `storage/` — private workspace layout (LIVE)

> **Migration:** root nouns in [`WORKSPACE-LAYOUT.md`](WORKSPACE-LAYOUT.md).
> Engine: `pdf_tool.paths` accepts both trees. **SEGO live files were copied** to
> `users/` · `vaults/` · `profiles/` · `resumes/` · `applications/` · `collages/` · `brands/`
> on 2026-08-13 (`scripts/migrate-workspace.py`). **`storage/` is still the alias** —
> do not delete it until dual-run smoke has lived on the new nouns.
>
> **Tracked protocol SSOT:** this page lives in `docs/` so a fresh clone can learn the flow.
> Your machine’s `storage/` folder is **gitignored** and holds only real personal data.

Everything under `storage/` is **local only**. It holds career data, applications, PDFs,
and **private brand palettes**. Private *notes* (`MARKETING` · `WORKSPACE` · history scrub)
now live under **`docs/`** (gitignored) — not a second docs tree here.

---

## Public vs private (one glance)

| Tracked in the repo (safe to clone) | Private in `storage/` (gitignored) | Lives in theme kits (website SSOT) |
|---|---|---|
| `src/`, `themes/`, `examples/`, `docs/`, `AGENTS.md` | `users/`, `*/resume-source.json`, `profiles/`, `_job-listings/`, `brand-design/`, `collages/`, `_exports/`, **`docs/`** | `www-theme-kit/profiles/…` (official kit) |
| Brand-neutral default theme + `examples/brand-design/` | Real brand maps + vaults + contacts + private notes | Live site primary/secondary/accent |
| `.config/mcp-pdf-designer.example.json` | Local `mcp-pdf-designer.json` (absolute paths) | — |

**Website kits own live site colors.** pdf-designer stores a **mapped copy** under
`storage/brand-design/brand-*.json` for exports and the Design Hub. That mapped file is the
**pdf-designer SSOT** for personal/studio résumé colors — edit it here, point everything else at it.

---

## Brand SSOT (pdf-designer)

| Who / what | Single file to edit | Pointed at by |
|---|---|---|
| **Jenni** personal | `storage/brand-design/brand-jenninexus.json` | `users/jenni.json` → `brandTheme.ssot`, `profiles/jenni-resume.json` |
| **Shade** personal (Synagen) | `storage/brand-design/brand-synagen.json` | `users/shade.json` → `brandTheme.ssot`, `profiles/shade-resume.json` |
| **Martian Games** studio | `storage/brand-design/brand-martian.json` | `profiles/martian-resume.json`, `profiles/studio-resume.json` |

Do **not** keep a second hex map in `users/*.json`. Upstream website profiles are
**inspiration / sync source**, not a second résumé SSOT.

**MG dark role lockstep** (do not swap secondary/accent): primary `#FF6B00` · secondary `#8B5CF6` ·
accent `#FF4500` · support `#42F4C8` — mirrors `www-theme-kit/profiles/martiangames.json` and
`www-theme-kit/palettes/resume-palettes.json#martian-resume`. Path is `brand-design/` (never legacy
`storage/brands/`).

**Cross-PC:** `storage/` is gitignored. After editing brand maps on SEGO, copy
`storage/brand-design/` → BEE `C:\p\pdf-designer\storage\brand-design\` over SMB
(`\\BEETHOVEN\p\…`). Tracked docs sync via `git pull` on BEE (pdf-designer uses a deploy key —
see `/jen/pdf` · `/jen/bee` §11b). Prefs chain: [`SSOT.md`](SSOT.md) § Personal palette prefs.

Tracked template for new users: [`../examples/brand-design/`](../examples/brand-design/).

---

## The four layers

Each layer answers exactly one question.

```
  ① WHO ─────────────  users/<user>.json
                       contact · emails · brandTheme.ssot → brand-design/brand-*.json
                       characterVoice  ← personality · contrast · register map
                                    │
                                    ▼
  ② WHAT ────────────  <user>/resume-source.json          ◀── ⭐ THE VAULT
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
  ④ THE JOB ─────────  _job-listings/<Track>/
                       <Company>.md · application.json · theme.json · *.html
                                    │
                                    ▼
  → OUT ─────────────  <user>/_exports/<Track>/
```

### Shared studio assets vs per-user assets (⭐ read before hunting images)

Both founders ship Martian Games title art in work-samples. That gallery is **shared**, not copied
twice. Personal / brand-identity art stays per-user.

| Asset class | SSOT path | Who |
|---|---|---|
| **MG title stills + MG logo** | `storage/studio/resources/images/martiangames/` | Jenni **and** Shade |
| Agency banner + agent faces | `storage/jenni/resources/images/agency/` | **Jenni only** |
| Synagen logo / engine shots | `storage/shade/resources/logos/` (+ `images/synagen/` when present) | **Shade lead** (Jenni may reference the logo file under her own `logos/` copy) |
| Source CVs / owner quotes | `storage/<user>/resources/refrence/` | That person |

```
storage/studio/resources/images/
  martiangames/             ⭐ SHARED MG gallery (WebP). README inside.
  README.md                 what belongs here vs per-user

storage/<user>/resources/images/martiangames/   → Windows JUNCTION → studio/.../martiangames/
```

**Keep both current:** edit files only under `studio/…/martiangames/`. The junctions mean
`jenni/.../martiangames/` and `shade/.../martiangames/` always resolve to the same bytes.
Person files point at the studio path via `users/<user>.json#portfolio.workSampleAssets.mgGallerySsot`.
Prefer **WebP** for new drops (PNG inlined in HTML balloons PDF size past upload caps).

Refresh MG atlas from: `C:\Users\Owner\Projects\www\mg\html\resources\images\atlas\`
Air Wars preferred hero source: `…\mg\src\assets\images\airwars\gallery\11b.png` →
`game-air-wars-sunset.webp`.

### Per-user directory layout (`storage/jenni/`, `storage/shade/`)

Each person's folder holds their vault + their **go-to default deliverables** + reusable assets and
finished-run history. Updated architecture 2026-07-20 / shared gallery 2026-07-21:

```
storage/<user>/
  resume-source.json        ⭐ THE VAULT (root — stays here)
  <user>-resume.html / shade-default-resume.html   the favorite/default source HTML (root)
  defaults/                 ⭐ GO-TO reusable PDFs — the generic "best-of" resume, cover letter,
                            and work-examples (light + dark), ready to submit to a NEW listing
                            without re-generating. NO template placeholders ([address] etc.) —
                            generic and submittable as-is.
  resources/                reusable user assets (NOT job-specific)
      images/
        martiangames/       JUNCTION → storage/studio/resources/images/martiangames/ (shared)
        agency/             (jenni only) Agency showcase
        synagen/            (shade — when engine screenshots arrive)
      logos/                brand marks — synagen-logo-16-9.png, etc. (per-user)
      refrence/             source CVs + owner quote docs (mg_cv_2025.pdf, Self-Described.md, …)
  _exports/<Track>/         per-listing generated PDFs (one subdir per job)
  _archive/                 ⛔ retired/superseded material — DO NOT DELETE on a "clean stale" pass
  _submitted/               (shade) sent-application record — DO NOT DELETE on a "clean stale" pass
```

> **⛔ `_archive/`, `_exports/`, and `_submitted/` are protected.** Never delete their contents during
> a "clean stale" / dangling-reference sweep — they are history and finished work the owner keeps on
> purpose. Stale-cleaning applies to broken *pointers*, not to these directories.
>
> **`defaults/` vs `_exports/`.** `_exports/<Track>/` is per-job output; **`defaults/` is the one place
> to grab a ready-to-send generic resume/cover/work-samples** so the owner never has to sort through
> `_exports/` or re-generate for a fresh listing. Keep `defaults/` current with the best-of vault.
>
> **⭐ Export defaults INTO `defaults/`** — same folder as the HTML (`--output-dir storage/<user>/defaults`
> or an explicit PDF path under that dir). **Never** write go-to packs to `_exports/defaults/` (that
> path hid PDFs from the Design Hub defaults picker). Vault `goToPacks.*.exportDir` must point at
> `storage/<user>/defaults/`. After editing a default HTML, re-export **light + dark** for **every**
> applicant (`exportPrefs.resumeDefault = light-and-dark`), run
> `python -m pdf_tool.check_generation` on the source, and `python -m pdf_tool.check_ats` on the light
> PDF (see [`QA.md`](QA.md) · [`JOB-ASSESSMENT.md`](JOB-ASSESSMENT.md) § Tier 4.5).
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
