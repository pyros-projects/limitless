"""Tests for codies_memory.schemas — record validation, parsing, and ID generation."""

from __future__ import annotations

from pathlib import Path

import pytest

from codies_memory.schemas import (
    REQUIRED_FIELDS,
    TRUST_LEVELS,
    TYPE_EXTRA_FIELDS,
    ValidationError,
    generate_id,
    parse_record,
    validate_frontmatter,
)


# ---------------------------------------------------------------------------
# TestValidateFrontmatter
# ---------------------------------------------------------------------------

class TestValidateFrontmatter:
    def test_valid_common_fields_pass(self, sample_frontmatter: dict) -> None:
        errors = validate_frontmatter(sample_frontmatter, "thread")
        assert errors == []

    def test_missing_required_field_returns_error(self, sample_frontmatter: dict) -> None:
        del sample_frontmatter["trust"]
        errors = validate_frontmatter(sample_frontmatter, "thread")
        assert any("trust" in e for e in errors), f"Expected 'trust' in errors: {errors}"

    def test_invalid_trust_level_returns_error(self, sample_frontmatter: dict) -> None:
        sample_frontmatter["trust"] = "bogus"
        errors = validate_frontmatter(sample_frontmatter, "thread")
        assert len(errors) > 0

    def test_invalid_scope_returns_error(self, sample_frontmatter: dict) -> None:
        sample_frontmatter["scope"] = "universe"
        errors = validate_frontmatter(sample_frontmatter, "thread")
        assert len(errors) > 0

    def test_valid_type_specific_fields_for_lesson(self, sample_frontmatter: dict) -> None:
        sample_frontmatter["type"] = "lesson"
        sample_frontmatter["scope"] = "project"
        sample_frontmatter["trigger"] = "when deploying to prod"
        sample_frontmatter["why"] = "avoids data loss"
        errors = validate_frontmatter(sample_frontmatter, "lesson")
        assert errors == []

    def test_provenance_fields_accepted(self, sample_frontmatter: dict) -> None:
        sample_frontmatter["captured_from"] = "slack"
        sample_frontmatter["capture_date"] = "2026-03-30"
        sample_frontmatter["original_created"] = "2026-01-01"
        errors = validate_frontmatter(sample_frontmatter, "thread")
        assert errors == []

    def test_validate_rejects_invalid_status(self) -> None:
        data = {
            "id": "TH-0001", "title": "t", "type": "thread", "status": "bogus",
            "trust": "working", "scope": "project", "created": "2026-04-01", "updated": "2026-04-01",
        }
        errors = validate_frontmatter(data, "thread")
        assert any("status" in e.lower() for e in errors)


# ---------------------------------------------------------------------------
# TestParseRecord
# ---------------------------------------------------------------------------

class TestParseRecord:
    def test_parses_valid_record_file(self, sample_record_file: Path) -> None:
        result = parse_record(sample_record_file)
        assert result["frontmatter"]["id"] == "TH-0001"
        assert result["frontmatter"]["type"] == "thread"
        assert "architecture" in result["body"]
        assert result["path"] == sample_record_file

    def test_missing_frontmatter_raises(self, tmp_path: Path) -> None:
        no_fm = tmp_path / "no-fm.md"
        no_fm.write_text("This file has no frontmatter at all.\n")
        with pytest.raises(ValidationError) as exc_info:
            parse_record(no_fm)
        assert "frontmatter" in str(exc_info.value).lower()

    def test_invalid_yaml_raises(self, tmp_path: Path) -> None:
        bad_yaml = tmp_path / "bad-yaml.md"
        bad_yaml.write_text("---\nkey: [unclosed bracket\n---\nbody\n")
        with pytest.raises(ValidationError):
            parse_record(bad_yaml)


# ---------------------------------------------------------------------------
# TestGenerateId
# ---------------------------------------------------------------------------

class TestGenerateId:
    def test_sequential_thread_in_project(self, tmp_project_vault: Path) -> None:
        result = generate_id("thread", "project", tmp_project_vault)
        assert result == "TH-0001"

    def test_sequential_increments(self, tmp_project_vault: Path) -> None:
        # Simulate an existing TH-0001 file
        (tmp_project_vault / "threads" / "TH-0001-something.md").write_text("")
        result = generate_id("thread", "project", tmp_project_vault)
        assert result == "TH-0002"

    def test_global_lesson_has_g_prefix(self, tmp_global_vault: Path) -> None:
        result = generate_id("lesson", "global", tmp_global_vault)
        assert result == "LS-G0001"

    def test_inbox_uses_timestamp_format(self, tmp_project_vault: Path) -> None:
        result = generate_id("inbox", "project", tmp_project_vault)
        assert result.startswith("IN-")
        # Format: IN-YYYYMMDD-XXXX (4 hex chars suffix)
        parts = result.split("-")
        assert len(parts) == 3
        assert len(parts[1]) == 8  # YYYYMMDD
        assert len(parts[2]) == 4  # 4 hex chars

    def test_session_uses_timestamp_format(self, tmp_project_vault: Path) -> None:
        result = generate_id("session", "project", tmp_project_vault)
        assert result.startswith("SS-")
        parts = result.split("-")
        assert len(parts) == 3
        assert len(parts[1]) == 8

    def test_reflection_sequential_global(self, tmp_global_vault: Path) -> None:
        result = generate_id("reflection", "global", tmp_global_vault)
        assert result == "RF-0001"

    def test_dream_sequential_global(self, tmp_global_vault: Path) -> None:
        result = generate_id("dream", "global", tmp_global_vault)
        assert result == "DR-0001"
