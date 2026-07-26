---
name: lesson-twin-files-always-fork
description: Two files maintained as "twins" always drift apart silently — make one the SSOT and reduce the other to a pointer
metadata:
  type: feedback
  date: 2026-07-25
---

**Never maintain the same content in two places as "twins."** Pick one file as the SSOT and reduce
the other to a **pointer** that carries no protocol of its own.

**Why:** `/voice-design` existed twice — `~/.claude/commands/jen/voice-design.md` (global) and
`voice-seed/.claude/commands/voice-design.md` (repo). Both said they were the same procedure and
told the reader to prefer the other in some situations. By 2026-07-25 they had **260 lines of
diff**, and *each held content the other lacked*:

- global only: the socials/bot "Quick answer" routing sections, and the `/lip-sync` ÷ `/tts`
  disambiguation ("voice" means three unrelated things)
- repo only: the `private provider` / Project Dynamo lane, cross-repo traps, repo docs

So the answer an agent gave depended on which file it happened to open — with no error and no
signal that anything was missing. Worse, the repo copy had grown a line saying *"see global twin for
full steps"* for three subcommands, which would have dead-ended the moment either side changed.

This is the same shape as the vault's **silent failure** ([[lesson-track-tags-hide-true-claims]]):
nothing breaks loudly, information just quietly stops being reachable.

**How to apply:**

- **One SSOT, one pointer.** The SSOT is normally the **repo that owns the domain** (voice-seed owns
  voice), not the global convenience copy — a repo file travels with clones and gets reviewed.
- **The pointer must be inert:** a link, a one-screen orientation table at most, and an explicit
  "⛔ do not add protocol here" banner. If a pointer starts growing steps, it is becoming a twin again.
- **Before reducing one side, diff them and port everything unique.** Both sides had material worth
  keeping; a naive "delete the older one" would have silently dropped the `/lip-sync` disambiguation.
- **Check for dangling cross-references** after the merge — "see the other file for X" must become X.
- Same rule already applied inside this repo: `storage/VAULT.md` and `storage/JOB-ASSESSMENT.md` are
  deliberately 7-line stubs pointing at `docs/`, not copies. Keep them that way.

Related: [[lesson-track-tags-hide-true-claims]] · [[lesson-guard-assumptions-must-be-measured]]
