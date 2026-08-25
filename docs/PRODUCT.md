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
| Folder UX (clone tree) | [`WORKSPACE-LAYOUT.md`](WORKSPACE-LAYOUT.md) — root-noun README scaffolds; SEGO data migrated and `storage/` retired |
| Product hub (local) | `C:\Github\product-design` · `docs/LAUNCH-PDF-DESIGNER.md` (Patreon first; Gumroad when extras exist) |
| Private marketing (local) | `docs/MARKETING.md` (gitignored — same folder as public docs) |
| Engineering checklist | [`../Plans/_Active/2026-08-22-product-polish-and-release-readiness.md`](../Plans/_Active/2026-08-22-product-polish-and-release-readiness.md) |

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
| SaaS wants your data | Local-first; private root nouns are never required for the public demo |

## Three surfaces, one engine

| Surface | Audience | Today | Monetize? |
|---|---|---|---|
| **Open toolkit** | Devs, agents, power users | ✅ MIT on GitHub | Free — trust + contributors |
| **Personal protocol** | Founders using this clone privately | ✅ local root nouns + bare commands | Never sell *their* vaults |
| **Packaged app** (pre-release) | Job-seekers who want Canva ease without lying | 🟡 Windows Electron/NSIS artifact builder; no public release | Paid / freemium **shell** |

**Hard privacy split:** root nouns (`users/` · `vaults/` · …) ship **README + examples only**;
real local data remains gitignored. `storage/` is retired, while the resolver keeps old URLs working.
GitHub ships
**`*.example.md` only** for commands. A stranger proves the product with
`examples/` + `themes/` alone — [`GETTING-STARTED.md`](GETTING-STARTED.md).

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

## Windows desktop shell (pre-release; not a storefront promise)

Prefer a **thin shell** over a second renderer.

1. Windows 10/11 x64 per-user Electron/NSIS installer that launches Design Hub on an ephemeral `127.0.0.1` port
2. Guided résumé wizard — vault → skills → palette → export light+dark
3. Job-application wizard (capture → gap-check → export) for non-agents
4. Template / recipe gallery (collage + letter packs)
5. No cloud sync in this product path; vaults remain local

```
┌─────────────────────────────────────────────────────────┐
│  Paid shell (pre-release)                                 │
│  OS installer · starts pdf_tool.preview · wizard chrome  │
└──────────────────────────┬──────────────────────────────┘
                           │ localhost HTTP
┌──────────────────────────▼──────────────────────────────┐
│  Free MIT core (ships today)                             │
│  Design Hub + pdf_tool + themes/ + layouts/ + QA         │
└─────────────────────────────────────────────────────────┘
```

Packaging precursor: [`PACKAGING.md`](PACKAGING.md) (wheel must include `themes/` + `layouts/`).
TestPyPI upload and fresh-install proof passed for `pdf-designer 0.4.0` on 2026-08-21. We deliberately will not publish production PyPI now: it is a developer library channel, while the Windows Electron/NSIS route is the customer install path. Installer proof: [`WINDOWS-ELECTRON.md`](WINDOWS-ELECTRON.md).

## Paying for PDF Designer (PayPal · Gumroad · Microsoft Store)

**Today (2026-08-25):** the honest ask is a **tip** on the free GitHub clone. There is
no listable installer. **Do not create an Azure Artifact Signing (Trusted Signing)
account this month** — that is the $9.99 click. Resume signing next month if budget
allows. Unsigned `PDF-Designer-Setup-0.1.0.exe` stays local-only.

