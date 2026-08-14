"""Public HTML examples must not depend on ignored local workspace files."""

from __future__ import annotations

import re
from pathlib import Path

from pdf_tool.check_generation import run_file



ROOT = Path(__file__).resolve().parents[1]
PRIVATE_ASSET_REF = re.compile(
    r"(?:src|href)\s*=\s*['\"][^'\"]*storage/|url\(\s*['\"]?[^)'\"]*storage/",
    re.IGNORECASE,
)


def test_public_example_html_has_no_private_storage_asset_references() -> None:
    offenders = [
        path.relative_to(ROOT).as_posix()
        for path in sorted((ROOT / "examples").rglob("*.html"))
        if PRIVATE_ASSET_REF.search(path.read_text(encoding="utf-8"))
    ]
    assert offenders == [], f"public examples reference ignored storage/: {offenders}"


def test_public_personal_letter_passes_the_full_generation_gate() -> None:
    result = run_file(ROOT / "examples/profiles/default-letter/personal-letter.html")
    assert result["passed"], result
