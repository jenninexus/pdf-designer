# Remaining — release gates + document layout / spacing

**Date:** 2026-08-25
**Status:** Complete — closed 2026-09-21
**Closed parents:**
[`../_Complete/2026-08-22-product-polish-and-release-readiness.md`](../_Complete/2026-08-22-product-polish-and-release-readiness.md) ·
[`../_Complete/2026-08-22-root-output-folder.md`](../_Complete/2026-08-22-root-output-folder.md) ·
[`../_Complete/2026-08-23-start-vault-import.md`](../_Complete/2026-08-23-start-vault-import.md)

Hub polish, LIVPHI **source** mirror, `/wizard` vault import, the public `output/` versus private
`_exports/` split, unsigned BundledRuntimeProof, and the 2026-09-21 Hub/docs consolidation are done.
Future product ideas and decision-gated release work now live in [`docs/ROADMAP.md`](../../docs/ROADMAP.md)
instead of keeping a finished dated plan artificially active.

Public GitHub must stay clone-safe. Signing-account, Store, Partner Center, and channel-specific notes
stay in `docs/CHANNELS.local.md` (gitignored), not `docs/PRODUCT.md`; the sibling product handoff is
`../product-design/Plans/_Active/2026-09-03-pdf-designer-first-signed-release.md`. JN `$5` checkout
stays off until fulfilment is wired.

---

## Where we are (cross-surface)

