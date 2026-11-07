# Packaging — PyPI / installer spike

How a **non-checkout** user gets `pdf-designer`. Companion to
[`PRODUCT.md`](PRODUCT.md) (business) and [`GETTING-STARTED.md`](GETTING-STARTED.md)
(public how-to from a clone).

> **Status (2026-08-21):** path resolution + wheel asset gate + **local fresh-venv
> install proof** landed (`scripts/testpypi-dry-run.py`). TestPyPI **upload is optional** —
> it is the sandbox for test.pypi.org so strangers can `pip install` without cloning.
> **Not required** for a GitHub-clone launch. Skip the token unless you want that path.
> Supported public install remains a **git checkout** + `pip install -e ".[dev]"` until then.

---

## The blocker we measured

`python -m build --wheel` on the pre-spike tree produced a wheel with **only**
`pdf_tool/*.py` + `static/hub.css`. It did **not** include `themes/` or
`layouts/`.

Those trees are required by:

| Caller | Needs |
|---|---|
| `pdf_tool.variants` | `themes/default-resume.json` + `themes/presets/*` |
| `pdf_tool.collage` | `themes/default-collage.json` + `layouts/collage/*` |
| `pdf_tool.preview` | public palettes under `themes/` (+ optional `brands/`) |

Hard-coding `Path(__file__).parents[2]` assumes an editable `src/` layout. A
site-packages install breaks that assumption.

## Decision (v1)

