---
name: lesson-track-tags-hide-true-claims
description: A true claim tagged for the wrong track becomes invisible to the résumé query — nothing errors, the best evidence just never appears
metadata:
  type: project
  date: 2026-07-25
---

**The vault's real danger is not a false claim — it is a true claim going invisible.** A claim tagged
with a track that does not match the job is simply never selected. Nothing errors. The résumé
renders, the page count is right, the palette passes, and the strongest evidence its owner has is
absent from the page.

**Why:** a résumé is a *query* against the vault. Track tags were being used to answer *"is this
relevant to this job?"* when they should only answer *"can this be selected at all?"* Conflating
those made real, provable experience unreachable:

| What went invisible | How |
|---|---|
| Five design claims (Photoshop, Figma, Affinity, Adobe CS, UX/UI) | Tagged `ui-ux` on a vault with no `ui-ux` track. A UI/UX résumé would have shipped without her entire design toolkit. |
| Five engine claims (WebGPU, multiplayer, WWISE, Unreal/Unity, platforms) | Tagged `game-dev` only, so an engine-research résumé built on the `ai` track could not see any of them. |
| **Shade's AAA credits (2026-07-25)** | `Oddworld: Soulstorm` (PS5), `Fruit Ninja 2`, `Cthulhu Chronicles` were tagged `game-dev` **only**. On the Sony **3D Character Art Lead** application — an AAA role — a `3d-art` query could not see her AAA console credit. Her single strongest proof for that listing was one tag away from never appearing. |

**How to apply:**

- **Relevance is the ranking's job, never the tag's.** Tags decide *selectable*; `toolbeltOrder` and
  `strength` decide *what leads*. Tools carry `tracks: ["any"]` deliberately — a game listing may ask
  about 3ds Max; an AI lab cares that you have shipped in Blender.
- **Run `check_vault --explain <user> <track>` BEFORE writing a word.** It prints every claim the
  track can reach, in rank order. **If something you would expect is missing from that list, it is
  tagged wrong and will never appear on any résumé — fix the tags, not the résumé.**
- **Shipped credits should usually be reachable from every track they plausibly serve.** A shipped
  title is evidence of delivery, not just of a genre.
- Then run `audit_resume <user> <track> <doc>.html` after building: it diffs the finished document
  against the vault and exits non-zero on a missing `lead` claim, so you cannot ship past one by
  accident. When you *do* omit a lead claim, be able to say why (e.g. Hasbro was omitted from the
  Sony résumé because it is a client relationship, not a character-art credit).

Related: [[lesson-ask-before-calling-it-a-gap]] · [[lesson-twin-files-always-fork]]
