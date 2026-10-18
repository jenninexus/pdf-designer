"""check_generation learns who a document belongs to from the workspace, not from engine constants."""
import json

from pdf_tool import check_generation as gate


def _workspace(root):
    (root / "users").mkdir()
    (root / "profiles").mkdir()
    (root / "resumes" / "jane").mkdir(parents=True)
    (root / "users" / "jane.json").write_text(json.dumps({
        "id": "jane", "aliases": ["jane", "jd"], "name": "Jane Doe",
        "contact": {"email": "jane@janedoe.test", "emailPersonal": "jd@mail.test",
                    "signatureName": "Jane Doe", "emailPolicy": "use the default"},
    }), encoding="utf-8")
    (root / "users" / "jane-studio.json").write_text(json.dumps({
        "id": "jane-studio", "name": "Jane Studio", "contact": {"email": "hello@studio.test"},
    }), encoding="utf-8")
    (root / "users" / "examples.json").write_text(json.dumps({
        "id": "examples", "contact": {"email": "jane@example.com", "signatureName": "Jane Example"},
    }), encoding="utf-8")
    (root / "profiles" / "arcade-resume.json").write_text("{}", encoding="utf-8")
    return root


def test_folder_and_filename_resolve_to_workspace_ids(tmp_path):
    root = _workspace(tmp_path)
    assert gate._detect_user(root / "resumes" / "jane" / "x.html", "", root=root) == "jane"
    assert gate._detect_user(root / "out" / "jd-cover.html", "", root=root) == "jane"
    assert gate._detect_user(root / "out" / "arcade-resume.html", "", root=root) == "arcade"
    assert gate._detect_user(root / "collages" / "arcade-collage" / "grid.html", "", root=root) == "arcade"
    assert gate._detect_user(root / "collages" / "arcadeish" / "grid.html", "", root=root) is None


def test_longest_alias_wins(tmp_path):
    root = _workspace(tmp_path)
    assert gate._detect_user(root / "out" / "jane-studio-letter.html", "", root=root) == "jane-studio"


def test_content_matches_contact_email_then_signature(tmp_path):
    root = _workspace(tmp_path)
    doc = root / "out" / "letter.html"
    assert gate._detect_user(doc, "<a>JD@MAIL.TEST</a>", root=root) == "jane"
    assert gate._detect_user(doc, "<p class='sig'>Jane Doe</p>", root=root) == "jane"
    # prose under an email* key is not an address
    assert gate._detect_user(doc, "use the default", root=root) is None


def test_examples_seed_and_unknown_people_are_not_detected(tmp_path):
    root = _workspace(tmp_path)
    doc = root / "out" / "letter.html"
    assert gate._detect_user(doc, "<a>jane@example.com</a><p>Jane Example</p>", root=root) is None
    assert gate._detect_user(root / "examples" / "x.html", "", root=root) is None


def test_folders_above_the_workspace_never_match(tmp_path):
    checkout = tmp_path / "jane"  # the checkout itself sits in a folder named like a user
    checkout.mkdir()
    root = _workspace(checkout)
    assert gate._detect_user(root / "out" / "letter.html", "", root=root) is None


def test_empty_workspace_detects_nobody(tmp_path):
    assert gate._detect_user(tmp_path / "x.html", "<p>anyone@else.test</p>", root=tmp_path) is None


def test_engine_source_holds_no_personal_identifiers():
    import re
    from pathlib import Path

    source = Path(gate.__file__).read_text(encoding="utf-8").lower()
    detect = source[source.index("_email_re ="):source.index("def _no_magenta_for")]
    assert not re.search(r"[a-z0-9]@[a-z0-9]", detect), "an email address is hardcoded in the detector"
