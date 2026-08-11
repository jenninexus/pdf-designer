---
description: Build a tailored, source-backed résumé for a job application. Researches company, verifies REMOTE + PAY, derives theme, exports per profiles/<user>-resume.json#exports.exportPrefs (default = résumé only; cover letter / work samples are separate opt-in commands). Use for "/make-resume", pasted job URL with no folder yet.
argument-hint: <user> <application-dir|job-url> [dark|light|full]
---

# /make-resume — Tailored Application Builder

Repo-local command for **`C:\Github\pdf-designer`**. Real data lives under `storage/` (gitignored).

## Usage

```
/make-resume jenni  storage/_job-listings/3D-Visualizer
/make-resume shade  storage/_job-listings/3D-Visualizer
/make-resume both   storage/_job-listings/3D-Visualizer    # matched-pair themes
/make-resume studio storage/_job-listings/<App>            # studio voice — capabilities
/make-resume martian storage/_job-listings/<App>           # studio voice — games
/make-resume jenni  storage/_job-listings/3D-Visualizer dark      # DARK PDF ONLY (skip light/ATS file)
/make-resume jenni  storage/_job-listings/3D-Visualizer <profile.json> <theme.css>
```

Only `<user>` and `<application-dir>` are required. `both` = build for Jenni AND Shade off one
company palette with **split accent runs** (same grid + type; a matched pair, not duplicates).

### 🗣 Argument parsing — accept how a human actually types it

**Do not require rigid positional arguments.** These all mean the same thing:

```
/make-resume for <user>       /make-resume <user>       make a resume for <user>
```

**Parse, don't reject.** From `$ARGUMENTS`, extract in this order:

1. **Applicant** — scan for a known user id **anywhere** in the string, case-insensitive, ignoring
   filler words (`for`, `please`, `a`, `the`, `resume`, `make`, `to`). Accept declared aliases too.
2. **Application dir** — any path token, or a fuzzy match against an existing `storage/_job-listings/<App>/`.
3. **Job URL** — any `http(s)://` token → the "pasted job URL with no folder yet" flow.
4. **Mode** — a bare `dark` · `light` · `full`.

**Missing applicant → ask one short question.** Never guess between two people. **Missing application
dir but applicant known → list the open (non-`SUBMITTED`) applications and ask**, rather than stopping.

> **This is the public seed** (`make-resume.example.md`, tracked). Copy to `make-resume.md`
> (gitignored) for personal specifics. The assistant runs the bare file when it exists.
>
> **Résumé only by default.** Cover letter and work samples are **separate opt-in commands**
> (personal copies: `make-cover-letter.md` / `make-work-examples.md`). Never auto-ship a letter
> unless the human asks or `exportPrefs` says so.

### Who is applying?

| `<user>` | Profile | Voice |
|---|---|---|
| `<you>` | `profiles/<you>-resume.json` | first person |
| `both` | matched pair | one company palette, split accent runs |
| studio voices | optional studio / brand profiles | capabilities vs games |

### ⭐ Step −1 — READ `exportPrefs` (UNIVERSAL board contract)

Open **`storage/profiles/<user>-resume.json#exports.exportPrefs`** before exporting.

**Every profile** (jenni · shade · studio · martian) ships **light + dark** résumé PDFs by default
(`resumeDefault: light-and-dark`, `includeLightAts: true`). That is the shared board contract —
inherited from `examples/profiles/default-resume/profile.json#verify.atsParse`. Do **not** invent a
dark-only pack and skip the light file.

### 📦 What you deliver (default = résumé only, both themes)

```
storage/<user>/_exports/<Job>/
    <name>-resume-light.pdf     ← ALWAYS — board upload (Jobright / Indeed / LinkedIn)
    <name>-resume-dark.pdf      ← branded / humans / email
```

| Need | How |
|---|---|
| Board submit | Upload **light** only · `python -m pdf_tool.check_ats <light.pdf>` exit 0 first |
| Cover letter | Ask explicitly, or run personal `/make-cover-letter` |
| Work samples | Ask explicitly, or run personal `/make-work-examples` |
| Bundle | Only when a portal wants one file |

