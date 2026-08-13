# Active plan — Product privacy · packaging · marketing

**Date:** 2026-08-12 · **Host:** SEGOPC  
**Prior hub wave (complete):** [`../_Complete/2026-08-10-hub-layouts-letterhead.md`](../_Complete/2026-08-10-hub-layouts-letterhead.md)  
**Prior product wave (complete):** [`../_Complete/2026-07-21-next-agent-product-prompt.md`](../_Complete/2026-07-21-next-agent-product-prompt.md)

---

## Session checklist (2026-08-12)

- [x] Confirm `storage/` never tracked (gitignore + `git ls-files` empty)
- [x] Untrack `.config/mcp-pdf-designer.json` — keep `.example.json` only on GitHub
- [x] Archive completed Plans (`07-21`, `08-10`) → `_Complete/`
- [x] Add private `storage/docs/` index (dev-only / personal workspace notes)
- [x] Refresh public PRODUCT / WHITE-LABEL / STORAGE / docs README / ROADMAP
- [x] Public seeds: `make-cover-letter.example.md` · `make-work-examples.example.md`
- [x] Durable lesson: Hub Collages + Profiles filter hides untagged projects
- [x] **Privatize bare `.claude/commands/`** — track **only** `*.example.md` (start/wrap/README/make-* local)
- [x] Add `make-collage.example.md`
- [x] Wire `/reflect` into project wrap + mandatory next-agent handoff
- [x] Public product entry: `examples/resume-studio/` + job-market résumé pitch in PRODUCT
- [ ] **TestPyPI upload** — needs `TESTPYPI_TOKEN` → `python scripts/testpypi-dry-run.py --upload`
- [ ] **Push origin/main** — needs `jenninexus` GitHub auth (MonoFinity gh fails “repo not found”)
- [x] **Public vs local SSOT** — `docs/PUBLIC-LOCAL-SPLIT.md` + `GETTING-STARTED.md` (WHITE-LABEL stub)
- [x] Tracked `storage/docs/README.md` placeholder; MARKETING / WORKSPACE / HISTORY-SCRUB private
- [x] **Codex command sync** — global `/pdf` + seven repo-local adapters regenerated one-way from Claude sources; `.codex/` stays private
- [x] **Public command audit** — replace the personal-content `make-resume.example.md` with a portable placeholder-only seed
- [x] **Public smoke repair** — default résumé now passes `check_generation` + light/dark export + ATS cues (`Job Title` / `Work Experience` / `Education`)
- [x] **Wheel hygiene** — clean stale `build/` and reject `_exports` / `_variants` / generated media in packaged `share/`
- [ ] **History scrub** — see `storage/docs/HISTORY-SCRUB.md` (filter-repo + human force-push)
- [x] Deepen `examples/resume-studio/` with a clone-safe walkthrough + direct Hub example link
- [ ] Optional: PyPI production after TestPyPI succeeds
- [ ] Optional: paid-shell spike (installer → Design Hub) — still shell-over-Hub, no second renderer

### Never

- Auto-submit · invent claims · fork the renderer · commit `storage/` · reopen Netflix  
- Force-add bare `.claude/commands/{start,wrap,README,make-*}.md` to GitHub

---

## Public vs private (decision)

| Surface | GitHub (free) | Local only | Future paid app |
|---|---|---|---|
| `pdf_tool` + themes + layouts + QA | ✅ | — | Same engine |
| Design Hub | ✅ | — | Shell launches Hub |
| `examples/resume-studio/` + protocol `*.example.md` | ✅ | — | Guided wizard UX |
| Protocol docs (VAULT shape, JOB-ASSESSMENT) | ✅ generic | Real vaults / listings | Guided wizard UX |
| Bare start/wrap/make-*/commands README | ❌ | ✅ SEGO ritual + `/reflect` | N/A |
| `mcp-pdf-designer.json` | ❌ `.example` only | ✅ | N/A |
| Brand maps · collages · exports · applicants | ❌ | ✅ `storage/` | User’s own local data |
| Marketing strategy with personal brands | High-level in [`docs/PRODUCT.md`](../../docs/PRODUCT.md) | Detail in `storage/docs/MARKETING.md` | Paid features list |

SSOT for free-vs-paid: [`docs/PRODUCT.md`](../../docs/PRODUCT.md).  
Architecture: [`docs/PUBLIC-LOCAL-SPLIT.md`](../../docs/PUBLIC-LOCAL-SPLIT.md).  
Clone how-to: [`docs/GETTING-STARTED.md`](../../docs/GETTING-STARTED.md) · [`examples/resume-studio/`](../../examples/resume-studio/).  
Private notes: [`storage/docs/`](../../storage/docs/) (bodies gitignored; `README.md` placeholder tracked).

