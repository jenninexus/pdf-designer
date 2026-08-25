# Windows Electron installer

**Status (2026-08-25):** **Hold Azure Trusted Signing this month** (no Artifact
Signing account → no $9.99). Unsigned NSIS is still **not listable**. Money /
channel comparison (PayPal · Gumroad · Microsoft Store · Copilot):
[`PRODUCT.md`](PRODUCT.md) § Paying for PDF Designer. Authenticode path when
budget allows: Azure Trusted Signing (not Syn Themes `VSCE_PAT`). SEGOPC
Documents is OneDrive. Closest installer proof is `-BundledRuntimeProof`, not a
clean VM. LIVPHI source mirror is `\\LIVPHI\Github`.

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

## How to get a signed installer you can put on Gumroad

Windows will warn “Unknown publisher” on an unsigned `.exe`. A **signed** installer
means Microsoft can see a real publisher name on the file (Authenticode). That is
a stamp on the EXE, not a website login.

**Syn Themes / VS Code publish cannot do this.** `C:\Github\syn-themes` uses
`VSCE_PAT` and `OVSX_PAT` to upload a `.vsix` theme to the Marketplace. Those
tokens are like “password to the store.” They cannot stamp a Windows installer.
There is no Azure Trusted Signing account, tenant, or code-signing certificate
in that repo or in the current user env (`AZURE_TENANT_ID` is empty).

**What `verify-authenticode.ps1` is:** a checker. It asks Windows
“does this file have a Valid publisher stamp?” Unsigned files print `NotSigned`
and a warning that they are **not listable**. That is the gate. electron-builder
may still log `signing with signtool.exe` while building; ignore that log unless
this script prints `PASS: Authenticode signature is Valid.`

### You do this once (portal; needs your Microsoft ID)

Sign in as the **dev publisher** used for Syn Themes: `jenninexus2.0@gmail.com`
(not `jenninexus@gmail.com`).

