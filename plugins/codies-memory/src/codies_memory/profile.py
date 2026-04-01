"""Profile loading with layered inheritance and defaults for codies-memory."""

from __future__ import annotations

import copy
from pathlib import Path

import yaml

DEFAULT_PROFILE: dict = {
    "boot_mode": "operational",
    "write_gate_bias": "hold",
    "maintenance_cadence": "weekly",
    "capture_reflections": True,
    "capture_dreams": True,
    "promotion_overrides": {},
}


def load_profile(
    global_vault: Path,
    project_vault: Path | None = None,
) -> dict:
    """Load a merged profile from global and optional project vaults.

    Starts with a copy of DEFAULT_PROFILE, then layers global profile.yaml
    (if it exists), then layers project profile.yaml (if it exists).

    Args:
        global_vault: Path to the global vault root directory.
        project_vault: Optional path to the project vault root directory.

    Returns:
        Merged profile dict.
    """
    profile = copy.deepcopy(DEFAULT_PROFILE)

    global_profile_path = global_vault / "profile.yaml"
    if global_profile_path.exists():
        data = yaml.safe_load(global_profile_path.read_text()) or {}
        profile.update(data)

    if project_vault is not None:
        project_profile_path = project_vault / "profile.yaml"
        if project_profile_path.exists():
            data = yaml.safe_load(project_profile_path.read_text()) or {}
            profile.update(data)

    return profile


def get_boot_mode(profile: dict) -> str:
    """Return the boot_mode value from the profile, defaulting to 'operational'."""
    return profile.get("boot_mode", "operational")


def get_write_gate_bias(profile: dict) -> str:
    """Return the write_gate_bias value from the profile, defaulting to 'hold'."""
    return profile.get("write_gate_bias", "hold")


def get_promotion_overrides(profile: dict) -> dict:
    """Return the promotion_overrides value from the profile, defaulting to {}."""
    return profile.get("promotion_overrides", {})
