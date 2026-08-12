# Product & commercialization — pdf-designer

**This is the business / product-direction SSOT** (free GitHub core → optional paid app later).
It is **not** the white-label how-to — that stays in [`WHITE-LABEL.md`](WHITE-LABEL.md)
(how a clone uses the public engine **without** private vaults).

| | |
|---|---|
| Free / open core | Engine + themes + layouts + guards + Design Hub + public docs + example protocol seeds |
| Paid later (hypothesis) | Packaged desktop app, templates marketplace, guided “studio” UX |
| **Public product story** | A **résumé creator for a broken job market** — customizable **vaults**, skills, palette prefs |
| Active engineering checklist | [`../Plans/_Active/2026-08-12-product-privacy-packaging.md`](../Plans/_Active/2026-08-12-product-privacy-packaging.md) |
| QA contract | [`QA.md`](QA.md) — judge the artifact |
| Public demo entry | [`../examples/resume-studio/`](../examples/resume-studio/) |
| Private marketing detail (local) | `storage/docs/MARKETING.md` (gitignored — not on GitHub) |

---

## Thesis (one sentence)

**Local-first résumé studio for a shitty job market:** your claims live in a private vault,
your skills and palette prefs are yours, and the tool prints ATS-honest light PDFs + branded
dark ones — free MIT engine on GitHub; future paid app sells guided UX, not your career data.

## Why this exists (market frame)

Boards and “AI match” tools reward keyword soup and punish honest specialists. Applicants
need **source-backed** résumés they can trust, **palette-controlled** exports that still parse,
and a workflow that **asks before inventing gaps** — not another cloud form that owns their
history.

| Pain | Our answer |
|---|---|
| Generic templates that look like everyone else | Per-user **vault** + **palette prefs** + dual light/dark |
| Claims that drift from truth | Vault is the brain — `check_vault` / gap-check before prose |
| ATS shreds fancy fonts | Light PDF + `check_ats`; dark is for humans |
| SaaS wants your data | Local-first; `storage/` never required for the public demo |

## Two products, one codebase

| Surface | Audience | Ships today? | Monetize? |
|---|---|---|---|
| **Open toolkit** (`pdf_tool` + `themes/` + `layouts/` + docs + `*.example.md`) | Developers, power users, other agents | ✅ MIT | Free — grows trust + contributors |
| **Personal protocol** (`storage/` vaults, bare `/make-resume`) | Founders using this repo privately | ✅ local-only | Never sell *their* PII / vaults |
| **Packaged app** (future) | Job-seekers who want Canva ease without lying | ❌ not built | Paid / freemium *shell* around the same engine |

**Hard privacy split (do not blur):** anything under `storage/` (vaults, real applications,
brand maps, images) stays gitignored. Bare `.claude/commands/{start,wrap,make-*}.md` are
**dev-only** — GitHub ships **`*.example.md` only**. The public repo must stay clone-safe
from `examples/` + `themes/` alone — that is the white-label path.

## What “free on GitHub” must always include

- HTML → PDF (light/ATS + dark branded), variants, merge, PNG verify
- Palette / overflow / generation QA gates ([`QA.md`](QA.md))
- Design Hub previewer
- Collage / layout recipes (`layouts/`, `themes/default-collage.json`)
- Public protocol seeds: `make-resume.example.md` · cover · work-examples · collage
- Documented contracts ([`AGENTS.md`](../AGENTS.md), [`SSOT.md`](SSOT.md), [`WHITE-LABEL.md`](WHITE-LABEL.md), [`VAULT.md`](VAULT.md))
- A stranger-proof demo: `python scripts/smoke-white-label.py` + [`examples/resume-studio/`](../examples/resume-studio/)

## What a future paid app could add (without forking the engine)

Ideas only — not commitments. Prefer thin shells over a second renderer.

1. **Installer that launches Design Hub** (shell-over-Hub — see below)
2. **Guided résumé wizard** — create vault → pick skills tags → choose palette → export light+dark
3. **Job-application wizard** (capture listing → gap-check → export) for non-agents
4. **Template / recipe gallery** with one-click collage + letter packs
5. **Cloud-optional sync** of *layouts/themes only* — never require cloud for vaults

