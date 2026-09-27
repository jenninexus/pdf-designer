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


def test_inline_local_srcs_inlines_relative_and_skips_remote(tmp_path: Path):
    from pdf_tool.inline_images import inline_local_srcs

    assets = tmp_path / "assets"
    assets.mkdir()
    Image.new("RGB", (64, 36), (10, 10, 10)).save(assets / "shot one.png", format="PNG")
    html = (
        '<img alt="a" src="assets/shot%20one.png">'
        '<img src="https://example.com/x.png">'
        '<img src="data:image/png;base64,AAAA">'
    )
    out = inline_local_srcs(html, tmp_path, max_edge=32, jpeg_quality=70)
    assert '<img alt="a" src="data:image/jpeg;base64,' in out
    assert 'src="https://example.com/x.png"' in out
    assert 'src="data:image/png;base64,AAAA"' in out

    try:
        inline_local_srcs('<img src="assets/missing.webp">', tmp_path)
    except FileNotFoundError as exc:
        assert "missing.webp" in str(exc)
    else:
        raise AssertionError("expected missing-local-src error")


def test_cli_accepts_board_after_pairs(tmp_path: Path):
    from pdf_tool.inline_images import main

    shot = tmp_path / "s.png"
    Image.new("RGB", (64, 36), (10, 10, 10)).save(shot, format="PNG")
    tpl = tmp_path / "t.html"
    tpl.write_text('<img src="{{img:s}}"><img src="s.png">', encoding="utf-8")
    out = tmp_path / "o.html"
    assert main([str(tpl), str(out), f"s={shot}", "--board"]) == 0
    text = out.read_text(encoding="utf-8")
    assert text.count("data:image/jpeg;base64,") == 2
