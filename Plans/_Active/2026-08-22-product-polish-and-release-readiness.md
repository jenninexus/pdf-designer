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
      route. A clean-machine Electron GUI/install test is explicitly deferred for the owner tomorrow.
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

- [ ] Mirror the local PDF Designer repository to LIVPHI's `C:\Github\pdf-designer` without copying
      ignored private workspace data, credentials, Electron runtime, or installer artifacts.
- [ ] Inspect the LIVPHI mirror and record its suitable role: source/docs mirror only, not proof of the
      clean-machine release gate until its preflight is explicitly passed.
- [x] BEETHOVEN `C:\p\pdf-designer` fast-forwarded to GitHub `829e0ca` (2026-08-22). Source/docs only —
      not a clean-machine proof host (Python/Node + checkout present).
- [x] Carry forward the only release blockers: clean Windows 10/11 x64 install/GUI/process-cleanup test,
      signing decision, and human-owned PayPal production/fulfilment policy.

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
- UNVERIFIED — clean-machine Windows installer GUI, lifecycle, uninstall, and signing behavior.
- VERIFIED — public-only QA workspace captured Library, Recipes, Vault, and Start at 390, 576, 768,
  992, 1200, 1400, and 1920px; 91 source tests passed.
- BLOCKED — LIVPHI answered ping and SMB tests. It advertises a `git` share but denies access to it; only
  unrelated non-admin shares are currently readable. Its administrative share denied access, WinRM is not
  trusted, and SSH has no approved non-interactive credential. Do not relax those controls merely to copy
  this repo; wait for an approved authenticated share or remote account that maps to `C:\Github`.
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

- Run the Electron installer and visible app on an independently preflighted clean Windows 10/11 x64
  machine tomorrow; use `scripts/verify-clean-machine.ps1` with the installer only, never a checkout.
- Create PayPal production credentials, accept processor terms, configure webhook secrets, set refund/
  tax/support policy, and activate protected versioned fulfilment only after the release gate passes.
- Production PyPI remains intentionally out of scope for the customer-facing desktop route.

## Next-agent handoff

Continue only the remaining release gates. Preserve all current uncommitted work from other agents.
Do not activate checkout, paid-download, account, cloud, updater, or second-renderer behavior. First obtain
an approved authenticated LIVPHI source-copy route (or leave that task blocked), then use a separately
provisioned clean Windows 10/11 x64 target for `scripts/verify-clean-machine.ps1 -ShowAppWindow`. Record
only observed installer, Electron lifecycle, export, uninstall, and signing evidence. Revisit the $5 direct
PayPal / $6 Gumroad channel policy and the prepared product-widget contract only after those gates and an
explicit release decision.
