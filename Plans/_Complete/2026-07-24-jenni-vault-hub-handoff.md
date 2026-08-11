# Handoff — Jenni vault · go-to résumés · Design Hub · command prefs (2026-07-24)

**Stack:** pdf-designer. Reflect + wrap land here (not www ROADMAP).

| Pointer | Role |
|---|---|
| **This file** | Session status + paste-ready next-agent prompt |
| [`2026-07-21-next-agent-product-prompt.md`](2026-07-21-next-agent-product-prompt.md) | Product / TestPyPI (recipe gallery ✅ · local-wheel dry-run ✅) |
| [`docs/PREVIEWER.md`](../../docs/PREVIEWER.md) | Hub `/vault` · `/recipes` · `/?doc=` · `/?palette=` |
| [`docs/PACKAGING.md`](../../docs/PACKAGING.md) | Wheel gate + `scripts/testpypi-dry-run.py` |
| [`docs/VAULT.md`](../../docs/VAULT.md) | Vault + audio split |
| [`storage/README.md`](../../storage/README.md) | Private protocol index (exportPrefs, boardSkills, Alignerr) |
| [`.claude/commands/wrap.md`](../../.claude/commands/wrap.md) | `/wrap` · `/jen:wrap` |
| Global router | `~/.claude/commands/jen/pdf.md` → thin links into this repo |

---

## Current status

### Alignerr (both SUBMITTED)

| Role | Status | PDF |
|---|---|---|
| Voice Recording Specialist | ✅ SUBMITTED 2026-07-24 | `storage/jenni/_exports/Alignerr/jenni-alignerr-voice-recording-resume-dark-v4.pdf` |
| AI Red Team Tester | ✅ SUBMITTED 2026-07-24 | `storage/jenni/_exports/Alignerr-AI-Red-Team/jenni-alignerr-ai-red-team-resume-dark-v3.pdf` |

Netflix **CLOSED**. Do not rebuild Alignerr/Netflix unless human asks.

### Go-to packs

| Pack | HTML | Dark PDF |
|---|---|---|
| voice ⭐ | `storage/jenni/defaults/jenni-default-voice-resume.html` | `_exports/defaults/jenni-default-voice-resume-dark.pdf` |
| ai-trainer | `…/jenni-default-ai-trainer-resume.html` | `…/jenni-default-ai-trainer-resume-dark-v3.pdf` |
| general | `…/jenni-default-resume.html` | `…/jenni-default-resume-dark.pdf` |

### Command / prefs

- **Jenni `exportPrefs`:** one **dark** résumé PDF only — `profiles/jenni-resume.json#exports.exportPrefs`
- **`/make-resume` does not auto-build cover letter** — use `/make-cover-letter`
- Pasted job URL → create `storage/_job-listings/<App>/` if missing
- Project wrap: **`wrap.md`** (`pdf-wrap.md` = alias)
- Global `/jen:pdf` = thin router into repo paths; **`boardSkills` sync reminder** lives there + `storage/README.md`
- Personal `make-resume.md` / `make-cover-letter.md` / `make-work-examples.md` stay **gitignored**

### Hub

- http://127.0.0.1:8787/vault · `/?doc=storage/jenni/defaults/jenni-default-voice-resume.html`
- http://127.0.0.1:8787/recipes · `GET /api/recipe-gallery` · palette try `/?palette=slate-ink&mode=dark`
- **Responsive chrome (2026-07-25):** shared `Library | Recipes | Vault` `.hub-nav` on all three surfaces;
  same breakpoints as library (`991.98` / `1200` / `1400`); `body.hub-shell` vs `body.hub-page`;
  styles in `hub.css` (not per-page inline). See `docs/PREVIEWER.md` + `www-theme-kit/profiles/pdf-designer.json`.

### Packaging

- ✅ `python scripts/check-wheel-assets.py` PASS (v0.4.0)
- ✅ `python scripts/testpypi-dry-run.py` PASS — fresh venv → site-packages `share/` → `check_generation` 10/10
- ❌ TestPyPI **upload** — no `TESTPYPI_TOKEN` / account in credential DB

### Still open

1. Sync `boardSkills` when she adds LinkedIn tags (still current as of 2026-07-24; no new tags this turn).
2. **Create TestPyPI account + API token** → `python scripts/testpypi-dry-run.py --upload`.

---

## Reflect (compact)

| | |
|---|---|
| **Mode** | pdf-designer + theme (www-theme-kit profile) |
| **Observation** | Vault/recipes shipped as one-off pages: purple JN accents, no shared nav, `body { overflow:hidden }` blocked scroll; kit BREAKPOINTS row said “see mcp cache” |
| **Root cause** | Subpages grown beside the library shell without adopting hub chrome / shared breakpoint contract |
| **Chosen improvement** | One `.hub-nav` + `hub-shell`/`hub-page` modes in `hub.css`; pin switch points in kit profile + BREAKPOINTS index |
| **Landed now** | Shared nav + responsive hub-page styles · vault regex fix · `profiles/pdf-designer.json#breakpoints` · BREAKPOINTS.md row |
| **Validated by** | Playwright 390–1200: 0 spill, `.on` correct; vault renders after `stripProto` |
| **Follow-up** | TestPyPI token → `--upload`; boardSkills on new LinkedIn tags |

---

## Prompt (copy into a new chat)

```
Continue pdf-designer from Plans/_Active/2026-07-24-jenni-vault-hub-handoff.md (dev-log s012).

Alignerr Voice + AI Red Team are both SUBMITTED — do not rebuild.
Jenni /make-resume default = one dark résumé. Cover letter = /make-cover-letter only.
/wrap → .claude/commands/wrap.md. /jen:pdf = thin router.

Hub chrome responsive ✅ — Library|Recipes|Vault shared nav; hub-shell vs hub-page;
same 991.98/1200/1400 switches (PREVIEWER.md · www-theme-kit profiles/pdf-designer.json).

Local-wheel dry-run ✅. Next preferred:
  (A) boardSkills sync if new LinkedIn tags → storage/jenni/resume-source.json#boardSkills
  (B) human creates TestPyPI token → python scripts/testpypi-dry-run.py --upload (PACKAGING.md)
Optional polish: card-stack / recipes tables below 576 if table-scroll still feels cramped.

Hub: http://127.0.0.1:8787/vault · http://127.0.0.1:8787/recipes
```
