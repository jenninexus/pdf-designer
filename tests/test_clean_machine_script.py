"""The clean-machine release harness stays parseable and deliberately strict."""

from pathlib import Path
import shutil
import subprocess

import pytest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "verify-clean-machine.ps1"


def test_clean_machine_harness_parses_in_powershell():
    shell = shutil.which("pwsh") or shutil.which("powershell")
    if shell is None:
        pytest.skip("PowerShell is not installed")
    script_path = str(SCRIPT).replace("'", "''")
    parser = (
        "$tokens = $null; $errors = $null; "
        f"[System.Management.Automation.Language.Parser]::ParseFile('{script_path}', [ref]$tokens, [ref]$errors) | Out-Null; "
        "if ($errors.Count) { $errors | ForEach-Object { $_.ToString() }; exit 1 }"
    )
    result = subprocess.run(
        [shell, "-NoProfile", "-Command", parser],
        check=False,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stderr or result.stdout


def test_clean_machine_harness_requires_clean_target_and_full_lifecycle():
    source = SCRIPT.read_text(encoding="utf-8")

    for contamination_guard in (
        "Clean-target preflight failed: checkout exists",
        '"python", "py", "node", "npm"',
        "workspace already exists",
        "Assert-NotInsideCheckout",
        "customer PC is not assumed",
    ):
        assert contamination_guard in source

    for required_behavior in (
        '"/S", "/D=$InstallDir"',
        "Start-Process -FilePath $appExe",
        "ShowAppWindow",
        "RequireAuthenticode",
        "BundledRuntimeProof",
        "AllowExistingWorkspace",
        "Get-AuthenticodeSignature",
        "pdf-designer-runtime.exe",
        "Get-NetTCPConnection -State Listen -OwningProcess $runtime.Id",
        "Jane Example",
        "FICTIONAL RELEASE-TEST VAULT ONLY",
        'ValidateSet("pdf-light", "pdf-dark")',
        "CloseMainWindow()",
        "Stop-Process -Id $App.Id",
        "pdf-designer-runtime child survived",
        "Invoke-SilentNsi -FilePath $uninstaller",
        "Uninstaller removed Documents\\\\PDF Designer",
    ):
        assert required_behavior in source
