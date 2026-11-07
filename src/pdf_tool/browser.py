"""Locate the one Chromium binary used by PDF Designer exports.

Normal developer and wheel installs let Playwright resolve its own browser.
The Windows desktop runtime is frozen with a copied Playwright Chromium beside
its executable, so it supplies that executable path explicitly instead of
depending on a user environment variable or a second rendering engine.
"""

from __future__ import annotations

import sys
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit


DOCUMENT_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".gif": "image/gif",
    ".svg": "image/svg+xml",
    ".woff": "font/woff",
    ".woff2": "font/woff2",
    ".ttf": "font/ttf",
    ".otf": "font/otf",
    ".pdf": "application/pdf",
}

# Allow the trusted Hub to style and size its preview, without giving document
# code script execution, embedded frames, form submission, or external assets.
DOCUMENT_CSP = (
    "sandbox allow-same-origin; default-src 'none'; "
    "style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self' data:; "
    "base-uri 'none'; form-action 'none'; frame-ancestors 'self'"
)


def open_render_document(
    browser, source: Path, *, workspace: Path | None = None, resolve_asset=None,
    wait_until="load", **page_options,
):
    """Open a trusted CLI file or an isolated Hub render with local assets only."""
    if workspace is None:
        page = browser.new_page(**page_options)
        page.goto(source.as_uri(), wait_until=wait_until)
        return page

    # Serve the browser from a virtual origin. It never opens file: URLs and
    # every request must resolve through the Hub's workspace asset boundary.
    origin = "https://pdf-designer.invalid"
    page = browser.new_page(java_script_enabled=False, service_workers="block", **page_options)

    def serve_asset(route):
        request = route.request
        url = urlsplit(request.url)
        if f"{url.scheme}://{url.netloc}" != origin or request.method != "GET":
            route.abort()
            return
        target = resolve_asset(unquote(url.path).lstrip("/"))
        if request.is_navigation_request():
            allowed = target == source and request.frame == page.main_frame
        else:
            allowed = target is not None and request.resource_type in {"stylesheet", "image", "font"}
        if not allowed:
            route.abort()
            return
        route.fulfill(path=target, headers={
            "Content-Type": DOCUMENT_TYPES[target.suffix.lower()],
            "Content-Security-Policy": DOCUMENT_CSP,
            "X-Content-Type-Options": "nosniff",
            "X-DNS-Prefetch-Control": "off",
        })

    page.context.route("**/*", serve_asset)
    page.goto(origin + "/" + quote(source.relative_to(workspace).as_posix()), wait_until=wait_until)
    return page


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
