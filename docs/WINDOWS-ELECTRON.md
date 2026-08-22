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

## Security and local-data boundary

- Windows 10/11 x64 only; assisted per-user NSIS install with Start Menu and desktop shortcuts.
- Electron uses `contextIsolation: true`, `nodeIntegration: false`, and `sandbox: true`.
- The renderer has no preload bridge, remote content, auto-updater, telemetry, account flow, or cloud sync.
- The runtime is bound to `127.0.0.1` on an ephemeral port. Electron accepts only the exact port written to its local ready file and blocks new windows/navigation elsewhere.
- The bundled Python runtime gives Playwright the adjacent, bundled Chromium executable explicitly. It does not need a user environment variable, system Python, or a second renderer.

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

Before any public release, verify the NSIS installer on a Windows machine that
has no checkout, Python, or Node; create and preserve a local vault; export
light and dark PDFs; uninstall; and confirm the workspace remains. Sign the
installer before asking ordinary users to download it—SmartScreen warnings on
the current unsigned artifact are expected and are not an acceptable customer
workflow.
