"""Desktop packaging helpers keep Playwright and first-run data local."""

from pathlib import Path
from unittest.mock import Mock

import pytest
from playwright.sync_api import Error

from pdf_tool.browser import bundled_chromium_path, chromium_launch_kwargs, launch_chromium
from pdf_tool.preview import _write_ready_file


def test_frozen_runtime_uses_only_a_bundled_playwright_chromium(tmp_path: Path, monkeypatch):
    runtime = tmp_path / "runtime" / "pdf-designer-runtime.exe"
    browser = runtime.parent / "browsers" / "chromium-1234" / "chrome-win64" / "chrome.exe"
    browser.parent.mkdir(parents=True)
    browser.write_text("fixture", encoding="utf-8")

    assert bundled_chromium_path(runtime, frozen=False) is None
    assert bundled_chromium_path(runtime, frozen=True) == browser
    monkeypatch.setattr("pdf_tool.browser.sys.frozen", True, raising=False)
    monkeypatch.setattr("pdf_tool.browser.sys.executable", str(runtime))
    kwargs = chromium_launch_kwargs()
    assert set(kwargs) == {"executable_path"}
    assert Path(kwargs["executable_path"]).samefile(browser)


def test_preview_ready_file_contains_the_actual_loopback_url(tmp_path: Path):
    ready_file = tmp_path / "nested" / "hub-url.txt"
    _write_ready_file(ready_file, "http://127.0.0.1:43210/")
    assert ready_file.read_text(encoding="utf-8") == "http://127.0.0.1:43210/\n"


def test_store_runtime_falls_back_from_edge_to_chrome(tmp_path, monkeypatch):
    (tmp_path / "installed-browser.txt").touch()
    monkeypatch.setattr("pdf_tool.browser.sys.frozen", True, raising=False)
    monkeypatch.setattr("pdf_tool.browser.sys.executable", str(tmp_path / "runtime.exe"))
    browser_type = Mock()
    browser = object()
    browser_type.launch.side_effect = [Error("Edge unavailable"), browser]
    assert launch_chromium(browser_type) is browser
    assert [call.kwargs["channel"] for call in browser_type.launch.call_args_list] == ["msedge", "chrome"]
    browser_type.launch.side_effect = Error("browser unavailable")
    with pytest.raises(RuntimeError, match="requires Microsoft Edge or Google Chrome"):
        launch_chromium(browser_type)
