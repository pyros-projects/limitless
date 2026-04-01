"""Tests for codies_memory.promotion — promotion pipeline."""

from __future__ import annotations

import datetime
from pathlib import Path

import pytest

from codies_memory.promotion import (
    check_contradictions,
    elevate_trust,
    evaluate_for_promotion,
    promote_to_global,
    promote_within_project,
    set_probation,
)
from codies_memory.records import create_record, read_record
from codies_memory.inbox import capture


# ---------------------------------------------------------------------------
# TestEvaluateForPromotion
# ---------------------------------------------------------------------------

class TestEvaluateForPromotion:
    def test_inbox_allow_gate_session_count_eligible(self, tmp_project_vault: Path) -> None:
        """Inbox with gate='allow' and session_count >= 1 is eligible."""
        path = capture(tmp_project_vault, "Something worth promoting", source="chat", gate="allow")
        record = read_record(path)
        result = evaluate_for_promotion(record, context={"session_count": 1})
        assert result["eligible"] is True
        assert any(t in result["suggested_types"] for t in ("thread", "lesson"))

    def test_inbox_hold_gate_not_eligible(self, tmp_project_vault: Path) -> None:
        """Inbox with gate='hold' is not eligible for promotion."""
        path = capture(tmp_project_vault, "Held back note", source="chat", gate="hold")
        record = read_record(path)
        result = evaluate_for_promotion(record, context={"session_count": 5})
        assert result["eligible"] is False

    def test_thread_session_count_eligible(self, tmp_project_vault: Path) -> None:
        """Thread with session_count >= 2 is eligible; suggested_types includes 'decision'."""
        path = create_record(
            vault=tmp_project_vault,
            record_type="thread",
            scope="project",
            title="Open question about caching",
            body="Investigating this.",
        )
        record = read_record(path)
        result = evaluate_for_promotion(record, context={"session_count": 2, "references": 0})
        assert result["eligible"] is True
        assert "decision" in result["suggested_types"]

    def test_thread_references_eligible(self, tmp_project_vault: Path) -> None:
        """Thread with references >= 2 is eligible even without enough sessions."""
        path = create_record(
            vault=tmp_project_vault,
            record_type="thread",
            scope="project",
            title="Frequently referenced thread",
            body="Referenced multiple times.",
        )
        record = read_record(path)
        result = evaluate_for_promotion(record, context={"session_count": 0, "references": 2})
        assert result["eligible"] is True

    def test_thread_below_threshold_not_eligible(self, tmp_project_vault: Path) -> None:
        """Thread with insufficient session_count and references is not eligible."""
        path = create_record(
            vault=tmp_project_vault,
            record_type="thread",
            scope="project",
            title="Fresh thread",
            body="Just started.",
        )
        record = read_record(path)
        result = evaluate_for_promotion(record, context={"session_count": 1, "references": 1})
        assert result["eligible"] is False


# ---------------------------------------------------------------------------
# TestPromoteWithinProject
# ---------------------------------------------------------------------------

class TestPromoteWithinProject:
    def test_inbox_to_thread(self, tmp_project_vault: Path) -> None:
        """Promoting inbox to thread creates a record with type='thread', trust='working', probation_until set."""
        source = capture(tmp_project_vault, "Interesting recurring idea", source="chat", gate="allow")
        new_path = promote_within_project(source, "thread", tmp_project_vault)
        assert new_path.exists()
        new_record = read_record(new_path)
        fm = new_record["frontmatter"]
        assert fm["type"] == "thread"
        assert fm["trust"] == "working"
        assert fm.get("probation_until") is not None

    def test_thread_to_lesson(self, tmp_project_vault: Path) -> None:
        """Promoting thread to lesson creates a record with type='lesson'."""
        source = create_record(
            vault=tmp_project_vault,
            record_type="thread",
            scope="project",
            title="Lesson-worthy thread",
            body="This became a lesson.",
        )
        new_path = promote_within_project(source, "lesson", tmp_project_vault)
        assert new_path.exists()
        new_record = read_record(new_path)
        assert new_record["frontmatter"]["type"] == "lesson"

    def test_source_marked_archived(self, tmp_project_vault: Path) -> None:
        """Source record is marked as archived after promotion."""
        source = capture(tmp_project_vault, "Archived after promotion", source="chat", gate="allow")
        promote_within_project(source, "thread", tmp_project_vault)
        source_record = read_record(source)
        assert source_record["frontmatter"]["status"] == "archived"

    def test_invalid_promotion_path_raises(self, tmp_project_vault: Path) -> None:
        """Attempting an invalid promotion path raises ValueError."""
        source = create_record(
            vault=tmp_project_vault,
            record_type="lesson",
            scope="project",
            title="A lesson",
            body="Already a lesson.",
        )
        with pytest.raises(ValueError):
            promote_within_project(source, "thread", tmp_project_vault)


