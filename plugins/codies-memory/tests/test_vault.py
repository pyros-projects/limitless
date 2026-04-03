"""Tests for codies_memory.vault — vault structure, validation, registry, path resolution."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from codies_memory.vault import (
    GLOBAL_DIRS,
    GLOBAL_REQUIRED_FILES,
    PROJECT_DIRS,
    PROJECT_REQUIRED_FILES,
    find_vaults,
    init_global_vault,
    init_project_vault,
    register_project_vault,
    resolve_global_vault,
    resolve_path,
    resolve_project_vault,
    validate_vault,
)


# ---------------------------------------------------------------------------
# TestResolveGlobalVault
# ---------------------------------------------------------------------------

class TestResolveGlobalVault:
    def test_exact_match(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(Path, "home", staticmethod(lambda: tmp_path))
        memory = tmp_path / ".memory"
        (memory / "Claude").mkdir(parents=True)
        result = resolve_global_vault("Claude")
        assert result == memory / "Claude"

    def test_case_insensitive_match(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(Path, "home", staticmethod(lambda: tmp_path))
        memory = tmp_path / ".memory"
        (memory / "Claude").mkdir(parents=True)
        result = resolve_global_vault("claude")
        assert result == memory / "Claude"

    def test_case_insensitive_upper(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(Path, "home", staticmethod(lambda: tmp_path))
        memory = tmp_path / ".memory"
        (memory / "Claude").mkdir(parents=True)
        result = resolve_global_vault("CLAUDE")
        assert result == memory / "Claude"

    def test_no_match_returns_exact_path(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """When no directory exists, return the exact (as-typed) path for init."""
        monkeypatch.setattr(Path, "home", staticmethod(lambda: tmp_path))
        memory = tmp_path / ".memory"
        memory.mkdir(parents=True)
        result = resolve_global_vault("newagent")
        assert result == memory / "newagent"

    def test_no_memory_dir_returns_exact_path(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """When ~/.memory doesn't exist yet, return the exact path."""
        monkeypatch.setattr(Path, "home", staticmethod(lambda: tmp_path))
        result = resolve_global_vault("claude")
        assert result == tmp_path / ".memory" / "claude"


# ---------------------------------------------------------------------------
# TestInitGlobalVault
# ---------------------------------------------------------------------------

class TestInitGlobalVault:
    def test_creates_all_dirs(self, tmp_path: Path) -> None:
        root = tmp_path / ".memory"
        init_global_vault(root)
        for d in GLOBAL_DIRS:
            assert (root / d).is_dir(), f"Missing global dir: {d}"

    def test_default_profile(self, tmp_path: Path) -> None:
        root = tmp_path / ".memory"
        init_global_vault(root)
        profile_path = root / "profile.yaml"
        assert profile_path.exists()
        data = yaml.safe_load(profile_path.read_text())
        assert data["boot_mode"] == "operational"
        assert data["write_gate_bias"] == "hold"

    def test_empty_registry(self, tmp_path: Path) -> None:
        root = tmp_path / ".memory"
        init_global_vault(root)
        registry_path = root / "registry" / "projects.yaml"
        assert registry_path.exists()
        data = yaml.safe_load(registry_path.read_text())
        assert data == {"projects": []}

    def test_seed_identity_files(self, tmp_path: Path) -> None:
        root = tmp_path / ".memory"
        init_global_vault(root)
        for name in ("self.md", "user.md", "rules.md"):
            f = root / "identity" / name
            assert f.exists(), f"Missing identity file: {name}"
            content = f.read_text()
            assert "---" in content, f"{name} should have frontmatter"

    def test_idempotent_on_existing_vault(self, tmp_path: Path) -> None:
        root = tmp_path / ".memory"
        init_global_vault(root)

        # Write custom content to profile and registry to check they are NOT clobbered
        profile_path = root / "profile.yaml"
        registry_path = root / "registry" / "projects.yaml"
        profile_path.write_text("boot_mode: custom\nwrite_gate_bias: allow\n")
        registry_path.write_text("projects:\n  - slug: existing\n")

        init_global_vault(root)  # second call

        profile_data = yaml.safe_load(profile_path.read_text())
        assert profile_data["boot_mode"] == "custom", "profile.yaml must not be overwritten"

        registry_data = yaml.safe_load(registry_path.read_text())
        assert len(registry_data["projects"]) == 1, "registry must not be reset"


# ---------------------------------------------------------------------------
# TestInitProjectVault
# ---------------------------------------------------------------------------

