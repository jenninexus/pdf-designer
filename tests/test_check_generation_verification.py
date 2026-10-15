"""A missing renderer must not turn a shipping gate green."""
from pdf_tool import check_generation as gate


def test_required_render_failure_cannot_pass(tmp_path, monkeypatch):
    source = tmp_path / "resume.html"
    source.write_text("<p>Resume</p>", encoding="utf-8")
    monkeypatch.setattr(gate, "CHECKS", [
        ("ats-text", "required text extraction", lambda p: (True, ["(skipped render — browser missing)"]), False)
    ])
    report = gate.run_file(source)
    assert report["passed"] is False
    assert "Required check did not run" in report["checks"][0]["messages"][0]


def test_explicit_source_only_mode_is_labelled(tmp_path, monkeypatch):
    source = tmp_path / "resume.html"
    source.write_text("<p>Resume</p>", encoding="utf-8")
    def should_not_run(path):
        raise AssertionError("source-only must not launch the renderer")
    monkeypatch.setattr(gate, "CHECKS", [("ats-text", "text extraction", should_not_run, False)])
    report = gate.run_file(source, do_render=False)
    assert report["mode"] == "source-only"
    assert report["checks"][0]["skipped"] is True


def test_non_applicable_resume_check_is_not_a_render_failure(tmp_path, monkeypatch):
    source = tmp_path / "cover-letter.html"
    source.write_text("<p>Letter</p>", encoding="utf-8")
    monkeypatch.setattr(gate, "CHECKS", [
        ("ats-text", "resume check", lambda p: (True, ["(not a résumé — skipped)"]), False)
    ])
    assert gate.run_file(source)["passed"] is True
