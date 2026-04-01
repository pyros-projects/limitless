"""Tests for the v2 agent-namespaced CLI commands."""

from __future__ import annotations

import argparse
import datetime
from pathlib import Path

import pytest

import json

from codies_memory.cli import (
    cmd_init, cmd_boot, cmd_status, cmd_capture, cmd_create, cmd_list,
    cmd_promote, cmd_validate, _resolve_agent,
)
from codies_memory.vault import GLOBAL_DIRS, PROJECT_DIRS


# ---------------------------------------------------------------------------
# _resolve_agent
# ---------------------------------------------------------------------------

class TestResolveAgent:

    def test_from_flag(self):
        ns = argparse.Namespace(agent="claude")
        assert _resolve_agent(ns) == "claude"

    def test_from_env(self, monkeypatch):
        monkeypatch.setenv("CODIES_MEMORY_AGENT", "opus")
        ns = argparse.Namespace(agent=None)
        assert _resolve_agent(ns) == "opus"

    def test_flag_overrides_env(self, monkeypatch):
        monkeypatch.setenv("CODIES_MEMORY_AGENT", "opus")
        ns = argparse.Namespace(agent="claude")
        assert _resolve_agent(ns) == "claude"

    def test_missing_exits(self, monkeypatch):
        monkeypatch.delenv("CODIES_MEMORY_AGENT", raising=False)
        ns = argparse.Namespace(agent=None)
        with pytest.raises(SystemExit):
            _resolve_agent(ns)


# ---------------------------------------------------------------------------
# cmd_init — global vault
# ---------------------------------------------------------------------------

class TestCmdInitGlobal:

    def test_creates_global_dirs(self, tmp_path, monkeypatch, capsys):
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        monkeypatch.setenv("HOME", str(fake_home))
        # resolve_global_vault uses Path.home() which reads HOME
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: fake_home))

        ns = argparse.Namespace(agent="claude", type="global")
        cmd_init(ns)

        global_vault = fake_home / ".memory" / "claude"
        assert global_vault.is_dir()
        for d in GLOBAL_DIRS:
            assert (global_vault / d).is_dir(), f"missing dir: {d}"
        # Seed files
        assert (global_vault / "profile.yaml").is_file()
        assert (global_vault / "registry" / "projects.yaml").is_file()
        assert (global_vault / "identity" / "self.md").is_file()

        out = capsys.readouterr().out
        assert "Initialized global vault" in out


# ---------------------------------------------------------------------------
# cmd_init — project vault
# ---------------------------------------------------------------------------

class TestCmdInitProject:

    def test_creates_project_vault(self, tmp_path, monkeypatch, capsys):
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: fake_home))

        working_dir = tmp_path / "myapp"
        working_dir.mkdir()

        # First init global so registry exists
        ns_global = argparse.Namespace(agent="claude", type="global")
        cmd_init(ns_global)

        # Now init project
        ns_project = argparse.Namespace(
            agent="claude",
            type="project",
            slug="myapp",
            working_dir=str(working_dir),
        )
        cmd_init(ns_project)

        project_vault = fake_home / ".memory" / "claude" / "projects" / "myapp"
        assert project_vault.is_dir()
        for d in PROJECT_DIRS:
            assert (project_vault / d).is_dir(), f"missing dir: {d}"

        # Marker file should be written in working_dir
        marker = working_dir / ".codies-memory"
        assert marker.is_file()
        assert marker.read_text().strip() == "myapp"

        # Registry should contain the project
        import yaml
        registry = fake_home / ".memory" / "claude" / "registry" / "projects.yaml"
        data = yaml.safe_load(registry.read_text())
        slugs = [p["slug"] for p in data.get("projects", [])]
        assert "myapp" in slugs

        out = capsys.readouterr().out
        assert "Initialized project vault" in out


# ---------------------------------------------------------------------------
# cmd_boot — with agent env var
# ---------------------------------------------------------------------------

