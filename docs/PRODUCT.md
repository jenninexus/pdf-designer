# Product & commercialization — pdf-designer

**Business / product-direction SSOT** for the free GitHub résumé toolkit and a possible
paid shell later. Clone path: [`GETTING-STARTED.md`](GETTING-STARTED.md). Architecture:
[`PUBLIC-LOCAL-SPLIT.md`](PUBLIC-LOCAL-SPLIT.md).

| | |
|---|---|
| Free / open core | Engine + themes + layouts + guards + Design Hub + public docs + `*.example.md` |
| Paid later (hypothesis) | Packaged desktop app — installer + guided vault/export UX |
| **Public product story** | Résumé creator for a broken job market — **vaults**, skills, palette prefs |
| Public demo | [`../examples/resume-studio/`](../examples/resume-studio/) |
| Folder UX (target) | [`WORKSPACE-LAYOUT.md`](WORKSPACE-LAYOUT.md) — root `users/` · `vaults/` · `profiles/` · … |
| Private marketing (local) | `docs/MARKETING.md` (gitignored — same folder as public docs) |
| Engineering checklist | [`../Plans/_Active/2026-08-13-intuitive-workspace-product.md`](../Plans/_Active/2026-08-13-intuitive-workspace-product.md) |

---

## Thesis (one sentence)

**Local-first résumé studio for a shitty job market:** claims live in a private vault,
skills and palette prefs are yours, and the tool prints ATS-honest light PDFs + branded
dark ones — free MIT engine on GitHub; a future paid app sells guided UX, not your career data.

## Why this exists

Boards and “AI match” tools reward keyword soup and punish honest specialists. Applicants
need **source-backed** résumés, **palette-controlled** exports that still parse, and a
workflow that **asks before inventing gaps** — not another cloud form that owns their history.

| Pain | Our answer |
|---|---|
| Generic templates | Per-user **vault** + **palette prefs** + dual light/dark |
| Claims that drift | Vault is the brain — `check_vault` / gap-check before prose |
| ATS shreds fancy fonts | Light PDF + `check_ats`; dark is for humans |
| SaaS wants your data | Local-first; `storage/` never required for the public demo |

## Three surfaces, one engine

| Surface | Audience | Today | Monetize? |
|---|---|---|---|
| **Open toolkit** | Devs, agents, power users | ✅ MIT on GitHub | Free — trust + contributors |
| **Personal protocol** | Founders using this clone privately | ✅ local `storage/` + bare commands | Never sell *their* vaults |
| **Packaged app** (future) | Job-seekers who want Canva ease without lying | ❌ not built | Paid / freemium **shell** |

**Hard privacy split:** `storage/` stays gitignored. GitHub ships **`*.example.md` only** for
commands. A stranger proves the product with `examples/` + `themes/` alone —
[`GETTING-STARTED.md`](GETTING-STARTED.md).

Network brand kits (`www-theme-kit`, `syna-theme-kit`) are **private infra**, not part of
the public GitHub pitch. Public color defaults live in-repo under `themes/`.

## What “free on GitHub” must always include

- HTML → PDF (light/ATS + dark branded), variants, merge, PNG verify
- Palette / overflow / generation QA ([`QA.md`](QA.md))
- Design Hub previewer
- Collage / layout recipes
- Public protocol seeds: `make-resume.example.md` · cover · work-examples · collage
- Docs: [`PUBLIC-LOCAL-SPLIT.md`](PUBLIC-LOCAL-SPLIT.md) · [`PRODUCT.md`](PRODUCT.md) ·
  [`GETTING-STARTED.md`](GETTING-STARTED.md) · [`VAULT.md`](VAULT.md) shape
- Stranger-proof demo: `python scripts/smoke-white-label.py` + `examples/resume-studio/`

## Future paid app (ideas — not commitments)

Prefer a **thin shell** over a second renderer.

1. Installer that launches Design Hub on `127.0.0.1`
2. Guided résumé wizard — vault → skills → palette → export light+dark
3. Job-application wizard (capture → gap-check → export) for non-agents
4. Template / recipe gallery (collage + letter packs)
5. Cloud-optional sync of *layouts/themes only* — never require cloud for vaults

```
┌─────────────────────────────────────────────────────────┐
│  Paid shell (future)                                     │
│  OS installer · starts pdf_tool.preview · wizard chrome  │
└──────────────────────────┬──────────────────────────────┘
                           │ localhost HTTP
┌──────────────────────────▼──────────────────────────────┐
│  Free MIT core (ships today)                             │
│  Design Hub + pdf_tool + themes/ + layouts/ + QA         │
└─────────────────────────────────────────────────────────┘
```

Packaging precursor: [`PACKAGING.md`](PACKAGING.md) (wheel must include `themes/` + `layouts/`).
TestPyPI upload still needs a human token.

## How to market it (public-safe)

| Layer | Message | Proof |
|---|---|---|
| Free GitHub | Résumé creator you control — vault + skills + palettes | `resume-studio/` · smoke · Hub |
| Who it’s for now | Agents + power users who refuse to lie on applications | Not a Canva beginner pitch yet |
| Paid later | Installer + guided vault/export around the **same** engine | Shell-over-Hub |
| Never as product | Someone’s vault, job history, or private brand maps | Privacy split *is* the brand |

Channels: README + Hub GIF from **`examples/` only** · PyPI when TestPyPI is green ·
short “export + check_generation” clips. Keep personal career work and Patreon drafts out.

Longer SEGO channel plan: `storage/docs/MARKETING.md`.

## Non-goals

- Auto-submit applications
- Cloud-only PII or SaaS vault as the default
- Inventing claims / résumé lies
- Selling private founder vaults or application history
- Shipping machine MCP config or bare session commands — **examples only**
- Shipping `www-theme-kit` as a required public dependency

## Doc map

| Question | Doc |
|---|---|
| Public vs private vs paid? | [`PUBLIC-LOCAL-SPLIT.md`](PUBLIC-LOCAL-SPLIT.md) |
| How do I clone and use it? | [`GETTING-STARTED.md`](GETTING-STARTED.md) |
| PyPI / wheel? | [`PACKAGING.md`](PACKAGING.md) |
| What may be claimed? | [`VAULT.md`](VAULT.md) · [`JOB-ASSESSMENT.md`](JOB-ASSESSMENT.md) |
| Where is private data? | [`STORAGE.md`](STORAGE.md) · `storage/docs/` |
| Verified? | [`QA.md`](QA.md) |

---

*Last updated 2026-08-12 — PUBLIC-LOCAL-SPLIT + GETTING-STARTED rename; history scrub still
pending human force-push auth.*