class TestInitProjectVault:
    def test_creates_all_dirs(self, tmp_path: Path) -> None:
        global_vault = tmp_path / "global"
        init_global_vault(global_vault)
        working_dir = tmp_path / "myproject"
        working_dir.mkdir()

        vault = init_project_vault(global_vault=global_vault, slug="myproject", working_dir=working_dir)
        for d in PROJECT_DIRS:
            assert (vault / d).is_dir(), f"Missing project dir: {d}"

    def test_default_project_profile(self, tmp_path: Path) -> None:
        global_vault = tmp_path / "global"
        init_global_vault(global_vault)
        working_dir = tmp_path / "myproject"
        working_dir.mkdir()

        vault = init_project_vault(global_vault=global_vault, slug="myproject", working_dir=working_dir)
        profile_path = vault / "profile.yaml"
        assert profile_path.exists()
        data = yaml.safe_load(profile_path.read_text())
        assert "project_name" in data
        assert data["project_name"] == "myproject"

    def test_auto_registers_when_flag_set(self, tmp_path: Path) -> None:
        global_vault = tmp_path / "global"
        init_global_vault(global_vault)
        working_dir = tmp_path / "myproject"
        working_dir.mkdir()

        init_project_vault(global_vault=global_vault, slug="myproject", working_dir=working_dir, register=True)

        registry_path = global_vault / "registry" / "projects.yaml"
        data = yaml.safe_load(registry_path.read_text())
        slugs = [p["slug"] for p in data["projects"]]
        assert "myproject" in slugs

    def test_does_not_register_when_flag_false(self, tmp_path: Path) -> None:
        global_vault = tmp_path / "global"
        init_global_vault(global_vault)
        working_dir = tmp_path / "myproject"
        working_dir.mkdir()

        init_project_vault(global_vault=global_vault, slug="myproject", working_dir=working_dir, register=False)

        registry_path = global_vault / "registry" / "projects.yaml"
        data = yaml.safe_load(registry_path.read_text())
        assert data["projects"] == []


# ---------------------------------------------------------------------------
# TestRegisterProjectVault
# ---------------------------------------------------------------------------

class TestRegisterProjectVault:
    def test_adds_project_to_registry(self, tmp_global_vault: Path) -> None:
        register_project_vault(
            global_vault=tmp_global_vault,
            slug="myproject",
            working_dir="/home/user/myproject",
            metadata={"description": "A test project"},
        )
        registry_path = tmp_global_vault / "registry" / "projects.yaml"
        data = yaml.safe_load(registry_path.read_text())
        slugs = [p["slug"] for p in data["projects"]]
        assert "myproject" in slugs
        entry = data["projects"][0]
        assert entry["working_dir"] == "/home/user/myproject"

    def test_updates_existing_entry(self, tmp_global_vault: Path) -> None:
        register_project_vault(
            global_vault=tmp_global_vault,
            slug="myproject",
            working_dir="/home/user/myproject",
            metadata={"description": "original"},
        )
        register_project_vault(
            global_vault=tmp_global_vault,
            slug="myproject",
            working_dir="/home/user/myproject",
            metadata={"description": "updated"},
        )
        registry_path = tmp_global_vault / "registry" / "projects.yaml"
        data = yaml.safe_load(registry_path.read_text())
        entries = [p for p in data["projects"] if p["slug"] == "myproject"]
        assert len(entries) == 1, "Must not duplicate entries for the same slug"
        assert entries[0]["metadata"]["description"] == "updated"

    def test_archives_stale_entry(self, tmp_global_vault: Path) -> None:
        register_project_vault(
            global_vault=tmp_global_vault,
            slug="stale-proj",
            working_dir="/home/user/old-path",
            metadata={},
        )
        register_project_vault(
            global_vault=tmp_global_vault,
            slug="stale-proj",
            working_dir="/home/user/old-path",
            metadata={},
            status="archived",
        )
        registry_path = tmp_global_vault / "registry" / "projects.yaml"
        data = yaml.safe_load(registry_path.read_text())
        entry = next(p for p in data["projects"] if p["slug"] == "stale-proj")
        assert entry["status"] == "archived"

    def test_stores_git_remote(self, tmp_global_vault: Path) -> None:
        register_project_vault(
            global_vault=tmp_global_vault,
            slug="remote-proj",
            working_dir="/home/user/remote-proj",
            metadata={},
            git_remote="git@github.com:user/remote-proj.git",
        )
        registry_path = tmp_global_vault / "registry" / "projects.yaml"
        data = yaml.safe_load(registry_path.read_text())
        entry = next(p for p in data["projects"] if p["slug"] == "remote-proj")
        assert entry["git_remote"] == "git@github.com:user/remote-proj.git"

    def test_omits_git_remote_when_none(self, tmp_global_vault: Path) -> None:
        register_project_vault(
            global_vault=tmp_global_vault,
            slug="no-remote",
            working_dir="/home/user/no-remote",
            metadata={},
        )
        registry_path = tmp_global_vault / "registry" / "projects.yaml"
        data = yaml.safe_load(registry_path.read_text())
        entry = next(p for p in data["projects"] if p["slug"] == "no-remote")
        assert "git_remote" not in entry


