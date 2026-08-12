# Resume Studio — clone-safe walkthrough

Resume Studio is the public front door for the free résumé creator. This walkthrough uses only
tracked example data and public themes: no `storage/`, personal command, machine path, or SaaS
account is required.

> **Design Hub example card:** start the Hub, then
> [open the default résumé directly](http://127.0.0.1:8787/?doc=examples%2Fprofiles%2Fdefault-resume%2Fdefault-resume.html).
> The link selects its existing library card and opens the exact HTML that the exporter prints.

## One complete public path

Run commands from the repository root.

### 1. Install the engine

```bash
pip install -e ".[dev]"
playwright install chromium
```

### 2. Read and validate the claim vault

The [example vault](../profiles/default-resume/resume-source.example.json) is the source-backed
inventory of claims, skills, employment, credits, and education. A résumé is a selection from this
inventory; the example warnings are teaching prompts, while invalid structure still fails.

```bash
python -m pdf_tool.check_vault examples/profiles/default-resume/resume-source.example.json
```

### 3. Read the profile

The [profile shape](../profiles/default-resume/profile.example.json) describes how one person's
verified claims should render, including layout and `exportPrefs`. The
[live example profile](../profiles/default-resume/profile.json) points to the tracked HTML fixture
and requires both light and dark résumé exports. In this public walkthrough these files are
reference contracts; no private person record is created.

### 4. Choose a public palette

The [default palette](../../themes/default-resume.json) defines the document tokens. You can audition
the tracked [preset palettes](../../themes/presets/) in the Design Hub without editing the source.
The reference HTML embeds the default token values so it remains a standalone, deterministic fixture.

```bash
python -m pdf_tool.preview --no-open --port 8787
```

Open the [direct example card](http://127.0.0.1:8787/?doc=examples%2Fprofiles%2Fdefault-resume%2Fdefault-resume.html),
then use the palette control to compare light and dark presentation.

### 5. Inspect the printable HTML

[`default-resume.html`](../profiles/default-resume/default-resume.html) is the browser source and the
export source. It contains ATS-visible `Job Title`, `Work Experience`, `Education`, and `Skills` cues,
plus matching light and dark print rules. The example vault and profile document how real verified
content would be selected; they do not silently generate or invent prose.

### 6. Run the ship gate, then export both modes

```bash
python -m pdf_tool.check_generation examples/profiles/default-resume/default-resume.html

python -m pdf_tool.html_to_pdf examples/profiles/default-resume/default-resume.html --output-dir examples/resume-studio/_exports
python -m pdf_tool.html_to_pdf examples/profiles/default-resume/default-resume.html --pdf-theme dark --output-dir examples/resume-studio/_exports
```

The first command creates `default-resume-light.pdf`; the second creates
`default-resume-dark.pdf`. Generated files stay under the gitignored `_exports/` directory.

### 7. Prove the board PDF is ATS-readable

```bash
python -m pdf_tool.check_ats examples/resume-studio/_exports/default-resume-light.pdf
```

A pass reports contiguous job-title, work-experience, and education cues with no unacceptable
mid-word splitting. Upload the **light** PDF to job boards; keep the dark PDF for human readers,
email, or a portfolio.

For the same end-to-end proof in one command, run:

```bash
python scripts/smoke-white-label.py
```

## What each layer owns

| Layer | Tracked example | Owns |
|---|---|---|
| Vault | [`resume-source.example.json`](../profiles/default-resume/resume-source.example.json) | What may be truthfully claimed |
| Profile | [`profile.example.json`](../profiles/default-resume/profile.example.json) | How selected claims render and export |
| Palette | [`default-resume.json`](../../themes/default-resume.json) | Color tokens; never page geometry |
| HTML | [`default-resume.html`](../profiles/default-resume/default-resume.html) | Browser and PDF source |
| QA | `check_generation` + `check_ats` | Artifact and ATS gates |

When you later add real information, copy the example shapes into gitignored `storage/`; never replace
these tracked fixtures with personal details. See [Getting started](../../docs/GETTING-STARTED.md),
[vault rules](../../docs/VAULT.md), and the [public/private split](../../docs/PUBLIC-LOCAL-SPLIT.md).
