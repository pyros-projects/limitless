"""Record schemas: constants, validation, parsing, and ID generation for codies-memory."""

from __future__ import annotations

import re
import secrets
import sys
from datetime import date
from pathlib import Path
from typing import Any

import yaml


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

TRUST_LEVELS: set[str] = {"canonical", "confirmed", "working", "speculative", "historical"}

SCOPES: set[str] = {"project", "global"}

STATUSES: set[str] = {"active", "completed", "archived", "superseded"}

REQUIRED_FIELDS: set[str] = {"id", "title", "type", "status", "trust", "scope", "created", "updated"}

PROVENANCE_FIELDS: set[str] = {"captured_from", "capture_date", "original_created"}

# Extra fields allowed (but not required) per record type
TYPE_EXTRA_FIELDS: dict[str, set[str]] = {
    "thread": {"review_after", "related", "tags", "gate"},
    "decision": {"review_after", "related", "tags", "gate", "rationale", "alternatives"},
    "lesson": {"review_after", "related", "tags", "gate", "trigger", "why", "applies_to"},
    "session": {"review_after", "related", "tags", "gate", "mode", "next_step", "artifacts", "write_gate_summary"},
    "inbox": {"review_after", "related", "tags", "gate", "source", "compacted_into"},
    "reflection": {"review_after", "related", "tags", "gate", "mood", "horizon"},
    "dream": {"review_after", "related", "tags", "gate", "horizon"},
    "skill": {"review_after", "related", "tags", "gate", "applies_to"},
    "playbook": {"review_after", "related", "tags", "gate", "applies_to", "steps"},
    "project": {"review_after", "related", "tags", "gate", "description", "status_detail"},
    "identity": {"review_after", "related", "tags"},
}

# 2-letter prefix per record type
_ID_PREFIXES: dict[str, str] = {
    "thread": "TH",
    "decision": "DC",
    "lesson": "LS",
    "session": "SS",
    "inbox": "IN",
    "reflection": "RF",
    "dream": "DR",
    "skill": "SK",
    "playbook": "PB",
    "project": "PJ",
}

# Record types that use timestamp-based IDs instead of sequential
_TIMESTAMP_ID_TYPES: set[str] = {"inbox", "session"}

# Record types that get a "G" prefix in the number when scope is global
_GLOBAL_G_PREFIX_TYPES: set[str] = {"lesson", "thread", "decision"}

# Valid gate values (if provided)
_VALID_GATES: set[str] = {"open", "hold", "closed", "allow", "discard"}


# ---------------------------------------------------------------------------
# Exception
# ---------------------------------------------------------------------------

class ValidationError(Exception):
    """Raised when record validation or parsing fails."""


# ---------------------------------------------------------------------------
# validate_frontmatter
# ---------------------------------------------------------------------------

def validate_frontmatter(data: dict[str, Any], record_type: str) -> list[str]:
    """Validate frontmatter dict for the given record_type.

    Returns a list of error strings. An empty list means the frontmatter is valid.
    """
    errors: list[str] = []

    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"Missing required field: '{field}'")

    # Validate trust level
    if "trust" in data and data["trust"] not in TRUST_LEVELS:
        errors.append(
            f"Invalid trust level: '{data['trust']}'. Must be one of: {sorted(TRUST_LEVELS)}"
        )

    # Validate scope
    if "scope" in data and data["scope"] not in SCOPES:
        errors.append(
            f"Invalid scope: '{data['scope']}'. Must be one of: {sorted(SCOPES)}"
        )

    # Validate status
    if "status" in data and data["status"] not in STATUSES:
        errors.append(
            f"Invalid status: '{data['status']}'. Must be one of: {sorted(STATUSES)}"
        )

    # Validate gate if present
    if "gate" in data and data["gate"] not in _VALID_GATES:
        errors.append(
            f"Invalid gate: '{data['gate']}'. Must be one of: {sorted(_VALID_GATES)}"
        )

    # Soft-warn on unknown extra fields (do not reject)
    known = (
        REQUIRED_FIELDS
        | TYPE_EXTRA_FIELDS.get(record_type, set())
        | PROVENANCE_FIELDS
        | {"probation_until", "promoted_from", "supersedes", "superseded_by", "compacted_into"}
    )
    unknown = set(data.keys()) - known
    if unknown:
        print(
            f"Warning: unknown fields {sorted(unknown)} for record type '{record_type}'",
            file=sys.stderr,
        )

    return errors


