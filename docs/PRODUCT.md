# Product & commercialization — pdf-designer

**This is the business / product-direction SSOT** (free GitHub core → optional paid app later).
It is **not** the white-label how-to — that stays in [`WHITE-LABEL.md`](WHITE-LABEL.md)
(how a clone uses the public engine **without** private vaults).

| | |
|---|---|
| Free / open core | Engine + themes + layouts + guards + Design Hub + public docs |
| Paid later (hypothesis) | Packaged desktop app, templates marketplace, guided “studio” UX |
| Inspiration | PowerPoint / Canva-class **layout + collage** tools — see collage engine + Design Hub |
| Active engineering checklist | [`../Plans/_Active/2026-07-21-next-agent-product-prompt.md`](../Plans/_Active/2026-07-21-next-agent-product-prompt.md) |
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
- A stranger-proof demo: `python scripts/smoke-white-label.py` (tracked `examples/` only)

## What a future paid app could add (without forking the engine)

Ideas only — not commitments. Prefer thin shells over a second renderer.

1. **Installer that launches Design Hub** (shell-over-Hub — see below)
2. **Template / recipe gallery** with one-click “make my resume / collage”
3. **Guided job-application wizard** (capture listing → gap-check → export) for non-agents
4. **Cloud-optional sync** of *layouts/themes only* — never require cloud for vaults
5. **Pro presets / print packs** as paid content while the engine stays MIT

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
│  • recipe gallery chrome + guided export flows           │
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
| Recipe gallery | Hub surface over tracked `layouts/` + `themes/presets/` | Structure + color registries already exist — UI, not a second engine |
| Data | Local `storage/` stays private / optional | Paid app never requires cloud vaults |
| Packaging precursor | PyPI / wheel with public assets | [`PACKAGING.md`](PACKAGING.md) — must ship `themes/` + `layouts/` inside the wheel |

**Spike done when:** this section + PACKAGING path resolution are honest, and the
next build step is either (a) Hub recipe-gallery UX or (b) TestPyPI dry-run —
not another architecture debate.

## Non-goals

- Auto-submit applications
- Cloud-only PII or a SaaS vault as the default
- Inventing claims / résumé lies
- Selling private founder vaults or application history

## Doc map (who owns what)

| Question | Doc |
|---|---|
| How do I clone and use it publicly? | [`WHITE-LABEL.md`](WHITE-LABEL.md) |
| How do non-devs install (PyPI / wheel)? | [`PACKAGING.md`](PACKAGING.md) |
| What do we build next (engineering)? | Active plan under `Plans/_Active/` |
| What may be claimed / how applications work? | [`VAULT.md`](VAULT.md) · [`JOB-ASSESSMENT.md`](JOB-ASSESSMENT.md) |
| Where is private data? | [`STORAGE.md`](STORAGE.md) |
| Is this “verified”? | [`QA.md`](QA.md) |

---

*Last updated 2026-07-21 — free-vs-paid story + shell-over-Hub spike; WHITE-LABEL stays the
public how-to only; PACKAGING owns the wheel/PyPI path.*
