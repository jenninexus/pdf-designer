# Layout System — the shared page model for résumés, cover letters & work samples

**One page model for every application document**, so the three doc types read as a family and the
sign-off always lands where it should. Established 2026-07-19 while refining the Netflix build.

> **Sibling docs:** [`THEME-DESIGN.md`](THEME-DESIGN.md) (tokens, dual light/dark, signature pin) ·
> [`EXPORTS.md`](EXPORTS.md) (export commands + pagination traps) ·
> [`../themes/PALETTE-RULES.md`](../themes/PALETTE-RULES.md) (color guard).
> **Profile hook:** `storage/profiles/jenni-resume.json → layout.system` points here.

---

## The one rule that fixes 90% of layout complaints

> **Every page is a flex column with a growing body and a footer pinned by `margin-top: auto`.**

```css
.page { display: flex; flex-direction: column; }   /* the sheet */
.page-main { flex: 1 1 auto; min-height: 0; }        /* body grows to fill */
.footer, .signature { margin-top: auto; }            /* sign-off pinned to the bottom */
```

Why it matters: without this, a short letter leaves its sign-off floating in the vertical middle with
a lake of empty space below it (the exact complaint that started this doc). With it, the body takes the
space it needs and the sign-off sits at the bottom with the **whitespace above** it — which is what
reads as "finished and deliberate." The résumé already did this (bottom-right signature); the
**cover letter and work-samples now do too**.

The **print** rule must repeat the flex declaration (some engines drop it when `.page` is restyled for
`@media print`) **and set `overflow: hidden`** — the second half of the fix:

```css
@media print {
  .page {
    display: flex; flex-direction: column;
    height: <content-box>in;   /* = 11in − 2 × equal-margin */
    overflow: hidden;          /* ⭐ clip; never bleed onto the next sheet */
  }
  .page-main, .letter-main { flex: 1 1 auto; min-height: 0; }
  .footer, .signature { margin-top: auto; }
}
```

### ⚠ `overflow: hidden` is not optional — it's what makes the bug impossible

**The 2026-07-19 overlap bug, understood properly.** With multiple manual `.page` divs (a 2-page
résumé) each at a fixed height, if a `break-inside: avoid` section can't fit the space left on page 1,
Chromium's print engine pushes that whole block onto page 2 — but page 2 is its *own* fixed-height sheet
that also starts at the top, so the bumped block lands **on top of** page 2's header and content. Neither
a page-count check nor a DOM height measurement catches this (page 1 "fits"; the PDF still has 2 pages).

`overflow: hidden` on the fixed-height `.page` makes it **structurally impossible**: any content past the
page edge is clipped, never rendered onto the next sheet. Worst case becomes a visibly cut-off tail
(loud, obvious — move a section), instead of a silent overlap. **Every `.page` in every template must
carry it in print.** `check_overflow` is the authoring *warning*; `overflow: hidden` is the *guarantee*.

**Ground truth is the exported PDF, not a DOM measurement or an HTML re-render.** When verifying a
pagination fix, rasterize the actual PDF and read it (`pdf_to_png`, or `pypdfium2`) — `check_overflow`'s
DOM measurement is a fast pre-flight, not a substitute for looking at the real output.
`check_generation`'s **footer-collision** check goes further: it exports a real PDF and inspects the
signature band for body text (the defect DOM height can still miss when a 2-col block sits under the
script). Ship gate: [`QA.md`](QA.md).

### ⚠ A line that belongs above the footer goes INSIDE the footer

A second failure mode (fixed 2026-07-19, work-samples last page): a loose `<p>` — e.g. a "full
portfolio · links" line — placed at the **end of `.page-main`, just before the pinned footer**, drifts
to the very bottom when the page fills and **collides with the signature**. `.page-main` grows to fill;
its last child ends up flush against the `margin-top:auto` footer. **Fix:** put that line *inside* the
pinned footer block, above the name/email row. Use the shared `.page-foot--stacked` pattern
(`.foot-line` above a `.foot-row`) in `themes/default-resume.css` — the line and the signature are then
pinned together and can never overlap.

---

## Equal margins — the professional frame

> **Every document uses ONE margin value on all four edges (top = right = bottom = left).**
> A resume that's 0.5in on top and 0.78in on the bottom looks lopsided; equal margins read as
> deliberate and professional, and make the three doc types a matched set.

The **default is `0.65in` on all four edges** (`themes/default-resume` — `@page { margin: 0.65in }`).
A document may open the frame *wider* for a specific look, but it must stay **equal**:

