"""Design Hub — local previewer for every renderable document in the repo.

The PowerPoint-style picker, generalized: a sidebar of live thumbnails for
every .html document it finds (resume renders, collage candidates, cover
letters), a large preview pane, a palette swapper to audition color schemes,
and one-click export of the selected document to PDF (light/dark) or PNG —
into whatever output folder you choose.

Zero new dependencies: stdlib http.server for the app shell; exports reuse
html_to_pdf.py / pdf_to_png.py (Playwright only -- no other engine needed).
Bound to 127.0.0.1 only.

Usage:
    python -m pdf_tool.preview                     # scan the repo, serve on :8787
    python -m pdf_tool.preview path/to/dir         # scan any directory instead
    python -m pdf_tool.preview --port 9000

Palettes offered by the swapper come from themes/*.json (public) and
storage/brands/*.json (private, gitignored) — drop another palette file there
to audition more color combos. Palette preview is WYSIWYG for export: the
chosen palette is injected into the PDF/PNG via html_to_pdf's css_vars hook.
"""

import json
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

from .html_to_pdf import export_html_to_pdf
from .pdf_to_png import render_to_png

_REPO_ROOT = Path(__file__).resolve().parents[2]
EXCLUDE_PARTS = {"_exports", "node_modules", ".git", "__pycache__", ".venv", "venv"}

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


def scan_documents(root: Path) -> list[dict]:
    docs = []
    for p in sorted(root.rglob("*.html")):
        rel = p.relative_to(root)
        if EXCLUDE_PARTS.intersection(rel.parts):
            continue
        group = str(rel.parent).replace("\\", "/")
        docs.append({"path": str(rel).replace("\\", "/"), "name": p.stem, "group": "." if group == "." else group})
    return docs


def load_palettes() -> list[dict]:
    """Every dark/light block from themes/*.json (public) + storage/brands/*.json (private)."""
    palettes = []
    for theme_dir in (_REPO_ROOT / "themes", _REPO_ROOT / "storage" / "brands"):
        if not theme_dir.is_dir():
            continue
        for f in sorted(theme_dir.glob("*.json")):
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
            except Exception:
                continue
            for mode in ("dark", "light"):
                block = data.get(mode)
                if not isinstance(block, dict):
                    continue
                vars_ = {}
                for var, section, key in _TOKEN_MAP:
                    value = block.get(section, {}).get(key)
                    if value:
                        vars_[var] = value
                if vars_:
                    palettes.append({"name": f"{f.stem} · {mode}", "vars": vars_})
    return palettes


