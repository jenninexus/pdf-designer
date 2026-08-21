---
name: lesson-hub-restart-for-app-html
description: Restart the local Design Hub after changing preview.py APP_HTML before judging a browser screenshot.
metadata:
  type: project
  date: 2026-08-21
---

When changing `src/pdf_tool/preview.py`'s `APP_HTML`, restart the local
`python -m pdf_tool.preview` process before visual QA. Static files are read on
request, but the Library page's Python string is loaded when the server starts.

**Why:** CSS and static route edits can appear immediately while the root Library
page still serves an old generated HTML string. That produces misleading results
(for example, an intentionally removed icon class renders as an empty button).

**How to apply:** Verify the root response contains the new markup, then run the
compact browser check. A server restart is not required for `hub.css`,
`recipes.html`, or `vault.html` alone.

Related: [[lesson-hub-stack-at-md-breaks-desktop-split]]