# ---------------------------------------------------------------------------
# TestValidateVault
# ---------------------------------------------------------------------------

class TestValidateVault:
    def test_valid_global_passes(self, tmp_global_vault: Path) -> None:
        result = validate_vault(tmp_global_vault, vault_type="global")
        assert result.is_valid
        assert result.missing == []

    def test_missing_dir_fails(self, tmp_path: Path) -> None:
        # An empty directory has nothing in it
        root = tmp_path / ".memory"
        root.mkdir()
        result = validate_vault(root, vault_type="global")
        assert not result.is_valid
        assert len(result.missing) > 0

    def test_valid_global_no_missing_files(self, tmp_global_vault: Path) -> None:
        result = validate_vault(tmp_global_vault, vault_type="global")
        assert result.missing_files == []

    def test_valid_project_passes(self, tmp_project_vault: Path) -> None:
        result = validate_vault(tmp_project_vault, vault_type="project")
        assert result.is_valid
        assert result.missing == []
        assert result.missing_files == []

    def test_validate_global_missing_profile(self, tmp_path: Path) -> None:
        vault = tmp_path / "vault"
        init_global_vault(vault)
        (vault / "profile.yaml").unlink()
        result = validate_vault(vault, vault_type="global")
        assert not result.is_valid
        assert "profile.yaml" in result.missing_files

    def test_validate_global_missing_registry(self, tmp_path: Path) -> None:
        vault = tmp_path / "vault"
        init_global_vault(vault)
        (vault / "registry" / "projects.yaml").unlink()
        result = validate_vault(vault, vault_type="global")
        assert not result.is_valid
        assert "registry/projects.yaml" in result.missing_files

    def test_validate_global_missing_identity_self(self, tmp_path: Path) -> None:
        vault = tmp_path / "vault"
        init_global_vault(vault)
        (vault / "identity" / "self.md").unlink()
        result = validate_vault(vault, vault_type="global")
        assert not result.is_valid
        assert "identity/self.md" in result.missing_files

    def test_validate_project_missing_profile(self, tmp_path: Path) -> None:
        global_vault = tmp_path / "global"
        init_global_vault(global_vault)
        working_dir = tmp_path / "proj"
        working_dir.mkdir()
        vault = init_project_vault(global_vault=global_vault, working_dir=working_dir)
        (vault / "profile.yaml").unlink()
        result = validate_vault(vault, vault_type="project")
        assert not result.is_valid


# ---------------------------------------------------------------------------
# TestResolvePath
# ---------------------------------------------------------------------------

class TestResolvePath:
    def test_thread_in_project(self, tmp_project_vault: Path) -> None:
        path = resolve_path(tmp_project_vault, "thread", "project")
        assert path == tmp_project_vault / "threads"

    def test_lesson_in_global(self, tmp_global_vault: Path) -> None:
        path = resolve_path(tmp_global_vault, "lesson", "global")
        assert path == tmp_global_vault / "procedural/lessons"

    def test_reflection_global(self, tmp_global_vault: Path) -> None:
        path = resolve_path(tmp_global_vault, "reflection", "global")
        assert path == tmp_global_vault / "reflections"

    def test_inbox_in_project(self, tmp_project_vault: Path) -> None:
        path = resolve_path(tmp_project_vault, "inbox", "project")
        assert path == tmp_project_vault / "inbox"

    def test_session_in_project(self, tmp_project_vault: Path) -> None:
        path = resolve_path(tmp_project_vault, "session", "project")
        assert path == tmp_project_vault / "sessions"

    def test_unknown_type_raises_value_error(self, tmp_project_vault: Path) -> None:
        with pytest.raises(ValueError):
            resolve_path(tmp_project_vault, "nonexistent", "project")


# ---------------------------------------------------------------------------
# TestFindVaults
# ---------------------------------------------------------------------------

