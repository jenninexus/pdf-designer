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

                page.goto(f"{origin}/?no-splash=1")
                bar = page.locator(".hub-bar")
                assert bar.evaluate("(el) => el.scrollWidth === el.clientWidth")
                assert page.locator("#exportBtn").evaluate("(el) => getComputedStyle(el).backgroundImage") == "none"

                page.goto(f"{origin}/recipes?no-splash=1")
                for width, wrap in ((1200, "1180px"), (1400, "1280px"), (1920, "1400px"), (3840, "1400px")):
                    page.set_viewport_size({"width": width, "height": 900})
                    assert page.locator(".hub-page-wrap").evaluate("(el) => getComputedStyle(el).maxWidth") == wrap
                browser.close()
        finally:
            server.shutdown()
            runner.join()


def test_pdf_reader_fits_real_spreads_and_preserves_manual_zoom(tmp_path):
    from pypdf import PdfWriter

    playwright = pytest.importorskip("playwright.sync_api")
    source = tmp_path / "_exports" / "fictional-review.pdf"
    source.parent.mkdir()
    writer = PdfWriter()
    for width, height in ((612, 792), (792, 612), (612, 792)):
        writer.add_blank_page(width=width, height=height)
    writer.write(source)
    handler = make_handler(tmp_path, scan_documents(tmp_path), load_palettes(tmp_path))

    with ThreadingHTTPServer(("127.0.0.1", 0), handler) as server:
        runner = Thread(target=server.serve_forever, daemon=True)
        runner.start()
        try:
            with playwright.sync_playwright() as driver:
                browser = driver.chromium.launch()
                page = browser.new_page(viewport={"width": 576, "height": 768})
                origin = f"http://127.0.0.1:{server.server_port}"
                page.goto(f"{origin}/pdf-viewer?doc=_exports/fictional-review.pdf")
                reader = page
                first = reader.get_by_role("img", name="PDF page 1", exact=True)
                assert first.evaluate("async (image) => { await image.decode(); return image.naturalWidth > 0; }")
                mode = reader.get_by_role("combobox", name="Reading mode")
                mode.select_option("two-up")
                second = reader.get_by_role("img", name="PDF page 2", exact=True)
                assert second.evaluate("async (image) => { await image.decode(); return image.naturalWidth > 0; }")
                assert abs(first.bounding_box()["y"] - second.bounding_box()["y"]) < 1
                assert first.evaluate("(image) => document.documentElement.scrollWidth <= document.documentElement.clientWidth")
                assert second.bounding_box()["x"] + second.bounding_box()["width"] < 576

                page.set_viewport_size({"width": 320, "height": 568})
                assert second.bounding_box()["y"] > first.bounding_box()["y"]
                assert first.evaluate("(image) => document.documentElement.scrollWidth <= document.documentElement.clientWidth")
                toolbar = reader.locator(".pdf-toolbar")
                assert toolbar.evaluate("(el) => el.scrollWidth === el.clientWidth")
                zoom_out = reader.get_by_role("button", name="Zoom out")
                assert zoom_out.bounding_box()["height"] == zoom_out.bounding_box()["width"] == 34
                assert zoom_out.evaluate("(el) => getComputedStyle(el).borderTopWidth") == "0px"
                reader.get_by_role("button", name="Next page").click()
                assert reader.get_by_role("spinbutton", name="Go to page").input_value() == "2"
                reader.get_by_role("button", name="Previous page").click()
                reader.get_by_role("button", name="Zoom in").click()
                zoomed_width = first.bounding_box()["width"]
                page.set_viewport_size({"width": 390, "height": 844})
                assert first.bounding_box()["width"] == zoomed_width
                fit = reader.get_by_role("button", name="Fit page width")
                assert fit.get_attribute("aria-pressed") == "false"
                fit.click()
                assert fit.get_attribute("aria-pressed") == "true"
                assert first.evaluate("""image => !image.dispatchEvent(new WheelEvent(
                    "wheel", { bubbles: true, cancelable: true, ctrlKey: true, deltaY: -100 }
                ))""")
                assert fit.get_attribute("aria-pressed") == "false"

                mode.select_option("single")
                reader.get_by_role("button", name="Next page").click()
                assert second.is_visible() and not first.is_visible()
                original = reader.get_by_role("link", name="Open original PDF in browser viewer")
                assert original.get_attribute("href") == "/_exports/fictional-review.pdf"
                assert page.request.get(origin + original.get_attribute("href")).body() == source.read_bytes()
                page.goto(f"{origin}/?no-splash=1&doc=_exports/fictional-review.pdf")
                embedded = page.frame_locator("#main")
                assert embedded.get_by_role("img", name="PDF page 1", exact=True).is_visible()
                assert embedded.get_by_role("combobox", name="Reading mode").input_value() == "single"
                library = page.locator("#hubLibrary")
                assert library.bounding_box()["height"] <= 128
                page.set_viewport_size({"width": 320, "height": 568})
                frame = page.locator("#main")
                height = frame.bounding_box()["height"]
                frame_url = frame.get_attribute("src")
                toggle = page.get_by_role("button", name="Expand preview")
                toggle.press("Enter")
                restore = page.get_by_role("button", name="Restore Library")
                assert restore.evaluate("(el) => el === document.activeElement")
                assert restore.get_attribute("aria-expanded") == "false"
                assert not library.is_visible() and not page.locator(".hub-bar").is_visible()
                assert frame.bounding_box()["height"] > height + 150
                assert frame.get_attribute("src") == frame_url
                assert embedded.get_by_role("combobox", name="Reading mode").input_value() == "single"
                for width in (576, 768, 1024):
                    page.set_viewport_size({"width": width, "height": 800})
                    assert page.locator(".hub-bar").is_visible()
                    assert not library.is_visible()
                    assert frame.bounding_box()["width"] == width
                restore.click()
                assert toggle.get_attribute("aria-expanded") == "true"
                assert library.is_visible()
                assert frame.bounding_box()["width"] < 1024
                browser.close()
        finally:
            server.shutdown()
            runner.join()
