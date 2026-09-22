---
name: lesson-pdf-viewer-needs-first-class-route
description: A themed iframe can look correct while its PDF document never loaded; serve the viewer as a first-class route and verify rendered pages inside the frame
metadata:
  type: project
  date: 2026-09-21
---

Do not accept a dark preview canvas as proof that the PDF viewer works. Serve the viewer document from the
first-class `/pdf-viewer` route, keep CSS and JavaScript under `/_hub/`, and verify that the iframe contains
the toolbar plus one rendered image per PDF page.

**Why:** a browser client blocked `/_hub/pdf-viewer.html` as an embedded document while still painting the
parent iframe's dark background. The result looked partly correct, returned healthy API responses, and passed
unit tests, but showed no PDF. Moving the document to `/pdf-viewer` preserved static assets while making the
navigation explicit and browser-safe.

**How to apply:** test `/api/pdf-info` and `/api/pdf-page`, then open a real `_exports/` PDF in the Hub and
inspect the iframe for `.pdf-toolbar` and `.pdf-page` elements. A screenshot of the shell alone is insufficient.

Related: [[lesson-hub-nav-switch-through-ipad-pro]]
