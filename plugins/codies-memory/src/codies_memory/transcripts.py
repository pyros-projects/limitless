"""Find agent session transcripts that no session record covers yet.

Claude Code and Codex write every session as JSONL. A session record links to
its transcript through the ``transcript`` and ``transcript_covered_at`` fields;
``transcript_checkpoint: true`` marks an interim record written after a
compaction. A transcript is open when nothing covers it, when the user wrote
more after the newest summary, or when anything happened after the newest
checkpoint. A ``codies-memory create session`` call inside the transcript
also covers it when the record it printed exists and carries no link of its
own, which handles records written before the link existed.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterator

import yaml

from codies_memory.schemas import parse_record


HARNESSES: tuple[str, ...] = ("claude-code", "codex")

# A transcript touched this recently probably belongs to a session that is
# still running in another window.
LIVE_WINDOW = timedelta(minutes=15)

DEFAULT_DAYS = 30

# Codex first: Codex started from a Claude Code shell (a review, a second
# opinion) inherits Claude's variables next to its own, while Claude Code is
# rarely started from inside Codex.
_SESSION_ENV: dict[str, tuple[str, ...]] = {
    "codex": ("CODEX_THREAD_ID", "CODEX_SESSION_ID"),
    "claude-code": ("CLAUDE_CODE_SESSION_ID", "CLAUDE_SESSION_ID"),
}

# A simple shell command that runs ``codies-memory create session``: the words
# start the command, after any ``VAR=value`` assignments.
_CLOSE_CALL = re.compile(r"^(?:[A-Za-z_][A-Za-z0-9_]*=\S*\s+)*codies-memory\s+create\s+session\b")
_COMMAND_SPLIT = re.compile(r"&&|\|\||[;|&()\n]|\b(?:then|do|else)\b")

# What ``create session`` prints when it wrote a record.
_SESSION_RECORD_ID = re.compile(r"\bSS-\d{8}-[0-9a-f]{4}\b")

_UUID_RE = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")

# Wrappers the harnesses write into user turns. Pasted text (<pasted_content>),
# images and shell input the user typed stay user messages.
_INJECTED_TAGS = re.compile(
    r"<(task-notification|command-name|command-message|command-args|local-command-stdout|"
    r"local-command-stderr|local-command-caveat|bash-stdout|bash-stderr|system-reminder|"
    r"artifact-view-context|user-prompt-submit-hook|teammate-message|environment_context|"
    r"user_instructions|user_action|turn_aborted|INSTRUCTIONS)[\s>]"
)

_FULLY = datetime.max.replace(tzinfo=timezone.utc)


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

@dataclass
class Entry:
    at: datetime | None
    kind: str  # "user", "assistant", "tool" (a call the agent made) or "summary"
    text: str


@dataclass
class Transcript:
    harness: str
    session_id: str
    path: Path
    cwd: str | None = None
    title: str | None = None
    interactive: bool = True
    # (time, record id) of each ``create session`` call that printed a record id
    close_calls: list[tuple[datetime, str]] = field(default_factory=list)
    # every user or agent line, tool calls and results included: work without prose counts too
    activity: list[datetime] = field(default_factory=list)
    entries: list[Entry] = field(default_factory=list)

    def closed_at(self, legacy_records: set[str]) -> datetime | None:
        """The newest close call whose record exists and has no transcript link of its own."""
        return max((at for at, record in self.close_calls if record in legacy_records), default=None)

    @property
    def started(self) -> datetime | None:
        return next((e.at for e in self.entries if e.at), None)

    @property
    def last_activity(self) -> datetime | None:
        return max([*self.activity, *(e.at for e in self.entries if e.at)], default=None)

    @property
    def user_messages(self) -> int:
        return sum(1 for e in self.entries if e.kind == "user")

    def user_messages_after(self, moment: datetime) -> int:
        return sum(1 for e in self.entries if e.kind == "user" and e.at and e.at > moment)

    def activity_after(self, moment: datetime) -> int:
        return sum(1 for at in self.activity if at > moment) or sum(1 for e in self.entries if e.at and e.at > moment)

    @property
    def label(self) -> str:
        if self.title:
            return self.title
        first = next((e.text for e in self.entries if e.kind == "user"), "")
        first = re.sub(r"\s+", " ", first).strip()
        return first[:60] + ("…" if len(first) > 60 else "")


@dataclass
class Coverage:
    at: datetime
    checkpoint: bool = False  # an interim record: any later activity reopens


@dataclass
class OpenTranscript:
    transcript: Transcript
    covered: Coverage | None  # None: nothing covers it yet

    @property
    def covered_at(self) -> datetime | None:
        return self.covered.at if self.covered else None


# ---------------------------------------------------------------------------
# Environment and hook input
# ---------------------------------------------------------------------------

def detect_harness(environ: dict[str, str] | None = None) -> str | None:
    """Return the harness this process runs in, judged by its session variables."""
    env = os.environ if environ is None else environ
    for harness, names in _SESSION_ENV.items():
        if any(env.get(name) for name in names):
            return harness
    return None


def current_session_id(harness: str | None = None, environ: dict[str, str] | None = None) -> str | None:
    """Return the session id the harness exposes to its tool processes."""
    env = os.environ if environ is None else environ
    harnesses = [harness] if harness else list(_SESSION_ENV)
    for name in harnesses:
        for var in _SESSION_ENV.get(name, ()):
            if env.get(var):
                return env[var]
    return None


def harness_from_path(path: str | Path | None) -> str | None:
    if not path:
        return None
    text = Path(path).as_posix()
    if "/.claude/projects/" in text:
        return "claude-code"
    if "/.codex/sessions/" in text:
        return "codex"
    return None


def read_hook_input(source: str) -> dict[str, Any]:
    """Read a SessionStart hook payload from a file, or from stdin for ``-``.

    Both harnesses send ``session_id``, ``transcript_path``, ``cwd`` and
    ``source`` (``startup``, ``resume``, ``clear`` or ``compact``). A missing
    or unreadable payload yields an empty dict, so boot still works.
    """
    try:
        if source == "-":
            import sys
            raw = sys.stdin.read()
        else:
            raw = Path(source).read_text(encoding="utf-8")
        data = json.loads(raw) if raw.strip() else {}
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def parse_time(value: Any) -> datetime | None:
    """Parse an ISO timestamp; a value without a zone counts as UTC."""
    if isinstance(value, datetime):
        moment = value
    elif isinstance(value, str) and value:
        try:
            moment = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
    else:
        return None
    return moment if moment.tzinfo else moment.replace(tzinfo=timezone.utc)


def isoformat(moment: datetime) -> str:
    return moment.astimezone(timezone.utc).isoformat(timespec="milliseconds")


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def _jsonl(path: Path, wanted: tuple[str, ...]) -> Iterator[dict[str, Any]]:
    """Yield the JSON objects of lines that contain one of *wanted*.

    Transcripts run to hundreds of megabytes, mostly request blobs and tool
    output; the substring test skips those lines without decoding them.
    """
    with path.open(encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if not any(marker in line for marker in wanted):
                continue
            try:
                obj = json.loads(line)
            except ValueError:
                continue
            if isinstance(obj, dict):
                yield obj


def _texts(content: Any, kinds: set[str]) -> str:
    if isinstance(content, str):
        return content
    parts: list[str] = []
    if isinstance(content, list):
        for block in content:
            if isinstance(block, dict) and block.get("type") in kinds and isinstance(block.get("text"), str):
                parts.append(block["text"])
    return "\n".join(parts)


def _is_injected(text: str) -> bool:
    """True for text the harness wrote into a user turn, not the user."""
    stripped = text.lstrip()
    return (
        not stripped
        or bool(_INJECTED_TAGS.match(stripped))
        or stripped.startswith("# AGENTS.md instructions")
        or stripped.startswith("[Request interrupted")
    )


_HEREDOC = re.compile(r"<<-?\s*(['\"]?)(\w+)\1[^\n]*\n.*?^\s*\2\s*$", re.S | re.M)
_QUOTED = re.compile(r"'[^']*'|\"(?:[^\"\\]|\\.)*\"")
_COMMENT = re.compile(r"(?:^|\s)#[^\n]*")


def _executed_code(command: str) -> str:
    """The parts of a shell command that run: without heredoc bodies, quoted text and comments."""
    code = _HEREDOC.sub("<<heredoc", command)
    code = _QUOTED.sub("''", code)
    return _COMMENT.sub(" ", code)


def _closes_itself(command: Any) -> bool:
    """True when *command* runs ``create session`` for its own session.

    A mention inside a heredoc, quotes or a comment does not run. Calls with
    link flags carry their own coverage. Whether the call wrote a record is
    settled later: the record id it printed must exist.
    """
    if not isinstance(command, str):
        return False
    calls = [part.strip() for part in _COMMAND_SPLIT.split(_executed_code(command))]
    calls = [part for part in calls if _CLOSE_CALL.match(part)]
    return bool(calls) and not any(
        flag in call for call in calls for flag in ("--transcript", "--checkpoint", "--covered-until")
    )


def _writes_checkpoint(command: Any) -> bool:
    """True when *command* runs ``create session --checkpoint``: its own result is no work after it."""
    if not isinstance(command, str):
        return False
    calls = [part.strip() for part in _COMMAND_SPLIT.split(_executed_code(command))]
    return any(_CLOSE_CALL.match(call) and "--checkpoint" in call for call in calls)


def _printed_record(output: Any) -> str | None:
    """The record id ``create session`` printed: a line that is the id and nothing else."""
    if not isinstance(output, str):
        output = _texts(output, {"text"}) if isinstance(output, list) else json.dumps(output) if output else ""
    for line in reversed(output.splitlines()):
        if _SESSION_RECORD_ID.fullmatch(line.strip()):
            return line.strip()
    return None


def _tool_line(name: Any, detail: Any) -> str:
    """One line about a tool call, for the digest: its name and what it ran or touched."""
    if isinstance(detail, dict):
        detail = next((detail[k] for k in ("command", "cmd", "file_path", "path", "pattern", "url", "description")
                       if isinstance(detail.get(k), str)), json.dumps(detail, ensure_ascii=False))
    text = " ".join(str(detail or "").split())
    return f"{name or 'tool'}: {text[:200]}{'…' if len(text) > 200 else ''}"


def _read_claude(path: Path) -> Transcript:
    transcript = Transcript("claude-code", path.stem, path)
    pending_closes: set[str] = set()
    checkpoints: set[str] = set()
    for obj in _jsonl(path, ('"type":"user"', '"type":"assistant"', '"type":"ai-title"')):
        if obj.get("isSidechain"):
            continue
        kind = obj.get("type")
        if kind == "ai-title" and obj.get("aiTitle"):
            transcript.title = str(obj["aiTitle"])
            continue
        if kind not in ("user", "assistant"):
            continue
        if transcript.cwd is None and obj.get("cwd"):
            transcript.cwd = str(obj["cwd"])
        at = parse_time(obj.get("timestamp"))
        content = (obj.get("message") or {}).get("content")
        blocks = [b for b in content if isinstance(b, dict)] if isinstance(content, list) else []
        results = [b for b in blocks if b.get("type") == "tool_result"]
        if at and not (results and all(b.get("tool_use_id") in checkpoints for b in results)):
            transcript.activity.append(at)
        if kind == "user":
            for block in blocks:
                record = _printed_record(block.get("content"))
                if (
                    block.get("type") == "tool_result"
                    and block.get("tool_use_id") in pending_closes
                    and not block.get("is_error")
                    and record and at
                ):
                    transcript.close_calls.append((at, record))
            if obj.get("isCompactSummary"):
                text = _texts(content, {"text"})
                if text.strip():
                    transcript.entries.append(Entry(at, "summary", text))
                continue
            if obj.get("isMeta"):
                continue
            text = _texts(content, {"text"})
            if not _is_injected(text):
                transcript.entries.append(Entry(at, "user", text))
            continue
        for block in blocks:
            if block.get("type") != "tool_use":
                continue
            transcript.entries.append(Entry(at, "tool", _tool_line(block.get("name"), block.get("input"))))
            if isinstance(block.get("input"), dict) and _writes_checkpoint(block["input"].get("command")) and block.get("id"):
                checkpoints.add(str(block["id"]))
            if (
                isinstance(block.get("input"), dict)
                and _closes_itself(block["input"].get("command"))
                and block.get("id")
            ):
                pending_closes.add(str(block["id"]))
        text = _texts(content, {"text"})
        if text.strip():
            transcript.entries.append(Entry(at, "assistant", text))
    return transcript


def _codex_meta(path: Path) -> dict[str, Any]:
    try:
        with path.open(encoding="utf-8", errors="replace") as handle:
            first = json.loads(handle.readline())
    except (OSError, ValueError):
        return {}
    if not isinstance(first, dict) or first.get("type") != "session_meta":
        return {}
    payload = first.get("payload")
    return payload if isinstance(payload, dict) else {}


def _codex_interactive(meta: dict[str, Any]) -> bool:
    """A session the user drove: not ``codex exec``, not a subagent."""
    if meta.get("originator") == "codex_exec":
        return False
    source = meta.get("source")
    return not (isinstance(source, dict) and "subagent" in source)


def _codex_id_from_name(path: Path) -> str:
    match = _UUID_RE.search(path.stem)
    return match.group(0) if match else path.stem


# ``cmd`` in the JavaScript of a custom ``exec`` call: ``cmd:"…"``,
# ``"cmd":"…"``, ``cmd:'…'`` or ``cmd:`…```. Commands built at run time are
# not recognized; detecting a close from the transcript is best effort.
_CODEX_CMD_RE = re.compile(
    r"""["']?\bcmd["']?\s*:\s*("(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*'|`(?:[^`\\]|\\.)*`)"""
)


def _unquote(literal: str) -> str:
    if literal.startswith('"'):
        try:
            return json.loads(literal)
        except ValueError:
            pass
    body = literal[1:-1]
    return re.sub(r"\\(.)", lambda m: {"n": "\n", "t": "\t"}.get(m.group(1), m.group(1)), body)


def _codex_command(payload: dict[str, Any]) -> str | None:
    """Return the shell command of a Codex tool call, if it ran one.

    Custom ``exec`` calls carry JavaScript such as
    ``tools.exec_command({cmd:"..."})``; function calls carry JSON arguments.
    """
    raw = payload.get("input")
    if isinstance(raw, str):
        commands = [_unquote(m.group(1)) for m in _CODEX_CMD_RE.finditer(raw)]
        return "\n".join(commands) or None
    arguments = payload.get("arguments")
    if isinstance(arguments, str):
        try:
            data = json.loads(arguments)
        except ValueError:
            return None
        if isinstance(data, dict):
            command = data.get("cmd") or data.get("command")
            if isinstance(command, list):
                return " ".join(str(part) for part in command)
            if isinstance(command, str):
                return command
    return None


def _read_codex(path: Path) -> Transcript:
    transcript = Transcript("codex", _codex_id_from_name(path), path)
    pending_closes: set[str] = set()
    checkpoints: set[str] = set()
    for obj in _jsonl(path, ('"type":"session_meta"', '"type":"compacted"', '"type":"response_item"')):
        kind = obj.get("type")
        payload = obj.get("payload") or {}
        if not isinstance(payload, dict):
            continue
        at = parse_time(obj.get("timestamp"))
        if at and kind == "response_item" and payload.get("call_id") not in checkpoints:
            transcript.activity.append(at)
        if kind == "session_meta":
            transcript.session_id = str(payload.get("id") or payload.get("session_id") or transcript.session_id)
            transcript.cwd = payload.get("cwd")
            transcript.interactive = _codex_interactive(payload)
        elif kind == "compacted":
            message = payload.get("message")
            if isinstance(message, str) and message.strip():
                transcript.entries.append(Entry(at, "summary", message))
        elif kind == "response_item":
            item = str(payload.get("type"))
            if item == "message" and payload.get("role") == "user":
                text = _texts(payload.get("content"), {"input_text"})
                if not _is_injected(text):
                    transcript.entries.append(Entry(at, "user", text))
            elif item == "message" and payload.get("role") == "assistant":
                text = _texts(payload.get("content"), {"output_text"})
                if text.strip():
                    transcript.entries.append(Entry(at, "assistant", text))
            elif item.endswith("_call"):
                command = _codex_command(payload)
                detail = command or payload.get("input") or payload.get("arguments")
                transcript.entries.append(Entry(at, "tool", _tool_line(payload.get("name"), detail)))
                if _closes_itself(command) and payload.get("call_id"):
                    pending_closes.add(str(payload["call_id"]))
                if _writes_checkpoint(command) and payload.get("call_id"):
                    checkpoints.add(str(payload["call_id"]))
            elif item.endswith("_call_output") and payload.get("call_id") in pending_closes:
                record = _printed_record(payload.get("output"))
                if record and at:
                    transcript.close_calls.append((at, record))
    return transcript


def read_transcript(path: Path, harness: str | None = None) -> Transcript:
    harness = harness or harness_from_path(path) or ("codex" if path.name.startswith("rollout-") else "claude-code")
    return _read_codex(path) if harness == "codex" else _read_claude(path)


# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------

def claude_project_dir(working_dir: Path, home: Path | None = None) -> Path:
    """Return where Claude Code keeps transcripts for sessions started in *working_dir*."""
    home = home or Path.home()
    return home / ".claude" / "projects" / re.sub(r"[^A-Za-z0-9]", "-", str(working_dir))


def _mtime(path: Path) -> datetime:
    return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)


def find_transcripts(
    harness: str,
    working_dir: Path,
    *,
    since: datetime,
    home: Path | None = None,
    transcript_dir: Path | None = None,
) -> list[Path]:
    """List transcripts of sessions started in *working_dir* and touched since *since*."""
    home = home or Path.home()
    if harness == "claude-code":
        directory = transcript_dir or claude_project_dir(working_dir, home)
        if not directory.is_dir():
            return []
        return sorted(p for p in directory.glob("*.jsonl") if _mtime(p) >= since)

    root = home / ".codex" / "sessions"
    if not root.is_dir():
        return []
    found: list[Path] = []
    for path in root.glob("*/*/*/rollout-*.jsonl"):
        if _mtime(path) < since:
            continue
        meta = _codex_meta(path)
        if not _codex_interactive(meta):
            continue
        if meta.get("cwd") and Path(meta["cwd"]) == working_dir:
            found.append(path)
    return sorted(found)


def locate_transcript(
    session_id: str,
    harness: str | None,
    working_dir: Path,
    home: Path | None = None,
) -> Path | None:
    """Find the transcript file of *session_id*, first in *working_dir*'s folder."""
    home = home or Path.home()
    if harness in (None, "claude-code"):
        local = claude_project_dir(working_dir, home) / f"{session_id}.jsonl"
        if local.is_file():
            return local
        matches = sorted((home / ".claude" / "projects").glob(f"*/{session_id}.jsonl"))
        if matches:
            return matches[0]
    if harness in (None, "codex"):
        matches = sorted((home / ".codex" / "sessions").glob(f"*/*/*/rollout-*{session_id}.jsonl"))
        if matches:
            return matches[0]
    return None


# ---------------------------------------------------------------------------
# Coverage
# ---------------------------------------------------------------------------

def newer_coverage(current: Coverage | None, candidate: Coverage | None) -> Coverage | None:
    """The newer of two coverages; at the same time a summary beats a checkpoint."""
    if candidate is None:
        return current
    if current is None or candidate.at > current.at:
        return candidate
    if candidate.at == current.at and current.checkpoint and not candidate.checkpoint:
        return candidate
    return current


def scan_records(global_vault: Path) -> tuple[dict[str, Coverage], set[str]]:
    """Read the session records of every project vault.

    Returns the newest coverage per transcript id, and the ids of records
    without a transcript link (written before the link existed, or outside a
    harness): a close call in a transcript counts only for one of those. Every
    project vault, because a summary may land in a different project than the
    directory the session started in. A record that names a transcript without
    ``transcript_covered_at`` covers all of it.
    """
    covered: dict[str, Coverage] = {}
    legacy: set[str] = set()
    for path in global_vault.glob("projects/*/sessions/*.md"):
        try:
            frontmatter = parse_record(path)["frontmatter"]
        except Exception:
            continue
        session_id = frontmatter.get("transcript")
        if not session_id:
            if frontmatter.get("id"):
                legacy.add(str(frontmatter["id"]))
            continue
        candidate = Coverage(
            parse_time(frontmatter.get("transcript_covered_at")) or _FULLY,
            checkpoint=frontmatter.get("transcript_checkpoint") is True,
        )
        key = str(session_id)
        covered[key] = newer_coverage(covered.get(key), candidate)
    return covered, legacy


def coverage(global_vault: Path) -> dict[str, Coverage]:
    """Map transcript id to the newest session record that covers it."""
    return scan_records(global_vault)[0]


def best_coverage(transcript: Transcript, covered: dict[str, Coverage], legacy: set[str],
                  skipped: dict[str, Coverage] | None = None) -> Coverage | None:
    """The newest of the linked records, a skip, and a legacy close call."""
    best = newer_coverage(covered.get(transcript.session_id), (skipped or {}).get(transcript.session_id))
    closed = transcript.closed_at(legacy)
    return newer_coverage(best, Coverage(closed)) if closed else best


def _skip_file(global_vault: Path) -> Path:
    return global_vault / "registry" / "transcripts.yaml"


def load_skipped(global_vault: Path) -> dict[str, Coverage]:
    """Map skipped transcript ids to how far the skip reaches."""
    path = _skip_file(global_vault)
    if not path.is_file():
        return {}
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        return {}
    skipped = data.get("skipped") if isinstance(data, dict) else None
    if not isinstance(skipped, dict):
        return {}
    result: dict[str, Coverage] = {}
    for key, value in skipped.items():
        through = parse_time(value.get("through")) if isinstance(value, dict) else None
        result[str(key)] = Coverage(through or _FULLY)  # a skip without a date reaches all of it
    return result


def skip_transcript(global_vault: Path, session_id: str, reason: str, through: datetime | None) -> Path:
    """Record that *session_id* needs no summary up to *through*.

    User messages after *through* make the session open again.
    """
    path = _skip_file(global_vault)
    raw: dict[str, Any] = {}
    if path.is_file():
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            raw = dict(data.get("skipped") or {}) if isinstance(data, dict) else {}
        except yaml.YAMLError:
            raw = {}
    entry: dict[str, Any] = {"reason": reason, "date": datetime.now().date().isoformat()}
    if through is not None:
        entry["through"] = isoformat(through)
    raw[session_id] = entry
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump({"skipped": raw}, sort_keys=True, allow_unicode=True), encoding="utf-8")
    return path


def needs_summary(transcript: Transcript, covered: Coverage | None) -> bool:
    """Decide whether *transcript* still needs a session summary.

    After a summary only the user's words count: the agent finishing its own
    close (a dream, a push) adds nothing. After a checkpoint everything counts,
    because the work goes on.
    """
    if covered is None:
        return True
    if covered.at == _FULLY:
        return False
    if covered.checkpoint:
        return transcript.activity_after(covered.at) > 0
    return transcript.user_messages_after(covered.at) > 0


def open_transcripts(
    global_vault: Path,
    harness: str,
    working_dir: Path,
    *,
    current_id: str | None = None,
    days: int = DEFAULT_DAYS,
    now: datetime | None = None,
    home: Path | None = None,
    transcript_dir: Path | None = None,
) -> list[OpenTranscript]:
    """Return earlier sessions in *working_dir* that still need a session summary.

    Newest first. Leaves out the current session, sessions without a user
    message, and sessions touched within ``LIVE_WINDOW``.
    """
    now = now or datetime.now(timezone.utc)
    covered, legacy = scan_records(global_vault)
    skipped = load_skipped(global_vault)
    result: list[OpenTranscript] = []
    for path in find_transcripts(
        harness, working_dir, since=now - timedelta(days=days), home=home, transcript_dir=transcript_dir
    ):
        touched = _mtime(path)
        if now - touched < LIVE_WINDOW:
            continue
        # The file's modification time bounds its last activity, so a summary
        # or skip that reaches past it settles the question without reading.
        if harness == "claude-code":
            known = newer_coverage(covered.get(path.stem), skipped.get(path.stem))
            if known and not known.checkpoint and touched <= known.at:
                continue
        transcript = read_transcript(path, harness)
        if transcript.session_id == current_id:
            continue
        if not transcript.interactive or transcript.user_messages == 0:
            continue
        last = transcript.last_activity
        if last is None or now - last < LIVE_WINDOW:
            continue
        best = best_coverage(transcript, covered, legacy, skipped)
        if needs_summary(transcript, best):
            result.append(OpenTranscript(transcript, best))
    result.sort(key=lambda o: o.transcript.last_activity or now, reverse=True)
    return result


def transcript_retention_warning(home: Path | None = None) -> str | None:
    """Warn when Claude Code will delete transcripts after its 30-day default."""
    settings = (home or Path.home()) / ".claude" / "settings.json"
    try:
        data = json.loads(settings.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        data = {}
    if isinstance(data, dict) and data.get("cleanupPeriodDays"):
        return None
    return (
        "Claude Code deletes transcripts after 30 days because cleanupPeriodDays is not set "
        f"in {settings}. Sessions older than that cannot be caught up."
    )


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def _local(moment: datetime | None, fmt: str = "%Y-%m-%d %H:%M") -> str:
    return moment.astimezone().strftime(fmt) if moment else "?"


def _span(transcript: Transcript) -> str:
    start = _local(transcript.started, "%Y-%m-%d")
    end = _local(transcript.last_activity, "%Y-%m-%d")
    return start if start == end else f"{start} → {end}"


def _state(item: OpenTranscript) -> str:
    t = item.transcript
    if item.covered is None:
        return f"{t.user_messages} user messages, never summarized"
    if item.covered.checkpoint:
        return f"work went on after the checkpoint of {_local(item.covered.at)}"
    return (
        f"{t.user_messages_after(item.covered.at)} of {t.user_messages} user messages "
        f"came after the summary of {_local(item.covered.at)}"
    )


def render_open_section(
    items: list[OpenTranscript],
    agent: str,
    harness: str,
    *,
    warning: str | None = None,
    limit: int = 5,
) -> str:
    """Render the boot section that lists sessions still needing a summary."""
    lines: list[str] = []
    if items:
        noun = "session" if len(items) == 1 else "sessions"
        lines.append(f"{len(items)} earlier {noun} in this directory still need a session summary ({harness}).")
        for item in items[:limit]:
            t = item.transcript
            lines.append(f"- {_span(t)} · {t.session_id} · \"{t.label}\" · {_state(item)}")
        if len(items) > limit:
            lines.append(f"- … and {len(items) - limit} more: `codies-memory transcripts open --agent {agent}`")
        lines.append(
            f"Catch up before new work: `codies-memory transcripts digest <id> --agent {agent}`, then write "
            "the summary with the `create session` command the digest prints, moments included. "
            f"Not worth a summary: `codies-memory transcripts skip <id> --reason \"...\" --agent {agent}`."
        )
    if warning:
        lines.append(f"Note: {warning}")
    return "\n".join(lines)