| Surface | State |
|---|---|
| **pdf-designer GitHub** | Public MIT clone. Suggested tip $3/$5 on README. No Setup.exe download. |
| **Design Hub** | http://127.0.0.1:8787/ — recipes at `/recipes`; ignored `_exports/` PDFs/images are visible as read-only local artifacts |
| **JN `/products`** | Local catalog already **free card + tip** (`jenninexus/public_html/includes/products.json`, 2026-08-25). Confirm live [jenninexus.com/products](https://jenninexus.com/products)#pdf-designer if not deployed this machine. Checkout stays off. |
| **product-design hub** | Local-only sibling. Card: `../product-design/docs/PDF-DESIGNER.md`. Money board: `../product-design/product-registry.md`. Command: `/products`. |
| **Jenni defaults** | HTML `resumes/jenni/defaults/` · private PDFs `_exports/jenni/resumes/` (work-examples ~1.18 MB, 2026-08-22). |
| **Shade defaults** | Same recipes. Work-examples **v2** ≈ 2.05 MB (`html_to_pdf --max-mb 5`). Pre-inline leftovers ~11.8 MB still sit beside them. |

---

## Done when

- [x] Jenni + Shade résumé / cover / work-examples match [`docs/LAYOUT-SYSTEM.md`](../../docs/LAYOUT-SYSTEM.md) rhythm. `check_generation` PASS 2026-08-25. Jane résumé + cover PASS. Jane Hub mosaic is collage-family (`0.6in` / `9.8in`) — `footer-collision` still FAILs (colored tiles vs résumé signature scan); not the 3-page pack.
- [x] Shade work-examples PDFs ≤ 5 MB — `_exports/shade/resumes/shade-default-work-examples-{light,dark}-v2.pdf` ≈ **2.05 MB** (`html_to_pdf --max-mb 5`). Older `*-light.pdf` / `*-dark.pdf` (~11.8 MB) are pre-inline leftovers.
- [x] Release boundary decided: Authenticode plus clean Win10/11 x64 VM proof remains mandatory before
  any future binary listing; the binary channel is held and the unsigned listing stays off.

---

## 1. Document layout / spacing (landed 2026-08-25)

Recipes (shared by Jenni and Shade — not per-person files):

| Doc | Recipe | Theme geometry |
|---|---|---|
| Résumé | `layouts/resume/two-page-standard.json` | `themes/default-resume.css` `--resume-page-margin` |
| Cover letter | `layouts/cover-letter/one-page-letter.json` | 0.75in equal; **no** print `height` + `overflow: hidden` |
| Work examples | `layouts/work-examples/work-examples.json` | 0.6in; 3 pages; links in body `.links-panel` |

**Observed drift (2026-08-25):** Jenni default HTML **inlines** CSS instead of importing the theme. The résumé is packed tighter than LAYOUT-SYSTEM (header ~10px vs ~20; `section` ~12px vs 16–19; `li` ~1px vs ~4). Cover letter is already closest to spec. Work-examples `.page-main` gap is ~22px vs recipe ~18px; `section:last-of-type { margin-top: auto }` fights the footer-pin rule.

**Recommended pass (do not shrink margins to “fit”):**

1. **Résumé** — restore section/list air to the recipe. If page 2 overflows, cut a bullet or move a block — never `--resume-page-margin`. Keep page-1 and page-2 gaps even. Studio Capabilities stays demoted, not crammed at 10.5px as a second résumé.
2. **Cover letter** — keep CZI geometry (`min-height`, 13px paras, 30px above sign-off). Eyeball the bottom 15% of the PDF. Fit-to-one-page order is already in LAYOUT-SYSTEM.
3. **Work examples** — set `.page-main` gap to ~18px; drop `margin-top: auto` on the last section. Keep full-width grids (`repeat(N, 1fr)`). Caption below hero. Then `check_generation` + raster.
4. **Jane Example** — same rhythm so the public clone matches what we print.
5. **Verify** — `python -m pdf_tool.check_generation` then `pdf_to_png`. Optional later: `/human-sim-qa` on Syqo’s **designated QA machine** (never SEGOPC pointer). Write `human-sim-qa-pdf-designer.md` before that run.

**Landed 2026-08-25 (layout HTML pass):** Jenni defaults + Shade go-to restored to equal margins and recipe air. Shade cover is CZI flex (`.letter-main` / `.signoff`); work-examples re-inlined JPEG ≤960 via `resumes/shade/defaults/_inline_work_examples.py`. Footer email tracking dropped to ~`0.03em` so `footer-collision` does not treat the mailto as body. `html_to_pdf` has no `--user` — that flag is `check_generation` only.

## 2. Decision-gated release work — routed, not shipped

From the closed 2026-08-22 polish plan. Detail: `docs/CHANNELS.local.md` + `docs/WINDOWS-ELECTRON.local.md`.

- [x] Signing remains explicitly held. If the private channel decision reopens it, use `dist:signed`
  and require Valid Authenticode. Detail stays in `docs/CHANNELS.local.md`; the durable public trigger
  stays in [`docs/ROADMAP.md`](../../docs/ROADMAP.md).
- [x] Clean-VM proof remains a future release gate, not unfinished work in this plan. Use a clean VM
  (or `-BundledRuntimeProof -RequireAuthenticode` after Valid), never a daily-driver PC as listing proof.
- [x] Do not enable live checkout, Gumroad overlay, or Microsoft Store on `/products`.
- [x] Shade work-examples ≤ 5 MB.

## 3. 2026-09-21 Design Hub / privacy consolidation

- [x] Align the PDF Designer nav switch at `xxl`/1400 across Hub CSS, the authoritative
  `www-theme-kit` profile, the byte-mirrored offcanvas SCSS, and the Syna cross-kit pointer profile.
- [x] Keep full-bleed drawer behavior phone-only (≤575.98 or short landscape ≤480px high); use the
  almost-full resizable end-panel from 576–1399.98; restore inline toolbar at 1400.
- [x] Expanded profile/folder/palette/format menus participate in the drawer's single scroll flow and
  cannot overlap adjacent controls.
- [x] Browse ignored `_exports/**/*.{pdf,png,jpg,jpeg,webp}` from the virtual `_exports` folder as
  read-only local artifacts; never re-export an artifact or track its payload.
- [x] Consolidate `Plans/_Active/` to this one file; move the completed PlayGo session to `_Complete/`.
- [x] Add one authoritative public-app versus personal-workspace diagram and path lookup; point the
  README/docs hubs to it instead of maintaining competing diagrams.
- [x] Add per-card comparison inclusion controls: uncheck unwanted cards, **Focus N**, edit, or reset.
- [x] Replace the browser-native light PDF surface with a dark Hub-owned real-page preview; retain an
  **Open original** action and match the library's cyan scrollbar.
- [x] Review and integrate the existing mixed Design Hub/docs working batch after its whitespace findings
  are normalized; do not combine private applicant payload with the public commit.
  - Integrated on local `main` as `cdb5173` + wrap follow-ups after full tests, wheel proof,
    white-label smoke, privacy scan, and live Hub verification. Remote synchronization is an operational
    credential blocker in the recovery ledger, not unfinished product work in this dated plan.

## 4. Product evolution carryover — transferred to the roadmap

These remain worthwhile ideas, but none was accepted as part of this dated delivery. The live backlog is
now [`docs/ROADMAP.md`](../../docs/ROADMAP.md); this completed plan records the transfer only.

- [x] **Canvas editor transferred:** drag/drop image tray, canvas-size presets, layout-family starting points, hero
  selection, and text blocks; read/write the same `collage-source.json` the CLI uses.
- [x] **Collage books transferred:** multi-page project manifest → render each page → `merge_pdfs` into one book.
- [x] **Native output-folder picker transferred:** preserve editable path text plus Browse;
  do not add a browser-only fake absolute-path control.
- [x] **Production PyPI decision transferred:** only after TestPyPI proof and explicit channel decision; GitHub clone
  remains the complete free product meanwhile.

---

## Assumptions

- `_Active/` may be empty between concrete product slices. Closed files in `_Complete/` are history;
  `docs/ROADMAP.md` owns the durable backlog.
- `/jen/www` wrap is for the **website** if `/products` still needs a live deploy; this plan does not own jennidrop rsync.
- `/jenni` is identity/web ops, not the applicant vault (`/pdf` + `/jenni` applicant router).

## Evidence

- VERIFIED — 2026-09-21 live Hub pass against a real three-page `_exports/shade/…` PDF: comparison
  deselect → Focus → Edit all works; `/pdf-viewer` contains its toolbar and three rendered page images;
  the dark canvas, white page boundary, and cyan left/right scrollbars are visibly distinct.
- VERIFIED — 2026-09-21 `pytest -q` = 118 passed; `scripts/check-wheel-assets.py` includes the viewer
  assets and excludes generated PDF/image payload; `scripts/smoke-white-label.py` passes light/dark/ATS.
- VERIFIED — 2026-09-03 Hub stills recaptured (`docs/images/hub-{library,home,recipes,vault,start}.png` from a git-tracked clone; `hub-resume-jennifer-nexus.png` from the local screenshot pack). Nav shows Wizard; wizard shows Patreon/PayPal. Script: `scripts/capture-hub-stills.py`.
- VERIFIED — wizard import tests exist; `output/` engine default landed (`190963f` / later).
- VERIFIED — JN local `products.json` sku `pdf-designer` is `status: free` + tip CTA (2026-08-25).
- UNVERIFIED — live droplet `/products` if deploy has not run since that catalog edit.
- VERIFIED — Jenni + Shade résumé / cover / 3-page work-examples `check_generation` PASS (2026-08-25). Jane résumé + cover PASS. Jane Hub mosaic still FAIL `footer-collision` (collage tiles vs signature scan).
- VERIFIED — Shade work-examples `*-v2.pdf` ≈ 2.05 MB. `html_to_pdf` now refuses positional paths that start with `-` (pytest `test_paths`).

## 2026-09-21 wrap closeout

| Phase | Outcome | Artifact |
|---|---|---|
| 1 — map the two journeys | Public clone/setup and personal Jenni/Shade workspaces share one engine but have explicit source and output paths | `docs/WORKSPACE-LAYOUT.md` |
| 2 — focus and preview | Library comparison inclusion + Focus/Edit/Reset and the dark real-page PDF viewer passed live verification | `cdb5173` |
| 3 — consolidate docs | Every tracked public doc has a unique ownership row; compatibility stubs are labeled; tracked Markdown links resolve | `docs/README.md` |
| 4 — close the plan | Future ideas moved to `docs/ROADMAP.md`; this finished dated checklist moved to `_Complete` | this file |
| 5 — preserve the trap | Empty styled PDF shells are not acceptance evidence; verify toolbar + rendered pages inside `/pdf-viewer` | `.memory/lesson-pdf-viewer-needs-first-class-route.md` |

`added_memory: [lesson-pdf-viewer-needs-first-class-route]`

**Difficulties / disposition:** the dated plan had accumulated decision-gated and someday ideas, which
made a completed delivery look unfinished. The bounded fix was to make `docs/ROADMAP.md` the durable
backlog and allow `_Active/` to be empty between concrete slices. Remote synchronization is still blocked
by the available HTTPS credential; local `main` is preserved and the exact next action remains in the
git-recovery ledger.