| Doc | Equal margin (all 4 edges) | Content box | Print `.page` height | Footer pin | Pages (FIXED) |
|---|---|---|---|---|---|
| **Résumé** *(the default)* | **0.65in** | 7.2 × 9.7in | `calc(11in − 2×0.65in)` = 9.7in | signature → **bottom-right** | **2** |
| **Cover letter** | 0.75in *(a notch airier — a formal letter)* | 7.0 × 9.5in | 9.5in | sign-off → **bottom-left** | **1** |
| **Work samples** | 0.60in *(a notch tighter — images keep width)* | 7.3 × 9.8in | 9.8in | footer row → **bottom** (name L, links R) | **3** |

**Content-box height math:** `11in − 2 × margin`. Set the print `.page { height }` to exactly this — a
value that's too tall spills a phantom trailing page (see EXPORTS.md pagination traps).
`0.65in → 9.7in`, `0.75in → 9.5in`, `0.60in → 9.8in`.

**The default theme carries this as one knob** — `themes/default-resume.css` exposes
`--resume-page-margin: 0.65in` and derives every edge from it; on screen it becomes `.page` padding, in
print it becomes the `@page` margin and the `.page` height is `calc(11in − 2 × var(--resume-page-margin))`.
Templates that don't `@import` the theme still follow the same equal-margin rule inline.

### Vertical rhythm (what "airier" meant)

- **Résumé:** `header` bottom-margin ~20px; `section` ~19px; under `h2` ~12px; list items ~4px; column
  gap ~32px. Signature `padding-top` ~18px.
- **Cover letter:** header block sits above a `border-bottom` rule with ~24px gap before the recipient;
  paragraph gap ~13px; **~30px gap above the sign-off** (plus `margin-top:auto`).
- **Work samples:** `section` ~20px; callout padding ~14–16px; footer `padding-top` ~20px.

### Work-samples imagery — keep height, minimize crop

Portfolio images are the point, so they get real height (they were over-cropped in v1):

| Element | Height |
|---|---|
| Hero (cover) | **252px** |
| Game shots (2-col grid) | **132px** |
| Agent cards (3-col grid) | **104px** |

`object-fit: cover` still crops to the box — these heights keep enough of each scene to read. If a
specific image's subject is getting cut, raise that grid's height rather than fighting `object-fit`.

---

## Work-samples build pattern (self-contained, image-led)

The work-samples PDF is a **visual** piece (NOT ATS-parsed), so it may go image-heavy. It's built to be
fully self-contained — no external image hosts:

1. Author `<doc>.template.html` with `{{img:name}}` placeholders; keep sources in the application's
   `assets/` dir.
2. A small Python inliner replaces each `{{img:name}}` with a base64 `data:` URI → `<doc>.html`.
3. Export light + dark to `storage/<user>/_exports/<App>/`. **Upload the dark version** for impact;
   keep the ATS `resume-light` as the primary Resume upload.

Worked example: `storage/_job-listings/Netflix-App/jenni-netflix-genai-work-samples.template.html`.
Profile contract: `storage/profiles/jenni-resume.json → workSamples`. Asset sources + flagship beats:
`storage/users/jenni.json → portfolio`.

---

## Verify before shipping

- **Page count from the PDF, never the browser:**
  `python -c "from pypdf import PdfReader; print(len(PdfReader('<f>.pdf').pages))"` — résumé **2**,
  cover **1**, work-samples **3**.
- **Palette guard:** `python -m pdf_tool.check_palette <doc>.html` (data-URI blobs don't trip it; it's a
  `#hex` regex).
- **Eyeball the render:** `python -m pdf_tool.pdf_to_png <doc>.html --pdf-theme dark`. Note the PNG
  renders **without** the `@page` gutter (full-bleed) — judge *relative* spacing and the pinned footer,
  not the outer margin (the PDF adds that).

---

## Auto-refresh preview

The Design Hub (`python -m pdf_tool.preview`) **auto-refreshes** — no restart when you export a new
resume or edit a source. It polls `/api/version` (a cheap tree signature over HTML sources + `_exports/`
outputs); when the signature changes the sidebar re-renders, the open preview reloads, and a small toast
flashes (`＋1 document`). So the loop is: edit/export → the hub updates itself. See
[`PREVIEWER.md`](PREVIEWER.md).

## Future work

- Promote the equal-margin knob (`--resume-page-margin`) is **done** in `themes/default-resume.css`;
  next: a shared `themes/application-layout.css` that templates `@import` so each HTML stops carrying its
  own copy of the flex/print rules (the Netflix templates still inline them).
- Parameterize per-doc image heights as CSS custom properties so a new company theme only overrides
  colors, never geometry (geometry stays locked per the AGENTS.md contract).
- Add a tiny `pdf_tool` check that fails if a template's print `.page { height }` doesn't match
  `11in − 2 × @page-margin` (catches the phantom-page trap automatically).
