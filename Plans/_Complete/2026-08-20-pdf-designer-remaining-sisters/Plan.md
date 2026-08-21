# Complete / superseded plan — PDF Designer remaining sisters

> **Superseded 2026-08-21.** The remaining release record and standalone-app work are consolidated in
> [`../../_Active/2026-08-21-standalone-app-remaining.md`](../../_Active/2026-08-21-standalone-app-remaining.md).
> This was a posting-day snapshot; do not revive completed Discord or Patreon actions from it.

**Date:** 2026-08-20 · **Host:** SEGOPC · **Mode:** `/auto-goal`

## Done when

- [x] Live Patreon URL stamped on published markdown + `npm run patreon:archive:jn` refreshed
- [x] `#announcements📢` Discord teaser SENT (not social-feed / patrons / supporters — those already fanned from Patreon)
- [x] `@JenniNexus` X composer completion recorded at the human’s direction 2026-08-21; live URL capture and `x:notify:jn` remain in the active plan
- [ ] MostlyJenniNexus Facebook Page posted with landscape promo card
- [ ] Instagram `@jenninexus` posted if Graph credentials validate; otherwise noted UNVERIFIED
- [x] Promo cards on public HTTPS (jenninexus.com/resources/images/blog/pdf-designer/)
- [x] TikTok / YouTube / Gumroad **not** posted (Hub examples / installer gates)

## Task checklist

- [x] Copy promo cards to JN blog image dir with clean filenames; SCP to jennidrop
- [x] Confirm HTTP 200 on landscape + portrait URLs
- [x] Stamp Patreon live URL via archive
- [x] Post Discord announcements (explicit OK 2026-08-20)
- [x] Attempt X (403) and Facebook (token expired 2026-06-07) — parked for composer
- [x] Update timelines / drafts records
- [x] Wrap

## Assumptions

- User confirmation that Patreon + Patreon-webhook Discord fan-out already succeeded is taken as fact; do not re-`--post` those three channels.
- Remaining "other /jen/socials posts" = announcements teaser + X + Meta. Short-form stays parked.
- Landscape `1200x675` promo card is the primary attach; portrait `675x1200` is uploaded for Stories later, not required on feed.
- Socials checkout is on sibling branch `codex/social-notifier-release` — do **not** land adapter edits there. Use public HTTPS URLs so Facebook/Instagram adapters work as-is.
- X timeline read may still 403; tweet *write* is still worth trying. If write fails, park X as UNVERIFIED with the exact API error. **Confirmed:** `v2.me` 403, so write never starts.

## Evidence

- VERIFIED — Discord announcements SENT 2026-08-20T12:33:42Z (`discord/published/2026-08-17-announcements-pdf-designer.json`). Channel https://discord.com/channels/280177126978748416/284873216252706816
- VERIFIED — Patreon live https://www.patreon.com/posts/pdf-designer-com-167093475 (API list + archive, 616 posts)
- VERIFIED — HTTPS 200 landscape 203129 bytes, portrait 167644 bytes
- VERIFIED — X fail: `Request failed with code 403` on `verifyXIdentity` / `v2.me`
- VERIFIED — Facebook fail: Page token expired 2026-06-07 07:00 PDT
- UNVERIFIED — Instagram (same expired Page token; not retried)

## Deferred

- TikTok / YouTube until Design Hub is `examples` mode
- Gumroad until installer/wizard
- Deploy of remaining JN blog PHP copy ("GitHub private" sentence) if still stale — not required to post sisters
- Graph Explorer refresh of `FB_PAGE_ACCESS_TOKEN` (human OAuth)
- JenniTweets pay-per-use repair (`npm run x:ready:jn`)
