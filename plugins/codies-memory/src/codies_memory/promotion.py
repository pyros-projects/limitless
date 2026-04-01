"""Promotion pipeline: evaluate, promote, trust elevation, and contradiction checking."""

from __future__ import annotations

import difflib
from datetime import date, timedelta
from pathlib import Path

from codies_memory.records import create_record, read_record, update_record


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_TRUST_ORDER: list[str] = ["speculative", "working", "confirmed", "canonical"]

_PROMOTION_PATHS: dict[str, set[str]] = {
    "inbox": {"thread", "lesson", "decision"},
    "thread": {"decision", "lesson"},
    "decision": {"lesson"},
}


# ---------------------------------------------------------------------------
# evaluate_for_promotion
# ---------------------------------------------------------------------------

def evaluate_for_promotion(record: dict, context: dict) -> dict:
    """Check whether a record is eligible for promotion.

    Args:
        record: A parsed record dict (with 'frontmatter' and 'body' keys).
        context: Supplemental context dict. May include 'session_count' and
                 'references' (int counts).

    Returns:
        A dict with keys:
          - 'eligible': bool
          - 'suggested_types': list of target type strings
          - 'reason': human-readable explanation
    """
    frontmatter = record.get("frontmatter", {})
    record_type = frontmatter.get("type", "")
    gate = frontmatter.get("gate", "hold")
    session_count = context.get("session_count", 0)
    references = context.get("references", 0)

    suggested_types: list[str] = []

    if record_type == "inbox":
        if gate == "hold":
            return {
                "eligible": False,
                "suggested_types": [],
                "reason": "Gate is 'hold'; record must be set to 'allow' before promotion.",
            }
        if session_count >= 1:
            suggested_types = ["thread", "lesson"]
            return {
                "eligible": True,
                "suggested_types": suggested_types,
                "reason": f"Inbox record with gate='{gate}' and session_count={session_count} is ready for promotion.",
            }
        return {
            "eligible": False,
            "suggested_types": [],
            "reason": "Inbox record has not appeared in enough sessions yet.",
        }

    if record_type == "thread":
        if session_count >= 2 or references >= 2:
            suggested_types = ["decision", "lesson"]
            return {
                "eligible": True,
                "suggested_types": suggested_types,
                "reason": (
                    f"Thread with session_count={session_count} and "
                    f"references={references} qualifies for promotion."
                ),
            }
        return {
            "eligible": False,
            "suggested_types": [],
            "reason": "Thread needs session_count >= 2 or references >= 2.",
        }

    return {
        "eligible": False,
        "suggested_types": [],
        "reason": f"No promotion path defined for type='{record_type}'.",
    }


# ---------------------------------------------------------------------------
# promote_within_project
# ---------------------------------------------------------------------------

def promote_within_project(
    source_path: Path,
    target_type: str,
    vault: Path,
    scope: str = "project",
) -> Path:
    """Promote a record to a higher type within the same project vault.

    Validates that the target type is a valid promotion from the source type,
    creates a new record with trust='working', sets a 7-day probation, and
    marks the source record as archived.

    Args:
        source_path: Path to the source record file.
        target_type: The type to promote to (e.g. 'thread', 'lesson').
        vault: Root path of the project vault.
        scope: Scope for the new record (default 'project').

    Returns:
        Path to the newly created record.

    Raises:
        ValueError: If the target_type is not a valid promotion from the source type.
    """
    source = read_record(source_path)
    frontmatter = source["frontmatter"]
    body = source["body"]
    source_type = frontmatter.get("type", "")

    allowed = _PROMOTION_PATHS.get(source_type, set())
    if target_type not in allowed:
        raise ValueError(
            f"Cannot promote from '{source_type}' to '{target_type}'. "
            f"Allowed targets: {sorted(allowed)}"
        )

    probation_until = str(date.today() + timedelta(days=7))

    new_path = create_record(
        vault=vault,
        record_type=target_type,
        scope=scope,
        title=frontmatter.get("title", ""),
        body=body,
        trust="working",
        probation_until=probation_until,
        promoted_from=frontmatter.get("id", ""),
    )

    update_record(source_path, status="archived")

    return new_path


# ---------------------------------------------------------------------------
# promote_to_global
# ---------------------------------------------------------------------------

