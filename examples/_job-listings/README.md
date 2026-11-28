# Application templates

The copyable starting point for a new job application.

| Copy this | To | For |
|---|---|---|
| [`Company.example.md`](example-application/Company.example.md) | `_job-apps/<company>/<opening>/<company>.md` | Listing and research |
| [`application.example.json`](example-application/application.example.json) | `_job-apps/<company>/<opening>/application.json` | Apply URL, status, and applicants for one opening |
| [`theme.example.json`](example-application/theme.example.json) | `_job-apps/<company>/<opening>/theme.json` | The company-derived palette |
| [`tracker.example.json`](tracker.example.json) | optional flat file | Shape only — prefer scanning `application.json` via `python -m pdf_tool.tracker list` |

Do **not** also copy into `storage/_job-listings/` or `applications/` — those names
are retired aliases. The live noun is `_job-apps/`.

The CLI discovers per-opening records recursively and also reads older flat folders.
Keep one `application.json` per opening. Use an applicant folder within an opening
when people need separate working files. Record confirmed submissions in your
private `_job-apps/applied-index.md`.

The workflow itself — and the two blocking rules — live in
[`../../docs/APPLICATIONS.md`](../../docs/APPLICATIONS.md). Read that first.
