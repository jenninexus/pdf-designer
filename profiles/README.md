# `profiles/` — how it prints

Render profiles: `profiles/<id>.json` (layout, export prefs, which HTML to open).

| Tracked | Gitignored |
|---|---|
| this README · [`examples.json`](examples.json) · `*.example.json` | real `<you>-resume.json` |

**Two files, two jobs:**

1. **[`examples.json`](examples.json)** — live Hub profile (`examples`). A clone sees Jane Example in the dropdown even after you add your own card. Do not rename this to hide it.
2. **[`you-resume.example.json`](you-resume.example.json)** — copy-me seed. Copy → `profiles/you-resume.json` (or `profiles/<you>-resume.json`) and fill it in. That copy is gitignored.

Same shape also lives in [`examples/profiles/default-resume/profile.example.json`](../examples/profiles/default-resume/profile.example.json).

Person + vault companions: [`users/examples.json`](../users/examples.json) · [`vaults/examples.json`](../vaults/examples.json).