| Layer | Choice |
|---|---|
| **SSOT** | Repo-root `themes/` + `layouts/` + `examples/` stay the edit surface |
| **Wheel payload** | Copy public trees into `src/pdf_tool/share/` at build time |
| **Runtime resolve** | `pdf_tool.paths.repo_root()` — **checkout wins** over `share/` (so live edits aren't shadowed); wheel-only installs fall through to `pdf_tool/share/` |
| **Private data** | Never package live root-noun payloads (`users/`, `vaults/`, `profiles/`, `_job-apps/`, `resumes/`, `collages/`, `brands/`, `_exports/`) or legacy `storage/` |
| **Chromium** | Still a post-install step: `playwright install chromium` |
| **Desktop installer** | Windows x64 Electron/NSIS builder exists locally; see [`WINDOWS-ELECTRON.md`](WINDOWS-ELECTRON.md). It remains unsigned and needs a clean-machine install proof before release. |

```bash
# Gate before any upload
python scripts/sync-wheel-share.py
python scripts/check-wheel-assets.py   # clean build + assert public source assets; reject generated PDFs/images

# Full dry-run: build + fresh venv + prove bundled share/ + check_generation
python scripts/testpypi-dry-run.py              # local wheel proof (no upload)
python scripts/testpypi-dry-run.py --upload     # needs TESTPYPI_TOKEN
python scripts/testpypi-dry-run.py --upload --prompt-token  # private one-use prompt
```

⚠ **Prove from outside the checkout.** Because checkout wins over `share/`, a
fresh-venv proof must run with cwd *outside* the repo (the dry-run script does
this). Verifying from the checkout directory will silently use live `themes/`.

## Supported install paths (today → next)

| Path | Who | Status |
|---|---|---|
| `git clone` + `pip install -e ".[dev]"` + `playwright install chromium` | Devs / agents | ✅ supported (white-label smoke) |
| Local wheel with synced `share/` | Spike / CI | ✅ `check-wheel-assets.py` + `testpypi-dry-run.py` |
| TestPyPI `pip install pdf-designer` | Non-dev trial | ✅ `pdf-designer 0.4.0` uploaded and fresh-installed 2026-08-21 |
| Production PyPI | Public | ❌ deliberate decision: do not publish now; it is a developer-package channel, not the Windows desktop delivery route |
| Windows Electron NSIS installer | Creatives | 🟡 local artifact builder works; unsigned + clean-machine install validation pending |

## Publish checklist (when ready)

1. Bump `project.version` in `pyproject.toml` if that version was already uploaded
2. `python scripts/check-wheel-assets.py` → PASS
3. `python scripts/smoke-white-label.py` from a clean clone (still the product gate)
4. **For a future TestPyPI release, create an API token** at https://test.pypi.org/manage/account/token/
   — keep it in your private credential manager or set the local-only `TESTPYPI_TOKEN`
   environment variable.
   For a single upload without retaining the token, the preferred path is:

   ```powershell
   python scripts/testpypi-dry-run.py --upload --prompt-token
   ```

   The prompt hides the token input and keeps it only in the upload process. To use an environment
   variable instead:

   ```powershell
   # Current PowerShell session only — preferred for one upload.
   $env:TESTPYPI_TOKEN = "pypi-your-token-here"

   # Optional: persist for your Windows user, then open a new terminal.
   [Environment]::SetEnvironmentVariable("TESTPYPI_TOKEN", "pypi-your-token-here", "User")
   ```

   Do not create a `.env` file or put the token in this repository.
5. `python scripts/testpypi-dry-run.py --upload` → upload + fresh-venv install from TestPyPI
6. Decide production PyPI independently. The current decision is **do not publish**:
   TestPyPI is the developer-package rehearsal and the Windows Electron/NSIS
   installer is the customer install route.
7. Add a README badge / install blurb only after a deliberate production-PyPI
   release, not merely because the TestPyPI proof passes.

## Non-goals for packaging

- Shipping vaults, brand maps, or application history
- Auto-downloading Chromium without an explicit `playwright install`
- A second renderer inside the wheel
- Replacing the Design Hub with an Electron fork just to get onto PyPI

## Related

- Product / paid shell: [`PRODUCT.md`](PRODUCT.md)
- Public clone demo: [`GETTING-STARTED.md`](GETTING-STARTED.md)
- License honesty: [`LICENSING-NOTES.md`](LICENSING-NOTES.md)


## Windows release readiness (2026-11-07)

The desktop implementation currently produces a local unsigned x64 NSIS installer. A Store-compatible package, clean-machine lifecycle, certification and listing remain open. Evaluate **Store-packaged MSIX/AppX first** for a trusted Windows install.

| Route | Cost and install behavior |
|---|---|
| Microsoft Store, packaged MSIX/AppX | Current onboarding is free for Individual and Company accounts. Microsoft describes the account as permanent and documents certification for app updates with no separate upload or annual fee. Microsoft hosts and re-signs the certified package. Store installation avoids the SmartScreen download warning and the Store delivers updates. [Account setup](https://learn.microsoft.com/en-us/windows/apps/publish/partner-center/open-a-developer-account) · [Release overview](https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/publish-first-app) · [Update workflow](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msix/publish-update-to-your-app-on-store) |
| Microsoft Store, existing MSI/EXE | Requires a versioned HTTPS installer URL and publisher Authenticode signing for the installer and its PE files. The app owns updates. [Distribution comparison](https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/choose-distribution-path) |
| Direct Windows download | The publisher owns hosting, signing and updates. Azure Artifact Signing Basic is US$9.99 per account per month, including 5,000 signatures. Timestamping preserves already signed files after the signing account is closed, subject to certificate trust and revocation. A new direct download can still trigger SmartScreen while it earns reputation. [Azure pricing](https://learn.microsoft.com/en-us/azure/artifact-signing/how-to-change-sku) · [Signing FAQ](https://learn.microsoft.com/en-us/azure/artifact-signing/faq) · [SmartScreen](https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/smartscreen-reputation) |

Choose the appropriate publisher and account type, then use the exact Partner Center identity in the production manifest. Prepare a listing with fictional screenshots, accurate platform requirements, support and the applicable ratings and disclosures. The Store requires a privacy policy URL for Win32 apps, including apps that access personal information locally. Build from a clean, pinned source revision. Inspect the actual package and its bundled Python, Chromium, dependencies and fictional workspace seed. Run Windows App Certification Kit and clean Windows 10/11 x64 lifecycle checks before submission. [Microsoft package requirements](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msix/app-package-requirements) · [Store privacy policy requirements](https://learn.microsoft.com/en-us/windows/apps/publish/store-policies#105-personal-information)

| Gate | Current evidence | Next proof |
|---|---|---|
| Engine and local UI | Implemented, with deterministic document checks | Reuse accepted source/artifact receipts; test each release source |
| Desktop shell | Electron main process, bundled-runtime builder and NSIS target exist | Rebuild from the chosen release source; old local binaries do not prove current source |
| Store package | `desktop/package.json` targets NSIS | Build a Store-compatible package with the actual Electron/Python/Chromium runtime and verify the installed application |
| Clean Windows lifecycle | A harness exists; release-specific clean-machine proof remains open | Install, launch, export, update, uninstall and retain the private workspace on clean Windows 10/11 |
| Publisher and commerce | Public source and optional tips are available | Confirm publisher, licensing and support. Treat paid packs and their fulfillment as a separate delivery path |
| Store review | No certification or listing acceptance recorded | Run applicable certification checks and obtain an explicit submission decision |

The public clone and packaged export flow use no project dotenv file. Build and publishing credentials belong in a private account or host configuration. Keep local settings, signing material and Windows release binaries out of public Git. Run the privacy hook and inspect the exact package file list before distribution. See [Public vs local split](PUBLIC-LOCAL-SPLIT.md).