def render_checkpoint(agent: str, session_id: str | None = None) -> str:
    link = f" --transcript {session_id}" if session_id else ""
    return (
        "This session was just compacted. Before you continue, save what the compaction summary "
        "covers as an interim session record, moments included:\n"
        f"`codies-memory create session --checkpoint{link} --agent {agent} --title \"...\" --body-file <file>`\n"
        "A checkpoint is not a close: the session shows up as open again if anything happens "
        "after it, until a final summary covers it."
    )


_CAPS = {"user": 1500, "assistant": 600, "tool": 300, "summary": 8000}
_LABELS = {"user": "User", "assistant": "Agent", "tool": "Tool", "summary": "Compaction summary"}


def render_digest(
    transcript: Transcript,
    *,
    covered_at: datetime | None = None,
    max_chars: int = 24000,
) -> str:
    """Render a transcript as a compact digest for writing its session summary.

    With *covered_at*, only entries after that time appear. Over budget, the
    oldest tool lines go first, then agent messages, then user messages, then
    all compaction summaries but the newest, which is cut to fit last.
    """
    entries = [e for e in transcript.entries if not (covered_at and e.at and e.at <= covered_at)]
    blocks: list[tuple[Entry, str]] = []
    for entry in entries:
        text = entry.text.strip()
        cap = _CAPS[entry.kind]
        if len(text) > cap:
            text = text[:cap] + " […]"
        blocks.append((entry, f"[{_local(entry.at)}] {_LABELS[entry.kind]}: {text}"))

    def size() -> int:
        return sum(len(b) + 2 for _, b in blocks)

    omitted = 0
    summaries = [i for i, (e, _) in enumerate(blocks) if e.kind == "summary"]
    newest_summary = blocks[summaries[-1]][0] if summaries else None
    for drop in ("tool", "assistant", "user", "summary"):
        index = 0
        while size() > max_chars and index < len(blocks):
            entry, _ = blocks[index]
            if entry.kind == drop and entry is not newest_summary:
                del blocks[index]
                omitted += 1
            else:
                index += 1
    if size() > max_chars and blocks:
        entry, block = blocks[-1]
        keep = max(0, max_chars - (size() - len(block)) - 8)
        blocks[-1] = (entry, block[:keep] + " […]")

    # What the digest has seen: a summary written from it covers this much and
    # no more, even if the session goes on in another window meanwhile.
    seen = transcript.last_activity
    header = [
        f"Transcript {transcript.session_id} ({transcript.harness})",
        f"Path: {transcript.path}",
        f"Directory: {transcript.cwd or '?'}",
        f"Span: {_local(transcript.started)} → {_local(transcript.last_activity)}",
    ]
    if transcript.title:
        header.append(f"Title: {transcript.title}")
    if covered_at:
        header.append(f"Already covered until {_local(covered_at)}; showing what came after.")
    if omitted:
        header.append(
            f"{omitted} older messages left out to fit {max_chars} characters; "
            "`--max-chars` or `--all` shows more."
        )
    covered_flag = f" --covered-until {isoformat(seen)}" if seen else ""
    header.append(
        f"Write the summary with `codies-memory create session --transcript {transcript.session_id}"
        f"{covered_flag} ...`."
    )
    return "\n".join(header) + "\n\n" + "\n\n".join(b for _, b in blocks) + "\n"
