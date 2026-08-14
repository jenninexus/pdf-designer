# Public font assets

This folder contains the small, licensed font set that a fresh clone may use
without reaching into a local `storage/` tree. The root `themes/` directory is
also copied into the wheel share during packaging, so these assets travel with
the public product.

| Font | Use | License |
|---|---|---|
| `Parisienne-Regular.woff2` | Optional script/display face for personal letters and brand flourishes. Never use it for ATS body text. | SIL Open Font License 1.1 |
| `Montserrat-VariableFont_wght.woff2` | Optional on-screen display face. Do not use it for printed résumé body text or `h2`; keep the system-font ATS rule. | SIL Open Font License 1.1 |

`OFL-1.1.txt` and `NOTICES.md` ship with the binaries. The font binaries are
exact, unmodified copies from the former local asset store; their embedded
metadata was checked before release. Add a font here only when its redistribution
license and copyright notice are known. Unverified local fonts stay private.

Use a repo-relative URL from an example, for example
`../../../themes/fonts/Parisienne-Regular.woff2` from a profile HTML file.
Never point a public example at `storage/fonts/`.
