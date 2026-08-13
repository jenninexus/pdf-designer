"""Dual-path workspace resolver — new nouns + storage/ alias."""

from __future__ import annotations

from pathlib import Path

from pdf_tool import paths


def test_alias_user_and_vault():
    assert paths.alias_rel_paths("users/jenni.json") == (
        "users/jenni.json",
        "storage/users/jenni.json",
    )
    assert paths.alias_rel_paths("storage/users/jenni.json") == (
        "users/jenni.json",
        "storage/users/jenni.json",
    )
    assert paths.alias_rel_paths("vaults/shade.json") == (
        "vaults/shade.json",
        "storage/shade/resume-source.json",
    )
    assert paths.alias_rel_paths("storage/shade/resume-source.json") == (
        "vaults/shade.json",
        "storage/shade/resume-source.json",
    )


def test_alias_applications_and_brands_bare_dirs():
    assert paths.alias_rel_paths("_job-apps") == (
        "_job-apps",
        "applications",
        "storage/_job-listings",
    )
    assert paths.alias_rel_paths("applications") == (
        "_job-apps",
        "applications",
        "storage/_job-listings",
    )
    assert paths.alias_rel_paths("storage/_job-listings/3D-Visualizer/application.json") == (
        "_job-apps/3D-Visualizer/application.json",
        "applications/3D-Visualizer/application.json",
        "storage/_job-listings/3D-Visualizer/application.json",
    )
    assert paths.alias_rel_paths("brands") == ("brands", "storage/brand-design")
    assert paths.alias_rel_paths("resumes/jenni/defaults/x.html") == (
        "resumes/jenni/defaults/x.html",
        "storage/jenni/defaults/x.html",
    )


def test_alias_leaves_examples_alone():
    assert paths.alias_rel_paths("examples/profiles/default-resume/x.html") == (
        "examples/profiles/default-resume/x.html",
    )


def test_resolve_prefers_new_file(tmp_path: Path):
    (tmp_path / "users").mkdir()
    (tmp_path / "users" / "alex.json").write_text("{}", encoding="utf-8")
    (tmp_path / "storage" / "users").mkdir(parents=True)
    (tmp_path / "storage" / "users" / "alex.json").write_text("old", encoding="utf-8")
    got = paths.user_path("alex", root=tmp_path)
    assert got == tmp_path / "users" / "alex.json"


def test_resolve_falls_back_to_storage(tmp_path: Path):
    (tmp_path / "storage" / "users").mkdir(parents=True)
    (tmp_path / "storage" / "users" / "alex.json").write_text("{}", encoding="utf-8")
    (tmp_path / "users").mkdir()
    (tmp_path / "users" / "README.md").write_text("scaffold", encoding="utf-8")
    got = paths.user_path("alex", root=tmp_path)
    assert got == tmp_path / "storage" / "users" / "alex.json"


def test_scaffold_dir_does_not_steal_legacy_jobs(tmp_path: Path):
    (tmp_path / "_job-apps").mkdir()
    (tmp_path / "_job-apps" / "README.md").write_text("scaffold", encoding="utf-8")
    (tmp_path / "applications").mkdir()
    (tmp_path / "applications" / "README.md").write_text("scaffold", encoding="utf-8")
    job = tmp_path / "storage" / "_job-listings" / "Track"
    job.mkdir(parents=True)
    (job / "application.json").write_text("{}", encoding="utf-8")
    assert paths.applications_dir(root=tmp_path) == tmp_path / "storage" / "_job-listings"


def test_neither_file_prefers_legacy_while_storage_exists(tmp_path: Path):
    (tmp_path / "storage").mkdir()
    got = paths.vault_path("alex", root=tmp_path)
    assert got == tmp_path / "storage" / "alex" / "resume-source.json"


def test_neither_file_prefers_new_on_fresh_clone(tmp_path: Path):
    got = paths.vault_path("alex", root=tmp_path)
    assert got == tmp_path / "vaults" / "alex.json"


def test_iter_vaults_prefers_new_and_skips_example(tmp_path: Path):
    (tmp_path / "vaults").mkdir()
    (tmp_path / "vaults" / "alex.json").write_text("{}", encoding="utf-8")
    (tmp_path / "vaults" / "you.example.json").write_text("{}", encoding="utf-8")
    legacy = tmp_path / "storage" / "alex" / "resume-source.json"
    legacy.parent.mkdir(parents=True)
    legacy.write_text("old", encoding="utf-8")
    other = tmp_path / "storage" / "blake" / "resume-source.json"
    other.parent.mkdir(parents=True)
    other.write_text("{}", encoding="utf-8")
    got = list(paths.iter_vault_paths(root=tmp_path))
    stems = {p.stem if p.parent.name == "vaults" else p.parent.name for p in got}
    assert stems == {"alex", "blake"}
    assert got[0] == tmp_path / "vaults" / "alex.json"


def test_iter_application_json_dedupes(tmp_path: Path):
    new_job = tmp_path / "_job-apps" / "Track"
    new_job.mkdir(parents=True)
    (new_job / "application.json").write_text("new", encoding="utf-8")
    old_job = tmp_path / "storage" / "_job-listings" / "Track"
    old_job.mkdir(parents=True)
    (old_job / "application.json").write_text("old", encoding="utf-8")
    extra = tmp_path / "storage" / "_job-listings" / "Other"
    extra.mkdir(parents=True)
    (extra / "application.json").write_text("{}", encoding="utf-8")
    got = list(paths.iter_application_json(root=tmp_path))
    ids = [p.parent.name for p in got]
    assert ids == ["Track", "Other"]
    assert got[0] == new_job / "application.json"


def test_iter_application_json_nested_same_leaf_is_not_collapsed(tmp_path: Path):
    """Leaf folder name is not identity — two Sony folders under different tracks stay two jobs."""
    new_sony = tmp_path / "_job-apps" / "3d-art" / "Sony"
    new_sony.mkdir(parents=True)
    (new_sony / "application.json").write_text("new", encoding="utf-8")
    old_sony = tmp_path / "storage" / "_job-listings" / "game-dev" / "Sony"
    old_sony.mkdir(parents=True)
    (old_sony / "application.json").write_text("old", encoding="utf-8")
    dup = tmp_path / "storage" / "_job-listings" / "3d-art" / "Sony"
    dup.mkdir(parents=True)
    (dup / "application.json").write_text("legacy-dup", encoding="utf-8")
    got = list(paths.iter_application_json(root=tmp_path))
    rels = [p.parent.relative_to(tmp_path).as_posix() for p in got]
    assert rels == [
        "_job-apps/3d-art/Sony",
        "storage/_job-listings/game-dev/Sony",
    ]


def test_workspace_rel_info():
    info = paths.workspace_rel_info("storage/jenni/defaults/x.html")
    assert info.bucket == "vault-renders"
    assert info.profile == "jenni"
    info = paths.workspace_rel_info("resumes/shade/defaults/x.html")
    assert info.profile == "shade"
    info = paths.workspace_rel_info("applications/3D-Visualizer/x.html")
    assert info.bucket == "_job-listings"
    info = paths.workspace_rel_info("_job-apps/3D-Visualizer/x.html")
    assert info.bucket == "_job-listings"
    info = paths.workspace_rel_info("examples/profiles/default-resume/x.html")
    assert info.bucket is None
