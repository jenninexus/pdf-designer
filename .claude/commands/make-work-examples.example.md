---
description: Build standalone work-samples / portfolio PDF pages from vault-backed claims. Public seed — copy to make-work-examples.md for personal specifics.
argument-hint: "[for] <user> [application-dir|track]"
---

# /make-work-examples — Work samples builder (public seed)

Generalized command. **No real client names.** Copy to `make-work-examples.md`
(gitignored) for your specifics.

> **Not auto-run by `/make-resume`.** Opt-in when the application needs a portfolio pack.

### Layout

**Recipe:** [`layouts/work-examples/`](../../layouts/work-examples/) (see [`layouts/README.md`](../../layouts/README.md)).
Signature: bottom-RIGHT (same family as résumés — avoid L/R footer false collisions;
see `.memory/lesson-work-samples-footer-row-false-collision.md`).

### Rules

- Source-backed only — every sample claim must exist in the vault
- Respect `storage/profiles/<user>-resume.json#exports.exportPrefs` and `workSamples`
- Dual mode (light + dark) when prefs say so
- `python -m pdf_tool.check_generation <doc>.html` before ship
- Export under `storage/<user>/_exports/<Job>/` (or profile `goToPacks.exportDir`)

### Checklist

0. Vault + profile loaded  
1. Confirm which samples the listing needs (ask on gaps)  
2. Write HTML from vault claims only  
3. Export + QA  
4. Log paths in `application.json`

Contracts: [`docs/VAULT.md`](../../docs/VAULT.md) · [`AGENTS.md`](../../AGENTS.md) ·
[`make-resume.example.md`](make-resume.example.md).
