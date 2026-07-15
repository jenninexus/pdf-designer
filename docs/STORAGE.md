# `storage/` — private workspace layout

> **Tracked protocol SSOT:** this page lives in `docs/` so a fresh clone can learn the flow.
> Your machine’s `storage/` folder is **gitignored** and holds only real personal data.
> A short pointer file may also exist at `storage/README.md` (local) — if they disagree, **this doc wins**.

Everything under `storage/` is **local only**. It holds career data, applications, PDFs, and
**private brand palettes**. Nothing here is pushed to GitHub.

---

## Public vs private (one glance)

| Tracked in the repo (safe to clone) | Private in `storage/` (gitignored) | Lives in theme kits (website SSOT) |
|---|---|---|
| `src/`, `themes/`, `examples/`, `docs/`, `AGENTS.md` | `users/`, `*/resume-source.json`, `profiles/`, `applications/`, `brands/`, `_exports/` | `www-theme-kit/profiles/…`, `syna-theme-kit/profiles/…` |
| Brand-neutral default theme + `examples/brands/` | Real brand maps + vaults + contacts | Live site primary/secondary/accent |

**Website kits own live site colors.** pdf-designer stores a **mapped copy** under
`storage/brands/brand-*.json` for exports and the Design Hub. That mapped file is the
**pdf-designer SSOT** for personal/studio résumé colors — edit it here, point everything else at it.

---

## Brand SSOT (pdf-designer)

| Who / what | Single file to edit | Pointed at by |
|---|---|---|
| **Jenni** personal | `storage/brands/brand-jenninexus.json` | `users/jenni.json` → `brandTheme.ssot`, `profiles/jenni-resume.json` |
| **Shade** personal (Synagen) | `storage/brands/brand-synagen.json` | `users/shade.json` → `brandTheme.ssot`, `profiles/shade-resume.json` |
| **Martian Games** studio | `storage/brands/brand-martian.json` | `profiles/martian-resume.json`, `profiles/studio-resume.json` |

Do **not** keep a second hex map in `users/*.json`. Upstream website profiles are
**inspiration / sync source**, not a second résumé SSOT.

Tracked template for new users: [`../examples/brands/`](../examples/brands/).

---

## The four layers

Each layer answers exactly one question.

```
  ① WHO ─────────────  users/<user>.json
                       contact · emails · brandTheme.ssot → brands/brand-*.json
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
  ④ THE JOB ─────────  applications/<Track>/
                       <Company>.md · application.json · theme.json · *.html
                                    │
                                    ▼
  → OUT ─────────────  <user>/_exports/<Track>/
```

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
| [`.claude/commands/make-resume.md`](../.claude/commands/make-resume.md) | End-to-end build routine |

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