---

## Marketing (summary — detail private)

1. **Free GitHub** — résumé creator for a broken market: vaults + skills + palettes; smoke + Hub.
2. **Audience** — agents + power users who refuse invented claims; paid shell later for seekers.
3. **Paid later** — installer + vault/export wizard; sell *time saved*, not vaults.
4. **Do not** market personal career data, founder names, or private brand maps as the product.

Full narrative: `storage/docs/MARKETING.md` (local).

---

## Auto-goal run — public Resume Studio proof + local packaging proof

**Objective:** finish every reversible local part of the remaining public-product work while the
human-gated push, history rewrite, and package uploads remain deferred.

### Done when

- [x] A stranger can open `examples/resume-studio/` and follow a concrete vault → profile → palette →
      HTML → light/dark/ATS walkthrough using tracked examples only.
- [x] The Resume Studio front door exposes a direct Design Hub link for the tracked example and does
      not imply private `storage/` data ships with the product.
- [x] `python scripts/testpypi-dry-run.py` proves a fresh local-wheel install from outside the checkout,
      including bundled assets and `check_generation`.
- [x] Public privacy scans, `python scripts/smoke-white-label.py`, `pytest`, and wheel-asset checks pass.
- [x] Push, history scrub, TestPyPI upload, and production PyPI remain visibly UNVERIFIED/deferred unless
      the required identity, token, and explicit human authorization exist.

### Task checklist

- [x] Audit recent packaging/product dev-log entries and current Resume Studio gaps.
- [x] Build the public walkthrough/deep-link surface without private names, paths, or claims.
- [x] Run the fresh-venv local wheel proof and repair only in-scope defects it exposes.
- [x] Run adversarial public/private and artifact verification.
- [x] Update plan/docs/memory if a durable rule changes; wrap, commit explicit tracked paths, and report.

### Assumptions

- The optional Resume Studio walkthrough is the highest-value authorized branch: the three higher
  priority items require credentials or irreversible/outward-facing consent.
- “Deepen” means a useful tracked walkthrough over the existing engine and example fixtures, not a new
  renderer, paid shell, or cloud workflow. A request for interactive wizard chrome would change this.
- Local wheel construction and isolated installation are reversible verification; publishing to either
  TestPyPI or PyPI is an outward-facing hard stop.

### Evidence

- VERIFIED — `python scripts/testpypi-dry-run.py` installed the 59-entry wheel into a fresh temporary
  venv, ran from `outside-cwd`, resolved `repo_root()` to `site-packages/pdf_tool/share`, and passed
  `pdf-designer-check-generation` on the bundled example HTML.
- VERIFIED — independent wheel listing contains zero `storage/`, `.codex/`, `.claude/commands/`,
  `_exports/`, `_variants/`, PDF, or image entries.
- VERIFIED — recent dev-log audit (s018–s021) found no conflict with this run; its only higher-priority
  remainder is externally gated.
- VERIFIED — `examples/resume-studio/README.md` now provides the seven-step tracked walkthrough; all
  nine referenced paths exist and the direct Hub example URL returns HTTP 200.
- VERIFIED — the adversarial pass found absolute `C:\\Github\\voice-seed` paths that the first marker
  scan missed; the fixtures now use `<VOICE_SEED>` and the smoke rejects real absolute Windows paths.
- VERIFIED — final `python scripts/smoke-white-label.py` passed the scoped privacy gate, generation
  11/11, two-page light/dark exports, and ATS with all required cues and zero mid-word splits.
- VERIFIED — `pytest -q` passed 43 tests; `python scripts/check-wheel-assets.py` passed with 59 files.

### Deferred

- Push `origin/main`: requires switching from MonoFinity to the approved `jenninexus` identity.
- History scrub/force-push: requires explicit human approval after reviewing `storage/docs/HISTORY-SCRUB.md`.
- TestPyPI/production PyPI upload: requires token plus outward-facing publish consent.
- Setuptools `project.license` table deprecation (deadline shown as 2027-02-18): non-blocking packaging
  maintenance; changing build metadata/version floors is outside this walkthrough proof.
- A repo-wide tracked-surface privacy inventory remains broader than this Resume Studio/public-seed
  gate; brand-named public palettes and layouts may be intentional API/content and need a separate,
  compatibility-aware decision before renaming or removing them.