| Channel | What they pay | What we pay | Role |
|---|---|---|---|
| **GitHub clone** | $0 | $0 | Always live. README suggested tip **$3 or $5** via [PayPal.Me/jenninexus](https://paypal.me/jenninexus) or [Patreon](https://www.patreon.com/c/JenniNexus). Tip ≠ installer. |
| **JN `/products` $5** (later) | $5 | PayPal merchant fees on that sale | Preferred paid link **after** a Valid-signed NSIS. PayPal **Standard Checkout** + webhook fulfilment — not PayPal.Me as the product button. |
| **Gumroad $6** (later) | $6 | Gumroad’s cut (higher than direct PayPal) | Same signed EXE; convenience listing, not a premium edition. |
| **Azure Trusted Signing** | — | **$9.99 for each month the Artifact Signing account exists** (Basic, not pro-rated). $0 in months you delete the account after a timestamped sign. | Stamps a **sideload** `.exe` so Windows is not “Unknown publisher.” Required for Gumroad / JN `$5` EXE. Not required for GitHub. |
| **Microsoft Store (Copilot model)** | $0 for Copilot | **$0/month** | Martian Copilot (`9PN7W26D3JQ3`) is a **free Hosted PWA**. Partner Center is **not a monthly bill**. Microsoft signs the MSIX. No Azure $9.99. |
| **Microsoft Store (paid PDF Designer)** | customer pays Store price | **15%** of net receipts (non-game Microsoft commerce; games 12%). Plus MSIX packaging + certification of a ~350 MB local Python/Chromium app | Possible later as a **second** channel. Cannot copy Copilot’s “just wrap a website.” JN page would be “Get it on Microsoft Store,” not PayPal for that binary. Do not publish PDF Designer under the **Martian Games** publisher name. |

**Best route while broke:** keep GitHub free + visible PayPal.Me / Patreon tips. Hold
Azure. Do not list unsigned EXE. Do not turn on JN `$5` checkout or Gumroad.

**Best route when we can spare ~$10 for one release month:** create Artifact Signing
Basic (East US) → identity validation → `npm run dist:signed` → `verify-authenticode.ps1 -RequireSigned` → upload **that** EXE to Gumroad `$6` / later JN Checkout `$5` → **delete the Artifact Signing account** so it does not recur. Timestamped signature on that build stays Valid; a **new** Setup EXE needs the account again that month.

**Why not Store instead of $9.99:** Copilot avoided Azure because it is a free website
shell (`copilot.martiangames.com`). PDF Designer is local-first (`127.0.0.1`). A Store
listing would still need a real MSIX, Store review on every binary, and either a free
listing (no installer money) or 15% of each paid sale. Playbook:
`C:\Github\martian-portal\docs\publish\MICROSOFT-STORE.md`.

**Partner Center:** the existing MG developer account does **not** charge monthly for
a free app sitting in the Store. Fees are the old one-time registration (already paid /
waived on new individual flow) and a **cut of paid Store commerce only**. Copilot IAP
is unused; that listing costs $0/month.

Engineering gates for any paid EXE: [`WINDOWS-ELECTRON.md`](WINDOWS-ELECTRON.md).
Hub card + catalog: `C:\Github\product-design\docs\PDF-DESIGNER.md`.

## How to market it (public-safe)

| Layer | Message | Proof |
|---|---|---|
| Free GitHub | Résumé creator you control — vault + skills + palettes | `resume-studio/` · smoke · Hub |
| Who it’s for now | Agents + power users who refuse to lie on applications | Not a Canva beginner pitch yet |
| Paid later | Installer + guided vault/export around the **same** engine | Shell-over-Hub |
| Never as product | Someone’s vault, job history, or private brand maps | Privacy split *is* the brand |

Channels: README + Hub GIF from **`examples/` only** · TestPyPI only for developer
package rehearsal (no production PyPI release) · short “export +
check_generation” clips. Keep personal career work and Patreon drafts out.

Longer SEGO channel plan: `docs/MARKETING.md` (gitignored).

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
| Where is private data? | [`WORKSPACE-LAYOUT.md`](WORKSPACE-LAYOUT.md) (root nouns) · [`STORAGE.md`](STORAGE.md) (`storage/` alias) |
| Verified? | [`QA.md`](QA.md) |

---

*Last updated 2026-08-25 — free GitHub + tip is the live ask; Azure Trusted Signing held until budget allows; unsigned NSIS is not listable.*
