"""Export light PDFs for every public palette — palette shopping without the Hub.

Writes under ``_variants/<stem>/`` next to the source HTML (never overwrites;
uses the same ``-v2`` / ``-v3`` pattern as ``html_to_pdf``).

Public palettes = ``themes/default-resume.json`` + ``themes/presets/*.json``.
Each export injects that palette's *light* token map via ``css_vars`` and runs
the palette guard on the HTML (and on solid hexes in the token map).

Usage:
    python -m pdf_tool.variants path/to/document.html
    python -m pdf_tool.html_to_pdf path/to/document.html --variants
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from .html_to_pdf import _guard_palette, _next_available_path, export_html_to_pdf
from .paths import repo_root

_HEX = re.compile(r"#([0-9a-fA-F]{6})\b")
_REPO = repo_root()

# Nested theme-JSON block -> pdf-designer CSS custom properties (mirrors preview.py)
_TOKEN_MAP = [
    ("--bg", "backgrounds", "body"),
    ("--surface", "backgrounds", "surface"),
    ("--elevated", "backgrounds", "elevated"),
    ("--text", "text", "primary"),
    ("--dim", "text", "secondary"),
    ("--dim2", "text", "muted"),
    ("--border", "borders", "subtle"),
    ("--border2", "borders", "strong"),
    ("--primary", "accents", "primary"),
    ("--secondary", "accents", "secondary"),
    ("--accent", "accents", "accent"),
    ("--support", "accents", "support"),
]


def _vars_from_token_map(block: dict) -> dict:
    vars_ = {}
    for key, value in block.items():
        if not (isinstance(key, str) and key.startswith("--") and isinstance(value, str)):
            continue
        if "gradient" in value.lower():
            continue
        vars_[key] = value
    return vars_


def _vars_from_nested_mode(block: dict) -> dict:
    vars_ = {}
    for var, section, key in _TOKEN_MAP:
        value = block.get(section, {}).get(key) if isinstance(block.get(section), dict) else None
        if value and isinstance(value, str) and "gradient" not in value.lower():
            vars_[var] = value
    return vars_


def _public_light_palettes() -> list[tuple[str, Path, dict]]:
    """Return (id, path, light css_vars) for default + presets."""
    out: list[tuple[str, Path, dict]] = []
    files = [_REPO / "themes" / "default-resume.json"]
    presets = _REPO / "themes" / "presets"
    if presets.is_dir():
        files.extend(sorted(presets.glob("*.json")))

    for f in files:
        if not f.is_file():
            continue
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        tokens = data.get("tokens") if isinstance(data.get("tokens"), dict) else None
        light = tokens.get("light") if tokens else None
        if isinstance(light, dict):
            vars_ = _vars_from_token_map(light)
        else:
            block = data.get("light")
            vars_ = _vars_from_nested_mode(block) if isinstance(block, dict) else {}
        if not vars_:
            continue
        out.append((f.stem, f, vars_))
    return out


def _guard_palette_json(path: Path, vars_: dict) -> list[str]:
    """Return banned-color labels found in solid hex token values."""
    from .check_palette import classify

    hits = []
    for key, value in vars_.items():
        m = _HEX.search(value)
        if not m:
            continue
        verdict, label = classify(m.group(1).lower())
        if verdict == "banned":
            hits.append(f"{path.name} {key} #{m.group(1)} <- {label}")
    return hits


def export_variants(html_path: str | Path, skip_palette: bool = False) -> list[Path]:
    """Export one light PDF per public palette into ``_variants/<stem>/``."""
    html = Path(html_path).resolve()
    if not html.exists():
        raise FileNotFoundError(html)

    if not skip_palette:
        _guard_palette(str(html))

    palettes = _public_light_palettes()
    if not palettes:
        raise SystemExit("no public palettes found under themes/ + themes/presets/")

    out_dir = html.parent / "_variants" / html.stem
    out_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    for pid, ppath, vars_ in palettes:
        banned = [] if skip_palette else _guard_palette_json(ppath, vars_)
        if banned:
            print(f"BLOCKED palette {pid}:", file=sys.stderr)
            for b in banned:
                print(f"  {b}", file=sys.stderr)
            raise SystemExit(2)

        default_path = out_dir / f"{pid}.pdf"
        out_path = _next_available_path(default_path)
        result = export_html_to_pdf(
            str(html),
            pdf_path=str(out_path),
            css_vars=vars_,
        )
        written.append(result)
        print(f"Saved: {result}")

    return written


def main(argv: list[str] | None = None) -> int:
    raw = list(argv if argv is not None else sys.argv[1:])
    skip_palette = "--skip-palette-check" in raw
    args = [a for a in raw if a not in ("--skip-palette-check", "--variants")]
    if not args:
        print(__doc__)
        return 2
    try:
        export_variants(args[0], skip_palette=skip_palette)
    except ModuleNotFoundError:
        print(
            "Playwright is not installed yet. Run:\n"
            "  pip install playwright\n"
            "  playwright install chromium\n"
            "then re-run this command."
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
