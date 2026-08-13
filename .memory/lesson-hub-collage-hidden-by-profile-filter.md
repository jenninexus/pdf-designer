---
name: lesson-hub-collage-hidden-by-profile-filter
description: Untagged collage projects vanish when Hub Profiles is set to martian/jenni/shade — clear to all profiles or search the folder.
metadata:
  type: feedback
  date: 2026-08-11
---

# Hub Collages filter ≠ Profiles filter

**What happened:** Agency Patreon desk collages lived under
`storage/collages/agency-patreon-desks/_candidates/` and were correctly classified
`kind=collage`, but they did not appear when browsing **Collages** because
**Profiles** was still set to `martian` (most other collage projects are path-tagged
`martian`). Untagged projects have `profile: null` and are filtered out.

**Rule:** When hunting a new collage project, set Profiles → **all profiles** (or search
the project folder name). Collages chip alone is not enough if a profile chip is sticky
in `localStorage`. Hyphen-bounded project names (`meet-jenni-bot`) now tag the matching
profile, so choosing **jenni** will show those collages. Untagged projects still vanish.

**Also:** Prefer a **flat** `_candidates/` directory (filenames encode canvas/bg/fit). Nested
`--out` subfolders still scan, but they clutter the folder picker and break the documented
shape in `make-collage.md`.

**Guard:** Docs — [`docs/PREVIEWER.md`](../docs/PREVIEWER.md) filters note · private tip in
`storage/docs/WORKSPACE.md`.