def promote_to_global(source_path: Path, global_vault: Path) -> Path:
    """Promote a project-scoped lesson to the global vault.

    Creates a new record with scope='global' in the global vault, sets a
    7-day probation, and marks the source as archived.

    Args:
        source_path: Path to the source project record.
        global_vault: Root path of the global vault.

    Returns:
        Path to the newly created global record.
    """
    source = read_record(source_path)
    frontmatter = source["frontmatter"]
    body = source["body"]

    record_type = frontmatter.get("type", "")
    if record_type not in {"lesson"}:
        raise ValueError(
            f"Only lessons can be promoted to global. Got type='{record_type}'."
        )

    probation_until = str(date.today() + timedelta(days=7))

    new_path = create_record(
        vault=global_vault,
        record_type=frontmatter.get("type", "lesson"),
        scope="global",
        title=frontmatter.get("title", ""),
        body=body,
        trust=frontmatter.get("trust", "working"),
        probation_until=probation_until,
        promoted_from=frontmatter.get("id", ""),
    )

    update_record(source_path, status="archived")

    return new_path


# ---------------------------------------------------------------------------
# elevate_trust
# ---------------------------------------------------------------------------

def elevate_trust(record_path: Path, new_trust: str) -> None:
    """Elevate the trust level of a record by one step.

    Raises ValueError if the new trust level skips a level (i.e. jumps more
    than one step up the trust order), or if new_trust is not in _TRUST_ORDER.

    Args:
        record_path: Path to the record file to update.
        new_trust: The desired new trust level.

    Raises:
        ValueError: If the promotion skips a trust level.
    """
    if new_trust not in _TRUST_ORDER:
        raise ValueError(
            f"Unknown trust level '{new_trust}'. "
            f"Must be one of: {_TRUST_ORDER}"
        )

    record = read_record(record_path)
    current_trust = record["frontmatter"].get("trust", "speculative")

    if current_trust not in _TRUST_ORDER:
        # If current is something else (e.g. 'historical'), just allow
        update_record(record_path, trust=new_trust)
        return

    current_idx = _TRUST_ORDER.index(current_trust)
    new_idx = _TRUST_ORDER.index(new_trust)

    if new_idx < current_idx:
        raise ValueError(
            f"Cannot demote trust from '{current_trust}' to '{new_trust}' via elevate_trust(). "
            f"Use update_record() directly if demotion is intentional."
        )

    if new_idx > current_idx + 1:
        raise ValueError(
            f"Cannot elevate trust from '{current_trust}' to '{new_trust}': "
            f"skipping trust levels is not allowed."
        )

    update_record(record_path, trust=new_trust)


# ---------------------------------------------------------------------------
# set_probation
# ---------------------------------------------------------------------------

def set_probation(record_path: Path, days: int = 7) -> None:
    """Set the probation_until field on a record.

    Args:
        record_path: Path to the record file.
        days: Number of days from today (default 7).
    """
    probation_until = str(date.today() + timedelta(days=days))
    update_record(record_path, probation_until=probation_until)


# ---------------------------------------------------------------------------
# check_contradictions
# ---------------------------------------------------------------------------

def check_contradictions(record: dict, existing_records: list[dict]) -> dict:
    """Check a record for contradictions against a list of existing records.

    Uses SequenceMatcher to compare titles and bodies.  A conflict is flagged
    when title similarity > 0.7 AND body similarity is between 0.3 and 0.9
    (exclusive on both ends) — similar titles but meaningfully divergent bodies.

    Args:
        record: The new/candidate record dict (with 'frontmatter' and 'body').
        existing_records: List of existing record dicts to compare against.

    Returns:
        A dict with:
          - 'has_contradictions': bool
          - 'conflicts': list of dicts describing each conflict
    """
    title = record.get("frontmatter", {}).get("title", "")
    body = record.get("body", "")

    conflicts: list[dict] = []

    for existing in existing_records:
        existing_title = existing.get("frontmatter", {}).get("title", "")
        existing_body = existing.get("body", "")

        title_ratio = difflib.SequenceMatcher(
            None, title.lower(), existing_title.lower()
        ).ratio()

        body_ratio = difflib.SequenceMatcher(
            None, body.lower(), existing_body.lower()
        ).ratio()

        if title_ratio > 0.7 and 0.3 < body_ratio < 0.9:
            conflicts.append({
                "existing_id": existing.get("frontmatter", {}).get("id", ""),
                "existing_title": existing_title,
                "title_similarity": title_ratio,
                "body_similarity": body_ratio,
            })

    return {
        "has_contradictions": len(conflicts) > 0,
        "conflicts": conflicts,
    }
