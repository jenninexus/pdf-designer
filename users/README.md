# `users/` — who is applying

Person cards: contact, `characterVoice`, brand pointer.

| Tracked | Gitignored |
|---|---|
| this README · [`examples.json`](examples.json) (Jane Example) · `*.example.json` | real `<id>.json` (PII) |

Copy [`you.example.json`](you.example.json) → `users/<you>.json`. The live Hub person
[`examples.json`](examples.json) stays tracked so Vault still has Jane Example after you add yourself.

This workspace follows Windows **Documents**. If OneDrive (or another provider) redirects
Documents, this folder can sync with that account. PDF Designer does not create the cloud
account; turning Documents backup off keeps the files only on this PC.

Same copy-me shape: [`examples/profiles/default-resume/user.example.json`](../examples/profiles/default-resume/user.example.json).

The engine also reads the legacy tree `storage/users/` until the alias is dropped. Layout: [`docs/WORKSPACE-LAYOUT.md`](../docs/WORKSPACE-LAYOUT.md).

Keep one record per identity. Its render settings live in [`profiles/`](../profiles/). A demo alias can have a separate person record limited to public brand data. A studio application uses studio-scoped evidence rather than a person's contact record.
