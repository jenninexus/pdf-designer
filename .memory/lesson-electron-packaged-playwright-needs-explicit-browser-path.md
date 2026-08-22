---
name: lesson-electron-packaged-playwright-needs-explicit-browser-path
description: A frozen desktop runtime must locate its copied Playwright Chromium explicitly; browser folder names vary by Playwright build.
metadata:
  type: project
  date: 2026-08-21
---

When packaging the Windows Electron sidecar, copy Playwright Chromium beside
the frozen runtime and pass its executable path only in frozen mode. Match
`chrome-win*/chrome.exe`, not one assumed Chrome folder spelling.

**Why:** the Playwright download used by the build named its directory
`chrome-win64`, while the first locator assumed `chrome-win`. The frozen app
therefore would fall back to a user Playwright cache or fail on a clean machine,
despite the browser being bundled correctly.

**How to apply:** keep `pdf_tool.browser` as the sole frozen-browser locator;
unit-test the `chrome-win64` layout and run a real frozen runtime export before
calling the installer build verified. Do not leave `PLAYWRIGHT_BROWSERS_PATH`
set for the installed app—the build may use it temporarily only to download the
bundle.

Related: [[lesson-public-clone-path-stays-tracked]]
