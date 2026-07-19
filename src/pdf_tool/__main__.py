"""CLI hub — ``python -m pdf_tool`` lists commands; modules run as ``python -m pdf_tool.<name>``."""

from __future__ import annotations

import sys

from . import __version__

_COMMANDS: tuple[tuple[str, str], ...] = (
    ("html_to_pdf", "HTML -> PDF (light/dark; optional --variants)"),
    ("variants", "Light PDF per public palette -> _variants/"),
    ("merge_pdfs", "Merge PDFs into one bundle"),
    ("pdf_to_png", "Screenshot each .page for visual verify"),
    ("check_palette", "Reject brown / mustard / lime"),
    ("check_overflow", "Catch page overflow / pinned-footer collision"),
    ("check_vault", "Vault schema / --explain / --coverage"),
    ("check_ats", "ATS text-layer guard on light PDF"),
    ("audit_resume", "Diff rendered HTML vs vault omissions"),
    ("tracker", "List / status over storage/applications"),
    ("collage", "Collage candidates + picker gallery"),
    ("preview", "Design Hub (localhost previewer)"),
)

_KNOWN = {name for name, _ in _COMMANDS}


def _help_text() -> str:
    lines = [
        f"pdf-designer engine  v{__version__}",
        "",
        "Commands:",
    ]
    width = max(len(n) for n, _ in _COMMANDS)
    for name, blurb in _COMMANDS:
        lines.append(f"  {name:<{width}}  {blurb}")
    lines += [
        "",
        "Usage: python -m pdf_tool.<command> ...",
        "Docs: docs/SSOT.md | AGENTS.md",
    ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    """Print hub help. Exit 0 on bare invoke / --help; exit 2 on unknown argv[1]."""
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] in ("-h", "--help"):
        print(_help_text())
        return 0

    name = args[0]
    if name in _KNOWN:
        print(
            f"Unknown invocation: pass module as python -m pdf_tool.{name} ...\n"
            f"(not: python -m pdf_tool {name})"
        )
        print()
        print(_help_text())
        return 2

    print(f"Unknown subcommand: {name}")
    print()
    print(_help_text())
    return 2


def entry_hub() -> None:
    """console_scripts entry — propagates hub exit codes."""
    raise SystemExit(main())


# --- console_scripts wrappers (mains that require argv=) ---


def entry_check_palette() -> None:
    from .check_palette import main as _main

    raise SystemExit(_main(sys.argv[1:]))


def entry_check_vault() -> None:
    from .check_vault import main as _main

    raise SystemExit(_main(sys.argv[1:]))


def entry_check_ats() -> None:
    from .check_ats import main as _main

    raise SystemExit(_main(sys.argv[1:]))


def entry_tracker() -> None:
    from .tracker import main as _main

    raise SystemExit(_main())


def entry_variants() -> None:
    from .variants import main as _main

    raise SystemExit(_main())


if __name__ == "__main__":
    raise SystemExit(main())
