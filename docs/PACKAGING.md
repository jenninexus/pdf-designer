# Packaging — PyPI / installer spike

How a **non-checkout** user gets `pdf-designer`. Companion to
[`PRODUCT.md`](PRODUCT.md) (business) and [`WHITE-LABEL.md`](WHITE-LABEL.md)
(public how-to from a clone).

> **Spike status (2026-07-21):** path resolution + wheel asset gate landed.
> Public TestPyPI upload is still a deliberate later step (account + version
> policy). Until then, the supported install remains a **git checkout** +
> `pip install -e ".[dev]"`.

---

## The blocker we measured

`python -m build --wheel` on the pre-spike tree produced a wheel with **only**
`pdf_tool/*.py` + `static/hub.css`. It did **not** include `themes/` or
`layouts/`.

Those trees are required by:

| Caller | Needs |
|---|---|
| `pdf_tool.variants` | `themes/default-resume.json` + `themes/presets/*` |
| `pdf_tool.collage` | `themes/default-collage.json` + `layouts/collage/*` |
| `pdf_tool.preview` | public palettes under `themes/` (+ optional `storage/brand-design/`) |

Hard-coding `Path(__file__).parents[2]` assumes an editable `src/` layout. A
site-packages install breaks that assumption.

## Decision (v1)

| Layer | Choice |
|---|---|
| **SSOT** | Repo-root `themes/` + `layouts/` + `examples/` stay the edit surface |
| **Wheel payload** | Copy public trees into `src/pdf_tool/share/` at build time |
| **Runtime resolve** | `pdf_tool.paths.repo_root()` — bundled `share/` first, else walk to checkout |
| **Private data** | Never package `storage/` |
| **Chromium** | Still a post-install step: `playwright install chromium` |
| **Desktop installer** | Later paid shell — see PRODUCT.md § shell-over-Hub; not required for PyPI |

```bash
# Gate before any upload
python scripts/sync-wheel-share.py
python scripts/check-wheel-assets.py   # sync + build + assert share/ in the wheel
```

## Supported install paths (today → next)

| Path | Who | Status |
|---|---|---|
| `git clone` + `pip install -e ".[dev]"` + `playwright install chromium` | Devs / agents | ✅ supported (white-label smoke) |
| Local wheel with synced `share/` | Spike / CI | ✅ `check-wheel-assets.py` |
| TestPyPI / PyPI `pip install pdf-designer` | Non-dev trial | ❌ not published yet |
| GUI installer (paid app) | Creatives | ❌ design only — PRODUCT.md |

## Publish checklist (when ready)

1. Bump `project.version` in `pyproject.toml`
2. `python scripts/check-wheel-assets.py` → PASS
3. `python scripts/smoke-white-label.py` from a clean clone (still the product gate)
4. Upload to **TestPyPI** first; install into a fresh venv; run:
   `pdf-designer-check-generation` on the bundled example path (or re-clone smoke)
5. Only then production PyPI
6. README badge / install blurb — only after a real `pip install pdf-designer` works

## Non-goals for packaging

- Shipping vaults, brand maps, or application history
- Auto-downloading Chromium without an explicit `playwright install`
- A second renderer inside the wheel
- Replacing the Design Hub with an Electron fork just to get onto PyPI

## Related

- Product / paid shell: [`PRODUCT.md`](PRODUCT.md)
- Public clone demo: [`WHITE-LABEL.md`](WHITE-LABEL.md)
- License honesty: [`LICENSING-NOTES.md`](LICENSING-NOTES.md)
