---
name: lesson-hub-profile-scopes-folder-and-kind
description: Restore the Hub profile filter before rebuilding folders; scope folder/kind to that profile or the library goes empty
metadata:
  type: feedback
  date: 2026-08-13
---

**Choosing a header profile must show that profile’s documents.** Restore
`pdf-designer.hub.profileFilter` **before** `buildFolderSelect()`, and derive
folder options plus kind-chip counts from `docsForProfile(activeProfile())`.
If the current kind has zero docs for that profile, reset kind to All.

**Why:** profile and folder both persist in `localStorage`. Restoring Jenni
*after* a collage/shade folder was already selected made the intersection
empty — 23 tagged Jenni HTML files scanned fine; the sidebar still said
“No templates match these filters.” Kind chips counted the whole library, so
Collages stayed clickable on Jenni even when she had zero tagged collages.

**How to apply:**

- `applyProfileChange()` rebuilds kind chips and folders after the profile
  select changes (desktop and drawer).
- Hyphen-bounded path tokens (`meet-jenni-bot`) tag the matching profile;
  untagged collages still need All profiles.
- A profile card with no HTML (studio, today) keeps its menu row; the empty
  copy must name the profile instead of looking like a blank bug.

Related: [[lesson-hub-collage-hidden-by-profile-filter]] · [[lesson-hub-options-must-follow-workspace]]
