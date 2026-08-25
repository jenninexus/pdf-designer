---
name: lesson-clean-host-is-not-a-dev-pc
description: Python/Node/npm on a Windows box disqualify it as the installer proof — the harness is proving the bundled runtime, not that NSIS can run next to a checkout.
metadata:
  type: project
  date: 2026-08-23
---

Do not treat a daily-driver or source-mirror PC as the **listing** clean-machine
proof. Default `verify-clean-machine.ps1` still refuses `python` / `py` /
`node` / `npm` and a checkout. When no spare VM exists, `-BundledRuntimeProof`
is the named substitute: skip PATH/checkout preflight, still install from a
drop folder, and assert the child is
`{InstallDir}\resources\runtime\pdf-designer-runtime\pdf-designer-runtime.exe`.
It is **not** a listing gate. Do not add a generic `-SkipToolchainCheck`.

**Why:** the NSIS package bundles Python + Playwright Chromium so a customer
never installs the toolchain. PATH Python on a developer PC would hide a
packaging bug. A listing still needs Authenticode Valid plus (preferred) a
fresh Win10/11 x64 VM.

**How to apply:** copy only the Setup EXE + script outside any git checkout.
Use `-BundledRuntimeProof` on a toolchain PC; use `-RequireAuthenticode` only
on a signed EXE. Details: `docs/WINDOWS-ELECTRON.md` (public) ·
`docs/WINDOWS-ELECTRON.local.md` (LAN hosts).

Related: [[lesson-clean-installer-target-must-be-proven]] · [[lesson-hidden-electron-close-needs-stop-process]]
