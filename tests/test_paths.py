"""pdf_tool.paths.repo_root — checkout vs bundled share discovery."""

from __future__ import annotations

from pathlib import Path

from pdf_tool import paths


def test_repo_root_finds_checkout_themes():
    paths.repo_root.cache_clear()
    root = paths.repo_root()
    assert (root / "themes" / "default-resume.json").is_file()
    assert (root / "layouts").is_dir()
    # Editable checkout must win over a leftover src/pdf_tool/share/ sync tree
    assert root.name != "share"
    assert (root / "pyproject.toml").is_file() or (root / ".git").exists()


def test_repo_root_is_absolute():
    paths.repo_root.cache_clear()
    assert paths.repo_root().is_absolute()


def test_reject_flag_looking_output_dir():
    import pytest

    with pytest.raises(SystemExit):
        paths.reject_flag_looking_path("--output-dir", flag="--output-dir")
    with pytest.raises(SystemExit):
        paths.reject_flag_looking_path("-o", flag="out-dir")
    paths.reject_flag_looking_path("output/jenni/resumes", flag="--output-dir")
    paths.reject_flag_looking_path(None, flag="--output-dir")


def test_default_output_dir_user_then_kind(tmp_path: Path):
    src = tmp_path / "resumes" / "jenni" / "defaults" / "pack.html"
    src.parent.mkdir(parents=True)
    src.write_text("<p></p>", encoding="utf-8")
    assert paths.default_output_dir(src, root=tmp_path) == tmp_path / "output" / "jenni" / "resumes"


def test_default_output_dir_job_leaf(tmp_path: Path):
    src = tmp_path / "resumes" / "jenni" / "_exports" / "Netflix-App" / "doc.html"
    src.parent.mkdir(parents=True)
    src.write_text("<p></p>", encoding="utf-8")
    assert (
        paths.default_output_dir(src, root=tmp_path)
        == tmp_path / "output" / "jenni" / "resumes" / "Netflix-App"
    )


def test_default_output_dir_job_folder_beside_user(tmp_path: Path):
    src = tmp_path / "resumes" / "jenni" / "CZI" / "jenni-czi-letter.html"
    src.parent.mkdir(parents=True)
    src.write_text("<p></p>", encoding="utf-8")
    assert (
        paths.default_output_dir(src, root=tmp_path)
        == tmp_path / "output" / "jenni" / "resumes" / "CZI"
    )


def test_default_output_dir_collage_maps_user(tmp_path: Path):
    src = tmp_path / "collages" / "meet-jenni-bot" / "images" / "a.png"
    src.parent.mkdir(parents=True)
    src.write_text("x", encoding="utf-8")
    assert paths.default_output_dir(src, root=tmp_path) == tmp_path / "output" / "jenni" / "collages"


def test_default_output_dir_unknown_is_output_root(tmp_path: Path):
    src = tmp_path / "scratch" / "one-off.html"
    src.parent.mkdir(parents=True)
    src.write_text("<p></p>", encoding="utf-8")
    assert paths.default_output_dir(src, root=tmp_path) == tmp_path / "output"


def test_default_output_dir_examples_kind_at_root(tmp_path: Path):
    src = tmp_path / "examples" / "profiles" / "default-resume" / "resume.html"
    src.parent.mkdir(parents=True)
    src.write_text("<p></p>", encoding="utf-8")
    assert paths.default_output_dir(src, root=tmp_path) == tmp_path / "output" / "examples"
