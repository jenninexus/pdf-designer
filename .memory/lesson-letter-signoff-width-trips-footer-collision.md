---
name: lesson-letter-signoff-width-trips-footer-collision
description: On a cover letter, a sign-off line wider than ~40% of the page makes check_generation's footer-collision fail even with half the page empty; cutting prose never fixes it
metadata:
  type: feedback
  date: 2026-10-18
---

`footer-collision` finds the lowest lit cluster (the signature) and counts any lit pixel on those same
rows in the *opposite* column as body text running into it. A cover letter signs bottom-left, and the
signature column ends at 40% of the page width. So a sign-off line that runs past that point is counted
as an intrusion into its own signature band. Long titles such as "Founder & Lead Developer, Studio ·
Creator of Product" do this.

**Symptom:** the check fails with "body content overlaps the pinned signature band … Move a section to
the next page". The reported rows **do not move** when you cut prose, and `pdf_to_png` shows a page
with plenty of room.

**Why:** a 2026-10-18 cover letter failed three times while prose was trimmed. The cause was the
sign-off title line, not the body.

**How to apply:** if the collision rows stay put after a cut, shorten the longest sign-off line first
(drop the "· …" tail; the body can carry it). Only then work through the length fixes in
`docs/LAYOUT-SYSTEM.md`.

Related: [[lesson-fixed-height-clips-content-silently]]
