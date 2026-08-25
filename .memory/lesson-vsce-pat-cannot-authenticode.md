---
name: lesson-vsce-pat-cannot-authenticode
description: A VS Code Marketplace PAT publishes a VSIX; it cannot Authenticode-sign a Windows Setup.exe
metadata:
  type: project
  date: 2026-08-24
---

Marketplace Personal Access Tokens are not a Windows code-signing certificate.
A `VSCE_PAT` / `OVSX_PAT` uploads a `.vsix`. They cannot make
`scripts/verify-authenticode.ps1 -RequireSigned` print Valid.

**Why:** Authenticode is a publisher stamp on an EXE. Marketplace tokens are a
store login. They are different products.

**How to apply:** unsigned packaging is `npm run dist`. A signed maintainer
build is `npm run dist:signed` only after gitignored credentials exist. Trust
`verify-authenticode.ps1`, not electron-builder's `signing with signtool.exe`
log. Never distribute `PDF-Designer-Setup-*.exe` while status is `NotSigned`.
Details: `docs/WINDOWS-ELECTRON.md` (public) · `docs/WINDOWS-ELECTRON.local.md`
(maintainer).

Related: [[lesson-unsigned-dist-must-disable-cert-auto-discovery]]
