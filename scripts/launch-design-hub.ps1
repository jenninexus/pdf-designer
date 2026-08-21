# Windows-first launcher spike for the existing local Design Hub.
# It starts only pdf_tool.preview on loopback, waits for the Hub response, then
# opens the default browser. No installer, account, telemetry, or cloud service.
[CmdletBinding()]
param(
    [ValidateRange(1024, 65535)]
    [int]$Port = 8787,
    [switch]$NoOpen
)

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
$url = "http://127.0.0.1:$Port/"

function Test-DesignHub {
    try {
        $response = Invoke-WebRequest -UseBasicParsing -Uri $url -TimeoutSec 1
        return $response.StatusCode -eq 200 -and $response.Content -match '<title>.*Design Hub'
    } catch {
        return $false
    }
}

if (-not (Test-DesignHub)) {
    $python = Get-Command python -ErrorAction SilentlyContinue
    if (-not $python) { $python = Get-Command python3 -ErrorAction SilentlyContinue }
    if (-not $python) {
        throw 'Python was not found. From this checkout run: pip install -e ".[dev]"; playwright install chromium'
    }

    $startInfo = [System.Diagnostics.ProcessStartInfo]::new()
    $startInfo.FileName = $python.Source
    $startInfo.Arguments = "-m pdf_tool.preview --port $Port --no-open"
    $startInfo.WorkingDirectory = $repoRoot
    $startInfo.UseShellExecute = $false
    $startInfo.CreateNoWindow = $true
    $startInfo.WindowStyle = [System.Diagnostics.ProcessWindowStyle]::Hidden
    [void][System.Diagnostics.Process]::Start($startInfo)

    $ready = $false
    for ($attempt = 0; $attempt -lt 40; $attempt++) {
        if (Test-DesignHub) { $ready = $true; break }
        Start-Sleep -Milliseconds 250
    }
    if (-not $ready) {
        throw "Design Hub did not become ready at $url. Verify the local package with: python -m pdf_tool.preview --port $Port --no-open"
    }
}

if (-not $NoOpen) { Start-Process $url }
Write-Host "Design Hub ready (local only): $url"
