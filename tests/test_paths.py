"""pdf_tool.paths.repo_root — checkout vs bundled share discovery."""

from __future__ import annotations

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
