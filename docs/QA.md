# QA — one gate for every generation

**Run this before shipping any resume, cover letter, or work-samples.** One command checks every house
rule at once, so a generation can't go out with a brown wash, a magenta Shade doc, an all-lowercase name,
a drifting margin, an unpinned signature, or a neon color painted over a photo.

```bash
python -m pdf_tool.check_generation <doc>.html            # auto-detects the user; runs all checks
python -m pdf_tool.check_generation <doc>.html --user shade   # force per-user rules (no-magenta)
python -m pdf_tool.check_generation --scan storage/shade/defaults   # sweep a folder of .html
python -m pdf_tool.check_generation <doc>.html --no-render     # skip render checks (fast source-only)
python -m pdf_tool.check_generation <doc>.html --json          # machine-readable
```

**Exit 0 = all pass · exit 1 = one or more FAIL · exit 2 = usage error.** CI-usable.

| | |
|---|---|
| [What it checks](#the-checks) | The 10 rules, and which SSOT owns each |
| [Per-user / per-doc rules](#per-user--per-doc-awareness) | Why Shade fails on magenta but Jenni doesn't |
| [Reading a report](#reading-a-report) | PASS/FAIL/skip and how to fix |
| [When to run](#when-to-run) | Wired into make-resume / make-work-examples |
| Related | [`../themes/GENERATION-RULES.md`](../themes/GENERATION-RULES.md) · [`../themes/PALETTE-RULES.md`](../themes/PALETTE-RULES.md) · [`LAYOUT-SYSTEM.md`](LAYOUT-SYSTEM.md) |

## ⭐ The governing principle — judge the ARTIFACT, not the source

> **A guard that inspects the source can only catch defects that exist in the source.**
> The reader sees a rendered PDF. Three defects shipped in 2026-07-21 precisely because every guard
> was reading CSS while the bug lived in the render:

| Guard | Measured | Missed |
|---|---|---|
| `check_palette` | source hex | brown **composited** at render time — a red-tinted dark grey averaging `2c2224`, and alpha layers producing `a08251` (no brown hex exists anywhere in the file) |
| `check_overflow` | DOM height at Playwright's **1280px** default viewport | real overflow at the **816px** paper width — measured 726px vs the true 940px, so a 9px overflow read as 205px of headroom and a footer overlap shipped |
| *(none existed)* | — | `@page` background drift between sibling docs — invisible on screen, visible as a mismatched PDF border |

**Rules that follow — apply these when writing ANY new check:**

1. **Render, then measure.** If a rule is about what the page *looks* like, the check must rasterize
   (Playwright screenshot or `pypdfium2` on the exported PDF) and inspect pixels.
2. **Measure at real paper width.** US Letter = **816 CSS px** (8.5in × 96dpi). In print media `.page`
   is `width: auto` and inherits the viewport, so a wide viewport silently under-reports height.
   `check_overflow._LETTER_PX` exists for this reason — never measure page fit at a default viewport.
3. **Exempt artwork.** Colors inside `<img>` regions belong to the photo, not the palette
   (`check_rendered_color` skips image boxes). A rule that fails on game art is a rule people disable.
4. **Discount antialiasing.** Subpixel text fringing produces off-hue pixels on every rendered page.
   Render at 2×, use greyscale AA, and require a neighbour cluster before counting a pixel.
5. **Control-test both directions.** A new guard must be shown to **FAIL the known-bad artifact** and
   **PASS the known-good one**. A check only ever verified against clean input proves nothing.
   Footer-collision's known-bad lives at
   [`tests/fixtures/known-bad-footer-overlap.html`](../tests/fixtures/known-bad-footer-overlap.html).

> **Never say "verified" after only checking the source.** Export (or let `check_generation` render),
> then trust the PASS — or open the PNG / PDF and look. The human eye on the artifact is still the
> final court of appeal.

## The checks

`check_generation` is the **one QA pass**. It composes the existing single-purpose guards and adds the
rules they didn't cover (**11 checks**):

| # | Check | Rule | SSOT |
|---|---|---|---|
| 1 | **palette** | no brown / mustard / lime; **+ no magenta/pink for Shade & Martian** | [PALETTE-RULES.md](../themes/PALETTE-RULES.md) |
| 2 | **rgba-magenta** | magenta/pink smuggled in as `rgba()`/`hsl()` — invisible to the hex-only palette guard | GENERATION-RULES |
| 3 | **casing** | names & company names **never all-lowercase** in display text (`jenni`, `shade`, `martian games`, `synagen`, …). Stylized wordmarks like the `jenninexus` logo are allowed | GENERATION-RULES §1 |
| 4 | **overlay** | no bright/neon/primary **fill washed over a banner/hero/photo** — only a black→transparent scrim | GENERATION-RULES §2 |
| 5 | **signature** | resume + work-samples: signature **bottom-pinned, bottom-right** (`margin-top:auto` + `align-self:flex-end`). Cover letter: a sign-off just needs to exist (natural flow) | LAYOUT-SYSTEM.md |
| 6 | **margins** | `@page` margins **equal on all four edges** (one value, or a symmetric v/h pair) — no drift | LAYOUT-SYSTEM.md §Equal margins |
| 7 | **page-bg** | `@page` background (PDF border colour) agrees inside the file **and** with same-applicant sibling docs in the folder | GENERATION-RULES |
| 8 | **rendered-color** | ⭐ no brown / large-area warm cast in **rendered pixels** (catches composited brown the hex guard cannot see) | GENERATION-RULES · `check_rendered_color` |
| 9 | **overflow** | no page overflows its print box at **816px** paper width. **Render-based**; `--no-render` skips | LAYOUT-SYSTEM.md §content-fit |
| 10 | **footer-collision** | ⭐ **PDF ground truth**: nothing overlaps the pinned signature band (catches 2-col text under the script that DOM height can miss). Detects signature alignment (résumé right / letter left) rather than assuming right | LAYOUT-SYSTEM.md |
| 11 | **letter-geometry** | ⭐ a **cover letter** must never declare a print `.page` `height` **together with** `overflow: hidden` — that combination CLIPS the sign-off at the box boundary while every DOM-based guard passes | [one-page-letter.json](../layouts/cover-letter/one-page-letter.json) · LAYOUT-SYSTEM.md |

Checks 1 / 8 / 9 / 11 shell out to the standalone `check_palette` / `check_rendered_color` /
`check_overflow` / `check_pagefit` so there is one implementation of each rule, not two.
Checks 8–10 need Playwright + pypdfium2; `--no-render` skips them (source-only — **not**
ship-ready). Check 11 is **source-only**, so it runs even with `--no-render`.

> ### ⚠ What check 11 exists for — and the limit of pixel checks
>
> On **2026-07-25** a cover letter shipped with *"Founder & CEO, Martian Games LLC"* sliced
> through the middle and the email line missing entirely, because it had copied the résumé's
> pinned-footer CSS. **Four checks passed:** `check_overflow` (DOM: content 7.29in inside a
> 9.6in box, `overflowBy: 0`), `check_generation` 10/10, page count 1, and the text layer —
> the clipped line still *exists* in it, so a grep succeeds where a human cannot read.
>
> **Pixel forensics cannot fix this.** Measured on a clipped export vs a clean one: identical
> bottom-ink row (y=1438 of 1584) and statistically identical final-line band heights (13px
> against a 16px median, in *both*). A rasteriser cannot tell "the line ended here" from "the
> line was cut here". So the defect is refused **at the source** instead — check 11 rejects
> the CSS pattern that causes it.
>
> **The human check that still matters:** rasterise and LOOK at the bottom of the page.
> `python -m pdf_tool.pdf_to_png <doc>.html --pdf-theme dark`

### Page-fit (separate, for exported PDFs)

```bash
python -m pdf_tool.check_pagefit <doc>.pdf                 # page count + edge ink + orphan tail
python -m pdf_tool.check_pagefit <doc>.pdf --expect 1
python -m pdf_tool.check_pagefit --source <doc>.html       # the letter-geometry rule alone
```

Asserts the exported page count (letter **1** · résumé **2** · work-samples **3**), that no ink
runs off the sheet, and that the last page is not an **orphan tail** (a signature stranded alone
on a final page — unprofessional even when nothing is clipped).

## Per-user / per-doc awareness

The tool detects **who** the doc is for (from the path or the signature/contact) and **what** it is
(resume / cover-letter / work-samples), then applies the right rule set:

- **Shade & Martian** → `no_magenta` is **on** (checks 1 + 2 ban pink). **Jenni** → off (her brand uses pink).
- **Cover letters** → the sign-off flows after the body (not bottom-pinned); check 5 only requires it exists.
- **Resumes / work-samples** → check 5 requires the bottom-right pin.

Override detection with `--user <name>` when the filename doesn't say.

## Reading a report

```
============================================================================
FAIL  storage/shade/…/foo.html   (user=shade, no-magenta=True)
  OK palette       …
  XX margins       equal/consistent @page margins
        - @page margin '0.42in 0.48in 0.48in' is asymmetric (drift) — use equal margins…
  ~ overflow      skipped
```

`OK` passed · `XX` failed (indented lines say exactly what + where) · `~` skipped (`--no-render`).
Fix the source and re-run. **Never override a FAIL** — fix it (a brown hex, a lowercase name, a margin,
an unpinned signature are all cheap to fix and each has bitten a real doc).

## When to run

- **make-resume** step 8 and **make-work-examples** step 4/5 call this as the final gate before an export
  is considered done — it replaces running `check_palette` + `check_overflow` separately.
- **Before any submission**, run it on the final `.html`.
- **After a bulk change** (palette swap, dir move), `--scan storage/<user>/defaults` sweeps the go-to set.
- **Go-to defaults:** after editing `storage/<user>/*-resume.html` (**any** applicant), re-export
  **light + dark** into `storage/<user>/defaults/`, run `check_generation` on the source HTML, and
  `python -m pdf_tool.check_ats <defaults/*-resume-light.pdf>` before treating the pack as board-ready.
> This tool found and fixed real margin drift in **both** favorite resumes (Shade `0.42/0.48/0.48`,
> Jenni `0.45/0.5/0.55`) the day it was written — exactly the "consistent margin/padding" class of bug
> it exists to catch. The 816px overflow correction later exposed a real jenni-resume footer overlap
> that the old viewport had hidden; that is now fixed at the source and guarded by check 10.
