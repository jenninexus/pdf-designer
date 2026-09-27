"""Inline ``{{img:name}}`` placeholders and shrink photos for board-sized PDFs.

Chromium's ``page.pdf()`` decodes WebP/PNG data URIs and re-embeds them as
large bitmaps, so a 3 MB self-contained HTML can become a 23 MB PDF that
Indeed (and similar portals) reject. Re-encoding as JPEG at print resolution
lets Chromium pass the JPEG through, which is how we stay under a 5 MB cap.
"""

from __future__ import annotations

import argparse
import base64
import mimetypes
import re
from io import BytesIO
from pathlib import Path
from urllib.parse import unquote

from PIL import Image

# Indeed / Greenhouse / many ATS "additional documents" caps.
BOARD_MAX_MB = 5
# ~150 dpi on a ~7.3in content box; plenty sharp on Letter, small in the PDF.
BOARD_MAX_EDGE = 960
BOARD_JPEG_QUALITY = 80

_PLACEHOLDER = re.compile(r"\{\{img:([^}]+)\}\}")


def encode_image_bytes(
    data: bytes,
    *,
    source_name: str = "image",
    max_edge: int | None = None,
    jpeg_quality: int | None = None,
) -> tuple[str, bytes]:
    """Return ``(mime, bytes)`` ready to put in a data URI.

    When ``max_edge`` or ``jpeg_quality`` is set, decode and re-encode as JPEG
    (RGB, optimized). Otherwise pass the original bytes through with a guessed MIME.
    """
    if max_edge is None and jpeg_quality is None:
        mime, _ = mimetypes.guess_type(source_name)
        if not mime:
            suffix = Path(source_name).suffix.lower()
            mime = "image/webp" if suffix == ".webp" else "image/png"
        return mime, data

    image = Image.open(BytesIO(data))
    if image.mode not in ("RGB", "L"):
        image = image.convert("RGB")
    elif image.mode == "L":
        image = image.convert("RGB")
    if max_edge and max(image.size) > max_edge:
        image.thumbnail((max_edge, max_edge), Image.Resampling.LANCZOS)
    buf = BytesIO()
    quality = 82 if jpeg_quality is None else jpeg_quality
    image.save(buf, format="JPEG", quality=quality, optimize=True)
    return "image/jpeg", buf.getvalue()


def data_uri_for_path(
    path: Path | str,
    *,
    max_edge: int | None = None,
    jpeg_quality: int | None = None,
) -> str:
    path = Path(path)
    mime, payload = encode_image_bytes(
        path.read_bytes(),
        source_name=path.name,
        max_edge=max_edge,
        jpeg_quality=jpeg_quality,
    )
    b64 = base64.b64encode(payload).decode("ascii")
    return f"data:{mime};base64,{b64}"


def inline_placeholders(
    html: str,
    mapping: dict[str, Path | str],
    *,
    max_edge: int | None = None,
    jpeg_quality: int | None = None,
) -> str:
    """Replace every ``{{img:name}}`` using ``mapping``. Fail loudly on gaps."""
    paths = {key: Path(value) for key, value in mapping.items()}
    missing: list[str] = []
    names = set(_PLACEHOLDER.findall(html))
    for name in names:
        if name not in paths:
            missing.append(name)
            continue
        if not paths[name].is_file():
            missing.append(f"{name} -> {paths[name]} (FILE NOT FOUND)")
    if missing:
        raise FileNotFoundError("Missing work-sample assets: " + "; ".join(missing))

    def repl(match: re.Match[str]) -> str:
        key = match.group(1)
        return data_uri_for_path(
            paths[key], max_edge=max_edge, jpeg_quality=jpeg_quality
        )

    out = _PLACEHOLDER.sub(repl, html)
    leftover = _PLACEHOLDER.findall(out)
    if leftover:
        raise ValueError(f"Leftover placeholders: {leftover}")
    return out


_LOCAL_IMG = re.compile(r'(<img\b[^>]*?\bsrc=")([^"]+)(")', re.IGNORECASE)
_NOT_LOCAL = ("data:", "http:", "https:", "//", "{{", "#", "mailto:", "blob:")


