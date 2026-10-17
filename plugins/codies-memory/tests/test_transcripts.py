"""Tests for finding and catching up sessions that ended without a summary."""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from codies_memory import transcripts
from codies_memory.cli import cmd_boot, cmd_create, cmd_init, main
from codies_memory.records import read_record


NOW = datetime(2026, 10, 17, 12, 0, tzinfo=timezone.utc)


def _iso(moment: datetime) -> str:
    return moment.isoformat().replace("+00:00", "Z")


def _write_jsonl(path: Path, objects: list[dict], touched: datetime) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(o, separators=(",", ":")) + "\n" for o in objects), encoding="utf-8")
    os.utime(path, (touched.timestamp(), touched.timestamp()))
    return path


def _claude_user(text: str, at: datetime, **extra) -> dict:
    return {"type": "user", "timestamp": _iso(at), "cwd": "/work/app", "message": {"role": "user", "content": text}, **extra}


def _claude_agent(at: datetime, text: str | None = None, command: str | None = None,
                  tool: str = "Bash", tool_id: str = "toolu_1") -> dict:
    content: list[dict] = []
    if text:
        content.append({"type": "text", "text": text})
    if command is not None:
        key = "command" if tool == "Bash" else "content"
        content.append({"type": "tool_use", "id": tool_id, "name": tool, "input": {key: command}})
    return {"type": "assistant", "timestamp": _iso(at), "message": {"role": "assistant", "content": content}}


def _claude_result(at: datetime, output: str, tool_id: str = "toolu_1", is_error: bool = False) -> dict:
    return {"type": "user", "timestamp": _iso(at), "message": {"role": "user", "content": [
        {"type": "tool_result", "tool_use_id": tool_id, "content": output, "is_error": is_error}]}}


def _claude_close(at: datetime, tool_id: str = "toolu_close") -> list[dict]:
    """A successful close: the call, then its result naming the new record."""
    return [
        _claude_agent(at, command="codies-memory create session --agent claude --body-file s.md", tool_id=tool_id),
        _claude_result(at + timedelta(seconds=2), "SS-20261016-ab12", tool_id=tool_id),
    ]


def _claude_session(home: Path, working_dir: Path, session_id: str, start: datetime, *, extra: list[dict] = ()) -> Path:
    objects = [
        {"type": "ai-title", "aiTitle": f"Title {session_id[:4]}", "sessionId": session_id},
        _claude_user("Please look at the parser", start),
        _claude_agent(start + timedelta(minutes=1), text="Looked at it, fixed the off-by-one."),
        *extra,
    ]
    last = max(datetime.fromisoformat(o["timestamp"].replace("Z", "+00:00")) for o in objects if "timestamp" in o)
    path = transcripts.claude_project_dir(working_dir, home) / f"{session_id}.jsonl"
    return _write_jsonl(path, objects, last)


