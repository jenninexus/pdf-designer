---
name: lesson-vsce-pat-cannot-authenticode
description: Syn Themes VSCE_PAT / OVSX_PAT publish a VSIX; they cannot Authenticode-sign PDF-Designer-Setup.exe
metadata:
  type: project
  date: 2026-08-24
---

Marketplace Personal Access Tokens are not a Windows code-signing certificate.
`C:\Github\syn-themes` `VSCE_PAT` / `OVSX_PAT` upload a `.vsix`. They cannot
make `scripts/verify-authenticode.ps1 -RequireSigned` print Valid.

**Why:** Authenticode is a publisher stamp on an EXE. Azure DevOps Marketplace
tokens are a store login. The Syn Themes publisher email (`jenninexus2.0@gmail.com`)
is only a hint for *who* should open Azure Portal. `AZURE_TENANT_ID` /
`AZURE_CLIENT_ID` / `AZURE_CLIENT_SECRET` were empty on SEGOPC; `az` is not
installed. Identity validation is a human ID-document step.

**How to apply:** after Azure Trusted Signing is Approved, fill gitignored
`desktop/azure-trusted-signing.json` and User env, then `npm run dist:signed`.
Trust `verify-authenticode.ps1`, not electron-builder's `signing with
signtool.exe` log. Never upload `PDF-Designer-Setup-0.1.0.exe` while status is
`NotSigned`. Details: `docs/WINDOWS-ELECTRON.md`.

Related: [[lesson-unsigned-dist-must-disable-cert-auto-discovery]]
