<div align="center">

# pdf-designer

![MIT](https://img.shields.io/badge/license-MIT-9b5cf6?style=flat-square&labelColor=1a1a2e)
![Runtime](https://img.shields.io/badge/runtime-python%20%2B%20playwright-63b3ed?style=flat-square&labelColor=1a1a2e)
![Dependencies](https://img.shields.io/badge/dependencies-headless%20chromium-42f4c8?style=flat-square&labelColor=1a1a2e)
![Mode](https://img.shields.io/badge/mode-local--first-ffaa00?style=flat-square&labelColor=1a1a2e)

## Fill forms. Export PDFs.
## Never invent a claim.

A local-first toolkit for filling PDF forms and generating polished HTML → PDF documents (resumes, cover letters, application forms) — with an optional job-application layer that tailors output from your own verified facts instead of inventing anything.

</div>

Not a SaaS. Your data stays on your machine. See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for the full design, [`docs/THEME-DESIGN.md`](docs/THEME-DESIGN.md) for the theme/profile contract, and [`docs/EXPORTS.md`](docs/EXPORTS.md) for light/dark PDF, bundle, and PNG export commands.

- Real headless-browser PDF export — CSS grid/flex and `@media print` render exactly like a browser's own Print → Save as PDF.
- Profiles separate theme, data, and rendered HTML so one theme can back many documents.
- Source-backed only — generated content never outruns your own verified claims.
- No auto-submission, ever.

---

## What's here today

- **`src/pdf_tool/html_to_pdf.py`** — render any HTML file to PDF with a real headless browser (Playwright + Chromium), so CSS grid/flex layout and `@media print` rules render exactly like a browser's own Print → Save as PDF.
- **`src/pdf_tool/merge_pdfs.py`** — combine cover letters, resumes, and supporting PDFs into one upload bundle, with optional US Letter validation.
- **`src/pdf_tool/pdf_to_png.py`** — render exported PDFs to one PNG per page for previews, review artifacts, or web images.
- **`themes/default-resume.css`** (+ `default-resume.json` as the same tokens in data form) — a generic professional theme with intentional dark preview/brand-export mode, light ATS/submission mode, and US Letter print geometry.
- **`examples/profiles/default-resume/`** — a full example profile, mirroring the pattern below: `profile.json` (metadata + which theme/render/data it uses), `default-resume.html` (the reference render), `resume-source.example.json` (the claim-vault schema, one entry per verified fact).
- **`examples/job-listing-capture.example.md`** — a template for capturing a job listing before tailoring anything toward it.
- **`examples/applications/`** — the one-folder-per-job-application workflow: where to drop the listing link, screenshots, and gig details, and how to track what was actually submitted. Copy `example-application/` per gig.
- **`examples/profiles/default-collage/`** + [`docs/COLLAGE-DESIGN.md`](docs/COLLAGE-DESIGN.md) — the multi-image collage layout profile (PowerPoint-Designer-style layout candidates from a directory of images). Scaffold + design SSOT today; `src/pdf_tool/collage.py` generator planned.
- **`AGENTS.md`** — the machine/agent-facing capability map of this repo, for any AI coding assistant (not tied to one vendor).

### Profiles

Each use case (a resume, a specific cover-letter style, a different document type) is a **profile**: a folder under `examples/profiles/<id>/` containing `profile.json`, a reference `.html` render, and its own example data file — same shape as `themes/` + `profiles/` in dashboard-style projects, so a theme can be reused across multiple profiles without duplicating the palette. Copy `examples/profiles/default-resume/` as the starting point for a new profile.

## What's planned

AcroForm PDF field filling, flat-PDF overlay filling, job-listing keyword extraction, a match-score report (strong / partial / missing, with evidence links), resume tailoring from verified claims only, browser-form autofill mapping, the collage layout generator (`pdf_tool/collage.py`, see [`docs/COLLAGE-DESIGN.md`](docs/COLLAGE-DESIGN.md)), and an optional React preview/customizer layer that can apply saved theme profiles through the token adapter contract. See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for the full roadmap.

## Default canvas sizes

Print documents default to **US Letter (8.5 × 11 in)**. Collage/image layouts additionally target the standard social canvases (preset data: [`themes/default-collage.json`](themes/default-collage.json), design notes: [`docs/COLLAGE-DESIGN.md`](docs/COLLAGE-DESIGN.md)):

| Ratio | Pixels | Use |
|---|---|---|
| 8.5 × 11 in (portrait/landscape) | 2550 × 3300 @300dpi | Print / PDF one-sheet |
| 16:9 | 1920 × 1080 or 1280 × 720 | YouTube, slides, banners |
| 9:16 | 1080 × 1920 or 720 × 1280 | Stories, Reels, Shorts |
| 4:3 / 3:4 | 1440 × 1080 / 1080 × 1440 | Classic photo layouts |
| 4:5 | 1080 × 1350 | Instagram portrait post |
| 1:1 | 1024 × 1024 (or 1000², 512²) | Instagram square, avatars |

## Quick start

```
pip install playwright
playwright install chromium

python -m pdf_tool.html_to_pdf path/to/your-document.html
python -m pdf_tool.html_to_pdf path/to/your-document.html --pdf-theme dark
python -m pdf_tool.html_to_pdf path/to/your-document.html --output-dir path/to/_exports
python -m pdf_tool.merge_pdfs final-application.pdf cover-letter.pdf resume.pdf --require-letter
python -m pdf_tool.pdf_to_png path/to/your-document.pdf
```

Re-running against the same HTML never overwrites a previous export by default — it writes `your-document-v2.pdf`, `-v3.pdf`, and so on, so you always keep the last version you actually sent somewhere. Default exports go into `_exports` next to the source HTML. Pass an explicit output path, `--output-dir`, or `--force` to control the export location/overwrite behavior.

By default, `html_to_pdf.py` renders **US Letter, 8.5 x 11 inches**. For resume templates, make that explicit in the HTML too:

```css
@media print {
  @page {
    size: Letter;
    margin: 0.5in 0.55in 0.72in;
  }
}
```

Use `@page` margins for real printed page padding. If you need a repeated footer, add a `position: fixed` footer inside `@media print`; Chromium repeats fixed print elements on each generated page.

When a job portal only accepts one upload, create a cover-letter-plus-resume bundle after exporting each source document:

```text
python -m pdf_tool.merge_pdfs final-application.pdf cover-letter.pdf resume.pdf --require-letter
```

`--require-letter` fails the merge if any page is not 8.5 x 11 inches, which keeps mixed page sizes out of application uploads.

For a branded dark PDF while keeping the same Letter pagination, add dark print overrides in the template:

```css
@media print {
  html[data-pdf-theme="dark"] {
    --bg: #0b0d12;
    --surface: #10131a;
    --text: rgba(240,242,246,0.94);
  }
}
```

Then export with `--pdf-theme dark`.

The default theme intentionally defines both modes:

- Light print/submission: white surfaces, dark text, restrained teal/gold/violet accents for ATS-safe PDFs.
- Dark preview/branded export: near-black surfaces, light text, the same teal/gold/violet accent roles for portfolio PDFs/PNGs.

### Theme and palette sync

`themes/default-resume.json` is the data SSOT and `themes/default-resume.css` is the CSS mirror. To use another palette system, map its tokens into the same names used here (`primary`, `secondary`, `accent`, `support`, `bg`, `surface`, `text`, `dim`, `border`) and keep the document geometry unchanged unless the target explicitly asks for another paper size. This lets external theme kits swap the look without changing resume layout, page breaks, or ATS-safe print behavior.

## Using this for your own resume/applications

1. Copy `examples/profiles/default-resume/` to `examples/profiles/<your-id>/` (or anywhere outside the repo) and fill in `resume-source.example.json` → your own real, verifiable claims.
2. Copy `examples/job-listing-capture.example.md` per job listing you're targeting.
3. Adapt `default-resume.html` (or build your own) against `themes/default-resume.css`, keeping any target-employer-specific language in a separate cover letter, not the resume body.
4. Render to PDF with `html_to_pdf.py`.

Keep your real, filled-in files out of version control unless you deliberately want them public — see `.gitignore` (it already ignores non-`.example.` resume-source/job-listing files).

## Principles

- Source-backed only — no invented claims.
- Honest gaps stay honest — an unverified skill is marked unverified, not upgraded.
- One generation voice per document, decided explicitly, not left ambiguous.
- Employer-specific framing lives in the cover letter, never baked into the reusable resume.
- No auto-submission, ever — this speeds up your own review, it doesn't replace it.

## License

`LICENSE` is currently MIT as a **placeholder, not a final decision** — if a paid tier is genuinely planned, read [`docs/LICENSING-NOTES.md`](docs/LICENSING-NOTES.md) before the first public push.

---

<div align="center">

If this helps you build something useful:

[Star this repo](https://github.com/jenninexus/pdf-designer) · [Links](https://jenninexus.com/links) · [Patreon](https://www.patreon.com/c/JenniNexus) · [Paypal](https://paypal.me/jenninexus)

Published by [Jenni](https://github.com/jenninexus) at [Monofinity Studio](https://github.com/monofinitystudio).

</div>
