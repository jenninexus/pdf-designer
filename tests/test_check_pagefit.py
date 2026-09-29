from __future__ import annotations

from pathlib import Path

import pytest

PIL = pytest.importorskip("PIL.Image")
from PIL import Image, ImageDraw  # noqa: E402

from pdf_tool.check_pagefit import EDGE_TOL, _page_ink, check_pagefit  # noqa: E402

W, H = 1224, 1584  # US Letter at 144 dpi


def _page(paper, mat, ink_at_top: bool):
    im = Image.new("RGB", (W, H), paper)
    d = ImageDraw.Draw(im)
    d.rectangle((100, 700, 1100, 1000), fill=mat)  # image mat across the mid-page probe line
    d.rectangle((200, 300, 900, 320), fill=mat)  # a line of body "text"
    if ink_at_top:
        d.rectangle((300, 0, 600, 3), fill=mat)
    return im


@pytest.mark.parametrize(
    "paper,mat",
    [((255, 255, 255), (8, 16, 21)), ((10, 19, 23), (241, 244, 247))],
    ids=["light-paper-dark-mat", "dark-paper-light-mat"],
)
def test_image_mat_is_not_edge_ink(paper, mat):
    rows, _, h, _ = _page_ink(_page(paper, mat, ink_at_top=False))
    assert min(rows) > EDGE_TOL
    assert max(rows) < h - EDGE_TOL


@pytest.mark.parametrize(
    "paper,mat",
    [((255, 255, 255), (8, 16, 21)), ((10, 19, 23), (241, 244, 247))],
    ids=["light", "dark"],
)
def test_real_edge_ink_is_flagged(paper, mat):
    rows, _, _, _ = _page_ink(_page(paper, mat, ink_at_top=True))
    assert min(rows) <= EDGE_TOL


def test_html_source_gets_a_clear_hint(tmp_path: Path):
    src = tmp_path / "letter.html"
    src.write_text("<html></html>", encoding="utf-8")
    ok, msgs = check_pagefit(src)
    assert not ok
    assert "exported PDF" in msgs[0]
