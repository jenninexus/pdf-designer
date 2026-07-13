# Export Workflow

pdf-designer exports HTML documents through a browser engine, then optionally
bundles PDFs and renders PNG previews.

## Default Folders

If no output path is supplied, exports go under `_exports` beside the source
document.

```text
profile/
  resume.html
  _exports/
    resume.pdf
    resume-v2.pdf
```

Use `--output-dir` or a full output path when a project needs a specific folder.

## Light PDF

Light mode is the default print/submission mode. Templates should implement it
inside `@media print`.

```powershell
python -m pdf_tool.html_to_pdf resume.html
python -m pdf_tool.html_to_pdf resume.html _exports/final/resume.pdf
python -m pdf_tool.html_to_pdf resume.html --output-dir _exports/final
```

## Dark PDF

Dark mode is opt-in and uses `html[data-pdf-theme="dark"]` inside print CSS.
It keeps the same paper size and page breaks.

```powershell
python -m pdf_tool.html_to_pdf resume.html _exports/final/resume-dark.pdf --pdf-theme dark
python -m pdf_tool.html_to_pdf cover-letter.html _exports/final/cover-letter-dark.pdf --pdf-theme dark
```

## Combined Upload PDF

Use this when a job portal accepts only one file. Put the cover letter first,
then the resume. Use `--require-letter` for application bundles.

```powershell
python -m pdf_tool.merge_pdfs _exports/final/application.pdf _exports/final/cover-letter.pdf _exports/final/resume.pdf --require-letter
python -m pdf_tool.merge_pdfs _exports/final/application-dark.pdf _exports/final/cover-letter-dark.pdf _exports/final/resume-dark.pdf --require-letter
```

## PNG Preview

Render the final PDF to one PNG per page for visual QA or portfolio previews.

```powershell
python -m pdf_tool.pdf_to_png _exports/final/application.pdf
python -m pdf_tool.pdf_to_png _exports/final/application-dark.pdf _exports/final/application-dark-preview
```

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

`pdf_tool.check_palette` rejects banned colors before you export.

```bash
python -m pdf_tool.check_palette resume.html
python -m pdf_tool.check_palette --scan .          # walk a whole tree
```

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

**Measure before trimming copy.** At `margin: 0.45in 0.5in 0.55in`, the printable
budget is **960px** per page. Check the real print-mode content height (not the
screen layout — screen `min-height`/padding will lie to you) before cutting text.

## Verify, always

Exporting is not finishing. Render the PDF to PNG and *look at it*, and assert the
page count:

```bash
python -m pdf_tool.pdf_to_png _exports/resume-light.pdf

python -c "import fitz; d=fitz.open('_exports/resume-light.pdf'); print(d.page_count,'pages', d[0].rect)"
```

A two-page resume that silently became three pages is the single most common
regression; the page-count assertion catches it in one line.

## Note: exports never overwrite

`html_to_pdf` writes `document-v2.pdf`, `-v3`, … rather than clobbering a previous
export. That means a second run for the dark theme lands as `-v2`, **not** as
`-dark`. Export into a clean directory and rename explicitly:

```bash
python -m pdf_tool.html_to_pdf doc.html --output-dir out && mv out/doc.pdf out/doc-light.pdf
python -m pdf_tool.html_to_pdf doc.html --output-dir out --pdf-theme dark && mv out/doc.pdf out/doc-dark.pdf
```