1. Azure subscription (free trial or pay-as-you-go) at [portal.azure.com](https://portal.azure.com).
2. Create **Azure Trusted Signing** in one region (East US is fine).
   Overview: https://learn.microsoft.com/en-us/azure/trusted-signing/quickstart
3. **Identity validation** — Microsoft checks that you are JenniNexus / the LLC.
   This step is you + ID documents; an agent cannot finish it. Wait until it is Approved.
4. Create a **Public Trust** certificate profile.
5. Entra ID → App registration → give it role **Trusted Signing Certificate Profile Signer**.
   Create a client secret. Put these three in Windows User env (or sys-admin), never git:
   `AZURE_TENANT_ID`, `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET`.
6. Copy `desktop/azure-trusted-signing.example.json` → `desktop/azure-trusted-signing.json`
   (gitignored). Fill the account name, profile name, and publisher name so they match
   what Azure issued. Leave `REPLACE_WITH_…` and the command will refuse to run.

Then, from `desktop/`:

```powershell
npm run dist:signed
```

When that exits 0, `scripts/verify-authenticode.ps1 -RequireSigned` has already passed.
**That** EXE is the Gumroad / later JN `$5` file. Until then, do not upload
`PDF-Designer-Setup-0.1.0.exe`.

Stay on electron-builder 26.15.3. Do not buy a USB OV/EV token for v1.

### Local unsigned dist (packaging only)

```powershell
Set-Location C:\Github\pdf-designer\desktop
npm ci
npm run dist
pwsh -NoProfile -File ..\scripts\verify-authenticode.ps1 `
  -InstallerPath .\dist\PDF-Designer-Setup-0.1.0.exe
```

`CSC_IDENTITY_AUTO_DISCOVERY=false` stops a random cert in Windows from stamping
the file by accident. Expected result today: `NotSigned` / not listable.

## Why the clean-machine harness refuses Python / Node / a checkout

`scripts/verify-clean-machine.ps1` is not “run the installer somewhere on the
LAN.” It proves a **customer PC with none of our toolchain** can still install,
export Jane Example light+dark, and keep `Documents\PDF Designer` after
uninstall. The packaged app ships its own Python runtime + Playwright Chromium.
If the test box already has `python`, `py`, `node`, `npm`, or this repo, a bug
that accidentally shells out to PATH would still pass — a false ship gate.

| Host | Role | Clean-machine proof? |
|---|---|---|
| SEGOPC | Daily driver + source | No — checkout + toolchain |
| BEETHOVEN `C:\p\pdf-designer` | Source/docs mirror | No — Python, Node, and a checkout |
| LIVPHI `\\LIVPHI\Github` | Source/docs mirror (writable). `\\LIVPHI\git` is access-denied | No — toolchain expected |
| Fresh Win10/11 x64 VM or spare user profile | Installer proof host | **Yes**, after preflight |

This LAN has no spare clean VM: SEGOPC, BEETHOVEN, and LIVPHI all carry Python/Node.
The closest completed proof is therefore:

```powershell
# Outside any git checkout — e.g. C:\pdf-designer-installer-drop\
pwsh -NoProfile -ExecutionPolicy Bypass -File .\verify-clean-machine.ps1 `
  -InstallerPath .\PDF-Designer-Setup-<version>.exe `
  -BundledRuntimeProof
```

That still installs, proves `pdf-designer-runtime.exe` came from the install
folder (not PATH Python), exports Jane light+dark, uninstalls, and keeps the
workspace. It is **not** a listing gate. Listing still needs `-RequireAuthenticode`
on a signed EXE (clean VM preferred; BundledRuntimeProof is acceptable on this
network until a spare user/VM exists).

**Observed (2026-08-24, SEGOPC):** drop folder `C:\pdf-designer-installer-drop\`,
flags `-BundledRuntimeProof -AllowExistingWorkspace`. Runtime path was the
install dir sidecar. Workspace was
`<user-home>\OneDrive\Documents\PDF Designer`. Light + dark Jane PDFs wrote
under `release-test-exports\`. Uninstall kept the workspace. Hidden-window
`CloseMainWindow()` is false; the harness now `Stop-Process`es the Electron PID
and still asserts runtime death. Authenticode remained `NotSigned`.

Do not add `-SkipToolchainCheck`. `-BundledRuntimeProof` is the named substitute.

Listing proof adds Authenticode:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File .\verify-clean-machine.ps1 `
  -InstallerPath .\PDF-Designer-Setup-<version>.exe `
  -ShowAppWindow `
  -RequireAuthenticode
```

Omit `-RequireAuthenticode` only when rehearsing an unsigned packaging build.
That rehearsal still cannot be listed.

## First launch: what a standalone user sees

1. Install the per-user Windows app, then open **PDF Designer** from Start Menu or the
   desktop shortcut. No checkout, Node, or system Python is required by the packaged app.
2. On a genuinely new workspace, the app copies the public fictional Jane Example to
   `Documents\PDF Designer`; it never overwrites an existing folder.
3. The window always opens the Hub title screen (**3s hold**, then **2s fade-out**;
   Enter / Escape / click skips). After that, the local Design Hub is in its
   dark-default workspace chrome. Choose **Start** for the guided route: local vault
   → source-backed skills → palette → light and dark export.
   The document's own palette is independent of the Hub theme.
4. Jane Example is a clearly labelled fictional template. The guided path creates no
   account, cloud connection, claim, or automatic submission. It uses the bundled local
   Hub and the existing Playwright renderer only.
5. Keep the `Documents\PDF Designer` folder when uninstalling. The uninstaller removes the
   application, not the person's vaults, resumes, palettes, or exports.

This describes the intended customer path, not current release eligibility. Until a
**signed** installer passes the clean-machine script with `-RequireAuthenticode`,
there is no paid download.

## Redirected Documents / OneDrive (decision)

**Policy: follow Windows Documents, including Known Folder Move.**

PDF Designer seeds and opens `Documents\PDF Designer`. It does not create a
Microsoft / OneDrive / Dropbox / iCloud account, and it does not relocate the
workspace to `%LOCALAPPDATA%` when Documents is redirected.

**Observed on SEGOPC (2026-08-24):** Windows Documents is
`<user-home>\OneDrive\Documents`. First-run therefore creates
`<user-home>\OneDrive\Documents\PDF Designer` (Jane Example). OneDrive may
sync it. The Hub still binds only to `127.0.0.1`. The first-run `users/README.md`
in the workspace says the same thing.

Why not force a local-only folder:

- The advertised path is `Documents\PDF Designer`. Silently moving it would
  orphan an existing Jane Example workspace and break the clean-machine harness,
  which uses `[Environment]::GetFolderPath("MyDocuments")`.
- People who turned on Known Folder Move expect Documents to be the canonical
  place. Fighting that is more surprising than documenting it.

What to tell a user who wants a strictly local vault: in OneDrive, stop backing
up the `PDF Designer` folder (or Documents), or set Documents to a local path
in Windows. The app will follow whatever Windows reports as Documents on the
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
Set-Location C:\Github\pdf-designer\desktop
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
window visible for the required UI/navigation observation; omit it only for
non-visual automation. Add `-RequireAuthenticode` only on a signed build.

LIVPHI remains a source-docs mirror via **`\\LIVPHI\Github`** (writable; public
clone only). The advertised `git` share is still access-denied — do not use
administrative shares or change SMB/WinRM policy from SEGOPC.
