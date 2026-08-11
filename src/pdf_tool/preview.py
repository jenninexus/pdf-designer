"""Design Hub — local previewer for every renderable document in the repo.

Jobright-style library + PowerPoint-style picker: filterable sidebar of live
thumbnails (resumes, cover letters, collages, examples), large preview pane,
palette swapper, one-click export.

Chrome tokens live in ``static/hub.css`` (vendored from www-theme-kit dashboard
tokens + syna glass). Document brand palettes still come from ``themes/`` +
``storage/brand-design/``.

Zero new dependencies: stdlib http.server; exports reuse html_to_pdf / pdf_to_png.
Binds to 127.0.0.1 only. No MCP / always-on server required.

Usage:
    python -m pdf_tool.preview                     # scan the repo, serve on :8787
    python -m pdf_tool.preview path/to/dir         # scan any directory instead
    python -m pdf_tool.preview --port 9000 --no-open
"""

from __future__ import annotations

import json
import re
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

from .html_to_pdf import export_html_to_pdf
from .paths import repo_root
from .pdf_to_png import render_to_png
from .recipe_gallery import build_recipe_gallery
from .vault_overview import build_vault_overview

_REPO_ROOT = repo_root()
_STATIC_DIR = Path(__file__).resolve().parent / "static"
EXCLUDE_PARTS = {
    "_exports",
    "node_modules",
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "build",
    "dist",
    ".eggs",
    "egg-info",
}

KINDS = ("resume", "cover-letter", "collage", "gallery", "example", "other")

# theme-JSON block -> pdf-designer CSS custom properties
_TOKEN_MAP = [
    ("--bg", "backgrounds", "body"),
    ("--surface", "backgrounds", "surface"),
    ("--elevated", "backgrounds", "elevated"),
    ("--elevated-2", "backgrounds", "elevated_2"),
    ("--text", "text", "primary"),
    ("--dim", "text", "secondary"),
    ("--dim2", "text", "muted"),
    ("--border", "borders", "subtle"),
    ("--border2", "borders", "strong"),
    ("--primary", "accents", "primary"),
    ("--secondary", "accents", "secondary"),
    ("--accent", "accents", "accent"),
    ("--support", "accents", "support"),
]


def classify_document(rel: str, stem: str) -> dict:
    """Tag each HTML for filters — kind / bucket / person / group folder."""
    path = rel.replace("\\", "/")
    path_l = path.lower()
    name_l = stem.lower()
    parts = path_l.split("/")

    if name_l == "index" and ("_candidates" in parts or "collage" in path_l):
        kind = "gallery"
    elif "_candidates" in parts or "/collages/" in path_l or "collage" in name_l:
        kind = "collage"
    elif "personal-letter" in name_l or name_l.endswith("-letter") and "cover" not in name_l:
        kind = "letter"
    elif "cover" in name_l:
        kind = "cover-letter"
    elif "resume" in name_l:
        kind = "resume"
    elif path_l.startswith("examples/"):
        kind = "example"
    else:
        kind = "other"

    if path_l.startswith("storage/_job-listings/"):
        bucket = "_job-listings"
    elif path_l.startswith("examples/"):
        bucket = "examples"
    elif "collage" in path_l or "_candidates" in parts:
        bucket = "collages"
    elif any(path_l.startswith(f"storage/{u}/") for u in ("jenni", "shade", "studio")):
        bucket = "vault-renders"
    else:
        bucket = "other"

    # Profile filter (Hub "Profiles" select) — person applicants + studio/martian entity decks.
    # Prefer path ownership, then filename prefix. `person` kept as alias of `profile` for
    # older deep-links / badges.
    profile = None
    if path_l.startswith("storage/jenni/") or name_l.startswith("jenni"):
        profile = "jenni"
    elif path_l.startswith("storage/shade/") or name_l.startswith("shade"):
        profile = "shade"
    elif (
        path_l.startswith("storage/studio/")
        or name_l.startswith("studio")
        or "/studio-" in path_l
    ):
        profile = "studio"
    elif name_l.startswith("martian") or "/martian-" in path_l or "martian-games" in name_l:
        profile = "martian"

    if "work-example" in name_l or "work-sample" in name_l or "work_examples" in name_l:
        kind = "work-samples"

    group = str(Path(path).parent).replace("\\", "/")
    if group == ".":
        group = "(root)"

    # Short template label for the stage bar
    label = stem.replace("-", " ")

    return {
        "path": path,
        "name": stem,
        "label": label,
        "group": group,
        "kind": kind,
        "bucket": bucket,
        "profile": profile,
        "person": profile,  # alias — Hub filter + badges
        "template": True,  # each HTML file is its own selectable template
    }


def _is_excluded_rel(rel_parts: tuple[str, ...]) -> bool:
    if EXCLUDE_PARTS.intersection(rel_parts):
        return True
    # setuptools egg-info dirs are named <pkg>.egg-info
    if any(part.endswith(".egg-info") for part in rel_parts):
        return True
    return False


def scan_documents(root: Path) -> list[dict]:
    docs = []
    for p in sorted(root.rglob("*.html")):
        rel = p.relative_to(root)
        if _is_excluded_rel(rel.parts):
            continue
        # Skip the hub's own static HTML if ever added under src/
        if "pdf_tool" in rel.parts and "static" in rel.parts:
            continue
        docs.append(classify_document(str(rel).replace("\\", "/"), p.stem))
    return docs


# File suffixes the auto-refresh watcher tracks. HTML sources change the doc
# list; PDFs/PNGs land in _exports/ when a resume is exported and are what the
# "refresh when I output a new resume" feature keys on.
_WATCH_SUFFIXES = {".html", ".pdf", ".png", ".jpg", ".jpeg", ".webp"}
# _exports is excluded from the DOC scan but MUST be watched for new outputs.
_WATCH_EXCLUDE = EXCLUDE_PARTS - {"_exports"}


