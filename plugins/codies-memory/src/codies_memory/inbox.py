"""Inbox capture, aging, compaction, and gate management for codies-memory."""

from __future__ import annotations

import datetime
from pathlib import Path

from codies_memory.records import create_record, update_record
from codies_memory.schemas import parse_record
from codies_memory.vault import resolve_path


def capture(
    vault: Path,
    content: str,
    source: str,
    gate: str = "hold",
) -> Path:
    """Capture a new inbox record in the vault.

    Creates a record with type="inbox", scope="project", trust="speculative".
    The title is truncated to 80 characters from the content.

    Returns the path to the created record file.
    """
    return create_record(
        vault=vault,
        record_type="inbox",
        scope="project",
        trust="speculative",
        title=content[:80],
        body=content,
        gate=gate,
        source=[source],
    )


def age_inbox(vault: Path) -> dict:
    """Scan the inbox directory and classify records by age.

    Records are classified as:
    - "aging": created 7–14 days ago (>= 7 days, < 14 days)
    - "stale": created 14+ days ago

    Archived records are skipped.

    Returns a dict with keys "aging" and "stale", each a list of parsed record dicts.
    """
    inbox_dir = resolve_path(vault, "inbox", "project")

    aging: list[dict] = []
    stale: list[dict] = []

    if not inbox_dir.is_dir():
        return {"aging": aging, "stale": stale}

    today = datetime.date.today()

    for md_file in inbox_dir.glob("*.md"):
        try:
            record = parse_record(md_file)
        except Exception:
            continue

        frontmatter = record["frontmatter"]

        # Skip archived records
        if frontmatter.get("status") == "archived":
            continue

        created_raw = frontmatter.get("created")
        if created_raw is None:
            continue

        # Parse created date — may be a date object or a string
        if isinstance(created_raw, datetime.date):
            created_date = created_raw
        else:
            try:
                created_date = datetime.date.fromisoformat(str(created_raw))
            except ValueError:
                continue

        age_days = (today - created_date).days

        if age_days >= 14:
            stale.append(record)
        elif age_days >= 7:
            aging.append(record)

    return {"aging": aging, "stale": stale}


def active_inbox(vault: Path) -> list[dict]:
    """Return all non-archived inbox records regardless of age.

    Uses resolve_path(vault, "inbox", "project") to find the inbox directory.
    Parses each .md file and skips archived records.

    Returns a list of parsed record dicts.
    """
    inbox_dir = resolve_path(vault, "inbox", "project")

    if not inbox_dir.is_dir():
        return []

    results: list[dict] = []

    for md_file in inbox_dir.glob("*.md"):
        try:
            record = parse_record(md_file)
        except Exception:
            continue

        if record["frontmatter"].get("status") == "archived":
            continue

        results.append(record)

    return results


def compact(record_path: Path, target_record_id: str) -> None:
    """Mark an inbox record as compacted into another record.

    Sets compacted_into=target_record_id and status="archived".
    """
    update_record(record_path, compacted_into=target_record_id, status="archived")


def discard(record_path: Path) -> None:
    """Mark an inbox record as discarded.

    Sets status="archived" and gate="discard".
    """
    update_record(record_path, status="archived", gate="discard")


def pending_review(vault: Path) -> dict:
    """Return inbox records that need review.

    Returns a dict with keys:
    - "active": all non-archived inbox records (from active_inbox)
    - "aging": records 7–14 days old (from age_inbox)
    - "stale": records 14+ days old (from age_inbox)
    """
    aged = age_inbox(vault)
    return {
        "active": active_inbox(vault),
        "aging": aged["aging"],
        "stale": aged["stale"],
    }
