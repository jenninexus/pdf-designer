---
name: lesson-hidden-electron-close-needs-stop-process
description: Hidden Electron (no ShowAppWindow) often has no main window, so CloseMainWindow() returns false and a clean-machine proof dies after a successful export
metadata:
  type: project
  date: 2026-08-24
---

`scripts/verify-clean-machine.ps1` must not require `CloseMainWindow()` to
succeed. If it returns false, `Stop-Process` the Electron PID, then wait for
exit and still assert the bundled `pdf-designer-runtime` and loopback port die.

**Why:** the harness defaults to a hidden window so it does not steal the
daily-driver foreground. A hidden Electron process often has no main window,
so `Process.CloseMainWindow()` is false even when install, Jane workspace,
and light/dark export already passed.

**How to apply:** keep `-ShowAppWindow` for human GUI observation. Automation
and `-BundledRuntimeProof` use the Stop-Process fallback. Do not treat a
hidden-window close failure as an installer defect.

Related: [[lesson-clean-host-is-not-a-dev-pc]]