def tree_signature(root: Path) -> str:
    """Cheap change token over the doc tree + _exports outputs.

    Returns a string that changes whenever a watched file is added, removed, or
    modified — the client polls /api/version and refreshes when it changes.
    Deliberately coarse (count + newest mtime + total size) so it is fast on a
    large tree and never touches file contents.
    """
    count = 0
    newest = 0.0
    total = 0
    for p in root.rglob("*"):
        if p.suffix.lower() not in _WATCH_SUFFIXES:
            continue
        try:
            rel_parts = p.relative_to(root).parts
        except ValueError:
            continue
        # Watch _exports even though scan_documents excludes them.
        if _WATCH_EXCLUDE.intersection(rel_parts):
            continue
        if any(part.endswith(".egg-info") for part in rel_parts):
            continue
        if part_is_buildish(rel_parts):
            continue
        if "pdf_tool" in rel_parts and "static" in rel_parts:
            continue
        try:
            st = p.stat()
        except OSError:
            continue
        count += 1
        total += st.st_size
        if st.st_mtime > newest:
            newest = st.st_mtime
    return f"{count}:{newest:.3f}:{total}"


def part_is_buildish(rel_parts: tuple[str, ...]) -> bool:
    """Skip build/dist artifacts in the watcher (same as library scan)."""
    blocked = {"build", "dist", ".eggs"}
    return bool(blocked.intersection(rel_parts))


def _vars_from_nested_mode(block: dict) -> dict:
    vars_ = {}
    for var, section, key in _TOKEN_MAP:
        value = block.get(section, {}).get(key) if isinstance(block.get(section), dict) else None
        if value:
            vars_[var] = value
    return vars_


def _vars_from_token_map(block: dict) -> dict:
    vars_ = {}
    for key, value in block.items():
        if not (isinstance(key, str) and key.startswith("--") and isinstance(value, str)):
            continue
        if "gradient" in value.lower():
            continue
        vars_[key] = value
    return vars_


def load_palettes() -> list[dict]:
    """themes/*.json + themes/presets/*.json (public) + storage/brand-design/*.json (private)."""
    palettes = []
    for theme_dir in (
        _REPO_ROOT / "themes",
        _REPO_ROOT / "themes" / "presets",
        _REPO_ROOT / "storage" / "brand-design",
    ):
        if not theme_dir.is_dir():
            continue
        for f in sorted(theme_dir.glob("*.json")):
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
            except Exception:
                continue
            tokens_root = data.get("tokens") if isinstance(data.get("tokens"), dict) else None
            for mode in ("dark", "light"):
                vars_ = {}
                if tokens_root and isinstance(tokens_root.get(mode), dict):
                    vars_ = _vars_from_token_map(tokens_root[mode])
                else:
                    block = data.get(mode)
                    if isinstance(block, dict):
                        vars_ = _vars_from_nested_mode(block)
                if vars_:
                    label = data.get("_meta", {}).get("name") if isinstance(data.get("_meta"), dict) else None
                    name = f"{label} · {mode}" if label else f"{f.stem} · {mode}"
                    palettes.append({"name": name, "vars": vars_, "id": f.stem, "mode": mode})
    return palettes


