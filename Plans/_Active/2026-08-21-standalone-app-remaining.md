# Active plan — Standalone app release path

**Date:** 2026-08-21 · **Host:** SEGOPC · **Status:** core toolkit shipped; distribution and desktop shell remain.

This is the one active plan. It replaces the completed launch handoffs in
[`../_Complete/2026-08-17-early-release-remaining.md`](../_Complete/2026-08-17-early-release-remaining.md)
and
[`../_Complete/2026-08-20-pdf-designer-remaining-sisters/Plan.md`](../_Complete/2026-08-20-pdf-designer-remaining-sisters/Plan.md).

## Honest completion picture

| Surface | Status | Evidence / boundary |
|---|---|---|
| Local-first engine + Design Hub | **Shipped** | HTML→PDF, variants, collage, vault/ATS/palette/overflow guards, public examples, and the localhost Hub are in `main`. |
| Public GitHub clone experience | **Shipped, regression-gated** | `scripts/smoke-white-label.py` passed 2026-08-21: public-only QA, light/dark export, and ATS parsing. |
| Installable Python package | **TestPyPI proved** | Wheel assets, upload, fresh TestPyPI install, and packaged `check_generation` passed 2026-08-21. |
| Public product record | **Shipped** | Public GitHub clone, clone-safe Hub examples, and the blog walkthrough exist. Social publication records are owned by `C:\Github\socials\Plans\_ACTIVE\2026-08-10-jn-agency-socials-sequence\Plan.md`, not this engineering plan. |
| Paid standalone desktop app | **Pre-release installer built locally** | The launcher plus a local Design Hub vault → skills → palette → light/dark walkthrough exist. A Windows x64 Electron/NSIS installer is built and runtime-tested locally; clean-machine GUI/install and signing remain separate gates. |

Do not turn these rows into invented percentages. The core can be used standalone from a clone today;
the non-developer desktop product is a separate, unstarted implementation phase.

## Public examples and privacy boundary

- [x] Keep the fictional Jane Example cards (`users/examples.json`, `vaults/examples.json`,
  `profiles/examples.json`) tracked so a fresh clone and the Hub demonstrate every document kind.
- [x] Replace the broad `_job-apps/_template/` smoke exception with named public seeds; remove the
  provider-specific material from the public tree. Real listings, provider records, names, phone numbers,
  and submission evidence remain local only.
- [x] Make `users/<you>.json#characterVoice` the one person-level voice-design area in the public
  seed; the vault is the sole application-prose layer and profiles only point at it.
- [x] New public Hub feature: `Start` uses the fictional Jane Example export path and is covered by `tests/test_wizard.py` (2026-08-21).

## Responsive Hub contract

- [x] Confirm the shared numeric scale comes from `www-theme-kit/scss/_breakpoint-tokens.scss`,
  while `src/pdf_tool/static/hub.css` owns this app's breakpoint and nav-switch behavior. The MCP
  breakpoint file is a cache/index only.
- [x] At the drawer switch, hide empty desktop groups and their divider borders; keep refresh/close
  compact; make drawer and search dismiss on outside click as well as Escape.
- [x] Visual/regression check the Hub (`/`, `/recipes`, `/vault`) at 390, 576, 768, 992, 1200, 1400,
  and 1920px against `www-theme-kit/profiles/pdf-designer.json` (2026-08-21). Fixed document-root
  overflow from the closed drawer and restored the 768px desktop hamburger boundary.
- [x] Replace the compact top-right menu glyph with Font Awesome Free 6.7.2 `bars-staggered` across
  Library, Recipes, and Vault (2026-08-21). The local SVG keeps the control offline and visually
  distinct from the drawer's close action.

## Distribution — optional, not a blocker for the clone product

- [x] Public-source smoke and local wheel gates exist.
- [x] TestPyPI: `pdf-designer 0.4.0` uploaded and passed the fresh-install + packaged `check_generation` proof on 2026-08-21.
- [x] Production-PyPI decision: do **not** publish now. TestPyPI remains the developer-package proof; the Windows installer is the intended customer install path.

## Paid desktop shell — Windows Electron delivery

