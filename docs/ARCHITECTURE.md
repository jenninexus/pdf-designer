# Architecture

pdf-designer is two things sharing one codebase:

1. **`pdf_tool`** — a general PDF/HTML document engine: fill AcroForm PDFs, overlay-fill flat PDFs, and render styled HTML (resumes, letters, forms) to PDF via a real headless browser.
2. **`application_assistant`** — an optional layer on top, for people using this to manage job applications: a resume/company source vault, job-listing capture, match scoring, and resume tailoring — all built so generated output only ever draws from your own verified claims.

You can use `pdf_tool` alone (just the PDF engine) without ever touching `application_assistant`.

For the concrete light/dark/bundle/PNG command flow, see [`EXPORTS.md`](EXPORTS.md). For the public theme/profile contract and private-profile pattern, see [`THEME-DESIGN.md`](THEME-DESIGN.md).

## Planned Layout

```text
pdf-designer/
  README.md
  LICENSE
  docs/
    ARCHITECTURE.md          (this file)
  src/
    pdf_tool/
      __init__.py
      html_to_pdf.py         (done — Playwright-based HTML → PDF export)
      merge_pdfs.py          (done — bundle PDFs with optional Letter validation)
      pdf_to_png.py          (done — render PDF pages to PNG previews)
      preview.py             (done — Design Hub: local preview server w/ palette swapper + export; see PREVIEWER.md)
      collage.py             (done — multi-image layout candidates + picker gallery from an image directory; see COLLAGE-DESIGN.md)
      inspect_pdf.py         (planned — detect AcroForm fields vs. flat/scanned PDFs)
      fill_pdf.py            (planned — AcroForm field fill)
      overlay.py             (planned — ReportLab overlay merge for flat PDFs)
      mapping.py             (planned — reusable field-map schema for both PDF paths)
      profile.py             (planned — applicant profile: contact/education/work history)
    application_assistant/
      job_listing.py         (planned — parse a job-listing-capture file)
      resume_sources.py      (planned — load/query a resume-source vault)
      match_score.py         (planned — score a listing against the vault: strong/partial/missing)
      tailor_resume.py       (planned — generate a tailored resume draft from verified claims only)
      autofill_profile.py    (planned — browser-form field mapping)
      submission_log.py      (planned — track what was submitted where, with which resume version)
  examples/
    job-listing-capture.example.md
    applications/            (one-folder-per-job-application workflow + copyable template)
      README.md
      example-application/
    profiles/
      default-resume/
        profile.json         (metadata: which theme/render/data this profile uses)
        default-resume.html  (reference render)
        resume-source.example.json
      default-collage/       (multi-image collage layouts — see COLLAGE-DESIGN.md)
        profile.json
        default-collage.html
        collage-source.example.json
  themes/
    default-resume.json      (tokens as data; dark/light + Letter export contract)
    default-resume.css       (same tokens as a CSS custom-property block)
    default-collage.json     (collage canvas presets + tokens)
  templates/
    pdf/                     (AcroForm/overlay templates go here)
    browser/                 (ATS field-map templates go here)
  tests/
```

## Profiles

Each use case (a resume, a different letter style, a different document type entirely) is a **profile**: a folder under `examples/profiles/<id>/` with `profile.json` (metadata: which theme it uses, which file is the reference render, which file is its example data), a reference `.html` render, and its own example data file. This mirrors the `themes/` + `profiles/{id}/` split used by dashboard-style projects internally — one theme can back multiple profiles without duplicating the palette. Copy `examples/profiles/default-resume/` as the starting point for a new one.

### Multiple people, one vault: `applies_to`

If more than one person can generate output from the same resume-source vault — a team where each member sometimes applies solo and sometimes as a combined team resume — every claim in the vault carries an `applies_to` array naming which profile id(s) may use it. `profile.json`'s `includeFilter` (`{ "applies_to": "<profile-id>" }`) is how a given profile's tailoring pass selects only the claims meant for it.

This matters because "true" and "belongs in this output" are different questions. A founder's personal alma mater, an engine only one team member personally authored, or any other founder-specific fact is real and source-backed, but it isn't the other team member's history — it should never appear when *they* apply solo, even though it's a perfectly true claim about the team. `examples/profiles/default-resume/resume-source.example.json`'s `education-example-scoped-out` entry is a worked example of exactly this: real, true, and deliberately excluded from a hypothetical co-founder's solo profile.

Rule of thumb: when adding a new claim, ask "does this belong to the team, or to one specific person?" Team facts (shipped products, studio history, shared tech stack) get every relevant profile id. Person-specific facts (education, a personally-authored side project, a personal specialty) get only that person's profile id(s) — never assume a fact should propagate to every profile just because it's true.

## Themes And Export Modes

`themes/default-resume.css` and `themes/default-resume.json` are the public default theme SSOT. They are intentionally self-contained and brand-neutral. The same template should support:

