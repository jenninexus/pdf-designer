# Job Listing Assessment Protocol

**What to capture, verify, and judge for EVERY job listing — before a single word of a resume is written.**

Run by `/make-resume` (Steps 2–4). This page is the SSOT for *what we track and why*.
Sibling docs: [`VAULT.md`](VAULT.md) (what we may claim) · [`STORAGE.md`](STORAGE.md) (layout + brand SSOT).

> **Why this exists.** On the Color X application we built two complete, polished applications before
> anyone asked where the listing came from — then nearly wrote the job off as dead because Indeed's
> company page said "no open jobs" (it was live the whole time). Both failures were *capture* failures,
> not judgment failures. Capture first, assess second, write third.

---

## 🔗 TIER 1 — Capture (BLOCKING: no build starts without these)

If the listing is pasted as raw text with no link, **ask for the URL before doing anything else.**

| # | Field | Why it matters |
|---|---|---|
| 1 | **Apply URL** (canonical) | Without it the application is unsubmittable. Strip tracking params — keep only the job key. |
| 2 | **Job / requisition ID** | Survives URL changes; the durable handle (Indeed `jk=`, Greenhouse/Lever IDs). |
| 3 | **How to apply** | In-board ("Apply with Indeed" / Easy Apply) · company portal (Workday/Greenhouse/Lever) · email · recruiter. Determines what file format you actually submit. |
| 4 | **Posting is live?** | **Fetch the direct link and confirm.** Screenshot it into `evidence/<board>-posting-<date>.jpeg`. |
| 5 | **Source** | Where it was found (job-alert email, LinkedIn, referral). Provenance for follow-up. |
| 6 | **Posted / closing date** | Age predicts responsiveness; a closing date is a deadline. |
| 7 | **Verbatim listing text** | Preserved below a `---` in the listing doc. It is the ATS keyword surface and the requirement source. |

### ⚠ Two traps that will fool you

1. **"No open jobs" on the company page ≠ the posting is dead.** Board-hosted *Easily apply* postings
   frequently never surface on the employer's company page, and many employers have **no careers page
   at all** (Color X has none; `/careers/` 404s). **Only the direct job link is authoritative.**
2. **Job-alert URLs are full of rot.** `?jk=069675c256f18987&tk=...&alid=...&utm_campaign=job_alerts&xkcb=...`
   → keep **`https://www.indeed.com/viewjob?jk=069675c256f18987`**. The `tk`/`xkcb`/`xpse` tokens are
   session-scoped, expire, and leak how you found the job.

---

## ⚠ TIER 2 — Red-flag checks (do these BEFORE investing in a build)

Put these in a table at the **top** of the listing doc. Each one can kill an application on its own.

| # | Check | Verdict must state |
|---|---|---|
| 1 | **Remote?** | Truly remote, hybrid, or on-site? Any **state/country restriction**? Required time zone or overlap hours? |
| 2 | **💰 Pay** | Extract the number. **Convert to hourly AND annual.** **Search the market rate** for that role + city. **If it's below market, say so loudly** with the comparison — never bury it. |
| 3 | **Employment type** | W2 / 1099 / contract / contract-to-hire? **Benefits? PTO?** A 1099 carries ~15.3% self-employment tax on top — a "$300/day" contract is not a $300/day job. |
| 4 | **Duration & extension** | Fixed-term? Is "possible extension" real or decorative? |
| 5 | **Company legitimate?** | Age, size, real address, named clients. Scam/staffing-mill check. |
| 6 | **Portfolio / test required?** | **Exactly what must be shown?** This is often the real gate — and the biggest hidden cost. |
| 7 | **Seniority mismatch** | Are we over- or under-leveled vs. the band? Expect the question; have the honest answer. |
| 8 | **Anything overlooked** | Visa/work auth, on-site days, equipment, non-compete, IP assignment, unusual asks. |

**Rule: a below-market rate gets a recommendation, not a shrug.** Give the options (apply and
negotiate / apply as a studio-pair / skip) and say which one you'd pick and why.

---

## 🏢 TIER 3 — Company research (shapes the pitch)

