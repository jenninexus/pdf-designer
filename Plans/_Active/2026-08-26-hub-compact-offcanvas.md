# Design Hub compact chrome — tablet + phone offcanvas

## Done when
- [x] At 390×844 the open menu is **full-bleed** (no leftover strip).
- [x] At iPad portrait 1024 and iPad Pro landscape 1366 the **header chips/nav/selects are in the hamburger**, not the top bar.
- [x] Desktop **≥1400** still shows the full header buttons.
- [x] Home kind-grid fills the stage width (no 920px cap / empty right void).
- [x] Short landscape (max-height 480) stacks library like a phone.
- [x] Patreon + PayPal tip controls exist on splash, in the drawer, and on `/wizard`.
- [x] www-theme-kit + syna-theme-kit document the same compact-offcanvas contract without forking numbers.
- [x] Hub at http://127.0.0.1:8787/ still loads.

## Task checklist
- [x] Raise Design Hub `nav_switch` from `md` (768) to `xxl` (1400)
- [x] Full-bleed drawer ≤1399.98; hide sash; 44px tap floor
- [x] Fill home grid; tighten tablet padding; short-landscape stack
- [x] Support / tip buttons (Patreon + PayPal.Me)
- [x] Wizard hamburger (it had none)
- [x] Kit mixins + `_offcanvas-nav.scss` + profile/docs
- [x] Verify at 390 / 768 / 1024 / 1366 / 1400

## Assumptions
- **nav_switch = xxl (1400).** iPad Pro 12.9 landscape is 1366 (xl). Rejected: `xl` (1200) because the attached landscape screenshot would still show header chips. Flip if a 13" laptop should keep inline nav.
- **Library column stays** from ≥576 (content, not chrome). Only header buttons move into the drawer. Flip if tablet should hide the library too.
- **Full-bleed sheet** on every compact width, not a 320px side panel. Flip if landscape tablet should keep a 480px end-panel.
- Tip URLs from `docs/PRODUCT.md`: PayPal.Me/jenninexus + Patreon `c/JenniNexus`. No extra features unlocked.
- Do **not** invent a new px number. Use existing `.98` maxes.
- Do **not** implement Jen DJ UI this run — document the shared contract + handoff prompt.
- **Hamburger is mobile-first.** Visible by default; hide at `min-width: 1400px`. Rejected: hide-by-default + until-xxl show (specificity war left 390 with `display:none`).

## Evidence
- **VERIFIED** Playwright headless Chromium (2026-08-26) `/?no-splash=1`:
  - 390×844: hamburger `flex` 44px, chips/nav `none`, drawer open width 390, home grid max-width none / width 366
  - 1024×1366: hamburger 44px, chips `none`, drawer 1024
  - 1366×1024: hamburger 44px, chips `none`, drawer 1366, grid 1102 (fills stage beside library)
  - 1400×900: hamburger `none`, chips/nav `flex`, until-xxl false
- **VERIFIED** HTTP smoke: splash/drawer Patreon + PayPal.Me; `/wizard` hamburger + support; `/_hub/hub-chrome.js` 200; hub.css has 1399.98 + `width: 100vw`, no 920px cap.
- **VERIFIED** Playwright 1024×1366 follow-up (2026-08-26): home grid **1 column** (card ~140×762); open drawer `x=0` width 1024; palette custom menu x=16 w=992 (inside viewport); copy 15.2px / tip pills min-height 34px; `hub-select.js` loaded.
- **UNVERIFIED** headed iPhone/iPad Safari (no device in this run). Jen DJ booth UI not implemented.

## Deferred
- Jen DJ booth-nav hamburger implementation (other agent) — contract in syna-theme-kit `_offcanvas-nav.scss` + `profiles/jen-dj.json`
- Headed Playwright on LIVPHI
- Raising other www sites' nav_switch to xxl (MG stays md)
- www-theme-kit commit sat on sibling branch `codex/social-notifier-release` — explicit-path commit only, no push of that branch