class TestCmdBoot:

    def test_global_only_boot(self, tmp_path, monkeypatch, capsys):
        """Boot with no project vault produces global-only output + warning."""
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: fake_home))
        monkeypatch.setenv("CODIES_MEMORY_AGENT", "claude")

        # Init global vault
        ns_global = argparse.Namespace(agent="claude", type="global")
        cmd_init(ns_global)

        # cwd is some random dir with no project
        working_dir = tmp_path / "unrelated"
        working_dir.mkdir()
        monkeypatch.chdir(working_dir)

        ns_boot = argparse.Namespace(agent=None, branch="main", budget=4000)
        cmd_boot(ns_boot)

        captured = capsys.readouterr()
        assert "Global Packet" in captured.out
        assert "no project vault found" in captured.err

    def test_boot_with_project(self, tmp_path, monkeypatch, capsys):
        """Boot with a project vault produces both packets."""
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: fake_home))
        monkeypatch.setenv("CODIES_MEMORY_AGENT", "claude")

        working_dir = tmp_path / "myapp"
        working_dir.mkdir()

        # Init global + project
        cmd_init(argparse.Namespace(agent="claude", type="global"))
        cmd_init(argparse.Namespace(
            agent="claude", type="project", slug="myapp",
            working_dir=str(working_dir),
        ))

        monkeypatch.chdir(working_dir)

        ns_boot = argparse.Namespace(agent=None, branch="main", budget=4000)
        cmd_boot(ns_boot)

        captured = capsys.readouterr()
        assert "Global Packet" in captured.out
        assert "Project Packet" in captured.out
        # No warning when project vault is found
        assert "no project vault found" not in captured.err


# ---------------------------------------------------------------------------
# cmd_status — active count
# ---------------------------------------------------------------------------

class TestCmdStatus:

    def _setup_vault_with_inbox(self, tmp_path, monkeypatch):
        """Helper: set up global + project vault and add inbox items."""
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: fake_home))
        monkeypatch.setenv("CODIES_MEMORY_AGENT", "claude")

        working_dir = tmp_path / "myapp"
        working_dir.mkdir()

        cmd_init(argparse.Namespace(agent="claude", type="global"))
        cmd_init(argparse.Namespace(
            agent="claude", type="project", slug="myapp",
            working_dir=str(working_dir),
        ))

        monkeypatch.chdir(working_dir)

        project_vault = fake_home / ".memory" / "claude" / "projects" / "myapp"
        return project_vault, working_dir

    def test_clean_inbox(self, tmp_path, monkeypatch, capsys):
        self._setup_vault_with_inbox(tmp_path, monkeypatch)

        ns = argparse.Namespace(agent=None, all=False)
        cmd_status(ns)

        out = capsys.readouterr().out
        assert "Active: 0" in out
        assert "Inbox is clean." in out

    def test_active_count(self, tmp_path, monkeypatch, capsys):
        project_vault, _ = self._setup_vault_with_inbox(tmp_path, monkeypatch)

        # Add an inbox item (recent, so "active" but not aging/stale)
        today = datetime.date.today().isoformat()
        inbox_dir = project_vault / "inbox"
        inbox_dir.mkdir(parents=True, exist_ok=True)
        (inbox_dir / "IX-0001-test.md").write_text(
            f"---\nid: IX-0001\ntitle: Test item\ntype: inbox\n"
            f"status: active\ntrust: speculative\nscope: project\n"
            f"created: \"{today}\"\nupdated: \"{today}\"\n---\n\nSome note.\n"
        )

        ns = argparse.Namespace(agent=None, all=False)
        cmd_status(ns)

        out = capsys.readouterr().out
        assert "Active: 1" in out

    def test_all_flag_lists_items(self, tmp_path, monkeypatch, capsys):
        project_vault, _ = self._setup_vault_with_inbox(tmp_path, monkeypatch)

        today = datetime.date.today().isoformat()
        inbox_dir = project_vault / "inbox"
        inbox_dir.mkdir(parents=True, exist_ok=True)
        (inbox_dir / "IX-0001-test.md").write_text(
            f"---\nid: IX-0001\ntitle: My task\ntype: inbox\n"
            f"status: active\ntrust: speculative\nscope: project\n"
            f"created: \"{today}\"\nupdated: \"{today}\"\n---\n\nContent.\n"
        )

        ns = argparse.Namespace(agent=None, all=True)
        cmd_status(ns)

        out = capsys.readouterr().out
        assert "Active: 1" in out
        assert "My task" in out

    def test_no_project_vault_exits(self, tmp_path, monkeypatch):
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: fake_home))
        monkeypatch.setenv("CODIES_MEMORY_AGENT", "claude")

        cmd_init(argparse.Namespace(agent="claude", type="global"))

        unrelated = tmp_path / "nowhere"
        unrelated.mkdir()
        monkeypatch.chdir(unrelated)

        ns = argparse.Namespace(agent=None, all=False)
        with pytest.raises(SystemExit):
            cmd_status(ns)