# ---------------------------------------------------------------------------
# TestPromoteToGlobal
# ---------------------------------------------------------------------------

class TestPromoteToGlobal:
    def test_project_lesson_to_global(
        self, tmp_project_vault: Path, tmp_global_vault: Path
    ) -> None:
        """Promoting a project lesson to global creates a record with scope='global' and id starting with 'LS-G'."""
        source = create_record(
            vault=tmp_project_vault,
            record_type="lesson",
            scope="project",
            title="Universal caching lesson",
            body="Always invalidate the cache on deploy.",
        )
        new_path = promote_to_global(source, tmp_global_vault)
        assert new_path.exists()
        new_record = read_record(new_path)
        fm = new_record["frontmatter"]
        assert fm["scope"] == "global"
        assert fm["id"].startswith("LS-G")

    def test_source_archived_after_global_promotion(
        self, tmp_project_vault: Path, tmp_global_vault: Path
    ) -> None:
        """Source record is archived after global promotion."""
        source = create_record(
            vault=tmp_project_vault,
            record_type="lesson",
            scope="project",
            title="Lesson to go global",
            body="Details here.",
        )
        promote_to_global(source, tmp_global_vault)
        source_record = read_record(source)
        assert source_record["frontmatter"]["status"] == "archived"

    def test_global_record_has_probation(
        self, tmp_project_vault: Path, tmp_global_vault: Path
    ) -> None:
        """New global record has probation_until set."""
        source = create_record(
            vault=tmp_project_vault,
            record_type="lesson",
            scope="project",
            title="Probation global lesson",
            body="Details.",
        )
        new_path = promote_to_global(source, tmp_global_vault)
        new_record = read_record(new_path)
        assert new_record["frontmatter"].get("probation_until") is not None

    def test_promote_to_global_rejects_thread(
        self, tmp_project_vault: Path, tmp_global_vault: Path
    ) -> None:
        """Promoting a thread to global raises ValueError."""
        source = create_record(
            vault=tmp_project_vault,
            record_type="thread",
            scope="project",
            title="A thread record",
            body="Thread content.",
        )
        with pytest.raises(ValueError, match="Only lessons can be promoted to global"):
            promote_to_global(source, tmp_global_vault)

    def test_promote_to_global_rejects_decision(
        self, tmp_project_vault: Path, tmp_global_vault: Path
    ) -> None:
        """Promoting a decision to global raises ValueError."""
        source = create_record(
            vault=tmp_project_vault,
            record_type="decision",
            scope="project",
            title="A decision record",
            body="Decision content.",
        )
        with pytest.raises(ValueError, match="Only lessons can be promoted to global"):
            promote_to_global(source, tmp_global_vault)


# ---------------------------------------------------------------------------
# TestElevateTrust
# ---------------------------------------------------------------------------

class TestElevateTrust:
    def test_working_to_confirmed(self, tmp_project_vault: Path) -> None:
        """Elevating from 'working' to 'confirmed' succeeds."""
        path = create_record(
            vault=tmp_project_vault,
            record_type="thread",
            scope="project",
            title="Trust elevation thread",
            body="Investigating.",
            trust="working",
        )
        elevate_trust(path, "confirmed")
        record = read_record(path)
        assert record["frontmatter"]["trust"] == "confirmed"

    def test_speculative_to_canonical_raises(self, tmp_project_vault: Path) -> None:
        """Skipping trust levels (speculative -> canonical) raises ValueError with 'Cannot elevate'."""
        path = create_record(
            vault=tmp_project_vault,
            record_type="thread",
            scope="project",
            title="Trust skip thread",
            body="Speculative content.",
            trust="speculative",
        )
        with pytest.raises(ValueError, match="Cannot elevate"):
            elevate_trust(path, "canonical")

    def test_confirmed_to_canonical(self, tmp_project_vault: Path) -> None:
        """Elevating from 'confirmed' to 'canonical' succeeds (one step)."""
        path = create_record(
            vault=tmp_project_vault,
            record_type="thread",
            scope="project",
            title="Nearly canonical",
            body="Almost there.",
            trust="confirmed",
        )
        elevate_trust(path, "canonical")
        record = read_record(path)
        assert record["frontmatter"]["trust"] == "canonical"

    def test_working_to_canonical_raises(self, tmp_project_vault: Path) -> None:
        """Skipping from 'working' to 'canonical' raises ValueError."""
        path = create_record(
            vault=tmp_project_vault,
            record_type="thread",
            scope="project",
            title="Big skip",
            body="Trying to jump.",
            trust="working",
        )
        with pytest.raises(ValueError, match="Cannot elevate"):
            elevate_trust(path, "canonical")

    def test_elevate_trust_rejects_demotion(self, tmp_project_vault: Path) -> None:
        """Demoting trust via elevate_trust() raises ValueError."""
        path = create_record(
            vault=tmp_project_vault,
            record_type="thread",
            scope="project",
            title="test",
            body="body",
            trust="confirmed",
        )
        with pytest.raises(ValueError, match="Cannot demote"):
            elevate_trust(path, "working")