def _session_record(project_vault: Path, transcript_id: str, covered_at: datetime | None,
                    checkpoint: bool = False, name: str | None = None) -> None:
    sessions = project_vault / "sessions"
    sessions.mkdir(parents=True, exist_ok=True)
    lines = [
        "---", "id: SS-20261017-abcd", "title: Session", "type: session", "status: active",
        "trust: working", "scope: project", "created: '2026-10-17'", "updated: '2026-10-17'",
        f"transcript: {transcript_id}",
    ]
    if covered_at:
        lines.append(f"transcript_covered_at: '{covered_at.isoformat()}'")
    if checkpoint:
        lines.append("transcript_checkpoint: true")
    lines += ["---", "", "Summary."]
    (sessions / f"SS-{name or transcript_id[:4]}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _legacy_record(project_vault: Path, record_id: str) -> None:
    """A session record written before records linked to transcripts."""
    sessions = project_vault / "sessions"
    sessions.mkdir(parents=True, exist_ok=True)
    (sessions / f"{record_id}-legacy.md").write_text(
        f"---\nid: {record_id}\ntitle: Session\ntype: session\nstatus: active\ntrust: working\n"
        "scope: project\ncreated: '2026-10-16'\nupdated: '2026-10-16'\n---\n\nSummary.\n", encoding="utf-8")


def _codex_rollout(path: Path, session_id: str, start: datetime, items: list[dict], *,
                   cwd: str = "/work/app", originator: str = "codex-tui", source="vscode") -> Path:
    objects = [{"timestamp": _iso(start), "type": "session_meta",
                "payload": {"id": session_id, "cwd": cwd, "originator": originator, "source": source}}]
    for offset, payload in enumerate(items):
        kind = payload.pop("_kind", "response_item")
        objects.append({"timestamp": _iso(start + timedelta(minutes=offset + 1)), "type": kind, "payload": payload})
    return _write_jsonl(path, objects, start + timedelta(minutes=len(items)))


def _codex_user(text: str) -> dict:
    return {"type": "message", "role": "user", "content": [{"type": "input_text", "text": text}]}


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

class TestReadClaude:

    def test_keeps_user_agent_and_summary_text(self, tmp_path):
        start = NOW - timedelta(days=1)
        path = _write_jsonl(tmp_path / "s1.jsonl", [
            {"type": "ai-title", "aiTitle": "Parser fix"},
            _claude_user("Fix the parser please", start),
            _claude_user("<command-name>/clear</command-name>", start),
            _claude_user("<task-notification>agent done</task-notification>", start),
            _claude_user("Caveat injected", start, isMeta=True),
            _claude_result(start, "ok"),
            _claude_user("side quest", start, isSidechain=True),
            _claude_agent(start + timedelta(minutes=1), text="Done."),
            _claude_user("This session is being continued...", start + timedelta(minutes=2), isCompactSummary=True),
            {"type": "api-request-blob", "body": "\"type\":\"user\" inside a blob"},
        ], start)

        transcript = transcripts.read_transcript(path, "claude-code")

        assert transcript.session_id == "s1"
        assert transcript.title == "Parser fix"
        assert transcript.cwd == "/work/app"
        assert [e.kind for e in transcript.entries] == ["user", "assistant", "summary"]
        assert transcript.started == start
        assert transcript.close_calls == []

    @pytest.mark.parametrize("text", [
        "<task>Implement the cache</task>",
        "<pasted_content>log output</pasted_content> what does this mean?",
        "<div>why does this render twice?</div>",
    ])
    def test_prompts_that_start_with_a_tag_are_still_the_users(self, tmp_path, text):
        path = _write_jsonl(tmp_path / "s3.jsonl", [_claude_user(text, NOW)], NOW)

        assert transcripts.read_transcript(path, "claude-code").user_messages == 1

    def test_a_summary_call_counts_once_its_record_exists_without_a_link(self, tmp_path):
        at = NOW - timedelta(hours=2)
        path = _write_jsonl(tmp_path / "s2.jsonl", [_claude_user("wrap up", at), *_claude_close(at)], at)

        transcript = transcripts.read_transcript(path, "claude-code")

        assert transcript.close_calls == [(at + timedelta(seconds=2), "SS-20261016-ab12")]
        assert transcript.closed_at({"SS-20261016-ab12"}) == at + timedelta(seconds=2)
        assert transcript.closed_at(set()) is None

    @pytest.mark.parametrize("command, output, is_error", [
        ("codies-memory create session --agent claude", "Error: --body or --body-file is required.", True),
        ("codies-memory create session --agent claude", "usage: codies-memory create ...", False),
        ("cat <<EOF\ncodies-memory create session --agent claude\nEOF", "codies-memory create session --agent claude", False),
        ("codies-memory create session --transcript other --agent claude", "SS-20261016-ab12", False),
        ("codies-memory create session --checkpoint --agent claude", "SS-20261016-ab12", False),
        ("codies-memory create session --covered-until 2026-10-16T08:00:00Z", "SS-20261016-ab12", False),
        ('grep -n "codies-memory create session" SKILL.md', "SS-20261016-ab12 in an example", False),
        ('echo "run codies-memory create session --agent x"', "SS-20261016-ab12", False),
        ("cat <<'EOF'\ncodies-memory create session --agent x\nSS-20261016-ab12\nEOF", "SS-20261016-ab12", False),
        ("# codies-memory create session --agent x\necho SS-20261016-ab12", "SS-20261016-ab12", False),
        ("echo codies-memory create session --agent x; echo SS-20261016-ab12", "SS-20261016-ab12", False),
    ])
    def test_failed_or_foreign_summary_calls_do_not_cover_it(self, tmp_path, command, output, is_error):
        at = NOW - timedelta(hours=2)
        path = _write_jsonl(tmp_path / "s2.jsonl", [
            _claude_user("wrap up", at),
            _claude_agent(at, command=command),
            _claude_result(at + timedelta(seconds=1), output, is_error=is_error),
        ], at)

        assert transcripts.read_transcript(path, "claude-code").close_calls == []

    @pytest.mark.parametrize("command", [
        "AGENT=claude TODAY=2026-10-16 codies-memory create session --agent claude",
        "cd /work/app && codies-memory create session --agent claude",
        "if true; then codies-memory create session --agent claude; fi",
    ])
    def test_close_calls_in_command_position(self, tmp_path, command):
        at = NOW - timedelta(hours=2)
        path = _write_jsonl(tmp_path / "s7.jsonl", [
            _claude_user("wrap up", at),
            _claude_agent(at, command=command, tool_id="t7"),
            _claude_result(at + timedelta(seconds=1), "SS-20261016-ab12", tool_id="t7"),
        ], at)

        assert transcripts.read_transcript(path, "claude-code").close_calls == [(at + timedelta(seconds=1), "SS-20261016-ab12")]

    def test_a_close_after_writing_its_body_with_a_heredoc_counts(self, tmp_path):
        at = NOW - timedelta(hours=2)
        command = "cat > /tmp/s.md <<'EOF'\n## What Happened\n- a lot\nEOF\ncodies-memory create session --agent claude --body-file /tmp/s.md"
        path = _write_jsonl(tmp_path / "s5.jsonl", [
            _claude_user("wrap up", at),
            _claude_agent(at, command=command, tool_id="t5"),
            _claude_result(at + timedelta(seconds=1), "SS-20261016-ab12", tool_id="t5"),
        ], at)

        assert transcripts.read_transcript(path, "claude-code").close_calls == [(at + timedelta(seconds=1), "SS-20261016-ab12")]

    def test_tool_work_without_prose_counts_as_activity(self, tmp_path):
        at = NOW - timedelta(hours=2)
        path = _write_jsonl(tmp_path / "s4.jsonl", [
            _claude_user("go on", at),
            _claude_agent(at + timedelta(minutes=30), command="pytest -q", tool_id="t9"),
            _claude_result(at + timedelta(minutes=31), "3 passed", tool_id="t9"),
        ], at)

        transcript = transcripts.read_transcript(path, "claude-code")

        assert transcript.last_activity == at + timedelta(minutes=31)
        assert transcript.activity_after(at + timedelta(minutes=10)) == 2


class TestReadCodex:

    def test_reads_messages_summaries_and_a_successful_close(self, tmp_path):
        start = NOW - timedelta(hours=3)
        session_id = "01a12f70-e8f8-7e80-b793-ae386e5b315c"
        path = _codex_rollout(tmp_path / f"rollout-2026-10-17T09-00-00-{session_id}.jsonl", session_id, start, [
            _codex_user("# AGENTS.md instructions\n..."),
            _codex_user("<environment_context>\n<cwd>/work/app</cwd>"),
            _codex_user("Review the PR"),
            {"type": "message", "role": "assistant", "content": [{"type": "output_text", "text": "Two findings."}]},
            {"_kind": "compacted", "message": "Summary so far"},
            {"type": "custom_tool_call", "name": "exec", "call_id": "c1",
             "input": 'text(await tools.exec_command({cmd:"codies-memory create session --agent codie --title \\"x\\""}))'},
            {"type": "custom_tool_call_output", "call_id": "c1", "output": "SS-20261017-cd34\n"},
        ])

        transcript = transcripts.read_transcript(path)

        assert transcript.harness == "codex"
        assert transcript.session_id == session_id
        assert transcript.interactive is True
        assert [e.kind for e in transcript.entries] == ["user", "assistant", "summary", "tool"]
        assert transcript.close_calls == [(start + timedelta(minutes=7), "SS-20261017-cd34")]

    @pytest.mark.parametrize("payload", [
        {"type": "custom_tool_call", "input": 'tools.exec_command({"cmd":"codies-memory create session --agent codie"})'},
        {"type": "custom_tool_call", "input": "tools.exec_command({cmd:'codies-memory create session --agent codie'})"},
        {"type": "function_call", "arguments": '{"cmd": "codies-memory create session --agent codie"}'},
    ])
    def test_close_calls_in_other_spellings(self, tmp_path, payload):
        start = NOW - timedelta(hours=3)
        path = _codex_rollout(tmp_path / "rollout-x.jsonl", "x", start, [
            _codex_user("wrap up"),
            {**payload, "call_id": "c1"},
            {"type": "function_call_output", "call_id": "c1", "output": "SS-20261017-cd34"},
        ])

        assert transcripts.read_transcript(path).close_calls == [(start + timedelta(minutes=3), "SS-20261017-cd34")]

    def test_subagent_and_exec_sessions_are_not_interactive(self, tmp_path):
        start = NOW - timedelta(hours=3)
        sub = _codex_rollout(tmp_path / "rollout-a.jsonl", "a", start, [_codex_user("task for you")],
                             source={"subagent": {"thread_spawn": {"parent_thread_id": "p"}}})
        exe = _codex_rollout(tmp_path / "rollout-b.jsonl", "b", start, [_codex_user("task")], originator="codex_exec")

        assert transcripts.read_transcript(sub).interactive is False
        assert transcripts.read_transcript(exe).interactive is False


# ---------------------------------------------------------------------------
# Open sessions
# ---------------------------------------------------------------------------

def _open_ids(global_vault: Path, home: Path, **kwargs) -> list[str]:
    items = transcripts.open_transcripts(global_vault, "claude-code", Path("/work/app"), now=NOW, home=home, **kwargs)
    return [o.transcript.session_id for o in items]


class TestOpenTranscripts:

    def test_lists_only_sessions_that_still_need_a_summary(self, tmp_path, tmp_global_vault, tmp_project_vault):
        home = tmp_path / "home"
        work = Path("/work/app")
        day = NOW - timedelta(days=2)
        _claude_session(home, work, "aaaa-never", day)
        _claude_session(home, work, "bbbb-covered", day)
        _session_record(tmp_project_vault, "bbbb-covered", day + timedelta(hours=1))
        _claude_session(home, work, "cccc-tail", day, extra=[_claude_user("one more thing", day + timedelta(hours=3))])
        _session_record(tmp_project_vault, "cccc-tail", day + timedelta(hours=1))
        _claude_session(home, work, "dddd-current", day)
        _claude_session(home, work, "eeee-live", NOW - timedelta(minutes=5))
        _claude_session(home, work, "ffff-skipped", day)
        transcripts.skip_transcript(tmp_global_vault, "ffff-skipped", "quick question", day + timedelta(minutes=1))
        _claude_session(home, work, "gggg-closed", day, extra=_claude_close(day + timedelta(minutes=2)))
        _legacy_record(tmp_project_vault, "SS-20261016-ab12")
        _claude_session(home, work, "hhhh-old", NOW - timedelta(days=40))

        items = transcripts.open_transcripts(
            tmp_global_vault, "claude-code", work, current_id="dddd-current", now=NOW, home=home)

        assert [o.transcript.session_id for o in items] == ["cccc-tail", "aaaa-never"]
        assert items[0].covered_at == day + timedelta(hours=1)
        assert items[1].covered is None

    def test_a_printed_example_with_a_record_id_closes_nothing(self, tmp_path, tmp_global_vault, tmp_project_vault):
        home = tmp_path / "home"
        day = NOW - timedelta(days=1)
        _claude_session(home, Path("/work/app"), "aaaa-example", day, extra=[
            _claude_agent(day + timedelta(minutes=2), command="cat <<EOF\ncodies-memory create session --agent x\nEOF"),
            _claude_result(day + timedelta(minutes=3), "codies-memory create session ... prints SS-20261016-ab12"),
        ])

        assert _open_ids(tmp_global_vault, home) == ["aaaa-example"]

    def test_a_linked_record_wins_over_its_own_close_call(self, tmp_path, tmp_global_vault, tmp_project_vault):
        # the record links to the transcript and covers it until 10 minutes in; the call that wrote it
        # came later, after a user message the record does not cover
        home = tmp_path / "home"
        day = NOW - timedelta(days=1)
        _claude_session(home, Path("/work/app"), "aaaa-linked", day, extra=[
            _claude_user("and the README", day + timedelta(minutes=12)),
            *_claude_close(day + timedelta(minutes=20)),
        ])
        sessions = tmp_project_vault / "sessions"
        sessions.mkdir(parents=True, exist_ok=True)
        (sessions / "SS-20261016-ab12-linked.md").write_text(
            "---\nid: SS-20261016-ab12\ntitle: S\ntype: session\nstatus: active\ntrust: working\nscope: project\n"
            "created: '2026-10-16'\nupdated: '2026-10-16'\ntranscript: aaaa-linked\n"
            f"transcript_covered_at: '{(day + timedelta(minutes=10)).isoformat()}'\n---\n\nS.\n", encoding="utf-8")

        assert _open_ids(tmp_global_vault, home) == ["aaaa-linked"]

    def test_an_example_naming_an_existing_record_closes_nothing(self, tmp_path, tmp_global_vault, tmp_project_vault):
        home = tmp_path / "home"
        day = NOW - timedelta(days=1)
        _legacy_record(tmp_project_vault, "SS-20261016-ab12")  # a real record of some other session
        _claude_session(home, Path("/work/app"), "aaaa-example2", day, extra=[
            _claude_agent(day + timedelta(minutes=2),
                          command="cat <<EOF\ncodies-memory create session --agent x\nSS-20261016-ab12\nEOF"),
            _claude_result(day + timedelta(minutes=3), "codies-memory create session --agent x\nSS-20261016-ab12"),
        ])

        assert _open_ids(tmp_global_vault, home) == ["aaaa-example2"]

    def test_tool_work_after_a_checkpoint_reopens(self, tmp_path, tmp_global_vault, tmp_project_vault):
        home = tmp_path / "home"
        day = NOW - timedelta(days=1)
        _claude_session(home, Path("/work/app"), "aaaa-tools", day, extra=[
            _claude_agent(day + timedelta(minutes=30), command="pytest -q", tool_id="t9"),
            _claude_result(day + timedelta(minutes=31), "3 passed", tool_id="t9"),
        ])
        _session_record(tmp_project_vault, "aaaa-tools", day + timedelta(minutes=10), checkpoint=True)

        assert _open_ids(tmp_global_vault, home) == ["aaaa-tools"]

    def test_the_checkpoint_calls_own_result_is_no_work_after_it(self, tmp_path, tmp_global_vault, tmp_project_vault):
        home = tmp_path / "home"
        day = NOW - timedelta(days=1)
        at = day + timedelta(minutes=10)
        _claude_session(home, Path("/work/app"), "aaaa-ckpt", day, extra=[
            _claude_agent(at - timedelta(seconds=2), command="codies-memory create session --checkpoint --agent claude",
                          tool_id="k1"),
            _claude_result(at + timedelta(seconds=1), "SS-20261016-cd12", tool_id="k1"),
        ])
        _session_record(tmp_project_vault, "aaaa-ckpt", at, checkpoint=True)

        assert _open_ids(tmp_global_vault, home) == []

    def test_a_user_message_right_after_the_summary_reopens(self, tmp_path, tmp_global_vault, tmp_project_vault):
        home = tmp_path / "home"
        day = NOW - timedelta(days=1)
        _claude_session(home, Path("/work/app"), "aaaa-followup", day, extra=[
            _claude_user("oh, and one more thing", day + timedelta(minutes=12))])
        _session_record(tmp_project_vault, "aaaa-followup", day + timedelta(minutes=10))

        assert _open_ids(tmp_global_vault, home) == ["aaaa-followup"]

    def test_the_agent_finishing_its_close_is_no_new_activity(self, tmp_path, tmp_global_vault, tmp_project_vault):
        home = tmp_path / "home"
        day = NOW - timedelta(days=1)
        _claude_session(home, Path("/work/app"), "aaaa-closing", day, extra=[
            _claude_agent(day + timedelta(minutes=50), text="Dream saved, pushed.")])
        _session_record(tmp_project_vault, "aaaa-closing", day + timedelta(minutes=10))

        assert _open_ids(tmp_global_vault, home) == []

    def test_work_after_a_checkpoint_reopens_until_a_summary_covers_it(self, tmp_path, tmp_global_vault, tmp_project_vault):
        home = tmp_path / "home"
        day = NOW - timedelta(days=1)
        _claude_session(home, Path("/work/app"), "aaaa-checkpoint", day, extra=[
            _claude_agent(day + timedelta(minutes=40), text="Implemented the rest.")])
        _session_record(tmp_project_vault, "aaaa-checkpoint", day + timedelta(minutes=10), checkpoint=True, name="cp")

        items = transcripts.open_transcripts(tmp_global_vault, "claude-code", Path("/work/app"), now=NOW, home=home)
        assert [o.transcript.session_id for o in items] == ["aaaa-checkpoint"]
        assert "after the checkpoint" in transcripts.render_open_section(items, "claude", "claude-code")

        _session_record(tmp_project_vault, "aaaa-checkpoint", day + timedelta(minutes=45), name="final")
        assert _open_ids(tmp_global_vault, home) == []

    def test_a_skip_reaches_only_as_far_as_the_session_went(self, tmp_path, tmp_global_vault):
        home = tmp_path / "home"
        day = NOW - timedelta(days=1)
        _claude_session(home, Path("/work/app"), "aaaa-resumed", day, extra=[
            _claude_user("picking this up again for real work", day + timedelta(hours=5))])
        transcripts.skip_transcript(tmp_global_vault, "aaaa-resumed", "quick question", day + timedelta(minutes=1))

        assert _open_ids(tmp_global_vault, home) == ["aaaa-resumed"]

    def test_a_record_without_covered_at_covers_the_whole_transcript(self, tmp_path, tmp_global_vault, tmp_project_vault):
        home = tmp_path / "home"
        _claude_session(home, Path("/work/app"), "aaaa-manual", NOW - timedelta(days=1))
        _session_record(tmp_project_vault, "aaaa-manual", None)

        assert _open_ids(tmp_global_vault, home) == []

    def test_codex_discovery_keeps_interactive_sessions_of_this_directory(self, tmp_path, tmp_global_vault):
        home = tmp_path / "home"
        start = NOW - timedelta(days=1)
        day_dir = home / ".codex" / "sessions" / "2026" / "10" / "16"

        def rollout(name: str, cwd: str, **meta) -> None:
            _codex_rollout(day_dir / f"rollout-2026-10-16T10-00-00-{name}.jsonl", name, start, [_codex_user("hi")],
                           cwd=cwd, **meta)

        rollout("11111111-1111-1111-1111-111111111111", "/work/app")
        rollout("22222222-2222-2222-2222-222222222222", "/work/other")
        rollout("33333333-3333-3333-3333-333333333333", "/work/app", originator="codex_exec")
        rollout("44444444-4444-4444-4444-444444444444", "/work/app", source={"subagent": "review"})

        items = transcripts.open_transcripts(tmp_global_vault, "codex", Path("/work/app"), now=NOW, home=home)

        assert [o.transcript.session_id for o in items] == ["11111111-1111-1111-1111-111111111111"]


# ---------------------------------------------------------------------------
# Digest
# ---------------------------------------------------------------------------

class TestRenderDigest:

    def _transcript(self, entries=None) -> transcripts.Transcript:
        start = NOW - timedelta(hours=5)
        entries = entries or [
            transcripts.Entry(start, "user", "first question"),
            transcripts.Entry(start + timedelta(minutes=1), "assistant", "first answer " * 20),
            transcripts.Entry(start + timedelta(minutes=2), "summary", "compaction summary text"),
            transcripts.Entry(start + timedelta(hours=2), "user", "later question"),
            transcripts.Entry(start + timedelta(hours=2, minutes=1), "assistant", "later answer"),
        ]
        return transcripts.Transcript("claude-code", "abcd", Path("/t/abcd.jsonl"), cwd="/work/app", entries=entries)

    def test_shows_only_what_came_after_the_last_summary(self):
        digest = transcripts.render_digest(self._transcript(), covered_at=NOW - timedelta(hours=4))

        assert "first question" not in digest
        assert "later question" in digest
        assert "Already covered until" in digest

    def test_tool_work_shows_up_in_the_digest(self, tmp_path):
        at = NOW - timedelta(hours=2)
        path = _write_jsonl(tmp_path / "s6.jsonl", [
            _claude_user("go on", at),
            _claude_agent(at + timedelta(minutes=30), command="pytest -q tests/test_cache.py", tool_id="t9"),
            _claude_result(at + timedelta(minutes=31), "3 passed", tool_id="t9"),
        ], at)
        transcript = transcripts.read_transcript(path, "claude-code")

        digest = transcripts.render_digest(transcript, covered_at=at + timedelta(minutes=10))

        assert "Tool: Bash: pytest -q tests/test_cache.py" in digest

    def test_codex_tool_calls_show_up_in_the_digest(self, tmp_path):
        start = NOW - timedelta(hours=3)
        path = _codex_rollout(tmp_path / "rollout-y.jsonl", "y", start, [
            _codex_user("run the tests"),
            {"type": "custom_tool_call", "name": "exec", "call_id": "c1",
             "input": 'text(await tools.exec_command({cmd:"pytest -q"}))'},
            {"type": "function_call", "name": "shell", "call_id": "c2", "arguments": '{"command": ["ls", "-la"]}'},
        ])

        digest = transcripts.render_digest(transcripts.read_transcript(path))

        assert "Tool: exec: pytest -q" in digest
        assert "Tool: shell: ls -la" in digest

    def test_over_budget_tool_lines_go_first(self):
        start = NOW - timedelta(hours=5)
        entries = [
            transcripts.Entry(start, "user", "question " * 10),
            transcripts.Entry(start + timedelta(minutes=1), "tool", "Bash: " + "x" * 250),
            transcripts.Entry(start + timedelta(minutes=2), "assistant", "answer " * 10),
        ]

        digest = transcripts.render_digest(self._transcript(entries), max_chars=250)

        assert "Tool:" not in digest
        assert "question" in digest and "answer" in digest

    def test_names_the_cutoff_a_summary_may_claim(self):
        transcript = self._transcript()

        digest = transcripts.render_digest(transcript)

        cutoff = transcripts.isoformat(transcript.last_activity)
        assert f"create session --transcript abcd --covered-until {cutoff}" in digest

    def test_over_budget_drops_agent_messages_first_and_keeps_summaries(self):
        digest = transcripts.render_digest(self._transcript(), max_chars=300)

        assert "compaction summary text" in digest
        assert "first question" in digest
        assert "first answer" not in digest
        assert "left out to fit 300 characters" in digest

    def test_the_limit_holds_with_many_long_compaction_summaries(self):
        start = NOW - timedelta(hours=5)
        entries = [transcripts.Entry(start + timedelta(minutes=i), "summary", f"summary {i} " + "x" * 8000)
                   for i in range(4)]

        digest = transcripts.render_digest(self._transcript(entries), max_chars=1000)

        body = digest.split("\n\n", 1)[1]
        assert len(body) <= 1100
        assert "summary 3" in body
        assert "summary 0" not in body


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _setup_cli(tmp_path, monkeypatch) -> tuple[Path, Path]:
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: home))
    work = tmp_path / "myapp"
    work.mkdir()
    cmd_init(argparse.Namespace(agent="claude", type="global"))
    cmd_init(argparse.Namespace(agent="claude", type="project", slug="myapp", working_dir=str(work)))
    monkeypatch.chdir(work)
    return home, work


