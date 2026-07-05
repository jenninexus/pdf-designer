# Licensing Notes

**Status: not finalized.** `LICENSE` in the repo root is currently MIT as a placeholder — reconsider it before the first public push if a paid tier is actually planned, not just "maybe someday."

## Why this needs a real decision, not a default

MIT/Apache-2.0 are simple and contributor-friendly, but they let anyone — including a well-funded competitor — take the code, host it, and sell it back to your own future customers without owing you anything. That's a fine trade for a pure utility library; it's a worse trade if the plan is "open core now, paid product later," because by the time there's something worth competing over, the permissive license already gave away the ability to stop that.

Because this project has a single author/copyright holder (you), you retain the option to **dual-license** — offer the community one license and separately sell a different license/product to companies who don't want the community terms. That option only stays open if contributors don't dilute copyright ownership without a CLA; worth keeping in mind once/if this takes outside contributions.

## Options actually on the table

1. **Open core (recommended starting point).** Keep this repo (the `pdf_tool` engine + example profiles/themes) permissively licensed — MIT or Apache-2.0. Apache-2.0 adds an explicit patent grant/termination clause, which is marginally more defensive for a dev tool; otherwise the two are functionally similar for this project's purposes. Build anything paid (hosted match-scoring service, cloud sync, premium profile/theme packs, team/organization features, ATS browser-extension-at-scale) as a **separate private repo** that depends on this one. Simplest to execute, no license engineering, keeps the door open.
2. **Source-available with a commercial carve-out (BSL / Functional Source License).** Code is public and inspectable, free for personal/non-production use, but running it as a competing commercial service requires a separate commercial license; it auto-converts to Apache/MIT after a change date (commonly 2–4 years). Used by Sentry, CockroachDB (pre-relicense), HashiCorp (pre-relicense). More legal overhead than option 1, and reduces casual open-source adoption/contributions since it's not OSI-approved "open source" in the strict sense — matters if community goodwill/contributions are a goal.
3. **AGPL-3.0 + commercial dual license.** AGPL forces anyone who runs a modified/hosted version to release their source, which deters silent SaaS forks. As sole copyright holder, you could still sell companies a separate commercial license that waives the AGPL obligations (the classic MySQL/Qt model). More friction for adopters who don't want AGPL obligations (some companies ban AGPL dependencies outright), and requires you to actually enforce/administer the dual license.

## Recommendation (non-binding — a real business call)

Start with **option 1 (open core, MIT or Apache-2.0 for this repo)** unless there's a specific, concrete near-term paid feature already planned — in which case work out that feature's home (separate private repo) *before* the first public push, not after. Revisit options 2–3 only if cloning-and-reselling by a direct competitor becomes an actual observed problem, not a hypothetical one — they cost real adoption friction to guard against a risk that may never materialize.

## Also relevant: internal-only theme sourcing

The default theme (`themes/default-theme.json` / `default-professional.css`) was adapted from a private internal design-system pattern that is **not public** and not a dependency of this project. Keep any exact sourcing trail in gitignored local notes only. Nothing in this repo should link to or assume access to private design-system repositories; if that source becomes public later, this note is the place to revisit turning "adapted from" into a real reference/dependency.
