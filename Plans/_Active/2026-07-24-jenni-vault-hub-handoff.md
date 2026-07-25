# Handoff — Jenni vault · go-to résumés · Design Hub Vault (2026-07-24)

**Stack:** pdf-designer (not www `/jen:reflect` destinations). Reflect landed here + Hub + vault.

| Pointer | Role |
|---|---|
| **This file** | Session status + paste-ready next-agent prompt |
| [`2026-07-21-next-agent-product-prompt.md`](2026-07-21-next-agent-product-prompt.md) | Product/TestPyPI / recipe-gallery plan (separate) |
| [`docs/PREVIEWER.md`](../../docs/PREVIEWER.md) | Design Hub + `/vault` + `/?doc=` deep-links |
| [`docs/VAULT.md`](../../docs/VAULT.md) | Vault rules (audio split updated) |

---

## Current status (read this)

### Alignerr
- **Voice Recording Specialist** — **SUBMITTED** (2026-07-24). Keep folder; do not rebuild unless asked.
  - Ship PDF: `storage/jenni/_exports/Alignerr/jenni-alignerr-voice-recording-resume-dark-v4.pdf`
- **AI Red Team Tester** — **READY_TO_SUBMIT** (human upload). Pack: AI-trainer default.
  - PDF: `storage/jenni/_exports/Alignerr-AI-Red-Team/jenni-alignerr-ai-red-team-resume-dark-v3.pdf`

### Go-to résumé packs (vault `goToPacks`)
| Pack | Path | Dark PDF (defaults export) | Use for |
|---|---|---|---|
| **voice** ⭐ | `storage/jenni/defaults/jenni-default-voice-resume.html` | `storage/jenni/_exports/defaults/jenni-default-voice-resume-dark.pdf` | Voice acting, narration, game audio, AI speech/voice training |
| **ai-trainer** | `storage/jenni/defaults/jenni-default-ai-trainer-resume.html` | `…/jenni-default-ai-trainer-resume-dark-v3.pdf` | Red-team / RLHF / AI trainer contractors |
| **general** | `storage/jenni/defaults/jenni-default-resume.html` (+ working copy `storage/jenni/jenni-resume.html`) | `…/jenni-default-resume-dark.pdf` | Default multi-hyphenate / game-dev / 3D |

**Voice pack focus (keep):** VO/narration credits, recording rig + tools, broadcast/PAX delivery, AI×audio for speech training, community badges (~22k). **Not** CC4/Unity-heavy game-dev spine. Do **not** replace with AI-trainer or Netflix ML.

**General default:** refreshed with voice best-of (summary, tags, tools, VO entry, community metrics) — still ≤2 pages, still game-dev/3D led.

### Vault skills (LinkedIn screenshot → `boardSkills` + claims)
Tags now in vault: VS Code, Server Administration, Web Dev/Design, AI, Live Streaming, Visual Arts, 3D*, Game Mechanics / Mobile / Video Games / Game Dev / Game Design.
New claims: `sk-server-admin`, `sk-web-design`, `sk-visual-arts`, `sk-game-mechanics`; `sk-webdev` strengthened.

