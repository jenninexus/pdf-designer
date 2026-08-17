# CLAUDE.md

**Read [`AGENTS.md`](AGENTS.md)** — it is the single agent-facing SSOT for this repo (capability map,
repo map, contracts, command surface, reading order). This file exists only so Claude Code auto-loads it;
everything in `AGENTS.md` applies here identically.

Quick start (all detailed in `AGENTS.md`):

- **Design Hub:** `python -m pdf_tool.preview` → http://127.0.0.1:8787/
- **One-time:** `pip install -e ".[dev]" && playwright install chromium`
- **Active plan:** [`Plans/_Active/2026-08-13-intuitive-workspace-product.md`](Plans/_Active/2026-08-13-intuitive-workspace-product.md)
- **Start / wrap:** local [`.claude/commands/pdf-start.md`](.claude/commands/pdf-start.md) · [`.claude/commands/pdf-wrap.md`](.claude/commands/pdf-wrap.md) · `/pdf-start` · `/pdf-wrap` (`/start` and `/wrap` are thin aliases) — wrap requires **`/reflect`** + next-agent handoff + `dev-log-sego.yaml` (bare commands are gitignored; GitHub has `*.example.md` only)
- **Jenni's cross-workspace doc tool:** `/jen:docs` — repo SSOT itself is [`docs/SSOT.md`](docs/SSOT.md) § Personal palette prefs
