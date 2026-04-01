"""Tests for codies_memory.boot — boot assembly with layered budgets, truncation, caching."""

from __future__ import annotations

from pathlib import Path

import pytest

from codies_memory.boot import (
    assemble_boot,
    build_cache_key,
    cache_boot_packet,
    compute_layer_budgets,
    estimate_tokens,
    is_cache_valid,
    truncate_to_budget,
)


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

    def test_contains_required_keys(self) -> None:
        budgets = compute_layer_budgets(4000)
        assert "global_identity" in budgets
        assert "project_context" in budgets

    def test_global_identity_proportion(self) -> None:
        budgets = compute_layer_budgets(4000)
        assert budgets["global_identity"] >= 800

    def test_project_context_proportion(self) -> None:
        budgets = compute_layer_budgets(4000)
        assert budgets["project_context"] >= 1200


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

    def test_respects_total_budget(
        self, tmp_global_vault: Path, tmp_project_vault: Path
    ) -> None:
        # Write large content into identity
        large_text = " ".join(["alpha"] * 2000)
        (tmp_global_vault / "identity" / "self.md").write_text(large_text)

        # Write large content into project
        (tmp_project_vault / "project").mkdir(parents=True, exist_ok=True)
        large_project = " ".join(["beta"] * 2000)
        (tmp_project_vault / "project" / "overview.md").write_text(large_project)

        result = assemble_boot(tmp_global_vault, tmp_project_vault, budget=500)

        total_tokens = estimate_tokens(result["global_packet"]) + estimate_tokens(
            result["project_packet"]
        )
        assert total_tokens <= 600


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
