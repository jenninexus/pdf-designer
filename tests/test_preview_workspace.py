"""Design Hub workspace discovery stays aligned with the dual-path resolver."""

from __future__ import annotations

import json
from pathlib import Path

from pdf_tool.preview import (
    available_profile_ids,
    load_palettes,
    profile_options,
    scan_documents,
    workspace_profile_ids,
)


def test_workspace_profiles_drive_document_tags_and_header_options(tmp_path: Path):
    users = tmp_path / "storage" / "users"
    users.mkdir(parents=True)
    (users / "alex.json").write_text(json.dumps({"id": "alex"}), encoding="utf-8")
    applications = tmp_path / "storage" / "_job-listings" / "Example"
    applications.mkdir(parents=True)
    (applications / "alex-role-resume.html").write_text("<p>Alex</p>", encoding="utf-8")

    assert workspace_profile_ids(tmp_path) == ["alex"]
    docs = scan_documents(tmp_path)
    assert docs[0]["profile"] == "alex"
    assert available_profile_ids(tmp_path, docs) == ["alex"]
    assert profile_options(["alex"]) == '<option value="alex">alex</option>'


def test_custom_preview_root_contributes_its_private_brand_palette(tmp_path: Path):
    brand_dir = tmp_path / "brands"
    brand_dir.mkdir()
    (brand_dir / "alex.json").write_text(
        json.dumps({"tokens": {"dark": {"--primary": "#123456"}}}), encoding="utf-8"
    )

    palettes = load_palettes(tmp_path)
    assert ("alex", "dark") in {(palette["id"], palette["mode"]) for palette in palettes}
