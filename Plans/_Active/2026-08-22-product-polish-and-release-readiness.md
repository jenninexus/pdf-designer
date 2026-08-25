# Active plan — Product polish, public-safe release readiness, and cross-repo alignment

**Date:** 2026-08-22  
**Status:** Active — replaces the completed 2026-08-21 release audit and standalone-build plan.  
**Scope:** PDF Designer is the control plan for this cross-repo work. It records references only; each
linked repository remains owner of its own implementation.

## Done when

- [x] PDF Designer's public engine, examples, docs, and local/private workspace boundary are audited and
      remain clone-safe; temporary or superseded material is archived instead of deleted.
- [x] The Design Hub and Electron-hosted Hub share one polished responsive contract at 390, 576, 768,
      992, 1200, 1400, and 1920px, with coherent navigation switches, touch targets, centered action
      rows, and local Font Awesome Free icon treatment.
- [x] A fresh, public-safe visual set covers Library, Recipes, Vault, and Start/Wizard; previous capture
      sets are retained under a dated archive rather than mistaken for current product evidence.
- [x] Product-design and JenniNexus product-widget preparation name the release-gated direct-PayPal,
      Gumroad, Patreon, and free-GitHub roles without creating a checkout or promising a download.
- [x] `www-theme-kit` remains the sole PDF Designer runtime-kit authority; the profile, MCP cache, and
      Hub breakpoints agree. `syna-theme-kit` remains historical lineage only, with no duplicate profile.
- [x] The optional Voice Seed handoff correctly distinguishes the character and application registers;
      no private claims, contacts, or vault data are copied into Voice Seed.
- [ ] PDF Designer is mirrored to `C:\Github\pdf-designer` on LIVPHI using the approved local-network
      route. A clean-machine Electron GUI/install test is **not** BEE or LIVPHI: those machines have
      Python/Node/checkouts. Proof host = a fresh Win10/11 x64 VM. See `docs/WINDOWS-ELECTRON.md`.
- [x] Start route can seed a gitignored vault from an uploaded résumé/cover letter (inferred claims,
      local parse only) and edit it before save (2026-08-23).
- [x] Docs, plan index, roadmap, local dev log, and next-agent handoff state verified versus unverified
      work precisely.

## Task checklist

### 1. Consolidate the project record

- [x] Move the completed 2026-08-21 release-audit companion to `_Complete/`.
- [x] Move the superseded 2026-08-21 standalone plan to `_Complete/`; carry its unfinished release
      gates below rather than leaving two competing active plans.
- [x] Reconcile `docs/README.md`, the public/local split, release audit, and generated workspace seed;
      retain only durable public documentation in the public index.
- [x] Verify `.gitignore` against the root-noun workspace, exports, capture artifacts, bare commands,
      local configuration, and generated Electron artifacts.

### 2. Product quality and responsive proof

- [x] Restyle the Start/Wizard route as a dark-default local-first experience; preserve the
      fictional Jane Example, one renderer, and no-account/no-write boundaries. Document the
      localhost and pre-release standalone first-launch path without promising a download.
- [x] Audit `src/pdf_tool/static/hub.css`, Hub pages, and Electron host against the shared breakpoint
      scale. Keep the current useful Dockview-derived idea (persisted local resizing) but do not add a
      movable-panel dependency to this thin shell.
- [x] Standardize action-row alignment, button hierarchy, Font Awesome Free icon treatment, focus,
      reduced motion, and touch-friendly sizing across Library, Recipes, Vault, and Start.
- [x] Run an independent local visual matrix from the public example workspace at all required
      breakpoints; distinguish local browser proof from tomorrow's clean-machine Electron proof.
- [x] Archive existing dated screenshots, then replace the public feature set with current
      public-example-only captures for each Hub page.

### 3. Theme, voice, and product alignment

- [x] Cross-check `www-theme-kit/profiles/pdf-designer.json`,
      `www-theme-kit/scss/_breakpoint-tokens.scss`, and `C:\mcp\.config\mcp-breakpoints.json`;
      correct only genuine drift.
