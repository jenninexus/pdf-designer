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
| `--elevated-2` | a second raised level (nested card, table stripe) |
| `--text` | primary text |
| `--dim` | secondary text |
| `--dim2` | muted text |
| `--border` | subtle rule/border |
| `--border2` | stronger rule/border |
| `--primary` | main brand/accent |
| `--secondary` | secondary accent |
| `--accent` | contrast accent |
| `--support` | optional support/tech accent |

**13 tokens — this table is the contract.** It matches `preview.py`'s `_TOKEN_MAP` exactly; if
you add a token to one, add it to the other. *(`--elevated-2` and `--border2` were live in the
code but missing from this table — a contract doc that under-reports the contract is worse than
no contract doc.)*

### ⚠ The one color rule that outranks everything

**No brown. No mustard. No puke/lime green.** Amber has **no readable dark form on white paper**
— darken it for print and it turns brown. On the light palette, hand the amber role to another
hue.

This is **enforced on every export** (`html_to_pdf` refuses to render a violating document).
Full rule and rationale: [`../themes/PALETTE-RULES.md`](../themes/PALETTE-RULES.md).

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

## The UI boundary (whatever the UI turns out to be)

The **Design Hub** already exists as a local web app ([`PREVIEWER.md`](PREVIEWER.md)), and the
plan is to wrap it in **pywebview** — not React, not Electron. *(An earlier version of this doc
recommended a React module tree; that predates the pywebview decision and is gone.)*

What matters isn't the framework — it's the boundary, which holds for any UI:

| Layer | Owns |
|---|---|
| **UI** | Controls, live token editing, the preview shell |
| **`pdf_tool`** | Deterministic HTML → PDF, merging, PNG rendering. **The only renderer.** |
| **Profiles** | Which theme, which data, which document, which export paths |

**The rule that makes previews trustworthy:** a UI layer *never re-implements rendering.* It
shows the same HTML file the exporter prints, in the same browser engine — so what you preview
is byte-for-byte what exports. UI layers may come and go; the documents and the CLI keep
working without them.

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
