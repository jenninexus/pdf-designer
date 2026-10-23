# Editable presentation starter

This public sample is the built-in **pitch** story starter rendered as a standalone HTML document. Edit the visible text in `default-deck.html`, or generate another starter:

```bash
python -m pdf_tool.deck --list-starters
python -m pdf_tool.deck --starter proposal --output proposal.html
python -m pdf_tool.html_to_pdf proposal.html
```

Available starters: `pitch`, `proposal`, `kickoff`, `status`, `case-study`, and `training`. Each deck uses an editable, semantic HTML source with fixed layouts for title, statement, two-column, process, timeline, metrics, team, quote, and closing slides. Copy `content.example.json` and use `--input content.json` to supply your own title, subtitle, and slide content. Each slide has a `kind` and `title`; other supported fields depend on its kind and are illustrated by the six built-in flows in `src/pdf_tool/deck.py`. Unknown kinds and extra fields are rejected.

Replace all bracketed prompts with your own verified material. Metric cards intentionally begin with prompts and do not imply business results. Add source, period, and definitions when supplying measures. The renderer escapes all supplied text and does not accept CSS, HTML, or scripts as content.

The generated HTML is designed for widescreen PDF export through the existing Chromium renderer. This tool does **not** generate or edit PPTX, chart data, or presentation software files.