- [x] Preserve the official decision: `www-theme-kit` is PDF Designer's runtime/design profile;
      `syna-theme-kit` owns Jen DJ and is lineage-only for PDF Designer.
- [x] Confirm the Voice Seed application/character register pointers against root-noun local data and
      public seeds; update the handoff only if paths or safety behavior drifted.
- [x] Update `C:\Github\product-design\product-registry.md` and its PDF Designer record with the
      release-gated direct-PayPal vs Gumroad price policy and Patreon membership boundary. Prepare a
      reusable JenniNexus product-widget data contract, but do not activate payment or delivery.

### 4. Cross-PC and release gates

- [x] Mirror the local PDF Designer repository to LIVPHI's `C:\Github\pdf-designer` without copying
      ignored private workspace data, credentials, Electron runtime, or installer artifacts.
      **Done 2026-08-24** via writable `\\LIVPHI\Github` (public `git clone --filter=blob:none --depth 1`
      https://github.com/jenninexus/pdf-designer.git). Advertised `\\LIVPHI\git` stays access-denied;
      do not use admin shares.
- [x] Inspect the LIVPHI mirror and record its suitable role: source/docs mirror only, not proof of the
      clean-machine release gate until its preflight is explicitly passed.
- [x] BEETHOVEN `C:\p\pdf-designer` fast-forwarded to GitHub `829e0ca` (2026-08-22). Source/docs only —
      not a clean-machine proof host (Python/Node + checkout present). `C:\p\pdf-designer-installer-drop\`
      is a valid *drop folder* for the EXE+script, but BEE still fails preflight because the toolchain
      is on PATH. That is correct. LIVPHI is the same class of machine.
- [x] Start /wizard résumé+cover import → review editor → gitignored starter vault (2026-08-23).
      Claims tagged `inferred`. No network parser. Reserved ids (`examples`, `you`) cannot be overwritten.
- [x] Carry forward the only release blockers: clean Windows 10/11 x64 install/GUI/process-cleanup test,
      signing decision, and human-owned PayPal production/fulfilment policy.
      **Signing decision (2026-08-24):** Azure Trusted Signing via electron-builder 26
      `win.azureSignOptions`. Local `npm run dist` stays unsigned (`CSC_IDENTITY_AUTO_DISCOVERY=false`)
      and is **not listable**. Signed dist is `npm run dist:signed` after the human provisions the
      Azure identity. Clean-machine proof remains a fresh Win10/11 x64 VM with
      `-RequireAuthenticode` on the signed EXE.

## Assumptions

- Direct website PayPal will be the customer-favorable **$5** route only after release gates pass;
  Gumroad may list the same installer at **$6** to absorb its materially higher direct-sale fee. The
  price difference is a channel-cost policy, not a feature tier. Revisit if processor fees change.
- Patreon remains voluntary membership/tip support, not proof of purchase or an installer entitlement,
  unless a later, explicitly designed entitlement and fulfilment system exists.
- Moving plans and captures to dated archives is reversible history preservation, not deletion.
- LIVPHI mirroring is authorized as a source mirror. Its Electron testing must not begin merely because
  the source arrives there; tomorrow's owner-led clean-machine verification remains its own gate.

## Evidence

- VERIFIED — the 2026-08-21 local plan records an unsigned Windows x64 Electron/NSIS build, frozen
  runtime export, wizard, test suite, and public clone checks.
- VERIFIED — PDF Designer's own config and docs identify `www-theme-kit` as the runtime-kit authority;
  `syna-theme-kit` is historical lineage only.
- UNVERIFIED — clean-machine Windows installer GUI on a **fresh VM**, and signed Authenticode behavior.
- VERIFIED — 2026-08-24 rebuilt unsigned `desktop/dist/PDF-Designer-Setup-0.1.0.exe`; Authenticode `NotSigned` (not listable). `npm run dist:signed` fails closed without Azure identity. Hub title screen measured 3s hold + 2s fade on localhost `/?splash=1`. Documents policy: follow Windows Documents (SEGOPC OneDrive KFM). `-BundledRuntimeProof` PASS from `C:\pdf-designer-installer-drop\` (bundled runtime path, Jane light+dark, uninstall kept workspace). That is **not** a listing gate. Syn Themes `VSCE_PAT` cannot sign the EXE.
- VERIFIED — public-only QA workspace captured Library, Recipes, Vault, and Start at 390, 576, 768,
  992, 1200, 1400, and 1920px; 91 source tests passed.
- BLOCKED — Azure Trusted Signing identity validation (human + ID documents as `jenninexus2.0@gmail.com`). Until Approved + `npm run dist:signed`, there is no Gumroad/JN `$5` file.
- VERIFIED — 2026-08-24 `\\LIVPHI\Github\pdf-designer` public clone exists (source/docs). `\\LIVPHI\git` remains access-denied. BEETHOVEN `C:\p\pdf-designer` already mirrored. Neither host is a clean-VM listing proof.
- VERIFIED — 2026-08-22 SEGO→GitHub `829e0ca`, then BEETHOVEN `C:\p\pdf-designer` reset onto `origin/main`
  (history-scrub divergence; working tree was otherwise clean). BEE now has current source. BEE is **not**
  a clean-machine installer target: Python/Node are present and `C:\p\pdf-designer` is a checkout.
  `scripts/verify-clean-machine.ps1` will refuse that host. Use a separate Windows 10/11 x64 box (or a
  fresh Windows user/VM with no Python/Node/checkout) for GUI/install/process-cleanup proof.
- VERIFIED — rechecked through sys-admin after the access request: the cached registry's passwordless
  `LIVPHI\\pcnet` SMB route cannot open the advertised `git` share, and its named `Synabrain`, `Synagen`,
  and `pc-network` shares are absent. SSH with the configured `Shade` key times out; WinRM rejects the
  workgroup host before a command can execute. This is current remote-state drift, not a reason to use an
  administrative-share workaround or change security policy from SEGOPC.

## Deferred / human-owned

- Provision Azure Trusted Signing **when budget allows** (held 2026-08-25). Identity
  validation + Entra app. Store `AZURE_*` in sys-admin; fill gitignored
  `desktop/azure-trusted-signing.json`. Then `npm run dist:signed`. Do **not** create
  the Artifact Signing account until ready to sign that same month ($9.99, not pro-rated).
- Run the **signed** Electron installer on an independently preflighted clean Windows 10/11 x64
  VM with `scripts/verify-clean-machine.ps1 -ShowAppWindow -RequireAuthenticode`; copy only the
  Setup EXE and that script, never a checkout. SEGOPC / BEETHOVEN / LIVPHI cannot be that host.
- Create PayPal production credentials, accept processor terms, configure webhook secrets, set refund/
  tax/support policy, and activate protected versioned fulfilment only after the release gate passes.
- Production PyPI remains intentionally out of scope for the customer-facing desktop route.
- LIVPHI `git` share stays denied. Source mirror is `\\LIVPHI\Github\pdf-designer` (done 2026-08-24).

## Next-agent handoff

Continue only the remaining release gates. Preserve all current uncommitted work from other agents.
Do not activate checkout, paid-download, account, cloud, updater, or second-renderer behavior.
LIVPHI source mirror is `\\LIVPHI\Github\pdf-designer`. After the human
provisions Azure Trusted Signing, rebuild with `npm run dist:signed` and prove it on a separately
provisioned clean Windows 10/11 x64 VM using `scripts/verify-clean-machine.ps1 -ShowAppWindow -RequireAuthenticode`
(or `-BundledRuntimeProof -RequireAuthenticode` on this LAN until a spare VM exists).
The unsigned 0.1.0 NSIS file is never listable. Revisit the $5 direct PayPal / $6 Gumroad channel
policy and the prepared product-widget contract only after those gates and an explicit release decision.
