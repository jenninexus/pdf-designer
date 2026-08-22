"""The installer seed must be sourced from public Git files, never local vaults."""

import importlib.util
from pathlib import Path


def _load_seed_module():
    root = Path(__file__).resolve().parents[1]
    spec = importlib.util.spec_from_file_location("sync_desktop_seed", root / "scripts" / "sync-desktop-seed.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_desktop_seed_copies_only_allowlisted_tracked_public_files(tmp_path: Path):
    module = _load_seed_module()
    root = tmp_path / "repo"
    (root / "themes").mkdir(parents=True)
    (root / "themes" / "default-resume.json").write_text("{}", encoding="utf-8")
    (root / "users").mkdir()
    (root / "users" / "README.md").write_text("public", encoding="utf-8")
    (root / "users" / "private.json").write_text("secret", encoding="utf-8")
    (root / ".git").mkdir()

    # The source list is deliberately supplied here: the production function
    # obtains the same list from `git ls-files`, never the filesystem walk.
    module.tracked_public_paths = lambda _root: [Path("themes/default-resume.json"), Path("users/README.md")]
    output = tmp_path / "seed"
    assert module.sync(output, root) == 0
    assert (output / "themes" / "default-resume.json").is_file()
    assert (output / "users" / "README.md").is_file()
    assert not (output / "users" / "private.json").exists()
