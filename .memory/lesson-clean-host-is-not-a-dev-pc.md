---
name: lesson-clean-host-is-not-a-dev-pc
description: Python/Node/npm on a Windows box disqualify it as the installer proof — the harness is proving the bundled runtime, not that NSIS can run next to a checkout.
metadata:
  type: project
  date: 2026-08-23
---

Do not treat BEETHOVEN, LIVPHI, or SEGOPC as the **listing** clean-machine proof.
Default `verify-clean-machine.ps1` still refuses `python` / `py` / `node` / `npm`
and a checkout. This LAN has no spare VM; `-BundledRuntimeProof` is the named
substitute: skip PATH/checkout preflight, still install from a drop folder, and
assert the child is `{InstallDir}\resources\runtime\pdf-designer-runtime\pdf-designer-runtime.exe`.
It is **not** a listing gate. Do not add a generic `-SkipToolchainCheck`.

**Why:** the NSIS package bundles Python + Playwright Chromium so a customer
never installs our toolchain. A PATH Python on SEGOPC/BEE/LIVPHI would hide a
packaging bug. A listing still needs Authenticode Valid plus (preferred) a
fresh Win10/11 x64 VM.

**How to apply:** copy only the Setup EXE + script to
`C:\pdf-designer-installer-drop\` (or `C:\p\pdf-designer-installer-drop\` on
BEE). Use `-BundledRuntimeProof` on a toolchain PC; use `-RequireAuthenticode`
only on a signed EXE. LIVPHI source mirror is `\\LIVPHI\Github\pdf-designer`,
not the denied `git` share. Details: `docs/WINDOWS-ELECTRON.md`.

Related: [[lesson-clean-installer-target-must-be-proven]] · [[lesson-hidden-electron-close-needs-stop-process]]
