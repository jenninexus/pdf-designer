"""Design Hub launch title screen is on every hub chrome page."""

from pathlib import Path

from pdf_tool.preview import APP_HTML

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
    assert "HOLD_MS" not in js
    assert "hubSplashOpen" in js
    assert "const FADE_MS = reduced ? 0 : 2000" in js
    assert "hub-splash-load 3s" in css
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


def test_splash_stays_until_open():
    js = (ROOT / "splash.js").read_text(encoding="utf-8")
    assert "setTimeout(dismiss" not in js
    assert "splash.addEventListener(\"click\"" not in js
    assert 'dismiss("/")' in js
    assert 'dismiss("/wizard")' in js
