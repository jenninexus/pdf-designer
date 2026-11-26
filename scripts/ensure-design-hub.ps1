# Compatibility entry used by the workspace task. The Windows-first launcher
# owns readiness validation, loopback-only hosting, and browser opening.
[CmdletBinding()]
param(
    [ValidateRange(1024, 65535)]
    [int]$Port = 8787,
    [switch]$NoOpen
)

& (Join-Path $PSScriptRoot 'launch-design-hub.ps1') @PSBoundParameters
