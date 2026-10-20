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

Voice is edited in exactly two places, never in a profile: `users/<you>.json#characterVoice`
holds personality and cross-register routing; `vaults/<you>.json#voice` holds application prose.
The profile's `voice` field is a pointer only, so it cannot become a conflicting third source.

**Spoken voice is a different job, and it does not live here.** The VoiceStudio profiles, the
clone-consent ledger and the engine renders are in the voice map's private overlay:
`voice-seed/private/voices/` (gitignored, 2026-10-20). They describe how a voice *sounds*, never how
prose reads, and they do contain recordings. Rules and public briefs: voice-seed
`docs/SPOKEN-VOICE.md`; the lab's own README is `voice-seed/private/voices/README.md`.

This repo keeps **written** voice only: `users/<you>.json#characterVoice` holds personality and
cross-register routing, `vaults/<you>.json#voice` holds application prose.
