# Roadmap (started 2026-07-11 · re-prioritized 2026-07-13)

Design SSOT: [`../../docs/PREVIEWER.md`](../../docs/PREVIEWER.md). This file is the working
checklist — check items off as they land.

---

## Where this stands

**Phase 1 shipped.** Phases 2–5 as originally written are **unbuilt and de-prioritized** —
verified against the source (no `--variants`, no `pdf_tool/app.py`, no canvas drag-and-drop, no
multi-page collage book).

**Why the re-prioritization.** The original plan spent its two largest phases (4 and 5) on a
**canvas editor** and **collage books**. But look at what this repo is actually used for:

| | Built | Used |
|---|---|---|
| **Résumé / application pipeline** | vault, 4 profiles, guards, `/make-resume` | **16 PDFs · 2 applications · both applicants** |
| **Collage** | 457 lines — the largest module | **1 collage** |

The roadmap was investing in the feature with the least traction. `collage.py` is *done and it
works* — the honest question is not "how do we build it a GUI," it's "does anyone want one?"

**So: the résumé pipeline is the product.** Everything below is ordered by what makes *that*
better, and the collage app work is parked (not deleted — parked) until there's real demand.

---

## ✅ Phase 1 — local previewer (2026-07-11)

- [x] `src/pdf_tool/preview.py` — the Design Hub (sidebar thumbnails, main preview, palette
      swapper, export panel)
- [x] `css_vars` injection in `html_to_pdf.py` — palette-swapped exports are WYSIWYG
- [x] Verified against a real résumé + collage candidates

## ✅ Guards (2026-07-13, unplanned — earned their way in)

- [x] **`check_palette` wired INTO `html_to_pdf`** — the export now *blocks* on a banned color.
      It was previously an optional command the docs told you to run, and a brown accent shipped
      anyway. A rule enforced only when someone remembers it is not enforced.
- [x] **`check_vault`** — validates claim schema. On its **first run** it found 5 claims tagged
      with a role track that didn't exist: they were *silently invisible*, and a résumé would
      have quietly shipped without them.
- [x] **`doNotClaim` → a verification ledger.** A flat blocklist couldn't distinguish *"we asked
      and they don't have it"* from *"nobody ever checked"* — so two industry-standard tools were
      forbidden for months while both applicants had years of experience with each. Every entry
      now carries a `status`; only `confirmed-absent` may ever be treated as a gap.

---

## Next — the résumé pipeline

### 🔜 A. Wire `check_vault` into the workflow *(small, high value)*
- [ ] Run it automatically at the top of `/make-resume` — a vault error should stop the build,
      not surface three steps later as a mysteriously thin résumé.
- [ ] Add an `--explain <track>` mode: print exactly which claims would be selected for a track,
      in rank order. **This is the missing debugging tool** — right now the only way to know what
      a résumé will contain is to generate it.

### 🔜 B. `--variants` *(the original Phase 2 — still the right next feature)*
- [ ] Render N palette variants of one document into `_variants/`, so the hub shows true
      side-by-side alternatives without hand-copying files.
- [ ] Résumé color shopping becomes: generate → open hub → pick → export.

### 🔜 C. Close the ATS loop *(new — the highest-leverage idea here)*
- [ ] `pdf_tool.check_ats <resume.pdf>` — extract the text layer the way a parser does, and
      **show it back**. A two-column layout once parsed into interleaved gibberish and we only
      caught it by chance. **The machine that reads the résumé is the one that decides**, and we
      currently never look at what it sees.
- [ ] Flag the known killers: multi-column bullets in an experience block, text inside an image,
      reading order ≠ DOM order.

### 🔜 D. Vault ergonomics
- [ ] `check_vault --coverage <listing.md>` — given a listing, report which requirements have
      vault backing and which don't, so the **gap-check** step becomes mechanical instead of
      remembered. This is the step we've gotten wrong the most.

---

## Parked — the app shell (original Phases 3–5)

Not cancelled. Just not the bottleneck.

<details>
<summary><b>Phase 3 — windowed app (pywebview)</b> — the analysis still holds; do it when the hub is worth wrapping</summary>

- [ ] `pdf_tool.app` — a pywebview window around the preview server
- [ ] Native file dialogs for "export to…" / "open directory"
- [ ] Electron/Tauri only if distributing to non-Python users

pywebview remains the right call (the engine is Python; ~1 MB vs. Electron's ~150 MB; the hub is
already a localhost web app, so the shell is trivial). **But a native window is polish** — the
browser works fine today, and no one has been blocked by its absence.
</details>

<details>
<summary><b>Phases 4–5 — canvas editor & collage books</b> — blocked on demand, not on effort</summary>

- [ ] Canvas-size preset picker · drag-and-drop image tray · layout families as a starting
      arrangement · reads/writes `collage-source.json` (the CLI and GUI share one data file)
- [ ] Multi-page project file → `merge_pdfs` → one PDF book

**Do not start these until a real collage need shows up.** One collage has been made. The CLI
already produces six layout families and a picker gallery. Building a drag-and-drop editor for a
feature used once a year is how a tool gets heavy without getting better.
</details>

---

## Also worth doing (cheap, unglamorous)

- [ ] **`storage/themes/`** is referenced by `preview.py:70`, `PREVIEWER.md`, and this file — and
      **has never existed.** Either create it (with a README) or drop the references.
- [ ] Reconcile the **canvas-preset tables**: README lists 5, `COLLAGE-DESIGN.md` lists 8,
      `PREVIEWER.md` cites a 4:3 row the README doesn't have. Three docs, three answers.
- [ ] `docs/THEME-DESIGN.md` recommends a **React** UI; `PREVIEWER.md` and this plan chose
      **pywebview**. Kill the React section.
- [ ] **Decide the license.** `LICENSE` + README say MIT; `LICENSING-NOTES.md` says "not
      finalized." The repo is private, so the choice is still live — but make it *on purpose*.
      See [`../../docs/LICENSING-NOTES.md`](../../docs/LICENSING-NOTES.md).
- [ ] There is **no test suite.** Not a crisis at 1,400 lines, but `check_palette.classify()` and
      the vault-ranking order are exactly the kind of pure functions that deserve a dozen asserts.