Print HTML: system font for **body + h2** in `@media print` (Montserrat shreds the text layer).
Jobright rank D ≠ unparseable — see [`docs/JOB-ASSESSMENT.md`](../../docs/JOB-ASSESSMENT.md) § Tier 4.5.
### 🔗 Pasted job URL with no folder yet

Create `storage/_job-listings/<App>/` with `<Company>.md` + `application.json` (Links table,
canonical apply URL) per [`docs/JOB-ASSESSMENT.md`](../../docs/JOB-ASSESSMENT.md), then continue.

---

## ✅ THE CHECKLIST (work top to bottom; don't skip)

📖 **Steps 2–4 are specified in full by [`docs/JOB-ASSESSMENT.md`](../../docs/JOB-ASSESSMENT.md)**
— the standing protocol for what to capture, verify, and judge on any listing. Read it.

- [ ] **0. Load `exportPrefs`** from `profiles/<user>-resume.json#exports.exportPrefs`. Print what you will ship.
- [ ] **1. Read** the listing + [`docs/VAULT.md`](../../docs/VAULT.md) + `users/<user>.json` + the vault (esp. **`roleTracks.<track>.angle`**) + `profiles/<user>-resume.json`. If only a URL was pasted → create `_job-listings/<App>/` first.
- [ ] **2. 🔗 CAPTURE (Tier 1) — BLOCKING.** Apply URL (canonical) · job ID · how-to-apply · **posting live?** (fetch the *direct* link; screenshot to `evidence/`) · source · dates. **No apply URL → no "ready to submit."**
- [ ] **3. ⚠ RED FLAGS (Tier 2).** **REMOTE?** · **PAY** (→ hourly + annual, compare to market, **say so loudly if below**) · W2/1099? benefits? · duration · company legit? · **portfolio/test?** · seniority mismatch · anything overlooked.
- [ ] **4. Research (Tier 3) + Evidence map (Tier 4).** What they *actually* do · named clients · what the listing **repeats** · then map every requirement → a real vault claim (✅ / ⚠ unbacked / ❌ never-claim).
- [ ] **4b. 🛑 GAP CHECK — BLOCKING. ASK THE USER.** See the box below. **Do not build until this is answered.**
- [ ] **5. Derive the theme** from their **real brand CSS** → save to `<App>/theme.json`. Then run the **palette guard**.
- [ ] **6. Rewrite the listing doc** (`<App>/<Company>.md`): status → **🔗 Links table** → routine-checks table → pay verdict → research → evidence map → gaps/prep → materials index → original listing verbatim below a `---`.
- [ ] **7. Write** the **résumé** only (company-agnostic within the track). Cover letter only if explicitly requested in this turn.
- [ ] **8. Export** per **`exportPrefs`** (light **and** dark résumé) to **`storage/<user>/_exports/<Job>/`**.
      Run `python -m pdf_tool.check_generation <doc>.html` then `python -m pdf_tool.check_ats <light.pdf>`.
      Cover letter / work samples / bundle / PNGs ONLY if asked.
- [ ] **9. Log** it in `<App>/application.json` and the listing doc.

---

## 🛑 Step 4b — THE GAP CHECK (blocking). Ask; do not assume.

> **The vault records what they have TOLD you. It is NOT the limit of what they can do.**

For every listing requirement with **no vault backing**, list it and **ask before building**:

> *"These N requirements have nothing in the vault — do you have experience with any of them?"*

**Both times we skipped this, we were wrong:**

| Lesson | What happened |
|---|---|
| **Color X** (2026-07-13) | 3ds Max, V-Ray, Unreal, and CC4 apparel were all missing from the vault. **All four turned out to be central strengths.** Nearly written off as gaps. |
| **Maya + ZBrush** (2026-07-13) | Sat in `doNotClaim` for months. **Both founders have years with both.** Forbidden on resumes purely because nobody asked. |

