"""Tests for the v2 agent-namespaced CLI commands."""

from __future__ import annotations

import argparse
import datetime
from pathlib import Path

import pytest

import json

from codies_memory.cli import (
    cmd_init, cmd_boot, cmd_status, cmd_capture, cmd_create, cmd_list,
    cmd_promote, cmd_refresh, cmd_validate, _resolve_agent,
)
from codies_memory.vault import GLOBAL_DIRS, LAZY_GLOBAL_DIRS, PROJECT_DIRS, resolve_global_vault


# ---------------------------------------------------------------------------
# _resolve_agent
# ---------------------------------------------------------------------------

class TestResolveAgent:

    def test_from_flag(self):
        ns = argparse.Namespace(agent="claude")
        assert _resolve_agent(ns) == "claude"

    def test_missing_exits(self):
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
            if d in LAZY_GLOBAL_DIRS:
                assert not (global_vault / d).exists()
                continue
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


        # Init global vault
        ns_global = argparse.Namespace(agent="claude", type="global")
        cmd_init(ns_global)

        # cwd is some random dir with no project
        working_dir = tmp_path / "unrelated"
        working_dir.mkdir()
        monkeypatch.chdir(working_dir)

        ns_boot = argparse.Namespace(agent="claude", branch="main", budget=4000)
        cmd_boot(ns_boot)

        captured = capsys.readouterr()
        assert "Global Packet" in captured.out
        assert "no project vault found" in captured.err

    def test_boot_with_project(self, tmp_path, monkeypatch, capsys):
        """Boot with a project vault produces both packets."""
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: fake_home))


        working_dir = tmp_path / "myapp"
        working_dir.mkdir()

        # Init global + project
        cmd_init(argparse.Namespace(agent="claude", type="global"))
        cmd_init(argparse.Namespace(
            agent="claude", type="project", slug="myapp",
            working_dir=str(working_dir),
        ))

        monkeypatch.chdir(working_dir)

        ns_boot = argparse.Namespace(agent="claude", branch="main", budget=4000)
        cmd_boot(ns_boot)

        captured = capsys.readouterr()
        assert "Global Packet" in captured.out
        assert "Project Packet" in captured.out
        # No warning when project vault is found
        assert "no project vault found" not in captured.err


class TestCmdBootBudgetReport:

    def test_boot_reports_budget_usage(self, tmp_path, monkeypatch, capsys):
        """Boot output ends with a budget report covering slices and total."""
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: fake_home))

        working_dir = tmp_path / "myapp"
        working_dir.mkdir()
        cmd_init(argparse.Namespace(agent="claude", type="global"))
        cmd_init(argparse.Namespace(
            agent="claude", type="project", slug="myapp",
            working_dir=str(working_dir),
        ))
        monkeypatch.chdir(working_dir)

        cmd_boot(argparse.Namespace(agent="claude", branch="main", budget=4000))

        captured = capsys.readouterr()
        assert "=== Boot Budget ===" in captured.out
        assert "identity:" in captured.out
        assert "exempt" in captured.out
        assert "total:" in captured.out
        assert "left" in captured.out

    def test_boot_warns_when_slice_nearly_full(self, tmp_path, monkeypatch, capsys):
        """Slices at 90%+ capacity carry an explicit warning marker."""
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: fake_home))

        working_dir = tmp_path / "myapp"
        working_dir.mkdir()
        cmd_init(argparse.Namespace(agent="claude", type="global"))
        cmd_init(argparse.Namespace(
            agent="claude", type="project", slug="myapp",
            working_dir=str(working_dir),
        ))

        gv = resolve_global_vault("claude")
        session = gv / "projects" / "myapp" / "sessions" / "SS-20260611-big.md"
        session.parent.mkdir(parents=True, exist_ok=True)
        session.write_text(
            "---\nid: SS-20260611\ntitle: Big Session\ntype: session\nstatus: active\ntrust: working\nscope: project\ncreated: '2026-06-11'\nupdated: '2026-06-11'\n---\n\n"
            + ("word " * 500)
            + "\n"
        )
        monkeypatch.chdir(working_dir)

        cmd_boot(argparse.Namespace(agent="claude", branch="main", budget=400))

        captured = capsys.readouterr()
        assert "over 90% full" in captured.out