# ---------------------------------------------------------------------------
# Shared vault setup helper
# ---------------------------------------------------------------------------

def _setup_project(tmp_path, monkeypatch):
    """Create global + project vault; chdir into working_dir. Returns project_vault."""
    fake_home = tmp_path / "home"
    fake_home.mkdir()
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: fake_home))
    monkeypatch.setenv("CODIES_MEMORY_AGENT", "claude")

    working_dir = tmp_path / "myapp"
    working_dir.mkdir()

    cmd_init(argparse.Namespace(agent="claude", type="global"))
    cmd_init(argparse.Namespace(
        agent="claude", type="project", slug="myapp",
        working_dir=str(working_dir),
    ))

    monkeypatch.chdir(working_dir)
    return fake_home / ".memory" / "claude" / "projects" / "myapp"


# ---------------------------------------------------------------------------
# cmd_capture
# ---------------------------------------------------------------------------

class TestCmdCapture:

    def test_cmd_capture(self, tmp_path, monkeypatch, capsys):
        project_vault = _setup_project(tmp_path, monkeypatch)
        capsys.readouterr()  # discard init output

        ns = argparse.Namespace(
            agent=None,
            content="The API returns 404",
            source="testing",
            gate="allow",
            working_dir=None,
        )
        cmd_capture(ns)

        out = capsys.readouterr().out.strip()
        assert out.startswith("IN-")

        # Verify record exists in inbox
        inbox_dir = project_vault / "inbox"
        files = list(inbox_dir.glob("*.md"))
        assert len(files) == 1
        assert "The API returns 404" in files[0].read_text()

    def test_cmd_capture_default_gate(self, tmp_path, monkeypatch, capsys):
        """When --gate is omitted, profile's write_gate_bias is used."""
        project_vault = _setup_project(tmp_path, monkeypatch)
        capsys.readouterr()  # discard init output

        ns = argparse.Namespace(
            agent=None,
            content="Something to remember",
            source="chat",
            gate=None,
            working_dir=None,
        )
        cmd_capture(ns)

        out = capsys.readouterr().out.strip()
        assert out.startswith("IN-")

        # The default profile has write_gate_bias=hold
        inbox_dir = project_vault / "inbox"
        files = list(inbox_dir.glob("*.md"))
        assert len(files) == 1
        content = files[0].read_text()
        assert "gate: hold" in content


# ---------------------------------------------------------------------------
# cmd_create
# ---------------------------------------------------------------------------