**`doNotClaim` means "not yet confirmed" — not "can't do it."** If they have it →
**write it into the vault first** (`source: "owner directive <date>"`) → then use it.
Only *after* asking may something honestly be called a gap.

**Assume broad competence.** Both founders are advanced across 3D art, modeling, animation, rigging,
character design, game dev (mobile/web/PC/VR), and AI tooling. Check the **capability matrix** in
[`docs/VAULT.md`](../../docs/VAULT.md) before concluding anything is missing.

---

## 🔗 Step 2 — CAPTURE THE LINK (blocking)

**A perfectly tailored application you can't submit is worthless.** This bit us on Color X: the listing
was pasted as raw text, nobody recorded where it came from, and by the time the resumes were done the
posting could no longer be found. **Never again.**

**Every listing doc MUST open with a Links table**, before anything else:

```markdown
## 🔗 Links

| Item | Value |
|---|---|
| **Apply URL** | <the exact posting URL — the thing you click to apply> |
| **How to apply** | portal / email address / recruiter contact |
| **Company site** | ... |
| **Company careers page** | ... (or "none — no careers page") |
| **Posting still live?** | ✅ verified <date> — or ⚠ could not confirm, see below |
```

**Rules:**
- **If the user pastes a listing with no URL, ASK FOR IT** before building anything. One question,
  asked up front, costs nothing; a dead application costs the whole build.
- **Verify the posting is still live** by fetching **the direct job URL itself**. If you cannot confirm
  it, say so plainly at the top of the doc and mark the status **BLOCKED**, not "ready to submit."
- **Also capture:** how to apply (portal vs. email vs. in-board), the requisition/job ID, the posting
  date, and the closing date if shown.
- **Never mark an application "ready to submit" without an apply URL or an apply email.** Status stays
  `BLOCKED — no apply link` until one exists.

### ⚠ Two traps that will fool you

**1. A company page showing "no open jobs" does NOT mean the posting is dead.** Indeed's *"Easily
apply"* postings frequently never appear on the employer's Indeed company page, and many employers
(Color X included) have no careers page at all. We nearly wrote off a **live** posting on exactly this
evidence. **Always fetch the direct job link before concluding anything.**

**2. Job-alert / email URLs are full of tracking cruft — canonicalize them.** An Indeed alert link looks
like:

```
https://www.indeed.com/viewjob?jk=069675c256f18987&q=3d+artist&l=Remote&tk=...&alid=...&utm_campaign=job_alerts&...
```

Keep **only the job key**, and record the rest as provenance:

```
https://www.indeed.com/viewjob?jk=069675c256f18987      ← canonical apply URL
jk / job ID: 069675c256f18987
source: Indeed job-alert email (alert 6a53..., query "3d artist" · Remote)
```

The `tk`/`xkcb`/`xpse` params are session tokens — they rot, and they can leak how you found the job.

### Applying *through* a job board (Indeed "Easily apply", LinkedIn Easy Apply)

- The board hosts the application — there's no company portal or email. **Upload the LIGHT/ATS PDF**
  (the board parses it); keep the dark version for direct email/portfolio only.
- If the flow offers a cover-letter **upload**, give it the merged bundle; if it only offers a **text
  box**, paste the cover-letter body.
- **Two applicants → two accounts.** A board ties an application to an account, so Jenni and Shade must
  each apply from their own login. Never submit both from one.

---

## Where things live (and where output goes)

```
storage/
  users/<user>.json              WHO is applying  (contact, emails, brand palette, hardFacts)
  <user>/resume-source.json      ⭐ THE VAULT — claims + voice + roleTracks[].angle
  profiles/<user>-resume.json    HOW it renders  (layout, exports, cover-letter policy)
                                 ↳ exactly 4: jenni · shade · martian (games) · studio (capabilities)
  _job-listings/<App-Dir>/       THE JOB
    <Company>.md                   research + the verbatim listing
    application.json               apply URL · pay · status · who applied
    theme.json                     the COMPANY-derived palette (shared, split accent runs)
    *.html                         the resume + cover-letter SOURCES
  <user>/_exports/<App-Dir>/     ⭐ ALL PDFs + PNGs GO HERE
```

