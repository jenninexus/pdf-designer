# PDF Designer examples

The public examples use fictional data and editable HTML. Open the Design Hub
to preview and export them. Use the [setup guide](../docs/GETTING-STARTED.md)
on a fresh clone.

## Resume Studio

[Open the example résumé in the Hub](http://127.0.0.1:8787/?doc=examples%2Fprofiles%2Fdefault-resume%2Fdefault-resume.html).
Try the palette picker to compare screen and print colors. The editable
[résumé HTML](profiles/default-resume/default-resume.html) prints in both modes.
The [sample vault](profiles/default-resume/resume-source.example.json)
illustrates the underlying claims and the [example profile](profiles/default-resume/profile.json)
identifies its render and export settings.

```bash
python -m pdf_tool.check_generation examples/profiles/default-resume/default-resume.html
python -m pdf_tool.html_to_pdf examples/profiles/default-resume/default-resume.html
python -m pdf_tool.html_to_pdf examples/profiles/default-resume/default-resume.html --pdf-theme dark
python -m pdf_tool.check_ats _exports/examples/default-resume-light.pdf
```

The generated files stay in `_exports/examples/` and appear in the Hub's
Exports view. For one end-to-end smoke test, run
`python scripts/smoke-white-label.py`.

### Make a local copy

Use the Hub Wizard or copy each starter in place, removing `.example` from
the filename. Enter your own identity in [users](../users/README.md), verified
claims in [vaults](../vaults/README.md), and document preferences in
[profiles](../profiles/README.md). See [storage and export paths](../docs/STORAGE.md).

| Copy | To |
|---|---|
| [Person starter](../users/you.example.json) | `users/you.json` |
| [Vault starter](../vaults/you.example.json) | `vaults/you.json` |
| [Résumé profile starter](../profiles/you-resume.example.json) | `profiles/you-resume.json` |
| [Brand palette shape](brand-design/brand-example.json) | `brands/brand-you.json` |
| [Job listing template](_job-listings/example-application/) | `_job-apps/My-Role/` |

## Document starters

| Starter | Preview or edit |
|---|---|
| Résumé | [Two-page résumé](profiles/default-resume/default-resume.html) |
| Cover letter | [One-page cover letter](profiles/default-cover-letter/default-cover-letter.html) |
| Work examples | [Work-samples page](profiles/default-work-examples/default-work-examples.html) |
| Personal letter | [Personal letter](profiles/default-letter/personal-letter.html) |
| Collage | [Collage canvas](profiles/default-collage/default-collage.html) |
| Collage gallery | [Candidate gallery](profiles/default-gallery/_candidates/index.html) |
| Presentation | [Widescreen pitch](profiles/default-deck/default-deck.html) |

## Presentation starter

Generate a pitch, proposal, kickoff, status update, case study, or training
deck. Edit the generated HTML, or copy the [deck content example](profiles/default-deck/content.example.json)
to supply your own title, subtitle, and slides with `--input content.json`.

```bash
python -m pdf_tool.deck --list-starters
python -m pdf_tool.deck --starter proposal --output proposal.html
python -m pdf_tool.check_deck proposal.html
python -m pdf_tool.html_to_pdf proposal.html
```

See [layout geometry](../docs/LAYOUT-SYSTEM.md) and
[document validation](../docs/QA.md) for export checks.
