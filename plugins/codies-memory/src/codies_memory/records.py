"""Record CRUD, supersession chains, and type inference for codies-memory."""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path
from typing import Any

import yaml

from codies_memory.schemas import generate_id, parse_record, validate_frontmatter, ValidationError
from codies_memory.vault import resolve_path


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _slugify(title: str) -> str:
    """Lowercase, remove non-word chars, replace spaces with hyphens, max 60 chars."""
    slug = title.lower()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    slug = slug.strip("-")
    slug = slug[:60]
    return slug if slug else "untitled"


def _write_record(path: Path, frontmatter: dict[str, Any], body: str) -> None:
    """Write a record file with YAML frontmatter and markdown body."""
    yaml_text = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)
    content = f"---\n{yaml_text}---\n\n{body}\n"
    path.write_text(content, encoding="utf-8")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def create_record(
    vault: Path,
    record_type: str,
    scope: str,
    title: str,
    body: str,
    status: str = "active",
    trust: str = "working",
    **extra_fields: Any,
) -> Path:
    """Create a new record file in the vault.

    Generates an ID, builds frontmatter, validates it, resolves the target
    directory, and writes the file with a slugified name.

    Returns the path to the created file.
    """
    today = str(date.today())
    record_id = generate_id(record_type, scope, vault)

    frontmatter: dict[str, Any] = {
        "id": record_id,
        "title": title,
        "type": record_type,
        "status": status,
        "trust": trust,
        "scope": scope,
        "created": today,
        "updated": today,
    }
    frontmatter.update(extra_fields)

    errors = validate_frontmatter(frontmatter, record_type)
    if errors:
        raise ValidationError(f"Invalid frontmatter for new record: {errors}")

    target_dir = resolve_path(vault, record_type, scope)
    target_dir.mkdir(parents=True, exist_ok=True)

    slug = _slugify(title)
    filename = f"{record_id}-{slug}.md"
    path = target_dir / filename

    _write_record(path, frontmatter, body)
    return path


def read_record(filepath: Path) -> dict[str, Any]:
    """Read and parse a record file.

    Raises FileNotFoundError if the file does not exist.
    Returns a dict with 'frontmatter', 'body', and 'path' keys.
    """
    if not filepath.exists():
        raise FileNotFoundError(f"Record file not found: '{filepath}'")
    return parse_record(filepath)


def update_record(filepath: Path, **fields: Any) -> None:
    """Update frontmatter fields in an existing record file.

    Bumps the 'updated' date to today and rewrites the file.
    """
    record = read_record(filepath)
    frontmatter = record["frontmatter"]
    body = record["body"]

    frontmatter.update(fields)
    frontmatter["updated"] = str(date.today())

    record_type = frontmatter.get("type", "")
    errors = validate_frontmatter(frontmatter, record_type)
    if errors:
        raise ValidationError(f"Invalid frontmatter after update: {errors}")

    _write_record(filepath, frontmatter, body)


def supersede_record(
    old_path: Path,
    vault: Path,
    scope: str,
    new_title: str,
    new_body: str,
    **extra_fields: Any,
) -> Path:
    """Create a new record that supersedes an old one, linking both.

    - New record gets ``supersedes=<old_id>``
    - Old record gets ``superseded_by=<new_id>`` and ``status="superseded"``

    Returns the path to the new record.
    """
    old_record = read_record(old_path)
    old_id = old_record["frontmatter"]["id"]
    record_type = old_record["frontmatter"]["type"]

    new_path = create_record(
        vault=vault,
        record_type=record_type,
        scope=scope,
        title=new_title,
        body=new_body,
        supersedes=old_id,
        **extra_fields,
    )

    new_record = read_record(new_path)
    new_id = new_record["frontmatter"]["id"]

    update_record(old_path, superseded_by=new_id, status="superseded")

    return new_path


def list_records(
    vault: Path,
    record_type: str,
    scope: str = "project",
    **filters: Any,
) -> list[dict[str, Any]]:
    """List all records of a given type, with optional frontmatter filters.

    Returns a list of parsed record dicts (each with 'frontmatter', 'body', 'path').
    """
    target_dir = resolve_path(vault, record_type, scope)
    if not target_dir.is_dir():
        return []

    results: list[dict[str, Any]] = []
    for md_file in target_dir.glob("*.md"):
        try:
            record = parse_record(md_file)
        except Exception:
            continue

        # Apply filters — each filter must match a frontmatter value
        if all(record["frontmatter"].get(k) == v for k, v in filters.items()):
            results.append(record)

    return results


def infer_record_type(content: str, context: str | None = None) -> str:
    """Infer the most likely record type from free-form text.

    Pattern matching (case-insensitive):
    - lesson:     "I learned", "lesson:", "pattern:", "when X always/never/check/use",
                  "rule of thumb"
    - decision:   "we decided", "decision:", "chose", "going with", "will use"
    - dream:      2+ matches from: "corridor", "dream", "woke up", "floating",
                  "mirror", "surreal"
    - reflection: "something about", "what it means", "identity", "consciousness",
                  "trust.*feel", "what matters"
    - thread:     "investigating", "exploring", "open question", "need to figure out"
    - default:    "inbox"
    """
    text = content.lower()
    if context:
        text = text + " " + context.lower()

    # Lesson patterns
    lesson_patterns = [
        r"i learned",
        r"lesson:",
        r"pattern:",
        r"when \w+ (always|never|check|use)\b",
        r"rule of thumb",
    ]
    if any(re.search(p, text) for p in lesson_patterns):
        return "lesson"

    # Decision patterns
    decision_patterns = [
        r"we decided",
        r"decision:",
        r"chose\b",
        r"going with",
        r"will use",
    ]
    if any(re.search(p, text) for p in decision_patterns):
        return "decision"

    # Dream patterns — need 2+ hits
    dream_keywords = ["corridor", "dream", "woke up", "floating", "mirror", "surreal"]
    dream_hits = sum(1 for kw in dream_keywords if kw in text)
    if dream_hits >= 2:
        return "dream"

    # Reflection patterns
    reflection_patterns = [
        r"something about",
        r"what it means",
        r"identity",
        r"consciousness",
        r"trust.*feel",
        r"what matters",
    ]
    if any(re.search(p, text) for p in reflection_patterns):
        return "reflection"

    # Thread patterns
    thread_patterns = [
        r"investigating",
        r"exploring",
        r"open question",
        r"need to figure out",
    ]
    if any(re.search(p, text) for p in thread_patterns):
        return "thread"

    return "inbox"