class TestCmdBootRefresh:

    def test_boot_regenerates_warm_summaries(self, tmp_path, monkeypatch, capsys):
        """Boot rebuilds warm artifacts so stale summaries never surface."""
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: fake_home))

        cmd_init(argparse.Namespace(agent="claude", type="global"))

        gv = resolve_global_vault("claude")
        (gv / "identity" / "self.md").write_text(
            "---\ntitle: self\ntype: identity\n---\n\nFresh identity fact."
        )
        (gv / "boot").mkdir(exist_ok=True)
        (gv / "boot" / "global-summary.md").write_text(
            "# Global Summary\nSTALE SUMMARY CONTENT\n"
        )

        working_dir = tmp_path / "unrelated"
        working_dir.mkdir()
        monkeypatch.chdir(working_dir)

        cmd_boot(argparse.Namespace(agent="claude", branch="main", budget=4000))

        captured = capsys.readouterr()
        assert "STALE SUMMARY CONTENT" not in captured.out
        assert "Fresh identity fact." in captured.out
        assert "STALE SUMMARY CONTENT" not in (gv / "boot" / "global-summary.md").read_text()


# ---------------------------------------------------------------------------
# cmd_status — active count
# ---------------------------------------------------------------------------

class TestCmdStatus:

    def _setup_vault_with_inbox(self, tmp_path, monkeypatch):
        """Helper: set up global + project vault and add inbox items."""
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: fake_home))


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

        ns = argparse.Namespace(agent="claude", all=False)
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

        ns = argparse.Namespace(agent="claude", all=False)
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

        ns = argparse.Namespace(agent="claude", all=True)
        cmd_status(ns)

        out = capsys.readouterr().out
        assert "Active: 1" in out
        assert "My task" in out

    def test_no_project_vault_shows_info(self, tmp_path, monkeypatch, capsys):
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: fake_home))

        cmd_init(argparse.Namespace(agent="claude", type="global"))

        unrelated = tmp_path / "nowhere"
        unrelated.mkdir()
        monkeypatch.chdir(unrelated)

        ns = argparse.Namespace(agent="claude", all=False)
        cmd_status(ns)

        out = capsys.readouterr().out
        assert "Global vault:" in out
        assert "Project vault: none" in out
        assert "init --type project" in out


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
            agent="claude",
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
            agent="claude",
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

    def test_capture_without_project_routes_to_general(self, tmp_path, monkeypatch, capsys):
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: fake_home))

        cmd_init(argparse.Namespace(agent="claude", type="global"))
        unrelated = tmp_path / "no-project"
        unrelated.mkdir()
        monkeypatch.chdir(unrelated)
        capsys.readouterr()

        cmd_capture(argparse.Namespace(
            agent="claude",
            content="Remember this outside any project",
            source="session",
            gate="allow",
            short="Outside project capture",
            working_dir=None,
        ))

        out = capsys.readouterr().out.strip()
        assert out.startswith("IN-")

        global_vault = fake_home / ".memory" / "claude"
        general = global_vault / "projects" / "_general"
        files = list((general / "inbox").glob("*.md"))
        assert len(files) == 1
        assert "short: Outside project capture" in files[0].read_text()

        logs = list((global_vault / "sessions").glob("*.md"))
        assert len(logs) == 1
        assert f"- [[{out}]] Outside project capture (_general)" in logs[0].read_text()


# ---------------------------------------------------------------------------
# cmd_create
# ---------------------------------------------------------------------------