APP_HTML = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>pdf-designer — Design Hub</title>
<style>
  :root { --bg:#0b0d12; --surface:#10131a; --line:rgba(79,209,201,0.16); --line2:rgba(79,209,201,0.5);
          --text:rgba(240,242,246,0.94); --dim:rgba(240,242,246,0.6); --teal:#4fd1c9; --gold:#e3b559; }
  * { box-sizing: border-box; }
  body { margin:0; height:100vh; display:flex; flex-direction:column; background:var(--bg); color:var(--text);
         font-family:'Inter',ui-sans-serif,system-ui,sans-serif; font-size:13px; }
  header { display:flex; align-items:center; gap:14px; padding:10px 16px; border-bottom:1px solid var(--line);
           background:var(--surface); flex-wrap:wrap; }
  header h1 { font-size:14px; margin:0; letter-spacing:0.08em; color:var(--teal); text-transform:uppercase; }
  header .root { color:var(--dim); font-size:11px; }
  select,input,button { background:#171b24; color:var(--text); border:1px solid var(--line); border-radius:7px;
                        padding:6px 9px; font-size:12px; font-family:inherit; }
  button { cursor:pointer; } button:hover { border-color:var(--line2); }
  button.primary { background:var(--teal); color:#08211f; font-weight:700; border-color:transparent; }
  #status { font-size:11.5px; color:var(--gold); max-width:340px; }
  main { flex:1; display:flex; min-height:0; }
  aside { width:262px; overflow-y:auto; border-right:1px solid var(--line); background:var(--surface); padding:12px; }
  aside h2 { font-size:10.5px; letter-spacing:0.12em; text-transform:uppercase; color:var(--dim); margin:14px 0 8px; }
  .thumb { display:block; width:100%; border:1px solid var(--line); border-radius:9px; overflow:hidden;
           margin-bottom:10px; background:#000; cursor:pointer; position:relative; }
  .thumb.sel { border-color:var(--line2); box-shadow:0 0 0 2px var(--line2); }
  .thumb .frame { height:150px; overflow:hidden; position:relative; pointer-events:none; }
  .thumb iframe { border:0; transform-origin:top left; position:absolute; top:0; left:0; }
  .thumb .cap { padding:6px 9px; font-size:11px; color:var(--teal); border-top:1px solid var(--line);
                background:var(--surface); white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
  #stage { flex:1; min-width:0; display:flex; flex-direction:column; }
  #stage iframe { flex:1; border:0; width:100%; background:#333; }
  #stagebar { padding:6px 14px; font-size:11.5px; color:var(--dim); border-bottom:1px solid var(--line); }
</style>
</head>
<body>
<header>
  <h1>Design Hub</h1>
  <span class="root">__ROOT__</span>
  <label>palette <select id="palette"><option value="">(document default)</option></select></label>
  <label>export <select id="fmt">
    <option value="pdf-light">PDF · light/print</option>
    <option value="pdf-dark">PDF · dark/branded</option>
    <option value="png-light">PNG pages · light</option>
    <option value="png-dark">PNG pages · dark</option>
  </select></label>
  <label>to <input id="outdir" size="28" placeholder="(default: _exports next to doc)"></label>
  <button class="primary" id="exportBtn">Export selected</button>
  <span id="status"></span>
</header>
<main>
  <aside id="sidebar"></aside>
  <div id="stage">
    <div id="stagebar">select a document on the left</div>
    <iframe id="main" src="about:blank"></iframe>
  </div>
</main>
<script>
const DOCS = __DOCS__;
const PALETTES = __PALETTES__;
let selected = null;

const paletteSel = document.getElementById('palette');
PALETTES.forEach((p,i)=>{ const o=document.createElement('option'); o.value=i; o.textContent=p.name; paletteSel.appendChild(o); });

function applyPalette(iframe){
  const idx = paletteSel.value;
  const doc = iframe.contentDocument; if(!doc) return;
  const st = doc.documentElement.style;
  // clear previous overrides, then apply
  for(const p of PALETTES) for(const k of Object.keys(p.vars)) st.removeProperty(k);
  if(idx !== '') for(const [k,v] of Object.entries(PALETTES[idx].vars)) st.setProperty(k,v);
}

const sidebar = document.getElementById('sidebar');
const groups = {};
DOCS.forEach(d => { (groups[d.group] ||= []).push(d); });
const THUMB_W = 236;
for(const [group, docs] of Object.entries(groups)){
  const h = document.createElement('h2'); h.textContent = group; sidebar.appendChild(h);
  for(const d of docs){
    const el = document.createElement('div'); el.className='thumb'; el.dataset.path=d.path;
    el.innerHTML = `<div class="frame"><iframe loading="lazy" src="/${d.path}" scrolling="no" tabindex="-1"></iframe></div><div class="cap">${d.name}</div>`;
    const ifr = el.querySelector('iframe');
    ifr.addEventListener('load', ()=>{
      const w = ifr.contentDocument?.body?.scrollWidth || 850;
      const s = THUMB_W / Math.max(w, 320);
      ifr.style.width = Math.max(w,320)+'px'; ifr.style.height = (150/s)+'px'; ifr.style.transform = `scale(${s})`;
      applyPalette(ifr);
    });
    el.addEventListener('click', ()=> select(d, el));
    sidebar.appendChild(el);
  }
}

const main = document.getElementById('main');
main.addEventListener('load', ()=> applyPalette(main));
paletteSel.addEventListener('change', ()=>{
  applyPalette(main);
  document.querySelectorAll('.thumb iframe').forEach(f=>applyPalette(f));
});

function select(d, el){
  selected = d;
  document.querySelectorAll('.thumb').forEach(t=>t.classList.remove('sel'));
  el.classList.add('sel');
  document.getElementById('stagebar').textContent = d.path;
  main.src = '/' + d.path;
}

document.getElementById('exportBtn').addEventListener('click', async ()=>{
  const status = document.getElementById('status');
  if(!selected){ status.textContent = 'select a document first'; return; }
  status.textContent = 'exporting…';
  const idx = paletteSel.value;
  const body = {
    doc: selected.path,
    format: document.getElementById('fmt').value,
    outDir: document.getElementById('outdir').value || null,
    cssVars: idx === '' ? null : PALETTES[idx].vars,
  };
  try {
    const r = await fetch('/api/export', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(body)});
    const data = await r.json();
    status.textContent = data.ok ? ('saved: ' + data.outputs.join(' · ')) : ('error: ' + data.error);
  } catch(e){ status.textContent = 'error: ' + e; }
});
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
            target = (root / path.lstrip("/")).resolve()
            if not str(target).startswith(str(root)) or not target.is_file():
                self._send(404, b"not found", "text/plain")
                return
            ctype = {
                ".html": "text/html; charset=utf-8", ".css": "text/css", ".js": "text/javascript",
                ".json": "application/json", ".png": "image/png", ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg", ".webp": "image/webp", ".gif": "image/gif", ".svg": "image/svg+xml",
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
                if not str(doc).startswith(str(root)) or not doc.is_file():
                    raise ValueError(f"bad doc path: {req['doc']}")
                fmt = req.get("format", "pdf-light")
                pdf_theme = "dark" if fmt.endswith("-dark") else None
                out_dir = req.get("outDir") or None
                if fmt.startswith("png"):
                    # PNGs render straight from the HTML -- no PDF round-trip. (They used
                    # to be rasterized out of the exported PDF by PyMuPDF, which is AGPL
                    # and had to go; see docs/LICENSING-NOTES.md.)
                    outputs = [
                        str(p)
                        for p in render_to_png(str(doc), out_dir, pdf_theme=pdf_theme)
                    ]
                else:
                    pdf = export_html_to_pdf(
                        str(doc), output_dir=out_dir, pdf_theme=pdf_theme, css_vars=req.get("cssVars"),
                    )
                    outputs = [str(pdf)]
                self._send(200, json.dumps({"ok": True, "outputs": outputs}).encode(), "application/json")
            except Exception as exc:  # surfaced to the UI status line
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
    print(f"Design Hub: {url}  ({len(docs)} documents, {len(palettes)} palettes, root: {root_path})")
    print("Ctrl+C to stop.")
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
            port = int(args[i + 1]); i += 1
        elif a.startswith("--port="):
            port = int(a.split("=", 1)[1])
        elif a == "--no-open":
            open_browser = False
        elif a in ("-h", "--help"):
            print(__doc__); raise SystemExit(0)
        else:
            root = a
        i += 1
    serve(root, port=port, open_browser=open_browser)


if __name__ == "__main__":
    main()
