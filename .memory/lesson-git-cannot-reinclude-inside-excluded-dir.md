---
name: lesson-git-cannot-reinclude-inside-excluded-dir
description: Git silently ignores `!path` when a parent directory is excluded — a tracked scaffold needs `dir/*`, not `dir/`
metadata:
  type: feedback
  date: 2026-10-16
---

To track one file inside an otherwise-ignored folder, exclude the folder's **contents** and negate the
file — never exclude the folder itself:

```gitignore
Plans/*
!Plans/README.md
```

`Plans/` + `!Plans/README.md` does **not** work, and it fails **silently**.

**Why:** git does not descend into an excluded directory, so a negation naming a file inside it is
never even considered. The rule is documented ("it is not possible to re-include a file if a parent
directory of that file is excluded"), but the *symptom* is the trap: `.gitignore` looks correct, the
file looks listed, and nothing warns you. The only visible tell is `git check-ignore -v <path>`, which
still reports the *directory* rule.

**How to apply:** after adding any `!path` exception for a file in an ignored tree, verify with
`git check-ignore -v <path>` and read which line matched — a match on the directory line means the
negation is dead. This repo hit it while making `Plans/README.md` a tracked scaffold; the caution now
sits at the point of use in `.gitignore`, and the change was withdrawn because it also reverses the
owner rule that keeps all of `Plans/` local (see [`docs/WORKSPACE-LAYOUT.md`](../docs/WORKSPACE-LAYOUT.md)
§ Session plans).

Related: [[lesson-public-clone-path-stays-tracked]]
