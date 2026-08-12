# Resume Studio — public product entry

**This folder is the marketed front door** for the free GitHub résumé creator.

Inspired by a broken job market: keyword soup, opaque board ranks, and templates that
look identical. This toolkit keeps **your claims in a vault**, **your skills tags** and
**palette prefs** under your control, and prints **ATS-honest light PDFs** plus branded
dark ones — all local, no SaaS vault.

> Not private data. Everything here points at tracked `examples/` + `themes/` only.
> Real applicants live under gitignored `storage/` on a developer machine.

| Want | Go here |
|---|---|
| Product thesis (free vs paid) | [`../../docs/PRODUCT.md`](../../docs/PRODUCT.md) |
| Clone how-to (no vaults) | [`../../docs/GETTING-STARTED.md`](../../docs/GETTING-STARTED.md) |
| Vault shape (what may be claimed) | [`../../docs/VAULT.md`](../../docs/VAULT.md) |
| Palette rule | [`../../themes/PALETTE-RULES.md`](../../themes/PALETTE-RULES.md) |
| Example HTML + profile | [`../profiles/default-resume/`](../profiles/default-resume/) |
| Brand map template | [`../brand-design/`](../brand-design/) |
| Job-folder template | [`../_job-listings/`](../_job-listings/) |
| Protocol seeds (agent commands) | [`../../.claude/commands/*.example.md`](../../.claude/commands/) |

---

## 60-second proof (fresh clone)

```bash
pip install -e ".[dev]" && playwright install chromium
python scripts/smoke-white-label.py          # QA + light/dark PDF + ATS
python -m pdf_tool.preview                   # Design Hub → http://127.0.0.1:8787/
```

Or open the example résumé directly in the Hub:

`http://127.0.0.1:8787/?doc=examples/profiles/default-resume/default-resume.html`

---

## What “customizable vault” means (public shape)

Copy the example files into your own gitignored `storage/` (see [`../README.md`](../README.md)):

| Layer | Example seed | You customize |
|---|---|---|
| Person | `profiles/default-resume/user.example.json` | Contact, brand pointer, voice prefs |
| Vault | `profiles/default-resume/resume-source.example.json` | Claims, skills / `boardSkills`, tracks |
| Profile | `profiles/default-resume/profile.example.json` | Layout + `exportPrefs` (light + dark) |
| Palette | `brand-design/brand-example.json` · `themes/presets/` | Colors mapped into token names |

Guards (`check_vault`, `check_palette`, `check_generation`, `check_ats`) keep the print
honest. Protocol for agents: start from `make-resume.example.md` (copy → bare
`make-resume.md` locally if you add personal specifics).

---

## Why a separate directory?

`examples/profiles/` holds **engine fixtures**. This folder holds the **product story** —
so README / marketing / paid-app planning can point at one URL without dragging
collage fixtures or private SEGO ritual into the pitch.
