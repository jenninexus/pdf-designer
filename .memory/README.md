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
| [lesson-work-samples-footer-row-false-collision.md](lesson-work-samples-footer-row-false-collision.md) | Work-samples L/R footer (name·links) false-triggers footer-collision — pin bottom-RIGHT; portfolio URLs in a body panel |
| [lesson-defaults-export-beside-html.md](lesson-defaults-export-beside-html.md) | Go-to pack PDFs export into `defaults/` next to the HTML — never `_exports/defaults/` |
| [lesson-utf8-json-roundtrip-on-windows.md](lesson-utf8-json-roundtrip-on-windows.md) | PowerShell/cp1252 round-trips corrupt UTF-8 JSON with ⭐ — surgical Edit + `encoding=utf-8` only |
| [lesson-ats-section-cues-must-be-contiguous.md](lesson-ats-section-cues-must-be-contiguous.md) | Jobright misses Job Title / Work Experience / Education when cues are creative, buried, or split in the text layer (Montserrat `W ORK`) — `check_ats` + system-font h2 |
| [lesson-jobright-content-score-is-not-parse-fail.md](lesson-jobright-content-score-is-not-parse-fail.md) | Jobright rank D / skills-count ≠ ATS parse fail — upload light; print body on system font; mid-word splits are the real shredder |
| [lesson-hub-drawer-css-without-html-clips-more.md](lesson-hub-drawer-css-without-html-clips-more.md) | Hub drawer CSS without HTML/JS + `overflow:hidden` clipped the ⋯ panel; recipe_gallery must scan layout category folders |
| [lesson-hub-stack-at-md-breaks-desktop-split.md](lesson-hub-stack-at-md-breaks-desktop-split.md) | Do not stack library/viewer at md (991.98) — desktop/zoomed windows look broken; keep LEFT/RIGHT until phones (≤575.98); folder pins = ghost ★ in picker |
| [lesson-hub-collage-hidden-by-profile-filter.md](lesson-hub-collage-hidden-by-profile-filter.md) | Untagged collage projects vanish when Profiles ≠ all — clear profile chip or search folder; keep `_candidates/` flat |
| [lesson-public-clone-path-stays-tracked.md](lesson-public-clone-path-stays-tracked.md) | Public clone how-to stays tracked; audit seed content and absolute paths; scope privacy claims honestly; gitignore ≠ history scrub |
| [lesson-scaffold-readme-must-not-win-path-resolution.md](lesson-scaffold-readme-must-not-win-path-resolution.md) | README-only root nouns (`users/` · `applications/` · …) must not win over live `storage/` during dual-run — resolve payload, not directory existence |
| [lesson-hub-options-must-follow-workspace.md](lesson-hub-options-must-follow-workspace.md) | Design Hub profile and palette controls follow the workspace root, never a hard-coded local roster |
| [lesson-hub-profile-scopes-folder-and-kind.md](lesson-hub-profile-scopes-folder-and-kind.md) | Restore profile before folders; scope folder/kind to the selected profile or the library goes empty |

## Related

- [`docs/VAULT.md`](../docs/VAULT.md) — claim rules (the "silent failure" section)
- [`docs/QA.md`](../docs/QA.md) — the ship gate
- [`docs/LAYOUT-SYSTEM.md`](../docs/LAYOUT-SYSTEM.md) — pagination + content-fit
- [`.claude/commands/wrap.md`](../.claude/commands/wrap.md) — the wrap that feeds this
