# Compatibility entry used by the workspace task. The Windows-first launcher
# owns readiness validation, loopback-only hosting, and browser opening.
& (Join-Path $PSScriptRoot 'launch-design-hub.ps1')
exit $LASTEXITCODE
