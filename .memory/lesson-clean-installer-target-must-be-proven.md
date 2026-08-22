---
name: lesson-clean-installer-target-must-be-proven
description: Network reachability or an absent checkout does not make a Windows machine a clean installer target; preflight every runtime and workspace condition.
metadata:
  type: project
  date: 2026-08-21
---

Never run a customer-installer validation on a nearby development or media PC
because it is reachable or lacks this repository. A clean target must be
observed to have no checkout, Python, Node/npm, existing PDF Designer install,
or `Documents\\PDF Designer` workspace before the run.

**Why:** BEETHOVEN had no `pdf-designer` checkout and could be reached over the
network, but it already had Python and Node tooling. LIVPHI was reachable but
could not be authenticated for a trustworthy preflight. Either machine would
have produced a false clean-machine claim or disturbed a shared host.

**How to apply:** use `scripts/verify-clean-machine.ps1` only on a newly
provisioned Windows 10/11 x64 VM or physical target. It fails before install on
contamination and verifies the public Jane seed, fictional test vault,
light/dark exports, graceful runtime cleanup, and workspace preservation.
Document the same-user loopback and Documents-redirection boundaries before
calling the product local-only.

Related: [[lesson-electron-packaged-playwright-needs-explicit-browser-path]]
