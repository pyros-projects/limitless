"""Favorite reflections and dreams: the agent's own picks, shown in full at every boot.

Each kind keeps one file in the global vault (``reflections/favorites.yaml``,
``dreams/favorites.yaml``) with up to five picks and why each was chosen.
Boot shows the picked records in full, never truncated and outside
``--budget``. Once an agent has picked, every new record of that kind makes the
pick due again: boot says so until the agent chooses again.
"""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path

import yaml

from codies_memory.records import list_records

FAVORITE_COUNT = 5
KINDS = {"reflections": "reflection", "dreams": "dream"}


class FavoritesError(ValueError):
    """A pick that cannot be saved (wrong count, unknown id, missing reason)."""


def favorites_path(global_vault: Path, kind: str) -> Path:
    return global_vault / kind / "favorites.yaml"


def _active_records(global_vault: Path, kind: str) -> list[dict]:
    return list_records(global_vault, KINDS[kind], scope="global", status="active")


def _id_number(record_id: str) -> int:
    number = re.search(r"(\d+)$", str(record_id or ""))
    return int(number.group(1)) if number else -1


def _newest_first_key(record: dict) -> tuple[str, int]:
    fm = record["frontmatter"]
    return str(fm.get("created") or ""), _id_number(fm.get("id"))


def _highest_id(global_vault: Path, kind: str) -> str:
    """The highest id of *kind*, whatever its status or date. Ids are sequential, so this
    is the one most recently written, even when it is backdated or archived later."""
    records = list_records(global_vault, KINDS[kind], scope="global")
    ids = [str(r["frontmatter"].get("id") or "") for r in records]
    return max(ids, key=_id_number, default="")


def newest_record(global_vault: Path, kind: str) -> dict | None:
    """The newest active record of *kind*: latest ``created``, then highest id number."""
    records = _active_records(global_vault, kind)
    return max(records, key=_newest_first_key) if records else None


def load_favorites(global_vault: Path, kind: str) -> dict | None:
    """The saved pick of *kind*, or None before the first pick.

    Raises :class:`FavoritesError` when the file cannot be read as a pick.
    """
    path = favorites_path(global_vault, kind)
    if not path.is_file():
        return None
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, ValueError, yaml.YAMLError) as exc:  # ValueError: bad UTF-8, impossible dates
        first_line = str(exc).splitlines()[0] if str(exc) else type(exc).__name__
        raise FavoritesError(f"{kind}/favorites.yaml is unreadable ({first_line})") from exc
    if not isinstance(data, dict) or not isinstance(data.get("favorites") or [], list):
        raise FavoritesError(f"{kind}/favorites.yaml does not hold a list of favorites")
    picks = [{**p, "id": str(p["id"])} for p in data.get("favorites") or []
             if isinstance(p, dict) and p.get("id")]
    return {"chosen": str(data.get("chosen") or ""), "after": str(data.get("after") or ""), "favorites": picks}


def save_favorites(global_vault: Path, kind: str, ids: list[str], reasons: list[str]) -> Path:
    """Validate and write a pick of *kind*; raises :class:`FavoritesError` when it does not hold."""
    records = {str(r["frontmatter"].get("id")): r for r in _active_records(global_vault, kind)}
    wanted = min(FAVORITE_COUNT, len(records))
    if len(ids) != wanted or len(set(ids)) != len(ids):
        raise FavoritesError(f"pick exactly {wanted} different {kind} (got {len(ids)})")
    unknown = [i for i in ids if i not in records]
    if unknown:
        raise FavoritesError(f"no active {KINDS[kind]} with id {', '.join(unknown)}")
    if len(reasons) != len(ids) or not all(r.strip() for r in reasons):
        raise FavoritesError("give one --why per pick, in the same order")
    data = {
        "chosen": date.today().isoformat(),
        "after": _highest_id(global_vault, kind),
        "favorites": [
            {"id": i, "title": str(records[i]["frontmatter"].get("title") or ""), "why": r.strip()}
            for i, r in zip(ids, reasons)
        ],
    }
    path = favorites_path(global_vault, kind)
    header = (f"# Five favorite {kind}, chosen by the agent. Boot shows them in full.\n"
              f"# Change with: codies-memory favorites {kind} ID ID ID --why ... --why ... --why ...\n")
    path.write_text(header + yaml.dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return path


def due_reason(global_vault: Path, kind: str) -> str:
    """Why the pick of *kind* is due again, or "" when it holds (or the agent never picked)."""
    try:
        current = load_favorites(global_vault, kind)
    except FavoritesError as exc:
        return f"{exc}; choosing again rewrites it"
    if current is None:
        return ""
    records = {str(r["frontmatter"].get("id")) for r in _active_records(global_vault, kind)}
    gone = [p["id"] for p in current["favorites"] if p["id"] not in records]
    if gone:
        return f"{', '.join(gone)} is no longer an active {KINDS[kind]}"
    highest = _highest_id(global_vault, kind)
    if _id_number(highest) > _id_number(current["after"]):
        return f"{highest} was written after you chose (pick made after {current['after'] or 'none'})"
    if len(current["favorites"]) < min(FAVORITE_COUNT, len(records)):
        return f"fewer than {FAVORITE_COUNT} picks"
    return ""


def render_favorites(global_vault: Path, kind: str) -> tuple[str, list[str]]:
    """Return the picked records of *kind* in full, plus their ids (nothing when the file is unreadable;
    boot then reports the pick as due)."""
    try:
        current = load_favorites(global_vault, kind)
    except FavoritesError:
        return "", []
    if not current or not current["favorites"]:
        return "", []
    records = {str(r["frontmatter"].get("id")): r for r in _active_records(global_vault, kind)}
    parts, ids = [], []
    for pick in current["favorites"]:
        record = records.get(pick["id"])
        if record is None:
            continue
        fm = record["frontmatter"]
        head = f"## Favorite {KINDS[kind].capitalize()}: {pick['id']} {fm.get('title', '')}".rstrip()
        why = f"*Why I keep it: {pick['why']}*" if pick.get("why") else ""
        parts.append("\n\n".join(p for p in [head, why, record["body"].strip()] if p))
        ids.append(pick["id"])
    return "\n\n---\n\n".join(parts), ids
