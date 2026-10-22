"""Tests for codies_memory.boot — boot assembly with layered budgets, truncation, caching."""

from __future__ import annotations

from pathlib import Path

import pytest

from codies_memory.boot import (
    DAILY_LOG_TAIL_LINES,
    LATEST_REFLECTION_MAX_TOKENS,
    assemble_boot,
    build_cache_key,
    cache_boot_packet,
    compute_layer_budgets,
    estimate_tokens,
    is_cache_valid,
    truncate_to_budget,
)
from codies_memory.records import create_record, update_record


# ---------------------------------------------------------------------------
# TestEstimateTokens
# ---------------------------------------------------------------------------

class TestEstimateTokens:
    def test_empty_string_returns_zero(self) -> None:
        assert estimate_tokens("") == 0

    def test_short_sentence_is_approximate(self) -> None:
        result = estimate_tokens("hello world this is a test")
        assert 5 <= result <= 12


# ---------------------------------------------------------------------------
# TestComputeLayerBudgets
# ---------------------------------------------------------------------------

class TestComputeLayerBudgets:
    def test_sum_within_total(self) -> None:
        budgets = compute_layer_budgets(4000)
        assert sum(budgets.values()) <= 4000

    def test_identity_has_no_slice(self) -> None:
        # Identity is exempt from truncation, so it gets no budget slice.
        budgets = compute_layer_budgets(4000)
        assert "global_identity" not in budgets

    def test_contains_required_keys(self) -> None:
        budgets = compute_layer_budgets(4000)
        assert "global_procedural" in budgets
        assert "project_context" in budgets
        assert "project_working" in budgets
        assert "branch_session" in budgets

    def test_project_context_proportion(self) -> None:
        # Half of the budget goes to project context.
        budgets = compute_layer_budgets(4000)
        assert budgets["project_context"] >= 1900


# ---------------------------------------------------------------------------
# TestTruncateToBudget
# ---------------------------------------------------------------------------

class TestTruncateToBudget:
    def test_under_budget_unchanged(self) -> None:
        content = "short content"
        result = truncate_to_budget(content, budget=1000)
        assert result == content

    def test_over_budget_fits_within_budget(self) -> None:
        # Generate content that is definitely over a tiny budget
        content = " ".join(["word"] * 500)
        result = truncate_to_budget(content, budget=50)
        # Allow some slack: estimate_tokens of result should be close to budget
        assert estimate_tokens(result) <= 50 + 10

    def test_over_budget_contains_truncated_marker(self) -> None:
        content = " ".join(["word"] * 500)
        result = truncate_to_budget(content, budget=50)
        assert "[truncated]" in result


# ---------------------------------------------------------------------------
# TestAssembleBoot
# ---------------------------------------------------------------------------

