# CLAUDE.md

**Read [`AGENTS.md`](AGENTS.md)** — it is the single agent-facing SSOT for this repo (capability map,
repo map, contracts, command surface, reading order). This file exists only so Claude Code auto-loads it;
everything in `AGENTS.md` applies here identically.

Quick start (all detailed in `AGENTS.md`):

- **Design Hub:** `python -m pdf_tool.preview` → http://127.0.0.1:8787/
- **One-time:** `pip install -e ".[dev]" && playwright install chromium`
- **Active plan:** [`Plans/_Active/2026-08-13-intuitive-workspace-product.md`](Plans/_Active/2026-08-13-intuitive-workspace-product.md)
- **Wrap:** local [`.claude/commands/wrap.md`](.claude/commands/wrap.md) · `/wrap` · `/jen:wrap` — **`/reflect`** + next-agent handoff + `dev-log-sego.yaml` (bare wrap is gitignored; GitHub has `*.example.md` only)
- **Jenni's cross-workspace doc tool:** `/jen:docs` — repo SSOT itself is [`docs/SSOT.md`](docs/SSOT.md) § Personal palette prefs
