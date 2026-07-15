# Ensure Design Hub is listening on 127.0.0.1:8787; open the browser either way.
# Usage: pwsh -NoProfile -File scripts/ensure-design-hub.ps1
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
    Write-Host "Design Hub already running — opened $Url"
    exit 0
}

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Error "python not found on PATH. From repo root: pip install -e `".[dev]`" && playwright install chromium"
    exit 1
}

# Fresh start: let preview open the browser (do not pass --no-open).
Start-Process -FilePath $python.Source -ArgumentList @(
    '-m', 'pdf_tool.preview', '--port', "$Port"
) -WorkingDirectory $RepoRoot -WindowStyle Normal

Write-Host "Design Hub starting on $Url (browser opens via preview)"
exit 0
