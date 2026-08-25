<#
.SYNOPSIS
Inspects Authenticode on a PDF Designer NSIS installer.

.DESCRIPTION
Unsigned packaging artifacts are expected from `npm run dist`. They are never
listable. A public/Gumroad/JN paid file must pass -RequireSigned.
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [ValidateScript({ Test-Path -LiteralPath $_ -PathType Leaf })]
    [string]$InstallerPath,

    [switch]$RequireSigned,

    [string]$ExpectedPublisher
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$resolved = (Resolve-Path -LiteralPath $InstallerPath).Path
$sig = Get-AuthenticodeSignature -FilePath $resolved
$subject = if ($sig.SignerCertificate) { $sig.SignerCertificate.Subject } else { "" }

Write-Host "Path: $resolved"
Write-Host "Status: $($sig.Status)"
Write-Host "StatusMessage: $($sig.StatusMessage)"
Write-Host "Signer: $subject"
if ($sig.SignerCertificate) {
    Write-Host "NotAfter: $($sig.SignerCertificate.NotAfter.ToString('u'))"
}

if ($RequireSigned) {
    if ($sig.Status -ne "Valid") {
        throw "Authenticode gate failed: $resolved is $($sig.Status). Unsigned NSIS artifacts are not listable."
    }
    if ($ExpectedPublisher -and ($subject -notlike "*$ExpectedPublisher*")) {
        throw "Authenticode publisher mismatch. Expected subject to contain '$ExpectedPublisher'; got '$subject'."
    }
    Write-Host "PASS: Authenticode signature is Valid."
    exit 0
}

if ($sig.Status -ne "Valid") {
    Write-Warning "Unsigned or invalid Authenticode signature ($($sig.Status)). This artifact is not listable."
}
exit 0