**Hard rule:** the application folder holds the **listing, the two JSON records, and the HTML sources** —
no PDFs. Every PDF and PNG goes to **`storage/<user>/_exports/<Application-Dir>/`** so each person's
finished files sit in one place.

**There are no per-track profile files.** The per-role framing lives in the vault at
`roleTracks.<track>.angle` (retired 2026-07-13 — they duplicated the vault and drifted).

---

## The vault is a QUERY, not a copy

📖 Read [`docs/VAULT.md`](../../docs/VAULT.md) first.

Every claim carries **`tracks`** (`game-dev` · `3d-art` · `3d-viz` · `ui-ux` · `ai` · `audio` · `synagen`;
`any` = everywhere) and **`strength`** (`lead` / `solid` / `supporting`).

**Read the track's `angle`, then rank claims in THIS order:**

> **① track-specific claims before `any` claims · ② then by `strength` (lead → solid → supporting)**

⚠ **Do not sort by `strength` alone.** An `any`+`lead` claim (the AI-pipeline one) will outrank every
claim that is actually *about the job* — sorted naively, an **audio** résumé opens with AI tooling, which
is exactly what the lead-identity rule forbids. Track-specific first, always.

Then **cut to two pages.** Choosing the best claims for *this* job is the whole craft — never dump the vault.

**Source-backed ≠ timid.** Never invent a tool, number, credit, or employer. *Do* elaborate
persuasively on genuine overlap, in the employer's own vocabulary. Creative-writing skill is welcome
for the prose; the facts stay honest.

- **New fact from the user → write it into the VAULT first** (`source: "owner directive <date>"`), then use it.
- **`doNotClaim` = "not yet confirmed", NOT "can't do it."** → **Step 4b: ask first.** Only a *confirmed*
  absence is a gap; then put the **`honestEquivalents`** entry on the resume and name it **once, plainly**,
  in the cover letter. That candor has won us credibility.

### 🧰 A tool you know is a tool you know

**Software claims are selectable from EVERY track** (`kind: "tool"`, `tracks: ["any"]`). A
game-dev listing may absolutely ask about 3ds Max; an AI lab building generative 3D cares that
you've shipped in Blender. **Hiding a tool behind a track tag doesn't focus the résumé — it makes
it incomplete.** (One vault's `game-dev` track once saw 4 of its 12 software claims; its `audio`
track saw zero.)

**Relevance is the RANKING's job, never the tag's.** Each track declares a **`toolbeltOrder`** —
which tools *lead* for that job family. A tool not listed is still claimable; it just doesn't open
the section.

**Shared vs. individual:** both founders know the same core software, and both worked on the
engine. What is NOT shared is **depth and title** — see the vault's `sharedCapabilities` block
before writing a word about who built what.

### ⚠ Three traps that will embarrass you

1. **Tenure.** The studio is **25 years** old (founded 2000). **Jenni's tenure is 15 years** (joined Dec 2011).
   Both true, different numbers. **Never imply Jenni has 25 years.** Shade *does* — she founded it.
2. **Audio.** Deep audio — engineering, composition, spatial, reactive, WWISE — is **Shade's specialty**.
   Jenni is competent (FL Studio, Audacity). An audio-centric listing is a **Shade** or **studio**
   application, never a Jenni solo one.
3. **Shade's lead identity changes by track** — AI specialist for frontier labs; creative technologist for
   3D/viz; audio engineer for audio; founder for game-dev. Read `voice.leadIdentityByTrack` before writing
   a word, and cap the AI depth at **one section** on non-AI tracks.
