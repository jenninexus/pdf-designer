# Public release content boundary

**Status:** [github.com/jenninexus/pdf-designer](https://github.com/jenninexus/pdf-designer)
is a **public MIT** repo today. This page is the clone-safety checklist for that
free product — not a “someday publish” plan.

Paid work (signed Windows installer, storefront, guided-wizard chrome) is a
**later shell** over the same engine. It is **not** required for the GitHub
product and must not gate clone-safe engine/docs fixes.

Companion: [`PUBLIC-LOCAL-SPLIT.md`](PUBLIC-LOCAL-SPLIT.md) · thesis:
[`PRODUCT.md`](PRODUCT.md) · clone path: [`GETTING-STARTED.md`](GETTING-STARTED.md).

## What the free GitHub product includes

A stranger who clones and runs `pip install -e ".[dev]"` + `playwright install chromium`
gets:

| Surface | What ships |
|---|---|
| Engine | `src/pdf_tool/` — HTML→PDF, Design Hub, collage, merge, PNG, guards |
| Look | `themes/` (default + presets + palette rule) · `layouts/` |
| Demo | `examples/` including `resume-studio/` and Jane Example |
| Protocol seeds | `.claude/commands/*.example.md` (placeholders only) |
| Docs | Public `docs/*.md` in this index · `README.md` · `LICENSE` (MIT) |
| Lessons | `.memory/README.md` + `.memory/lesson-*.md` |
| Export layout | Tracked `output/README.md` — engine default is `output/<user>/<kind>/` (PDF/PNG payload gitignored) |
| Proof | `python scripts/smoke-white-label.py` · `python scripts/check-wheel-assets.py` |

**Intended public fixes** (engine/docs/examples that a clone needs) land on
`main` and are pushed. They are the free product. Do not hold them for a paid
installer, TestPyPI, or a clean-machine Electron gate.

Current example: repo-root `output/` as the default export tree (HTML stays in
`resumes/` / `collages/` / `examples/`). That is clone UX, not a paid feature.

## What the free product does not include

| Keep off GitHub / out of the pitch | Why |
|---|---|
| Live `users/` · `vaults/` · `profiles/` · `resumes/` payload · `_job-apps/` listings · `collages/` images · `brands/` hex | Real people and jobs |
| Generated `output/**/*.pdf` (and PNG) | Personal renders; the folder *shape* is public, the files are not |
| Bare `.claude/commands/*.md` (`start` / `wrap` / `make-*` / commands README) | Dev ritual + personal specifics |
| `Plans/` · `dev-log-sego.yaml` · `docs/MARKETING.md` · `WORKSPACE.md` · `HISTORY-SCRUB.md` | Operating records |
| Machine `.config/mcp-pdf-designer.json` | Absolute paths |
| Signed Electron/NSIS download, PayPal/Gumroad fulfilment, production PyPI | Paid / later channels — [`PRODUCT.md`](PRODUCT.md) · [`PACKAGING.md`](PACKAGING.md) · [`WINDOWS-ELECTRON.md`](WINDOWS-ELECTRON.md) |
| `www-theme-kit` as a required dependency | Private brand infra; public color lives in `themes/` |

## Keep public (checklist)

- The engine, layouts, public themes and font notices.
- Fictional examples and the white-label smoke test.
- Product-facing technical documentation: setup, exports (including `output/`),
  previewer, packaging, quality checks, licensing, theming, collage design, and
  the optional Voice Seed handoff contract.
- Deliberately approved promotional images under `docs/images/`.
- Durable lessons (`.memory/lesson-*.md`) that do not embed vault bodies.

## Keep local only

- Agent session ritual, `Plans/`, session memory logs, and history-rewrite notes.
- Live user, vault, profile, job, résumé, brand, export payload, and collage data.
- Application workflow notes that describe real people, real work, or local paths.
- Any secret, token, environment configuration, capture, or unpublished media.

## Ongoing clone-safety (every push to public `main`)

1. Stage **explicit clone-safe paths**. Never `git add -A`. Never stage vaults,
   real PDFs, bare command files, or force-add gitignored paths.
2. Public docs must not grow machine paths, private names, or operational history.
3. Public `*.example.*` files stay placeholders; audit **content**, not the suffix.
4. Run `python scripts/smoke-white-label.py` and
   `python scripts/check-wheel-assets.py` when engine, examples, or wheel assets
   change.
5. **History rewrite / force-push** still needs explicit human approval.
   Ordinary fast-forward of tracked, clone-safe commits *is* how this public
   product updates.

Ignore policy + docs index are in place. Live private files stay on disk via
`.gitignore`. GitHub should match `main` for the free toolkit — including export
layout and these boundary docs.
