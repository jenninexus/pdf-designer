---
name: lesson-hub-native-select-ignores-device-frame
description: Chrome device-mode native select popups ignore the emulated viewport — keep Hub lists inside the sheet
metadata:
  type: project
  date: 2026-08-26
---

Do not put a long native `<select>` in the Design Hub drawer (or any compact offcanvas). Chrome DevTools device mode draws the OS/browser popup against the **real** window, so options clip off the fake iPad/phone frame. Real tablets can do the same when the list is wider than the sheet.

**Why:** Native `<option>` UI is not a descendant of the page. CSS `max-width: 100%` on the `<select>` does not constrain the popup. The folder picker already avoided this with a custom list; palette / profiles / format did not.

**How to apply:** Wrap drawer `<select>`s (except `.hub-folder-native`) with `hub-select.js` — trigger + absolutely positioned menu, `left:0; right:0; max-width:100%`, `max-height: min(40vh, 320px)`, overflow-y auto. Restart the Hub after changing `preview.py` HTML (`[[lesson-hub-restart-for-app-html]]`). Do not invent a 1024px breakpoint; stack home cards at existing `lg-max` (1199.98).

`C:\mcp\.config\mcp-breakpoints.json` is a **registry** of who uses which set, not the numeric SSOT. Numbers stay in both kits’ `_breakpoint-tokens.scss`.

[[see-also: lesson-hub-nav-switch-through-ipad-pro]] [[see-also: lesson-hub-drawer-css-without-html-clips-more]] [[see-also: docs/PREVIEWER.md]]