- **🧍 WHOSE CREDIT IS IT? — submission-identity scoping.** Martian Games has two founders; a *studio*
  credit is not automatically *this applicant's* credit.
  - **Jenni applying as herself → NEVER cite Hasbro / Halfbrick / Oddworld / MetaArcade**, in any framing,
    **including "our studio."** Those contracts were executed by **Shade**; Jenni had no hands-on role.
  - **Shade, the studio, or both founders together →** may cite them as studio contract work.
  - Recorded in each vault under `clients.studioContracts_scoped` (`usableWhen`/`forbiddenWhen`).
  - *Why:* an interviewer asking "tell me about the Hasbro project" must get a first-person answer. A
    credit you can't speak to is a liability. **`/make-resume jenni` defaults to NOT USING them.**
  - Kixeye IS genuine prior employment — for **Shade** only.
- **Numbers:** use `metrics` verbatim (25 yrs, 15 titles, 12M+ plays). Never round up or invent.
- **Match the vault's `voice` block** — it matters as much as the facts.

### Three claims that win jobs — lead with them when the listing allows
1. **AI-powered creative pipeline** — listings ask explicitly; most applicants have nothing real. Both have it.
2. **Character Creator 4 apparel authoring** — custom clothing, footwear, hair, beauty on hyper-real
   humans. Rare, and decisive for apparel/fashion/beauty/retail/character employers. **Both** are specialists.
3. **Reactive / spatial game audio + the WWISE-Unity tools credit on *Oddworld: Soulstorm*** *(Shade)* — most
   "audio" applicants do linear audio. She wrote the integration layer on a AAA title.

---

## 📧 Emails — use the professional address

Each person's addresses and the rule for choosing between them live in
**`storage/users/<user>.json → contact` + `contact.emailPolicy`** (gitignored — real addresses stay
out of the tracked repo).

**The policy, in short:** use the professional address on the person's own domain by default; use the
studio address in a studio context; **never use a personal gmail on an application.**

---

## 🎨 Theme — derive from the company, obey the house palette rule

Pull their real brand CSS:

```bash
curl -sL "https://<company>/" -o /tmp/c.html
grep -oiE 'href="[^"]*\.css[^"]*"' /tmp/c.html
curl -sL "<that stylesheet>" | grep -oiE '#[0-9a-f]{6}\b' | sort | uniq -c | sort -rn | head -15
```

Map their hexes into the token contract (`--bg --surface --elevated --text --dim --dim2 --border
--border2 --primary --secondary --accent --support`) and give the palette a **concept** tied to what
the company *is* (Color X is a large-format *printing house* → their palette is a CMYK ink set → an
ink-primaries resume reads as fluency in their medium). No usable signal → fall back to the person's
`brandTheme`.

Save the derived palette to **`<App>/theme.json`** — it belongs to the *company*, and both applicants
render from it. Worked example: [`storage/_job-listings/3D-Visualizer/theme.json`](../../storage/_job-listings/3D-Visualizer/theme.json)
(Color X is a printing house → their palette is a CMYK ink set → an ink-primaries resume reads as
fluency in their medium; Jenni takes the warm run, Shade the cool one).

Brand fallbacks when a company gives no usable signal:
`storage/brand-design/brand-{jenninexus,synagen,martian}.json` (private, gitignored)

### 🏛 HOUSE GENERATION RULES — apply to EVERY generated doc

📖 **One-page SSOT: [`themes/GENERATION-RULES.md`](../../themes/GENERATION-RULES.md).** Must-always-be-true
rules for resume + cover letter + work-samples:

- **⛔ Names & company names are NEVER all-lowercase** in display text (headings, signature, body). A
  stylized UPPERCASE header or a wordmark image is fine; all-lowercase reads as a typo and is a defect.
- **⛔ Never wash a bright/neon/primary color over a banner, hero, or photo.** For text over an image use a
  **black → transparent gradient scrim** (or a dark solid at low opacity), never a saturated brand fill.
  Brand color goes on text/rules/borders/panels *beside* the image.
- **16:9, no-crop framing** for image galleries — `object-fit: contain` on a dark mat or a true-16:9
  source; never crop the subject off. Logos sized to look good, not huge.

