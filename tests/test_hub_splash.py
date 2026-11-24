"""Design Hub launch title screen is on every hub chrome page."""

from http.server import ThreadingHTTPServer
from pathlib import Path
from threading import Thread

import pytest

from pdf_tool.preview import APP_HTML, load_palettes, make_handler, scan_documents

ROOT = Path(__file__).resolve().parents[1] / "src" / "pdf_tool" / "static"
SKIP = 'classList.add("hub-splash-skip")'
MARK = 'id="hubSplash"'
SCRIPT = 'src="/_hub/splash.js"'


def test_splash_assets_and_hub_pages_include_title_screen():
    css = (ROOT / "hub.css").read_text(encoding="utf-8")
    js = (ROOT / "splash.js").read_text(encoding="utf-8")
    assert ".hub-splash" in css
    assert "hub-splash-mark" in css
    assert "pdf-designer.hub.splash" in js
    assert "MAX_MS" in js
    assert "hubSplashOpen" in js
    assert "Math.min(2700" in js
    assert "Math.min(180" in js
    assert "MAX_MS - EXIT_MS - (performance.now() - started)" in js
    assert "hub-splash-load 2.4s" in css
    assert ".hub-splash-open" in css

    pages = [APP_HTML]
    for name in ("wizard.html", "vault.html", "recipes.html"):
        pages.append((ROOT / name).read_text(encoding="utf-8"))
    for html in pages:
        assert SKIP in html
        assert MARK in html
        assert SCRIPT in html
        assert ">P</span>" in html
        assert ">D</span>" in html
        assert ">F</span>" in html
        assert 'id="hubSplashOpen"' in html
        assert 'id="hubSplashWizard"' in html
        assert "Enter to skip" not in html


def test_splash_auto_advances_preserving_deep_links_and_support_is_post_launch():
    js = (ROOT / "splash.js").read_text(encoding="utf-8")
    assert "deadline = setTimeout" in js
    assert "if (reduced.matches) { dismiss(); return; }" in js
    assert "el.inert = true" in js
    assert "el.inert = inert" in js
    assert "splash.addEventListener(\"click\"" not in js
    assert "dismiss();" in js
    assert "dismiss('/wizard')" in js
    for markup in [APP_HTML, *[(ROOT / name).read_text(encoding="utf-8") for name in ("wizard.html", "vault.html", "recipes.html")]]:
        splash_region = markup.split('id="hubSplash"', 1)[1].split("<header", 1)[0]
        assert "hub-support" not in splash_region
        assert 'src="/_hub/hub-aesyna.css"' not in splash_region
        assert 'href="/_hub/hub-aesyna.css"' in markup
        assert 'class="hub-support' in markup


def test_compact_navigation_keeps_modes_reachable_and_drawer_focus_contained(tmp_path):
    playwright = pytest.importorskip("playwright.sync_api")
    handler = make_handler(tmp_path, scan_documents(tmp_path), load_palettes(tmp_path))
    with ThreadingHTTPServer(("127.0.0.1", 0), handler) as server:
        runner = Thread(target=server.serve_forever, daemon=True)
        runner.start()
        origin = f"http://127.0.0.1:{server.server_port}"
        try:
            with playwright.sync_playwright() as driver:
                browser = driver.chromium.launch()
                page = browser.new_page(
                    viewport={"width": 320, "height": 568},
                    is_mobile=True, has_touch=True, reduced_motion="reduce",
                )
                for route in ("/", "/recipes", "/vault", "/wizard"):
                    page.goto(f"{origin}{route}?no-splash=1")
                    modes = page.locator(".hub-modes a")
                    assert modes.all_inner_texts() == ["Library", "Recipes", "Vault", "Wizard"]
                    assert page.evaluate("document.documentElement.scrollWidth") == 320
                    for mode in modes.all():
                        box = mode.bounding_box()
                        assert box["width"] >= 44 and box["height"] >= 44
                        assert box["x"] >= 0 and box["x"] + box["width"] <= 320

                    toggle = page.locator("#drawerToggle")
                    drawer = page.locator("#hubDrawer")
                    toggle.click()
                    assert drawer.evaluate("(el) => getComputedStyle(el).transitionDuration") == "0s"
                    assert drawer.locator("[aria-current=page]").count() == 1
                    assert page.locator(".hub-bar").evaluate("(el) => el.inert")
                    assert page.evaluate("document.activeElement.id") == "drawerClose"
                    page.keyboard.press("Shift+Tab")
                    assert drawer.evaluate("(el) => el.contains(document.activeElement)")
                    page.keyboard.press("Escape")
                    assert page.evaluate("document.activeElement.id") == "drawerToggle"
                    assert drawer.evaluate("(el) => el.inert")

                page.set_viewport_size({"width": 991, "height": 800})
                toggle.click()
                drawer_width = drawer.bounding_box()["width"]
                assert drawer_width < 991
                page.mouse.click((991 - drawer_width) / 2, 400)
                assert drawer.evaluate("(el) => el.inert")
                assert page.evaluate("document.activeElement.id") == "drawerToggle"
                toggle.click()
                page.set_viewport_size({"width": 992, "height": 800})
                page.wait_for_function("document.querySelector('#hubDrawer').inert")
                assert not toggle.is_visible()
                assert page.locator(".hub-brand").first.evaluate("(el) => el === document.activeElement")
                browser.close()
        finally:
            server.shutdown()
            runner.join()
