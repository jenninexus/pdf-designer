"""Locate the one Chromium binary used by PDF Designer exports.

Normal developer and wheel installs let Playwright resolve its own browser.
The Windows desktop runtime is frozen with a copied Playwright Chromium beside
its executable, so it supplies that executable path explicitly instead of
depending on a user environment variable or a second rendering engine.
"""

from __future__ import annotations

import sys
from pathlib import Path


def bundled_chromium_path(executable: Path | None = None, *, frozen: bool | None = None) -> Path | None:
    """Return a bundled Windows Chromium when the app is frozen, if present."""
    if frozen is None:
        frozen = bool(getattr(sys, "frozen", False))
    if not frozen:
        return None
    runtime = (executable or Path(sys.executable)).resolve().parent
    candidates = sorted((runtime / "browsers").glob("chromium-*/chrome-win*/chrome.exe"))
    return candidates[0] if candidates else None


def chromium_launch_kwargs() -> dict[str, str]:
    """Give Playwright its packaged browser path only for a frozen runtime."""
    chromium = bundled_chromium_path()
    return {"executable_path": str(chromium)} if chromium else {}
