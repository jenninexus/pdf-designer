# PDF Designer desktop shell

This folder builds the thin Windows application host for PDF Designer. Electron supplies only the local application window. The bundled `pdf-designer-runtime.exe` starts the existing local Python service, which continues to own all HTML-to-PDF work through its existing Playwright/Chromium renderer. This shell does not add a renderer.

## Build contract

The packaged runtime is built by this shell and must produce `desktop/runtime/pdf-designer-runtime/pdf-designer-runtime.exe` plus its copied Playwright browser. Then, from this directory:

```powershell
npm ci
npm run dist
```

`npm run runtime` runs the reproducible sidecar build by itself; `pack` and
`dist` run it first. The build downloads Electron, PyInstaller, Python package
dependencies, and Playwright Chromium into ignored build folders. The installed
application itself uses no accounts, cloud resources, secrets, or user-set
environment variables.

`npm run pack` creates an unpacked x64 Windows app for local packaging checks. `npm run dist` creates the assisted, per-user x64 NSIS installer named `PDF-Designer-Setup-<version>.exe`. Publishing is explicitly disabled; this project has no auto-update mechanism and no cloud release configuration.

The first app run copies `workspace-seed/` to `Documents/PDF Designer` only if that folder does not already exist. Existing workspace data is never overwritten or merged. If Windows redirects Documents to OneDrive or another sync provider, that provider may sync the folder; PDF Designer still does not create a cloud account. The desktop window may navigate only to the exact local loopback URL written by the runtime; it has no preload API, remote content, account flow, telemetry, or synchronization. Each launch forces the Hub title screen (`?splash=1`).

## Signing

Default `npm run dist` is unsigned on purpose (`CSC_IDENTITY_AUTO_DISCOVERY=false`).
Windows SmartScreen warnings are expected for those test builds. Do not treat the
unsigned artifact as a customer download.

A listable build is a separate local maintainer command (`npm run dist:signed`) that
fails closed without gitignored credentials, then
`scripts/verify-authenticode.ps1 -RequireSigned` must exit 0. Details:
[`docs/WINDOWS-ELECTRON.md`](../docs/WINDOWS-ELECTRON.md).
