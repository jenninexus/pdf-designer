# Windows Electron installer

Pre-release **contributor** notes for the thin Windows shell. This is not a
customer download page. Public product story: [`PRODUCT.md`](PRODUCT.md).
Maintainer signing and LAN proof stay local (`WINDOWS-ELECTRON.local.md`).

## One engine, two local processes

```
PDF Designer.exe (Electron window; no renderer APIs)
  └─ pdf-designer-runtime.exe (one local child)
       └─ pdf_tool.preview on http://127.0.0.1:<ephemeral-port>/
            └─ existing Playwright Chromium PDF renderer
```

Electron provides only the native Windows window, first-run workspace seed,
and child-process lifecycle. It never calls Electron PDF printing APIs and
never introduces another HTML-to-PDF renderer.

The first run copies the public, Git-tracked Jane Example seed into
`Documents/PDF Designer` only when that directory does not exist. Later runs
never merge, overwrite, sync, or delete that workspace. The installer/uninstaller
must not remove a user's vaults, resumes, palettes, or exports.

## Local unsigned dist (packaging only)

From `desktop/` in a Windows checkout:

```powershell
npm ci
npm run dist
pwsh -NoProfile -File ..\scripts\verify-authenticode.ps1 `
  -InstallerPath .\dist\PDF-Designer-Setup-0.1.0.exe
```

`CSC_IDENTITY_AUTO_DISCOVERY=false` stops a random cert in Windows from stamping
the file by accident. Default `npm run dist` is **unsigned**. Windows SmartScreen
warnings on that artifact are expected. Do not treat it as a customer download.

A signed maintainer build is a separate local command (`npm run dist:signed`) that
fails closed without gitignored credentials. The gate is
`scripts/verify-authenticode.ps1 -RequireSigned` printing Valid — not
electron-builder’s `signing with signtool.exe` log.

## Why the clean-machine harness refuses Python / Node / a checkout

`scripts/verify-clean-machine.ps1` is not “run the installer on a machine that
already develops this repo.” It proves a **PC with none of the toolchain** can
still install, export Jane Example light+dark, and keep `Documents\PDF Designer`
after uninstall. The packaged app ships its own Python runtime + Playwright
Chromium. If the test box already has `python`, `py`, `node`, `npm`, or this
repo, a bug that accidentally shells out to PATH would still pass — a false
ship gate.

A same-network PC that already has the repo is a **source mirror**, not listing
proof. Closest packaging rehearsal without a spare VM:

```powershell
# Outside any git checkout
pwsh -NoProfile -ExecutionPolicy Bypass -File .\verify-clean-machine.ps1 `
  -InstallerPath .\PDF-Designer-Setup-<version>.exe `
  -BundledRuntimeProof
```

That still installs, proves `pdf-designer-runtime.exe` came from the install
folder (not PATH Python), exports Jane light+dark, uninstalls, and keeps the
workspace. It is **not** a listing gate. A listable build also needs
`-RequireAuthenticode`.

Do not add `-SkipToolchainCheck`. `-BundledRuntimeProof` is the named substitute
when no spare clean user/VM exists.

Hidden-window `CloseMainWindow()` is often false for this Electron host; the
harness `Stop-Process`es the Electron PID and still asserts runtime death.

## First launch: what a standalone user sees

1. Install the per-user Windows app, then open **PDF Designer** from Start Menu or the
   desktop shortcut. No checkout, Node, or system Python is required by the packaged app.
2. On a genuinely new workspace, the app copies the public fictional Jane Example to
   `Documents\PDF Designer`; it never overwrites an existing folder.
3. The window always opens the Hub title screen. It stays until **Open**, **Start
   wizard**, Enter, or Escape (no auto-dismiss). After that, the local Design Hub is in its
   dark-default workspace chrome. Choose **Start wizard** (or **Wizard** in the header) for
   the guided route: local vault → source-backed skills → palette → light and dark export.
   The document's own palette is independent of the Hub theme.
4. Jane Example is a clearly labelled fictional template. The guided path creates no
   account, cloud connection, claim, or automatic submission. It uses the bundled local
   Hub and the existing Playwright renderer only.
5. Keep the `Documents\PDF Designer` folder when uninstalling. The uninstaller removes the
   application, not the person's vaults, resumes, palettes, or exports.

This describes the intended customer path, not current release eligibility.

## Redirected Documents / OneDrive (decision)

**Policy: follow Windows Documents, including Known Folder Move.**

PDF Designer seeds and opens `Documents\PDF Designer`. It does not create a
Microsoft / OneDrive / Dropbox / iCloud account, and it does not relocate the
workspace to `%LOCALAPPDATA%` when Documents is redirected.

If Windows Documents is already redirected (OneDrive or similar), first-run
creates `Documents\PDF Designer` there. That provider may sync it. The Hub still
binds only to `127.0.0.1`.

Why not force a local-only folder:

- The advertised path is `Documents\PDF Designer`. Silently moving it would
  orphan an existing Jane Example workspace and break the clean-machine harness,
  which uses `[Environment]::GetFolderPath("MyDocuments")`.
- People who turned on Known Folder Move expect Documents to be the canonical
  place. Fighting that is more surprising than documenting it.

What to tell a user who wants a strictly local vault: in the sync client, stop
backing up the `PDF Designer` folder (or Documents), or set Documents to a local
path in Windows. The app will follow whatever Windows reports as Documents on the
next launch; it still never merges or overwrites an existing folder.

The shell logs a warning when the Documents path looks redirected (`OneDrive`,
`Dropbox`, `iCloud`, `Google Drive`). It does not change the path.

## Security and local-data boundary

- Windows 10/11 x64 only; assisted per-user NSIS install with Start Menu and desktop shortcuts.
- Electron uses `contextIsolation: true`, `nodeIntegration: false`, and `sandbox: true`.
- The renderer has no preload bridge, remote content, auto-updater, telemetry, account flow, or cloud sync.
- The runtime is bound to `127.0.0.1` on an ephemeral port. Electron accepts only the exact port written to its local ready file and blocks new windows/navigation elsewhere.
- The bundled Python runtime gives Playwright the adjacent, bundled Chromium executable explicitly. It does not need a user environment variable, system Python, or a second renderer.

### Local-process and Documents boundary

`127.0.0.1` prevents network access; it is not an authentication boundary
between processes running as the same Windows user. A same-user local process
that learns the ephemeral port can reach the Hub just as it can reach other
user-owned local files. This is the intentional local trust model for v1, not a
claim of secrecy from malware or other same-user processes.

## Build and local verification

From a Windows checkout with Python and Node available:

```powershell
Set-Location desktop
npm ci
npm run pack       # ignored unpacked application artifact
npm run dist       # ignored unsigned PDF-Designer-Setup-<version>.exe
```

`runtime` first creates an ignored PyInstaller sidecar and copies the existing
Playwright Chromium plus a seed generated only from Git-tracked public files.
`verify-shell` asserts the security/lifecycle/NSIS contract before packaging.
The build deliberately has no publishing configuration.

For a real clean-target test, copy the installer and the standalone companion
script (not a checkout) to the test machine, then run:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File .\verify-clean-machine.ps1 `
  -InstallerPath .\PDF-Designer-Setup-0.1.0.exe -ShowAppWindow
```

The companion refuses a contaminated target, uses only Jane Example plus a
clearly labelled fictional release-test vault, verifies light and dark exports,
and proves the workspace remains after uninstall. `-ShowAppWindow` leaves the
window visible for UI observation; omit it only for non-visual automation.
Add `-RequireAuthenticode` only on a signed build.
