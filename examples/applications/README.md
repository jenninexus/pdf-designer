# applications/ — One Folder Per Job Application

Every job listing you tailor a resume for gets **its own folder**, so there is
always one obvious place to drop everything about that gig: the listing link,
screenshots, notes, the tailored resume/cover letter, and the final exports.

## Where real applications live

Real applications are private. Keep them in the gitignored local workspace:

```text
storage/applications/<yyyy-mm-dd>-<company>-<role>/
```

Example: `storage/applications/2026-07-10-disney-systems-designer/`

The date prefix keeps folders sorted by when you started the application, and
the company + role slug makes each one findable at a glance.

## Folder contents (copy `example-application/`)

```text
<yyyy-mm-dd>-<company>-<role>/
  application.md                 the hub page: link, status, notes, checklist
  job-listing-capture.md         filled copy of ../job-listing-capture.example.md
  screenshots/                   listing screenshots, portal pages, anything visual
  resume.html                    tailored copy of your base resume render
  cover-letter.html              employer-specific framing lives HERE, not in the resume
  _exports/                      generated PDFs/PNGs (gitignored everywhere)
```

Only `application.md` is mandatory — add the rest as the application progresses.

## Workflow

1. **Capture** — create the folder, copy
   [`example-application/application.md`](example-application/application.md)
   into it, paste the job URL, drop in screenshots.
2. **Analyze** — fill `job-listing-capture.md` (keywords, requirements, match
   notes) from the listing.
3. **Tailor** — copy your base resume render (e.g. from
   `storage/<your-id>/`), adjust emphasis using ONLY claims from your
   resume-source vault. Employer-specific language goes in the cover letter.
4. **Export** — light PDF for submission, dark PDF for reference, bundle if
   the portal takes one file. See [`../../docs/EXPORTS.md`](../../docs/EXPORTS.md).
5. **Log** — record in `application.md` what you submitted, where, and when,
   with the exact export filename. Future you will thank you.

## Principles (inherited from the repo root)

- Source-backed only — a tailored resume never claims anything not in the vault.
- Employer-specific framing lives in the cover letter, never the resume body.
- No auto-submission, ever.
