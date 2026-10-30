# The application workflow

One folder per job — how to go after a job without ever inventing a claim.

The workflow for going after a job without ever inventing a claim.

> Your real applications live in `_job-apps/` (gitignored). The copyable templates live
> in [`../examples/_job-listings/example-application/`](../examples/_job-listings/example-application/).
> Human log (who × job × outcome): `_job-apps/applied-index.md`. Do **not** daily-count submissions.
> Do **not** store listings in `applications/` or `storage/_job-listings/` — those names are
> retired aliases the engine still accepts.

---

## Two rules, both blocking

### 🔗 1. Capture the apply link BEFORE you build

**A perfectly tailored application you can't submit is worthless.**

If a listing arrives with no URL — **ask for it.** One question costs nothing; a dead
application costs the whole build. Status stays **`BLOCKED`** until an apply URL or an apply
email exists. This has already burned us twice.

> **Trap:** a company page showing *"no open jobs"* does **not** mean the posting is dead.
> Board postings frequently never appear on the employer's own page. **Only the direct job
> link is authoritative** — fetch it before concluding anything.

### 🛑 2. Ask about gaps BEFORE you build

For every listing requirement with **no vault backing** — **ask the applicant first.**

The vault records what they have *told* you. It is **not the limit of what they can do.** On a
real application, four requirements looked like gaps and *all four* turned out to be
long-standing strengths nobody had thought to ask about. Two industry-standard tools sat on a
"never claim" list for months while the applicants had years of experience with each.

**Only a *confirmed* absence is a gap.** Then — and only then — name the honest equivalent and
address it once, plainly, in the cover letter. That candor wins credibility.

---

## Folder anatomy

Folders are keyed by **role track**, *not* by date — so each new job in a track is a
copy-and-tweak of the last one rather than a rebuild.

```text
_job-apps/
  3D-Visualizer/            ← the TRACK, not a date
    Company.md              research · verified links · pay verdict · evidence map · the listing verbatim
    application.json        the machine record: apply URL · pay · status · who applied
    theme.json              the palette derived from THIS COMPANY's real brand CSS
    *.html                  the résumé + cover-letter SOURCES
    evidence/               screenshots of the live posting
  Backend/
  …
```

**⭐ No PDFs in here.** Private finished PDFs and PNGs go to **`resumes/<user>/<Track>/`**
per *person*, so everything one applicant needs to send sits in one place:

```text
resumes/alex/Example-Role/     one applicant's PDFs for that job
resumes/blair/Example-Role/     the other's, for the same job
```

**A company that posts many near-identical roles gets one folder, so the role folders don't pile up
flat** — and its role folder inside drops the company prefix:

```text
resumes/alex/ExampleCo/Research-Engineering/
resumes/alex/ExampleCo/Art-Related-Professional/
resumes/alex/ExampleCo/Technical-Game-Designer/
resumes/alex/Example-Company-Role/        ← single-application company stays flat
```

Group only at two-or-more applications per person, and note that **exports into a company group need an
explicit `--output-dir`** (the engine infers a flat path from the `_job-apps/<App>/` name) —
[`STORAGE.md`](STORAGE.md) § Company grouping.

Facts about the *job* (the apply link, the pay, the company palette) belong to the *job* — so
two people applying to the same posting share **one** record and it can never drift apart
between them.

## Templates in this folder

| Copy this | To | For |
|---|---|---|
| [`Company.example.md`](../examples/_job-listings/example-application/Company.example.md) | `<Track>/<Company>.md` | Research — links, checks, the requirement→evidence map, the verbatim listing |
| [`application.example.json`](../examples/_job-listings/example-application/application.example.json) | `<Track>/application.json` | The machine record — apply URL, pay verdict, status, applicants |
| [`theme.example.json`](../examples/_job-listings/example-application/theme.example.json) | `<Track>/theme.json` | The company-derived palette — with split accent runs when two people apply |

---

## Build it

```bash
/make-resume <user> _job-apps/<Track>
```

One command runs the routine end to end: capture the apply link → verify remote + pay →
**gap-check and ask** → research the company → derive a theme from their real brand CSS →
write → export light + dark for both documents → merge the bundle → log it.

