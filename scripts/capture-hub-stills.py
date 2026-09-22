#!/usr/bin/env python3
"""Recapture public Design Hub stills into docs/images/.

Clone-safe pages (Library, Recipes, Vault, Wizard) are served from a temporary
git-tracked checkout so the shots match a fresh clone: Jane Example only, no
local vaults or job listings. Hub chrome still comes from this working tree
(``src/pdf_tool/static``), so Wizard, centered Open, and tip icons are current.

The optional Jennifer Nexus peek still is captured from the real workspace
only when that gitignored screenshot pack exists on disk.

    python scripts/capture-hub-stills.py
    python scripts/capture-hub-stills.py --skip-nexus
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

from pdf_tool.preview import serve

REPO = Path(__file__).resolve().parents[1]
IMAGES = REPO / "docs" / "images"
ARCHIVE = IMAGES / "_archive" / "2026-08-22-public-set"
NEXUS_RESUME = REPO / "resumes" / "jenni-nexus" / "defaults" / "jenni-nexus-resume.html"

VIEWPORT = {"width": 1440, "height": 900}

PRIVATE_MARKERS = (
    "resumes/jenni/",
    "resumes/shade/",
    "vaults/jenni",
    "vaults/shade",
    "_job-apps",
    "jenni-resume",
    "shade-resume",
    "jenni-nexus",
    "personal vault",
)


def wait_http(url: str, timeout: float = 90.0) -> None:
    deadline = time.time() + timeout
    last = None
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=2) as resp:
                if resp.status == 200:
                    return
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            last = exc
        time.sleep(0.2)
    raise SystemExit(f"Hub did not respond at {url}: {last}")


def archive_current() -> None:
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    for name in ("hub-library.png", "hub-recipes.png", "hub-vault.png", "hub-start.png"):
        src = IMAGES / name
        dest = ARCHIVE / name
        if src.exists() and not dest.exists():
            shutil.copy2(src, dest)
            print(f"archived {name} -> {dest.relative_to(REPO)}")


def public_clone() -> Path:
    tmp = Path(tempfile.mkdtemp(prefix="pdf-hub-public-"))
    prefix = str(tmp).replace("\\", "/") + "/"
    subprocess.run(
        ["git", "checkout-index", "-a", f"--prefix={prefix}"],
        cwd=REPO,
        check=True,
    )
    return tmp


def start_hub(root: Path, port: int, name: str) -> threading.Thread:
    thread = threading.Thread(
        target=serve,
        kwargs={"root": str(root), "port": port, "open_browser": False},
        daemon=True,
        name=name,
    )
    thread.start()
    wait_http(f"http://127.0.0.1:{port}/")
    print(f"Hub {name} at http://127.0.0.1:{port}/ root={root}")
    return thread


def assert_clone_safe(page, label: str) -> None:
    text = page.inner_text("body")
    hits = [marker for marker in PRIVATE_MARKERS if marker.lower() in text.lower()]
    if hits:
        raise SystemExit(f"{label} leaked private workspace markers: {hits}")
    nav = page.inner_text("header .hub-nav")
    if "Wizard" not in nav:
        raise SystemExit(f"{label}: expected Wizard in the header nav, got {nav!r}")
    if "Start" in nav.split():
        raise SystemExit(f"{label}: header still shows a Start tab")


def new_page(context, profile: str):
    page = context.new_page()
    page.add_init_script(
        f"""
        try {{
          localStorage.setItem("pdf-designer.hub.profileFilter", {profile!r});
          sessionStorage.setItem("pdf-designer.hub.splash", "1");
        }} catch (e) {{}}
        """
    )
    return page


def shot(page, url: str, dest: Path, *, wait_for: str) -> None:
    page.goto(url, wait_until="domcontentloaded")
    page.locator(wait_for).first.wait_for(state="visible", timeout=20000)
    page.wait_for_timeout(500)
    dest.parent.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(dest), full_page=False)
    print(f"wrote {dest.relative_to(REPO)} ({dest.stat().st_size} bytes)")


def capture_splash(context, base: str) -> None:
    page = context.new_page()
    page.add_init_script(
        """
        try { localStorage.setItem("pdf-designer.hub.profileFilter", "examples"); } catch (e) {}
        """
    )
    page.goto(f"{base}/?splash=1", wait_until="domcontentloaded")
    page.locator("#hubSplashOpen").wait_for(state="visible", timeout=20000)
    page.wait_for_timeout(3400)
    dest = IMAGES / "hub-splash.png"
    page.screenshot(path=str(dest), full_page=False)
    print(f"wrote {dest.relative_to(REPO)} ({dest.stat().st_size} bytes)")
    text = page.inner_text("#hubSplash").lower()
    if "open" not in text or "start wizard" not in text:
        raise SystemExit("splash still is missing Open / Start wizard")
    if "patreon" not in text:
        raise SystemExit("splash still is missing tip buttons")
    page.close()


def capture_public(base: str) -> None:
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        context = browser.new_context(
            viewport=VIEWPORT,
            device_scale_factor=1,
            color_scheme="dark",
        )
        capture_splash(context, base)
        page = new_page(context, "examples")

        shot(page, f"{base}/?no-splash=1", IMAGES / "hub-library.png", wait_for=".hub-home-card")
        assert_clone_safe(page, "library")
        shutil.copy2(IMAGES / "hub-library.png", IMAGES / "hub-home.png")
        print("wrote docs/images/hub-home.png (copy of hub-library.png)")

        shot(page, f"{base}/recipes?no-splash=1", IMAGES / "hub-recipes.png", wait_for="a.hub-open")
        assert_clone_safe(page, "recipes")

        shot(page, f"{base}/vault?no-splash=1", IMAGES / "hub-vault.png", wait_for="section.hub-card h2")
        assert_clone_safe(page, "vault")
        if "Jane Example" not in page.inner_text("body"):
            raise SystemExit("vault still is not showing Jane Example")

        shot(page, f"{base}/wizard?no-splash=1", IMAGES / "hub-start.png", wait_for="aside.wizard-support .hub-support-btn.patreon")
        assert_clone_safe(page, "wizard")
        body = page.inner_text("aside.wizard-support")
        if "Patreon" not in body or "PayPal" not in body:
            raise SystemExit("wizard still is missing donate buttons")

        browser.close()


def capture_nexus(base: str) -> None:
    if not NEXUS_RESUME.is_file():
        print("skip hub-resume-jennifer-nexus.png — jenni-nexus pack not on disk")
        return
    rel = NEXUS_RESUME.relative_to(REPO).as_posix()
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        context = browser.new_context(
            viewport=VIEWPORT,
            device_scale_factor=1,
            color_scheme="dark",
        )
        page = new_page(context, "jenni-nexus")
        page.goto(f"{base}/?doc={rel}&no-splash=1", wait_until="domcontentloaded")
        page.locator("#main").wait_for(state="visible", timeout=20000)
        frame = page.frame_locator("#main")
        frame.locator("h1").first.wait_for(state="visible", timeout=20000)
        heading = frame.locator("h1").first.inner_text()
        if "Jennifer Nexus" not in heading:
            raise SystemExit(f"nexus resume heading was {heading!r}")
        visible = page.inner_text("body")
        if "resumes/jenni/" in visible or "resumes/shade/" in visible or "_job-apps" in visible:
            raise SystemExit("nexus still leaked a private applicant path")
        dest = IMAGES / "hub-resume-jennifer-nexus.png"
        page.screenshot(path=str(dest), full_page=False)
        print(f"wrote {dest.relative_to(REPO)} ({dest.stat().st_size} bytes)")
        browser.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8791, help="Clone-safe Hub port")
    parser.add_argument("--nexus-port", type=int, default=8792)
    parser.add_argument("--skip-nexus", action="store_true")
    parser.add_argument("--splash-only", action="store_true")
    args = parser.parse_args()

    archive_current()
    if args.splash_only:
        start_hub(REPO, args.port, "splash")
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            context = browser.new_context(
                viewport=VIEWPORT,
                device_scale_factor=1,
                color_scheme="dark",
            )
            capture_splash(context, f"http://127.0.0.1:{args.port}")
            browser.close()
        return
    clone = public_clone()
    try:
        start_hub(clone, args.port, "public-clone")
        capture_public(f"http://127.0.0.1:{args.port}")
        if not args.skip_nexus:
            start_hub(REPO, args.nexus_port, "workspace")
            capture_nexus(f"http://127.0.0.1:{args.nexus_port}")
    finally:
        shutil.rmtree(clone, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
