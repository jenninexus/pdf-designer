# Licensing

**Settled 2026-07-13: MIT + open core.** © Jenni Nexus, sole copyright holder.
`LICENSE` is MIT, the README says MIT, **every dependency is permissive**, and the paid-vs-open
question is **decided** (below) rather than left hanging.

| | |
|---|---|
| [The AGPL problem](#the-problem-we-had-an-agpl-dependency) | What was actually broken, and why it mattered |
| [How it was fixed](#how-it-was-fixed) | PyMuPDF removed; nothing lost |
| [The dependency audit](#the-dependency-audit) | Every dep, every license |
| **[The decision: MIT + open core](#the-decision-mit--open-core)** | **Why, and the one rule that keeps your options open** |
| [Theme provenance](#theme-provenance) | The one other thing to keep clean |

---

## The problem: we had an AGPL dependency

Until 2026-07-13, `pyproject.toml` declared **PyMuPDF** as a hard, unconditional dependency.

**PyMuPDF is AGPL-3.0** (or a paid Artifex commercial license). The AGPL is the strongest
copyleft in common use: distribute a work that combines with it, and the **entire combined work**
must be offered under the AGPL — source included — to anyone who receives it *or merely uses it
over a network*.

So the repo was offering people **MIT rights it did not have the power to grant.**

**Was that illegal?** Not yet — and this is worth being precise about, because the honest answer
is narrower than the scary one:

- The repo was **private** and had **never been distributed**. The AGPL's obligations trigger on
  *distribution* (and on network use of a modified version). Neither had happened.
- Using AGPL software privately, for yourself, obligates you to nothing. That is explicitly fine.
- **The moment it went public or shipped to anyone, it would have been a real license violation** —
  simultaneously breaching the AGPL (by not offering the combined work under AGPL) and
  misrepresenting the license to every downstream user who relied on the MIT grant.

It was a **loaded gun, not a fired one.** The fix had to land before the first public push, and it
did.

## How it was fixed

**PyMuPDF was removed.** It was used in exactly one place — `pdf_to_png.py`, to rasterize PDF
pages into PNG previews.

The replacement isn't a compromise; it's better:

**`pdf_to_png` now screenshots the HTML source directly.** Every document in this repo wraps each
printed page in a `.page` element (the pagination contract — see [`EXPORTS.md`](EXPORTS.md)). So
we screenshot **each `.page` element** in the *same* headless Chromium, in the *same* print media
mode, that `html_to_pdf` prints from.

| | PyMuPDF (before) | Playwright (now) |
|---|---|---|
| **License** | ❌ AGPL-3.0 | ✅ Apache-2.0 |
| **New dependency** | yes, a whole PDF engine | **none** — Chromium was already shipping |
| **Fidelity** | rasterizes the PDF | screenshots the *same DOM the PDF renders* |
| **Round-trip** | HTML → PDF → PNG | HTML → PNG |

Page counting and ATS text extraction — the other things `fitz` was used for in the docs — moved
to **`pypdf`** (BSD-3-Clause), which does both.

**Nothing was lost.** Verified: 2-page résumés render as 2 PNGs, 1-page cover letters as 1, in
both light and dark.

## The dependency audit

Every runtime dependency, with its real license (read from the installed package metadata, not
from memory):

| Dependency | License | MIT-compatible? |
|---|---|---|
| **playwright** | Apache-2.0 | ✅ Permissive. Patent grant included. |
| **pypdf** | BSD-3-Clause | ✅ Permissive. |
| **Pillow** | MIT-CMU | ✅ Permissive. |
| ~~pymupdf~~ | ~~AGPL-3.0~~ | ❌ **REMOVED 2026-07-13.** |

**Nothing here is copyleft.** MIT is now an honest, unqualified claim: this is safe to
open-source, safe to build a commercial product on, and safe to distribute without triggering
anyone's source-disclosure obligations.

> **Keep it that way.** Before adding *any* dependency, check its license. AGPL and GPL are the
> ones that will silently poison an MIT project — and `pip install` will not warn you. A one-line
> check:
> ```bash
> python -c "import importlib.metadata as m; d=m.metadata('PKG'); print(d.get('License-Expression') or d.get('License'))"
> ```

## The decision: MIT + open core

**Decided 2026-07-13. This repo stays MIT. Anything paid lives in a separate private repo.**

This section used to be a three-option menu with a hedge at the bottom. A menu isn't a decision,
and an undecided license is a decision to be surprised later. So — decided.

### Why MIT and not something more defensive

The instinct to protect the code is real, and the fear is legitimate: a permissive license lets a
well-funded competitor take this, host it, and sell it back to your own future customers owing you
nothing. BSL and AGPL exist precisely to stop that.

**But they guard against the wrong risk for this project.**

- **The moat isn't the code — it's the vault.** The engine is ~1,400 lines of Playwright glue.
  Anyone competent could rewrite it in a weekend; it is not what makes this valuable. What makes it
  valuable is the *system* around it — the claim vault, the role-track angles, the guards, the
  accumulated judgment about what actually wins a job. **That's data and doctrine, and it is
  already private.** Licensing the engine defensively protects the part nobody wants to steal.
- **Nobody clones an unknown repo.** BSL and AGPL solve a problem you get *after* traction. Right
  now the scarce resource is people finding this useful at all — and both licenses actively cost
  you that. Many companies **ban AGPL dependencies outright**; BSL isn't OSI-approved, so it reads
  as "not really open source" and suppresses casual adoption and contribution.
- **You're paying legal overhead today to insure a hypothetical.** Administering a dual license is
  real, ongoing work. Do it when there's something to defend, not before.
- **MIT is reversible in the direction that matters.** You are the **sole copyright holder** (the
  `LICENSE` names you, deliberately). That means you can *always* relicense future versions,
  dual-license, or sell a commercial license later. What you can't do is retroactively claw back
  the version you already published — so the only real cost of MIT is that any single released
  version stays MIT forever. That is a cheap price for adoption.

### What "open core" means in practice

| Layer | Where it lives | License |
|---|---|---|
| **The engine** — `pdf_tool`, themes, examples, the docs | this repo | **MIT**, public |
| **The vault + your real applications** | `storage/` | **gitignored, never published** |
| **Anything paid later** — hosted service, cloud sync, team features, premium theme packs | **a separate private repo** that depends on this one | your choice, decided then |

The split already exists — `storage/` is gitignored and the guards keep real data out of tracked
paths. **Open core isn't a future migration; it's the shape the repo is already in.**

### The one rule that keeps the option open

**Don't take outside contributions without a CLA.** The moment a contributor's copyright lands in
the tree without an assignment or license agreement, you lose the unilateral right to relicense or
dual-license — that option depends on *sole* ownership. If someone offers a PR and this ever
matters to you, get a CLA signed first, or rewrite the contribution yourself.

### When to revisit

Revisit **only on evidence**, not on anxiety:

- Someone is actually running a competing hosted version of this. *(Then: AGPL + commercial dual
  license, for future versions.)*
- You are actually about to ship a paid product. *(Then: decide where it lives — a separate private
  repo — **before** the first public push of this one, not after.)*

Until one of those is true, this section is closed.

## Theme provenance

The default theme (`themes/default-resume.json` / `.css`) was adapted from a private internal
design-system pattern that is **not public** and **not a dependency**. Keep any exact sourcing
trail in gitignored local notes only.

**Nothing tracked in this repo may link to, or assume access to, a private repository.** *(Two
brand-palette files briefly violated this by citing a private sibling repo as their
provenance; they were made self-contained on 2026-07-13.)*
