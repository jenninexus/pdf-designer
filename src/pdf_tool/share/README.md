# `pdf_tool/share/` — wheel asset tree (generated)

**SSOT stays at the repo root:** `themes/`, `layouts/`, `examples/`.

Before building a wheel / sdist for non-checkout installs, run:

```bash
python scripts/sync-wheel-share.py
```

That copies the public asset trees into this folder so setuptools can ship them
inside the package. Generated subdirs are gitignored — do not edit them by hand.