def _create_session(**extra) -> None:
    ns = argparse.Namespace(
        agent="claude", type="session", title="Session Summary", body="What happened.",
        body_file=None, scope="project", trust="working", field=None, short=None, working_dir=None,
    )
    for key, value in extra.items():
        setattr(ns, key, value)
    cmd_create(ns)


def _last_session(home: Path, capsys) -> dict:
    record_id = capsys.readouterr().out.strip().splitlines()[-1]
    path = next((home / ".memory" / "claude" / "projects" / "myapp" / "sessions").glob(f"{record_id}-*.md"))
    return read_record(path)["frontmatter"]


def test_codex_started_from_claude_code_counts_as_codex():
    env = {"CLAUDE_CODE_SESSION_ID": "parent-claude", "CODEX_THREAD_ID": "child-codex"}

    assert transcripts.detect_harness(env) == "codex"
    assert transcripts.current_session_id(environ=env) == "child-codex"


class TestCreateSessionLink:

    def test_links_the_session_it_runs_in(self, tmp_path, monkeypatch, capsys):
        home, work = _setup_cli(tmp_path, monkeypatch)
        monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", "live-session")

        _create_session()

        frontmatter = _last_session(home, capsys)
        assert frontmatter["transcript"] == "live-session"
        assert transcripts.parse_time(frontmatter["transcript_covered_at"]).tzinfo is not None
        assert "transcript_checkpoint" not in frontmatter

    def test_explicit_transcript_and_cutoff_win(self, tmp_path, monkeypatch, capsys):
        home, work = _setup_cli(tmp_path, monkeypatch)
        monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", "live-session")

        _create_session(transcript="older-session", covered_until="2026-10-16T08:00:00Z")

        frontmatter = _last_session(home, capsys)
        assert frontmatter["transcript"] == "older-session"
        assert transcripts.parse_time(frontmatter["transcript_covered_at"]) == datetime(2026, 10, 16, 8, tzinfo=timezone.utc)

    def test_a_checkpoint_is_marked(self, tmp_path, monkeypatch, capsys):
        home, work = _setup_cli(tmp_path, monkeypatch)
        monkeypatch.setenv("CODEX_THREAD_ID", "codex-session")

        _create_session(checkpoint=True)

        frontmatter = _last_session(home, capsys)
        assert frontmatter["transcript"] == "codex-session"
        assert frontmatter["transcript_checkpoint"] is True

    @pytest.mark.parametrize("extra", [
        {"type": "lesson", "transcript": "older-session"},
        {"covered_until": "2026-10-16T08:00:00Z"},
        {"transcript": "older-session", "covered_until": "yesterday"},
        {"transcript": "older-session", "covered_until": ""},
    ])
    def test_link_flags_that_cannot_apply_are_refused(self, tmp_path, monkeypatch, extra):
        _setup_cli(tmp_path, monkeypatch)

        with pytest.raises(SystemExit):
            _create_session(**extra)

    def test_outside_an_agent_session_nothing_is_linked(self, tmp_path, monkeypatch, capsys):
        home, work = _setup_cli(tmp_path, monkeypatch)

        _create_session()

        assert "transcript" not in _last_session(home, capsys)


