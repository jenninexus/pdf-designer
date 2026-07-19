# Ensure the Design Hub is listening on 127.0.0.1:8787, then open the browser.
# Machine-agnostic: uses `python` from PATH and repo-relative paths only — no
# personal paths, no absolute interpreter. Safe for any cloned checkout.
#
# The server is launched HIDDEN (no flashing console window). It keeps running
# after this script exits and auto-refreshes the UI when documents change
# (poll of /api/version), so you rarely need to restart it.
#
# Usage: pwsh -NoProfile -File scripts/ensure-design-hub.ps1
#        (falls back to Windows PowerShell if pwsh is unavailable)
$ErrorActionPreference = 'Stop'
$Port = 8787
$Url = "http://127.0.0.1:$Port/"
$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot

function Test-DesignHubListening {
    try {
        $client = [System.Net.Sockets.TcpClient]::new()
        $iar = $client.BeginConnect('127.0.0.1', $Port, $null, $null)
        $ok = $iar.AsyncWaitHandle.WaitOne(400)
        if ($ok -and $client.Connected) {
            $client.EndConnect($iar)
            $client.Close()
            return $true
        }
        $client.Close()
    } catch {
        # not listening
    }
    return $false
}

if (Test-DesignHubListening) {
    Start-Process $Url
    Write-Host "Design Hub already running - opened $Url"
    exit 0
}

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    $python = Get-Command python3 -ErrorAction SilentlyContinue
}
if (-not $python) {
    Write-Error "python not found on PATH. From the repo root run: pip install -e `".[dev]`" ; playwright install chromium"
    exit 1
}

# Launch the server HIDDEN (no console window). Pass --no-open; this script
# opens the browser itself once the port is up, so we never double-open.
$psi = [System.Diagnostics.ProcessStartInfo]::new()
$psi.FileName = $python.Source
$psi.Arguments = "-m pdf_tool.preview --port $Port --no-open"
$psi.WorkingDirectory = $RepoRoot
$psi.UseShellExecute = $false
$psi.CreateNoWindow = $true
$psi.WindowStyle = 'Hidden'
[void][System.Diagnostics.Process]::Start($psi)

# Wait briefly for the port, then open the browser.
for ($i = 0; $i -lt 20; $i++) {
    if (Test-DesignHubListening) { break }
    Start-Sleep -Milliseconds 250
}
Start-Process $Url
Write-Host "Design Hub started (hidden) on $Url"
exit 0
