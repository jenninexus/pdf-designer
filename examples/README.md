# `examples/` — start here, then copy into `storage/`

This folder is the **public, tracked template set**. It shows the shape of every file the toolkit uses,
with placeholder data only — no real names, contacts, or claims. Your real work lives in a **gitignored
`storage/`** folder that mirrors this structure, so nothing private is ever committed.

> **The mental model:** `examples/` (public shapes) → copy → `storage/` (your real data, gitignored).
> Full protocol: [`../docs/STORAGE.md`](../docs/STORAGE.md). Layout system:
> [`../docs/LAYOUT-SYSTEM.md`](../docs/LAYOUT-SYSTEM.md).

## First run (fresh clone)

```bash
pip install -e ".[dev]" && playwright install chromium     # one-time
python -m pdf_tool.preview                                  # Design Hub → http://127.0.0.1:8787/
```

The Design Hub already renders everything in `examples/` (and it **auto-refreshes** when you export a
new document — no restart). To make it yours:

```bash
mkdir -p storage/users storage/profiles storage/brands storage/applications

# a person + their claim vault + a render profile
cp examples/profiles/default-resume/user.example.json         storage/users/me.json
cp examples/profiles/default-resume/resume-source.example.json storage/me/resume-source.json
cp examples/profiles/default-resume/profile.example.json      storage/profiles/me-resume.json

# your brand palette (colors only — no personal data)
cp examples/brands/brand-example.json                         storage/brands/brand-me.json

# a job application folder
cp -r examples/applications/example-application               storage/applications/My-Role
```

Then edit those copies with your real details and export:

```bash
python -m pdf_tool.html_to_pdf storage/applications/My-Role/my-resume.html          # light / ATS PDF
python -m pdf_tool.html_to_pdf storage/applications/My-Role/my-resume.html --pdf-theme dark  # branded
```

## What's here

| Path | It's the template for |
|---|---|
| [`profiles/default-resume/`](profiles/default-resume/) | A person: `user.example.json` (who), `resume-source.example.json` (the **claim vault**), `profile.example.json` (how it renders), plus a working `default-resume.html` you can open in the hub |
| [`profiles/default-collage/`](profiles/default-collage/) | A collage/gallery document |
| [`brands/`](brands/) | A brand-neutral color palette (`brand-example.json`) — map your real colors into these token names |
| [`applications/`](applications/) | One-folder-per-job workflow: the listing doc, `application.json`, `theme.json`, and the HTML sources. `tracker.example.json` shows the status roll-up. |

## The rules that keep it clean

- **Equal margins, pinned footer.** Every document uses one margin on all four edges (default `0.65in`),
  the header flows at the top, the footer/signature pins to the bottom. Don't fight it — reuse the
  classes in [`../themes/default-resume.css`](../themes/default-resume.css). Full spec:
  [`../docs/LAYOUT-SYSTEM.md`](../docs/LAYOUT-SYSTEM.md).
- **Content must fit the page box** (9.7in tall at the default) or the pinned signature collides with
  the last lines. `python -m pdf_tool.check_overflow <doc>.html --pdf-theme dark` catches it (and
  auto-warns on every export). If it warns, **move a section to the next page** — never shrink the margin.
- **Palette rule.** No brown, no mustard, no puke/lime green. Run
  `python -m pdf_tool.check_palette <doc>.html` before every export.
  ([`../themes/PALETTE-RULES.md`](../themes/PALETTE-RULES.md)).
- **Source-backed only.** A résumé is a *query* against the vault — never write a claim that isn't in it.
  ([`../docs/VAULT.md`](../docs/VAULT.md)).
- **Nothing real in tracked paths.** Real data goes in `storage/` (gitignored). `*.example.*` files stay
  public; everything you copy off them stays local.
