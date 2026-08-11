---
name: lesson-hub-stack-at-md-breaks-desktop-split
description: Do not stack library above stage at md (991.98) — desktop/zoomed windows look broken; keep LEFT/RIGHT until phones (≤575.98).
metadata:
  type: feedback
  date: 2026-08-11
---

# Hub: stacking at md breaks the desktop split

## Rule

**Keep Design Hub as library LEFT + viewer RIGHT from ≥576px.** Only stack on phone widths
(`≤575.98px`). Do **not** use `max-width: 991.98px` to force `grid-template-columns: 1fr` +
`library { max-height: 38vh }` — that is what made a “great yesterday” hub look like a thin
thumbnail strip over an empty void on ordinary desktop / zoomed windows.

## Why it bit us

`hub.css` treated md-max (991.98) as “layout compact = stack.” Many real desktop viewports (IDE
split panes, 125% zoom, ~900–1100 CSS px) sat under that line and got the phone layout while still
showing the full desktop toolbar. The fix looked like a broken viewer; the root cause was the
breakpoint, not missing HTML.

## Related traps

- Toolbar **★** as a separate control: font metrics leave the glyph off-center and wastes header
  space. Pin inside the folder dropdown (ghost ★ on hover → filled when pinned → sort to top).
- Folder picker menu as `position:absolute` inside `.hub-bar-scroll` (`overflow-y:hidden`) —
  opens in the DOM but is clipped (looks “dead”). Use `position:fixed` + JS top/left from the
  trigger rect — same clip class as `hub-more` before it moved into `.hub-bar-pin`.
- CSS-only drawer contracts without HTML/JS — see `lesson-hub-drawer-css-without-html-clips-more.md`.

## Guard / SSOT

- `src/pdf_tool/static/hub.css` — stack only in `@media (max-width: 575.98px)`
- `docs/PREVIEWER.md` · `.config/mcp-pdf-designer.json#breakpoints` ·
  `www-theme-kit/profiles/pdf-designer.json#breakpoints`