### 🚫 HOUSE PALETTE RULE — NO EXCEPTIONS

> **No brown. No mustard. No puke/lime green.**
> Yellow and orange only as **bright, clean tones.** Any other green is fine.

**The trap:** darkening amber/gold for white paper **turns it brown.** Amber has *no readable dark form
on white.* On the light/print palette, hand the amber role to **another hue** (blue, teal, magenta).
Dark mode keeps the bright amber — it's fine there.

📖 **Full rule + the guard's exact bands:** [`themes/PALETTE-RULES.md`](../../themes/PALETTE-RULES.md)

**Enforced — run before every export (the one gate):**

```bash
python -m pdf_tool.check_generation storage/_job-listings/<App>/<doc>.html
python -m pdf_tool.check_generation --scan storage/<user>/defaults
```

`check_generation` runs palette + 9 other house rules (see [`docs/QA.md`](../../docs/QA.md)).
Exits non-zero and names the defect. **Fix it; don't override it.** Source-only
`check_palette` is fine as a quick preflight, but it is **not** ship verification.

> Two gotchas: the guard is a raw regex over 6-digit hex, so (a) it can't see `rgba()`/`hsl()`/3-digit
> colors, and (b) **it will flag a hex you write in a comment** — write example hexes in prose *without*
> the leading `#`.

---

## Export, verify, bundle

```bash
cd C:/Github/pdf-designer/src
APP=../storage/_job-listings/<App-Dir>
O=../storage/<user>/_exports/<App-Dir>          # ⭐ per-USER, not per-application
mkdir -p "$O"

for doc in <user>-<company>-<track>-resume <user>-<company>-<track>-cover-letter; do
  python -m pdf_tool.html_to_pdf "$APP/$doc.html" --output-dir "$O" && mv -f "$O/$doc.pdf" "$O/$doc-light.pdf"
  python -m pdf_tool.html_to_pdf "$APP/$doc.html" --output-dir "$O" --pdf-theme dark && mv -f "$O/$doc.pdf" "$O/$doc-dark.pdf"
done

python -m pdf_tool.merge_pdfs "$O/FINAL-<Name>-<Role>-Cover-Letter-and-Resume.pdf" \
  "$O/<user>-<company>-<track>-cover-letter-light.pdf" \
  "$O/<user>-<company>-<track>-resume-light.pdf" \
  --require-letter --title "<Name> - <Role> - Cover Letter and Resume"
```

> `html_to_pdf` writes `-light.pdf` / `-dark.pdf` directly (theme picks the suffix) and **never
> overwrites** — it appends `-v2`, `-v3`. Export into a clean dir. **Dark-only:** run just the
> `--pdf-theme dark` line.

**VERIFY — don't skip.** Page count + the QA gate + read the PNGs:

```bash
python -c "from pypdf import PdfReader; import glob,os
for f in sorted(glob.glob('$O/*.pdf')):
    print(len(PdfReader(f).pages),'p ',os.path.basename(f))"
# ONE QA GATE — palette · casing · margins · rendered-color · overflow@816px · footer-collision:
python -m pdf_tool.check_generation "$APP/<doc>.html"
python -m pdf_tool.pdf_to_png "$APP/<doc>.html" --pdf-theme dark
# then READ the PNGs — "check_generation PASS" is necessary but looking is still the final court
```

Resume = **exactly 2 pages** · cover letter = **1** · work-samples = **3** · bundle = **3** · all US Letter.

> **Layout.** Recipes: résumé → `layouts/resume/two-page-standard.json` (signature **bottom-RIGHT**);
> cover letter → `layouts/cover-letter/one-page-letter.json` (sign-off **bottom-LEFT**, CZI padding). Equal margins
> `@page { margin: 0.65in }` résumé / `0.75in` letter. **⚠ Each résumé page must FIT its box** or the pinned
> signature collides — `check_generation` catches it; **move a section**, never shrink the margin. Letter
> print uses `min-height` only — never résumé `height` + `overflow:hidden`. Full model:
> `docs/LAYOUT-SYSTEM.md` · `layouts/README.md` · QA: `docs/QA.md`.

