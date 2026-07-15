# Architecture

How pdf-designer is put together, what it deliberately does *not* do, and what is actually
built versus planned.

> **Everything marked "built" below was verified against the source.** Where a feature is
> planned, it says so plainly. This document previously described modules that had never been
> written — if you find a claim here the code doesn't back, that is a bug *in this file*.

| | |
|---|---|
| [The engine](#the-engine) | What `pdf_tool` actually does |
| [One renderer](#the-one-hard-rule-one-renderer) | The rule that keeps previews honest |
| [The résumé layer](#the-résumé-layer-a-protocol-not-a-module) | Why it's a *protocol*, not code |
| [Guards](#guards--what-is-actually-enforced) | Enforced vs. advisory |
| [Repo map](#repo-map) | Where everything lives |
| [Contracts](#contracts--do-not-break-these) | What must not break |
| [Planned](#planned) | The honest roadmap |

---

## The engine

`src/pdf_tool/` — seven modules, ~1,400 lines, no framework.

| Module | Does | |
|---|---|---|
| `html_to_pdf` | HTML → PDF via headless Chromium. Light (default) and dark (`--pdf-theme dark`) from one source. Injects palette overrides as CSS vars. | ✅ built |
| `merge_pdfs` | Cover letter + résumé → one bundle. `--require-letter` validates US Letter. | ✅ built |
| `pdf_to_png` | One PNG per page. **This is the agent's eyes** — export, render, *read the PNG*. | ✅ built |
| `check_palette` | The palette guard. Rejects brown / mustard / lime. | ✅ built |
| `check_vault` | The vault guard. Validates claim schema; catches *invisible* claims. | ✅ built |
| `collage` | Six layout families from a folder of images, plus a picker gallery. | ✅ built |
| `preview` | The **Design Hub** — local previewer, live thumbnails, palette swapper, export. | ✅ built |

### No network. No environment variables.

The tool reads **zero** environment variables and makes **zero** outbound calls. Every knob is a
CLI flag or a constant; the only network-adjacent operation is Playwright loading a local
`file://` URL. The README's promise — *your data never leaves your machine* — is true at the
code level, not just as marketing.

This is also why there is **no `.env` and no `.env.example`**. Adding one would advertise a
configuration surface that does not exist and invite someone to wire up variables nothing reads.

Third-party imports are **lazy** (inside functions), so a missing Playwright breaks PDF export
without breaking the guards.

## The one hard rule: one renderer

**The Python engine is the only renderer.** Every preview is the *same HTML file* the exporter
prints, in the same browser engine. UI layers — the gallery, the palette swapper, any future
canvas editor — are thin shells that **never re-implement rendering**.

So what you preview is byte-for-byte what exports, this year and in five. UI layers may come and
go; the documents and the CLI keep working without them.

## The résumé layer: a protocol, not a module

**There is no `application_assistant` module — and there shouldn't be.**

The job-application workflow (the claim vault, company research, gap-checking, tailoring,
theming) lives in [`../.claude/commands/make-resume.md`](../.claude/commands/make-resume.md): a
**markdown protocol** an agent — or a human — follows, backed by plain JSON under `storage/` and
two Python guards.

That is a deliberate architectural choice, not an unfinished module:

- **The judgment can't be coded.** *"Does this claim genuinely answer what they're asking for?"*
  and *"is this pay below market?"* are reasoning tasks, not parsing tasks. A `match_score.py`
  computing keyword overlap would emit a number that *feels* like an answer and isn't one.
- **The data is the product.** The vault (`storage/<user>/resume-source.json`) is the real asset.
  Plain JSON: greppable, diffable, hand-editable, readable by any agent — and it will outlive
  whatever code we wrap around it.
- **Code only where correctness is mechanical.** Two things are: *is this hex brown?* and *does
  this claim reference a real track?* Both are guards; both fail loudly. Everything else is
  protocol.

The four data layers are documented in [`STORAGE.md`](STORAGE.md).

## Guards — what is actually enforced

The difference between a *rule* and a *guard* is that a guard runs whether or not anyone
remembers it. We learned that the expensive way: a brown accent shipped into a shared palette
while a perfectly good palette checker sat right there, as an optional command nobody ran.

| Guard | When it runs | On failure |
|---|---|---|
| **Palette** | **Automatically, on every `html_to_pdf` export** | **Blocks the export.** `--skip-palette-check` overrides. |
| **US Letter** | `merge_pdfs --require-letter` | Refuses to bundle |
| **Vault schema** | `python -m pdf_tool.check_vault --all` | Non-zero exit |
| **Never overwrite** | Always | Writes `-v2`, `-v3` instead of clobbering |

`check_vault` is not yet automatic — run it after editing a vault. *(It earned its keep on its
very first run: it found five claims tagged with a role track that didn't exist. They were
silently invisible, and a résumé would have quietly shipped without them.)*

## Repo map

```text
src/pdf_tool/                 the engine (7 modules — see the table above)
themes/
  PALETTE-RULES.md            ⭐ the color rule, and why it exists
  default-resume.{json,css}   the public default theme (JSON is the token SSOT; CSS mirrors it)
  brand-*.json                brand token maps — light + dark, all guard-clean
  default-collage.json        canvas presets
examples/
  profiles/default-resume/    a worked profile + the .example shapes for user / profile / vault
  profiles/default-collage/
  applications/               the one-folder-per-application workflow + its templates
docs/                         you are here
storage/                      ⛔ GITIGNORED — the real vaults, applications, exports
Plans/_Active/                live roadmap checklists
.claude/commands/             the /make-resume protocol (agent-agnostic markdown)
pyproject.toml                `pip install -e .` → `pdf_tool` importable from the repo root
```

## Contracts — do not break these

- **Geometry is locked.** US Letter, `@page { size: Letter; margin: 0.5in 0.55in 0.78in; }`.
  A palette change never alters paper size, margins, or pagination.
- **Dual mode is intentional.** Every document renders light (print / ATS — the default) *and*
  dark (`html[data-pdf-theme="dark"]`). Keep both working when you touch a template.
- **The token contract** between a theme and a document:
  `--bg --surface --elevated --elevated-2 --text --dim --dim2 --border --border2
  --primary --secondary --accent --support`. External palettes are *mapped into* these names —
  see [`THEME-DESIGN.md`](THEME-DESIGN.md).
- **Source-backed only.** No résumé claim that isn't in the vault. Employer-specific framing
  belongs in the cover letter, never the résumé body.
- **Ask before calling something a gap.** The vault records what someone *told* you — it is not
  the limit of what they can do.
- **No auto-submission.** The tool prepares; the human submits.
- **Privacy split.** `storage/`, `*.pdf`, `*.png`, `_exports/`, and every non-`.example` real
  data file are gitignored. Never move real personal data into a tracked path.

## Planned

Honest status — nothing below exists yet.

| What | Status |
|---|---|
| **Design Hub app** — pywebview shell around the existing previewer; variant generation; canvas editor | Roadmapped. The previewer already works; the shell is polish. See [`PREVIEWER.md`](PREVIEWER.md) and `Plans/_Active/`. |
| **PDF form filling** — AcroForm field filling, flat-PDF overlay filling | **Deferred indefinitely.** This was the repo's *original* premise and has never once been needed — every real document has been HTML → PDF. Don't build it until something actually demands it. |

> The previous version of this document described a `src/application_assistant/` package
> (`job_listing.py`, `match_score.py`, `tailor_resume.py`, …) plus `templates/` and `tests/`
> trees. **None of it was ever written**, and the résumé layer turned out to work better as a
> protocol. Those trees are deleted from this doc rather than left standing as aspirational
> fiction — a roadmap that reads like an inventory is worse than no roadmap.

## See also

[`STORAGE.md`](STORAGE.md) — the four data layers ·
[`EXPORTS.md`](EXPORTS.md) — export commands and pagination traps ·
[`THEME-DESIGN.md`](THEME-DESIGN.md) — the token contract ·
[`../themes/PALETTE-RULES.md`](../themes/PALETTE-RULES.md) — the color rule ·
[`PREVIEWER.md`](PREVIEWER.md) · [`COLLAGE-DESIGN.md`](COLLAGE-DESIGN.md)
