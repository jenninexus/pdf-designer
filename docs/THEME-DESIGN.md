# Theme Design

pdf-designer separates public, reusable design defaults from private brand
profiles.

## Theme sources

The `www-theme-kit/profiles/pdf-designer.json` profile owns the shared breakpoint contract. `syna-theme-kit/adapters/pdf-designer.json` supplies the generated Aesyna visual adapter; the vendored CSS lets a public clone run without either kit. Document palettes and private brand maps remain separate.

## Hub responsive contract

The shared breakpoint **numbers** live in
[`www-theme-kit/scss/_breakpoint-tokens.scss`](../../www-theme-kit/scss/_breakpoint-tokens.scss).
The Design Hub's actual behavior lives in
[`src/pdf_tool/static/hub.css`](../src/pdf_tool/static/hub.css): CSS media queries cannot consume
runtime variables. Cross-project caches and
`.config/mcp-pdf-designer*.json` are pointers for tools; neither owns the numbers or can override
the Hub implementation.

| Width | Hub behavior |
|---|---|
| `>= 992px` | Full toolbar and side-by-side library/viewer |
| `768–991.98px` | Tighter desktop split; full toolbar remains |
| `<= 767.98px` | Drawer switch: desktop groups are removed, hamburger/search appear, library/viewer stay split |
| `<= 575.98px` | Phone layout: library stacks above viewer |
| `< 390px` | Horizontal-overflow safety floor |

The drawer and search overlay must both close when the user clicks their visible outside surface;
Escape remains an optional keyboard shortcut. Drawer refresh and close affordances stay compact
icon controls. Any responsive change must be checked against the shared width matrix (390, 576,
768, 992, 1200, 1400, 1920) and the related `www-theme-kit/profiles/pdf-designer.json` profile.

## Public Defaults

Tracked default theme files:

- `themes/default-resume.json` - token data and export contract.
- `themes/default-resume.css` - CSS custom-property mirror.
- `themes/presets/*.json` - **6 public audition palettes** (slate-ink, ocean-breeze, synagentic, void-circuit, cinematic-studio, midnight-chrome). Loaded by Design Hub.
- `examples/profiles/default-resume/profile.json` - default resume profile.
- `examples/profiles/default-resume/default-resume.html` - reference render.

Private brand maps belong in ignored `brands/`; profile and person files point to those maps. The Hub scans public themes and private maps independently.

The public default is intentionally brand-neutral. It supports:

- dark browser preview
- light ATS-safe PDF export
- optional dark branded PDF export through `--pdf-theme dark`
- US Letter output, 8.5 x 11 inches
- user-facing generated files beside their document family (`resumes/<user>/`, `collages/<project>/`,
  `_exports/` fallback) and `output/` automation/test scratch
- cover-letter + resume bundles through `merge_pdfs.py --require-letter`

**Page layout (SSOT):** [`docs/LAYOUT-SYSTEM.md`](LAYOUT-SYSTEM.md) + `themes/default-resume.json#document`.
Two rules define the professional frame:

1. **Equal margins on all four edges.** Default `@page { size: Letter; margin: 0.65in }` — top = right =
   bottom = left, so content is framed identically. `themes/default-resume.css` derives every edge from
   one knob (`--resume-page-margin`); a doc may open it wider (0.75in for a formal letter) but must stay
   equal. Never asymmetric.
2. **Header flows, footer pins.** `.page` is a flex column; the header flows at the top inside the equal
   margin; the body region (`.page-main` / `.letter-main`) grows with `flex: 1`; the footer/signature
   (`.page-sig` bottom-right for résumés, `.letter-sign` bottom-left for letters, `.page-foot` for work
   samples) pins to the bottom with `margin-top: auto`. Print CSS gives `.page` a fixed content-box
   height `calc(11in − 2 × margin)` so the flex pin lands on the page bottom. Reusable classes live in
   `themes/default-resume.css`; see also `document.layout_prefs` / `document.layout_system`.

## Private Profiles

Private, real profiles belong outside tracked public examples. The recommended
local location inside this repo is:

```text
users/
  you.json
vaults/
  you.json                    ← the vault
profiles/
  you-resume.json
brands/
  brand-yours.json            ← private brand token maps (gitignored)
```

Root nouns are ignored by git. Use them for local brand profiles, private source
paths, real output paths, and project-specific palette mappings. `storage/` remains
a dual-run alias until retirement.

Map any approved external palette into a private `brands/brand-*.json` using the token contract below. Public starters use fictional or neutral values.

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

The **Design Hub** already exists as a local web app ([`PREVIEWER.md`](PREVIEWER.md)). The
Windows pre-release package uses a thin **Electron** host over that existing Hub;
[`WINDOWS-ELECTRON.md`](WINDOWS-ELECTRON.md) records its local-only security and
installer boundary. pywebview is parked. Neither is a renderer or a React rewrite.

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
gitignored file under `profiles/`.

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

**Trap (2026-07-21):** never let `@media (prefers-color-scheme: light)` restyle
`:root:not([data-theme="dark"])` outside a `screen` qualifier. That selector is
specificity `(0,2,0)` and **beats** `html[data-pdf-theme="dark"]` `(0,1,1)`, so on
a light OS preference the dark PDF stays light paper. Use
`@media screen and (prefers-color-scheme: light)` (see `themes/default-resume.css`
and the public example resume).

## Export Flow

See `docs/EXPORTS.md` for exact commands.

Typical sequence:

```powershell
python -m pdf_tool.html_to_pdf resume.html _exports/unfiled/resume.pdf
python -m pdf_tool.html_to_pdf resume.html _exports/unfiled/resume-dark.pdf --pdf-theme dark
python -m pdf_tool.merge_pdfs _exports/unfiled/application.pdf _exports/unfiled/cover-letter.pdf _exports/unfiled/resume.pdf --require-letter
python -m pdf_tool.pdf_to_png resume.html
```