class TestCmdCreate:

    def test_cmd_create_lesson(self, tmp_path, monkeypatch, capsys):
        project_vault = _setup_project(tmp_path, monkeypatch)
        capsys.readouterr()

        ns = argparse.Namespace(
            agent=None,
            type="lesson",
            title="Check YAML tabs",
            body="YAML rejects tabs; always use spaces.",
            body_file=None,
            scope="project",
            trust="working",
            field=None,
            working_dir=None,
        )
        cmd_create(ns)

        out = capsys.readouterr().out.strip()
        assert out.startswith("LS-")

        lessons_dir = project_vault / "lessons"
        files = list(lessons_dir.glob("*.md"))
        assert len(files) == 1
        content = files[0].read_text()
        assert "Check YAML tabs" in content
        assert "YAML rejects tabs" in content

    def test_cmd_create_with_body_file(self, tmp_path, monkeypatch, capsys):
        project_vault = _setup_project(tmp_path, monkeypatch)
        capsys.readouterr()

        body_file = tmp_path / "body.md"
        body_file.write_text("Body from file.")

        ns = argparse.Namespace(
            agent=None,
            type="thread",
            title="File-sourced thread",
            body=None,
            body_file=str(body_file),
            scope="project",
            trust="working",
            field=None,
            working_dir=None,
        )
        cmd_create(ns)

        out = capsys.readouterr().out.strip()
        assert out.startswith("TH-")

        threads_dir = project_vault / "threads"
        files = list(threads_dir.glob("*.md"))
        assert len(files) == 1
        assert "Body from file." in files[0].read_text()

    def test_cmd_create_with_extra_fields(self, tmp_path, monkeypatch, capsys):
        _setup_project(tmp_path, monkeypatch)
        capsys.readouterr()

        ns = argparse.Namespace(
            agent=None,
            type="decision",
            title="Use pytest",
            body="We decided to use pytest.",
            body_file=None,
            scope="project",
            trust="working",
            field=["rationale=fast and simple"],
            working_dir=None,
        )
        cmd_create(ns)

        out = capsys.readouterr().out.strip()
        assert out.startswith("DC-")

    def test_cmd_create_reflection_auto_routes_to_global(self, tmp_path, monkeypatch, capsys):
        """create reflection without --scope global should succeed via auto-routing."""
        _setup_project(tmp_path, monkeypatch)
        capsys.readouterr()

        ns = argparse.Namespace(
            agent=None,
            type="reflection",
            title="On persistence",
            body="Memory is what makes us continuous.",
            body_file=None,
            scope="project",  # default — should be auto-routed to global
            trust="working",
            field=None,
            working_dir=None,
        )
        cmd_create(ns)

        out = capsys.readouterr().out.strip()
        assert out.startswith("RF-")

        # Verify it landed in the global vault's reflections dir, not project
        global_vault = tmp_path / "home" / ".memory" / "claude"
        reflections_dir = global_vault / "reflections"
        files = list(reflections_dir.glob("*.md"))
        assert len(files) == 1
        content = files[0].read_text()
        assert "On persistence" in content


# ---------------------------------------------------------------------------
# cmd_validate
# ---------------------------------------------------------------------------

class TestCmdValidate:

    def test_validate_project_with_working_dir(self, tmp_path, monkeypatch, capsys):
        """validate --type project --working-dir works when cwd is elsewhere."""
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: fake_home))
        monkeypatch.setenv("CODIES_MEMORY_AGENT", "claude")

        working_dir = tmp_path / "myapp"
        working_dir.mkdir()

        cmd_init(argparse.Namespace(agent="claude", type="global"))
        cmd_init(argparse.Namespace(
            agent="claude", type="project", slug="myapp",
            working_dir=str(working_dir),
        ))
        capsys.readouterr()

        # chdir somewhere unrelated
        elsewhere = tmp_path / "elsewhere"
        elsewhere.mkdir()
        monkeypatch.chdir(elsewhere)

        ns = argparse.Namespace(
            agent=None,
            type="project",
            working_dir=str(working_dir),
        )
        cmd_validate(ns)

        out = capsys.readouterr().out
        assert "is valid" in out


# ---------------------------------------------------------------------------
# cmd_list
# ---------------------------------------------------------------------------

