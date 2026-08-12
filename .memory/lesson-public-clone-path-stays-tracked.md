---
name: lesson-public-clone-path-stays-tracked
description: Do not bury the public clone how-to in storage/; gitignore ≠ history scrub
metadata:
  type: feedback
  date: 2026-08-12
---

**Do not move the stranger clone checklist into gitignored `storage/docs/`.** Keep it tracked
as [`docs/GETTING-STARTED.md`](../docs/GETTING-STARTED.md). Architecture lives in
[`docs/PUBLIC-LOCAL-SPLIT.md`](../docs/PUBLIC-LOCAL-SPLIT.md). And **gitignore is not a history
scrub** — bare commands / machine MCP config once committed stay in old SHAs until
`git filter-repo` + human-authorized force-push (`storage/docs/HISTORY-SCRUB.md`).

**Why:** “Dev-only” and “clone-safe public how-to” got conflated because the old filename
(`WHITE-LABEL`) sounded internal. Working-tree ignores hide current files from `git status`
but leave them in history for anyone who clones an old commit.

**How to apply:** When privatizing docs, ask “does a stranger need this to prove the free
product?” If yes → `docs/`. If it names SEGO paths, brands, or scrub commands → `storage/docs/`.
Before a wide public launch, run the HISTORY-SCRUB checklist; never force-push without
jenninexus auth + explicit OK.

Related: [[lesson-twin-files-always-fork]]
