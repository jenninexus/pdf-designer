---
name: lesson-hub-nav-switch-through-ipad-pro
description: Select a named nav switch from the kit; PDF Designer uses lg after the owner desktop-toolbar decision
metadata:
  type: project
  date: 2026-10-30
---

Use the existing `lg`/992 breakpoint for Design Hub navigation. The owner explicitly changed the previous `xxl`/1400 choice on 2026-10-30 to keep the scrollable toolbar on smaller desktop windows.

**Why:** the former rule treated every 1366px desktop as a tablet, hiding controls the owner uses. Device names are not a reliable nav-switch policy.

**Guard:** update `www-theme-kit/profiles/pdf-designer.json`, Hub CSS, drawer-resize.js, project config and PREVIEWER together. Check both sides of 991.98/992. Phones (≤575.98 or short landscape ≤480px high) keep the full-bleed sheet; 576–991.98 uses the resizable end-panel. Library/viewer stacking remains a separate phone-only choice. Header icons must exist before scripts run so mode navigation cannot briefly replace them with labels.

Syna supplies visual adapter tokens; www owns responsive geometry. Neither private kit is a runtime dependency of the public clone.

[[see-also: docs/PREVIEWER.md]] [[see-also: www-theme-kit/docs/BREAKPOINTS.md]]
