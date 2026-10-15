# `brands/` — private palette maps

Mapped token files the Design Hub and exports actually load (`brand-<name>.json`).

| Tracked | Gitignored |
|---|---|
| this README · `*.example.json` | real brand hex maps |

Copy [`examples/brand-design/brand-example.json`](../examples/brand-design/brand-example.json) → `brands/brand-<yours>.json`.

Career documents use a portable system sans-serif stack, for example `Arial, Helvetica, sans-serif`,
for body, headings, names, contact and wordmarks in **both** light and dark exports. Keep active
brand CSS free of `@font-face` imports. Old private font assets may remain for historical or
non-document artwork; their existence is not permission to load them into a new résumé.

The relevant terms are **ATS parsing** and an **extractable PDF text layer**. A font name alone
cannot guarantee that a job site will fill every form field correctly. Export real text, run
`check_ats`, inspect reading order, and review the populated fields before submitting. See
[`docs/QA.md`](../docs/QA.md). Historical submitted PDFs are preserved, not silently regenerated.

Legacy alias: `storage/brand-design/` (retired). Palette rule: [`themes/PALETTE-RULES.md`](../themes/PALETTE-RULES.md).
