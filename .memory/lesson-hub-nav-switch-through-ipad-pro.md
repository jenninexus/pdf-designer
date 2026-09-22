---
name: lesson-hub-nav-switch-through-ipad-pro
description: Design Hub hamburger must cover iPad Pro landscape (1366), not stop at 768
metadata:
  type: project
  date: 2026-08-26
---

Header-chip apps (Design Hub) treat **iPad Pro 12.9 landscape (1366px)** as tablet chrome, not desktop.

`md` (768) as `nav_switch` leaves the full header chips + a 920px-capped home grid on both iPad portrait and iPad Pro landscape. The leftover 16px strip on a 390px offcanvas is the same class of bug: the **phone** sheet is not full-bleed.

**Guard:** `nav_switch: xxl` (1400) in `www-theme-kit/profiles/pdf-designer.json`. Hamburger is **mobile-first** (visible by default; `@media (min-width: 1400px)` hides it). Do not `display:none !important` on the base `.hub-drawer-toggle` — a later until-xxl show can lose the specificity war and leave 390 with no menu. **Full-bleed is phones only** (`@media (max-width: 575.98px)` and short landscape). From 576–1399.98 the drawer is an almost-full end-panel (`min(92vw, 100vw - 24px)`), sash on — never `width: 100vw` on a laptop. Header icon buttons share one 1:1 `--hub-icon-box` square (Export `primary` is color only). Kit: `scss/_offcanvas-nav.scss` + `@mixin until-xxl` / `offcanvas-end-panel`. Short landscape (`max-height: 480`) stacks the library and uses the phone sheet.

Do not invent a new px. Mixer/bottom-tab apps (Jen DJ phone) keep tabs; they only reuse this sheet for overflow menus.

[[see-also: docs/PREVIEWER.md]] [[see-also: www-theme-kit/docs/BREAKPOINTS.md]]