📖 [`.claude/commands/make-resume.md`](../.claude/commands/make-resume.example.md) — and it is
**agent-agnostic**: plain markdown, no vendor APIs. Any assistant, or a human with a terminal,
can follow it.

## Fill the portal form

Most company portals (Workday, Greenhouse, Lever) **autofill the form from the first file you upload**.
That decides the upload order:

| Upload | File | Why |
|---|---|---|
| First (the parsed file) | the **light** résumé, optionally with work samples merged *after* it | The parser reads the résumé first and fills the experience from it. Light for upload; dark is for people. |
| Second file or Cover Letter field | the cover letter, on its own | A letter at the front of the parsed file pours letter prose into the autofill. |
| Email or recruiter | the letter-first bundle (letter, résumé, work samples) | A person reads it top to bottom. |

Build the bundles with `python -m pdf_tool.merge_pdfs <out.pdf> <first.pdf> <second.pdf> …` and run
`check_ats` on the uploaded file.

**Answer sheet.** Each application can carry `<Track>/form-answers.md`, built from `users/<id>.json` and the
vault. It covers the portal's steps in order (contact, experience, application questions) and marks
**OWNER** on anything the files do not prove: legal name, address, work authorization, sponsorship,
salary, start date, and every voluntary disclosure. A preferred name or a city is not a legal name or an address.

**What an agent may do with it.** In a browser, with the applicant watching and their OK in that session,
an agent can open the apply link, upload the files in the order above, fill each field the sheet answers,
and correct what autofill got wrong. It stops at every **OWNER** field.

**What only the applicant does:**
- Create the portal account and sign in. Agents never create accounts or type passwords.
- Answer the voluntary disclosures: gender, race, veteran and disability status.
- Read the review page and press **Submit**.

Then record the submission and freeze the sent files (below).

## Then log it — three places

1. `<Track>/application.json` — the machine record
2. `_job-apps/applied-index.md` — the human index, with the status and any ⚠ caveat
3. `<Track>/<Company>.md` — the status line + the materials index

*A finished application nobody can find in a month wasn't finished.*

## And freeze what you actually sent

The moment something is submitted, the **exact bytes that left** stop being a working export and become
a record. Move them into a dated `submitted-*` folder beside their document family:

```text
resumes/<user>/<Track>/submitted-<company>-<slug>-<YYYY-MM-DD>/
  <the exact sent file(s), unchanged>
  README.md      what was sent · to what posting · when · how · sha256 · the confirmation
```

- **`<slug>` is the role, not the folder name.** A referral link, an Indeed "easily apply" button or a
  recruiter can point at a *sibling* posting with different terms. Record the **posted role id and URL**
  in `application.json#submission.<user>.postedRole*` — the folder name is not the target.
- **`<user>` is one person.** A shared job record never makes two applicants' files one set.
- Move, don't copy: one unambiguous artifact, and the folder's own README carries the hash so the
  original export set is still provable.
- **Reusing an already-sent file verbatim? Point at the frozen original — do not duplicate it.** Record
  the hash and the path in the new application's `submission` block; a second identical copy is a
  second thing that can silently diverge. A rebuilt or edited document is different bytes and gets its
  own `submitted-*` folder.
- **Never edit a sent file.** New facts or fonts mean a new version, and the sent one stays as-is.
- Keep the confirmation beside the listing (`_job-apps/<Track>/evidence/`) and cite it (sender, subject,
  timestamp, Message-ID) — **an export is not proof of submission**, an acknowledgement is.
- A portal's *"your application is incomplete"* email is **submission proof plus a to-do**, not a
  rejection. Record the outstanding step in `application.json#submission.nextAction`.

Sent files live under `resumes/`, so they stay **local** — never commit them
([`PUBLIC-LOCAL-SPLIT.md`](PUBLIC-LOCAL-SPLIT.md) · [`STORAGE.md`](STORAGE.md)).

## Principles

- **Source-backed only** — a tailored résumé never claims anything not in the vault.
- **Employer-specific framing lives in the cover letter**, never in the résumé body.
- **No auto-submission, ever.** The tool prepares; the human submits.