def inline_local_srcs(
    html: str,
    base_dir: Path | str,
    *,
    max_edge: int | None = None,
    jpeg_quality: int | None = None,
) -> str:
    """Inline every ``<img src="relative/path">`` that points at a local file.

    Lets a template reference the asset SSOT directly (for example
    ``../../resumes/<user>/resources/images/project-hero.webp``), so it
    previews correctly in a browser or the Design Hub before inlining. Fails loudly
    on a relative path that does not resolve — a silently dropped image is the defect.
    """
    base = Path(base_dir)
    missing: list[str] = []

    def repl(match: re.Match[str]) -> str:
        src = match.group(2).strip()
        if src.lower().startswith(_NOT_LOCAL):
            return match.group(0)
        path = (base / unquote(src)).resolve()
        if not path.is_file():
            missing.append(f"{src} -> {path}")
            return match.group(0)
        uri = data_uri_for_path(path, max_edge=max_edge, jpeg_quality=jpeg_quality)
        return f"{match.group(1)}{uri}{match.group(3)}"

    out = _LOCAL_IMG.sub(repl, html)
    if missing:
        raise FileNotFoundError("Missing local image sources: " + "; ".join(missing))
    return out


def inline_template_file(
    template: Path | str,
    dest: Path | str,
    mapping: dict[str, Path | str],
    *,
    max_edge: int | None = None,
    jpeg_quality: int | None = None,
) -> Path:
    """Inline ``{{img:name}}`` placeholders AND relative ``<img src>`` paths."""
    template = Path(template)
    dest = Path(dest)
    html = inline_placeholders(
        template.read_text(encoding="utf-8"),
        mapping,
        max_edge=max_edge,
        jpeg_quality=jpeg_quality,
    )
    html = inline_local_srcs(html, template.parent, max_edge=max_edge, jpeg_quality=jpeg_quality)
    dest.write_text(html, encoding="utf-8")
    return dest


def pdf_size_mb(path: Path | str) -> float:
    return Path(path).stat().st_size / (1024 * 1024)


def assert_pdf_under_mb(path: Path | str, max_mb: float = BOARD_MAX_MB) -> None:
    size = pdf_size_mb(path)
    if size > max_mb:
        raise SystemExit(
            f"{path} is {size:.2f} MB — over the {max_mb:g} MB board cap. "
            "Re-inline with --max-edge 960 --jpeg-quality 80 "
            "(python -m pdf_tool.inline_images) and re-export."
        )


def _parse_mapping(pairs: list[str]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for arg in pairs:
        if "=" not in arg:
            raise SystemExit(f"expected name=path, got {arg!r}")
        key, value = arg.split("=", 1)
        mapping[key] = value
    return mapping


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m pdf_tool.inline_images",
        description=(
            "Inline {{img:name}} placeholders and relative <img src> paths for a "
            "self-contained work-samples HTML."
        ),
    )
    parser.add_argument("template")
    parser.add_argument("out")
    parser.add_argument(
        "images",
        nargs="*",
        help="name=path pairs matching {{img:name}} placeholders",
    )
    parser.add_argument(
        "--max-edge",
        type=int,
        default=None,
        help=f"longest pixel edge after resize (board default: {BOARD_MAX_EDGE})",
    )
    parser.add_argument(
        "--jpeg-quality",
        type=int,
        default=None,
        help=f"re-encode as JPEG at this quality (board default: {BOARD_JPEG_QUALITY})",
    )
    parser.add_argument(
        "--board",
        action="store_true",
        help=f"Indeed-class pack: --max-edge {BOARD_MAX_EDGE} --jpeg-quality {BOARD_JPEG_QUALITY}",
    )
    # Intermixed: accept --board before OR after the name=path pairs.
    args = parser.parse_intermixed_args(argv)
    max_edge = BOARD_MAX_EDGE if args.board and args.max_edge is None else args.max_edge
    jpeg_quality = (
        BOARD_JPEG_QUALITY if args.board and args.jpeg_quality is None else args.jpeg_quality
    )
    dest = inline_template_file(
        args.template,
        args.out,
        _parse_mapping(args.images),
        max_edge=max_edge,
        jpeg_quality=jpeg_quality,
    )
    print(
        f"OK wrote {dest} ({dest.stat().st_size:,} bytes"
        + (f", max-edge={max_edge}" if max_edge else "")
        + (f", jpeg-q={jpeg_quality}" if jpeg_quality else "")
        + ")"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
