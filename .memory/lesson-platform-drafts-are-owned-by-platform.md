---
name: lesson-platform-drafts-are-owned-by-platform
description: Release sisters belong in each Socials platform's sibling drafts/published folders; never bury published output in a devlog topic directory.
metadata:
  type: feedback
  date: 2026-08-13
---

For PDF Designer release work, the JenniNexus blog draft lives in
`socials/content/jenninexus/devlogs/drafts/` and the Patreon sister lives in
`socials/content/jenninexus/patreon/drafts/`. Use the same dated slug for the two files.
After a platform is actually live, move only that platform's file to its sibling `published/` folder.

**Why:** the old JN README described a devlog topic directory that also held generated platform
outputs. That made draft status and the eventual archive location ambiguous, and left stale
blog/Patreon pointers on the product card.

**How to apply:** start with `content/jenninexus/README.md` and
`content/jenninexus/format-manifest.json#pipeline`; use the dated paths on
`product-design/docs/PDF-DESIGNER.md`; dry-run `npx tsx scripts/site-publish.ts --brand jn --draft <file>`
before any human publication review. A dry run is not authority to run `--write`, build, SSH, deploy, or post.

Related: [[lesson-twin-files-always-fork]]