class TestAssembleBoot:
    def test_produces_global_and_project_packets(
        self, tmp_global_vault: Path, tmp_project_vault: Path
    ) -> None:
        # Seed identity file
        (tmp_global_vault / "identity" / "self.md").write_text(
            "I am a helpful AI assistant with a persistent memory system."
        )
        # Seed project overview
        (tmp_project_vault / "project").mkdir(parents=True, exist_ok=True)
        (tmp_project_vault / "project" / "overview.md").write_text(
            "This project is a memory management system for AI agents."
        )

        result = assemble_boot(tmp_global_vault, tmp_project_vault)

        assert "global_packet" in result
        assert "project_packet" in result
        assert "helpful AI assistant" in result["global_packet"]
        assert "memory management system" in result["project_packet"]

    def test_identity_is_never_truncated(
        self, tmp_global_vault: Path, tmp_project_vault: Path
    ) -> None:
        # Identity larger than the entire budget must still surface in full.
        large_text = " ".join(["alpha"] * 2000)
        (tmp_global_vault / "identity" / "self.md").write_text(large_text)

        # Write large content into project
        (tmp_project_vault / "project").mkdir(parents=True, exist_ok=True)
        large_project = " ".join(["beta"] * 2000)
        (tmp_project_vault / "project" / "overview.md").write_text(large_project)

        result = assemble_boot(tmp_global_vault, tmp_project_vault, budget=500)

        assert large_text in result["global_packet"]
        # Non-identity layers still respect their budgets.
        assert estimate_tokens(result["project_packet"]) <= 600

    def test_reports_layer_usage(
        self, tmp_global_vault: Path, tmp_project_vault: Path
    ) -> None:
        (tmp_global_vault / "identity" / "self.md").write_text(
            "I am a helpful AI assistant."
        )
        (tmp_project_vault / "project").mkdir(parents=True, exist_ok=True)
        (tmp_project_vault / "project" / "overview.md").write_text(
            "Project overview text."
        )

        result = assemble_boot(tmp_global_vault, tmp_project_vault, budget=4000)

        usage = result["usage"]
        assert usage["identity"]["budget"] is None
        assert usage["identity"]["used"] > 0
        layers = usage["layers"]
        assert set(layers) == {
            "global_procedural",
            "project_context",
            "project_working",
            "branch_session",
        }
        assert layers["project_context"]["used"] > 0
        assert layers["project_context"]["budget"] == 2000
        assert usage["total"]["budget"] == sum(l["budget"] for l in layers.values())
        assert usage["total"]["used"] == sum(l["used"] for l in layers.values())

    def test_prefers_warm_summaries_when_present(
        self, tmp_global_vault: Path, tmp_project_vault: Path
    ) -> None:
        (tmp_global_vault / "identity" / "self.md").write_text("I am Codie.")
        (tmp_global_vault / "boot" / "global-summary.md").write_text("# Global Summary\nWarm global map.")
        (tmp_project_vault / "boot" / "project-summary.md").write_text("# Project Summary\nWarm project map.")
        (tmp_project_vault / "boot" / "recent-episodes.md").write_text("# Recent Episodes\nWarm recent map.")

        result = assemble_boot(tmp_global_vault, tmp_project_vault)

        assert "Warm global map." in result["global_packet"]
        assert "Warm project map." in result["project_packet"]
        assert "Warm recent map." in result["project_packet"]

    def test_boot_includes_latest_daily_log_tail(
        self, tmp_global_vault: Path, tmp_project_vault: Path
    ) -> None:
        (tmp_project_vault / "sessions" / "SS-20260613-current.md").write_text(
            "---\ntitle: Current Session\n---\nLatest project session stays first."
        )
        sessions = tmp_global_vault / "sessions"
        sessions.mkdir()
        lines = [
            f"- [[SS-20260613-{i:04d}]] Daily item {i:02d} (project-{i:02d})"
            for i in range(1, DAILY_LOG_TAIL_LINES + 6)
        ]
        (sessions / "2026-06-13.md").write_text(
            "---\n"
            "id: DL-20260613\n"
            "title: '2026-06-13'\n"
            "type: daily-log\n"
            "status: active\n"
            "trust: canonical\n"
            "scope: global\n"
            "created: '2026-06-13T12:00:00+02:00'\n"
            "updated: '2026-06-13T12:00:00+02:00'\n"
            "---\n\n"
            + "\n".join(lines)
            + "\n"
        )

        result = assemble_boot(tmp_global_vault, tmp_project_vault)

        assert "Latest project session stays first." in result["project_packet"]
        assert "## Global Daily Log" in result["project_packet"]
        assert "Daily item 01" not in result["project_packet"]
        assert f"Daily item {DAILY_LOG_TAIL_LINES + 5:02d}" in result["project_packet"]

    def test_global_only_boot_includes_daily_log_tail(
        self, tmp_global_vault: Path
    ) -> None:
        sessions = tmp_global_vault / "sessions"
        sessions.mkdir()
        lines = [
            f"- [[SS-20260614-{i:04d}]] Daily item {i:02d} (project-{i:02d})"
            for i in range(1, DAILY_LOG_TAIL_LINES + 4)
        ]
        (sessions / "2026-06-14.md").write_text(
            "---\n"
            "id: DL-20260614\n"
            "title: '2026-06-14'\n"
            "type: daily-log\n"
            "status: active\n"
            "trust: canonical\n"
            "scope: global\n"
            "created: '2026-06-14T12:00:00+02:00'\n"
            "updated: '2026-06-14T12:00:00+02:00'\n"
            "---\n\n"
            + "\n".join(lines)
            + "\n"
        )

        result = assemble_boot(tmp_global_vault, project_vault=None, budget=4000)

        assert result["project_packet"].startswith("## Global Daily Log")
        assert "Daily item 01" not in result["project_packet"]
        assert f"Daily item {DAILY_LOG_TAIL_LINES + 3:02d}" in result["project_packet"]
        assert "branch_session" in result["usage"]["layers"]


# ---------------------------------------------------------------------------
# TestBootCache
# ---------------------------------------------------------------------------

class TestBuildCacheKey:
    def test_cache_key_with_path_inputs(self) -> None:
        """build_cache_key handles Path inputs without raising."""
        key = build_cache_key(Path("/tmp/test"), Path("/tmp/project"), "main", "default", "operational", 4000)
        assert isinstance(key, str) and len(key) == 16

    def test_cache_key_with_date_inputs(self) -> None:
        """build_cache_key handles date inputs without raising."""
        from datetime import date
        key = build_cache_key(date.today(), date.today(), "main", "default", "operational", 4000)
        assert isinstance(key, str) and len(key) == 16


