---
name: lesson-voice-preview-never-heuristically-redacts-private-text
description: A browser card cannot safely infer that free-form local voice prose contains no private data; show a skeletal card until an owner approves a write.
metadata:
  type: feedback
  date: 2026-08-21
---

Never expose free-form private `characterVoice` or vault `voice` text in a
read-only Design Hub preview, even behind a lexical "redaction" filter. For a
named local profile, return only a fixed generic summary and empty lists. Use
the fictional tracked Jane Example fixture to demonstrate populated card
fields.

**Why:** writing preferences can carry client names, telephone numbers,
credentials, or résumé claims without predictable locator syntax. A pattern
filter can remove obvious URLs and emails yet still leak that context.

**How to apply:** keep the `/api/voice-card` private projection skeletal and
test it with non-obvious private values. Add any populated private Voice Seed
card only through a separately designed, human-approved editor/write flow with
an explicit destination.

Related: [[lesson-one-checkout-privacy-is-gitignore]]
