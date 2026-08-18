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

**How to use this at session start:** read **this index**. Open a lesson file only when
its hook matches the work in front of you. Protocol that is already a standing rule
lives in `docs/` (VAULT, QA, LAYOUT-SYSTEM, JOB-ASSESSMENT, PREVIEWER) — do not re-read
every lesson as if it were the SSOT.

**Do not archive this directory.** A lesson recorded only in gitignored `dev-log-sego.yaml`
is invisible to the next clone. Thin the *reading* obligation, not the files.

### Already a standing rule in docs (open the doc, not the lesson, unless you need the *why*)

| Lesson | Standing rule lives in |
|---|---|
| ask-before-calling-it-a-gap · track-tags-hide-true-claims | [`docs/VAULT.md`](../docs/VAULT.md) |
| overflow-fix-is-move-not-shrink · work-samples-footer-row-false-collision · fixed-height-clips-content-silently | [`docs/LAYOUT-SYSTEM.md`](../docs/LAYOUT-SYSTEM.md) · [`docs/QA.md`](../docs/QA.md) |
| ats-section-cues · jobright-content-score-is-not-parse-fail | [`docs/JOB-ASSESSMENT.md`](../docs/JOB-ASSESSMENT.md) § Tier 4.5 |
| twin-files-always-fork | [`AGENTS.md`](../AGENTS.md) (`.example` vs bare commands) |
| public-clone-path-stays-tracked | [`docs/GETTING-STARTED.md`](../docs/GETTING-STARTED.md) · [`docs/PUBLIC-LOCAL-SPLIT.md`](../docs/PUBLIC-LOCAL-SPLIT.md) |
| utf8-json-roundtrip-on-windows | `/jen/sys-admin` UTF-8 note · [`docs/QA.md`](../docs/QA.md) |

Hub-specific traps (profile scope, scaffold vs payload, drawer clip) stay as lesson files until [`docs/PREVIEWER.md`](../docs/PREVIEWER.md) absorbs them — those are still the cheapest *why*.

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
| [lesson-private provider-fellowship-never-names-partners.md](lesson-private provider-fellowship-never-names-partners.md) | private provider AI trainer listings use company “private provider AI Fellowship” — never partner lab names |
| [lesson-flag-looking-output-dir.md](lesson-flag-looking-output-dir.md) | `pdf_to_png` treats leftover `--output-dir` as a folder name — refuse paths that start with `-` |
| [lesson-ssot-dashboard-must-name-live-paths.md](lesson-ssot-dashboard-must-name-live-paths.md) | After a folder rename, update `SSOT.md` + wrap checklists in the same wrap — dual-run is not honesty |
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
| [lesson-public-examples-cannot-reference-private-assets.md](lesson-public-examples-cannot-reference-private-assets.md) | A tracked example must not load fonts, images, or styles from ignored `storage/`; enforce it with an asset-reference test and render gate |
| [lesson-scaffold-readme-must-not-win-path-resolution.md](lesson-scaffold-readme-must-not-win-path-resolution.md) | README-only root nouns (`users/` · `_job-apps/` · …) must not win over live `storage/` during dual-run — resolve payload, not directory existence |
| [lesson-hub-options-must-follow-workspace.md](lesson-hub-options-must-follow-workspace.md) | Design Hub profile and palette controls follow the workspace root, never a hard-coded local roster |
| [lesson-hub-profile-scopes-folder-and-kind.md](lesson-hub-profile-scopes-folder-and-kind.md) | Restore profile before folders; scope folder/kind to the selected profile or the library goes empty |
| [lesson-hub-archive-not-found.md](lesson-hub-archive-not-found.md) | Hub "not found" for galleries/work-samples — exclude `_archive` + `*.template.html`; resolve stale `/storage/<user>/` to `resumes/<user>/` |
| [lesson-one-checkout-privacy-is-gitignore.md](lesson-one-checkout-privacy-is-gitignore.md) | One engine; gitignore + examples; no .env; tracker is who×job not a count |
| [lesson-platform-drafts-are-owned-by-platform.md](lesson-platform-drafts-are-owned-by-platform.md) | Release sisters live in the Socials platform's sibling `drafts/` / `published/` folders — never inside a devlog topic directory |

## Related

- [`docs/VAULT.md`](../docs/VAULT.md) — claim rules (the "silent failure" section)
- [`docs/QA.md`](../docs/QA.md) — the ship gate
- [`docs/LAYOUT-SYSTEM.md`](../docs/LAYOUT-SYSTEM.md) — pagination + content-fit
- [`.claude/commands/pdf-wrap.md`](../.claude/commands/pdf-wrap.md) — the wrap that feeds this
