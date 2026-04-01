"""Tests for codies_memory.inbox — capture, aging, compaction, and gate management."""

from __future__ import annotations

import datetime
from pathlib import Path

import yaml
import pytest

from codies_memory.inbox import active_inbox, age_inbox, capture, compact, discard, pending_review
from codies_memory.records import read_record, update_record


# ---------------------------------------------------------------------------
# Helper: backdate an inbox record's created field
# ---------------------------------------------------------------------------

def _backdate(record_path: Path, days_ago: int) -> None:
    """Rewrite the record's frontmatter 'created' field to a backdated date."""
    record = read_record(record_path)
    frontmatter = record["frontmatter"]
    body = record["body"]

    new_date = datetime.date.today() - datetime.timedelta(days=days_ago)
    frontmatter["created"] = str(new_date)

    yaml_text = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)
    content = f"---\n{yaml_text}---\n\n{body}\n"
    record_path.write_text(content, encoding="utf-8")


# ---------------------------------------------------------------------------
# TestCapture
# ---------------------------------------------------------------------------

class TestCapture:
    def test_creates_inbox_record(self, tmp_project_vault: Path) -> None:
        path = capture(tmp_project_vault, "Some inbox note", source="chat")
        assert path.exists()
        record = read_record(path)
        assert record["frontmatter"]["type"] == "inbox"
        assert record["frontmatter"]["gate"] == "hold"

    def test_default_gate_is_hold(self, tmp_project_vault: Path) -> None:
        path = capture(tmp_project_vault, "Another note", source="chat")
        record = read_record(path)
        assert record["frontmatter"]["gate"] == "hold"

    def test_allow_gate_works(self, tmp_project_vault: Path) -> None:
        path = capture(tmp_project_vault, "Allowed note", source="chat", gate="allow")
        record = read_record(path)
        assert record["frontmatter"]["gate"] == "allow"

    def test_trust_is_speculative(self, tmp_project_vault: Path) -> None:
        path = capture(tmp_project_vault, "Speculative note", source="chat")
        record = read_record(path)
        assert record["frontmatter"]["trust"] == "speculative"


# ---------------------------------------------------------------------------
# TestAgeInbox
# ---------------------------------------------------------------------------

class TestAgeInbox:
    def test_fresh_items_untouched(self, tmp_project_vault: Path) -> None:
        capture(tmp_project_vault, "Fresh item today", source="chat")
        result = age_inbox(tmp_project_vault)
        assert len(result["aging"]) == 0
        assert len(result["stale"]) == 0

    def test_8_day_old_items_flagged_aging(self, tmp_project_vault: Path) -> None:
        path = capture(tmp_project_vault, "Eight day old item", source="chat")
        _backdate(path, days_ago=8)
        result = age_inbox(tmp_project_vault)
        assert len(result["aging"]) == 1
        assert len(result["stale"]) == 0

    def test_15_day_old_items_flagged_stale(self, tmp_project_vault: Path) -> None:
        path = capture(tmp_project_vault, "Fifteen day old item", source="chat")
        _backdate(path, days_ago=15)
        result = age_inbox(tmp_project_vault)
        assert len(result["aging"]) == 0
        assert len(result["stale"]) == 1


# ---------------------------------------------------------------------------
# TestCompact
# ---------------------------------------------------------------------------

class TestCompact:
    def test_marks_compacted(self, tmp_project_vault: Path) -> None:
        path = capture(tmp_project_vault, "Item to compact", source="chat")
        compact(path, target_record_id="LS-0001")
        record = read_record(path)
        assert record["frontmatter"]["compacted_into"] == "LS-0001"
        assert record["frontmatter"]["status"] == "archived"


# ---------------------------------------------------------------------------
# TestDiscard
# ---------------------------------------------------------------------------

class TestDiscard:
    def test_marks_discarded(self, tmp_project_vault: Path) -> None:
        path = capture(tmp_project_vault, "Item to discard", source="chat")
        discard(path)
        record = read_record(path)
        assert record["frontmatter"]["status"] == "archived"
        assert record["frontmatter"]["gate"] == "discard"


# ---------------------------------------------------------------------------
# TestActiveInbox
# ---------------------------------------------------------------------------

class TestActiveInbox:
    def test_active_inbox_returns_fresh_items(self, tmp_project_vault: Path) -> None:
        capture(vault=tmp_project_vault, content="Fresh observation", source="test", gate="allow")
        result = active_inbox(tmp_project_vault)
        assert len(result) == 1
        assert result[0]["frontmatter"]["title"] == "Fresh observation"

    def test_active_inbox_excludes_archived(self, tmp_project_vault: Path) -> None:
        path = capture(vault=tmp_project_vault, content="Will archive", source="test", gate="allow")
        update_record(path, status="archived")
        result = active_inbox(tmp_project_vault)
        assert len(result) == 0

    def test_active_inbox_empty_when_no_inbox_dir(self, tmp_project_vault: Path) -> None:
        import shutil
        inbox_dir = tmp_project_vault / "inbox"
        if inbox_dir.is_dir():
            shutil.rmtree(inbox_dir)
        result = active_inbox(tmp_project_vault)
        assert result == []


# ---------------------------------------------------------------------------
# TestPendingReview
# ---------------------------------------------------------------------------

class TestPendingReview:
    def test_returns_aging_and_stale_items(self, tmp_project_vault: Path) -> None:
        # Fresh item — should not appear in aging/stale
        capture(tmp_project_vault, "Fresh item", source="chat")

        # 10-day-old item — should appear as aging
        aging_path = capture(tmp_project_vault, "Ten day old item", source="chat")
        _backdate(aging_path, days_ago=10)

        result = pending_review(tmp_project_vault)
        assert len(result["aging"]) == 1
        assert len(result["stale"]) == 0

    def test_pending_review_includes_active_key(self, tmp_project_vault: Path) -> None:
        capture(vault=tmp_project_vault, content="Fresh observation", source="test", gate="allow")
        result = pending_review(tmp_project_vault)
        assert "active" in result
        assert len(result["active"]) == 1

    def test_pending_review_active_includes_all_ages(self, tmp_project_vault: Path) -> None:
        # Fresh item
        capture(tmp_project_vault, "Fresh item", source="chat")
        # Aging item
        aging_path = capture(tmp_project_vault, "Aging item", source="chat")
        _backdate(aging_path, days_ago=10)
        # Stale item
        stale_path = capture(tmp_project_vault, "Stale item", source="chat")
        _backdate(stale_path, days_ago=15)

        result = pending_review(tmp_project_vault)
        assert len(result["active"]) == 3
        assert len(result["aging"]) == 1
        assert len(result["stale"]) == 1