| # | Capture | Use it for |
|---|---|---|
| 1 | **What they actually do** | The pitch angle. *Color X doesn't just design retail — they print, fabricate, and install it. So a render has to survive the shop floor.* That one sentence drove both cover letters. |
| 2 | **Founded / size / scale** | Credibility and stability signals. |
| 3 | **Named clients** | The strongest personalization hook. (Color X: Nike, Bloomingdale's, J.Crew, Michael Kors, the Met.) |
| 4 | **Their real brand colors** | Pull their site CSS → derive the resume theme. See `/make-resume` Step 5. |
| 5 | **What the listing repeats** | Repetition = priority. Color X asked for **AI-powered creative tools twice** — that's the sleeper requirement, and most applicants have nothing real to say. |
| 6 | **What they're admitting** | *"Own our growing library… build scalable systems"* = their asset pipeline is immature. That's an opening, not a chore. |

---

## 🛑 TIER 3.5 — THE GAP CHECK (ask the user BEFORE you build)

**Owner directive 2026-07-13 — BLOCKING.**

While building the Tier 4 map, you will hit requirements with **no vault backing**. Do **not** silently
write them off as gaps and print the resume. **STOP and ask.**

> **The vault is a record of what we've told you — not the limit of what we've done.**
> Jenni and Shade have 14 and 25 years of experience. The vault captures a fraction of it. A
> requirement that looks like a gap is very often just a fact nobody has written down yet.

### The rule

For **every** listing requirement where you find no related experience, tool, or verifiable proof in the
vault:

1. **List it explicitly, before writing anything.** Group them: *"These 4 requirements have no vault
   backing: Rhino, SketchUp, IWD, retail-merchandising experience."*
2. **Ask the user directly:** *"Do you have experience with any of these? Anything adjacent I should
   know about — a project, a client, a course, a tool you use that I don't have recorded?"*
3. **If they do → write it into the vault first** (`source: "owner directive <date>"`), then use it.
   The vault gets permanently richer, and the next application in that track benefits automatically.
4. **If they genuinely don't → only then** treat it as a real gap: honest equivalent on the resume,
   named once in the cover letter.

### Why this is worth the interruption

- **Asking costs one message. Not asking costs the job.** A resume that omits a qualification you
  actually hold is strictly worse than one that includes it.
- **It compounds.** Every answer permanently improves the vault. The Color X build alone surfaced 3ds
  Max, V-Ray, Unreal, and CC4 apparel authoring — none of which were in the vault beforehand, and **all
  four turned out to be central to the pitch.** Had nobody asked, we'd have submitted a resume claiming
  only Blender and Unity for a job requiring 3ds Max. That's the whole cautionary tale.
- **It respects the honesty rule rather than straining it.** We are not inventing anything — we are
  *asking* whether a real thing exists.

**Never print a resume with an unexamined gap.** If the user is unavailable, say plainly in the summary
which requirements went unverified.

---

## ✅ TIER 4 — Requirement → Evidence map (the honesty ledger)

A table mapping **every** listing requirement to what the vault can truthfully back:

| Their ask | Our honest answer | Status |
|---|---|---|
| Advanced 3ds Max | Trained + experienced | ✅ |
| V-Ray / Corona / Enscape | V-Ray yes; Corona/Enscape no | ✅ partial |
| Advanced Rhino, SketchUp | **Not claimed** — adjacent, adoptable | ⚠ **gap → cover letter** |
| AI-powered creative tools | 3 yrs production pipeline | ✅ **differentiator** |
| Experience with IWD | Not claimed | ⚠ preferred-only |

- **✅ = lead with it.** **⚠ = name it honestly in the cover letter, once, then pivot to the equivalent.**
  **❌ = never claim it** (check the vault's `doNotClaim` + `honestEquivalents`).
- Close with an explicit line: *"Never claimed on these resumes: Rhino, SketchUp, …"* — so a future
  reader can audit the honesty at a glance.

---

## 📋 TIER 5 — Prep & gaps (what to do before submitting)

Rank by **leverage**, not by effort. State the single highest-value action plainly.

- **The real gate** — for Color X it's the retail portfolio, not the tool gap. *"Render 2–3 retail
  vignettes: a CC4 mannequin in custom garments, a lit window bay, one stylized + one photoreal pass.
  That afternoon of work converts this from interesting outsider to obvious hire."*
- **Questions to ask them** (W2 or 1099? extension path? equipment?).
- **The upsell**, if there is one (Synagen as bespoke tooling).
- **Interview landmines** to rehearse (overqualification, the tool gap).

---

## 🤖 TIER 4.5 — ATS PARSE SAFETY (the light PDF must survive a machine)

**Owner-observed 2026-07-13, Indeed · 2026-08 Jobright.** The light/ATS PDF is not just "the printable
one" — it is the file a **parser** reads. Design it for the machine, not only for the eye.

### How to know a résumé is parseable (every profile)

| Step | Command / action | Pass looks like |
|---|---|---|
| 1 | Export **light** PDF (`html_to_pdf` default — no `--pdf-theme dark`) | `*-resume-light.pdf` beside the HTML |
| 2 | `python -m pdf_tool.check_ats <resume-light.pdf>` | Exit 0 · required cues `[OK] job title` · `[OK] work experience` · `[OK] education` |
| 3 | **Read the text dump** in that command | Contiguous phrases a human can find — not `W ORK EXPERIENCE`, not two-column gibberish |
| 4 | Board upload (Jobright / Indeed / LinkedIn) | No “missing Job Title / Work Experience / Education” warning |

**Applies to every profile under `storage/profiles/`** (jenni · shade · studio · martian) and the
public `examples/profiles/default-resume/`. Creative headings (`My Journey`, bare `Experience`,
`Training`) are not parseable field names. Work-samples PDFs are visual — boards get the **light
résumé**, not the portfolio.

`check_ats` is the local SSOT for “is it parseable?” — dashboard also in [`SSOT.md`](SSOT.md) § ATS
parseability. **Dark is not “unparseable”** (same HTML text layer as light); boards still want the
**light** upload. Prefer running `check_ats` on `*-resume-light.pdf` and uploading that file.

### 🚫 Two-column bullet lists are BANNED in the resume body

Indeed read our two-column bullets **across the columns**, interleaving them into nonsense:

> *"Lighting, materials, texturing, and camera composition **AI-powered creative tooling in production —
> ideation → iteration →** Photorealistic and stylized rendering for the same subject **asset**"*
> *"Hyper-real character + apparel authoring (CC4): clothing, shoes, **Fast iterative cadence…**"*
> *"**hair, beauty** Cross-discipline coordination…"*

The garbled text is what the employer sees, and "hair, beauty" ends up orphaned on its own line.

**Rules for the resume body:**
- **Bullets = one column.** A two-column *grid* is fine for short, self-contained items (tag chips, a
  tools list, page-2 side-by-side entries), but **never for prose bullets in an experience block.**
- **Reading order = DOM order.** If a human reading the raw HTML top-to-bottom gets gibberish, so will
  the parser.
- **No text in `position: absolute`** anywhere the parser needs it (our signature block is fine — it's
  decorative and duplicated in the contact line).
- Keep arrows/glyphs (`→`, `·`, `—`) out of bullets that carry keywords; they survive, but they add noise.

### Verify the parse before submitting

Extract the text in reading order and *read it*. If it doesn't make sense to you, it won't to the ATS:

```bash
python -c "import fitz; d=fitz.open('<resume>-light.pdf'); print(d[0].get_text())"
```

### When the board pre-fills from the resume

Boards (Indeed, LinkedIn, **Jobright**) parse the upload into editable work-experience entries. **Always review and
hand-fix those entries** — a clean fix in the form beats a mangled auto-parse. Paste single-column,
plain-text bullets.

**Upload the resume-only light PDF** — never the merged cover-letter+resume bundle, and prefer the
**light** export over the dark branded one for board parsers. A parser fed the bundle will read the
cover letter as resume content.

### ⚠ Jobright / board “missing Job Title / Work Experience / Education”

Owner-observed 2026-08 (Jobright.ai). Their checker warns when it cannot map those three fields —
even if the words exist somewhere in the PDF. Fixes that cleared it on the Jenni default:

| Field | What fails | What to put in the HTML |
|---|---|---|
| **Job Title** | Title mashed into `COMPANY — ROLE` on one line; or only a soft tagline | Header line `Job Title` + role; each job block = **title line**, then **company**, then dates |
| **Work Experience** | Heading is only `Experience` | Exact heading **`Work Experience`** (`h2`) |
| **Education** | Buried as an `h3` inside a two-column grid | Top-level **`Education`** section (`h2`), full width |

Also — **font metrics matter.** Montserrat’s `W` glyph advances made the PDF text layer extract
`WORK EXPERIENCE` as `W ORK EXPERIENCE` (Jobright then warns the section is missing), even at
`letter-spacing: 0`. Section `h2` cues on the Jenni default use `"Segoe UI", Arial, Helvetica`
so the cue stays contiguous. Extreme tracking on brand words (`0.18em` → `je nnine xus`) has the
same failure mode — keep decorative spacing ≤ `0.04em` on ATS-critical labels.

---

## 🗂 What ends up on disk

```
storage/_job-listings/<Role-Track>/
  <Company>.md                       ← the assessment (Tiers 1–5) + verbatim listing below a ---
  evidence/
    <board>-posting-<date>.jpeg      ← screenshot proving it was live, and what it said
  <user>-<company>-<track>-resume.html
  <user>-<company>-<track>-cover-letter.html

storage/<user>/_exports/<Role-Track>/   ← ALL PDFs + PNGs (never in the application folder)
```

**Also log** into `profiles/<user>-<track>-resume.json → roleTrack.applications[]`:
`applyUrl` · `jobId` · `howToApply` · `postingVerified` · `status` · `caution`.

### Status vocabulary (be precise — the user relies on it)

| Status | Means |
|---|---|
| `BLOCKED — no apply link` | Materials may exist, but it **cannot be submitted**. Never call this "ready." |
| `BLOCKED — posting dead` | Direct link fetched; posting is gone. |
| `READY TO SUBMIT` | Apply URL verified live + materials generated, bundled, and page-count checked. |
| `SUBMITTED <date>` | Sent. Record which files and from which account. |

---

## The one-line version

> **Capture the link and the pay before you write a word.** Verify the posting from its *direct* URL,
> never from a company page. Map every requirement to a real claim, name the gaps out loud, and say
> plainly whether the money is worth it.
