"""Tests for codies_memory.profile."""

from __future__ import annotations

from pathlib import Path

import pytest

from codies_memory.profile import (
    DEFAULT_PROFILE,
    get_boot_mode,
    get_promotion_overrides,
    get_write_gate_bias,
    load_profile,
)


class TestLoadProfile:
    """Tests for load_profile()."""

    def test_loads_global_profile(self, tmp_global_vault: Path) -> None:
        """Global vault with boot_mode: operational is loaded correctly."""
        profile = load_profile(tmp_global_vault)
        assert profile["boot_mode"] == "operational"
        assert profile["write_gate_bias"] == "hold"

    def test_project_overrides_global(
        self, tmp_global_vault: Path, tmp_project_vault: Path
    ) -> None:
        """Project profile overrides global; keys absent in project keep global value."""
        # Write a project profile that changes boot_mode but not write_gate_bias
        (tmp_project_vault / "profile.yaml").write_text("boot_mode: personal\n")

        profile = load_profile(tmp_global_vault, tmp_project_vault)

        assert profile["boot_mode"] == "personal"
        # write_gate_bias comes from the global profile (hold)
        assert profile["write_gate_bias"] == "hold"

    def test_missing_global_uses_defaults(self, tmp_path: Path) -> None:
        """When global vault dir has no profile.yaml, DEFAULT_PROFILE values apply."""
        empty_vault = tmp_path / "empty_vault"
        empty_vault.mkdir()

        profile = load_profile(empty_vault)

        for key, value in DEFAULT_PROFILE.items():
            assert profile[key] == value

    def test_missing_project_uses_global_only(self, tmp_global_vault: Path) -> None:
        """When project_vault is None, only the global profile is used."""
        profile = load_profile(tmp_global_vault, project_vault=None)

        assert profile["boot_mode"] == "operational"
        assert profile["write_gate_bias"] == "hold"


    def test_profile_deepcopy_isolation(self, tmp_path: Path) -> None:
        """Mutating a loaded profile's nested dict does not affect the next load."""
        vault = tmp_path / "vault"
        vault.mkdir()
        (vault / "profile.yaml").write_text("boot_mode: operational\n")
        p1 = load_profile(vault)
        p1["promotion_overrides"]["test"] = True
        p2 = load_profile(vault)
        assert "test" not in p2.get("promotion_overrides", {})


class TestProfileAccessors:
    """Tests for get_boot_mode, get_write_gate_bias, get_promotion_overrides."""

    def test_get_boot_mode_returns_value_when_present(self) -> None:
        profile = {"boot_mode": "mixed"}
        assert get_boot_mode(profile) == "mixed"

    def test_get_boot_mode_returns_default_when_absent(self) -> None:
        assert get_boot_mode({}) == "operational"

    def test_get_write_gate_bias_returns_value_when_present(self) -> None:
        profile = {"write_gate_bias": "allow"}
        assert get_write_gate_bias(profile) == "allow"

    def test_get_write_gate_bias_returns_default_when_absent(self) -> None:
        assert get_write_gate_bias({}) == "hold"

    def test_get_promotion_overrides_returns_empty_when_absent(self) -> None:
        assert get_promotion_overrides({}) == {}

    def test_get_promotion_overrides_returns_value_when_present(self) -> None:
        overrides = {"TH-0001": "promote", "TH-0002": "suppress"}
        profile = {"promotion_overrides": overrides}
        assert get_promotion_overrides(profile) == overrides
