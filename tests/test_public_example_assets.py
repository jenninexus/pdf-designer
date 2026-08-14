"""Public HTML examples must not depend on ignored local workspace files."""

from __future__ import annotations

import re
from pathlib import Path

from pdf_tool.check_generation import run_file



ROOT = Path(__file__).resolve().parents[1]
PRIVATE_ASSET_REF = re.compile(
    r"(?:src|href)\s*=\s*['\"][^'\"]*(?:storage|users|vaults|profiles|resumes|_job-apps|applications|collages|brands)/"
    r"|url\(\s*['\"]?[^)'\"]*(?:storage|users|vaults|profiles|resumes|_job-apps|applications|collages|brands)/",
    re.IGNORECASE,
)


def test_public_example_html_has_no_private_workspace_asset_references() -> None:
    offenders = [
        path.relative_to(ROOT).as_posix()
        for path in sorted((ROOT / "examples").rglob("*.html"))
        if PRIVATE_ASSET_REF.search(path.read_text(encoding="utf-8"))
    ]
    assert offenders == [], f"public examples reference ignored workspace assets: {offenders}"


def test_public_letter_uses_the_tracked_parisienne_asset() -> None:
    letter = ROOT / "examples/profiles/default-letter/personal-letter.html"
    text = letter.read_text(encoding="utf-8")
    assert "../../../themes/fonts/Parisienne-Regular.woff2" in text
    assert (ROOT / "themes/fonts/Parisienne-Regular.woff2").is_file()


def test_public_personal_letter_passes_the_full_generation_gate() -> None:
    result = run_file(ROOT / "examples/profiles/default-letter/personal-letter.html")
    assert result["passed"], result
