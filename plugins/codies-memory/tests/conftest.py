"""Shared fixtures for codies-memory tests."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest


@pytest.fixture
def tmp_global_vault(tmp_path: Path) -> Path:
    """Create a minimal global vault directory structure."""
    root = tmp_path / ".memory"
    for d in [
        "registry",
        "identity",
        "procedural/lessons",
        "procedural/skills",
        "procedural/playbooks",
        "threads",
        "decisions",
        "reflections",
        "dreams",
        "boot",
        "projects",
    ]:
        (root / d).mkdir(parents=True)
    # Seed default profile
    (root / "profile.yaml").write_text(
        "boot_mode: operational\nwrite_gate_bias: hold\n"
    )
    # Seed empty registry
    (root / "registry" / "projects.yaml").write_text("projects: []\n")
    # Seed identity file
    (root / "identity" / "self.md").write_text(
        "---\ntitle: self\ntype: identity\n---\n"
    )
    return root


@pytest.fixture
def tmp_project_vault(tmp_global_vault: Path) -> Path:
    """Create a minimal project vault directory structure under global vault."""
    root = tmp_global_vault / "projects" / "myproject"
    for d in [
        "project/branch-overlays",
        "threads",
        "decisions",
        "lessons",
        "sessions",
        "inbox",
        "boot",
    ]:
        (root / d).mkdir(parents=True, exist_ok=True)
    (root / "profile.yaml").write_text("project_name: myproject\n")
    return root


@pytest.fixture
def sample_frontmatter() -> dict:
    """Return a valid common frontmatter dict."""
    return {
        "id": "TH-0001",
        "title": "Test Thread",
        "type": "thread",
        "status": "active",
        "trust": "working",
        "scope": "project",
        "created": "2026-03-30",
        "updated": "2026-03-30",
    }


@pytest.fixture
def sample_record_file(tmp_project_vault: Path) -> Path:
    """Create a sample thread record file in a project vault."""
    content = """---
id: TH-0001
title: Test Thread
type: thread
status: active
trust: working
scope: project
created: "2026-03-30"
updated: "2026-03-30"
review_after: "2026-04-06"
---

This is a test thread about architecture decisions.
"""
    path = tmp_project_vault / "threads" / "TH-0001-test-thread.md"
    path.write_text(content)
    return path
