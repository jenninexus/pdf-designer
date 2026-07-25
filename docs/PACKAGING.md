# Packaging — PyPI / installer spike

How a **non-checkout** user gets `pdf-designer`. Companion to
[`PRODUCT.md`](PRODUCT.md) (business) and [`WHITE-LABEL.md`](WHITE-LABEL.md)
(public how-to from a clone).

> **Status (2026-07-25):** path resolution + wheel asset gate + **local fresh-venv
> install proof** landed (`scripts/testpypi-dry-run.py`). TestPyPI **upload** is
> still blocked — no TestPyPI account/API token in the credential DB yet. Until
> upload works, the supported public install remains a **git checkout** +
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
| **Runtime resolve** | `pdf_tool.paths.repo_root()` — **checkout wins** over `share/` (so live edits aren't shadowed); wheel-only installs fall through to `pdf_tool/share/` |
| **Private data** | Never package `storage/` |
| **Chromium** | Still a post-install step: `playwright install chromium` |
| **Desktop installer** | Later paid shell — see PRODUCT.md § shell-over-Hub; not required for PyPI |

```bash
# Gate before any upload
python scripts/sync-wheel-share.py
python scripts/check-wheel-assets.py   # sync + build + assert share/ in the wheel

# Full dry-run: build + fresh venv + prove bundled share/ + check_generation
python scripts/testpypi-dry-run.py              # local wheel proof (no upload)
python scripts/testpypi-dry-run.py --upload     # needs TESTPYPI_TOKEN
```

⚠ **Prove from outside the checkout.** Because checkout wins over `share/`, a
fresh-venv proof must run with cwd *outside* the repo (the dry-run script does
this). Verifying from the checkout directory will silently use live `themes/`.

## Supported install paths (today → next)

| Path | Who | Status |
|---|---|---|
| `git clone` + `pip install -e ".[dev]"` + `playwright install chromium` | Devs / agents | ✅ supported (white-label smoke) |
| Local wheel with synced `share/` | Spike / CI | ✅ `check-wheel-assets.py` + `testpypi-dry-run.py` |
| TestPyPI `pip install pdf-designer` | Non-dev trial | 🟡 local proof green; **upload blocked** (no token yet) |
| Production PyPI | Public | ❌ not until TestPyPI upload + install works |
| GUI installer (paid app) | Creatives | ❌ design only — PRODUCT.md |

## Publish checklist (when ready)

1. Bump `project.version` in `pyproject.toml` if that version was already uploaded
2. `python scripts/check-wheel-assets.py` → PASS
3. `python scripts/smoke-white-label.py` from a clean clone (still the product gate)
4. **Create TestPyPI account + API token** at https://test.pypi.org/manage/account/token/
   — store in sys-admin `userdata.db` (`category=API Keys`, `service=TestPyPI`,
   `key=api_token`) or export `TESTPYPI_TOKEN` for the shell
5. `python scripts/testpypi-dry-run.py --upload` → upload + fresh-venv install from TestPyPI
6. Only then production PyPI
7. README badge / install blurb — only after a real `pip install pdf-designer` works

## Non-goals for packaging

- Shipping vaults, brand maps, or application history
- Auto-downloading Chromium without an explicit `playwright install`
- A second renderer inside the wheel
- Replacing the Design Hub with an Electron fork just to get onto PyPI

## Related

- Product / paid shell: [`PRODUCT.md`](PRODUCT.md)
- Public clone demo: [`WHITE-LABEL.md`](WHITE-LABEL.md)
- License honesty: [`LICENSING-NOTES.md`](LICENSING-NOTES.md)
