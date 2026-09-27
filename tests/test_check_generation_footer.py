"""Control-test footer-collision both directions (docs/QA.md rule 5).

A guard only ever verified against clean input proves nothing — this fixture
reconstructs the known-bad Tools-under-signature case and MUST FAIL.
"""

from __future__ import annotations

from pathlib import Path

from pdf_tool.check_generation import check_footer_collision

FIXTURE = Path(__file__).parent / "fixtures" / "known-bad-footer-overlap.html"


def test_footer_collision_fails_known_bad_overlap():
    assert FIXTURE.is_file(), f"missing fixture: {FIXTURE}"
    ok, msgs = check_footer_collision(FIXTURE)
    assert ok is False, "known-bad overlap fixture must FAIL footer-collision"
    assert any("overlaps the pinned signature" in m for m in msgs), msgs


GOOD_FIXTURE = Path(__file__).parent / "fixtures" / "known-good-probe-on-text.html"


def test_footer_collision_passes_when_mid_page_is_text_dense():
    """The background must be the page's modal colour, not whatever glyph sits at (inset, H/2)."""
    assert GOOD_FIXTURE.is_file(), f"missing fixture: {GOOD_FIXTURE}"
    ok, msgs = check_footer_collision(GOOD_FIXTURE)
    assert ok is True, msgs
