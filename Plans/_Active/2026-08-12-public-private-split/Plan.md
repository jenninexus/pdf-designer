# Public vs private architecture + history scrub prep

## Done when

- [x] `docs/PUBLIC-LOCAL-SPLIT.md` exists and matches agency sibling pattern
- [x] Public docs audited: clone-safe protocol stays; SEGO-only detail lives under `storage/docs/`
- [x] `docs/PRODUCT.md` + `storage/docs/{MARKETING,WORKSPACE,README}.md` describe the same free/paid + public/private map
- [x] Tracked placeholder `storage/docs/README.md` on GitHub (socials-style gitignore exception)
- [x] History-scrub plan lists paths + commands; **no force-push** until human authorizes (Hard Stop)
- [x] Sibling pointers: agency / socials / dashboard / www-theme-kit profiles updated
- [x] Active packaging plan + AGENTS/SSOT/docs README cross-links updated

## Task checklist

- [x] Write PUBLIC-LOCAL-SPLIT + GETTING-STARTED (public clone path; WHITE-LABEL → alias stub)
- [x] Move SEGO history-scrub + private packaging notes into storage/docs
- [x] Refresh PRODUCT / MARKETING / WORKSPACE / storage docs index
- [x] Gitignore: `!storage/docs/README.md`
- [x] History scrub script/doc (local only until push auth)
- [x] Cross-repo: agency sibling table, socials PUBLIC-LOCAL-SPLIT, dashboard split doc, theme-kit profiles
- [ ] Verify links; commit tracked paths; wrap

## Assumptions

1. **WHITE-LABEL content stays public** under a clearer name (`GETTING-STARTED.md`). Burying the clone path in gitignored `storage/` would break the free-product story. Rejected: move entire WHITE-LABEL private.
2. **Career protocol docs** (`VAULT`, `JOB-ASSESSMENT`, `APPLICATIONS`, `STORAGE`) stay public as *rules without PII* — same as socials’ public `docs/DISCORD.md`.
3. **History rewrite is prepared, not executed.** Force-push / filter-repo onto `origin/main` needs jenninexus auth + explicit human OK (Hard Stop #1).
4. **Plans folder stays `_Active`** (existing convention), not `_ACTIVE`.
5. **www-theme-kit stays private** (not a public product); profiles get privacy/product pointers only.

## Evidence

- VERIFIED: `git add -n storage/docs/README.md` stages; `MARKETING.md` refused as ignored
- VERIFIED: `git ls-files .claude/commands` = `*.example.md` only (prior session)
- VERIFIED: history still contains start/wrap/make-resume/mcp json — scrub doc lists them
- UNVERIFIED: force-push scrub (parked — Hard Stop)
- UNVERIFIED: push to origin (auth)

## Deferred

- Actual `git filter-repo` + force-push to GitHub
- TestPyPI upload (`TESTPYPI_TOKEN`)
- Push of commits ahead of origin (auth)
- Deepen `examples/resume-studio/` Hub card
- Agency Patreon collage shelve