class TestCmdCreate:

    def test_cmd_create_lesson(self, tmp_path, monkeypatch, capsys):
        project_vault = _setup_project(tmp_path, monkeypatch)
        capsys.readouterr()

        ns = argparse.Namespace(
            agent="claude",
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
            agent="claude",
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

    def test_cmd_create_normalizes_literal_newlines_in_body(self, tmp_path, monkeypatch, capsys):
        project_vault = _setup_project(tmp_path, monkeypatch)
        capsys.readouterr()

        ns = argparse.Namespace(
            agent="claude",
            type="session",
            title="Multiline summary",
            body="Line one\\nLine two",
            body_file=None,
            scope="project",
            trust="working",
            field=None,
            working_dir=None,
        )
        cmd_create(ns)

        out = capsys.readouterr().out.strip()
        assert out.startswith("SS-")

        sessions_dir = project_vault / "sessions"
        files = list(sessions_dir.glob("*.md"))
        assert len(files) == 1
        content = files[0].read_text()
        assert "Line one\nLine two" in content
        assert "Line one\\nLine two" not in content

    def test_cmd_create_with_extra_fields(self, tmp_path, monkeypatch, capsys):
        _setup_project(tmp_path, monkeypatch)
        capsys.readouterr()

        ns = argparse.Namespace(
            agent="claude",
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
            agent="claude",
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

        logs = list((global_vault / "sessions").glob("*.md"))
        assert len(logs) == 1
        assert "(global)" in logs[0].read_text()
        assert "(_general)" not in logs[0].read_text()

    def test_create_without_project_routes_to_general(self, tmp_path, monkeypatch, capsys):
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: fake_home))

        cmd_init(argparse.Namespace(agent="claude", type="global"))
        unrelated = tmp_path / "no-project"
        unrelated.mkdir()
        monkeypatch.chdir(unrelated)
        capsys.readouterr()

        cmd_create(argparse.Namespace(
            agent="claude",
            type="session",
            title="No project closeout",
            body="Closed the floating session.",
            body_file=None,
            scope="project",
            trust="working",
            field=None,
            short="Floating session closed",
            working_dir=None,
        ))

        out = capsys.readouterr().out.strip()
        assert out.startswith("SS-")

        global_vault = fake_home / ".memory" / "claude"
        general = global_vault / "projects" / "_general"
        files = list((general / "sessions").glob("*.md"))
        assert len(files) == 1
        assert "short: Floating session closed" in files[0].read_text()

        logs = list((global_vault / "sessions").glob("*.md"))
        assert len(logs) == 1
        assert f"- [[{out}]] Floating session closed (_general)" in logs[0].read_text()

    def test_short_sanitization_and_storage(self, tmp_path, monkeypatch, capsys):
        project_vault = _setup_project(tmp_path, monkeypatch)
        capsys.readouterr()
        raw_short = "  " + ("x" * 60) + "\n" + ("y" * 80) + "  "
        expected_short = (("x" * 60) + " " + ("y" * 80))[:120]

        cmd_create(argparse.Namespace(
            agent="claude",
            type="lesson",
            title="Sanitize short",
            body="Body.",
            body_file=None,
            scope="project",
            trust="working",
            field=None,
            short=raw_short,
            working_dir=None,
        ))

        out = capsys.readouterr().out.strip()
        record_file = next((project_vault / "lessons").glob("*.md"))
        text = record_file.read_text()
        assert f"short: {expected_short}" in text

        global_vault = tmp_path / "home" / ".memory" / "claude"
        log = next((global_vault / "sessions").glob("*.md")).read_text()
        assert f"- [[{out}]] {expected_short} (myapp)" in log


# ---------------------------------------------------------------------------
# cmd_refresh
# ---------------------------------------------------------------------------

class TestCmdRefresh:

    def test_refresh_writes_global_and_project_summaries(self, tmp_path, monkeypatch, capsys):
        project_vault = _setup_project(tmp_path, monkeypatch)
        global_vault = tmp_path / "home" / ".memory" / "claude"
        capsys.readouterr()

        (global_vault / "identity" / "self.md").write_text(
            "---\ntitle: self\ntype: identity\n---\nCodie keeps durable operational memory."
        )
        (project_vault / "project" / "overview.md").write_text(
            "---\ntitle: overview\ntype: project\nstatus: active\ntrust: working\nscope: project\ncreated: '2026-04-22'\nupdated: '2026-04-22'\n---\nThis repo is testing warm summaries."
        )

        ns = argparse.Namespace(agent="claude", scope="both", working_dir=None)
        cmd_refresh(ns)

        out = capsys.readouterr().out
        assert "global_summary:" in out
        assert "project_summary:" in out
        assert "recent_episodes:" in out
        assert (global_vault / "boot" / "global-summary.md").is_file()
        assert (project_vault / "boot" / "project-summary.md").is_file()
        assert (project_vault / "boot" / "recent-episodes.md").is_file()

    def test_refresh_global_scope_only_writes_global_summary(self, tmp_path, monkeypatch, capsys):
        _setup_project(tmp_path, monkeypatch)
        global_vault = tmp_path / "home" / ".memory" / "claude"
        capsys.readouterr()

        ns = argparse.Namespace(agent="claude", scope="global", working_dir=None)
        cmd_refresh(ns)

        out = capsys.readouterr().out
        assert "global_summary:" in out
        assert "project_summary:" not in out
        assert (global_vault / "boot" / "global-summary.md").is_file()


# ---------------------------------------------------------------------------
# cmd_validate
# ---------------------------------------------------------------------------

