# Export Workflow

pdf-designer exports HTML documents through a browser engine, then optionally
bundles PDFs and renders PNG previews. Root [`README.md`](../README.md) stays
short — **this file is the command + export SSOT.** One-line module map:
[`SSOT.md`](SSOT.md)#engine-cli-map.

## Commands

```bash
pip install -e . && playwright install chromium

python -m pdf_tool                                              # hub — list commands
python -m pdf_tool.html_to_pdf <doc>.html                       # → <stem>-light.pdf
python -m pdf_tool.html_to_pdf <doc>.html --pdf-theme dark      # → <stem>-dark.pdf
python -m pdf_tool.html_to_pdf <doc>.html --output-dir <dir>
python -m pdf_tool.html_to_pdf <doc>.html --variants            # light PDF per public palette
python -m pdf_tool.variants <doc>.html                          # same as --variants
python -m pdf_tool.merge_pdfs out.pdf a.pdf b.pdf --require-letter
python -m pdf_tool.pdf_to_png <doc>.html                        # one PNG per .page (visual QA)
python -m pdf_tool.check_palette <doc>.html                     # palette guard (also auto on export)
python -m pdf_tool.check_palette --scan <dir>
python -m pdf_tool.check_vault --all
python -m pdf_tool.check_vault --explain <user> <track>
python -m pdf_tool.check_vault --coverage <user> <track> <listing.md>
python -m pdf_tool.check_ats <resume-light.pdf>
python -m pdf_tool.audit_resume <user> <track> <resume.html>
python -m pdf_tool.tracker list
python -m pdf_tool.tracker status
python -m pdf_tool.collage <imagesDir> --layout auto --png
python -m pdf_tool.preview --no-open --port 8787                # Design Hub
```

After `pip install -e .` you also get console scripts: `pdf-designer`,
`pdf-designer-preview`, `pdf-designer-check-palette`, `pdf-designer-check-vault`,
`pdf-designer-check-ats`, `pdf-designer-tracker`, `pdf-designer-variants`.

## Default Folders

If no output path is supplied, exports go under `_exports` beside the source
document. Dual-mode default names are **`<stem>-light.pdf`** / **`<stem>-dark.pdf`**.
Re-exports never overwrite — they bump to `-v2`, `-v3`, …

```text
profile/
  resume.html
  _exports/
    resume-light.pdf
    resume-dark.pdf
    resume-light-v2.pdf
```

Use `--output-dir` or a full output path when a project needs a specific folder.

## Light PDF

Light mode is the default print/submission mode. Templates should implement it
inside `@media print`.

```powershell
python -m pdf_tool.html_to_pdf resume.html
python -m pdf_tool.html_to_pdf resume.html _exports/final/resume-light.pdf
python -m pdf_tool.html_to_pdf resume.html --output-dir _exports/final
```

## Dark PDF

Dark mode is opt-in and uses `html[data-pdf-theme="dark"]` inside print CSS.
It keeps the same paper size and page breaks.

```powershell
python -m pdf_tool.html_to_pdf resume.html --pdf-theme dark
python -m pdf_tool.html_to_pdf resume.html _exports/final/resume-dark.pdf --pdf-theme dark
python -m pdf_tool.html_to_pdf cover-letter.html --output-dir _exports/final --pdf-theme dark
```

## Combined Upload PDF

Use this when a job portal accepts only one file. Put the cover letter first,
then the resume. Use `--require-letter` for application bundles.

```powershell
python -m pdf_tool.merge_pdfs _exports/final/application.pdf _exports/final/cover-letter.pdf _exports/final/resume.pdf --require-letter
python -m pdf_tool.merge_pdfs _exports/final/application-dark.pdf _exports/final/cover-letter-dark.pdf _exports/final/resume-dark.pdf --require-letter
```

## PNG Preview

One PNG per page, for visual QA — **this is how an agent sees its own output.**

It renders the **HTML source**, not the PDF: it screenshots each `.page` element in the same
headless Chromium, in the same print media mode, that `html_to_pdf` prints from. Same DOM, same
engine, so the image is exact.

```powershell
python -m pdf_tool.pdf_to_png resume.html
python -m pdf_tool.pdf_to_png resume.html _exports/preview --pdf-theme dark --scale 2
```

> **Why HTML and not the PDF?** It used to rasterize the exported PDF with **PyMuPDF — which is
> AGPL-3.0.** An MIT project cannot carry a mandatory AGPL dependency without the license claim
> becoming incoherent, so it's gone. Screenshotting the `.page` elements needs no second
> rasterizer, adds no dependency, and is exact rather than approximate. See
> [`LICENSING-NOTES.md`](LICENSING-NOTES.md).

## Required Resume Geometry

For normal resumes and cover letters, keep US Letter output:

```css
@media print {
  @page {
    size: Letter;
    margin: 0.5in 0.55in 0.78in;
  }
}
```

Letter is 8.5 x 11 inches. Do not switch to Legal unless the receiving system
explicitly asks for 8.5 x 14 inches.

## Palette Guard — no brown, no mustard, no lime

**The guard runs automatically on every export.** `html_to_pdf` refuses to render a document
that uses a banned color — you don't have to remember it, and you can't forget it.

```bash
python -m pdf_tool.html_to_pdf resume.html        # guard runs; BLOCKS on a violation
python -m pdf_tool.html_to_pdf resume.html --skip-palette-check   # override (say why)
```

Run it standalone to check without exporting:

```bash
python -m pdf_tool.check_palette resume.html
python -m pdf_tool.check_palette --scan .          # walk a whole tree
```

> It used to be *only* the standalone command, with docs telling you to run it first — and a
> brown light-mode accent shipped into a shared palette anyway. "Remember to run the guard" is
> not a guarantee, it's a hope. Now it's a gate.

**House rule:** no brown, no mustard, no puke/lime green. Yellow and orange are
allowed only as **bright, clean** tones; any other green is fine.

**Why this exists (the amber trap):** amber and gold have **no readable dark form
on white paper.** Darkening `#FCB72F` for a light/print palette produces `#9A6A05`
or `#8A6D0B` — objectively brown (≈30% lightness at a 40–46° hue). This is a
color-space fact, not a mistake anyone makes on purpose, so it recurs unless
something checks for it.

**The fix:** keep the bright amber in **dark** mode, where it works. In the
**light** palette, give the amber role to a *different* hue from the same palette
(a blue, teal, or magenta). Don't try to darken amber — it can't be saved.

The checker exits non-zero and prints the offending hex, its classification, the
file, and the line.

## Pagination — two traps that cost real time

**1. The phantom blank page.** A trailing `break-after: page` on the last page
container emits an extra empty sheet. Break *before* subsequent pages instead:

```css
/* WRONG — trailing break emits a blank sheet */
.page { break-after: page; }
.page:last-child { break-after: auto; }

/* RIGHT */
.page + .page { break-before: page; }
```

**2. The orphaned section.** A `break-inside: avoid` section that doesn't fit in
the space left on page 1 gets pushed onto a sheet of its own — and shoves page 2's
content to page 3. If a section keeps orphaning, **move it to the next page** in
the markup rather than fighting the CSS.

**3. The unbreakable column.** `break-inside: avoid` on a *column wrapper* (`.cols > div`) makes the
entire multi-entry column one atomic block. It then can't fit in what's left of the page and gets
orphaned onto a sheet of its own — silently turning a 2-page résumé into 3. Put `break-inside: avoid`
on the **entries**, never on the column that holds them.

**⚠ Measure the PDF, not the browser.** `getBoundingClientRect()` in print-emulation mode does NOT
predict the real pagination — it reports the screen box. The only truth is the exported PDF:

```bash
python -c "from pypdf import PdfReader; print(len(PdfReader('out.pdf').pages), 'pages')"
```

**Measure before trimming copy.** At the locked geometry — `@page { size: Letter;
margin: 0.5in 0.55in 0.78in; }` — the printable budget is:

| | |
|---|---|
| **Height** | 11in − 0.5 − 0.78 = **9.72in = 933px** per page |
| **Width** | 8.5in − (0.55 × 2) = **7.4in = 710px** |

Check the real *print-mode* content height before cutting text — the screen layout will lie to
you (screen `min-height` and padding don't apply in print).

> ⚠ This doc used to quote **960px**, derived from a margin set (`0.45in 0.5in 0.55in`) the repo
> does not use. That's 27px of budget that doesn't exist — enough to silently push a two-page
> résumé onto a third sheet. The margins above are the contract; they're also in
> [`ARCHITECTURE.md`](ARCHITECTURE.md) and [`../AGENTS.md`](../AGENTS.md).

## Verify, always

Exporting is not finishing. Render the PDF to PNG and *look at it*, and assert the
page count:

```bash
python -m pdf_tool.pdf_to_png _exports/resume-light.pdf

python -c "from pypdf import PdfReader; r=PdfReader('_exports/resume-light.pdf'); b=r.pages[0].mediabox; print(len(r.pages),'pages', f'{float(b.width)/72:.2f}x{float(b.height)/72:.2f}in')"
```

A two-page resume that silently became three pages is the single most common
regression; the page-count assertion catches it in one line.

## Note: exports never overwrite

Default dual-mode names already separate light and dark (`<stem>-light.pdf` /
`<stem>-dark.pdf`). Re-running the **same** theme bumps `-v2`, `-v3`, … instead of
clobbering. Pass an explicit output path if you want a fixed filename.
