# PDF Designer — 2026-09-29 spoken-voice profiles

**Started:** 2026-09-29 · **Status:** open — designed profiles written; install + audition remain.
**Durable backlog:** [`docs/ROADMAP.md`](../../docs/ROADMAP.md)

Public-safe checklist. The profiles themselves live in gitignored `profiles/voices/` (local only; its
`README.md` has the load steps). Rules and public briefs: voice-seed `docs/SPOKEN-VOICE.md`.

## Done

- [x] Designed-voice profiles for the three voice-seed ids `jenni`, `shade`, `martiangames` in
  `profiles/voices/<id>.voicestudio.json`: the exact VoiceStudio save request (`POST /profiles`, multipart,
  `kind=design`, `vd_states`, `instruct`, `seed`, `ref_text`), per-call pace (`speed`), delivery do/don't,
  and sample lines written in each voice's register.
- [x] Tags verified against VoiceStudio's own validators (`sanitize_instruct`, `instruct_to_vd_states`,
  `parse_description`): all round-trip.
- [x] `profiles/voices/import-voicestudio.ps1` (design only, refuses clone, skips existing names;
  `-DryRun` verified) and a local clone-consent ledger (empty: no consent given).
- [x] voice-seed cards carry a public `Spoken voice (brief)` + `Tool profile:` label; SPOKEN-VOICE.md
  now says design mode only hears tags.
- [x] Privacy audit: tracked-but-ignored `.memory/MEMORY.md` and `_Complete/2026-09-29-pdf-work.md`
  allowlisted; two personal handoff plans untracked (local copies kept).

## Remaining

- [ ] Install VoiceStudio on the machine Syqo designates for VRAM-heavy work
  (`GET /api/cc/machines?job=heavy`), as a separate AGPL app; do not vendor its code.
- [ ] Import the three profiles (`import-voicestudio.ps1`), audition every sample line at the profile's
  `speed`; if the speaker is wrong change `seed`, re-import, and record the winning seed.
- [ ] Owner review of the flagged taste calls in each profile's `consent.ownerReviewNeeded`
  (accent assumption; Shade's gender tag vs. she/her/they; brand voice gender).
- [ ] Only if Jenni or Shade explicitly consents: record consent in the local ledger first, then clone
  from recordings they supply. Never clone a founder's voice for the studio brand.
- [ ] Bind voices to agents by **name** through VoiceStudio's MCP (`/mcp`); nothing voice-related in git.
- [ ] Owner decision: other tracked historical plans still name specific job applications
  (e.g. `_Complete/2026-07-14-professional-product-roadmap.md`) and so do `AGENTS.md` and some docs —
  untrack/redact or keep. History is already public; a scrub is a separate, explicit decision.
