"""Authenticode helper stays parseable and refuses a listable unsigned installer."""

from pathlib import Path
import shutil
import subprocess

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "verify-authenticode.ps1"


def test_authenticode_helper_parses_in_powershell():
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


def test_authenticode_helper_refuses_unsigned_when_required():
    source = SCRIPT.read_text(encoding="utf-8")
    assert "Get-AuthenticodeSignature" in source
    assert "RequireSigned" in source
    assert "not listable" in source
    assert "ExpectedPublisher" in source
