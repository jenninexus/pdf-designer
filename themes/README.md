# Document themes and Hub chrome

This folder owns reusable document palettes, fonts and generation rules. Public defaults and presets ship with the engine. Personal mapped brand colors belong in ignored `brands/`; person records point there rather than duplicating hex values.

The Design Hub has a separate visual shell:

| Concern | Authoring authority | Public runtime copy |
|---|---|---|
| Layout and named navigation breakpoint | Optional private `www-theme-kit/profiles/pdf-designer.json` | `src/pdf_tool/static/hub.css` and `drawer-resize.js` |
| Aesyna visual and motion tokens | Optional private `syna-theme-kit/adapters/pdf-designer.json` | Generated `src/pdf_tool/static/hub-aesyna.css` |
| Document palettes and print geometry | This folder and `layouts/` | The same packaged engine assets |

Only the www kit has a PDF Designer **profile**. The Syna adapter contains visual tokens, not a competing responsive profile. Maintainers regenerate it with `node scripts/sync-pdf-designer.mjs` from the Syna kit and verify with `--check`. Consumers copy the result; never import a sibling kit from a running public application. Fresh clones need neither private kit.

The existing named scale is `bootstrap_5_3_8_extended_390_4k`; PDF navigation uses `lg`/992 while library stacking remains phone-only. Portable project pointers live in `.config/mcp-pdf-designer.example.json`; local MCP server registrations do not own theme data. See [PREVIEWER](../docs/PREVIEWER.md) and [SSOT](../docs/SSOT.md).
