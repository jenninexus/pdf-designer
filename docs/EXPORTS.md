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