class TestCmdValidate:

    def test_validate_project_with_working_dir(self, tmp_path, monkeypatch, capsys):
        """validate --type project --working-dir works when cwd is elsewhere."""
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: fake_home))


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
            agent="claude",
            type="project",
            working_dir=str(working_dir),
        )
        cmd_validate(ns)

        out = capsys.readouterr().out
        assert "is valid" in out

    def test_validate_project_does_not_fallback_to_general(self, tmp_path, monkeypatch, capsys):
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: fake_home))

        cmd_init(argparse.Namespace(agent="claude", type="global"))
        unrelated = tmp_path / "no-project"
        unrelated.mkdir()
        monkeypatch.chdir(unrelated)
        capsys.readouterr()

        with pytest.raises(SystemExit):
            cmd_validate(argparse.Namespace(agent="claude", type="project", working_dir=None))

        err = capsys.readouterr().err
        assert "no project vault found" in err


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
                agent="claude", content=text, source="test",
                gate="allow", working_dir=None,
            ))
        capsys.readouterr()

        # List inbox
        cmd_list(argparse.Namespace(
            agent="claude", type="inbox", scope="project",
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
            agent="claude", content="JSON test item", source="test",
            gate="allow", working_dir=None,
        ))
        capsys.readouterr()

        cmd_list(argparse.Namespace(
            agent="claude", type="inbox", scope="project",
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
            agent="claude", content="Paths test", source="test",
            gate="allow", working_dir=None,
        ))
        capsys.readouterr()

        cmd_list(argparse.Namespace(
            agent="claude", type="inbox", scope="project",
            status=None, trust=None, format="paths",
            working_dir=None,
        ))

        out = capsys.readouterr().out.strip()
        assert out.endswith(".md")

    def test_cmd_list_with_status_filter(self, tmp_path, monkeypatch, capsys):
        _setup_project(tmp_path, monkeypatch)
        capsys.readouterr()

        cmd_capture(argparse.Namespace(
            agent="claude", content="Active item", source="test",
            gate="allow", working_dir=None,
        ))
        capsys.readouterr()

        # Filter for status=archived should return nothing
        cmd_list(argparse.Namespace(
            agent="claude", type="inbox", scope="project",
            status="archived", trust=None, format="table",
            working_dir=None,
        ))

        out = capsys.readouterr().out
        assert "No records found." in out

    def test_cmd_list_empty(self, tmp_path, monkeypatch, capsys):
        _setup_project(tmp_path, monkeypatch)
        capsys.readouterr()

        cmd_list(argparse.Namespace(
            agent="claude", type="inbox", scope="project",
            status=None, trust=None, format="table",
            working_dir=None,
        ))

        out = capsys.readouterr().out
        assert "No records found." in out

    def test_cmd_list_project_does_not_fallback_to_general(self, tmp_path, monkeypatch, capsys):
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: fake_home))

        cmd_init(argparse.Namespace(agent="claude", type="global"))
        unrelated = tmp_path / "no-project"
        unrelated.mkdir()
        monkeypatch.chdir(unrelated)
        capsys.readouterr()

        with pytest.raises(SystemExit):
            cmd_list(argparse.Namespace(
                agent="claude", type="sessions", scope="project",
                status=None, trust=None, format="table", working_dir=None,
            ))

        err = capsys.readouterr().err
        assert "no project vault found" in err

    def test_cmd_list_daily_log_global(self, tmp_path, monkeypatch, capsys):
        _setup_project(tmp_path, monkeypatch)
        capsys.readouterr()

        cmd_create(argparse.Namespace(
            agent="claude",
            type="lesson",
            title="Listed daily",
            body="Body.",
            body_file=None,
            scope="project",
            trust="working",
            field=None,
            short="Listed daily",
            working_dir=None,
        ))
        capsys.readouterr()

        cmd_list(argparse.Namespace(
            agent="claude", type="daily-log", scope="global",
            status=None, trust=None, format="table", working_dir=None,
        ))

        out = capsys.readouterr().out
        assert "DL-" in out


# ---------------------------------------------------------------------------
# cmd_promote
# ---------------------------------------------------------------------------

class TestCmdPromote:

    def test_cmd_promote_to_thread(self, tmp_path, monkeypatch, capsys):
        project_vault = _setup_project(tmp_path, monkeypatch)
        capsys.readouterr()

        # Capture an inbox item first
        cmd_capture(argparse.Namespace(
            agent="claude", content="Investigate the 404 bug",
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
            agent="claude", source=str(source_path), to="thread",
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
            agent="claude", type="lesson", title="Global lesson",
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
            agent="claude", source=str(source_path),
            to=None, to_global=True, working_dir=None,
        ))

        out = capsys.readouterr().out.strip()
        assert out.startswith("LS-")
        # Global IDs have G prefix in the number
        assert "G" in out

    def test_cmd_promote_invalid_source(self, tmp_path, monkeypatch):
        _setup_project(tmp_path, monkeypatch)

        ns = argparse.Namespace(
            agent="claude", source="/nonexistent/path.md",
            to="thread", to_global=False, working_dir=None,
        )
        with pytest.raises(SystemExit):
            cmd_promote(ns)
