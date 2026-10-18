---
name: lesson-second-git-dir-sees-public-gitignore
description: A second git dir sharing this worktree inherits the public .gitignore (hiding every private file) and its merges overwrite ignored files
metadata:
  type: feedback
  date: 2026-10-18
---

`scripts/private-sync.py` runs a second repository (`.git-private/`) over the same working tree.
Two Git behaviours bite that setup, and neither shows up in a test repo without the real `.gitignore`:

1. **The public `.gitignore` applies to the private repo too.** Every `.gitignore` in the worktree is
   read by any git dir using it, and ours ignores exactly the private roots. `git add --all` staged
   nothing and the first real run reported "nothing private to share". Fix: list candidates with
   `git ls-files --others --exclude-from=.git-private/info/exclude` (no `--exclude-standard`, so no
   `.gitignore`), then `git add -f` that list.
2. **Merges overwrite ignored files.** Git treats an ignored untracked file as expendable, and every
   private file is "ignored". A pull would have silently replaced a machine's unshared résumé with an
   incoming file of the same name. Fix: `git merge --no-overwrite-ignore`.

**Why:** the tests first built machines without the real `.gitignore`, so both traps passed. The
fixture now copies the repo's `.gitignore`, and `tests/test_private_sync.py` covers the overwrite case.

**How to apply:** any tool that drives `.git-private/` must use the private exclude file for discovery
and `--no-overwrite-ignore` for every merge or checkout that could create files.
