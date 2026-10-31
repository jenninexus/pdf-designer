# Extension action QA needs a managed debugger attachment

**Trigger:** installed Chromium extension action tests time out on popup initialization or
raw CDP calls while ordinary extension tabs work. Do not infer a production CSP failure.

Playwright's Chromium driver normally detaches from protocol targets classified as `other`.
An extension action can have that classification even when the HTTP debugging target list
reports `page`. A competing raw websocket debugger and the driver's attach/resume lifecycle
caused intermittent timeouts in repeated real-action tests.

`browser-extension/test-browser.py` sets `PW_CHROMIUM_ATTACH_TO_OTHER=1` in its own QA process
before starting Playwright, then uses Playwright's managed page for the new action created by
the browser's native `Extensions.triggerAction` command on the exact fixture target. It identifies
a newly created action page and closes that exact owned popup.
This is harness configuration, not a production permission, CSP change or substitute action.
The native command avoids foreground-activation races and global keyboard input entirely.
Resolve the exact `tab` target with `Target.getTargets`; the renderer's `page` target is rejected.
Reuse the open action for same-document cases, resetting the fictional DOM before a fresh review;
reopen after browser dismissal. Recreating a native popup per assertion needlessly repeats startup.

Inspect the installed driver's handling again if upgrading Playwright changes this behavior;
do not silently downgrade acceptance to a normal extension tab. The owning
[browser-helper guide](../docs/BROWSER-HELPER.md#reproducible-checks) records the repeatable checks.