APP_HTML = """<!doctype html>
<html lang="en" data-theme="dark" data-bs-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>pdf-designer — Design Hub</title>
<link rel="stylesheet" href="/_hub/hub.css">
</head>
<body class="hub-shell">
<header class="hub-bar" aria-label="Design Hub toolbar">
  <div class="hub-bar-scroll" id="hubBarScroll" tabindex="0" title="Scroll horizontally — mouse wheel works here">
    <div class="hub-group hub-brand-group">
      <h1 class="hub-brand" title="__ROOT__">Design Hub</h1>
    </div>
    <div class="hub-group" title="Profiles — applicants + studio entity decks">
      <select id="personFilter" title="Profiles" aria-label="Profiles">
        <option value="">all profiles</option>
        <option value="jenni">jenni</option>
        <option value="shade">shade</option>
        <option value="studio">studio</option>
        <option value="martian">martian</option>
      </select>
    </div>
    <div class="hub-group">
      <div class="chips" id="kindChips" role="tablist" aria-label="Document kind"></div>
    </div>
    <nav class="hub-group hub-nav" id="hubNav" aria-label="Hub sections">
      <a class="hub-link on" href="/" title="Document library" aria-current="page">Library</a>
      <a class="hub-link" href="/recipes" title="Browse layouts/ + themes/presets">Recipes</a>
      <a class="hub-link" href="/vault" title="Readable vault · skills · go-to résumés">Vault</a>
    </nav>
    <div class="hub-group hub-filters">
      <input id="search" type="search" placeholder="Search…" autocomplete="off" title="Search name or path" aria-label="Search">
      <select id="folderFilter" title="Folder — pin go-tos with ★" aria-label="Folder"><option value="">all folders</option></select>
      <button type="button" id="pinFolderBtn" class="hub-pin-btn" title="Pin / unpin this folder (kept after Refresh)" aria-label="Pin folder" disabled>★</button>
      <select id="palette" title="Palette" aria-label="Palette"><option value="">doc default</option></select>
      <select id="fmt" title="Export format" aria-label="Export format">
        <option value="pdf-light">PDF light</option>
        <option value="pdf-dark">PDF dark</option>
        <option value="png-light">PNG light</option>
        <option value="png-dark">PNG dark</option>
      </select>
    </div>
  </div>
  <div class="hub-bar-pin" aria-label="Pinned actions">
    <details class="hub-more" id="hubMore">
      <summary title="More export options" aria-label="More export options">
        <svg class="hub-icon" viewBox="0 0 448 512" aria-hidden="true" focusable="false"><path fill="currentColor" d="M8 256a56 56 0 1 1 112 0A56 56 0 1 1 8 256zm160 0a56 56 0 1 1 112 0 56 56 0 1 1 -112 0zm216-56a56 56 0 1 1 0 112 56 56 0 1 1 0-112z"/></svg>
      </summary>
      <div class="hub-more-panel">
        <label>Output folder
          <input id="outdir" type="text" placeholder="_exports next to doc">
        </label>
      </div>
    </details>
    <button type="button" class="hub-search-trigger" id="searchTrigger" title="Search (Ctrl/Cmd+K)" aria-label="Search">
      <svg class="hub-icon" viewBox="0 0 512 512" aria-hidden="true" focusable="false"><path fill="currentColor" d="M416 208c0 45.9-14.9 88.3-40 122.7L502.6 457.4c12.5 12.5 12.5 32.8 0 45.3s-32.8 12.5-45.3 0L330.7 376c-34.4 25.2-76.8 40-122.7 40C93.1 416 0 322.9 0 208S93.1 0 208 0S416 93.1 416 208zM208 352a144 144 0 1 0 0-288 144 144 0 1 0 0 288z"/></svg>
    </button>
    <button id="refreshBtn" type="button" class="hub-icon-btn" title="Re-scan the repo for new/changed documents" aria-label="Refresh">
      <svg class="hub-icon" viewBox="0 0 512 512" aria-hidden="true" focusable="false"><path fill="currentColor" d="M105.1 202.6c7.7-21.8 20.2-42.3 37.8-59.8c62.5-62.5 163.8-62.5 226.3 0L386.3 160 352 160c-17.7 0-32 14.3-32 32s14.3 32 32 32l111.5 0c0 0 0 0 0 0l.4 0c17.7 0 32-14.3 32-32l0-112c0-17.7-14.3-32-32-32s-32 14.3-32 32l0 35.2L414.4 97.6c-87.5-87.5-229.3-87.5-316.8 0C73.2 122 55.6 150.7 44.8 181.4c-5.9 16.7 2.9 34.9 19.5 40.8s34.9-2.9 40.8-19.5zM39 289.3c-5 1.5-9.8 4.2-13.7 8.2c-4 4-6.7 8.8-8.1 14c-.3 1.2-.6 2.5-.8 3.8c-.3 1.7-.4 3.4-.4 5.1L16 432c0 17.7 14.3 32 32 32s32-14.3 32-32l0-35.1 17.6 17.5c0 0 0 0 0 0c87.5 87.4 229.3 87.4 316.7 0c24.4-24.4 42.1-53.1 52.9-83.8c5.9-16.7-2.9-34.9-19.5-40.8s-34.9 2.9-40.8 19.5c-7.7 21.8-20.2 42.3-37.8 59.8c-62.5 62.5-163.8 62.5-226.3 0l-.1-.1L125.6 352l34.4 0c17.7 0 32-14.3 32-32s-14.3-32-32-32L48.4 288c-1.6 0-3.2 .1-4.8 .3s-3.1 .5-4.6 1z"/></svg>
    </button>
    <button class="primary hub-icon-btn" id="exportBtn" type="button" title="Export selected document" aria-label="Export">
      <svg class="hub-icon" viewBox="0 0 512 512" aria-hidden="true" focusable="false"><path fill="currentColor" d="M288 32c0-17.7-14.3-32-32-32s-32 14.3-32 32l0 242.7-73.4-73.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3l128 128c12.5 12.5 32.8 12.5 45.3 0l128-128c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L288 274.7 288 32zM64 352c-35.3 0-64 28.7-64 64l0 32c0 35.3 28.7 64 64 64l384 0c35.3 0 64-28.7 64-64l0-32c0-35.3-28.7-64-64-64l-101.5 0-45.3 45.3c-25 25-65.5 25-90.5 0L165.5 352 64 352zm368 56a24 24 0 1 1 0 48 24 24 0 1 1 0-48z"/></svg>
    </button>
    <button type="button" class="hub-drawer-toggle" id="drawerToggle" title="Menu" aria-label="Open menu" aria-expanded="false" aria-controls="hubDrawer">
      <span class="bars" aria-hidden="true"><span></span></span>
    </button>
    <span id="status"></span>
  </div>
</header>

<div class="hub-drawer-backdrop" id="hubDrawerBackdrop" hidden></div>
<aside class="hub-drawer" id="hubDrawer" aria-hidden="true" aria-label="Design Hub menu">
  <div class="hub-drawer-head">
    <span class="hub-brand">Design Hub</span>
    <button type="button" class="hub-drawer-close" id="drawerClose" aria-label="Close menu">&times;</button>
  </div>
  <div class="hub-drawer-body">
    <div class="hub-drawer-section">
      <span class="hub-drawer-label">Navigate</span>
      <nav class="hub-nav" id="drawerNav" aria-label="Hub sections (menu)">
        <a class="hub-link on" href="/">Library</a>
        <a class="hub-link" href="/recipes">Recipes</a>
        <a class="hub-link" href="/vault">Vault</a>
      </nav>
    </div>
    <div class="hub-drawer-section">
      <span class="hub-drawer-label">Kind</span>
      <div class="chips" id="drawerKindChips" role="tablist" aria-label="Document kind (menu)"></div>
    </div>
    <div class="hub-drawer-section">
      <div class="hub-drawer-field">
        <label for="drawerPersonFilter">Profiles</label>
        <select id="drawerPersonFilter" aria-label="Profiles">
          <option value="">all profiles</option>
          <option value="jenni">jenni</option>
          <option value="shade">shade</option>
          <option value="studio">studio</option>
          <option value="martian">martian</option>
        </select>
      </div>
      <div class="hub-drawer-field">
        <label for="drawerFolderFilter">Folder</label>
        <select id="drawerFolderFilter" aria-label="Folder"><option value="">all folders</option></select>
      </div>
      <div class="hub-drawer-field">
        <label for="drawerPalette">Palette</label>
        <select id="drawerPalette" aria-label="Palette"><option value="">doc default</option></select>
      </div>
      <div class="hub-drawer-field">
        <label for="drawerFmt">Export format</label>
        <select id="drawerFmt" aria-label="Export format">
          <option value="pdf-light">PDF light</option>
          <option value="pdf-dark">PDF dark</option>
          <option value="png-light">PNG light</option>
          <option value="png-dark">PNG dark</option>
        </select>
      </div>
      <div class="hub-drawer-field">
        <label for="outdirDrawer">Output folder</label>
        <input id="outdirDrawer" type="text" placeholder="_exports next to doc">
      </div>
    </div>
  </div>
  <div class="hub-drawer-actions">
    <button type="button" id="drawerRefresh" class="hub-icon-btn" title="Refresh" aria-label="Refresh">
      <svg class="hub-icon" viewBox="0 0 512 512" aria-hidden="true" focusable="false"><path fill="currentColor" d="M105.1 202.6c7.7-21.8 20.2-42.3 37.8-59.8c62.5-62.5 163.8-62.5 226.3 0L386.3 160 352 160c-17.7 0-32 14.3-32 32s14.3 32 32 32l111.5 0c0 0 0 0 0 0l.4 0c17.7 0 32-14.3 32-32l0-112c0-17.7-14.3-32-32-32s-32 14.3-32 32l0 35.2L414.4 97.6c-87.5-87.5-229.3-87.5-316.8 0C73.2 122 55.6 150.7 44.8 181.4c-5.9 16.7 2.9 34.9 19.5 40.8s34.9-2.9 40.8-19.5zM39 289.3c-5 1.5-9.8 4.2-13.7 8.2c-4 4-6.7 8.8-8.1 14c-.3 1.2-.6 2.5-.8 3.8c-.3 1.7-.4 3.4-.4 5.1L16 432c0 17.7 14.3 32 32 32s32-14.3 32-32l0-35.1 17.6 17.5c0 0 0 0 0 0c87.5 87.4 229.3 87.4 316.7 0c24.4-24.4 42.1-53.1 52.9-83.8c5.9-16.7-2.9-34.9-19.5-40.8s-34.9 2.9-40.8 19.5c-7.7 21.8-20.2 42.3-37.8 59.8c-62.5 62.5-163.8 62.5-226.3 0l-.1-.1L125.6 352l34.4 0c17.7 0 32-14.3 32-32s-14.3-32-32-32L48.4 288c-1.6 0-3.2 .1-4.8 .3s-3.1 .5-4.6 1z"/></svg>
    </button>
  </div>
  <div class="hub-drawer-foot"><kbd>Esc</kbd> closes</div>
</aside>

<div class="hub-search-ovl" id="hubSearchOvl" hidden>
  <div class="hub-search-ovl-inner">
    <input class="hub-search-ovl-input" id="searchOvlInput" type="search" placeholder="Search name or path…" autocomplete="off" aria-label="Search documents">
    <div class="hub-search-ovl-results" id="searchOvlResults"></div>
    <div class="hub-search-ovl-foot"><kbd>Esc</kbd> closes · <kbd>Enter</kbd> opens first</div>
  </div>
</div>

<main class="hub-main">
  <aside class="library">
    <div class="library-head">Library <span id="visibleCount">0</span></div>
    <div class="library-scroll" id="sidebar"></div>
  </aside>
  <div class="stage">
    <div class="stagebar" id="stagebar">
      <span>Select a template in the library →</span>
    </div>
    <iframe id="main" title="Document preview" src="about:blank"></iframe>
  </div>
</main>

<script>
let DOCS = __DOCS__;
const PALETTES = __PALETTES__;
const KIND_ORDER = ["all","resume","cover-letter","letter","work-samples","collage","gallery","example","other"];
const KIND_LABEL = {
  all: "All",
  resume: "Resumes",
  "cover-letter": "Cover Letters",
  letter: "Letters",
  "work-samples": "Work Samples",
  collage: "Collages",
  gallery: "Galleries",
  example: "Examples",
  other: "Other",
};

let selected = null;
let kindFilter = "all";

/* ---- Hub prefs (localStorage — survives Refresh + full page reload) ---- */
const HUB_PIN_KEY = "pdf-designer.hub.pinnedFolders";
const HUB_FOLDER_KEY = "pdf-designer.hub.folderFilter";
const HUB_PROFILE_KEY = "pdf-designer.hub.profileFilter";

function loadPinnedFolders() {
  try {
    const raw = JSON.parse(localStorage.getItem(HUB_PIN_KEY) || "[]");
    return Array.isArray(raw) ? raw.map(String).filter(Boolean) : [];
  } catch (_) { return []; }
}
function savePinnedFolders(pins) {
  try { localStorage.setItem(HUB_PIN_KEY, JSON.stringify([...new Set(pins)])); } catch (_) {}
}
function isPinned(folder) {
  return !!folder && loadPinnedFolders().includes(folder);
}
function togglePinFolder(folder) {
  if (!folder) return;
  const pins = loadPinnedFolders();
  const i = pins.indexOf(folder);
  if (i >= 0) pins.splice(i, 1);
  else pins.push(folder);
  savePinnedFolders(pins);
  buildFolderSelect();
  syncPinButton();
}

/* Horizontal wheel-scroll on the header strip (and its scrollbar). */
(function hubBarWheelScroll() {
  const sc = document.getElementById("hubBarScroll");
  const bar = document.querySelector(".hub-bar");
  if (!sc) return;
  const onWheel = (e) => {
    if (Math.abs(e.deltaY) < Math.abs(e.deltaX)) return;
    if (sc.scrollWidth <= sc.clientWidth) return;
    e.preventDefault();
    sc.scrollLeft += e.deltaY;
  };
  sc.addEventListener("wheel", onWheel, { passive: false });
  if (bar) bar.addEventListener("wheel", (e) => {
    if (e.target.closest(".hub-bar-pin")) return;
    onWheel(e);
  }, { passive: false });
})();

const paletteSel = document.getElementById("palette");
const drawerPaletteSel = document.getElementById("drawerPalette");
PALETTES.forEach((p, i) => {
  const o = document.createElement("option");
  o.value = i;
  o.textContent = p.name;
  paletteSel.appendChild(o);
  if (drawerPaletteSel) drawerPaletteSel.appendChild(o.cloneNode(true));
});

function applyPalette(iframe) {
  const idx = paletteSel.value;
  const doc = iframe.contentDocument;
  if (!doc) return;
  const st = doc.documentElement.style;
  for (const p of PALETTES) for (const k of Object.keys(p.vars)) st.removeProperty(k);
  if (idx !== "") for (const [k, v] of Object.entries(PALETTES[idx].vars)) st.setProperty(k, v);
}

function counts() {
  const c = { all: DOCS.length };
  for (const d of DOCS) c[d.kind] = (c[d.kind] || 0) + 1;
  return c;
}

function buildStats() { /* counts live on kind chips — no separate stats row */ }

function fillKindChipHost(wrap) {
  if (!wrap) return;
  const c = counts();
  wrap.innerHTML = "";
  for (const k of KIND_ORDER) {
    if (k !== "all" && !c[k]) continue;
    const b = document.createElement("button");
    b.type = "button";
    b.className = "chip" + (kindFilter === k ? " on" : "");
    b.dataset.kind = k;
    b.setAttribute("role", "tab");
    b.setAttribute("aria-selected", kindFilter === k ? "true" : "false");
    b.innerHTML = `${KIND_LABEL[k]}<span class="n">${c[k] || 0}</span>`;
    b.addEventListener("click", () => {
      kindFilter = k;
      buildKindChips();
      renderLibrary();
      closeDrawer();
    });
    wrap.appendChild(b);
  }
}
function buildKindChips() {
  fillKindChipHost(document.getElementById("kindChips"));
  fillKindChipHost(document.getElementById("drawerKindChips"));
}

function uniqueFolders() {
  return [...new Set(DOCS.map(d => d.group))].sort();
}

function populateFolderSelect(sel, cur, all, pins, pinSet) {
  if (!sel) return;
  sel.innerHTML = "";
  const allOpt = document.createElement("option");
  allOpt.value = "";
  allOpt.textContent = "all folders";
  sel.appendChild(allOpt);

  const pinnedAlive = pins.filter(p => all.includes(p));
  if (pinnedAlive.length) {
    const og = document.createElement("optgroup");
    og.label = "Pinned";
    for (const g of pinnedAlive.sort()) {
      const o = document.createElement("option");
      o.value = g;
      o.textContent = "★ " + g;
      og.appendChild(o);
    }
    sel.appendChild(og);
  }

  const ogAll = document.createElement("optgroup");
  ogAll.label = "All folders";
  for (const g of all) {
    const o = document.createElement("option");
    o.value = g;
    o.textContent = (pinSet.has(g) ? "★ " : "") + g;
    ogAll.appendChild(o);
  }
  sel.appendChild(ogAll);

  if ([...sel.options].some(o => o.value === cur)) sel.value = cur;
  else sel.value = "";
}
function buildFolderSelect() {
  const sel = document.getElementById("folderFilter");
  const drawerSel = document.getElementById("drawerFolderFilter");
  const cur = sel.value || (localStorage.getItem(HUB_FOLDER_KEY) || "");
  const all = uniqueFolders();
  const pins = loadPinnedFolders().filter(p => all.includes(p) || p);
  const pinSet = new Set(pins);
  populateFolderSelect(sel, cur, all, pins, pinSet);
  populateFolderSelect(drawerSel, cur, all, pins, pinSet);
  syncPinButton();
}

function syncPinButton() {
  const btn = document.getElementById("pinFolderBtn");
  const folder = document.getElementById("folderFilter").value;
  if (!btn) return;
  btn.disabled = !folder;
  const on = isPinned(folder);
  btn.classList.toggle("on", on);
  btn.title = !folder
    ? "Select a folder to pin it"
    : (on ? "Unpin folder (kept in Pinned until you unpin)" : "Pin this folder — survives Refresh");
  btn.setAttribute("aria-pressed", on ? "true" : "false");
}

function filteredDocs() {
  const q = document.getElementById("search").value.trim().toLowerCase();
  const folder = document.getElementById("folderFilter").value;
  const profile = document.getElementById("personFilter").value;
  return DOCS.filter(d => {
    if (kindFilter !== "all" && d.kind !== kindFilter) return false;
    if (folder && d.group !== folder) return false;
    const dProfile = d.profile || d.person || null;
    if (profile && dProfile !== profile) return false;
    if (q) {
      const hay = `${d.path} ${d.name} ${d.label} ${d.group} ${d.kind} ${dProfile || ""}`.toLowerCase();
      if (!hay.includes(q)) return false;
    }
    return true;
  });
}

const THUMB_W = 248;
const sidebar = document.getElementById("sidebar");

function renderLibrary() {
  const docs = filteredDocs();
  document.getElementById("visibleCount").textContent = String(docs.length);
  sidebar.innerHTML = "";
  if (selected && !docs.some(d => d.path === selected.path)) {
    // Selection hidden by filters — keep preview, drop false sidebar highlight
  }
  if (!docs.length) {
    sidebar.innerHTML = '<div class="empty">No templates match these filters.</div>';
    return;
  }
  const groups = {};
  for (const d of docs) (groups[d.group] ||= []).push(d);
  for (const [group, list] of Object.entries(groups)) {
    const det = document.createElement("details");
    det.className = "group";
    det.open = true;
    const sum = document.createElement("summary");
    sum.innerHTML = `<span class="path" title="${group}">${group}</span><span class="count">${list.length}</span>`;
    det.appendChild(sum);
    for (const d of list) {
      const el = document.createElement("div");
      el.className = "thumb" + (selected && selected.path === d.path ? " sel" : "");
      el.dataset.path = d.path;
      const badges = [`<span class="badge kind-${d.kind}">${d.kind}</span>`];
      const prof = d.profile || d.person;
      if (prof) badges.push(`<span class="badge person-${prof}">${prof}</span>`);
      if (d.bucket === "examples") badges.push('<span class="badge">template</span>');
      el.innerHTML =
        `<div class="frame"><iframe loading="lazy" src="/${d.path}" scrolling="no" tabindex="-1" title=""></iframe></div>` +
        `<div class="meta"><div class="name" title="${d.path}">${d.name}</div><div class="badges">${badges.join("")}</div></div>`;
      const ifr = el.querySelector("iframe");
      ifr.addEventListener("load", () => {
        try {
          const w = ifr.contentDocument?.body?.scrollWidth || 850;
          const s = THUMB_W / Math.max(w, 320);
          ifr.style.width = Math.max(w, 320) + "px";
          ifr.style.height = (132 / s) + "px";
          ifr.style.transform = `scale(${s})`;
          applyPalette(ifr);
        } catch (_) { /* cross-origin unlikely on localhost */ }
      });
      el.addEventListener("click", () => select(d, el));
      det.appendChild(el);
    }
    sidebar.appendChild(det);
  }
}

const main = document.getElementById("main");
main.addEventListener("load", () => applyPalette(main));
paletteSel.addEventListener("change", () => {
  applyPalette(main);
  document.querySelectorAll(".thumb iframe").forEach(f => applyPalette(f));
});

function select(d, el, { pushUrl = true } = {}) {
  selected = d;
  document.querySelectorAll(".thumb").forEach(t => t.classList.remove("sel"));
  if (el) el.classList.add("sel");
  else {
    const match = document.querySelector(`.thumb[data-path="${CSS.escape(d.path)}"]`);
    if (match) match.classList.add("sel");
  }
  const bar = document.getElementById("stagebar");
  bar.innerHTML =
    `<span class="badge kind-${d.kind}">${d.kind}</span>` +
    (d.person ? `<span class="badge person-${d.person}">${d.person}</span>` : "") +
    `<span class="badge">${d.bucket}</span>` +
    `<span class="path" title="${d.path}">${d.path}</span>`;
  main.src = "/" + d.path;
  if (pushUrl) {
    try {
      const u = new URL(location.href);
      u.searchParams.set("doc", d.path);
      history.replaceState(null, "", u.pathname + u.search);
    } catch (_) {}
  }
}

/** Deep-link: /?doc=storage/jenni/defaults/….html — used by /vault pack links. */
function openFromQuery() {
  const raw = new URLSearchParams(location.search).get("doc");
  if (!raw) return false;
  const want = String(raw).replace(/^\/+/, "").split("\\\\").join("/");
  const d = DOCS.find(x => x.path === want || x.path.endsWith("/" + want));
  if (!d) {
    document.getElementById("status").textContent = "doc not in library: " + want;
    return false;
  }
  // Clear filters that would hide the target, then select.
  kindFilter = "all";
  document.getElementById("folderFilter").value = "";
  document.getElementById("personFilter").value = (d.profile || d.person || "");
  document.getElementById("search").value = "";
  buildKindChips();
  syncPinButton();
  renderLibrary();
  select(d, null, { pushUrl: true });
  // Scroll the library card into view once thumbs paint.
  requestAnimationFrame(() => {
    const el = document.querySelector(`.thumb[data-path="${CSS.escape(d.path)}"]`);
    if (el) el.scrollIntoView({ block: "nearest", behavior: "smooth" });
  });
  return true;
}

/** Deep-link: /?palette=slate-ink&mode=dark — used by /recipes "Try in Hub". */
function openPaletteFromQuery() {
  const params = new URLSearchParams(location.search);
  const id = params.get("palette");
  if (!id) return false;
  const mode = params.get("mode") || "dark";
  const idx = PALETTES.findIndex(p => p.id === id && p.mode === mode);
  if (idx < 0) {
    document.getElementById("status").textContent = "palette not found: " + id + " · " + mode;
    return false;
  }
  paletteSel.value = String(idx);
  applyPalette(main);
  document.querySelectorAll(".thumb iframe").forEach(f => applyPalette(f));
  document.getElementById("status").textContent = "palette: " + (PALETTES[idx].name || id);
  return true;
}

document.getElementById("folderFilter").addEventListener("change", () => {
  const v = document.getElementById("folderFilter").value;
  try { localStorage.setItem(HUB_FOLDER_KEY, v); } catch (_) {}
  const d = document.getElementById("drawerFolderFilter");
  if (d) d.value = v;
  syncPinButton();
  renderLibrary();
});
document.getElementById("personFilter").addEventListener("change", () => {
  const v = document.getElementById("personFilter").value;
  try { localStorage.setItem(HUB_PROFILE_KEY, v); } catch (_) {}
  const d = document.getElementById("drawerPersonFilter");
  if (d) d.value = v;
  renderLibrary();
});
document.getElementById("search").addEventListener("input", renderLibrary);
const pinBtn = document.getElementById("pinFolderBtn");
if (pinBtn) pinBtn.addEventListener("click", () => {
  togglePinFolder(document.getElementById("folderFilter").value);
});

function readOutdir() {
  const a = document.getElementById("outdir");
  const b = document.getElementById("outdirDrawer");
  return (a && a.value) || (b && b.value) || null;
}
function syncOutdir(fromId) {
  const a = document.getElementById("outdir");
  const b = document.getElementById("outdirDrawer");
  if (!a || !b) return;
  if (fromId === "outdir") b.value = a.value;
  else a.value = b.value;
}
["outdir", "outdirDrawer"].forEach(id => {
  const el = document.getElementById(id);
  if (el) el.addEventListener("input", () => syncOutdir(id));
});

function syncSelectPair(primaryId, drawerId, onChange) {
  const a = document.getElementById(primaryId);
  const b = document.getElementById(drawerId);
  if (!a || !b) return;
  a.addEventListener("change", () => { b.value = a.value; onChange && onChange(); });
  b.addEventListener("change", () => { a.value = b.value; a.dispatchEvent(new Event("change")); });
}
syncSelectPair("fmt", "drawerFmt");
syncSelectPair("palette", "drawerPalette", () => {
  applyPalette(main);
  document.querySelectorAll(".thumb iframe").forEach(f => applyPalette(f));
});
(function wireDrawerPersonFolder() {
  const dp = document.getElementById("drawerPersonFilter");
  const df = document.getElementById("drawerFolderFilter");
  if (dp) dp.addEventListener("change", () => {
    document.getElementById("personFilter").value = dp.value;
    document.getElementById("personFilter").dispatchEvent(new Event("change"));
    closeDrawer();
  });
  if (df) df.addEventListener("change", () => {
    document.getElementById("folderFilter").value = df.value;
    document.getElementById("folderFilter").dispatchEvent(new Event("change"));
    closeDrawer();
  });
})();

/* ---- Drawer + search overlay (responsive ≤767.98) ---- */
function openDrawer() {
  const drawer = document.getElementById("hubDrawer");
  const backdrop = document.getElementById("hubDrawerBackdrop");
  const toggle = document.getElementById("drawerToggle");
  if (!drawer) return;
  drawer.classList.add("open");
  drawer.setAttribute("aria-hidden", "false");
  if (backdrop) { backdrop.hidden = false; backdrop.classList.add("open"); }
  document.body.classList.add("drawer-open");
  if (toggle) toggle.setAttribute("aria-expanded", "true");
}
function closeDrawer() {
  const drawer = document.getElementById("hubDrawer");
  const backdrop = document.getElementById("hubDrawerBackdrop");
  const toggle = document.getElementById("drawerToggle");
  if (!drawer) return;
  drawer.classList.remove("open");
  drawer.setAttribute("aria-hidden", "true");
  if (backdrop) { backdrop.classList.remove("open"); backdrop.hidden = true; }
  document.body.classList.remove("drawer-open");
  if (toggle) toggle.setAttribute("aria-expanded", "false");
}
function openSearchOvl() {
  const ovl = document.getElementById("hubSearchOvl");
  const input = document.getElementById("searchOvlInput");
  if (!ovl) return;
  ovl.hidden = false;
  ovl.classList.add("open");
  if (input) {
    input.value = document.getElementById("search").value || "";
    input.focus();
    input.select();
  }
  renderSearchOvl();
}
function closeSearchOvl() {
  const ovl = document.getElementById("hubSearchOvl");
  if (!ovl) return;
  ovl.classList.remove("open");
  ovl.hidden = true;
}
function renderSearchOvl() {
  const box = document.getElementById("searchOvlResults");
  const input = document.getElementById("searchOvlInput");
  if (!box || !input) return;
  const q = input.value.trim().toLowerCase();
  document.getElementById("search").value = input.value;
  const hits = !q ? [] : DOCS.filter(d => {
    const hay = `${d.path} ${d.name} ${d.label} ${d.group} ${d.kind}`.toLowerCase();
    return hay.includes(q);
  }).slice(0, 40);
  box.innerHTML = "";
  if (!q) {
    box.innerHTML = '<div class="hub-search-ovl-empty">Type to search the library</div>';
    return;
  }
  if (!hits.length) {
    box.innerHTML = '<div class="hub-search-ovl-empty">No matches</div>';
    return;
  }
  for (const d of hits) {
    const row = document.createElement("button");
    row.type = "button";
    row.className = "hub-search-ovl-item";
    row.innerHTML = `<span class="name">${d.name}</span><span class="path">${d.path}</span>`;
    row.addEventListener("click", () => {
      closeSearchOvl();
      kindFilter = "all";
      buildKindChips();
      renderLibrary();
      select(d, null, { pushUrl: true });
    });
    box.appendChild(row);
  }
}
(function wireDrawerSearch() {
  const toggle = document.getElementById("drawerToggle");
  const closeBtn = document.getElementById("drawerClose");
  const backdrop = document.getElementById("hubDrawerBackdrop");
  const searchTrigger = document.getElementById("searchTrigger");
  const searchOvlInput = document.getElementById("searchOvlInput");
  const drawerRefresh = document.getElementById("drawerRefresh");
  if (toggle) toggle.addEventListener("click", () => {
    const open = document.getElementById("hubDrawer")?.classList.contains("open");
    if (open) closeDrawer(); else openDrawer();
  });
  if (closeBtn) closeBtn.addEventListener("click", closeDrawer);
  if (backdrop) backdrop.addEventListener("click", closeDrawer);
  if (searchTrigger) searchTrigger.addEventListener("click", openSearchOvl);
  if (searchOvlInput) {
    searchOvlInput.addEventListener("input", () => {
      renderSearchOvl();
      renderLibrary();
    });
    searchOvlInput.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        const first = document.querySelector(".hub-search-ovl-item");
        if (first) first.click();
      }
    });
  }
  if (drawerRefresh) drawerRefresh.addEventListener("click", () => {
    document.getElementById("refreshBtn")?.click();
    closeDrawer();
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") { closeDrawer(); closeSearchOvl(); }
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
      e.preventDefault();
      openSearchOvl();
    }
  });
})();

document.getElementById("exportBtn").addEventListener("click", async () => {
  const status = document.getElementById("status");
  if (!selected) { status.textContent = "select a template first"; return; }
  status.textContent = "exporting…";
  const idx = paletteSel.value;
  const body = {
    doc: selected.path,
    format: document.getElementById("fmt").value,
    outDir: readOutdir(),
    cssVars: idx === "" ? null : PALETTES[idx].vars,
  };
  try {
    const r = await fetch("/api/export", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const data = await r.json();
    status.textContent = data.ok ? ("saved: " + data.outputs.join(" · ")) : ("error: " + data.error);
  } catch (e) {
    status.textContent = "error: " + e;
  }
});

buildStats();
buildKindChips();
buildFolderSelect();
/* Restore profile filter after folder options exist (folder value restored in buildFolderSelect). */
(function restoreHubPrefs() {
  try {
    const prof = localStorage.getItem(HUB_PROFILE_KEY) || "";
    const sel = document.getElementById("personFilter");
    if (prof && [...sel.options].some(o => o.value === prof)) sel.value = prof;
  } catch (_) {}
  syncPinButton();
})();
renderLibrary();
openFromQuery();
openPaletteFromQuery();

/* ---- Auto-refresh watcher ----
   Polls /api/version; when the tree signature changes (a new resume exported,
   an HTML source edited), refresh the library, reload the open preview, and
   flash a subtle toast. No manual restart needed. */
(function autoRefresh() {
  let sig = null;
  let busy = false;
  const INTERVAL = 1500;

  function toast(msg) {
    let t = document.getElementById("refreshToast");
    if (!t) {
      t = document.createElement("div");
      t.id = "refreshToast";
      t.style.cssText =
        "position:fixed;bottom:16px;right:16px;z-index:9999;padding:8px 14px;" +
        "border-radius:999px;font:600 12px/1 'Inter',system-ui,sans-serif;" +
        "background:rgba(20,20,22,0.92);color:#fff;border:1px solid rgba(255,255,255,0.18);" +
        "box-shadow:0 6px 24px rgba(0,0,0,0.4);opacity:0;transition:opacity .25s;pointer-events:none;";
      document.body.appendChild(t);
    }
    t.textContent = msg;
    t.style.opacity = "1";
    clearTimeout(t._h);
    t._h = setTimeout(() => { t.style.opacity = "0"; }, 2200);
  }

  function applyDocs(data) {
    const prevCount = DOCS.length;
    DOCS = data.docs;
    if (selected) {
      const still = DOCS.find(d => d.path === selected.path);
      selected = still || null;
    }
    buildKindChips();
    buildFolderSelect();
    renderLibrary();
    if (selected) { try { main.src = "/" + selected.path + "?t=" + Date.now(); } catch (_) {} }
    return DOCS.length - prevCount;
  }

  async function tick() {
    if (busy) return;
    busy = true;
    try {
      const r = await fetch("/api/version", { cache: "no-store" });
      if (r.ok) {
        const data = await r.json();
        if (sig === null) {
          sig = data.sig;
        } else if (data.sig !== sig) {
          sig = data.sig;
          const delta = applyDocs(data);
          toast(delta > 0 ? ("＋" + delta + " document" + (delta > 1 ? "s" : "")) :
                delta < 0 ? (delta + " document" + (delta < -1 ? "s" : "")) :
                "updated");
        }
      }
    } catch (_) { /* server down mid-poll — ignore, retry next tick */ }
    finally { busy = false; }
  }

  // Manual refresh — re-scan on demand (always re-render, even if the signature
  // is unchanged), so the button is a reliable "show me what's on disk now".
  async function forceRefresh() {
    try {
      const r = await fetch("/api/version", { cache: "no-store" });
      if (!r.ok) { toast("refresh failed"); return; }
      const data = await r.json();
      sig = data.sig;
      const delta = applyDocs(data);
      toast(delta === 0 ? ("refreshed · " + DOCS.length + " docs")
            : (delta > 0 ? "＋" : "") + delta + " · " + DOCS.length + " docs");
    } catch (_) { toast("refresh failed"); }
  }

  const rb = document.getElementById("refreshBtn");
  if (rb) rb.addEventListener("click", forceRefresh);

  tick();
  setInterval(tick, INTERVAL);
})();
</script>
</body>
</html>
"""


