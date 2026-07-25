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
EXCLUDE_PARTS = {"_exports", "node_modules", ".git", "__pycache__", ".venv", "venv"}

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
    elif any(path_l.startswith(f"storage/{u}/") for u in ("jenni", "shade")):
        bucket = "vault-renders"
    else:
        bucket = "other"

    person = None
    if name_l.startswith("jenni"):
        person = "jenni"
    elif name_l.startswith("shade"):
        person = "shade"

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
        "person": person,
        "template": True,  # each HTML file is its own selectable template
    }


def scan_documents(root: Path) -> list[dict]:
    docs = []
    for p in sorted(root.rglob("*.html")):
        rel = p.relative_to(root)
        if EXCLUDE_PARTS.intersection(rel.parts):
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
        if _WATCH_EXCLUDE.intersection(rel_parts):
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
  <h1 class="hub-brand" title="__ROOT__">Design Hub</h1>
  <nav class="hub-nav" aria-label="Hub sections">
    <a class="hub-link on" href="/" title="Document library" aria-current="page">Library</a>
    <a class="hub-link" href="/recipes" title="Browse layouts/ + themes/presets">Recipes</a>
    <a class="hub-link" href="/vault" title="Readable vault · skills · go-to résumés">Vault</a>
  </nav>
  <div class="chips" id="kindChips" role="tablist" aria-label="Document kind"></div>
  <div class="hub-spacer"></div>
  <input id="search" type="search" placeholder="Search…" autocomplete="off" title="Search name or path" aria-label="Search">
  <select id="folderFilter" title="Folder" aria-label="Folder"><option value="">all folders</option></select>
  <select id="personFilter" title="Who" aria-label="Person">
    <option value="">anyone</option>
    <option value="jenni">jenni</option>
    <option value="shade">shade</option>
  </select>
  <select id="palette" title="Palette" aria-label="Palette"><option value="">doc default</option></select>
  <select id="fmt" title="Export format" aria-label="Export format">
    <option value="pdf-light">PDF light</option>
    <option value="pdf-dark">PDF dark</option>
    <option value="png-light">PNG light</option>
    <option value="png-dark">PNG dark</option>
  </select>
  <details class="hub-more">
    <summary title="More export options">⋯</summary>
    <div class="hub-more-panel">
      <label>Output folder
        <input id="outdir" type="text" placeholder="_exports next to doc">
      </label>
    </div>
  </details>
  <button id="refreshBtn" type="button" title="Re-scan the repo for new/changed documents">&#8635; Refresh</button>
  <button class="primary" id="exportBtn" type="button">Export</button>
  <span id="status"></span>
</header>

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
const KIND_ORDER = ["all","resume","cover-letter","collage","gallery","example","other"];
const KIND_LABEL = {
  all: "All",
  resume: "Resumes",
  "cover-letter": "Cover letters",
  collage: "Collages",
  gallery: "Galleries",
  example: "Examples",
  other: "Other",
};

let selected = null;
let kindFilter = "all";

const paletteSel = document.getElementById("palette");
PALETTES.forEach((p, i) => {
  const o = document.createElement("option");
  o.value = i;
  o.textContent = p.name;
  paletteSel.appendChild(o);
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

function buildKindChips() {
  const c = counts();
  const wrap = document.getElementById("kindChips");
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
    });
    wrap.appendChild(b);
  }
}

function uniqueFolders() {
  return [...new Set(DOCS.map(d => d.group))].sort();
}

function buildFolderSelect() {
  const sel = document.getElementById("folderFilter");
  const cur = sel.value;
  sel.innerHTML = '<option value="">all folders</option>';
  for (const g of uniqueFolders()) {
    const o = document.createElement("option");
    o.value = g;
    o.textContent = g;
    sel.appendChild(o);
  }
  if ([...sel.options].some(o => o.value === cur)) sel.value = cur;
}

function filteredDocs() {
  const q = document.getElementById("search").value.trim().toLowerCase();
  const folder = document.getElementById("folderFilter").value;
  const person = document.getElementById("personFilter").value;
  return DOCS.filter(d => {
    if (kindFilter !== "all" && d.kind !== kindFilter) return false;
    if (folder && d.group !== folder) return false;
    if (person && d.person !== person) return false;
    if (q) {
      const hay = `${d.path} ${d.name} ${d.label} ${d.group} ${d.kind}`.toLowerCase();
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
      if (d.person) badges.push(`<span class="badge person-${d.person}">${d.person}</span>`);
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
  document.getElementById("personFilter").value = d.person || "";
  document.getElementById("search").value = "";
  buildKindChips();
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

document.getElementById("folderFilter").addEventListener("change", renderLibrary);
document.getElementById("personFilter").addEventListener("change", renderLibrary);
document.getElementById("search").addEventListener("input", renderLibrary);

document.getElementById("exportBtn").addEventListener("click", async () => {
  const status = document.getElementById("status");
  if (!selected) { status.textContent = "select a template first"; return; }
  status.textContent = "exporting…";
  const idx = paletteSel.value;
  const body = {
    doc: selected.path,
    format: document.getElementById("fmt").value,
    outDir: document.getElementById("outdir").value || null,
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