### Design Hub — Vault UI
- Observe: [http://127.0.0.1:8787/vault](http://127.0.0.1:8787/vault)
- API: `GET /api/vault-overview`
- Deep-link: [/?doc=storage/jenni/defaults/jenni-default-voice-resume.html](http://127.0.0.1:8787/?doc=storage/jenni/defaults/jenni-default-voice-resume.html) — selects in library
- Code: `src/pdf_tool/vault_overview.py` + `static/vault.html` + `preview.py` (`openFromQuery`) + Hub “Vault” link

### Landed this continuation (2026-07-24 evening)
1. ✅ `check_generation` PASS on general + voice defaults
2. ✅ Dark PDFs → `storage/jenni/_exports/defaults/` (general + voice)
3. ✅ Vault **Open in library** → `/?doc=` deep-link; library selection writes `?doc=` back to URL
4. ✅ Profiles joined under each person on `/vault` (orphans listed separately)
5. ✅ Vault `goToPacks.*.darkPdf` / `exportDir` pointers for general + voice

### Still worth doing next
1. Optional: mark AI Red Team submitted **only after human confirms upload**.
2. Keep `boardSkills` in sync if she adds more LinkedIn tags.
3. Product plan items (TestPyPI / recipe gallery) remain on the 2026-07-21 plan.

---

## Reflect (compact)

| | |
|---|---|
| **Mode** | pdf-designer session (routed here, not JN ROADMAP) |
| **Observation** | Humans struggle to read vault JSON; skills lived only as claim prose; voice go-to wasn’t formalized under `defaults/` |
| **Root cause** | Hub scanned HTML only; no overview API over users/profiles/vault |
| **Chosen improvement** | `boardSkills` + `goToPacks` in vault + `/vault` + `/api/vault-overview` + library deep-links |
| **Landed now** | vault fields, defaults HTML, Hub page, deep-links, dark PDF exports, VAULT.md audio split, this handoff |
| **Validated by** | check_vault PASS · vault-overview tags/packs · check_generation PASS · Hub serves `openFromQuery` + vault “Open in library” |
| **Expected signal** | Open `/vault` → **Open in library** on voice pack → Hub selects that résumé |
| **Follow-up** | AI Red Team SUBMITTED only on human confirm; boardSkills sync |

---

## Prompt (copy into a new chat)

```
You are continuing work on C:\Github\pdf-designer for Jenni's vault + go-to résumés + Design Hub.

## Mission
1) Keep the voice-acting résumé pack as the go-to for VO / AI audio / speech-training jobs.
2) Keep the general default résumé (≤2 pages) current with voice best-of + board skills.
3) Make vault/skills/profiles easy to preview without reading raw JSON (Design Hub /vault).
4) Only touch Alignerr job folders if the human asks — Voice is SUBMITTED; AI Red Team is READY.

## Read first
1. AGENTS.md
2. docs/VAULT.md          ← audio split updated 2026-07-24
3. docs/PREVIEWER.md      ← /vault + /api/vault-overview + /?doc= deep-links
4. Plans/_Active/2026-07-24-jenni-vault-hub-handoff.md  ← ⭐ this status
5. storage/jenni/resume-source.json → roleTracks.voice, goToPacks, boardSkills
6. storage/users/jenni.json · storage/profiles/jenni-resume.json

## Go-to packs (do not blur)
| Pack | HTML | Dark PDF |
|---|---|---|
| voice ⭐ | storage/jenni/defaults/jenni-default-voice-resume.html | storage/jenni/_exports/defaults/jenni-default-voice-resume-dark.pdf |
| ai-trainer | storage/jenni/defaults/jenni-default-ai-trainer-resume.html | …/jenni-default-ai-trainer-resume-dark-v3.pdf |
| general | storage/jenni/defaults/jenni-default-resume.html | …/jenni-default-resume-dark.pdf |

Voice pack focus: credits + demos (YT playlist, IMDb nm11112925, Newgrounds), rig/tools
(Audacity/FL/Cool Edit/DJ Pro/DaVinci/OBS), broadcast/PAX, AI×audio. NOT Unity/CC4-led.
Shipped Alignerr proof PDF: storage/jenni/_exports/Alignerr/jenni-alignerr-voice-recording-resume-dark-v4.pdf

## What already landed (2026-07-24) — don't redo blindly
- boardSkills + goToPacks + voice goToResume pointer
- Design Hub Vault page + API + /?doc= library deep-links
- General/voice defaults refreshed; check_generation PASS; dark PDFs in _exports/defaults/

## Do next (pick and finish)
A. If human confirms AI Red Team upload → mark Alignerr-AI-Red-Team application.json SUBMITTED
B. Keep boardSkills in sync if she adds more LinkedIn tags
C. Product plan (TestPyPI / recipe gallery) — separate active plan 2026-07-21

## Contracts
- Source-backed vault only; ask before calling something a gap
- Email default: jenni@jenninexus.com
- No auto-submit; Netflix CLOSED
- check_generation before any ship
- Privacy: never commit storage/

## Observe
- Hub library: http://127.0.0.1:8787/
- Vault overview: http://127.0.0.1:8787/vault
- Voice pack deep-link: http://127.0.0.1:8787/?doc=storage/jenni/defaults/jenni-default-voice-resume.html
```
