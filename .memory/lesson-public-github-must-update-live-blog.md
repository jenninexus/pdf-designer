---
name: lesson-public-github-must-update-live-blog
description: When the GitHub repo flips public, the live blog clone sentence is a publication gate — a still-private paragraph on a live post is a lie
metadata:
  type: feedback
  date: 2026-08-20
---

**When GitHub goes public, retarget the live blog in the same session.** Do not leave
“the repo is still private / clone URL goes here later” on a page that already
returns HTTP 200.

**Why:** The 2026-08-19 flip made `github.com/jenninexus/pdf-designer` public. The
landing post at `/blog/pdf-designer` (and vanity `/pdf-designer`) kept the private
placeholder until 2026-08-20. Socials sisters and the Patreon paste already said
clone-it; the live HTML did not. Search and Discord unfurls read the site, not
the local markdown copy.

**How to apply:** After a public switch, grep the live PHP (and the Socials
`devlogs/published/` sister) for `private`, `flip the switch`, and `clone URL goes
here`. Put the real clone URL in the body, then deploy that page. Local markdown
alone is not the public page.

Related: [[lesson-ssot-dashboard-must-name-live-paths]]
