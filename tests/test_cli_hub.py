"""The CLI hub is the product's front door — it must never die on a console encoding.

Regression guard for a real failure: ``python -m pdf_tool`` (the first command in
``AGENTS.md``) crashed with ``UnicodeEncodeError`` on a Windows cp1252 console because
its own help text contained "≤". A stray non-Latin-1 glyph anywhere in `_COMMANDS`
reintroduces it, so assert the text is plain ASCII rather than trusting review.
"""

from __future__ import annotations

import io

import pytest

from pdf_tool.__main__ import _COMMANDS, _help_text, main


def test_help_text_is_console_encodable() -> None:
    """cp1252 is what a Windows console gives us — that is the real constraint.

    Em dashes and accented characters are fine (cp1252 has them, and the house style
    uses them); the glyph that actually crashed the hub was "≤" (U+2264), which cp1252
    cannot represent. Anything outside cp1252 raises here instead of at a user's terminal.
    """
    _help_text().encode("cp1252")


def test_every_command_has_a_blurb() -> None:
    for name, blurb in _COMMANDS:
        assert name and not name.startswith("-"), f"bad command name: {name!r}"
        assert blurb.strip(), f"missing blurb for {name!r}"


def test_bare_invoke_prints_help_and_exits_zero(capsys: pytest.CaptureFixture[str]) -> None:
    assert main([]) == 0
    out = capsys.readouterr().out
    assert "Commands:" in out
    assert "pdf-designer engine" in out


def test_unknown_command_exits_two(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["definitely-not-a-command"]) == 2
    assert "Unknown subcommand" in capsys.readouterr().out


def test_module_form_hint_exits_two(capsys: pytest.CaptureFixture[str]) -> None:
    """`python -m pdf_tool track` should point at the module form, not silently run."""
    assert main(["tracker"]) == 2
    assert "python -m pdf_tool.tracker" in capsys.readouterr().out


def test_help_survives_an_ascii_only_console(monkeypatch: pytest.MonkeyPatch) -> None:
    """With a cp1252 stdout, printing help must not raise."""
    strict = io.TextIOWrapper(io.BytesIO(), encoding="cp1252", errors="strict")
    monkeypatch.setattr("sys.stdout", strict)
    try:
        assert main([]) == 0
    finally:
        strict.flush()
