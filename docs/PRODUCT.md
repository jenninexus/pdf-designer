# Product & commercialization — pdf-designer

**This is the business / product-direction SSOT** (free GitHub core → optional paid app later).
It is **not** the white-label how-to — that stays in [`WHITE-LABEL.md`](WHITE-LABEL.md)
(how a clone uses the public engine **without** private vaults).

| | |
|---|---|
| Free / open core | Engine + themes + layouts + guards + Design Hub + public docs |
| Paid later (hypothesis) | Packaged desktop app, templates marketplace, guided “studio” UX |
| Inspiration | PowerPoint / Canva-class **layout + collage** tools — see collage engine + Design Hub |
| Active engineering checklist | [`../Plans/_Active/2026-07-14-professional-product-roadmap.md`](../Plans/_Active/2026-07-14-professional-product-roadmap.md) |
| QA contract | [`QA.md`](QA.md) — judge the artifact |

---

## Thesis (one sentence)

**Local-first document studio:** vault-backed truth → tailored HTML → print-perfect PDF/PNG,
with a free MIT engine on GitHub and a future packaged app that sells the *experience*
(guided layouts, collage recipes, one-click export), not the private career data.

## Two products, one codebase

| Surface | Audience | Ships today? | Monetize? |
|---|---|---|---|
| **Open toolkit** (`pdf_tool` + `themes/` + `layouts/` + docs) | Developers, power users, other agents | ✅ MIT | Free — grows trust + contributors |
| **Personal protocol** (`storage/` vaults, `/make-resume`) | Founders using this repo privately | ✅ local-only | Never sell *their* PII / vaults |
| **Packaged app** (future) | Non-dev creatives who want PowerPoint/collage ease | ❌ not built | Paid / freemium *shell* around the same engine |

**Hard privacy split (do not blur):** anything under `storage/` (vaults, real applications,
brand maps, images) stays gitignored. The public repo must stay clone-safe and demoable from
`examples/` + `themes/` alone — that is the white-label path.

## What “free on GitHub” must always include

- HTML → PDF (light/ATS + dark branded), variants, merge, PNG verify
- Palette / overflow / generation QA gates ([`QA.md`](QA.md))
- Design Hub previewer
- Collage / layout recipes (`layouts/`, `themes/default-collage.json`)
- Documented contracts ([`AGENTS.md`](../AGENTS.md), [`SSOT.md`](SSOT.md), [`WHITE-LABEL.md`](WHITE-LABEL.md))

## What a future paid app could add (without forking the engine)

Ideas only — not commitments. Prefer thin shells over a second renderer.

1. **Installer + desktop window** (pywebview or similar was parked; Design Hub browser is today’s shell)
2. **Template / recipe gallery** with one-click “make my resume / collage”
3. **Guided job-application wizard** (capture listing → gap-check → export) for non-agents
4. **Cloud-optional sync** of *layouts/themes only* — never require cloud for vaults
5. **Pro presets / print packs** as paid content while the engine stays MIT

## Non-goals

- Auto-submit applications
- Cloud-only PII or a SaaS vault as the default
- Inventing claims / résumé lies
- Selling private founder vaults or application history

## Doc map (who owns what)

| Question | Doc |
|---|---|
| How do I clone and use it publicly? | [`WHITE-LABEL.md`](WHITE-LABEL.md) |
| What do we build next (engineering)? | Active plan under `Plans/_Active/` |
| What may be claimed / how applications work? | [`VAULT.md`](VAULT.md) · [`JOB-ASSESSMENT.md`](JOB-ASSESSMENT.md) |
| Where is private data? | [`STORAGE.md`](STORAGE.md) |
| Is this “verified”? | [`QA.md`](QA.md) |

---

*Last clarified 2026-07-21 — product direction was previously implied by the roadmap + white-label
split; this file makes the free-vs-paid story explicit so agents stop treating WHITE-LABEL as a business plan.*