## Paid-app spike — shell-over-Hub (design decision)

**Do not fork the renderer.** The paid product is a thin distribution + UX layer
around the same `pdf_tool` engine and the same Design Hub HTTP UI that already
ships free.

```
┌─────────────────────────────────────────────────────────┐
│  Paid shell (future)                                     │
│  • OS installer / start menu                             │
│  • starts `pdf_tool.preview` on 127.0.0.1                │
│  • opens Hub (browser today; native window optional)     │
│  • résumé / vault wizard + recipe gallery chrome         │
└──────────────────────────┬──────────────────────────────┘
                           │ localhost HTTP (unchanged)
┌──────────────────────────▼──────────────────────────────┐
│  Free MIT core (ships today)                             │
│  Design Hub + pdf_tool + themes/ + layouts/ + QA gates   │
└─────────────────────────────────────────────────────────┘
```

| Decision | Choice | Why |
|---|---|---|
| First shell | **Browser → Design Hub** (`python -m pdf_tool.preview`) | Already the interactive SSOT; zero new deps |
| Native window | **pywebview parked** | Optional polish only ([archived](../Plans/_Archive/2026-07-11-design-hub-parked-phases.md)); revive when packaging for non-Python users |
| Recipe gallery | ✅ Hub `/recipes` + `/api/recipe-gallery` over `layouts/` + `themes/presets/` | Structure + color registries already exist — UI, not a second engine |
| Data | Local `storage/` stays private / optional | Paid app never requires cloud vaults |
| Packaging precursor | PyPI / wheel with public assets | [`PACKAGING.md`](PACKAGING.md) — must ship `themes/` + `layouts/` inside the wheel |

**Spike status (2026-07-25):** Hub `/recipes` + local-wheel dry-run both shipped.
Next packaging step is **TestPyPI upload** (needs account token) — see
[`PACKAGING.md`](PACKAGING.md). Not another architecture debate.

## How to market it (public-safe)

| Layer | Message | Proof |
|---|---|---|
| **Free GitHub** | Résumé creator you control — vault + skills + palettes, local PDF | `examples/resume-studio/` · `smoke-white-label.py` · Hub |
| **Who it’s for now** | Agents + power users who refuse to lie on applications | Not a Canva beginner pitch (yet) |
| **Paid later** | Installer + guided vault/export UX around the **same** engine | Shell-over-Hub — sell time saved |
| **Never as product** | Someone’s vault, job history, or private brand maps | Privacy split is the brand |

Channels for the free core: README + Hub demo GIF from **`examples/` only** · TestPyPI/PyPI
when the token exists · short “export + check_generation” clips. Keep personal career work
and Patreon drafts out of public marketing.

## Non-goals

- Auto-submit applications
- Cloud-only PII or a SaaS vault as the default
- Inventing claims / résumé lies
- Selling private founder vaults or application history
- Shipping machine-local config (`.config/mcp-pdf-designer.json`) — **`.example` only** on GitHub
- Shipping bare `.claude/commands/{start,wrap,README,make-*}.md` — **`*.example.md` only**

## Doc map (who owns what)

| Question | Doc |
|---|---|
| How do I clone and use it publicly? | [`WHITE-LABEL.md`](WHITE-LABEL.md) · [`../examples/resume-studio/`](../examples/resume-studio/) |
| How do non-devs install (PyPI / wheel)? | [`PACKAGING.md`](PACKAGING.md) |
| What do we build next (engineering)? | Active plan under `Plans/_Active/` |
| What may be claimed / how applications work? | [`VAULT.md`](VAULT.md) · [`JOB-ASSESSMENT.md`](JOB-ASSESSMENT.md) |
| Where is private data? | [`STORAGE.md`](STORAGE.md) · local `storage/docs/` |
| Is this “verified”? | [`QA.md`](QA.md) |

---

*Last updated 2026-08-12 — résumé-studio product frame; commands `*.example.md` only on GitHub;
TestPyPI upload still needs a token.*
