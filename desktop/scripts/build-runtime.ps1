[CmdletBinding()]
param()

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

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) { $python = Get-Command python3 -ErrorAction SilentlyContinue }
if (-not $python) { throw 'Python 3.9+ is required to build the local desktop runtime.' }

& $python.Source "$repoRoot\scripts\sync-wheel-share.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $python.Source "$repoRoot\scripts\sync-desktop-seed.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

if (-not (Test-Path -LiteralPath $venvPython)) {
    & $python.Source -m venv $venvRoot
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

& $venvPython -m pip install --disable-pip-version-check -e "$repoRoot" "pyinstaller==6.22.2"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

# The browser is an explicit sibling of the frozen runtime. `pdf_tool.browser`
# passes its executable path to Playwright only when frozen, avoiding a user
# environment variable and retaining the existing Playwright renderer.
$bundledChrome = Get-ChildItem -LiteralPath $browserRoot -Filter chrome.exe -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
if (-not $bundledChrome) {
    $previousBrowserPath = $env:PLAYWRIGHT_BROWSERS_PATH
    try {
        $env:PLAYWRIGHT_BROWSERS_PATH = $browserRoot
        & $venvPython -m playwright install chromium
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    } finally {
        if ($null -eq $previousBrowserPath) { Remove-Item Env:PLAYWRIGHT_BROWSERS_PATH -ErrorAction SilentlyContinue }
        else { $env:PLAYWRIGHT_BROWSERS_PATH = $previousBrowserPath }
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
Copy-Item -LiteralPath $browserRoot -Destination (Join-Path $finalRuntimeRoot 'browsers') -Recurse

$bundledChrome = Get-ChildItem -LiteralPath (Join-Path $finalRuntimeRoot 'browsers') -Filter chrome.exe -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
if (-not $bundledChrome) { throw 'The runtime is missing bundled Playwright Chromium.' }
& (Join-Path $finalRuntimeRoot 'pdf-designer-runtime.exe') --help
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "PASS - desktop runtime ready: $finalRuntimeRoot"
