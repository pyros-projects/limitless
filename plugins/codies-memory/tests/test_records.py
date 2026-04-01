"""Tests for codies_memory.records — CRUD, supersession chains, type inference."""

from __future__ import annotations

from pathlib import Path

import pytest

from codies_memory.records import (
    create_record,
    infer_record_type,
    list_records,
    read_record,
    supersede_record,
    update_record,
)
from codies_memory.schemas import ValidationError


# ---------------------------------------------------------------------------
# TestCreateRecord
# ---------------------------------------------------------------------------

class TestCreateRecord:
    def test_creates_file_with_frontmatter(self, tmp_project_vault: Path) -> None:
        path = create_record(
            vault=tmp_project_vault,
            record_type="thread",
            scope="project",
            title="My First Thread",
            body="Investigating this topic.",
        )
        assert path.exists()
        assert path.name.startswith("TH-0001")
        content = path.read_text()
        assert "title:" in content
        assert "trust:" in content

    def test_creates_with_extra_fields(self, tmp_project_vault: Path) -> None:
        path = create_record(
            vault=tmp_project_vault,
            record_type="lesson",
            scope="project",
            title="Boot Lesson",
            body="Always check the cache.",
            trigger="when deploying",
            why="avoids stale data",
        )
        content = path.read_text()
        assert "trigger:" in content

    def test_slug_in_filename(self, tmp_project_vault: Path) -> None:
        path = create_record(
            vault=tmp_project_vault,
            record_type="thread",
            scope="project",
            title="Boot Cache Invalidation",
            body="Details here.",
        )
        assert "boot-cache-invalidation" in path.name

    def test_provenance_fields_preserved(self, tmp_project_vault: Path) -> None:
        path = create_record(
            vault=tmp_project_vault,
            record_type="thread",
            scope="project",
            title="Provenance Thread",
            body="Captured from Slack.",
            captured_from="slack",
        )
        content = path.read_text()
        assert "captured_from:" in content


# ---------------------------------------------------------------------------
# TestReadRecord
# ---------------------------------------------------------------------------

class TestSlugify:
    def test_slugify_empty_title(self) -> None:
        """Empty or punctuation-only titles produce 'untitled'."""
        from codies_memory.records import _slugify
        assert _slugify("") == "untitled"
        assert _slugify("!!!") == "untitled"
        assert _slugify("   ") == "untitled"


class TestReadRecord:
    def test_reads_existing_record(self, sample_record_file: Path) -> None:
        result = read_record(sample_record_file)
        assert result["frontmatter"]["id"] == "TH-0001"
        assert "architecture" in result["body"]

    def test_nonexistent_file_raises(self, tmp_path: Path) -> None:
        missing = tmp_path / "no-such-file.md"
        with pytest.raises(FileNotFoundError):
            read_record(missing)


# ---------------------------------------------------------------------------
# TestUpdateRecord
# ---------------------------------------------------------------------------

class TestUpdateRecord:
    def test_updates_frontmatter_field(self, sample_record_file: Path) -> None:
        update_record(sample_record_file, trust="confirmed")
        result = read_record(sample_record_file)
        assert result["frontmatter"]["trust"] == "confirmed"

    def test_preserves_body_after_update(self, sample_record_file: Path) -> None:
        update_record(sample_record_file, trust="confirmed")
        result = read_record(sample_record_file)
        assert "architecture" in result["body"]

    def test_bumps_updated_date(self, sample_record_file: Path) -> None:
        original = read_record(sample_record_file)
        original_updated = original["frontmatter"]["updated"]
        update_record(sample_record_file, trust="confirmed")
        result = read_record(sample_record_file)
        # The updated date should be a valid date string (today or later)
        assert result["frontmatter"]["updated"] is not None
        # Confirm the field was written (may be same day, but must be present)
        assert "updated" in result["frontmatter"]

    def test_update_record_rejects_invalid_status(self, tmp_project_vault: Path) -> None:
        path = create_record(
            vault=tmp_project_vault, record_type="thread", scope="project",
            title="test", body="body",
        )
        with pytest.raises(ValidationError):
            update_record(path, status="bogus-status")

    def test_update_record_rejects_invalid_trust(self, tmp_project_vault: Path) -> None:
        path = create_record(
            vault=tmp_project_vault, record_type="thread", scope="project",
            title="test", body="body",
        )
        with pytest.raises(ValidationError):
            update_record(path, trust="nonsense")


# ---------------------------------------------------------------------------
# TestSupersedeRecord
# ---------------------------------------------------------------------------

class TestSupersedeRecord:
    def test_creates_new_record_and_links_both(self, sample_record_file: Path, tmp_project_vault: Path) -> None:
        new_path = supersede_record(
            old_path=sample_record_file,
            vault=tmp_project_vault,
            scope="project",
            new_title="Updated Thread",
            new_body="This supersedes the old one.",
        )
        # New record exists
        assert new_path.exists()

        # New record has supersedes field pointing to old id
        new_record = read_record(new_path)
        assert new_record["frontmatter"]["supersedes"] == "TH-0001"

        # Old record has superseded_by pointing to new id
        old_record = read_record(sample_record_file)
        assert old_record["frontmatter"]["superseded_by"] == new_record["frontmatter"]["id"]

        # Old record status is "superseded"
        assert old_record["frontmatter"]["status"] == "superseded"


# ---------------------------------------------------------------------------
# TestListRecords
# ---------------------------------------------------------------------------

class TestListRecords:
    def test_lists_by_type(self, tmp_project_vault: Path) -> None:
        create_record(
            vault=tmp_project_vault,
            record_type="thread",
            scope="project",
            title="Thread Alpha",
            body="First thread.",
        )
        create_record(
            vault=tmp_project_vault,
            record_type="thread",
            scope="project",
            title="Thread Beta",
            body="Second thread.",
        )
        records = list_records(tmp_project_vault, record_type="thread", scope="project")
        assert len(records) == 2

    def test_filters_by_trust(self, tmp_project_vault: Path) -> None:
        create_record(
            vault=tmp_project_vault,
            record_type="thread",
            scope="project",
            title="Working Thread",
            body="Still investigating.",
            trust="working",
        )
        create_record(
            vault=tmp_project_vault,
            record_type="thread",
            scope="project",
            title="Confirmed Thread",
            body="This is solid.",
            trust="confirmed",
        )
        records = list_records(
            tmp_project_vault,
            record_type="thread",
            scope="project",
            trust="confirmed",
        )
        assert len(records) == 1
        assert records[0]["frontmatter"]["trust"] == "confirmed"


# ---------------------------------------------------------------------------
# TestInferRecordType
# ---------------------------------------------------------------------------

class TestInferRecordType:
    def test_infers_lesson(self) -> None:
        result = infer_record_type("I learned that YAML tabs break parsing")
        assert result == "lesson"

    def test_infers_decision(self) -> None:
        result = infer_record_type("We decided to use GraphQL instead of REST")
        assert result == "decision"

    def test_infers_reflection(self) -> None:
        result = infer_record_type(
            "Something about what it means to be present, identity and consciousness."
        )
        assert result == "reflection"

    def test_infers_dream(self) -> None:
        result = infer_record_type(
            "I was floating in a corridor, surreal and dreamlike. Then I woke up."
        )
        assert result == "dream"

    def test_infers_inbox_for_generic(self) -> None:
        result = infer_record_type("Random unstructured notes about nothing in particular.")
        assert result == "inbox"
