---
name: lesson-kit-contract-lands-on-trunk
description: Compact-offcanvas / nav_switch kit docs must land on main, not a sibling WIP branch
metadata:
  type: feedback
  date: 2026-08-26
---

When pdf-designer (or Jen DJ) changes a **shared kit contract** (`docs/BREAKPOINTS.md`, `docs/PROTOCOL.md`, `profiles/pdf-designer.json`, `scss/_offcanvas-nav.scss`), commit those paths on the kit’s **`main`**. Do not leave them only on a sibling WIP branch (`codex/social-notifier-release` and friends).

**Why:** A clone or `git pull origin/main` never sees commits that live only on a socials/notifier branch. The next Hub/Jen DJ session then re-derives `until-xxl` from screenshots. `mcp-breakpoints.json` is a gitignored registry — it cannot carry the contract.

**How to apply:** Use a **worktree on `main`** (`git worktree add <temp> main`) so dirty sibling files stay put. Checkout explicit paths from the WIP tip, restore any unrelated deletions, commit, push **`origin/main`**, remove the worktree. Never `git push` the sibling branch for this. Do not invent a 1024px breakpoint.

[[see-also: lesson-hub-nav-switch-through-ipad-pro]] [[see-also: lesson-hub-native-select-ignores-device-frame]]
