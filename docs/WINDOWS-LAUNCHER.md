# Windows launcher spike

The launcher is deliberately a small PowerShell wrapper around the existing
`pdf_tool.preview` server. It is the first acceptance-tested desktop-distribution
step, not an installer, native shell, or second renderer.

```powershell
pwsh -NoProfile -File scripts/launch-design-hub.ps1
```

It starts `python -m pdf_tool.preview --port 8787 --no-open` only when a Design
Hub response is not already ready, waits for `http://127.0.0.1:8787/` to return
the expected Hub HTML, then opens the user's default browser. `-NoOpen` is
available for an automated or manual readiness check.

## Acceptance checks

1. From a checked-out, installed package, run
   `pwsh -NoProfile -File scripts/launch-design-hub.ps1 -NoOpen`.
2. Confirm it reports `Design Hub ready (local only)` and that
   `Invoke-WebRequest http://127.0.0.1:8787/` returns the Design Hub page.
3. Run it again without `-NoOpen`; it reuses the already-ready local Hub and
   opens the browser instead of starting a second server.
4. In the Hub, open the Library, Recipes, and Vault at each breakpoint in the
   project matrix: 390, 576, 768, 992, 1200, 1400, 1920, 2560, and 3840 px.
   At `<=767.98px`, all three use the same drawer switch. Drag its left edge,
   reload, and confirm the local browser preference is restored; at 390px the
   width remains within the viewport and the menu chips stay compact.
5. Confirm the drawer Refresh icon is adjacent to its X on every route; it is
   not repeated at the bottom. Close with X, the backdrop, and Escape.
6. Confirm the network boundary: the URL is loopback (`127.0.0.1`) and neither
   the launcher nor the Hub asks for an account, writes a cloud credential, or
   sends vault data anywhere.

The preferences are browser-only `localStorage` values. Documents, vaults,
profiles, palettes, and exports remain in the existing checkout's local files.

## Scope boundary

This spike intentionally does not create an installer executable, paid checkout,
cloud sync, or wizard. Those need separate product decisions after this proven
launcher path; the renderer remains the Python engine.
