"""Public HTML examples must not depend on ignored local workspace files."""

from __future__ import annotations

import re
from pathlib import Path

import pytest
from pypdfium2 import PdfDocument

from pdf_tool.check_generation import run_file
from pdf_tool.html_to_pdf import export_html_to_pdf


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


def test_tracked_tree_has_no_personal_applicant_files() -> None:
    import subprocess

    listed = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True)
    banned_prefixes = (
        "users/jenni",
        "users/shade",
        "users/studio",
        "vaults/jenni",
        "vaults/shade",
        "vaults/studio",
        "profiles/jenni",
        "profiles/shade",
        "profiles/studio",
        "resumes/jenni",
        "resumes/shade",
        "resumes/studio",
    )
    leaked = [
        line.replace("\\", "/")
        for line in listed.splitlines()
        if any(line.replace("\\", "/").startswith(prefix) for prefix in banned_prefixes)
    ]
    assert leaked == [], f"personal applicant files are tracked: {leaked}"


def test_tracked_job_template_has_no_provider_specific_material() -> None:
    import subprocess

    listed = subprocess.check_output(["git", "ls-files", "_job-apps"], cwd=ROOT, text=True)
    visible = [path for path in listed.splitlines() if (ROOT / path).exists()]
    forbidden = "hand" + "shake"
    assert all(forbidden not in path.lower() for path in visible)


def test_public_personal_letter_uses_system_fonts() -> None:
    letter = ROOT / "examples/profiles/default-letter/personal-letter.html"
    text = letter.read_text(encoding="utf-8")
    assert '@font-face' not in text
    assert '--signature: "Georgia", "Times New Roman", Times, serif;' in text


def test_public_personal_letter_passes_the_full_generation_gate() -> None:
    result = run_file(ROOT / "examples/profiles/default-letter/personal-letter.html")
    assert result["passed"], result


def test_public_cover_letter_passes_the_full_generation_gate() -> None:
    result = run_file(ROOT / "examples/profiles/default-cover-letter/default-cover-letter.html")
    assert result["passed"], result


@pytest.mark.parametrize(
    ("mode", "background", "expected"),
    [
        ("light", None, (255, 255, 255)),
        ("light", "#f5f3fb", (245, 243, 251)),
        ("dark", "#0a0a12", (10, 10, 18)),
    ],
)
def test_default_resume_prints_the_selected_background_to_every_edge(
    tmp_path: Path, mode: str, background: str | None, expected: tuple[int, int, int]
) -> None:
    source = ROOT / "examples/profiles/default-resume/default-resume.html"
    pdf = export_html_to_pdf(
        source,
        pdf_path=tmp_path / "example.pdf",
        pdf_theme=mode,
        css_vars={"--bg": background} if background else None,
    )
    with PdfDocument(pdf) as document:
        assert len(document) == 2
        for page in document:
            try:
                assert page.get_size() == (612, 792)
                with page.render(scale=1).to_pil() as image:
                    for x, y in ((10, 10), (10, 400), (600, 400), (305, 780)):
                        assert image.getpixel((x, y))[:3] == expected
            finally:
                page.close()