- **Screen / preview mode**: dark by default, suitable for browser review and portfolio-style presentation.
- **Light PDF mode**: default `@media print` output for ATS-safe submission PDFs.
- **Dark PDF mode**: opt-in branded output through `html_to_pdf.py --pdf-theme dark`, using `html[data-pdf-theme="dark"]` print overrides while keeping the same paper geometry.
- **Bundle PDF mode**: combine multiple exported PDFs with `merge_pdfs.py --require-letter` when a portal accepts one upload file.
- **PNG mode**: render any generated PDF to one image per page with `pdf_to_png.py`.

Default output should stay organized: `html_to_pdf.py` writes to `_exports` next to the source HTML when no explicit output path is supplied, `--output-dir` can redirect that default, and `pdf_to_png.py` writes preview images under `_exports/<pdf-name>-png` unless a directory is provided.

Resume templates must keep physical paper geometry explicit:

```css
@media print {
  @page {
    size: Letter;
    margin: 0.5in 0.55in 0.78in;
  }
}
```

Letter means **8.5 x 11 inches**. Legal is 8.5 x 14 inches and should not be used for normal resumes unless explicitly required.

Resume profiles should also show page boundaries in browser preview. Use explicit screen-visible page wrappers such as:

```css
.page {
  width: 8.5in;
  height: 11in;
  box-sizing: border-box;
  position: relative;
}

@media print {
  .page {
    width: auto;
    height: auto;
    break-after: page;
  }

  .page:last-child {
    break-after: auto;
  }
}
```

This keeps the browser review close to the final PDF/PNG and prevents featured sections from being split accidentally.

Fixed print footers are supported, but templates must reserve bottom space through `@page` margins and, when needed, deliberate page breaks. This prevents footer/content collisions in Chromium-generated PDFs.

## Theme Token Sync

`themes/default-resume.json` is the data SSOT; `themes/default-resume.css` is the CSS mirror. Other palette systems can drive a profile by mapping their own token names into the pdf-designer contract:

- `primary`, `secondary`, `accent`, `support`
- `bg`, `surface`, `elevated`, `text`, `dim`, `dim2`
- `border`, `border2`
- document tokens such as `paper`, `width_in`, `height_in`, and print margins

Palette swaps should not change paper size, page-break strategy, or ATS-safe print behavior unless the profile explicitly opts into that. This keeps design-sync/palette tools focused on visual identity while pdf-designer owns output geometry.

If a React preview/customizer layer is added later, it should import or normalize external saved theme profiles into this same token contract, then apply them as CSS custom properties for screen preview only. Animation, glass, and theme transitions belong to the screen preview layer; PDF/PNG exports remain static and deterministic. See [`THEME-DESIGN.md`](THEME-DESIGN.md).

## Design Principles

- **Source-backed only.** Every generated resume bullet or filled form value should trace back to an entry in your resume-source vault, a public profile link, or a manually approved addition — never an invented claim.
- **Honest gaps stay honest.** A vault entry can be `"confidence": "explicitly-unverified"` — the tailoring layer should surface that as a gap, not silently upgrade it to a claim.
- **One voice, no accidental over-sharing.** If you use this for a company/team resume, decide up front whether generated output speaks as one person or names contributors, and encode that as a policy claim in the vault (see the `generation-policy-example` entry in `examples/resume-source.example.json`) so tooling enforces it instead of relying on manual review every time. For multi-person vaults, pair this with `applies_to` scoping (see "Multiple people, one vault" above) so a person-specific fact never leaks into a teammate's solo profile.
- **Employer-specific framing lives in the cover letter, not the resume.** Keep the resume itself reusable across applications; put target-listing language in a separate generated cover letter.
- **Review before anything goes out.** No auto-submission. Match scores and tailored drafts are there to speed up your own review, not replace it.
- **Local-first.** Your resume-source vault and job-listing captures can contain identifying/private information — keep them out of version control (see `.gitignore`) unless you deliberately want them public.

## PDF Export Decision

`html_to_pdf.py` uses Playwright + headless Chromium rather than `reportlab`/`wkhtmltopdf`. Real documents lean on real CSS (grid/flex layout, `@media print`, web fonts) that only a browser engine renders faithfully — Playwright's `page.pdf()` reproduces exactly what "Print → Save as PDF" gives you in an actual browser.

Setup:

```
pip install playwright
playwright install chromium
```

Usage:

```
python -m pdf_tool.html_to_pdf path/to/document.html
python -m pdf_tool.html_to_pdf path/to/document.html --pdf-theme dark
python -m pdf_tool.html_to_pdf path/to/document.html --output-dir path/to/_exports
python -m pdf_tool.merge_pdfs final-application.pdf cover-letter.pdf resume.pdf --require-letter
python -m pdf_tool.pdf_to_png path/to/document.pdf
```

## Licensing

Not finalized — see [`LICENSING-NOTES.md`](LICENSING-NOTES.md) before the first public push, especially if a paid tier is actually planned.