class TestFindVaults:
    def _add_project(
        self,
        global_vault: Path,
        slug: str,
        working_dir: str,
        status: str = "active",
    ) -> None:
        register_project_vault(
            global_vault=global_vault,
            slug=slug,
            working_dir=working_dir,
            metadata={},
            status=status,
        )

    def test_returns_active_projects(self, tmp_global_vault: Path) -> None:
        self._add_project(tmp_global_vault, "proj-a", "/home/user/proj-a", status="active")
        self._add_project(tmp_global_vault, "proj-b", "/home/user/proj-b", status="active")
        results = find_vaults(tmp_global_vault)
        slugs = [r["slug"] for r in results]
        assert "proj-a" in slugs
        assert "proj-b" in slugs

    def test_excludes_archived_by_default(self, tmp_global_vault: Path) -> None:
        self._add_project(tmp_global_vault, "active-proj", "/home/user/active", status="active")
        self._add_project(tmp_global_vault, "archived-proj", "/home/user/archived", status="archived")
        results = find_vaults(tmp_global_vault, include_archived=False)
        slugs = [r["slug"] for r in results]
        assert "active-proj" in slugs
        assert "archived-proj" not in slugs

    def test_includes_archived_when_requested(self, tmp_global_vault: Path) -> None:
        self._add_project(tmp_global_vault, "active-proj", "/home/user/active", status="active")
        self._add_project(tmp_global_vault, "archived-proj", "/home/user/archived", status="archived")
        results = find_vaults(tmp_global_vault, include_archived=True)
        slugs = [r["slug"] for r in results]
        assert "active-proj" in slugs
        assert "archived-proj" in slugs

    def test_returns_computed_vault_path(self, tmp_global_vault: Path) -> None:
        self._add_project(tmp_global_vault, "proj-x", "/home/user/proj-x")
        results = find_vaults(tmp_global_vault)
        entry = results[0]
        assert entry["vault_path"] == str(tmp_global_vault / "projects" / "proj-x")
        assert entry["working_dir"] == "/home/user/proj-x"


# ---------------------------------------------------------------------------
# TestInitProjectVaultV2 — new behaviour for project-external storage
# ---------------------------------------------------------------------------

class TestInitProjectVaultV2:
    def test_init_project_vault_v2(self, tmp_path: Path) -> None:
        """Vault created at global/projects/slug/, marker file exists in
        working_dir, registered in registry."""
        global_vault = tmp_path / "global"
        init_global_vault(global_vault)
        working_dir = tmp_path / "my-project"
        working_dir.mkdir()

        vault = init_project_vault(
            global_vault=global_vault,
            slug="my-project",
            working_dir=working_dir,
        )

        # Vault lives under global/projects/slug/
        assert vault == global_vault / "projects" / "my-project"
        assert (vault / "inbox").is_dir()
        assert (vault / "profile.yaml").exists()

        # Marker file created in working dir
        marker = working_dir / ".codies-memory"
        assert marker.exists()
        assert marker.read_text().strip() == "my-project"

        # Registered in global registry
        registry = yaml.safe_load(
            (global_vault / "registry" / "projects.yaml").read_text()
        )
        slugs = [p["slug"] for p in registry["projects"]]
        assert "my-project" in slugs
        entry = registry["projects"][0]
        assert entry["working_dir"] == str(working_dir)

    def test_init_project_vault_v2_default_slug(self, tmp_path: Path) -> None:
        """Slug defaults to working_dir.name."""
        global_vault = tmp_path / "global"
        init_global_vault(global_vault)
        working_dir = tmp_path / "cool-app"
        working_dir.mkdir()

        vault = init_project_vault(
            global_vault=global_vault,
            working_dir=working_dir,
        )
        # Slug defaults to working dir name
        assert vault == global_vault / "projects" / "cool-app"

        # Marker should contain the default slug
        marker = working_dir / ".codies-memory"
        assert marker.read_text().strip() == "cool-app"

    def test_init_project_vault_v2_idempotent(self, tmp_path: Path) -> None:
        """Re-running does not clobber existing profile or duplicate registry."""
        global_vault = tmp_path / "global"
        init_global_vault(global_vault)
        working_dir = tmp_path / "my-project"
        working_dir.mkdir()

        vault = init_project_vault(
            global_vault=global_vault,
            slug="my-project",
            working_dir=working_dir,
        )

        # Write custom content to profile to verify it is not overwritten
        profile_path = vault / "profile.yaml"
        profile_path.write_text("project_name: my-project\ncustom_key: keep\n")

        # Run again
        vault2 = init_project_vault(
            global_vault=global_vault,
            slug="my-project",
            working_dir=working_dir,
        )

        assert vault2 == vault

        # Profile must not be overwritten (custom_key preserved)
        profile_data = yaml.safe_load(profile_path.read_text())
        assert profile_data.get("custom_key") == "keep", "profile.yaml must not be overwritten"

        # Registry must not have duplicate entries
        registry = yaml.safe_load(
            (global_vault / "registry" / "projects.yaml").read_text()
        )
        entries = [p for p in registry["projects"] if p["slug"] == "my-project"]
        assert len(entries) == 1, "Must not duplicate registry entries"


