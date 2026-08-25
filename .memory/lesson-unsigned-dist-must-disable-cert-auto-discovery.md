---
name: lesson-unsigned-dist-must-disable-cert-auto-discovery
description: electron-builder will silently Authenticode-sign from the Windows cert store unless CSC_IDENTITY_AUTO_DISCOVERY=false
metadata:
  type: project
  date: 2026-08-24
---

Default `npm run dist` must set `CSC_IDENTITY_AUTO_DISCOVERY=false`. A Valid
Authenticode signature is not proof of the Azure Trusted Signing release path.

**Why:** electron-builder auto-discovers a code-signing certificate in the
Windows store. A leftover personal or unrelated publisher cert would produce an
installer that looks "signed" while using the wrong identity — and it would still
not be the listable Azure Trusted Signing artifact.

**How to apply:** unsigned packaging goes through `desktop/scripts/dist-nsis.cjs`.
Listable builds go through `npm run dist:signed` plus
`scripts/verify-authenticode.ps1 -RequireSigned`. Never attach
`PDF-Designer-Setup-0.1.0.exe` to Gumroad or JN checkout.

Related: [[lesson-clean-installer-target-must-be-proven]] · [[lesson-clean-host-is-not-a-dev-pc]] · [[lesson-vsce-pat-cannot-authenticode]]
