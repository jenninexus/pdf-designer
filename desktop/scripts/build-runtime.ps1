[CmdletBinding()]
param([string]$PythonExecutable, [switch]$Release, [string]$BrowserCache, [switch]$Store)

# Build a self-contained Python/Playwright sidecar for the Windows Electron
# shell. This runs only at packaging time; the produced app reads no user
# environment variables or credentials.
$ErrorActionPreference = 'Stop'
$desktopRoot = Split-Path -Parent $PSScriptRoot
$repoRoot = Split-Path -Parent $desktopRoot
$buildRoot = Join-Path $desktopRoot '.runtime-build'
$venvRoot = Join-Path $buildRoot 'venv'
$venvPython = Join-Path $venvRoot 'Scripts\python.exe'
$browserRoot = Join-Path $buildRoot 'browsers'
$distRoot = Join-Path $buildRoot 'dist'
$workRoot = Join-Path $buildRoot 'work'
$specRoot = Join-Path $buildRoot 'spec'
$finalRuntimeRoot = Join-Path $desktopRoot 'runtime\pdf-designer-runtime'
$runtimeEntry = Join-Path $desktopRoot 'runtime_entry.py'

function Assert-WorkspaceChild([string]$candidate, [string]$parent) {
    $resolvedCandidate = [IO.Path]::GetFullPath($candidate)
    $resolvedParent = [IO.Path]::GetFullPath($parent).TrimEnd('\') + '\'
    if (-not $resolvedCandidate.StartsWith($resolvedParent, [StringComparison]::OrdinalIgnoreCase)) {
        throw "Refusing path outside the desktop build area: $resolvedCandidate"
    }
}

Assert-WorkspaceChild $buildRoot $desktopRoot
Assert-WorkspaceChild $finalRuntimeRoot (Join-Path $desktopRoot 'runtime')

$python = if ($PythonExecutable) {
    (Resolve-Path -LiteralPath $PythonExecutable).Path
} else {
    (Get-Command python.exe -ErrorAction Stop).Source
}
if ($Release) {
    $pythonVersion = & $python -c 'import platform, struct; print(platform.python_version(), struct.calcsize("P") * 8)'
    if ($LASTEXITCODE -or $pythonVersion -ne '3.12.10 64') {
        throw "Windows release requires CPython 3.12.10 x64. Found: $pythonVersion"
    }
    if ((Test-Path -LiteralPath $buildRoot) -or (Test-Path -LiteralPath $finalRuntimeRoot)) {
        throw 'Build a release from a fresh checkout with no staged runtime or browser cache.'
    }
}
if ($Store -and (-not $Release -or $BrowserCache)) {
    throw 'Store requires Release and uses an installed browser instead of BrowserCache.'
}
if ($BrowserCache -and -not $Release) {
    throw 'BrowserCache applies only to the release runtime.'
}

& $python "$repoRoot\scripts\sync-wheel-share.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $python "$repoRoot\scripts\sync-desktop-seed.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

if (-not (Test-Path -LiteralPath $venvPython)) {
    & $python -m venv $venvRoot
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

$locked = if ($Release) { @('-r', "$desktopRoot\runtime-requirements.txt") } else { @() }
& $venvPython -m pip install --disable-pip-version-check -e "$repoRoot" "pyinstaller==6.22.2" @locked
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

# Non-Store builds keep a Playwright browser beside the frozen runtime.
# Store builds skip the download and resolve a browser installed on the PC.
if (-not $Store) {
    $bundledChrome = Get-ChildItem -LiteralPath $browserRoot -Filter chrome.exe -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($BrowserCache) {
        $cachePath = (Resolve-Path -LiteralPath $BrowserCache).Path
        $previousBrowserPath = $env:PLAYWRIGHT_BROWSERS_PATH
        try {
            $env:PLAYWRIGHT_BROWSERS_PATH = $cachePath
            $cachedExecutable = & $venvPython -c 'from playwright.sync_api import sync_playwright; p=sync_playwright().start(); print(p.chromium.executable_path); p.stop()'
            if ($LASTEXITCODE -or -not $cachedExecutable) { throw 'Playwright could not resolve its pinned browser.' }
            Assert-WorkspaceChild $cachedExecutable $cachePath
            if (-not (Test-Path -LiteralPath $cachedExecutable -PathType Leaf)) {
                throw 'BrowserCache is missing the full Chromium revision pinned by Playwright.'
            }
            $bundledChrome = Get-Item -LiteralPath $cachedExecutable
        } finally {
            if ($null -eq $previousBrowserPath) { Remove-Item Env:PLAYWRIGHT_BROWSERS_PATH -ErrorAction SilentlyContinue }
            else { $env:PLAYWRIGHT_BROWSERS_PATH = $previousBrowserPath }
        }
    }
    if (-not $bundledChrome) {
        $previousBrowserPath = $env:PLAYWRIGHT_BROWSERS_PATH
        try {
            $env:PLAYWRIGHT_BROWSERS_PATH = $browserRoot
            $installArgs = @('-m', 'playwright', 'install')
            if ($Release) { $installArgs += '--no-shell' }
            & $venvPython @installArgs chromium
            if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
        } finally {
            if ($null -eq $previousBrowserPath) { Remove-Item Env:PLAYWRIGHT_BROWSERS_PATH -ErrorAction SilentlyContinue }
            else { $env:PLAYWRIGHT_BROWSERS_PATH = $previousBrowserPath }
        }
        $bundledChrome = Get-ChildItem -LiteralPath $browserRoot -Filter chrome.exe -Recurse | Select-Object -First 1
        if (-not $bundledChrome) { throw 'Playwright did not install full Chromium.' }
    }
}

& $venvPython -m PyInstaller --noconfirm --clean --onedir --name pdf-designer-runtime `
    --paths "$repoRoot\src" `
    --collect-all pdf_tool --collect-all playwright --collect-all pypdf --collect-all PIL `
    --distpath $distRoot --workpath $workRoot --specpath $specRoot $runtimeEntry
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$builtRuntime = Join-Path $distRoot 'pdf-designer-runtime'
$runtimeExe = Join-Path $builtRuntime 'pdf-designer-runtime.exe'
if (-not (Test-Path -LiteralPath $runtimeExe)) { throw "PyInstaller did not produce $runtimeExe" }
if (Test-Path -LiteralPath $finalRuntimeRoot) { Remove-Item -LiteralPath $finalRuntimeRoot -Recurse -Force }
New-Item -ItemType Directory -Path (Split-Path -Parent $finalRuntimeRoot) -Force | Out-Null
Copy-Item -LiteralPath $builtRuntime -Destination $finalRuntimeRoot -Recurse
$targetBrowsers = Join-Path $finalRuntimeRoot 'browsers'
if ($Store) {
    Set-Content -LiteralPath (Join-Path $finalRuntimeRoot 'installed-browser.txt') -Value 'Edge or Chrome'
} elseif ($Release) {
    New-Item -ItemType Directory -Path $targetBrowsers | Out-Null
    $browserRevision = $bundledChrome.Directory.Parent
    Copy-Item -LiteralPath $browserRevision.FullName -Destination $targetBrowsers -Recurse
    # The frozen runtime launches chrome.exe directly. The updater installer is
    # unnecessary in an offline runtime and is flagged by Store certification.
    $stagedSetup = Join-Path $targetBrowsers "$($browserRevision.Name)/$($bundledChrome.Directory.Name)/setup.exe"
    if (Test-Path -LiteralPath $stagedSetup -PathType Leaf) {
        Remove-Item -LiteralPath $stagedSetup -Force
    }
} else {
    Copy-Item -LiteralPath $browserRoot -Destination $targetBrowsers -Recurse
}

if ($Release) {
    $notices = New-Item -ItemType Directory -Path (Join-Path $finalRuntimeRoot 'notices')
    $pythonLicense = & $venvPython -c 'from pathlib import Path; import sys; print(Path(sys.base_prefix) / "LICENSE.txt")'
    Copy-Item -LiteralPath $pythonLicense -Destination (Join-Path $notices.FullName 'Python-LICENSE.txt')
    Copy-Item -LiteralPath "$repoRoot\LICENSE" -Destination (Join-Path $notices.FullName 'PDF-Designer-LICENSE.txt')
    foreach ($distribution in Get-ChildItem -LiteralPath "$venvRoot\Lib\site-packages" -Directory -Filter '*.dist-info') {
        $licenses = Get-ChildItem -LiteralPath $distribution.FullName -Recurse -File |
            Where-Object { $_.Name -match '^(LICEN[CS]E|COPYING|NOTICE|AUTHORS)' }
        foreach ($notice in $licenses) {
            $target = Join-Path $notices.FullName (Join-Path $distribution.BaseName (
                [IO.Path]::GetRelativePath($distribution.FullName, $notice.FullName)
            ))
            New-Item -ItemType Directory -Path (Split-Path -Parent $target) -Force | Out-Null
            Copy-Item -LiteralPath $notice.FullName -Destination $target
        }
    }
    @(
        "CPython $pythonVersion"
        (& $venvPython -m pip freeze --exclude-editable)
    ) | Set-Content -LiteralPath (Join-Path $notices.FullName 'runtime-versions.txt') -Encoding utf8
}

if (-not $Store) {
    $bundledChrome = Get-ChildItem -LiteralPath (Join-Path $finalRuntimeRoot 'browsers') -Filter chrome.exe -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
    if (-not $bundledChrome) { throw 'The runtime is missing bundled Playwright Chromium.' }
}
& (Join-Path $finalRuntimeRoot 'pdf-designer-runtime.exe') --help
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "PASS - desktop runtime ready: $finalRuntimeRoot"
