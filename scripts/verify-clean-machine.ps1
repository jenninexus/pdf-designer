<#
.SYNOPSIS
Exercises the unsigned PDF Designer installer on an intentionally clean Windows target.

.DESCRIPTION
This script is a release gate, not an installer. Copy it and the built Setup EXE to
an otherwise clean Windows 10/11 x64 test machine, then run it from a directory
outside a source checkout. It refuses to run if it sees the expected checkout,
system Python, Node, npm, an existing PDF Designer workspace, or an existing test
installation. It uses only the public Jane Example seed and writes one conspicuously
fictional release-test vault copy.

It deliberately does not delete the Documents workspace. A successful run proves
the NSIS uninstaller preserves it.
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [ValidateScript({ Test-Path -LiteralPath $_ -PathType Leaf })]
    [string]$InstallerPath,

    [string]$InstallDir = (Join-Path $env:LOCALAPPDATA "Programs\PDF Designer Release Test"),

    [string]$ExpectedCheckout = "C:\Github\pdf-designer",

    [ValidateRange(30, 600)]
    [int]$TimeoutSeconds = 180,

    # Use this on the clean target when the release tester must observe the
    # Electron window. The default stays hidden for automated execution.
    [switch]$ShowAppWindow
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

$workspace = Join-Path ([Environment]::GetFolderPath("MyDocuments")) "PDF Designer"
$appExe = Join-Path $InstallDir "PDF Designer.exe"
$uninstaller = Join-Path $InstallDir "Uninstall PDF Designer.exe"
$fixtureVault = Join-Path $workspace "vaults\release-test-fictional.json"
$exportDir = Join-Path $workspace "release-test-exports"
$installed = $false
$uninstallAttempted = $false

function Assert-Condition {
    param(
        [Parameter(Mandatory)][bool]$Condition,
        [Parameter(Mandatory)][string]$Message
    )
    if (-not $Condition) { throw $Message }
}

function Test-CommandPresent {
    param([Parameter(Mandatory)][string]$Name)
    return $null -ne (Get-Command $Name -ErrorAction SilentlyContinue)
}

function Assert-NotInsideCheckout {
    param([Parameter(Mandatory)][string]$Path)
    $current = Split-Path -Parent (Resolve-Path -LiteralPath $Path).Path
    while ($current) {
        if ((Test-Path -LiteralPath (Join-Path $current ".git")) -and
            (Test-Path -LiteralPath (Join-Path $current "pyproject.toml"))) {
            throw "Clean-target preflight failed: the harness is running inside a PDF Designer checkout ($current)."
        }
        $parent = Split-Path -Parent $current
        if ($parent -eq $current) { break }
        $current = $parent
    }
}

function Assert-CleanTarget {
    Assert-Condition (-not (Test-Path -LiteralPath $ExpectedCheckout)) "Clean-target preflight failed: checkout exists at $ExpectedCheckout."
    Assert-NotInsideCheckout -Path $PSCommandPath

    foreach ($tool in @("python", "py", "node", "npm")) {
        Assert-Condition (-not (Test-CommandPresent -Name $tool)) "Clean-target preflight failed: system command '$tool' is available."
    }

    Assert-Condition (-not (Test-Path -LiteralPath $workspace)) "Clean-target preflight failed: workspace already exists at $workspace."
    Assert-Condition (-not (Test-Path -LiteralPath $InstallDir)) "Clean-target preflight failed: install directory already exists at $InstallDir."
    Assert-Condition ($null -eq (Get-Process -Name "PDF Designer" -ErrorAction SilentlyContinue)) "Clean-target preflight failed: PDF Designer is already running."
}

function Invoke-SilentNsi {
    param([Parameter(Mandatory)][string]$FilePath)
    # NSIS requires /D to be its final command-line argument.
    $process = Start-Process -FilePath $FilePath -ArgumentList @("/S", "/D=$InstallDir") -Wait -PassThru -WindowStyle Hidden
    Assert-Condition ($process.ExitCode -eq 0) "NSIS command failed with exit code $($process.ExitCode): $FilePath"
}

function Wait-ForLocalRuntime {
    param([Parameter(Mandatory)][datetime]$StartedAfter)
    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    do {
        $runtimes = @(Get-Process -Name "pdf-designer-runtime" -ErrorAction SilentlyContinue |
            Where-Object { $_.StartTime -ge $StartedAfter })
        foreach ($runtime in $runtimes) {
            $listeners = @(Get-NetTCPConnection -State Listen -OwningProcess $runtime.Id -ErrorAction SilentlyContinue |
                Where-Object { $_.LocalAddress -eq "127.0.0.1" })
            foreach ($listener in $listeners) {
                $url = "http://127.0.0.1:$($listener.LocalPort)/"
                try {
                    $response = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 5
                    if ($response.StatusCode -eq 200 -and $response.Content -match "Design Hub") {
                        return [pscustomobject]@{ Process = $runtime; Url = $url; Port = $listener.LocalPort }
                    }
                } catch {
                    # The listener may be live before the Hub response is ready.
                }
            }
        }
        Start-Sleep -Milliseconds 500
    } while ((Get-Date) -lt $deadline)
    throw "The packaged pdf-designer-runtime did not expose a ready Design Hub within $TimeoutSeconds seconds."
}