class TestBootSections:

    def _hook(self, tmp_path: Path, home: Path, work: Path, source: str) -> Path:
        hook = tmp_path / "hook.json"
        hook.write_text(json.dumps({
            "session_id": "current-one",
            "transcript_path": str(transcripts.claude_project_dir(work, home) / "current-one.jsonl"),
            "cwd": str(work),
            "source": source,
        }))
        return hook

    def test_boot_lists_open_sessions_and_asks_for_a_checkpoint_after_compaction(self, tmp_path, monkeypatch, capsys):
        home, work = _setup_cli(tmp_path, monkeypatch)
        day = datetime.now(timezone.utc) - timedelta(days=1)
        _claude_session(home, work, "older-one", day)
        _claude_session(home, work, "current-one", day)

        cmd_boot(argparse.Namespace(
            agent="claude", branch="main", budget=4000, hook_input=str(self._hook(tmp_path, home, work, "compact"))))
        out = capsys.readouterr().out

        assert "=== Checkpoint ===" in out
        assert "create session --checkpoint --transcript current-one" in out
        open_section = out.split("=== Open Sessions ===", 1)[1]
        assert "older-one" in open_section
        assert "current-one" not in open_section
        assert "cleanupPeriodDays is not set" in out
        assert out.rstrip().splitlines()[-1].startswith("total:")

    def test_the_hooks_directory_decides_the_project(self, tmp_path, monkeypatch, capsys):
        home, work = _setup_cli(tmp_path, monkeypatch)
        elsewhere = tmp_path / "elsewhere"
        elsewhere.mkdir()
        monkeypatch.chdir(elsewhere)

        cmd_boot(argparse.Namespace(
            agent="claude", branch="main", budget=4000, hook_input=str(self._hook(tmp_path, home, work, "startup"))))
        captured = capsys.readouterr()

        assert "no project vault found" not in captured.err

    def test_general_takes_the_vault_and_the_hook_still_names_the_directory(self, tmp_path, monkeypatch, capsys):
        home, work = _setup_cli(tmp_path, monkeypatch)
        elsewhere = tmp_path / "elsewhere"
        elsewhere.mkdir()
        monkeypatch.chdir(elsewhere)
        _claude_session(home, work, "in-myapp", datetime.now(timezone.utc) - timedelta(days=1))

        cmd_boot(argparse.Namespace(
            agent="claude", branch="main", budget=4000, general=True,
            hook_input=str(self._hook(tmp_path, home, work, "startup"))))

        assert "in-myapp" in capsys.readouterr().out

    def test_working_dir_overrides_the_hooks_transcript_folder(self, tmp_path, monkeypatch, capsys):
        home, work = _setup_cli(tmp_path, monkeypatch)
        other = tmp_path / "other"
        other.mkdir()
        day = datetime.now(timezone.utc) - timedelta(days=1)
        _claude_session(home, work, "in-myapp", day)
        _claude_session(home, other, "in-other", day)

        cmd_boot(argparse.Namespace(
            agent="claude", branch="main", budget=4000, working_dir=str(other),
            hook_input=str(self._hook(tmp_path, home, work, "startup"))))
        out = capsys.readouterr().out

        assert "in-other" in out
        assert "in-myapp" not in out

    def test_startup_boot_without_open_sessions_is_quiet(self, tmp_path, monkeypatch, capsys):
        home, work = _setup_cli(tmp_path, monkeypatch)
        (home / ".claude").mkdir(exist_ok=True)
        (home / ".claude" / "settings.json").write_text('{"cleanupPeriodDays": 90}')

        cmd_boot(argparse.Namespace(
            agent="claude", branch="main", budget=4000, hook_input=str(self._hook(tmp_path, home, work, "startup"))))
        out = capsys.readouterr().out

        assert "=== Checkpoint ===" not in out
        assert "=== Open Sessions ===" not in out

    def test_boot_outside_a_harness_skips_transcripts(self, tmp_path, monkeypatch, capsys):
        home, work = _setup_cli(tmp_path, monkeypatch)
        _claude_session(home, work, "older-one", datetime.now(timezone.utc) - timedelta(days=1))

        cmd_boot(argparse.Namespace(agent="claude", branch="main", budget=4000))

        assert "=== Open Sessions ===" not in capsys.readouterr().out


class TestTranscriptsCommand:

    def test_skip_then_open_and_digest(self, tmp_path, monkeypatch, capsys):
        home, work = _setup_cli(tmp_path, monkeypatch)
        day = datetime.now(timezone.utc) - timedelta(days=1)
        _claude_session(home, work, "first-one", day)
        _claude_session(home, work, "second-one", day)

        def run(*arguments: str) -> str:
            monkeypatch.setattr(sys, "argv", ["codies-memory", "transcripts", *arguments, "--agent", "claude"])
            main()
            return capsys.readouterr().out

        assert "Skipped first-one" in run("skip", "first-one", "--reason", "quick question")
        with pytest.raises(SystemExit):
            run("skip", "no-such-session", "--reason", "typo")
        listed = run("open", "--harness", "claude-code", "--format", "json")
        assert [item["session_id"] for item in json.loads(listed)] == ["second-one"]
        digest = run("digest", "second-one")
        assert "Please look at the parser" in digest
        assert "create session --transcript second-one --covered-until" in digest