class TestBootCache:
    def test_cache_and_validate(self, tmp_path: Path) -> None:
        boot_dir = tmp_path / "boot"
        key = "abc123"
        packet = "# Boot packet content"
        manifest = {"files": ["identity/self.md"], "hash": "deadbeef"}

        cache_boot_packet(boot_dir, key, packet, manifest)

        assert is_cache_valid(boot_dir, key, manifest) is True

    def test_invalid_after_manifest_change(self, tmp_path: Path) -> None:
        boot_dir = tmp_path / "boot"
        key = "abc123"
        packet = "# Boot packet content"
        manifest_v1 = {"files": ["identity/self.md"], "hash": "aaa"}
        manifest_v2 = {"files": ["identity/self.md"], "hash": "bbb"}

        cache_boot_packet(boot_dir, key, packet, manifest_v1)

        assert is_cache_valid(boot_dir, key, manifest_v2) is False

    def test_missing_cache_returns_false(self, tmp_path: Path) -> None:
        boot_dir = tmp_path / "boot"
        boot_dir.mkdir()
        assert is_cache_valid(boot_dir, "nonexistent", {}) is False


class TestLatestReflection:
    def _reflection(self, vault: Path, title: str, body: str, created: str = "2026-10-22") -> Path:
        path = create_record(vault, "reflection", "global", title=title, body=body)
        update_record(path, created=created)
        return path

    def test_newest_reflection_is_in_the_global_packet_whole(self, tmp_global_vault: Path) -> None:
        self._reflection(tmp_global_vault, "On Older Things", "older body text", created="2026-10-14")
        self._reflection(tmp_global_vault, "On Newer Things", "newer body text\n\nsecond paragraph")

        result = assemble_boot(tmp_global_vault, project_vault=None)

        packet = result["global_packet"]
        assert "## Latest Reflection: RF-0002 On Newer Things" in packet
        assert "newer body text\n\nsecond paragraph" in packet
        assert "older body text" not in packet
        assert result["usage"]["latest_reflection"]["used"] > 0

    def test_same_day_reflections_pick_the_higher_id(self, tmp_global_vault: Path) -> None:
        self._reflection(tmp_global_vault, "First Today", "first body")
        self._reflection(tmp_global_vault, "Second Today", "second body")

        packet = assemble_boot(tmp_global_vault, project_vault=None)["global_packet"]

        assert "second body" in packet
        assert "first body" not in packet

    def test_reflection_is_outside_the_budget_but_capped(self, tmp_global_vault: Path) -> None:
        self._reflection(tmp_global_vault, "On Length", "word " * 5000)

        result = assemble_boot(tmp_global_vault, project_vault=None, budget=600)

        packet = result["global_packet"]
        assert "[truncated]" in packet
        assert "Full text: " in packet and "RF-0001" in packet
        reflection_part = "## Latest Reflection" + packet.split("## Latest Reflection")[1]
        assert estimate_tokens(reflection_part) <= LATEST_REFLECTION_MAX_TOKENS
        assert result["usage"]["latest_reflection"]["used"] <= LATEST_REFLECTION_MAX_TOKENS
        assert "latest_reflection" not in result["usage"]["layers"]

    def test_ids_compare_as_numbers(self, tmp_global_vault: Path) -> None:
        older = create_record(tmp_global_vault, "reflection", "global", title="Nine", body="nine body")
        newer = create_record(tmp_global_vault, "reflection", "global", title="Ten", body="ten body")
        update_record(older, id="RF-9999", created="2026-10-22")
        update_record(newer, id="RF-10000", created="2026-10-22")

        packet = assemble_boot(tmp_global_vault, project_vault=None)["global_packet"]

        assert "ten body" in packet
        assert "nine body" not in packet

    def test_no_reflection_means_no_section(self, tmp_global_vault: Path) -> None:
        result = assemble_boot(tmp_global_vault, project_vault=None)

        assert "Latest Reflection" not in result["global_packet"]
        assert result["usage"]["latest_reflection"]["used"] == 0


class TestGlobalOnlyBoot:
    def test_no_project_vault_returns_empty_project_packet(
        self, tmp_global_vault: Path
    ) -> None:
        (tmp_global_vault / "identity" / "self.md").write_text("I am Claude.")
        result = assemble_boot(tmp_global_vault, project_vault=None)
        assert "Claude" in result["global_packet"]
        assert result["project_packet"] == ""

    def test_no_project_vault_does_not_crash(
        self, tmp_global_vault: Path
    ) -> None:
        result = assemble_boot(tmp_global_vault, project_vault=None)
        assert isinstance(result, dict)


class TestNestedSessionDiscovery:
    def test_finds_sessions_in_yearly_subdirs(
        self, tmp_global_vault: Path, tmp_project_vault: Path
    ) -> None:
        # Create session in spec-defined nested layout
        year_dir = tmp_project_vault / "sessions" / "2026"
        year_dir.mkdir(parents=True)
        (year_dir / "2026-03-30-session-summary.md").write_text(
            "---\ntitle: Session\n---\nBuilt the memory system."
        )
        result = assemble_boot(tmp_global_vault, tmp_project_vault)
        assert "memory system" in result["project_packet"]