# ---------------------------------------------------------------------------
# TestProbation
# ---------------------------------------------------------------------------

class TestProbation:
    def test_sets_probation_until_7_days(self, tmp_project_vault: Path) -> None:
        """set_probation sets probation_until to today + 7 days."""
        path = create_record(
            vault=tmp_project_vault,
            record_type="thread",
            scope="project",
            title="Probation test thread",
            body="Testing probation.",
        )
        set_probation(path)
        record = read_record(path)
        expected = str(datetime.date.today() + datetime.timedelta(days=7))
        assert record["frontmatter"]["probation_until"] == expected

    def test_sets_probation_custom_days(self, tmp_project_vault: Path) -> None:
        """set_probation accepts a custom number of days."""
        path = create_record(
            vault=tmp_project_vault,
            record_type="thread",
            scope="project",
            title="Custom probation thread",
            body="Testing custom days.",
        )
        set_probation(path, days=14)
        record = read_record(path)
        expected = str(datetime.date.today() + datetime.timedelta(days=14))
        assert record["frontmatter"]["probation_until"] == expected


# ---------------------------------------------------------------------------
# TestCheckContradictions
# ---------------------------------------------------------------------------

class TestCheckContradictions:
    def _make_record(self, title: str, body: str) -> dict:
        """Build a minimal record dict without writing to disk."""
        return {
            "frontmatter": {"id": f"TH-{hash(title) % 9999:04d}", "title": title},
            "body": body,
        }

    def test_no_contradictions_different_topics(self) -> None:
        """Two records about completely different topics have no contradictions."""
        record = self._make_record(
            "Caching strategy for Redis",
            "Use Redis with TTL of 300 seconds for session data.",
        )
        existing = [
            self._make_record(
                "Database migration playbook",
                "Run migrations in a transaction and roll back on failure.",
            )
        ]
        result = check_contradictions(record, existing)
        assert result["has_contradictions"] is False
        assert result["conflicts"] == []

    def test_flags_similar_titles_divergent_bodies(self) -> None:
        """Records with >0.7 title similarity and 0.3-0.9 body similarity are flagged."""
        record = self._make_record(
            "Caching strategy for the API layer",
            "Always use a short TTL (30s) to avoid stale responses. Never cache auth tokens.",
        )
        existing = [
            self._make_record(
                "Caching strategy for the API layer",
                "Use a long TTL (3600s) to maximise cache hits and reduce backend load significantly.",
            )
        ]
        result = check_contradictions(record, existing)
        assert result["has_contradictions"] is True
        assert len(result["conflicts"]) == 1
        assert result["conflicts"][0]["title_similarity"] > 0.7

    def test_identical_bodies_not_flagged(self) -> None:
        """Two records with identical bodies are not flagged (body similarity >= 0.9)."""
        body = "Use Redis with TTL of 300 seconds for all cache entries."
        record = self._make_record("Caching strategy for the API", body)
        existing = [self._make_record("Caching strategy for the API", body)]
        result = check_contradictions(record, existing)
        # body_ratio == 1.0, which is >= 0.9, so not a contradiction
        assert result["has_contradictions"] is False

    def test_empty_existing_records(self) -> None:
        """No existing records means no contradictions."""
        record = self._make_record("Some title", "Some body content.")
        result = check_contradictions(record, [])
        assert result["has_contradictions"] is False
