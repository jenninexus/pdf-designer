"""The Windows launcher stays a local shell around the existing preview server."""

from pathlib import Path


def test_windows_launcher_is_loopback_only_and_waits_for_design_hub():
    root = Path(__file__).resolve().parents[1]
    launcher = (root / "scripts" / "launch-design-hub.ps1").read_text(encoding="utf-8")
    workspace_entry = (root / "scripts" / "ensure-design-hub.ps1").read_text(encoding="utf-8")
    assert "127.0.0.1" in launcher
    assert "-m pdf_tool.preview" in launcher
    assert "--no-open" in launcher
    assert "<title>.*Design Hub" in launcher
    assert "Start-Process $url" in launcher
    assert "cloud" in launcher.lower()
    assert "launch-design-hub.ps1" in workspace_entry


def test_launcher_acceptance_spec_covers_local_data_and_breakpoint_matrix():
    root = Path(__file__).resolve().parents[1]
    doc = (root / "docs" / "_archive" / "WINDOWS-LAUNCHER.md").read_text(encoding="utf-8")
    for width in (390, 576, 768, 992, 1200, 1400, 1920, 2560, 3840):
        assert str(width) in doc
    assert "127.0.0.1" in doc
    assert "second renderer" in doc
    assert "cloud" in doc.lower()