# ---------------------------------------------------------------------------
# parse_record
# ---------------------------------------------------------------------------

def parse_record(filepath: Path) -> dict[str, Any]:
    """Parse a markdown record file into frontmatter, body, and path.

    The file must begin with a YAML frontmatter block delimited by ``---``.

    Returns a dict with keys:
      - ``frontmatter``: parsed YAML dict
      - ``body``: markdown body text (stripped)
      - ``path``: the original filepath

    Raises :class:`ValidationError` if:
      - No frontmatter block is found
      - The YAML is malformed
      - The parsed frontmatter is not a dict
    """
    text = filepath.read_text(encoding="utf-8")

    # Must start with ---
    if not text.startswith("---"):
        raise ValidationError(
            f"No frontmatter found in '{filepath}': file must begin with '---'"
        )

    # Split on ---: first segment is empty, second is YAML, rest is body
    # We look for the closing --- delimiter
    # Pattern: ^---\n ... \n---\n
    match = re.match(r"^---\n(.*?)\n---\n?(.*)", text, re.DOTALL)
    if match is None:
        # Try the case where file starts with --- and has a closing ---
        # but maybe on same line or different structure
        parts = text.split("---", 2)
        if len(parts) < 3:
            raise ValidationError(
                f"Malformed frontmatter in '{filepath}': missing closing '---'"
            )
        yaml_text = parts[1]
        body = parts[2].strip()
    else:
        yaml_text = match.group(1)
        body = match.group(2).strip()

    try:
        frontmatter = yaml.safe_load(yaml_text)
    except yaml.YAMLError as exc:
        raise ValidationError(
            f"Invalid YAML in frontmatter of '{filepath}': {exc}"
        ) from exc

    if not isinstance(frontmatter, dict):
        raise ValidationError(
            f"Frontmatter in '{filepath}' must be a YAML mapping, got: {type(frontmatter).__name__}"
        )

    return {
        "frontmatter": frontmatter,
        "body": body,
        "path": filepath,
    }


# ---------------------------------------------------------------------------
# generate_id
# ---------------------------------------------------------------------------

def generate_id(record_type: str, scope: str, vault_path: Path) -> str:
    """Generate a unique ID for a new record.

    Strategy:
      - Timestamp types (inbox, session): ``{PREFIX}-{YYYYMMDD}-{4 hex chars}``
      - Sequential types: scan target dir, find max existing number, increment.
        Global-scoped lesson/thread/decision get a "G" infix: e.g. ``LS-G0001``.

    Args:
        record_type: The type of record (e.g. "thread", "lesson").
        scope: Either "project" or "global".
        vault_path: Root path of the vault (project or global).

    Returns:
        A unique ID string.
    """
    from codies_memory.vault import resolve_path

    prefix = _ID_PREFIXES.get(record_type, record_type[:2].upper())

    if record_type in _TIMESTAMP_ID_TYPES:
        today = date.today().strftime("%Y%m%d")
        suffix = secrets.token_hex(2)  # 4 hex chars
        return f"{prefix}-{today}-{suffix}"

    # Sequential ID
    target_dir = resolve_path(vault_path, record_type, scope)

    # Determine whether this type gets a "G" prefix for global scope
    use_g_prefix = scope == "global" and record_type in _GLOBAL_G_PREFIX_TYPES

    if use_g_prefix:
        # Pattern matches e.g. LS-G0001
        pattern = re.compile(rf"^{re.escape(prefix)}-G(\d+)")
        number_format = "G{:04d}"
    else:
        # Pattern matches e.g. TH-0001
        pattern = re.compile(rf"^{re.escape(prefix)}-(\d+)")
        number_format = "{:04d}"

    max_num = 0
    if target_dir.is_dir():
        for f in target_dir.iterdir():
            m = pattern.match(f.name)
            if m:
                num = int(m.group(1))
                if num > max_num:
                    max_num = num

    next_num = max_num + 1
    number_str = number_format.format(next_num)
    return f"{prefix}-{number_str}"
