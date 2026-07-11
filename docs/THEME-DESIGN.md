# Theme Design

pdf-designer separates public, reusable design defaults from private brand
profiles.

## Public Defaults

Tracked default theme files:

- `themes/default-resume.json` - token data and export contract.
- `themes/default-resume.css` - CSS custom-property mirror.
- `examples/profiles/default-resume/profile.json` - default resume profile.
- `examples/profiles/default-resume/default-resume.html` - reference render.

The public default is intentionally brand-neutral. It supports:

- dark browser preview
- light ATS-safe PDF export
- optional dark branded PDF export through `--pdf-theme dark`
- US Letter output, 8.5 x 11 inches
- `_exports` output folders
- cover-letter + resume bundles through `merge_pdfs.py --require-letter`

## Private Profiles

Private, real profiles belong outside tracked public examples. The recommended
local location inside this repo is:

```text
storage/
  profiles/
    your-profile.json
```

`storage/` is ignored by git. Use it for local brand profiles, private source
paths, real output paths, and project-specific palette mappings.

## Token Map Contract

External theme kits should map their own palette tokens into the pdf-designer
theme variable contract:

| pdf-designer token | Meaning |
|---|---|
| `--bg` | document/app background |
| `--surface` | page or primary surface |
| `--elevated` | raised card/section surface |
| `--text` | primary text |
| `--dim` | secondary text |
| `--dim2` | muted text |
| `--border` | subtle rule/border |
| `--primary` | main brand/accent |
| `--secondary` | secondary accent |
| `--accent` | contrast accent |
| `--support` | optional support/tech accent |

Geometry tokens are not brand tokens. Do not change paper size, page margins,
or page-break strategy during palette sync unless the destination explicitly
requires it.

## Theme-Kit Adapter Contract

Future UI layers can let users apply a saved theme profile from another design
system to a pdf-designer document preview. Treat that as an adapter problem:
read the external profile, map it into the token contract above, then render the
same document with those mapped variables.

A compatible saved theme/profile should be normalized into:

```json
{
  "mode": "dark",
  "palette": {
    "primary": "#4fd1c9",
    "secondary": "#e3b559",
    "accent": "#9d8cd9",
    "support": "#6aa7ff"
  },
  "surface": {
    "bg": "#0b0d12",
    "surface": "#10131a",
    "elevated": "#171b24",
    "text": "rgba(240,242,246,0.94)"
  },
  "effects": {
    "glass": { "blur": "12px", "opacity": 0.68 },
    "motion": "normal"
  }
}
```

The adapter may support richer source schemas, but pdf-designer should only
depend on the normalized shape. This keeps the renderer usable without any
specific theme-kit dependency.

## Animated HTML Previews

HTML previews can support richer presentation than PDFs:

- animated section reveals
- theme transitions
- glass/blur effects
- hover states
- portfolio-style landing or resume hub views

These effects belong to screen media only:

```css
@media screen {
  .resume-section {
    transition: transform 180ms ease, opacity 180ms ease;
  }
}

@media print {
  * {
    animation: none !important;
    transition: none !important;
  }
}
```

PDF and PNG exports must remain static, deterministic, and physically sized.
Do not let animation timing, viewport-height effects, sticky elements, or
scroll-triggered states control printed layout.

## React UI Roadmap

If pdf-designer gets a React preview/customizer later, keep the boundary clear:

- React owns controls, saved-profile import, live token editing, and preview
  animation.
- `pdf_tool` owns deterministic HTML to PDF, PDF merging, and PNG rendering.
- Profiles own which theme, source data, document HTML, and export paths are
  active.

Recommended React modules:

- `ThemeProvider` - writes normalized tokens to CSS custom properties.
- `ThemeProfileLoader` - imports saved theme/profile JSON and normalizes it.
- `PreviewShell` - renders animated screen preview with page wrappers.
- `ExportPanel` - calls light PDF, dark PDF, bundle PDF, and PNG commands.
- `ProfileInspector` - shows active profile, source vault, and export mode.

Use `prefers-reduced-motion` and a profile-level motion flag so animated resume
hub pages can be expressive without making the core document inaccessible.

## Default Resume Profile

The tracked `default-resume` profile is the public starting point. It defines
the shape of a single-voice resume:

- header
- profile
- core capabilities
- selected credits / flagship work
- about
- technology

Copy it for new public-safe examples. For private profiles, extend it from a
gitignored file under `storage/profiles/`.

## Dark and Light Modes

The same HTML should support both modes:

- **Light PDF:** default print output for ATS-safe submission.
- **Dark PDF:** branded/review output via `html_to_pdf.py --pdf-theme dark`.

Templates should implement this using print CSS:

```css
@media print {
  :root {
    /* light submission tokens */
  }

  html[data-pdf-theme="dark"] {
    /* dark branded tokens */
  }
}
```

## Export Flow

See `docs/EXPORTS.md` for exact commands.

Typical sequence:

```powershell
python -m pdf_tool.html_to_pdf resume.html _exports/final/resume.pdf
python -m pdf_tool.html_to_pdf resume.html _exports/final/resume-dark.pdf --pdf-theme dark
python -m pdf_tool.merge_pdfs _exports/final/application.pdf _exports/final/cover-letter.pdf _exports/final/resume.pdf --require-letter
python -m pdf_tool.pdf_to_png _exports/final/application.pdf
```