def make_handler(root: Path, docs: list[dict], palettes: list[dict]):
    app_page = (
        APP_HTML.replace("__DOCS__", json.dumps(docs))
        .replace("__PALETTES__", json.dumps(palettes))
        .replace("__ROOT__", str(root))
    )

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def _send(self, code: int, body: bytes, ctype: str):
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            path = unquote(urlparse(self.path).path)
            if path in ("/", "/index.html"):
                self._send(200, app_page.encode("utf-8"), "text/html; charset=utf-8")
                return
            if path == "/api/version":
                # Auto-refresh poll: current tree signature + a fresh doc list.
                # Re-scanning docs here keeps the sidebar live when HTML sources
                # or _exports outputs change, without restarting the server.
                sig = tree_signature(root)
                payload = {"sig": sig, "docs": scan_documents(root)}
                self._send(200, json.dumps(payload).encode("utf-8"), "application/json")
                return
            if path == "/api/vault-overview":
                payload = build_vault_overview(root)
                self._send(200, json.dumps(payload).encode("utf-8"), "application/json")
                return
            if path == "/api/recipe-gallery":
                payload = build_recipe_gallery(root)
                self._send(200, json.dumps(payload).encode("utf-8"), "application/json")
                return
            if path in ("/vault", "/vault.html"):
                target = (_STATIC_DIR / "vault.html").resolve()
                if not target.is_file():
                    self._send(404, b"vault.html missing", "text/plain")
                    return
                self._send(200, target.read_bytes(), "text/html; charset=utf-8")
                return
            if path in ("/recipes", "/recipes.html"):
                target = (_STATIC_DIR / "recipes.html").resolve()
                if not target.is_file():
                    self._send(404, b"recipes.html missing", "text/plain")
                    return
                self._send(200, target.read_bytes(), "text/html; charset=utf-8")
                return
            if path.startswith("/_hub/"):
                name = path[len("/_hub/") :]
                if not re.fullmatch(r"[A-Za-z0-9._-]+", name or ""):
                    self._send(404, b"not found", "text/plain")
                    return
                target = (_STATIC_DIR / name).resolve()
                if not str(target).startswith(str(_STATIC_DIR.resolve())) or not target.is_file():
                    self._send(404, b"not found", "text/plain")
                    return
                ctype = {
                    ".css": "text/css; charset=utf-8",
                    ".js": "text/javascript; charset=utf-8",
                    ".svg": "image/svg+xml",
                }.get(target.suffix.lower(), "application/octet-stream")
                self._send(200, target.read_bytes(), ctype)
                return
            target = (root / path.lstrip("/")).resolve()
            if not str(target).startswith(str(root.resolve())) or not target.is_file():
                self._send(404, b"not found", "text/plain")
                return
            ctype = {
                ".html": "text/html; charset=utf-8",
                ".css": "text/css",
                ".js": "text/javascript",
                ".json": "application/json",
                ".png": "image/png",
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".webp": "image/webp",
                ".gif": "image/gif",
                ".svg": "image/svg+xml",
            }.get(target.suffix.lower(), "application/octet-stream")
            self._send(200, target.read_bytes(), ctype)

        def do_POST(self):
            if urlparse(self.path).path != "/api/export":
                self._send(404, b"{}", "application/json")
                return
            try:
                length = int(self.headers.get("Content-Length", 0))
                req = json.loads(self.rfile.read(length))
                doc = (root / req["doc"]).resolve()
                if not str(doc).startswith(str(root.resolve())) or not doc.is_file():
                    raise ValueError(f"bad doc path: {req['doc']}")
                fmt = req.get("format", "pdf-light")
                pdf_theme = "dark" if fmt.endswith("-dark") else None
                out_dir = req.get("outDir") or None
                if fmt.startswith("png"):
                    outputs = [
                        str(p)
                        for p in render_to_png(str(doc), out_dir, pdf_theme=pdf_theme)
                    ]
                else:
                    pdf = export_html_to_pdf(
                        str(doc),
                        output_dir=out_dir,
                        pdf_theme=pdf_theme,
                        css_vars=req.get("cssVars"),
                    )
                    outputs = [str(pdf)]
                self._send(200, json.dumps({"ok": True, "outputs": outputs}).encode(), "application/json")
            except Exception as exc:
                self._send(200, json.dumps({"ok": False, "error": str(exc)}).encode(), "application/json")

    return Handler


