<div align="center">

# PDF Designer

## Design in HTML. Print what you see.
## A local résumé studio that keeps your career data yours.

![MIT](https://img.shields.io/badge/license-MIT-9b5cf6?style=flat-square&labelColor=1a1a2e)
![Runtime](https://img.shields.io/badge/runtime-python%20%2B%20playwright-63b3ed?style=flat-square&labelColor=1a1a2e)
![Engine](https://img.shields.io/badge/engine-headless-chromium-42f4c8?style=flat-square&labelColor=1a1a2e)
![Local](https://img.shields.io/badge/local--first-no%20SaaS-ff6ec4?style=flat-square&labelColor=1a1a2e)

**Zero network calls. Zero environment variables. Zero telemetry.**

</div>

![Design Hub title screen](docs/images/hub-splash.png)

![Design Hub home — public examples](docs/images/hub-home.png)

One HTML file becomes two PDFs: a **light** ATS upload for job boards, and a **dark** branded twin with the **same pages**. Palettes change color, never paper size.

- Light + dark export from the same document
- Palette, overflow, and ATS text-layer guards
- Private vaults stay on disk and gitignored
- No SaaS, no account, no `.env`

---

## Quick start

```bash
git clone https://github.com/jenninexus/pdf-designer.git
cd pdf-designer
pip install -e ".[dev]"
playwright install chromium
python scripts/smoke-white-label.py
python -m pdf_tool.preview          # → http://127.0.0.1:8787/
```

Clone setup, Design Hub wizard, Windows wrapper, and export recipes live in **[`docs/GETTING-STARTED.md`](docs/GETTING-STARTED.md)** — not here.

See the **[public app vs personal workspace diagram](docs/WORKSPACE-LAYOUT.md#two-journeys-one-engine)**
for exactly where new-user `.example` setup, Jenni/Shade vaults, job sources, collages, `output/`,
and private `_exports/` deliverables live.

---

## Peek

<table>
<tr>
<td width="50%">

**Light résumé**<br>
Public-brand pack: first name, Nexus, email only.

![Jennifer Nexus résumé](docs/images/hub-resume-jennifer-nexus.png)

</td>
<td width="50%">

**Recipes**<br>
Named layouts + audition palettes. Geometry stays locked.

![Recipes](docs/images/hub-recipes.png)

</td>
</tr>
</table>

More stills: [`docs/images/`](docs/images/README.md).

---

## Docs

| | |
|---|---|
| [`docs/GETTING-STARTED.md`](docs/GETTING-STARTED.md) | Clone path, Hub, smoke, commands |
| [`docs/README.md`](docs/README.md) | Full index |
| [`docs/PRODUCT.md`](docs/PRODUCT.md) | Free GitHub vs later paid shell |
| [`AGENTS.md`](AGENTS.md) | Agent map (contributors) |

Protocol seeds on GitHub are `*.example.md` only. Personal vaults stay gitignored.

---

MIT — use, fork, customize. See [`LICENSE`](LICENSE). © 2026 Jenni Nexus.

Honest MIT: playwright, pypdf, pypdfium2, Pillow. AGPL history → [`docs/LICENSING-NOTES.md`](docs/LICENSING-NOTES.md).

<div align="center">

If this saves you a night of fighting a job board, a **$3 or $5** tip is welcome — it never unlocks extra features.

[Star this repo](https://github.com/jenninexus/pdf-designer) · [Links](https://jenninexus.com/links) · [Patreon](https://www.patreon.com/c/JenniNexus) · [PayPal](https://paypal.me/jenninexus)

Published by [Jenni](https://github.com/jenninexus) at [Monofinity Studio](https://github.com/monofinitystudio).

</div>
