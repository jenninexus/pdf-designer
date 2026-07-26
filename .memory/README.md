# `.memory/` — durable learnings for this repo

**What goes here:** facts a *future agent or contributor* needs and cannot derive from the code,
the docs, or `git log`. Most importantly: **mistakes that have already been made, and why they
happened**, so they are not repeated.

This directory is **tracked in git**. It travels with every clone. That is the whole point — the
daily dev-log (`dev-log-sego.yaml`) is gitignored and local, so anything recorded only there is
invisible to the next person and to a fresh checkout.

## The split — which surface gets what

| Surface | Tracked? | Holds | Lifetime |
|---|---|---|---|
| **`.memory/*.md`** ⭐ | ✅ yes | **Durable learnings** — a trap, its root cause, and the guard that now prevents it | Permanent; survives clones |
| `dev-log-sego.yaml` | 🔒 gitignored | Per-session narrative — what happened today, `next_steps`, `difficulties` | Local, chronological |
| `docs/*.md` | ✅ yes | **Protocol** — the rule as it stands now | Permanent, rewritten in place |
| `docs/ROADMAP.md` · `Plans/_Active/` | ✅ yes | Planned work | Until done |

**The flow:** a session hits friction → `/jen:reflect` writes the `difficulties` block into
`dev-log-sego.yaml` (local, narrative) → **if the lesson is durable, it also lands here as a
`lesson-*.md` file** → if it changes a rule, the owning `docs/` page is edited too.

> **Rule of thumb:** if an agent could hit the same wall next month, it belongs here. If it only
> mattered today, the dev-log is enough.

## File format

One fact per file, `lesson-<kebab-slug>.md`, with frontmatter:

```markdown
---
name: lesson-<kebab-slug>
description: <one line — used to judge relevance during recall>
metadata:
  type: feedback | project | reference
  date: YYYY-MM-DD
---

<What to do / not do — stated as a rule.>

**Why:** <the root cause. The mechanism, not just the symptom.>

**How to apply:** <what a future agent should concretely do>

Related: [[lesson-other-slug]]
```

`type` — `feedback`: guidance on how to work here · `project`: durable context about this
codebase · `reference`: pointer to an external resource.

## Index

| Lesson | Hook |
|---|---|
| [lesson-guard-assumptions-must-be-measured.md](lesson-guard-assumptions-must-be-measured.md) | A QA guard that hard-codes a layout assumption fails silently on the other layout — measure the pixels before trusting the verdict |
| [lesson-twin-files-always-fork.md](lesson-twin-files-always-fork.md) | Two files maintained as "twins" always drift; make one the SSOT and the other a pointer |
| [lesson-track-tags-hide-true-claims.md](lesson-track-tags-hide-true-claims.md) | A true claim tagged for the wrong track goes invisible — nothing errors, the evidence just vanishes |
| [lesson-ask-before-calling-it-a-gap.md](lesson-ask-before-calling-it-a-gap.md) | `doNotClaim` means "not yet confirmed", never "cannot do" — ask before writing anything off |
| [lesson-overflow-fix-is-move-not-shrink.md](lesson-overflow-fix-is-move-not-shrink.md) | Page overflow is fixed by moving or cutting content, never by shrinking the equal margins |
| [lesson-fixed-height-clips-content-silently.md](lesson-fixed-height-clips-content-silently.md) | ⚠ A print `height` + `overflow:hidden` on a cover letter CLIPS the sign-off while every guard passes — verify the bottom of the page by eye |
| [lesson-applicant-fit-before-polish.md](lesson-applicant-fit-before-polish.md) | Decide *who* is applying against the listing's real spine before building anything |

## Related

- [`docs/VAULT.md`](../docs/VAULT.md) — claim rules (the "silent failure" section)
- [`docs/QA.md`](../docs/QA.md) — the ship gate
- [`docs/LAYOUT-SYSTEM.md`](../docs/LAYOUT-SYSTEM.md) — pagination + content-fit
- [`.claude/commands/wrap.md`](../.claude/commands/wrap.md) — the wrap that feeds this