---

## 🤖 ATS parse safety — the light PDF is read by a MACHINE

**How you know it’s parseable:** after light export, run
`python -m pdf_tool.check_ats <resume-light.pdf>` — exit 0 with `[OK] job title`,
`[OK] work experience`, `[OK] education`, **mid-word splits ≤ 2**, and a text dump you can read.
Full checklist: [`docs/JOB-ASSESSMENT.md`](../../docs/JOB-ASSESSMENT.md) § Tier 4.5. Same rule for
**every** profile (`jenni` · `shade` · `studio` · `martian`).

**Jobright rank D ≠ unparseable.** Their IMPROVABLE / skills-count / “Lack of Accomplishment” score is
a **content AI**. The parse gate is missing Job Title / Work Experience / Education (or a shredded
text layer). Do not “fix parseability” by rewriting claims that already pass `check_ats`.

- **🚫 NO two-column bullet lists in the resume body.** Indeed parsed our two-column experience bullets
  *across* the columns and interleaved them into gibberish (*"…camera composition **AI-powered creative
  tooling — ideation →** Photorealistic and stylized rendering… **hair, beauty** Cross-discipline…"*).
  A two-column grid is fine for **tag chips / a tools list / page-2 side-by-side entries**; never for
  prose bullets inside an experience block. **Reading order must equal DOM order.**
- **Standard `h2` labels:** `Work Experience` (not bare `Experience`), `Education`, `Skills`, plus a
  header `Job Title` line. Section `h2` **and print body** on a system font (`Segoe UI` / Arial) —
  Montserrat can split `WORK EXPERIENCE` → `W ORK EXPERIENCE` and body words → `Gam es` / `m aterials`.
- **Job blocks:** title line → company line → dates (never `COMPANY — ROLE` mashed on one line).
  Page-2 roles need company + dates too (Jobright “Important Fields Missing”).
- **Upload the resume-only light PDF**, never the merged bundle, never the dark file for boards
  (Jobright / Indeed / LinkedIn). Prefer light over dark for parsers.
- **When a board pre-fills work-experience entries from the upload, hand-fix them** — paste clean,
  single-column, plain-text bullets.
- **Cover letter / work samples:** run `check_generation`; boards still receive the light **résumé**.
  Work-samples are visual — not an ATS substitute.
## Contracts (from `AGENTS.md` — do not break)

- **Geometry locked:** US Letter, `@page { size: Letter; margin: 0.45in 0.5in 0.55in; }`. Palette
  changes never alter paper size, margins, or pagination.
- **Dual mode:** light print (default, ATS-safe) AND dark branded (`html[data-pdf-theme="dark"]`).
- **Source-backed only.** Employer-specific framing lives in the cover letter, never the resume body.
- **No auto-submission.** Prepare materials; the human submits.
- **Privacy:** `storage/` is gitignored. Never move real personal data into tracked paths; never put a
  private brand palette into the tracked default theme.

## 📝 Log it (step 9) — three places, no exceptions

1. **`<App>/application.json`** — the machine record: apply URL, pay, status, who applied, export paths.
2. **`storage/_job-listings/README.md`** — the human index, with the status and any ⚠ caveat.
3. **`<App>/<Company>.md`** — the research doc: status line + materials index.

A finished application that isn't logged is one nobody can find in a month.

## Related

[`docs/VAULT.md`](../../docs/VAULT.md) — the claim rules + capability matrix ·
[`docs/JOB-ASSESSMENT.md`](../../docs/JOB-ASSESSMENT.md) — the 5-tier listing protocol ·
[`docs/STORAGE.md`](../../docs/STORAGE.md) — the storage map ·
[`themes/PALETTE-RULES.md`](../../themes/PALETTE-RULES.md) — the color rule ·
[`docs/EXPORTS.md`](../../docs/EXPORTS.md) · [`AGENTS.md`](../../AGENTS.md)