- [x] Owner decision (2026-08-21): support **Windows 10/11 x64** first, delivered as a per-user NSIS installer. Electron is a thin desktop host over the existing local `pdf_tool.preview` service; it is never a second document renderer.
- [x] Write a small acceptance spec for the first launcher: starts the existing Hub on localhost, opens the browser, and leaves all vault data local. See [`docs/WINDOWS-LAUNCHER.md`](../../docs/WINDOWS-LAUNCHER.md).
- [x] Build and test the Windows launcher spike without forking the renderer or introducing a cloud account.
- [x] Add the smallest guided vault → skills → palette → light/dark export wizard after the launcher proof: [`/wizard`](http://127.0.0.1:8787/wizard) keeps input in local ignored templates and proves dual export with fictional Jane Example through the existing Library renderer (2026-08-21).
- [x] Build the Windows Electron NSIS installer: bundle only the Python/Playwright runtime it needs, start one ephemeral loopback Hub child, and show that route in a sandboxed Electron window. Static shell checks, frozen-runtime export, unpacked-resource inspection, and local NSIS build passed (2026-08-21).
- [ ] Run the installer and Electron window on a clean Windows 10/11 x64 machine, including observing that Electron terminates only its own loopback child on exit.
- [ ] Keep a paid listing blocked until the installer has a real, tested no-Python user path and a signed-binary decision.
- [x] Owner direction (2026-08-21): the future Jenninexus `/products` card will use **PayPal**; page, payment, receipt/tax/refund policy, and secure versioned fulfilment are intentionally a later human-owned external action.
- [x] Define the optional Voice Seed handoff contract in [`docs/VOICE-SEED-HANDOFF.md`](../../docs/VOICE-SEED-HANDOFF.md): create/import a user's own public-safe voice card only after local `characterVoice` + vault `voice` are set. It remains optional, never copies private vault claims or contacts, and never adds Voice Seed as a renderer dependency.

## Guardrails

- Never post, deploy, or use `--post` without explicit human authorization.
- Never auto-submit applications or commit private vaults, job listings, brands, PDFs, or bare commands.
- Launch media uses only public Jennifer Nexus / Jane Example assets — never real vaults, résumés, listings, or brand hex.
- The desktop shell starts the existing `pdf_tool.preview`; it does not reimplement HTML/PDF rendering.

## Verification record

Run before declaring the public toolkit healthy after engine or packaging changes:

```powershell
python scripts/smoke-white-label.py
python scripts/check-wheel-assets.py
python scripts/testpypi-dry-run.py
```

Related: [`../../docs/PRODUCT.md`](../../docs/PRODUCT.md) ·
[`../../docs/PACKAGING.md`](../../docs/PACKAGING.md) ·
[`../../docs/PREVIEWER.md`](../../docs/PREVIEWER.md).

## Autonomous completion run — 2026-08-21

### Done when

- [x] The production-PyPI decision is documented: **do not publish to production PyPI now**. TestPyPI remains the proven developer-package rehearsal; the Windows customer route is an Electron NSIS installer, and production PyPI would add public Python-package support obligations without completing that route.
- [x] A Windows launcher starts the existing local Hub, opens the browser, and keeps all data local. Acceptance record: [`docs/WINDOWS-LAUNCHER.md`](../../docs/WINDOWS-LAUNCHER.md).
- [x] A guided local wizard covers vault → skills → palette → dual export without a second renderer (Jane Example public proof; `/wizard`).
- [x] The optional Voice Seed flow presents a redacted, read-only card preview and never needs a network dependency (`/wizard` → `/api/voice-card`, 2026-08-21). Saving/copying a human-approved card remains deliberately out of scope.
- [x] A Windows x64 Electron NSIS artifact is built with an isolated bundled Hub runtime, public workspace seed, and only the existing Playwright renderer; the frozen runtime made an actual light PDF export without a system Python interpreter (2026-08-21).
- [ ] A clean Windows 10/11 x64 GUI/install test observes the Electron host launch the artifact and clean up only its own child process on exit.
- [ ] The changed surfaces have automated and observable verification, then are committed and pushed as authorized. The 2026-08-21 status audit found 14 existing release commits ahead of the public `origin/main`; publishing remains an explicit authorization gate.

### Task checklist

- [x] Audit existing launcher, installer, wizard, and release mechanisms.
- [x] Implement the smallest Windows distribution path around `pdf_tool.preview` (`scripts/launch-design-hub.ps1`).
- [x] Implement the guided local wizard.
- [x] Implement the bounded optional Voice Seed preview handoff (separate from the local wizard; no save/copy action).
- [x] Record the Windows/Electron delivery and no-production-PyPI decisions from local product and Electron references.
- [x] Implement the Electron main/package and a reproducible bundled Python/Playwright runtime build. The shell has no preload capabilities and uses the existing local renderer only.
- [x] Build and inspect the unsigned Windows NSIS artifact locally (`desktop/dist/PDF-Designer-Setup-0.1.0.exe`, 368,302,759 bytes); a clean-machine install remains a later external-machine validation.
- [x] Verify the distribution and wizard paths; update release docs and plan (84 pytest, white-label QA/light/dark/ATS, wheel asset gate, and fresh local `/wizard` response, 2026-08-21).
- [ ] Obtain explicit publish authorization, then push all committed in-scope paths to the verified public `origin/main` and confirm the remote tip.

### Assumptions

- The first paid-shell target is Windows, because this is the requested platform and the active work occurs on Windows.
- Production PyPI is deferred unless an existing production credential and public-release gate make publication independently verifiable; TestPyPI remains the proved distribution rehearsal.
- The wizard is a Design Hub surface over existing local data and renderer commands, never a new renderer or cloud account.
- Private free-form voice text is not heuristically redacted in a browser preview. The current local profile card is deliberately skeletal until a human-approved editor/write flow exists; fictional Jane Example demonstrates the populated public shape.
- Windows 10/11 x64 is the sole v1 desktop target. NSIS per-user install was chosen over Microsoft Store/MSIX and a web installer because it is the most conventional, reversible local-first Windows package; reconsider only after code signing, support volume, or Store policy makes another channel materially better.
- Production PyPI remains intentionally unpublished. The TestPyPI proof is sufficient for developer packaging; it does not replace the no-Python desktop product path.
- Electron may host the loopback Hub but must use `contextIsolation: true`, `nodeIntegration: false`, `sandbox: true`, strict loopback navigation, no preload capabilities, no auto-updater, and no remote content.

### Evidence

- VERIFIED — 2026-08-21 TestPyPI uploaded `pdf-designer 0.4.0`, fresh-installed it outside the checkout, and passed the packaged `check_generation` gate.
- VERIFIED — 2026-08-21 `/wizard` serves locally, has focused coverage, and the fictional Jane Example path passes vault validation, generation QA, dual PDF export, and ATS parsing through the existing engine.
- VERIFIED — 2026-08-21 `/api/voice-card` emits only a constrained redacted schema, defaults to fictional Jane Example, and the wizard presents it without any write, account, sync, or renderer dependency. Independent re-review passed; 86 pytest plus white-label QA/light/dark/ATS and wheel asset gates passed; fresh loopback API and wizard checks passed on :8793.
- VERIFIED — 2026-08-21 local Electron references (`Synagen.Engine.Desktop`, `Syqo`, and `martian-portal`) and current Electron/electron-builder primary documentation support a per-user x64 NSIS wrapper with one loopback child, sandboxed renderer, and no updater. `www-theme-kit/profiles/pdf-designer.json` already matches the Hub's existing responsive/local-only contract; no `syna-theme-kit` profile is warranted for the thin host.
- VERIFIED — 2026-08-21 `desktop/scripts/build-runtime.ps1` built a PyInstaller one-directory runtime with an explicitly bundled Playwright Chromium. The frozen sidecar produced a real Jane Example light PDF with no system Python, `node desktop/scripts/verify-shell.cjs` passed, `npm run pack` verified both runtime and public workspace seed in the unpacked Electron resources, and `npm run dist` produced the 368,302,759-byte per-user x64 NSIS executable. `Get-AuthenticodeSignature` reports `NotSigned` as expected for this local pre-release.
- UNVERIFIED — The GUI Electron window and NSIS install/uninstall have not been run because this developer machine is not a clean target and this run avoids opening a visible desktop window. A Windows 10/11 x64 clean-machine run must prove first-run seed copy, navigation, child-process cleanup, uninstall behavior, and SmartScreen/signing decisions.

### Deferred

- Production PyPI publication itself is outward-facing and remains separate from the reversible production-PyPI decision unless its release conditions are fully met.
- PayPal product-page publication, payment processing, tax/receipt/refund policy, secure download fulfilment, code signing, and a clean-machine install test require later explicit human-owned actions. No checkout or public-page change is part of this engineering run.

## Clean-machine validation run — 2026-08-21

### Done when

- [ ] The unsigned installer is observed on a genuinely clean Windows 10/11 x64 target: no checkout, Python, Node, or existing `Documents\\PDF Designer` before the test.
- [ ] First run creates only the public Jane Example seed; a clearly labelled fictional release-test vault can be created locally; existing-engine light and dark exports succeed.
- [ ] Closing the Electron window removes only the runtime process tree it created; uninstall preserves `Documents\\PDF Designer` and its release-test files.
- [ ] The release privacy wording has an explicit policy for Windows Documents redirection (for example OneDrive), and treats same-user local processes as in-scope to the loopback threat model.

### Task checklist

- [x] Preflight available local/network targets without changing them. SEGOPC is contaminated by the checkout, Python, and Node; BEETHOVEN has no PDF Designer checkout/workspace but has Python and Node; LIVPHI cannot be authenticated for its preflight; no local Hyper-V VM is present.
- [x] Add `scripts/verify-clean-machine.ps1`, a standalone clean-target companion that refuses contamination and automates install, visible-app option, Jane seed, fictional test vault, light/dark export, graceful close, uninstall, and preservation assertions. Its PowerShell parser/static contract tests pass locally; it has not been run against an installer here.
- [ ] **BLOCKED — external clean target required.** Obtain a clean Windows 10/11 x64 VM or physical target, or authenticated access that proves a target meets the preflight. Do not use a shared development/media machine merely because it is reachable.
- [ ] Transfer only the installer plus the standalone verification companion—never a source checkout—and run the full install/launch/export/close/uninstall observation.
- [ ] Record observed process IDs/paths, export paths, and post-uninstall workspace existence; do not treat a build or source review as a substitute.
- [ ] Decide whether Documents redirected by the operating system is acceptable for private vaults, or change the documented workspace policy before public release.
- [x] Document the same-user loopback and Documents-redirection boundaries in [`docs/WINDOWS-ELECTRON.md`](../../docs/WINDOWS-ELECTRON.md); the owner decision remains open.

### Assumptions

- A Windows Sandbox or new VM is the most reversible clean target. This host has no enumerated Hyper-V VM and its Sandbox executable is absent; enabling or provisioning either is a separate machine-configuration action.
- BEETHOVEN and LIVPHI remain out of scope as test targets until independently proven clean and safe to disturb. Their network reachability is not evidence that they meet the no-Python/no-Node requirement.

### Evidence

- VERIFIED — read-only preflight: BEETHOVEN and LIVPHI respond to ping/SMB, but PowerShell remoting is not trusted. BEETHOVEN's accessible filesystem shows no checkout, while independent SSH inspection found Python/Node; it is disqualified. LIVPHI authentication fails, so its state is unverified. Local `Get-VM` returned no VMs under elevation; SEGOPC is Windows 11 Pro x64 but has the checkout, Python, and Node.
- UNVERIFIED — no genuinely clean Windows target is presently available, so no installer, GUI, seed, export, shutdown, or uninstall observation has been made in the required environment.
- BLOCKED — after the third consecutive clean-target audit, the standalone harness was run only through its non-destructive preflight on SEGOPC and exited `1` before installation: `Clean-target preflight failed: checkout exists at C:\\Github\\pdf-designer`. No runtime process was present afterward. This confirms the gate, not the installer behavior.
- VERIFIED — `tests/test_clean_machine_script.py` parses the standalone PowerShell companion and asserts its contamination checks plus install/seed/export/shutdown/uninstall contract (2 passed, 2026-08-21). This is a reproducible test procedure, not target-environment proof.
- REVIEW FINDING — the current Documents workspace can be redirected by Windows/OneDrive, and the unauthenticated loopback Hub is accessible to same-user local processes that learn the ephemeral port. The app adds no cloud service and binds no network interface, but product wording must state these operating-system/local-user boundaries before release.

### Deferred

- Provisioning a new VM/Sandbox, enabling optional Windows features, changing remote credentials/TrustedHosts, or altering another machine's configuration is intentionally not performed by this run.