class TestCmdList:

    def test_cmd_list_inbox(self, tmp_path, monkeypatch, capsys):
        _setup_project(tmp_path, monkeypatch)
        capsys.readouterr()

        # Capture two items
        for text in ["First item", "Second item"]:
            cmd_capture(argparse.Namespace(
                agent=None, content=text, source="test",
                gate="allow", working_dir=None,
            ))
        capsys.readouterr()

        # List inbox
        cmd_list(argparse.Namespace(
            agent=None, type="inbox", scope="project",
            status=None, trust=None, format="table",
            working_dir=None,
        ))

        out = capsys.readouterr().out
        assert "ID" in out  # header
        assert "IN-" in out
        # Should see both items
        lines = [l for l in out.strip().split("\n") if l.startswith("IN-")]
        assert len(lines) == 2

    def test_cmd_list_json_format(self, tmp_path, monkeypatch, capsys):
        _setup_project(tmp_path, monkeypatch)
        capsys.readouterr()

        cmd_capture(argparse.Namespace(
            agent=None, content="JSON test item", source="test",
            gate="allow", working_dir=None,
        ))
        capsys.readouterr()

        cmd_list(argparse.Namespace(
            agent=None, type="inbox", scope="project",
            status=None, trust=None, format="json",
            working_dir=None,
        ))

        out = capsys.readouterr().out
        data = json.loads(out)
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["type"] == "inbox"

    def test_cmd_list_paths_format(self, tmp_path, monkeypatch, capsys):
        _setup_project(tmp_path, monkeypatch)
        capsys.readouterr()

        cmd_capture(argparse.Namespace(
            agent=None, content="Paths test", source="test",
            gate="allow", working_dir=None,
        ))
        capsys.readouterr()

        cmd_list(argparse.Namespace(
            agent=None, type="inbox", scope="project",
            status=None, trust=None, format="paths",
            working_dir=None,
        ))

        out = capsys.readouterr().out.strip()
        assert out.endswith(".md")

    def test_cmd_list_with_status_filter(self, tmp_path, monkeypatch, capsys):
        _setup_project(tmp_path, monkeypatch)
        capsys.readouterr()

        cmd_capture(argparse.Namespace(
            agent=None, content="Active item", source="test",
            gate="allow", working_dir=None,
        ))
        capsys.readouterr()

        # Filter for status=archived should return nothing
        cmd_list(argparse.Namespace(
            agent=None, type="inbox", scope="project",
            status="archived", trust=None, format="table",
            working_dir=None,
        ))

        out = capsys.readouterr().out
        assert "No records found." in out

    def test_cmd_list_empty(self, tmp_path, monkeypatch, capsys):
        _setup_project(tmp_path, monkeypatch)
        capsys.readouterr()

        cmd_list(argparse.Namespace(
            agent=None, type="inbox", scope="project",
            status=None, trust=None, format="table",
            working_dir=None,
        ))

        out = capsys.readouterr().out
        assert "No records found." in out


# ---------------------------------------------------------------------------
# cmd_promote
# ---------------------------------------------------------------------------

class TestCmdPromote:

    def test_cmd_promote_to_thread(self, tmp_path, monkeypatch, capsys):
        project_vault = _setup_project(tmp_path, monkeypatch)
        capsys.readouterr()

        # Capture an inbox item first
        cmd_capture(argparse.Namespace(
            agent=None, content="Investigate the 404 bug",
            source="testing", gate="allow", working_dir=None,
        ))
        capsys.readouterr()

        # Find the inbox file
        inbox_dir = project_vault / "inbox"
        inbox_files = list(inbox_dir.glob("*.md"))
        assert len(inbox_files) == 1
        source_path = inbox_files[0]

        # Promote to thread
        cmd_promote(argparse.Namespace(
            agent=None, source=str(source_path), to="thread",
            to_global=False, working_dir=None,
        ))

        out = capsys.readouterr().out.strip()
        assert out.startswith("TH-")

        # Thread should exist
        threads_dir = project_vault / "threads"
        thread_files = list(threads_dir.glob("*.md"))
        assert len(thread_files) == 1
        content = thread_files[0].read_text()
        assert "Investigate the 404 bug" in content

        # Source should be archived
        source_content = source_path.read_text()
        assert "archived" in source_content

    def test_cmd_promote_to_global(self, tmp_path, monkeypatch, capsys):
        project_vault = _setup_project(tmp_path, monkeypatch)
        capsys.readouterr()

        # Create a lesson first (promote_to_global requires type=lesson)
        cmd_create(argparse.Namespace(
            agent=None, type="lesson", title="Global lesson",
            body="A lesson worth sharing globally.",
            body_file=None, scope="project", trust="working",
            field=None, working_dir=None,
        ))
        capsys.readouterr()

        # Find the lesson file
        lessons_dir = project_vault / "lessons"
        lesson_files = list(lessons_dir.glob("*.md"))
        assert len(lesson_files) == 1
        source_path = lesson_files[0]

        # Promote to global
        cmd_promote(argparse.Namespace(
            agent=None, source=str(source_path),
            to=None, to_global=True, working_dir=None,
        ))

        out = capsys.readouterr().out.strip()
        assert out.startswith("LS-")
        # Global IDs have G prefix in the number
        assert "G" in out

    def test_cmd_promote_invalid_source(self, tmp_path, monkeypatch):
        _setup_project(tmp_path, monkeypatch)

        ns = argparse.Namespace(
            agent=None, source="/nonexistent/path.md",
            to="thread", to_global=False, working_dir=None,
        )
        with pytest.raises(SystemExit):
            cmd_promote(ns)