# ---------------------------------------------------------------------------
# TestResolveProjectVault — three-tier resolution
# ---------------------------------------------------------------------------

class TestResolveProjectVault:
    def test_resolve_via_marker(self, tmp_path: Path) -> None:
        """Tier 1: resolve via .codies-memory marker file in working_dir."""
        global_vault = tmp_path / "global"
        init_global_vault(global_vault)
        working_dir = tmp_path / "my-project"
        working_dir.mkdir()

        vault = init_project_vault(
            global_vault=global_vault, slug="my-project", working_dir=working_dir,
        )

        result = resolve_project_vault(global_vault, working_dir)
        assert result == vault
        assert result == global_vault / "projects" / "my-project"

    def test_resolve_via_registry_working_dir(self, tmp_path: Path) -> None:
        """Tier 2: marker deleted, fall back to registry working_dir match."""
        global_vault = tmp_path / "global"
        init_global_vault(global_vault)
        working_dir = tmp_path / "my-project"
        working_dir.mkdir()

        vault = init_project_vault(
            global_vault=global_vault, slug="my-project", working_dir=working_dir,
        )

        # Remove the marker file to force tier-2 lookup
        marker = working_dir / ".codies-memory"
        marker.unlink()
        assert not marker.exists()

        result = resolve_project_vault(global_vault, working_dir)
        assert result == vault

    def test_resolve_via_git_remote(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Tier 3: marker deleted, working_dir changed, fall back to git remote match."""
        global_vault = tmp_path / "global"
        init_global_vault(global_vault)
        original_dir = tmp_path / "original"
        original_dir.mkdir()

        init_project_vault(
            global_vault=global_vault, slug="remote-proj", working_dir=original_dir,
        )

        # Simulate a different checkout location with the same remote
        new_dir = tmp_path / "new-checkout"
        new_dir.mkdir()
        # No marker file at new_dir

        # Mock _get_git_remote so it returns the same URL that was stored
        # First, read what was stored (init_project_vault called _get_git_remote
        # on original_dir, which likely returned None for a non-git dir)
        registry = yaml.safe_load(
            (global_vault / "registry" / "projects.yaml").read_text()
        )
        entry = registry["projects"][0]
        # Manually set a git_remote so we can test tier 3
        entry["git_remote"] = "git@github.com:user/remote-proj.git"
        (global_vault / "registry" / "projects.yaml").write_text(
            yaml.dump(registry, default_flow_style=False, allow_unicode=True)
        )

        monkeypatch.setattr(
            "codies_memory.vault._get_git_remote",
            lambda _wd: "git@github.com:user/remote-proj.git",
        )

        result = resolve_project_vault(global_vault, new_dir)
        assert result == global_vault / "projects" / "remote-proj"

    def test_resolve_unregistered_returns_none(self, tmp_path: Path) -> None:
        """Unknown working_dir with no marker, no registry match → None."""
        global_vault = tmp_path / "global"
        init_global_vault(global_vault)
        unknown_dir = tmp_path / "unknown-project"
        unknown_dir.mkdir()

        result = resolve_project_vault(global_vault, unknown_dir)
        assert result is None

    def test_resolve_lazily_updates_registry(self, tmp_path: Path) -> None:
        """Resolve from a new path with the marker → vault found AND registry updated."""
        global_vault = tmp_path / "global"
        init_global_vault(global_vault)
        original_dir = tmp_path / "path-a"
        original_dir.mkdir()

        init_project_vault(
            global_vault=global_vault, slug="mobile-proj", working_dir=original_dir,
        )

        # Verify original registry entry
        registry = yaml.safe_load(
            (global_vault / "registry" / "projects.yaml").read_text()
        )
        entry = next(p for p in registry["projects"] if p["slug"] == "mobile-proj")
        assert entry["working_dir"] == str(original_dir)

        # Simulate moving the project to a new directory with the same marker
        new_dir = tmp_path / "path-b"
        new_dir.mkdir()
        marker = new_dir / ".codies-memory"
        marker.write_text("mobile-proj\n")

        result = resolve_project_vault(global_vault, new_dir)
        assert result == global_vault / "projects" / "mobile-proj"

        # Registry should now reflect the new working_dir
        registry = yaml.safe_load(
            (global_vault / "registry" / "projects.yaml").read_text()
        )
        entry = next(p for p in registry["projects"] if p["slug"] == "mobile-proj")
        assert entry["working_dir"] == str(new_dir)
