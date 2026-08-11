# Character Voice Design SSOT (ARCHIVED 2026-07-14)

> **Shipped.** Live rules: [`docs/VAULT.md`](../../docs/VAULT.md) (voice layers) ·
> `storage/users/<user>.json#characterVoice` · vault `#voice` · `/make-resume` step 0b.
> Optional leftover (agency Discord catalogue pointer) is out of scope for pdf-designer.

---

Protocol SSOT: [`../../docs/STORAGE.md`](../../docs/STORAGE.md) ·
[`../../docs/VAULT.md`](../../docs/VAULT.md) ·
[`../../.claude/commands/make-resume.md`](../../.claude/commands/make-resume.md).

This file is the working checklist — check items off as they land.

---

## Where this stands

Voice was already split by purpose across the network. What was missing: a
**person-level character sheet** and a **hard `/make-resume` checkpoint**.

| Register | Purpose | SSOT | Status |
|---|---|---|---|
| **Application** | Resume + cover letter prose | `storage/<user>/resume-source.json#voice` | Keep + deepen |
| **Character / personality** | Traits, contrast, emoji prefs, register map | `storage/users/<user>.json#characterVoice` | New |
| **Social / Discord** | Posts, embeds, hearts, Mars crew | `socials/content/*/format-manifest.json` + bot STYLE-SPECs | Pointer only |
| **Agency bots** | Audit personas (Vidette, etc.) | `agency/agents/*.md` | Do not reuse as human voice |

**Hybrid home:**

- Edit personality / contrast / register map in **`users/<user>.json#characterVoice`**
- Edit how cover letters and résumés *sound* in **`storage/<user>/resume-source.json#voice`**
- Profiles stay one-line pointers (no second copy of leadIdentity)

---

## Checklist

### A. Person files — `characterVoice`

- [x] Schema + seed on `storage/users/jenni.json`
- [x] Schema + seed on `storage/users/shade.json`
- [x] `identity.voice` stays a one-line summary pointing at characterVoice + vault

### B. Vault `voice` deepen

- [x] Normalize keys → camelCase (`signatureMoves`, `backgroundFlavor`)
- [x] Add `personality` + `vsPartner` + coverLetter/resume notes (both vaults)
- [x] Shade: sync `leadIdentityByTrack` (`audio`, `ui-ux`)
- [x] Update tracked `examples/profiles/default-resume/resume-source.example.json`
- [x] Update tracked `examples/profiles/default-resume/user.example.json`

### C. Profiles slim

- [x] Shade profile: leadIdentity → pointer + rule only (vault owns the map)

### D. Protocol / command

- [x] `/make-resume` step **0b. Load voice**
- [x] `docs/VAULT.md` — voice row + authoring step
- [x] `docs/STORAGE.md` — person layer includes characterVoice

### E. Socials cross-links

- [x] `content/jenninexus/format-manifest.json` → `_meta.voiceSsot`
- [x] `content/martiangames/format-manifest.json` → `_meta.voiceSsot`
- [x] `content/README.md` — Voice layers note
- [ ] Agency Discord chatVoice catalogue pointer (jenni-bot `agency-profiles.json`) — linked from socials voice note; agents stay audit characters

---

## Out of scope

- Agency agent personalities stay site-audit characters (Discord chatVoice is a *separate* community register on the bot catalogue — still not human/resume voice)
- Studio / martian voices stay on `profiles/studio-resume.json` / `martian-resume.json`
- No emoji on ATS light PDFs
- No SEGO↔BEE vault merges
