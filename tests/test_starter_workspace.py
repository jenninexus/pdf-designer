"""Starter workspace writes gitignored person/vault/profile files and refuses reserved ids."""

from pathlib import Path

import pytest

from pdf_tool.seed_from_resume import draft_from_text
from pdf_tool.starter_workspace import save_starter
from tests.test_seed_from_resume import RESUME

ROOT = Path(__file__).resolve().parents[1]


def test_save_starter_writes_inferred_vault(tmp_path: Path):
    draft = draft_from_text(resume_text=RESUME, filenames=["alex-resume.txt"])
    result = save_starter(tmp_path, draft, slug="alex-rivera", template_root=ROOT)
    vault = (tmp_path / "vaults" / "alex-rivera.json").read_text(encoding="utf-8")
    user = (tmp_path / "users" / "alex-rivera.json").read_text(encoding="utf-8")
    assert result["ok"] is True
    assert '"confidence": "inferred"' in vault
    assert "roleTracks" in vault
    assert "roleTracks" in vault
    assert "alex@example.studio" in user
    assert (tmp_path / "profiles" / "alex-rivera-resume.json").is_file()


def test_save_starter_refuses_examples_slug(tmp_path: Path):
    draft = draft_from_text(resume_text=RESUME, filenames=["alex-resume.txt"])
    with pytest.raises(ValueError, match="examples"):
        save_starter(tmp_path, draft, slug="examples", template_root=ROOT)


def test_save_starter_refuses_existing_without_overwrite(tmp_path: Path):
    draft = draft_from_text(resume_text=RESUME, filenames=["alex-resume.txt"])
    save_starter(tmp_path, draft, slug="alex-rivera", template_root=ROOT)
    with pytest.raises(FileExistsError):
        save_starter(tmp_path, draft, slug="alex-rivera", template_root=ROOT)


def test_save_starter_creates_one_asset_home_and_exports_to_library(tmp_path: Path):
    import json

    draft = draft_from_text(resume_text=RESUME, filenames=["alex-resume.txt"])
    result = save_starter(tmp_path, draft, slug="alex-rivera", template_root=ROOT)
    assert result["assets"]["images"] == "resumes/alex-rivera/resources/images/"
    assert (tmp_path / "resumes/alex-rivera/resources/images").is_dir()
    assert (tmp_path / "resumes/alex-rivera/resources/logos").is_dir()
    assert (tmp_path / "resumes/alex-rivera/resources/videos").is_dir()
    assert (tmp_path / "resumes/alex-rivera/resources/references").is_dir()
    assert (tmp_path / "resumes/alex-rivera/resources/README.md").is_file()
    user = json.loads((tmp_path / "users/alex-rivera.json").read_text(encoding="utf-8"))
    assert user["portfolio"]["imagesDir"] == "resumes/alex-rivera/resources/images/"
    assert user["portfolio"]["videosDir"] == "resumes/alex-rivera/resources/videos/"
    assert user["portfolio"]["referencesDir"] == "resumes/alex-rivera/resources/references/"
    profile = json.loads((tmp_path / "profiles/alex-rivera-resume.json").read_text(encoding="utf-8"))
    assert profile["exports"]["dir"] == "../resumes/alex-rivera/"
