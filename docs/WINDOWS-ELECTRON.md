# Windows Electron installer

**Status (2026-08-21):** the local build produces an unsigned, per-user x64
NSIS installer. It is a packaging artifact—not a public download or paid
listing. A clean-machine install and code-signing decision remain release
gates.

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

## First launch: what a standalone user sees

1. Install the per-user Windows app, then open **PDF Designer** from Start Menu or the
   desktop shortcut. No checkout, Node, or system Python is required by the packaged app.
2. On a genuinely new workspace, the app copies the public fictional Jane Example to
   `Documents\PDF Designer`; it never overwrites an existing folder.
3. The local Design Hub opens in its dark-default workspace chrome. Choose **Start** for
   the guided route: local vault → source-backed skills → palette → light and dark export.
   The document's own palette is independent of the Hub theme.
4. Jane Example is a clearly labelled fictional template. The guided path creates no
   account, cloud connection, claim, or automatic submission. It uses the bundled local
   Hub and the existing Playwright renderer only.
5. Keep the `Documents\PDF Designer` folder when uninstalling. The uninstaller removes the
   application, not the person's vaults, resumes, palettes, or exports.

This describes the intended customer path, not current release eligibility. The present
artifact is unsigned and has not yet passed the clean-machine Windows validation below.

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

The default workspace follows Windows `Documents`. If the operating system or
the user's policy redirects Documents to OneDrive or another sync provider,
that provider can sync the workspace even though PDF Designer creates no cloud
account or network connection. Before a public release, choose and document
whether redirected Documents is supported or require a clearly local workspace.

## Build and local verification

From a Windows checkout with Python and Node available:

```powershell
Set-Location C:\Github\pdf-designer\desktop
npm ci
npm run pack       # ignored unpacked application artifact
npm run dist       # ignored PDF-Designer-Setup-<version>.exe
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
window visible for the required UI/navigation observation; omit it only for
non-visual automation.

Before any public release, verify the NSIS installer on a Windows machine that
has no checkout, Python, or Node; create and preserve a local vault; export
light and dark PDFs; uninstall; and confirm the workspace remains. Sign the
installer before asking ordinary users to download it—SmartScreen warnings on
the current unsigned artifact are expected and are not an acceptable customer
workflow.
