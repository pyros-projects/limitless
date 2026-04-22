"""Derived warm-memory artifacts for boot-time orientation."""

from __future__ import annotations

from pathlib import Path

from codies_memory.records import list_records, parse_record


def _first_content_line(text: str) -> str:
    """Return the first non-empty content line after frontmatter."""
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            text = parts[2]
    for line in text.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return ""


def _truncate_line(text: str, limit: int = 140) -> str:
    """Return a short single-line excerpt."""
    clean = " ".join(text.split())
    if len(clean) <= limit:
        return clean
    return clean[: limit - 3].rstrip() + "..."


def _summarize_identity_file(path: Path) -> str | None:
    if not path.exists():
        return None
    excerpt = _truncate_line(_first_content_line(path.read_text(encoding="utf-8")))
    if not excerpt:
        return None
    return f"- `{path.stem}`: {excerpt}"


def _summarize_record_line(record: dict, extra_key: str | None = None) -> str:
    fm = record["frontmatter"]
    title = fm.get("title", "(no title)")
    line = f"- `{fm.get('id', '')}` {title}"
    if extra_key and fm.get(extra_key):
        line += f" — {fm[extra_key]}"
    return line


def build_global_summary(global_vault: Path) -> str:
    """Build a concise global summary from canonical files."""
    lines: list[str] = ["# Global Summary", ""]

    identity_lines = [
        _summarize_identity_file(global_vault / "identity" / "self.md"),
        _summarize_identity_file(global_vault / "identity" / "user.md"),
        _summarize_identity_file(global_vault / "identity" / "rules.md"),
    ]
    identity_lines = [line for line in identity_lines if line]
    if identity_lines:
        lines.extend(["## Identity", *identity_lines, ""])

    lessons = list_records(global_vault, "lesson", scope="global")
    if lessons:
        lines.append("## Global Lessons")
        for record in lessons[:5]:
            lines.append(_summarize_record_line(record, extra_key="applies_to"))
        lines.append("")

    skills_dir = global_vault / "procedural" / "skills"
    skill_files = sorted(skills_dir.glob("*.md"))[:5] if skills_dir.is_dir() else []
    if skill_files:
        lines.append("## Procedural Skills")
        for skill_file in skill_files:
            lines.append(f"- `{skill_file.stem}`")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def build_project_summary(project_vault: Path) -> str:
    """Build a concise project summary from canonical project files."""
    lines: list[str] = ["# Project Summary", ""]

    project_dir = project_vault / "project"
    overview_files = sorted(project_dir.glob("*.md")) if project_dir.is_dir() else []
    overview_lines: list[str] = []
    for overview_file in overview_files:
        if overview_file.parent.name == "branch-overlays":
            continue
        excerpt = _truncate_line(_first_content_line(overview_file.read_text(encoding="utf-8")))
        if excerpt:
            overview_lines.append(f"- `{overview_file.stem}`: {excerpt}")
    if overview_lines:
        lines.extend(["## Project Context", *overview_lines, ""])

    decisions = list_records(project_vault, "decision", scope="project", status="active")
    if decisions:
        lines.append("## Active Decisions")
        for record in decisions[:5]:
            lines.append(_summarize_record_line(record, extra_key="rationale"))
        lines.append("")

    threads = list_records(project_vault, "thread", scope="project", status="active")
    if threads:
        lines.append("## Active Threads")
        for record in threads[:5]:
            lines.append(_summarize_record_line(record))
        lines.append("")

    lessons = list_records(project_vault, "lesson", scope="project")
    if lessons:
        lines.append("## Recent Lessons")
        for record in lessons[:3]:
            lines.append(_summarize_record_line(record, extra_key="trigger"))
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def build_recent_episodes(project_vault: Path) -> str:
    """Build a bounded recent-episodes summary from latest sessions."""
    lines: list[str] = ["# Recent Episodes", ""]

    sessions_dir = project_vault / "sessions"
    session_files = sorted(sessions_dir.rglob("*.md"))[-3:] if sessions_dir.is_dir() else []
    if not session_files:
        return "\n".join(lines).rstrip() + "\n"

    for session_file in reversed(session_files):
        record = parse_record(session_file)
        fm = record["frontmatter"]
        title = fm.get("title", session_file.stem)
        next_step = fm.get("next_step")
        excerpt = _truncate_line(_first_content_line(record["body"]))
        lines.append(f"## {title}")
        if excerpt:
            lines.append(excerpt)
        if next_step:
            lines.append(f"Next: {next_step}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def write_warm_artifacts(
    global_vault: Path,
    project_vault: Path | None = None,
) -> dict[str, Path]:
    """Write warm-memory artifacts and return their paths."""
    written: dict[str, Path] = {}

    global_summary = global_vault / "boot" / "global-summary.md"
    global_summary.parent.mkdir(parents=True, exist_ok=True)
    global_summary.write_text(build_global_summary(global_vault), encoding="utf-8")
    written["global_summary"] = global_summary

    if project_vault is not None:
        project_summary = project_vault / "boot" / "project-summary.md"
        recent_episodes = project_vault / "boot" / "recent-episodes.md"
        project_summary.parent.mkdir(parents=True, exist_ok=True)
        project_summary.write_text(build_project_summary(project_vault), encoding="utf-8")
        recent_episodes.write_text(build_recent_episodes(project_vault), encoding="utf-8")
        written["project_summary"] = project_summary
        written["recent_episodes"] = recent_episodes

    return written
