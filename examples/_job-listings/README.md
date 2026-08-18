# Application templates

The copyable starting point for a new job application.

| Copy this | To | For |
|---|---|---|
| [`Company.example.md`](example-application/Company.example.md) | `_job-apps/<Track>/<Company>.md` | Research — links, checks, the requirement→evidence map, the verbatim listing |
| [`application.example.json`](example-application/application.example.json) | `_job-apps/<Track>/application.json` | The machine record — apply URL, pay verdict, status, applicants |
| [`theme.example.json`](example-application/theme.example.json) | `_job-apps/<Track>/theme.json` | The company-derived palette |
| [`tracker.example.json`](tracker.example.json) | optional flat file | Shape only — prefer scanning `application.json` via `python -m pdf_tool.tracker list` |

Do **not** also copy into `storage/_job-listings/` or `applications/` — those names
are retired aliases. The live noun is `_job-apps/`.

The workflow itself — and the two blocking rules — live in
[`../../docs/APPLICATIONS.md`](../../docs/APPLICATIONS.md). Read that first.