def serve(root: str | None = None, port: int = 8787, open_browser: bool = True):
    root_path = Path(root).resolve() if root else _REPO_ROOT
    if not root_path.is_dir():
        raise FileNotFoundError(root_path)
    docs = scan_documents(root_path)
    palettes = load_palettes()
    server = ThreadingHTTPServer(("127.0.0.1", port), make_handler(root_path, docs, palettes))
    url = f"http://127.0.0.1:{port}/"
    by_kind = {}
    for d in docs:
        by_kind[d["kind"]] = by_kind.get(d["kind"], 0) + 1
    kind_summary = ", ".join(f"{k}={v}" for k, v in sorted(by_kind.items()))
    print(f"Design Hub: {url}")
    print(f"  {len(docs)} templates ({kind_summary})")
    print(f"  {len(palettes)} palettes · root: {root_path}")
    print("  Filters: kind · folder · person · search — Ctrl+C to stop.")
    if open_browser:
        threading.Timer(0.4, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


def main() -> None:
    args = sys.argv[1:]
    port = 8787
    open_browser = True
    root = None
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--port":
            port = int(args[i + 1])
            i += 1
        elif a.startswith("--port="):
            port = int(a.split("=", 1)[1])
        elif a == "--no-open":
            open_browser = False
        elif a in ("-h", "--help"):
            print(__doc__)
            raise SystemExit(0)
        else:
            root = a
        i += 1
    serve(root, port=port, open_browser=open_browser)


if __name__ == "__main__":
    main()