function Invoke-HubExport {
    param(
        [Parameter(Mandatory)][string]$HubUrl,
        [Parameter(Mandatory)][ValidateSet("pdf-light", "pdf-dark")][string]$Format
    )
    $payload = @{
        doc = "examples/profiles/default-resume/default-resume.html"
        format = $Format
        outDir = $exportDir
    } | ConvertTo-Json -Compress
    $result = Invoke-RestMethod -Uri ($HubUrl + "api/export") -Method Post -ContentType "application/json" -Body $payload -TimeoutSec $TimeoutSeconds
    Assert-Condition ($result.ok -eq $true) "Hub $Format export failed: $($result.error)"
    $output = @($result.outputs)[0]
    Assert-Condition (Test-Path -LiteralPath $output -PathType Leaf) "Hub $Format export did not create its reported output: $output"
    Assert-Condition ((Resolve-Path -LiteralPath $output).Path.StartsWith((Resolve-Path -LiteralPath $workspace).Path, [StringComparison]::OrdinalIgnoreCase)) "Hub $Format export escaped the local test workspace."
    return $output
}

function Assert-SeedAndCreateFictionalVault {
    $janeUser = Join-Path $workspace "users\examples.json"
    $janeVault = Join-Path $workspace "vaults\examples.json"
    $janeProfile = Join-Path $workspace "profiles\examples.json"
    $janeResume = Join-Path $workspace "examples\profiles\default-resume\default-resume.html"
    foreach ($required in @($janeUser, $janeVault, $janeProfile, $janeResume)) {
        Assert-Condition (Test-Path -LiteralPath $required -PathType Leaf) "Jane Example seed is incomplete: missing $required"
    }
    $jane = Get-Content -LiteralPath $janeUser -Raw | ConvertFrom-Json
    Assert-Condition ($jane.name -eq "Jane Example") "Jane Example seed identity did not match the public fixture."

    $releaseFixture = Get-Content -LiteralPath $janeVault -Raw | ConvertFrom-Json
    $releaseFixture._meta.whatThisIs = "FICTIONAL RELEASE-TEST VAULT ONLY — copied from public Jane Example; contains no customer or private data."
    $releaseFixture._meta.validate = "Release-test fixture only; do not use for a real applicant."
    # `utf8` works in both Windows PowerShell 5.1 and PowerShell 7; the fixture
    # has no privacy-sensitive contents and only needs to remain valid JSON.
    $releaseFixture | ConvertTo-Json -Depth 100 | Set-Content -LiteralPath $fixtureVault -Encoding utf8
    Assert-Condition ((Get-Content -LiteralPath $fixtureVault -Raw) -match "FICTIONAL RELEASE-TEST VAULT ONLY") "The local test vault is not clearly labelled fictional/release-test."
}

function Stop-AppGracefully {
    param(
        [Parameter(Mandatory)][System.Diagnostics.Process]$App,
        [Parameter(Mandatory)][System.Diagnostics.Process]$Runtime,
        [Parameter(Mandatory)][int]$RuntimePort
    )
    Assert-Condition ($App.CloseMainWindow()) "PDF Designer did not accept a graceful main-window close request."
    Assert-Condition ($App.WaitForExit($TimeoutSeconds * 1000)) "PDF Designer did not exit after a graceful main-window close request."
    Start-Sleep -Seconds 2
    Assert-Condition ($null -eq (Get-Process -Id $Runtime.Id -ErrorAction SilentlyContinue)) "The Electron-owned pdf-designer-runtime child survived application exit."
    Assert-Condition ($null -eq (Get-NetTCPConnection -State Listen -LocalAddress "127.0.0.1" -LocalPort $RuntimePort -ErrorAction SilentlyContinue)) "The runtime loopback listener survived application exit."
}

try {
    Assert-CleanTarget
    $installer = (Resolve-Path -LiteralPath $InstallerPath).Path
    Write-Host "Installing unsigned release-test artifact..."
    Invoke-SilentNsi -FilePath $installer
    $installed = $true
    Assert-Condition (Test-Path -LiteralPath $appExe -PathType Leaf) "Installer completed without PDF Designer.exe at $appExe"
    Assert-Condition (Test-Path -LiteralPath $uninstaller -PathType Leaf) "Installer completed without its NSIS uninstaller at $uninstaller"

    $startedAfter = Get-Date
    $appWindowStyle = if ($ShowAppWindow) { "Normal" } else { "Hidden" }
    $app = Start-Process -FilePath $appExe -PassThru -WindowStyle $appWindowStyle
    $runtime = Wait-ForLocalRuntime -StartedAfter $startedAfter
    Assert-SeedAndCreateFictionalVault
    $lightPdf = Invoke-HubExport -HubUrl $runtime.Url -Format "pdf-light"
    $darkPdf = Invoke-HubExport -HubUrl $runtime.Url -Format "pdf-dark"
    Stop-AppGracefully -App $app -Runtime $runtime.Process -RuntimePort $runtime.Port

    Write-Host "Uninstalling release-test artifact..."
    Invoke-SilentNsi -FilePath $uninstaller
    $uninstallAttempted = $true
    Assert-Condition (-not (Test-Path -LiteralPath $appExe)) "Uninstaller left PDF Designer.exe behind."
    Assert-Condition (Test-Path -LiteralPath $workspace -PathType Container) "Uninstaller removed Documents\\PDF Designer."
    Assert-Condition (Test-Path -LiteralPath $fixtureVault -PathType Leaf) "Uninstaller removed the fictional release-test vault."
    Assert-Condition ((Test-Path -LiteralPath $lightPdf -PathType Leaf) -and (Test-Path -LiteralPath $darkPdf -PathType Leaf)) "Uninstaller removed light or dark local export evidence."
    Write-Host "PASS: clean-machine installer verification completed; workspace and fictional test data were preserved."
}
finally {
    if ($installed -and -not $uninstallAttempted -and (Test-Path -LiteralPath $uninstaller -PathType Leaf)) {
        Write-Warning "Verification did not finish; attempting silent cleanup uninstall."
        try { Invoke-SilentNsi -FilePath $uninstaller } catch { Write-Warning "Cleanup uninstall failed: $($_.Exception.Message)" }
    }
}
