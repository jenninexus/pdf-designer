#!/usr/bin/env python3
"""Inline {{img:name}} placeholders in a work-samples template -> self-contained HTML.

Usage:
  python scripts/inline-work-sample-images.py <template.html> <out.html> name=path [name=path ...]
  python scripts/inline-work-sample-images.py <template.html> <out.html> --board name=path ...

``--board`` re-encodes photos as JPEG at print resolution so Chromium's PDF
stays under Indeed-class 5 MB caps. Same engine: ``python -m pdf_tool.inline_images``.
"""
from pdf_tool.inline_images import main

if __name__ == "__main__":
    raise SystemExit(main())
