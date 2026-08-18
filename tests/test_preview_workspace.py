"""Design Hub workspace discovery stays aligned with the dual-path resolver."""

from __future__ import annotations

import json
from pathlib import Path

from pdf_tool.preview import (
    APP_HTML,
    _hyphen_token_in_rel,
    available_profile_ids,
    classify_document,
    load_palettes,
    profile_options,
    resolve_preview_file,
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


def test_hyphen_token_matches_meet_jenni_bot_not_jennifer():
    assert _hyphen_token_in_rel(
        "storage/collages/meet-jenni-bot/images/_candidates/uniform-grid.html",
        "uniform-grid",
        "jenni",
    )
    assert _hyphen_token_in_rel("storage/jenni/defaults/jenni-default-resume.html", "jenni-default-resume", "jenni")
    assert not _hyphen_token_in_rel("examples/jennifer-letter.html", "jennifer-letter", "jenni")


def test_collage_project_token_tags_workspace_profile(tmp_path: Path):
    users = tmp_path / "storage" / "users"
    users.mkdir(parents=True)
    (users / "jenni.json").write_text(json.dumps({"id": "jenni"}), encoding="utf-8")
    collage = tmp_path / "storage" / "collages" / "meet-jenni-bot" / "_candidates"
    collage.mkdir(parents=True)
    (collage / "uniform-grid.html").write_text("<p>grid</p>", encoding="utf-8")
    resume = tmp_path / "storage" / "jenni" / "defaults"
    resume.mkdir(parents=True)
    (resume / "jenni-default-resume.html").write_text("<p>resume</p>", encoding="utf-8")

    docs = {doc["path"].replace("\\", "/"): doc for doc in scan_documents(tmp_path)}
    assert docs["storage/jenni/defaults/jenni-default-resume.html"]["profile"] == "jenni"
    assert docs["storage/collages/meet-jenni-bot/_candidates/uniform-grid.html"]["profile"] == "jenni"


def test_classify_fallback_tokens_without_workspace_card():
    tagged = classify_document(
        "storage/collages/meet-jenni-bot/_candidates/uniform-grid.html",
        "uniform-grid",
        (),
    )
    assert tagged["profile"] == "jenni"


def test_profile_card_without_html_still_appears_in_header(tmp_path: Path):
    profiles = tmp_path / "storage" / "profiles"
    profiles.mkdir(parents=True)
    (profiles / "studio-resume.json").write_text(json.dumps({"id": "studio-resume"}), encoding="utf-8")
    assert workspace_profile_ids(tmp_path) == ["studio"]
    assert available_profile_ids(tmp_path, []) == ["studio"]


def test_hub_js_restores_profile_before_folder_rebuild():
    assert "function applyProfileChange()" in APP_HTML
    assert "docsForProfile(activeProfile())" in APP_HTML
    assert 'id="hubHomeLink"' in APP_HTML
    assert 'const cur = sel ? sel.value : "";' in APP_HTML
    boot = APP_HTML.split("if (!openFromQuery())", 1)[0]
    assert boot.rfind("restoreHubPrefs") < boot.rfind("buildFolderSelect();")


def test_public_example_rel_tags_examples_profile():
    tagged = classify_document(
        "examples/profiles/default-resume/default-resume.html",
        "default-resume",
        (),
    )
    assert tagged["profile"] == "examples"
    assert tagged["kind"] == "resume"
    assert tagged["bucket"] == "examples"
    work = classify_document(
        "profiles/default-work-examples/default-work-examples.html",
        "default-work-examples",
        (),
    )
    assert work["profile"] == "examples"
    assert work["kind"] == "work-samples"


def test_examples_profile_sorts_first(tmp_path: Path):
    users = tmp_path / "users"
    users.mkdir()
    (users / "alex.json").write_text(json.dumps({"id": "alex"}), encoding="utf-8")
    (users / "examples.json").write_text(json.dumps({"id": "examples"}), encoding="utf-8")
    assert workspace_profile_ids(tmp_path) == ["examples", "alex"]


def test_scan_skips_archive_and_template_html(tmp_path: Path):
    (tmp_path / "resumes" / "alex" / "defaults").mkdir(parents=True)
    (tmp_path / "resumes" / "alex" / "defaults" / "alex-resume.html").write_text("<p>ok</p>", encoding="utf-8")
    (tmp_path / "resumes" / "alex" / "defaults" / "alex-resume.template.html").write_text("<p>tmpl</p>", encoding="utf-8")
    archived = tmp_path / "_archive" / "old"
    archived.mkdir(parents=True)
    (archived / "ghost-resume.html").write_text("<p>ghost</p>", encoding="utf-8")
    nested = tmp_path / "storage" / "_archive" / "dupes"
    nested.mkdir(parents=True)
    (nested / "ghost-cover.html").write_text("<p>ghost</p>", encoding="utf-8")

    docs = {doc["path"].replace("\\", "/") for doc in scan_documents(tmp_path)}
    assert docs == {"resumes/alex/defaults/alex-resume.html"}


def test_resolve_preview_file_follows_storage_alias(tmp_path: Path):
    live = tmp_path / "resumes" / "alex" / "defaults"
    live.mkdir(parents=True)
    (live / "alex-resume.html").write_text("<p>live</p>", encoding="utf-8")
    got = resolve_preview_file(tmp_path, "storage/alex/defaults/alex-resume.html")
    assert got == (live / "alex-resume.html").resolve()
    assert resolve_preview_file(tmp_path, "missing.html") is None


def test_public_examples_cover_each_hub_kind():
    root = Path(__file__).resolve().parents[1]
    docs = scan_documents(root / "examples")
    by_kind: dict[str, list[str]] = {}
    for doc in docs:
        by_kind.setdefault(doc["kind"], []).append(doc["path"].replace("\\", "/"))
    assert any("default-resume" in path for path in by_kind.get("resume", []))
    assert any("cover-letter" in path for path in by_kind.get("cover-letter", []))
    assert any("letter" in path.lower() for path in by_kind.get("letter", []))
    assert any("work-example" in path for path in by_kind.get("work-samples", []))
    assert any("collage" in path for path in by_kind.get("collage", []))
    assert any(path.endswith("_candidates/index.html") for path in by_kind.get("gallery", []))
    assert all(doc.get("profile") == "examples" for doc in docs)
