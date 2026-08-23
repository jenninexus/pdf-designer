"""Board-size JPEG inlining — Chromium PDF bloat guard."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path

from PIL import Image

from pdf_tool.inline_images import (
    BOARD_MAX_EDGE,
    encode_image_bytes,
    inline_placeholders,
)


def _png_bytes(width: int = 1600, height: int = 900) -> bytes:
    image = Image.new("RGB", (width, height), (40, 80, 160))
    buf = BytesIO()
    image.save(buf, format="PNG")
    return buf.getvalue()


def test_passthrough_keeps_png_mime():
    mime, payload = encode_image_bytes(_png_bytes(), source_name="hero.png")
    assert mime == "image/png"
    assert payload[:8] == b"\x89PNG\r\n\x1a\n"


def test_board_encode_is_jpeg_and_under_max_edge():
    mime, payload = encode_image_bytes(
        _png_bytes(1800, 1000),
        source_name="shot.webp",
        max_edge=BOARD_MAX_EDGE,
        jpeg_quality=80,
    )
    assert mime == "image/jpeg"
    out = Image.open(BytesIO(payload))
    assert max(out.size) <= BOARD_MAX_EDGE
    assert out.format == "JPEG"


def test_inline_placeholders_rewrites_and_fails_on_gap(tmp_path: Path):
    shot = tmp_path / "shot.jpg"
    Image.new("RGB", (64, 36), (10, 10, 10)).save(shot, format="JPEG")
    html = '<img src="{{img:shot.jpg}}">'
    out = inline_placeholders(html, {"shot.jpg": shot}, max_edge=32, jpeg_quality=70)
    assert out.startswith('<img src="data:image/jpeg;base64,')
    assert "{{img:" not in out

    try:
        inline_placeholders(html, {})
    except FileNotFoundError as exc:
        assert "shot.jpg" in str(exc)
    else:
        raise AssertionError("expected missing-placeholder error")
