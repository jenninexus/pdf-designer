---
name: lesson-socials-api-preflight-before-posting-day
description: Before auto-posting X or Meta sisters, run x:ready:jn and fb-auth — Discord webhooks being live does not mean Graph or JenniTweets tokens are
metadata:
  type: feedback
  date: 2026-08-20
---

**Preflight Socials API tokens on posting day before promising X or Meta will go out from the CLI.** A live Discord webhook and a live Patreon receiver do not imply `X_*` or `FB_PAGE_ACCESS_TOKEN` still work.

**Why:** 2026-08-20 Patreon + `#announcements📢` posted. The same session then hit JenniTweets `v2.me` HTTP 403 and a MostlyJenniNexus Page token that expired 2026-06-07. Both failures are documented in Socials (`TWITTER-X.md`, `FACEBOOK-INSTAGRAM.md`) but a posting-day wrap still treated “configured” as “callable.”

**How to apply:** From `C:\Github\socials`, before `--post` on X/Meta:

```powershell
npm run x:ready:jn
npx tsx scripts/auth/fb-auth.ts
```

If either fails, switch to composer paste (landscape promo card at `docs/images/promo-card-landscape.png` / the HTTPS copy on jenninexus.com) and do not spend the session retrying the dead API. After a manual X URL exists, `npm run x:notify:jn`. Refresh Graph tokens via Graph Explorer (`pages_manage_posts`) — do not invent OAuth in-session.

Related: [[lesson-platform-drafts-are-owned-by-platform]] · [[lesson-public-github-must-update-live-blog]]
