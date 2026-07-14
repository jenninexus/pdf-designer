# Licensing

**Status: MIT, and now honestly so.** `LICENSE` is MIT, the README says MIT, and — as of
2026-07-13 — **every dependency is permissive**, so that claim is finally true without a caveat.

| | |
|---|---|
| [The AGPL problem](#the-problem-we-had-an-agpl-dependency) | What was actually broken, and why it mattered |
| [How it was fixed](#how-it-was-fixed) | PyMuPDF removed; nothing lost |
| [The dependency audit](#the-dependency-audit) | Every dep, every license |
| [Is MIT the right license?](#is-mit-the-right-license-still-a-business-call) | Still an open business question |
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

## Is MIT the right license? (still a business call)

Resolved above: MIT is now *coherent*. Whether it's *optimal* is a separate question, and it is
still open — the repo is private, so nothing is locked in.

MIT and Apache-2.0 are simple and contributor-friendly, but they let anyone — including a
well-funded competitor — take the code, host it, and sell it back to your own future customers
owing you nothing. That's a fine trade for a utility library. It's a worse trade for "open core
now, paid product later," because by the time there's something worth competing over, the
permissive license already gave away the ability to stop it.

**You are the sole copyright holder**, which preserves the **dual-licensing** option: offer the
community one license, and separately sell a commercial license to companies that don't want the
community terms. That option survives only if contributors don't dilute copyright ownership
without a CLA — worth remembering if this ever takes outside contributions.

### The options

1. **Open core (the current path, and a reasonable default).** Keep this repo permissive — MIT, or
   Apache-2.0 if you want an explicit patent grant. Build anything paid as a **separate private
   repo** that depends on this one. Simplest to execute; keeps every door open.
2. **Source-available with a commercial carve-out** (BSL / Functional Source License). Public and
   inspectable, free for personal and non-production use, but running it as a competing commercial
   service requires a commercial license; auto-converts to Apache/MIT after 2–4 years. More legal
   overhead, and it isn't OSI-approved "open source," which costs casual adoption.
3. **AGPL-3.0 + commercial dual license.** Deters silent SaaS forks; you'd still sell companies a
   commercial license waiving the AGPL terms (the MySQL/Qt model). But many companies **ban AGPL
   dependencies outright**, and you'd have to administer the dual license.

**Recommendation (non-binding — this is a business decision, not a technical one):** stay with
**option 1** unless a concrete paid feature is already planned, in which case decide *where it
lives* (a separate private repo) **before** the first public push. Revisit 2–3 only if
clone-and-resell becomes an observed problem rather than a hypothetical one — they cost real
adoption friction to guard against a risk that may never arrive.

## Theme provenance

The default theme (`themes/default-resume.json` / `.css`) was adapted from a private internal
design-system pattern that is **not public** and **not a dependency**. Keep any exact sourcing
trail in gitignored local notes only.

**Nothing tracked in this repo may link to, or assume access to, a private repository.** *(Two
`themes/brand-*.json` files briefly violated this by citing a private sibling repo as their
provenance; they were made self-contained on 2026-07-13.)*
