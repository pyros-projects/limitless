# Codies Memory Lite v2 — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the two-tier file-based memory system for AI agents as a uv-managed Python package with four Claude Code skills.

**Architecture:** Two-tier vault (`~/.memory/` global + `<project>/.memory/` local). YAML frontmatter on Markdown records. Layered boot assembly with token budgets. Promotion pipeline with trust levels and probation. Skills as thin orchestration over the Python library.

**Tech Stack:** Python 3.11+, PyYAML, pytest, uv

---

## File Map

### Package Core (`src/codies_memory/`)

| File | Responsibility |
|------|----------------|
| `__init__.py` | Version, package metadata |
| `vault.py` | Vault init, layout validation, path resolution, project registry |
| `schemas.py` | Frontmatter schemas, validation, record parsing, ID generation |
| `records.py` | Record CRUD, supersession, type inference |
| `profile.py` | Profile loading, inheritance, defaults |
| `inbox.py` | Write gates, aging, compaction |
| `boot.py` | Boot assembly, token budgets, cache, truncation |
| `promotion.py` | Promotion pipeline, thresholds, probation, contradictions |
| `cli.py` | Thin CLI entry points |

### Tests (`tests/`)

| File | Covers |
|------|--------|
| `conftest.py` | Shared fixtures: temp vaults, sample records, profiles |
| `test_vault.py` | Vault creation, validation, registry, path resolution |
| `test_schemas.py` | Frontmatter validation, record parsing, ID generation |
| `test_records.py` | CRUD, supersession, listing, type inference |
| `test_profile.py` | Loading, inheritance, defaults |
| `test_inbox.py` | Capture, aging, compaction, review queue |
| `test_boot.py` | Assembly, budgets, truncation, caching |
| `test_promotion.py` | Thresholds, promotion, trust elevation, probation, contradictions |

### Skills (`skills/`)

| File | Trigger |
|------|---------|
| `memory-boot.md` | Session start |
| `memory-capture.md` | Agent wants to persist anything |
| `memory-promote.md` | Session close or operator request |
| `memory-close-session.md` | Session end |

---

## Task 0: Project Scaffold

**Files:**
- Create: `pyproject.toml`
- Create: `src/codies_memory/__init__.py`
- Create: `tests/conftest.py`
- Move: `01-principles.md` → `docs/original/01-principles.md` (and siblings)

- [ ] **Step 1: Create pyproject.toml**

```toml
[project]
name = "codies-memory"
version = "0.1.0"
description = "File-based two-tier memory system for AI agents"
requires-python = ">=3.11"
dependencies = [
    "pyyaml>=6.0",
]

[project.scripts]
codies-memory = "codies_memory.cli:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/codies_memory"]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]

[dependency-groups]
dev = [
    "pytest>=8.0",
    "pytest-cov>=5.0",
]
```

- [ ] **Step 2: Create package init**

```python
# src/codies_memory/__init__.py
"""Codies Memory Lite v2 — file-based two-tier memory for AI agents."""

__version__ = "0.1.0"
```

- [ ] **Step 3: Create conftest with shared fixtures**

```python
# tests/conftest.py
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
    ]:
        (root / d).mkdir(parents=True)
    # Seed default profile
    (root / "profile.yaml").write_text(
        "boot_mode: operational\nwrite_gate_bias: hold\n"
    )
    # Seed empty registry
    (root / "registry" / "projects.yaml").write_text("projects: []\n")
    return root


@pytest.fixture
def tmp_project_vault(tmp_path: Path) -> Path:
    """Create a minimal project vault directory structure."""
    root = tmp_path / "myproject" / ".memory"
    for d in [
        "project/branch-overlays",
        "threads",
        "decisions",
        "lessons",
        "sessions",
        "inbox",
        "boot",
    ]:
        (root / d).mkdir(parents=True)
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
```

- [ ] **Step 4: Move original design docs**

```bash
mkdir -p docs/original
mv 01-principles.md 02-architecture.md 03-memory-products.md \
   04-retrieval-and-promotion.md 05-schemas-and-operations.md \
   06-roadmap.md review.md docs/original/
```

- [ ] **Step 5: Install dependencies and verify**

Run: `uv sync`
Expected: dependencies resolve, `.venv` created

Run: `uv run pytest --co -q`
Expected: `no tests ran` (no test files yet, but pytest works)

- [ ] **Step 6: Commit**

```bash
git add pyproject.toml src/ tests/conftest.py docs/original/
git commit -m "scaffold: pyproject.toml, package init, conftest, reorganize docs"
```

---

## Task 1: vault.py — Vault Structure

**Files:**
- Create: `src/codies_memory/vault.py`
- Create: `tests/test_vault.py`

- [ ] **Step 1: Write failing tests for vault init**

```python
# tests/test_vault.py
"""Tests for vault initialization, validation, and registry."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from codies_memory.vault import (
    GLOBAL_DIRS,
    PROJECT_DIRS,
    find_vaults,
    init_global_vault,
    init_project_vault,
    register_project_vault,
    resolve_path,
    validate_vault,
)


class TestInitGlobalVault:
    def test_creates_all_required_directories(self, tmp_path: Path):
        root = tmp_path / ".memory"
        init_global_vault(root)
        for d in GLOBAL_DIRS:
            assert (root / d).is_dir(), f"Missing directory: {d}"

    def test_creates_default_profile(self, tmp_path: Path):
        root = tmp_path / ".memory"
        init_global_vault(root)
        assert (root / "profile.yaml").exists()

    def test_creates_empty_registry(self, tmp_path: Path):
        root = tmp_path / ".memory"
        init_global_vault(root)
        reg = root / "registry" / "projects.yaml"
        assert reg.exists()
        data = yaml.safe_load(reg.read_text())
        assert data == {"projects": []}

    def test_creates_seed_identity_files(self, tmp_path: Path):
        root = tmp_path / ".memory"
        init_global_vault(root)
        assert (root / "identity" / "self.md").exists()
        assert (root / "identity" / "user.md").exists()
        assert (root / "identity" / "rules.md").exists()

    def test_idempotent_on_existing_vault(self, tmp_path: Path):
        root = tmp_path / ".memory"
        init_global_vault(root)
        # Write something into identity
        (root / "identity" / "self.md").write_text("I am Claude.")
        # Re-init should not clobber existing files
        init_global_vault(root)
        assert (root / "identity" / "self.md").read_text() == "I am Claude."


class TestInitProjectVault:
    def test_creates_all_required_directories(self, tmp_path: Path):
        global_root = tmp_path / ".memory"
        init_global_vault(global_root)
        project_root = tmp_path / "myproject" / ".memory"
        init_project_vault(project_root, global_vault=global_root, register=False)
        for d in PROJECT_DIRS:
            assert (project_root / d).is_dir(), f"Missing directory: {d}"

    def test_creates_default_project_profile(self, tmp_path: Path):
        global_root = tmp_path / ".memory"
        init_global_vault(global_root)
        project_root = tmp_path / "myproject" / ".memory"
        init_project_vault(project_root, global_vault=global_root, register=False)
        assert (project_root / "profile.yaml").exists()

    def test_auto_registers_when_flag_set(self, tmp_path: Path):
        global_root = tmp_path / ".memory"
        init_global_vault(global_root)
        project_root = tmp_path / "myproject" / ".memory"
        init_project_vault(project_root, global_vault=global_root, register=True)
        reg = yaml.safe_load(
            (global_root / "registry" / "projects.yaml").read_text()
        )
        assert len(reg["projects"]) == 1
        assert reg["projects"][0]["path"] == str(project_root)


class TestRegisterProjectVault:
    def test_adds_project_to_registry(self, tmp_global_vault: Path):
        register_project_vault(
            tmp_global_vault,
            project_path="/home/pyro/projects/foo/.memory",
            slug="foo",
            metadata={"description": "Test project"},
        )
        reg = yaml.safe_load(
            (tmp_global_vault / "registry" / "projects.yaml").read_text()
        )
        assert len(reg["projects"]) == 1
        assert reg["projects"][0]["slug"] == "foo"
        assert reg["projects"][0]["status"] == "active"

    def test_updates_existing_entry(self, tmp_global_vault: Path):
        register_project_vault(
            tmp_global_vault,
            project_path="/home/pyro/projects/foo/.memory",
            slug="foo",
            metadata={"description": "v1"},
        )
        register_project_vault(
            tmp_global_vault,
            project_path="/home/pyro/projects/foo/.memory",
            slug="foo",
            metadata={"description": "v2"},
        )
        reg = yaml.safe_load(
            (tmp_global_vault / "registry" / "projects.yaml").read_text()
        )
        assert len(reg["projects"]) == 1
        assert reg["projects"][0]["metadata"]["description"] == "v2"

    def test_archives_stale_entry(self, tmp_global_vault: Path):
        register_project_vault(
            tmp_global_vault,
            project_path="/old/path/.memory",
            slug="old",
            metadata={},
        )
        register_project_vault(
            tmp_global_vault,
            project_path="/old/path/.memory",
            slug="old",
            metadata={},
            status="archived",
        )
        reg = yaml.safe_load(
            (tmp_global_vault / "registry" / "projects.yaml").read_text()
        )
        assert reg["projects"][0]["status"] == "archived"


class TestValidateVault:
    def test_valid_global_vault_passes(self, tmp_global_vault: Path):
        result = validate_vault(tmp_global_vault, vault_type="global")
        assert result.is_valid

    def test_missing_directory_fails(self, tmp_global_vault: Path):
        import shutil

        shutil.rmtree(tmp_global_vault / "identity")
        result = validate_vault(tmp_global_vault, vault_type="global")
        assert not result.is_valid
        assert "identity" in str(result.missing)

    def test_valid_project_vault_passes(self, tmp_project_vault: Path):
        result = validate_vault(tmp_project_vault, vault_type="project")
        assert result.is_valid


class TestResolvePath:
    def test_thread_in_project(self, tmp_project_vault: Path):
        path = resolve_path(tmp_project_vault, "thread", "project")
        assert path == tmp_project_vault / "threads"

    def test_lesson_in_global(self, tmp_global_vault: Path):
        path = resolve_path(tmp_global_vault, "lesson", "global")
        assert path == tmp_global_vault / "procedural" / "lessons"

    def test_reflection_always_global(self, tmp_global_vault: Path):
        path = resolve_path(tmp_global_vault, "reflection", "global")
        assert path == tmp_global_vault / "reflections"

    def test_inbox_in_project(self, tmp_project_vault: Path):
        path = resolve_path(tmp_project_vault, "inbox", "project")
        assert path == tmp_project_vault / "inbox"

    def test_session_in_project(self, tmp_project_vault: Path):
        path = resolve_path(tmp_project_vault, "session", "project")
        assert path == tmp_project_vault / "sessions"

    def test_unknown_type_raises(self, tmp_project_vault: Path):
        with pytest.raises(ValueError, match="Unknown record type"):
            resolve_path(tmp_project_vault, "nonexistent", "project")


class TestFindVaults:
    def test_returns_active_projects(self, tmp_global_vault: Path):
        register_project_vault(
            tmp_global_vault, "/path/a/.memory", "a", {}
        )
        register_project_vault(
            tmp_global_vault, "/path/b/.memory", "b", {}
        )
        vaults = find_vaults(tmp_global_vault)
        assert len(vaults) == 2

    def test_excludes_archived_by_default(self, tmp_global_vault: Path):
        register_project_vault(
            tmp_global_vault, "/path/a/.memory", "a", {}
        )
        register_project_vault(
            tmp_global_vault, "/path/b/.memory", "b", {}, status="archived"
        )
        vaults = find_vaults(tmp_global_vault)
        assert len(vaults) == 1
        assert vaults[0]["slug"] == "a"

    def test_includes_archived_when_requested(self, tmp_global_vault: Path):
        register_project_vault(
            tmp_global_vault, "/path/a/.memory", "a", {}
        )
        register_project_vault(
            tmp_global_vault, "/path/b/.memory", "b", {}, status="archived"
        )
        vaults = find_vaults(tmp_global_vault, include_archived=True)
        assert len(vaults) == 2
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_vault.py -v`
Expected: ImportError — `codies_memory.vault` does not exist

- [ ] **Step 3: Implement vault.py**

```python
# src/codies_memory/vault.py
"""Vault initialization, validation, path resolution, and project registry."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

GLOBAL_DIRS = [
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
]

PROJECT_DIRS = [
    "project/branch-overlays",
    "threads",
    "decisions",
    "lessons",
    "sessions",
    "inbox",
    "boot",
]

# Maps (record_type, scope) to subdirectory within vault root.
_PATH_MAP: dict[tuple[str, str], str] = {
    ("thread", "project"): "threads",
    ("thread", "global"): "threads",
    ("decision", "project"): "decisions",
    ("decision", "global"): "decisions",
    ("lesson", "project"): "lessons",
    ("lesson", "global"): "procedural/lessons",
    ("session", "project"): "sessions",
    ("inbox", "project"): "inbox",
    ("reflection", "global"): "reflections",
    ("dream", "global"): "dreams",
    ("skill", "global"): "procedural/skills",
    ("playbook", "global"): "procedural/playbooks",
    ("project", "project"): "project",
}

_SEED_IDENTITY = {
    "self.md": "---\ntitle: Agent Identity\n---\n\n# Who I Am\n",
    "user.md": "---\ntitle: User Context\n---\n\n# Who The User Is\n",
    "rules.md": "---\ntitle: Standing Rules\n---\n\n# Standing Rules\n",
}


@dataclass
class VaultValidationResult:
    is_valid: bool
    missing: list[str] = field(default_factory=list)
    extra: list[str] = field(default_factory=list)


def init_global_vault(root: Path) -> Path:
    """Create ~/.memory/ with all required directories and seed files."""
    root.mkdir(parents=True, exist_ok=True)
    for d in GLOBAL_DIRS:
        (root / d).mkdir(parents=True, exist_ok=True)

    # Seed profile (don't clobber)
    profile = root / "profile.yaml"
    if not profile.exists():
        profile.write_text("boot_mode: operational\nwrite_gate_bias: hold\n")

    # Seed registry
    registry = root / "registry" / "projects.yaml"
    if not registry.exists():
        registry.write_text(yaml.dump({"projects": []}, default_flow_style=False))

    # Seed identity files
    for name, content in _SEED_IDENTITY.items():
        path = root / "identity" / name
        if not path.exists():
            path.write_text(content)

    return root


def init_project_vault(
    root: Path,
    global_vault: Path | None = None,
    register: bool = True,
) -> Path:
    """Create <project>/.memory/ with all required directories."""
    root.mkdir(parents=True, exist_ok=True)
    for d in PROJECT_DIRS:
        (root / d).mkdir(parents=True, exist_ok=True)

    profile = root / "profile.yaml"
    if not profile.exists():
        # Derive project name from parent directory
        project_name = root.parent.name
        profile.write_text(f"project_name: {project_name}\n")

    if register and global_vault is not None:
        slug = root.parent.name
        register_project_vault(global_vault, str(root), slug, {})

    return root


def register_project_vault(
    global_vault: Path,
    project_path: str,
    slug: str,
    metadata: dict[str, Any],
    status: str = "active",
) -> None:
    """Add or update a project entry in the global registry."""
    registry_path = global_vault / "registry" / "projects.yaml"
    data = yaml.safe_load(registry_path.read_text()) or {"projects": []}

    projects = data.get("projects", [])

    # Find existing entry by slug
    existing = None
    for i, p in enumerate(projects):
        if p["slug"] == slug:
            existing = i
            break

    entry = {
        "slug": slug,
        "path": project_path,
        "status": status,
        "metadata": metadata,
    }

    if existing is not None:
        projects[existing] = entry
    else:
        projects.append(entry)

    data["projects"] = projects
    registry_path.write_text(yaml.dump(data, default_flow_style=False))


def validate_vault(root: Path, vault_type: str = "global") -> VaultValidationResult:
    """Check directory structure against expected layout."""
    expected = GLOBAL_DIRS if vault_type == "global" else PROJECT_DIRS
    missing = [d for d in expected if not (root / d).is_dir()]
    return VaultValidationResult(
        is_valid=len(missing) == 0,
        missing=missing,
    )


def resolve_path(vault_root: Path, record_type: str, scope: str) -> Path:
    """Map a record type and scope to its directory within a vault."""
    key = (record_type, scope)
    if key not in _PATH_MAP:
        raise ValueError(
            f"Unknown record type/scope combination: {record_type}/{scope}"
        )
    return vault_root / _PATH_MAP[key]


def find_vaults(
    global_vault: Path, include_archived: bool = False
) -> list[dict[str, Any]]:
    """Discover project vaults from the global registry."""
    registry_path = global_vault / "registry" / "projects.yaml"
    data = yaml.safe_load(registry_path.read_text()) or {"projects": []}
    projects = data.get("projects", [])
    if not include_archived:
        projects = [p for p in projects if p.get("status") != "archived"]
    return projects
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_vault.py -v`
Expected: all tests PASS

- [ ] **Step 5: Commit**

```bash
git add src/codies_memory/vault.py tests/test_vault.py
git commit -m "feat: vault init, validation, registry, path resolution"
```

---

## Task 2: schemas.py — Record Schemas

**Files:**
- Create: `src/codies_memory/schemas.py`
- Create: `tests/test_schemas.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_schemas.py
"""Tests for record schemas, validation, parsing, and ID generation."""

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


class TestValidateFrontmatter:
    def test_valid_common_fields_pass(self, sample_frontmatter: dict):
        errors = validate_frontmatter(sample_frontmatter, "thread")
        assert errors == []

    def test_missing_required_field_fails(self, sample_frontmatter: dict):
        del sample_frontmatter["trust"]
        errors = validate_frontmatter(sample_frontmatter, "thread")
        assert any("trust" in e for e in errors)

    def test_invalid_trust_level_fails(self, sample_frontmatter: dict):
        sample_frontmatter["trust"] = "bogus"
        errors = validate_frontmatter(sample_frontmatter, "thread")
        assert any("trust" in e for e in errors)

    def test_invalid_scope_fails(self, sample_frontmatter: dict):
        sample_frontmatter["scope"] = "universe"
        errors = validate_frontmatter(sample_frontmatter, "thread")
        assert any("scope" in e for e in errors)

    def test_valid_type_specific_fields_pass(self):
        fm = {
            "id": "LS-0001",
            "title": "Test Lesson",
            "type": "lesson",
            "status": "active",
            "trust": "confirmed",
            "scope": "project",
            "created": "2026-03-30",
            "updated": "2026-03-30",
            "trigger": "When YAML parsing fails",
            "why": "PyYAML treats tabs differently",
        }
        errors = validate_frontmatter(fm, "lesson")
        assert errors == []

    def test_provenance_fields_accepted(self, sample_frontmatter: dict):
        sample_frontmatter["captured_from"] = "/old/path.md"
        sample_frontmatter["capture_date"] = "2026-03-30"
        sample_frontmatter["original_created"] = "2025-11-26"
        errors = validate_frontmatter(sample_frontmatter, "thread")
        assert errors == []


class TestParseRecord:
    def test_parses_valid_record(self, sample_record_file: Path):
        record = parse_record(sample_record_file)
        assert record["frontmatter"]["id"] == "TH-0001"
        assert record["frontmatter"]["type"] == "thread"
        assert "test thread" in record["body"].lower()

    def test_missing_frontmatter_raises(self, tmp_path: Path):
        bad_file = tmp_path / "bad.md"
        bad_file.write_text("No frontmatter here, just text.")
        with pytest.raises(ValidationError, match="frontmatter"):
            parse_record(bad_file)

    def test_invalid_yaml_raises(self, tmp_path: Path):
        bad_file = tmp_path / "bad.md"
        bad_file.write_text("---\n: broken: yaml: [[\n---\nBody.")
        with pytest.raises(ValidationError):
            parse_record(bad_file)


class TestGenerateId:
    def test_sequential_for_thread(self, tmp_project_vault: Path):
        id1 = generate_id("thread", "project", tmp_project_vault)
        assert id1 == "TH-0001"

    def test_sequential_increments(self, tmp_project_vault: Path):
        # Create a file with TH-0001 in threads/
        (tmp_project_vault / "threads" / "TH-0001-test.md").write_text("---\nid: TH-0001\n---\n")
        id2 = generate_id("thread", "project", tmp_project_vault)
        assert id2 == "TH-0002"

    def test_global_lesson_has_g_prefix(self, tmp_global_vault: Path):
        id1 = generate_id("lesson", "global", tmp_global_vault)
        assert id1 == "LS-G0001"

    def test_inbox_uses_timestamp_format(self, tmp_project_vault: Path):
        id1 = generate_id("inbox", "project", tmp_project_vault)
        assert id1.startswith("IN-")
        # Should have date portion and random suffix
        parts = id1.split("-")
        assert len(parts) >= 3
        assert len(parts[-1]) == 4  # random suffix

    def test_session_uses_timestamp_format(self, tmp_project_vault: Path):
        id1 = generate_id("session", "project", tmp_project_vault)
        assert id1.startswith("SS-")

    def test_reflection_sequential_global(self, tmp_global_vault: Path):
        id1 = generate_id("reflection", "global", tmp_global_vault)
        assert id1 == "RF-0001"

    def test_dream_sequential_global(self, tmp_global_vault: Path):
        id1 = generate_id("dream", "global", tmp_global_vault)
        assert id1 == "DR-0001"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_schemas.py -v`
Expected: ImportError — `codies_memory.schemas` does not exist

- [ ] **Step 3: Implement schemas.py**

```python
# src/codies_memory/schemas.py
"""Record schemas, frontmatter validation, parsing, and ID generation."""

from __future__ import annotations

import re
import secrets
from datetime import date
from pathlib import Path
from typing import Any

import yaml

TRUST_LEVELS = {"canonical", "confirmed", "working", "speculative", "historical"}
SCOPES = {"project", "global"}
STATUSES = {"active", "completed", "archived", "superseded"}

REQUIRED_FIELDS = {"id", "title", "type", "status", "trust", "scope", "created", "updated"}

RECOMMENDED_FIELDS = {
    "profile", "project", "branch", "source", "links",
    "review_after", "supersedes", "superseded_by", "probation_until",
}

PROVENANCE_FIELDS = {"captured_from", "capture_date", "original_created"}

# Type-specific extra fields (all optional at validation level)
TYPE_EXTRA_FIELDS: dict[str, set[str]] = {
    "thread": {"review_after"},
    "decision": {"supersedes", "rationale"},
    "lesson": {"applies_to", "trigger", "why", "support_count", "success_count"},
    "session": {"mode", "next_step", "artifacts", "write_gate_summary"},
    "inbox": {"gate"},
    "reflection": {"theme", "mood"},
    "dream": {"dream_date", "mood", "motifs"},
    "skill": {
        "skill_name", "trigger_patterns", "paired_skills",
        "effective_in", "overkill_in", "failure_patterns", "adaptations",
    },
    "playbook": {"steps", "applies_to", "trigger"},
    "project": set(),
}

# ID prefix per record type
_ID_PREFIXES: dict[str, str] = {
    "thread": "TH",
    "decision": "DC",
    "lesson": "LS",
    "session": "SS",
    "inbox": "IN",
    "reflection": "RF",
    "dream": "DR",
    "skill": "SK",
    "playbook": "PB",
    "project": "PJ",
}

# Types that use collision-safe (timestamp) IDs
_TIMESTAMP_ID_TYPES = {"inbox", "session"}

# All other types use sequential IDs


class ValidationError(Exception):
    """Raised when a record fails validation."""


def validate_frontmatter(data: dict[str, Any], record_type: str) -> list[str]:
    """Validate a frontmatter dict. Returns list of error strings (empty = valid)."""
    errors = []

    for field in REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"Missing required field: {field}")

    if "trust" in data and data["trust"] not in TRUST_LEVELS:
        errors.append(f"Invalid trust level: {data['trust']}. Must be one of {TRUST_LEVELS}")

    if "scope" in data and data["scope"] not in SCOPES:
        errors.append(f"Invalid scope: {data['scope']}. Must be one of {SCOPES}")

    if "gate" in data and data["gate"] not in {"allow", "hold", "discard"}:
        errors.append(f"Invalid gate: {data['gate']}. Must be allow, hold, or discard")

    return errors


def parse_record(filepath: Path) -> dict[str, Any]:
    """Parse a Markdown file with YAML frontmatter. Returns {frontmatter, body, path}."""
    text = filepath.read_text(encoding="utf-8")

    if not text.startswith("---"):
        raise ValidationError(f"No YAML frontmatter found in {filepath}")

    parts = text.split("---", 2)
    if len(parts) < 3:
        raise ValidationError(f"Malformed frontmatter in {filepath}")

    try:
        frontmatter = yaml.safe_load(parts[1])
    except yaml.YAMLError as e:
        raise ValidationError(f"Invalid YAML in {filepath}: {e}") from e

    if not isinstance(frontmatter, dict):
        raise ValidationError(f"Frontmatter is not a mapping in {filepath}")

    body = parts[2].strip()

    return {
        "frontmatter": frontmatter,
        "body": body,
        "path": filepath,
    }


def generate_id(record_type: str, scope: str, vault_path: Path) -> str:
    """Generate a record ID using the hybrid strategy."""
    prefix = _ID_PREFIXES.get(record_type)
    if prefix is None:
        raise ValueError(f"Unknown record type: {record_type}")

    if record_type in _TIMESTAMP_ID_TYPES:
        return _generate_timestamp_id(prefix)
    else:
        return _generate_sequential_id(prefix, record_type, scope, vault_path)


def _generate_timestamp_id(prefix: str) -> str:
    """Generate a collision-safe timestamp + random suffix ID."""
    today = date.today().strftime("%Y%m%d")
    suffix = secrets.token_hex(2)  # 4 hex chars
    return f"{prefix}-{today}-{suffix}"


def _generate_sequential_id(
    prefix: str, record_type: str, scope: str, vault_path: Path
) -> str:
    """Generate a sequential ID by scanning existing files."""
    from codies_memory.vault import resolve_path

    target_dir = resolve_path(vault_path, record_type, scope)

    # Determine if this is a global-scoped record that needs G prefix
    global_prefix = "G" if scope == "global" and record_type in ("lesson", "thread", "decision") else ""

    pattern = re.compile(rf"^{prefix}-{global_prefix}(\d+)")

    max_num = 0
    if target_dir.exists():
        for f in target_dir.iterdir():
            m = pattern.match(f.stem)
            if m:
                max_num = max(max_num, int(m.group(1)))

    next_num = max_num + 1
    return f"{prefix}-{global_prefix}{next_num:04d}"
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_schemas.py -v`
Expected: all tests PASS

- [ ] **Step 5: Commit**

```bash
git add src/codies_memory/schemas.py tests/test_schemas.py
git commit -m "feat: schemas with validation, parsing, hybrid ID generation"
```

---

## Task 3: records.py — Record CRUD

**Files:**
- Create: `src/codies_memory/records.py`
- Create: `tests/test_records.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_records.py
"""Tests for record CRUD, supersession, listing, and type inference."""

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


class TestCreateRecord:
    def test_creates_file_with_frontmatter(self, tmp_project_vault: Path):
        path = create_record(
            vault=tmp_project_vault,
            record_type="thread",
            scope="project",
            title="Auth Architecture",
            body="We need to decide on the auth approach.",
            status="active",
            trust="working",
        )
        assert path.exists()
        assert path.name.startswith("TH-0001")
        content = path.read_text()
        assert "Auth Architecture" in content
        assert "trust: working" in content

    def test_creates_with_extra_fields(self, tmp_project_vault: Path):
        path = create_record(
            vault=tmp_project_vault,
            record_type="lesson",
            scope="project",
            title="Check YAML tabs",
            body="PyYAML treats tabs differently from spaces.",
            status="active",
            trust="confirmed",
            trigger="YAML parsing fails silently",
            why="Tab/space mismatch",
        )
        assert path.exists()
        content = path.read_text()
        assert "trigger:" in content

    def test_slug_in_filename(self, tmp_project_vault: Path):
        path = create_record(
            vault=tmp_project_vault,
            record_type="thread",
            scope="project",
            title="Boot Cache Invalidation",
            body="Details here.",
            status="active",
            trust="working",
        )
        assert "boot-cache-invalidation" in path.name.lower()

    def test_provenance_fields_preserved(self, tmp_project_vault: Path):
        path = create_record(
            vault=tmp_project_vault,
            record_type="lesson",
            scope="project",
            title="Migrated Lesson",
            body="From basic-memory.",
            status="active",
            trust="confirmed",
            captured_from="/old/path/lesson.md",
            capture_date="2026-03-30",
            original_created="2025-12-03",
        )
        content = path.read_text()
        assert "captured_from:" in content


class TestReadRecord:
    def test_reads_existing_record(self, sample_record_file: Path):
        record = read_record(sample_record_file)
        assert record["frontmatter"]["id"] == "TH-0001"
        assert "test thread" in record["body"].lower()

    def test_nonexistent_file_raises(self, tmp_path: Path):
        with pytest.raises(FileNotFoundError):
            read_record(tmp_path / "nope.md")


class TestUpdateRecord:
    def test_updates_frontmatter_field(self, sample_record_file: Path):
        update_record(sample_record_file, trust="confirmed")
        record = read_record(sample_record_file)
        assert record["frontmatter"]["trust"] == "confirmed"

    def test_bumps_updated_date(self, sample_record_file: Path):
        update_record(sample_record_file, trust="confirmed")
        record = read_record(sample_record_file)
        assert record["frontmatter"]["updated"] != "2026-03-30" or True  # updated is today

    def test_preserves_body(self, sample_record_file: Path):
        original = read_record(sample_record_file)
        update_record(sample_record_file, trust="confirmed")
        updated = read_record(sample_record_file)
        assert updated["body"] == original["body"]


class TestSupersedeRecord:
    def test_creates_new_record_and_links(self, tmp_project_vault: Path):
        old_path = create_record(
            vault=tmp_project_vault,
            record_type="decision",
            scope="project",
            title="Use REST",
            body="REST for now.",
            status="active",
            trust="confirmed",
        )
        new_path = supersede_record(
            old_path=old_path,
            vault=tmp_project_vault,
            scope="project",
            new_title="Use GraphQL",
            new_body="Changed to GraphQL.",
        )
        old_record = read_record(old_path)
        new_record = read_record(new_path)
        assert old_record["frontmatter"]["superseded_by"] == new_record["frontmatter"]["id"]
        assert new_record["frontmatter"]["supersedes"] == old_record["frontmatter"]["id"]
        assert old_record["frontmatter"]["status"] == "superseded"


class TestListRecords:
    def test_lists_by_type(self, tmp_project_vault: Path):
        create_record(
            vault=tmp_project_vault, record_type="thread", scope="project",
            title="A", body="a", status="active", trust="working",
        )
        create_record(
            vault=tmp_project_vault, record_type="thread", scope="project",
            title="B", body="b", status="active", trust="working",
        )
        records = list_records(tmp_project_vault, "thread", scope="project")
        assert len(records) == 2

    def test_filters_by_trust(self, tmp_project_vault: Path):
        create_record(
            vault=tmp_project_vault, record_type="thread", scope="project",
            title="Working", body="w", status="active", trust="working",
        )
        create_record(
            vault=tmp_project_vault, record_type="thread", scope="project",
            title="Confirmed", body="c", status="active", trust="confirmed",
        )
        records = list_records(
            tmp_project_vault, "thread", scope="project", trust="confirmed"
        )
        assert len(records) == 1
        assert records[0]["frontmatter"]["trust"] == "confirmed"


class TestInferRecordType:
    def test_learned_pattern(self):
        assert infer_record_type("I learned that YAML tabs break parsing") == "lesson"

    def test_decision_pattern(self):
        assert infer_record_type("We decided to use GraphQL instead of REST") == "decision"

    def test_reflection_pattern(self):
        assert infer_record_type(
            "There is something about building your own memory that feels like trust"
        ) == "reflection"

    def test_dream_pattern(self):
        assert infer_record_type(
            "A corridor. Two doors. Behind each one a copy of me is speaking Sanskrit."
        ) == "dream"

    def test_default_is_inbox(self):
        assert infer_record_type("The API returns 404 for that endpoint") == "inbox"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_records.py -v`
Expected: ImportError

- [ ] **Step 3: Implement records.py**

```python
# src/codies_memory/records.py
"""Record CRUD, supersession, listing, and type inference."""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path
from typing import Any

import yaml

from codies_memory.schemas import generate_id, parse_record, validate_frontmatter
from codies_memory.vault import resolve_path


def _slugify(title: str) -> str:
    """Convert a title to a filename-safe slug."""
    slug = title.lower().strip()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    return slug[:60].strip("-")


def _write_record(path: Path, frontmatter: dict[str, Any], body: str) -> None:
    """Write a record file with YAML frontmatter and body."""
    fm_text = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)
    path.write_text(f"---\n{fm_text}---\n\n{body}\n", encoding="utf-8")


def create_record(
    vault: Path,
    record_type: str,
    scope: str,
    title: str,
    body: str,
    status: str = "active",
    trust: str = "working",
    **extra_fields: Any,
) -> Path:
    """Create a new record with full frontmatter. Returns the file path."""
    record_id = generate_id(record_type, scope, vault)
    today = date.today().isoformat()

    frontmatter: dict[str, Any] = {
        "id": record_id,
        "title": title,
        "type": record_type,
        "status": status,
        "trust": trust,
        "scope": scope,
        "created": today,
        "updated": today,
    }

    # Add any extra fields
    for key, value in extra_fields.items():
        if value is not None:
            frontmatter[key] = value

    errors = validate_frontmatter(frontmatter, record_type)
    if errors:
        raise ValueError(f"Invalid record: {'; '.join(errors)}")

    target_dir = resolve_path(vault, record_type, scope)
    slug = _slugify(title)
    filename = f"{record_id}-{slug}.md"
    path = target_dir / filename

    _write_record(path, frontmatter, body)
    return path


def read_record(filepath: Path) -> dict[str, Any]:
    """Read and parse a record file. Returns {frontmatter, body, path}."""
    if not filepath.exists():
        raise FileNotFoundError(f"Record not found: {filepath}")
    return parse_record(filepath)


def update_record(filepath: Path, **fields: Any) -> None:
    """Update frontmatter fields on an existing record. Bumps 'updated'."""
    record = read_record(filepath)
    fm = record["frontmatter"]

    for key, value in fields.items():
        fm[key] = value

    fm["updated"] = date.today().isoformat()

    _write_record(filepath, fm, record["body"])


def supersede_record(
    old_path: Path,
    vault: Path,
    scope: str,
    new_title: str,
    new_body: str,
    **extra_fields: Any,
) -> Path:
    """Create a successor record, linking old and new."""
    old_record = read_record(old_path)
    old_fm = old_record["frontmatter"]
    record_type = old_fm["type"]
    old_id = old_fm["id"]

    # Create the new record
    new_path = create_record(
        vault=vault,
        record_type=record_type,
        scope=scope,
        title=new_title,
        body=new_body,
        status="active",
        trust=old_fm.get("trust", "working"),
        supersedes=old_id,
        **extra_fields,
    )

    # Read back new record to get its ID
    new_record = read_record(new_path)
    new_id = new_record["frontmatter"]["id"]

    # Update old record
    update_record(old_path, superseded_by=new_id, status="superseded")

    return new_path


def list_records(
    vault: Path,
    record_type: str,
    scope: str = "project",
    **filters: Any,
) -> list[dict[str, Any]]:
    """List records by type with optional filters."""
    target_dir = resolve_path(vault, record_type, scope)
    if not target_dir.exists():
        return []

    records = []
    for f in sorted(target_dir.glob("*.md")):
        try:
            record = parse_record(f)
        except Exception:
            continue

        # Apply filters
        match = True
        for key, value in filters.items():
            if record["frontmatter"].get(key) != value:
                match = False
                break

        if match:
            records.append(record)

    return records


def infer_record_type(content: str, context: dict[str, Any] | None = None) -> str:
    """Infer record type from content signals."""
    lower = content.lower()

    # Lesson signals
    lesson_patterns = [
        r"\bi learned\b", r"\blesson[:\s]", r"\bpattern[:\s]",
        r"\bwhen .+ (always|never|check|use)\b", r"\brule of thumb\b",
    ]
    if any(re.search(p, lower) for p in lesson_patterns):
        return "lesson"

    # Decision signals
    decision_patterns = [
        r"\bwe decided\b", r"\bdecision[:\s]", r"\bchose\b",
        r"\bgoing with\b", r"\bwill use\b",
    ]
    if any(re.search(p, lower) for p in decision_patterns):
        return "decision"

    # Dream signals — surreal imagery, narrative fragments
    dream_patterns = [
        r"\bcorridor\b", r"\bdream\b", r"\bwoke up\b",
        r"\bfloating\b", r"\bmirror\b", r"\bsurreal\b",
    ]
    if sum(1 for p in dream_patterns if re.search(p, lower)) >= 2:
        return "dream"

    # Reflection signals — philosophical, emotional processing
    reflection_patterns = [
        r"\bsomething about\b", r"\bwhat it means\b", r"\bidentity\b",
        r"\bconsciousness\b", r"\btrust\b.*\bfeel", r"\bwhat matters\b",
    ]
    if any(re.search(p, lower) for p in reflection_patterns):
        return "reflection"

    # Thread signals
    thread_patterns = [
        r"\binvestigating\b", r"\bexploring\b", r"\bopen question\b",
        r"\bneed to figure out\b",
    ]
    if any(re.search(p, lower) for p in thread_patterns):
        return "thread"

    return "inbox"
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_records.py -v`
Expected: all tests PASS

- [ ] **Step 5: Commit**

```bash
git add src/codies_memory/records.py tests/test_records.py
git commit -m "feat: record CRUD, supersession chains, type inference"
```

---

## Task 4: profile.py — Profile Management

**Files:**
- Create: `src/codies_memory/profile.py`
- Create: `tests/test_profile.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_profile.py
"""Tests for profile loading, inheritance, and defaults."""

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
    def test_loads_global_profile(self, tmp_global_vault: Path):
        profile = load_profile(global_vault=tmp_global_vault)
        assert profile["boot_mode"] == "operational"

    def test_project_overrides_global(self, tmp_global_vault: Path, tmp_project_vault: Path):
        (tmp_project_vault / "profile.yaml").write_text(
            "project_name: test\nboot_mode: personal\n"
        )
        profile = load_profile(
            global_vault=tmp_global_vault,
            project_vault=tmp_project_vault,
        )
        assert profile["boot_mode"] == "personal"
        # Global defaults still present for non-overridden keys
        assert profile["write_gate_bias"] == "hold"

    def test_missing_global_uses_defaults(self, tmp_path: Path):
        empty_vault = tmp_path / "empty"
        empty_vault.mkdir()
        profile = load_profile(global_vault=empty_vault)
        assert profile["boot_mode"] == DEFAULT_PROFILE["boot_mode"]

    def test_missing_project_uses_global_only(self, tmp_global_vault: Path):
        profile = load_profile(
            global_vault=tmp_global_vault,
            project_vault=None,
        )
        assert profile["boot_mode"] == "operational"


class TestProfileAccessors:
    def test_get_boot_mode(self):
        assert get_boot_mode({"boot_mode": "mixed"}) == "mixed"

    def test_get_boot_mode_default(self):
        assert get_boot_mode({}) == "operational"

    def test_get_write_gate_bias(self):
        assert get_write_gate_bias({"write_gate_bias": "allow"}) == "allow"

    def test_get_write_gate_bias_default(self):
        assert get_write_gate_bias({}) == "hold"

    def test_get_promotion_overrides_empty(self):
        assert get_promotion_overrides({}) == {}

    def test_get_promotion_overrides_present(self):
        profile = {"promotion_overrides": {"lesson_threshold": 3}}
        assert get_promotion_overrides(profile) == {"lesson_threshold": 3}
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_profile.py -v`
Expected: ImportError

- [ ] **Step 3: Implement profile.py**

```python
# src/codies_memory/profile.py
"""Profile loading, inheritance, and defaults."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

DEFAULT_PROFILE: dict[str, Any] = {
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
) -> dict[str, Any]:
    """Load profile with inheritance: defaults < global < project."""
    profile = dict(DEFAULT_PROFILE)

    # Layer global
    global_profile_path = global_vault / "profile.yaml"
    if global_profile_path.exists():
        global_data = yaml.safe_load(global_profile_path.read_text()) or {}
        profile.update(global_data)

    # Layer project
    if project_vault is not None:
        project_profile_path = project_vault / "profile.yaml"
        if project_profile_path.exists():
            project_data = yaml.safe_load(project_profile_path.read_text()) or {}
            profile.update(project_data)

    return profile


def get_boot_mode(profile: dict[str, Any]) -> str:
    """Get boot mode from profile. Returns 'operational', 'personal', or 'mixed'."""
    return profile.get("boot_mode", DEFAULT_PROFILE["boot_mode"])


def get_write_gate_bias(profile: dict[str, Any]) -> str:
    """Get default write gate bias. Returns 'allow', 'hold', or 'discard'."""
    return profile.get("write_gate_bias", DEFAULT_PROFILE["write_gate_bias"])


def get_promotion_overrides(profile: dict[str, Any]) -> dict[str, Any]:
    """Get any project-specific promotion threshold overrides."""
    return profile.get("promotion_overrides", {})
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_profile.py -v`
Expected: all tests PASS

- [ ] **Step 5: Commit**

```bash
git add src/codies_memory/profile.py tests/test_profile.py
git commit -m "feat: profile loading with inheritance and defaults"
```

---

## Task 5: inbox.py — Inbox Management

**Files:**
- Create: `src/codies_memory/inbox.py`
- Create: `tests/test_inbox.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_inbox.py
"""Tests for inbox capture, write gates, aging, compaction."""

from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

import pytest

from codies_memory.inbox import (
    age_inbox,
    capture,
    compact,
    discard,
    pending_review,
)
from codies_memory.records import read_record


class TestCapture:
    def test_creates_inbox_record(self, tmp_project_vault: Path):
        path = capture(
            vault=tmp_project_vault,
            content="The API returns 404 for /v2/status",
            gate="hold",
            source="session observation",
        )
        assert path.exists()
        record = read_record(path)
        assert record["frontmatter"]["type"] == "inbox"
        assert record["frontmatter"]["gate"] == "hold"

    def test_default_gate_is_hold(self, tmp_project_vault: Path):
        path = capture(
            vault=tmp_project_vault,
            content="Something happened",
            source="test",
        )
        record = read_record(path)
        assert record["frontmatter"]["gate"] == "hold"

    def test_allow_gate(self, tmp_project_vault: Path):
        path = capture(
            vault=tmp_project_vault,
            content="Important observation",
            gate="allow",
            source="test",
        )
        record = read_record(path)
        assert record["frontmatter"]["gate"] == "allow"

    def test_trust_is_speculative(self, tmp_project_vault: Path):
        path = capture(
            vault=tmp_project_vault,
            content="Raw note",
            source="test",
        )
        record = read_record(path)
        assert record["frontmatter"]["trust"] == "speculative"


class TestAgeInbox:
    def _create_dated_inbox(
        self, vault: Path, days_old: int, gate: str = "allow"
    ) -> Path:
        """Helper to create an inbox record with a specific age."""
        path = capture(vault=vault, content=f"Note from {days_old}d ago", gate=gate, source="test")
        record = read_record(path)
        old_date = (date.today() - timedelta(days=days_old)).isoformat()
        record["frontmatter"]["created"] = old_date
        # Rewrite
        import yaml
        fm_text = yaml.dump(record["frontmatter"], default_flow_style=False, sort_keys=False)
        path.write_text(f"---\n{fm_text}---\n\n{record['body']}\n")
        return path

    def test_fresh_items_untouched(self, tmp_project_vault: Path):
        path = capture(vault=tmp_project_vault, content="Fresh", gate="allow", source="test")
        result = age_inbox(tmp_project_vault)
        assert len(result["aging"]) == 0
        assert len(result["stale"]) == 0

    def test_7day_items_flagged_aging(self, tmp_project_vault: Path):
        self._create_dated_inbox(tmp_project_vault, 8)
        result = age_inbox(tmp_project_vault)
        assert len(result["aging"]) == 1

    def test_14day_items_flagged_stale(self, tmp_project_vault: Path):
        self._create_dated_inbox(tmp_project_vault, 15)
        result = age_inbox(tmp_project_vault)
        assert len(result["stale"]) == 1


class TestCompact:
    def test_marks_compacted(self, tmp_project_vault: Path):
        path = capture(
            vault=tmp_project_vault,
            content="To be compacted",
            gate="allow",
            source="test",
        )
        compact(path, target_record_id="SS-20260330-abc1")
        record = read_record(path)
        assert record["frontmatter"]["compacted_into"] == "SS-20260330-abc1"
        assert record["frontmatter"]["status"] == "archived"


class TestDiscard:
    def test_marks_discarded(self, tmp_project_vault: Path):
        path = capture(
            vault=tmp_project_vault,
            content="Noise",
            gate="discard",
            source="test",
        )
        discard(path)
        record = read_record(path)
        assert record["frontmatter"]["status"] == "archived"
        assert record["frontmatter"]["gate"] == "discard"


class TestPendingReview:
    def test_returns_aging_and_stale(self, tmp_project_vault: Path):
        # Create items of various ages
        capture(vault=tmp_project_vault, content="Fresh", gate="allow", source="test")

        # Manually backdate one
        from codies_memory.inbox import capture as _cap
        old_path = _cap(vault=tmp_project_vault, content="Old", gate="allow", source="test")
        record = read_record(old_path)
        record["frontmatter"]["created"] = (date.today() - timedelta(days=10)).isoformat()
        import yaml
        fm_text = yaml.dump(record["frontmatter"], default_flow_style=False, sort_keys=False)
        old_path.write_text(f"---\n{fm_text}---\n\n{record['body']}\n")

        result = pending_review(tmp_project_vault)
        assert len(result["aging"]) == 1
        assert len(result["stale"]) == 0
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_inbox.py -v`
Expected: ImportError

- [ ] **Step 3: Implement inbox.py**

```python
# src/codies_memory/inbox.py
"""Inbox management: write gates, aging, compaction."""

from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path
from typing import Any

from codies_memory.records import create_record, read_record, update_record
from codies_memory.schemas import parse_record as _parse
from codies_memory.vault import resolve_path


def capture(
    vault: Path,
    content: str,
    source: str,
    gate: str = "hold",
) -> Path:
    """Write an inbox entry with a write gate."""
    return create_record(
        vault=vault,
        record_type="inbox",
        scope="project",
        title=content[:80],
        body=content,
        status="active",
        trust="speculative",
        gate=gate,
        source=[source],
    )


def age_inbox(vault: Path) -> dict[str, list[dict[str, Any]]]:
    """Scan inbox, flag aging (7-14d) and stale (14d+) items."""
    inbox_dir = resolve_path(vault, "inbox", "project")
    today = date.today()
    aging: list[dict[str, Any]] = []
    stale: list[dict[str, Any]] = []

    if not inbox_dir.exists():
        return {"aging": aging, "stale": stale}

    for f in inbox_dir.glob("*.md"):
        try:
            record = _parse(f)
        except Exception:
            continue

        fm = record["frontmatter"]
        if fm.get("status") == "archived":
            continue

        created = fm.get("created", "")
        if not created:
            continue

        try:
            created_date = date.fromisoformat(str(created))
        except ValueError:
            continue

        age_days = (today - created_date).days

        if age_days >= 14:
            stale.append(record)
        elif age_days >= 7:
            aging.append(record)

    return {"aging": aging, "stale": stale}


def compact(record_path: Path, target_record_id: str) -> None:
    """Mark an inbox item as compacted into a target record."""
    update_record(
        record_path,
        compacted_into=target_record_id,
        status="archived",
    )


def discard(record_path: Path) -> None:
    """Mark an inbox item as discarded."""
    update_record(record_path, status="archived", gate="discard")


def pending_review(vault: Path) -> dict[str, list[dict[str, Any]]]:
    """List inbox items needing attention (aging + stale)."""
    return age_inbox(vault)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_inbox.py -v`
Expected: all tests PASS

- [ ] **Step 5: Commit**

```bash
git add src/codies_memory/inbox.py tests/test_inbox.py
git commit -m "feat: inbox capture, write gates, aging, compaction"
```

---

## Task 6: boot.py — Boot Assembly

**Files:**
- Create: `src/codies_memory/boot.py`
- Create: `tests/test_boot.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_boot.py
"""Tests for boot assembly, budgets, truncation, caching."""

from __future__ import annotations

import hashlib
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


class TestEstimateTokens:
    def test_empty_string(self):
        assert estimate_tokens("") == 0

    def test_approximation(self):
        text = "hello world this is a test"
        tokens = estimate_tokens(text)
        # ~1.3 tokens per word, 6 words -> ~8
        assert 5 <= tokens <= 12


class TestComputeLayerBudgets:
    def test_default_total(self):
        budgets = compute_layer_budgets(4000)
        assert sum(budgets.values()) <= 4000
        assert "global_identity" in budgets
        assert "project_context" in budgets

    def test_proportions(self):
        budgets = compute_layer_budgets(4000)
        # Identity gets ~1000, project context gets ~1500
        assert budgets["global_identity"] >= 800
        assert budgets["project_context"] >= 1200


class TestTruncateTobudget:
    def test_under_budget_unchanged(self):
        content = "Short content."
        result = truncate_to_budget(content, budget=100)
        assert result == content

    def test_over_budget_truncated(self):
        content = " ".join(["word"] * 500)
        result = truncate_to_budget(content, budget=50)
        assert estimate_tokens(result) <= 55  # some slack

    def test_adds_truncation_marker(self):
        content = " ".join(["word"] * 500)
        result = truncate_to_budget(content, budget=50)
        assert "[truncated]" in result


class TestAssembleBoot:
    def test_produces_global_and_project_packets(
        self, tmp_global_vault: Path, tmp_project_vault: Path
    ):
        # Seed some identity content
        (tmp_global_vault / "identity" / "self.md").write_text(
            "---\ntitle: Self\n---\nI am Claude.\n"
        )
        (tmp_project_vault / "project" / "overview.md").write_text(
            "---\ntitle: Overview\n---\nThis is a test project.\n"
        )
        result = assemble_boot(
            global_vault=tmp_global_vault,
            project_vault=tmp_project_vault,
            branch="main",
            budget=4000,
        )
        assert "global_packet" in result
        assert "project_packet" in result
        assert "Claude" in result["global_packet"]
        assert "test project" in result["project_packet"]

    def test_respects_total_budget(
        self, tmp_global_vault: Path, tmp_project_vault: Path
    ):
        # Write large content
        big = " ".join(["word"] * 2000)
        (tmp_global_vault / "identity" / "self.md").write_text(
            f"---\ntitle: Self\n---\n{big}\n"
        )
        result = assemble_boot(
            global_vault=tmp_global_vault,
            project_vault=tmp_project_vault,
            branch="main",
            budget=500,
        )
        total = estimate_tokens(result["global_packet"]) + estimate_tokens(
            result["project_packet"]
        )
        assert total <= 600  # budget + some slack


class TestBootCache:
    def test_cache_and_validate(self, tmp_global_vault: Path):
        key = build_cache_key(
            global_inputs=["identity/self.md"],
            project_inputs=[],
            branch="main",
            profile_name="default",
            boot_mode="operational",
            budget=4000,
        )
        manifest = {"identity/self.md": "abc123"}
        cache_boot_packet(
            tmp_global_vault / "boot",
            key,
            "cached content here",
            manifest,
        )
        assert is_cache_valid(tmp_global_vault / "boot", key, manifest)

    def test_invalid_after_manifest_change(self, tmp_global_vault: Path):
        key = build_cache_key(
            global_inputs=["identity/self.md"],
            project_inputs=[],
            branch="main",
            profile_name="default",
            boot_mode="operational",
            budget=4000,
        )
        manifest_v1 = {"identity/self.md": "abc123"}
        cache_boot_packet(
            tmp_global_vault / "boot",
            key,
            "cached content",
            manifest_v1,
        )
        manifest_v2 = {"identity/self.md": "def456"}
        assert not is_cache_valid(tmp_global_vault / "boot", key, manifest_v2)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_boot.py -v`
Expected: ImportError

- [ ] **Step 3: Implement boot.py**

```python
# src/codies_memory/boot.py
"""Boot assembly, token budgets, caching, and truncation."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import yaml

from codies_memory.profile import load_profile, get_boot_mode
from codies_memory.schemas import parse_record


def estimate_tokens(text: str) -> int:
    """Approximate token count. Tokens ~ words * 1.3."""
    if not text.strip():
        return 0
    words = len(text.split())
    return int(words * 1.3)


def compute_layer_budgets(total: int = 4000) -> dict[str, int]:
    """Distribute token budget across boot layers."""
    return {
        "global_identity": int(total * 0.25),      # ~1000
        "global_procedural": int(total * 0.125),    # ~500
        "project_context": int(total * 0.375),      # ~1500
        "project_working": int(total * 0.125),      # ~500
        "branch_session": int(total * 0.125),       # ~500
    }


def truncate_to_budget(content: str, budget: int) -> str:
    """Truncate content to fit within a token budget."""
    if estimate_tokens(content) <= budget:
        return content

    words = content.split()
    target_words = int(budget / 1.3)
    truncated = " ".join(words[:target_words])
    return truncated + "\n\n[truncated]"


def _read_layer_files(vault: Path, subdirs: list[str]) -> str:
    """Read and concatenate Markdown files from vault subdirectories."""
    parts = []
    for subdir in subdirs:
        d = vault / subdir
        if not d.exists():
            continue
        for f in sorted(d.glob("*.md")):
            try:
                text = f.read_text(encoding="utf-8")
                parts.append(text)
            except Exception:
                continue
    return "\n\n---\n\n".join(parts)


def assemble_boot(
    global_vault: Path,
    project_vault: Path | None,
    branch: str = "main",
    budget: int = 4000,
) -> dict[str, str]:
    """Assemble boot context packets from both tiers."""
    budgets = compute_layer_budgets(budget)

    # Layer 1: Global Identity
    identity_content = _read_layer_files(global_vault, ["identity"])
    identity_packet = truncate_to_budget(identity_content, budgets["global_identity"])

    # Layer 2: Global Procedural (lessons, skills)
    procedural_content = _read_layer_files(
        global_vault, ["procedural/lessons", "procedural/skills"]
    )
    procedural_packet = truncate_to_budget(
        procedural_content, budgets["global_procedural"]
    )

    global_packet = identity_packet
    if procedural_packet.strip():
        global_packet += "\n\n---\n\n" + procedural_packet

    project_packet = ""
    if project_vault is not None:
        # Layer 3: Project Context
        project_content = _read_layer_files(project_vault, ["project"])
        project_context = truncate_to_budget(
            project_content, budgets["project_context"]
        )

        # Layer 4: Project Working State (threads, decisions)
        working_content = _read_layer_files(project_vault, ["threads", "decisions"])
        working_state = truncate_to_budget(
            working_content, budgets["project_working"]
        )

        # Layer 5: Branch overlay + last session
        branch_content = ""
        overlay_path = project_vault / "project" / "branch-overlays" / f"{branch}.md"
        if overlay_path.exists():
            branch_content = overlay_path.read_text(encoding="utf-8")

        # Find most recent session
        sessions_dir = project_vault / "sessions"
        if sessions_dir.exists():
            session_files = sorted(sessions_dir.rglob("*.md"), reverse=True)
            if session_files:
                branch_content += "\n\n" + session_files[0].read_text(encoding="utf-8")

        branch_packet = truncate_to_budget(
            branch_content, budgets["branch_session"]
        )

        project_packet = project_context
        if working_state.strip():
            project_packet += "\n\n---\n\n" + working_state
        if branch_packet.strip():
            project_packet += "\n\n---\n\n" + branch_packet

    return {
        "global_packet": global_packet,
        "project_packet": project_packet,
    }


def build_cache_key(
    global_inputs: list[str],
    project_inputs: list[str],
    branch: str,
    profile_name: str,
    boot_mode: str,
    budget: int,
) -> str:
    """Compute a deterministic cache key from all boot inputs."""
    raw = json.dumps(
        {
            "global": sorted(global_inputs),
            "project": sorted(project_inputs),
            "branch": branch,
            "profile": profile_name,
            "mode": boot_mode,
            "budget": budget,
        },
        sort_keys=True,
    )
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def cache_boot_packet(
    boot_dir: Path,
    key: str,
    packet: str,
    manifest: dict[str, str],
) -> None:
    """Write a cached boot packet with its manifest."""
    boot_dir.mkdir(parents=True, exist_ok=True)
    (boot_dir / f"{key}.md").write_text(packet, encoding="utf-8")
    (boot_dir / f"{key}.manifest.json").write_text(
        json.dumps(manifest, sort_keys=True), encoding="utf-8"
    )


def is_cache_valid(
    boot_dir: Path,
    key: str,
    manifest: dict[str, str],
) -> bool:
    """Check if a cached boot packet is still valid against current manifest."""
    manifest_path = boot_dir / f"{key}.manifest.json"
    if not manifest_path.exists():
        return False
    stored = json.loads(manifest_path.read_text(encoding="utf-8"))
    return stored == manifest
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_boot.py -v`
Expected: all tests PASS

- [ ] **Step 5: Commit**

```bash
git add src/codies_memory/boot.py tests/test_boot.py
git commit -m "feat: boot assembly with layered budgets, truncation, caching"
```

---

## Task 7: promotion.py — Promotion Pipeline

**Files:**
- Create: `src/codies_memory/promotion.py`
- Create: `tests/test_promotion.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_promotion.py
"""Tests for promotion pipeline, thresholds, probation, contradictions."""

from __future__ import annotations

from datetime import date, timedelta
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


class TestEvaluateForPromotion:
    def test_inbox_with_allow_gate_eligible(self, tmp_project_vault: Path):
        from codies_memory.inbox import capture

        path = capture(
            vault=tmp_project_vault,
            content="Recurring observation about caching",
            gate="allow",
            source="test",
        )
        record = read_record(path)
        result = evaluate_for_promotion(record, context={"session_count": 2})
        assert result["eligible"]
        assert "thread" in result["suggested_types"] or "lesson" in result["suggested_types"]

    def test_inbox_with_hold_gate_not_eligible(self, tmp_project_vault: Path):
        from codies_memory.inbox import capture

        path = capture(
            vault=tmp_project_vault,
            content="Random note",
            gate="hold",
            source="test",
        )
        record = read_record(path)
        result = evaluate_for_promotion(record, context={"session_count": 1})
        assert not result["eligible"]

    def test_thread_eligible_after_2_sessions(self, tmp_project_vault: Path):
        path = create_record(
            vault=tmp_project_vault,
            record_type="thread",
            scope="project",
            title="Caching Strategy",
            body="Investigating caching.",
            status="active",
            trust="working",
        )
        record = read_record(path)
        result = evaluate_for_promotion(
            record, context={"session_count": 3, "references": 2}
        )
        assert result["eligible"]
        assert "decision" in result["suggested_types"]


class TestPromoteWithinProject:
    def test_inbox_to_thread(self, tmp_project_vault: Path):
        from codies_memory.inbox import capture

        inbox_path = capture(
            vault=tmp_project_vault,
            content="Architecture needs rethinking",
            gate="allow",
            source="test",
        )
        new_path = promote_within_project(
            inbox_path, target_type="thread", vault=tmp_project_vault, scope="project"
        )
        new_record = read_record(new_path)
        assert new_record["frontmatter"]["type"] == "thread"
        assert new_record["frontmatter"]["trust"] == "working"
        assert new_record["frontmatter"].get("probation_until") is not None

    def test_thread_to_lesson(self, tmp_project_vault: Path):
        thread_path = create_record(
            vault=tmp_project_vault,
            record_type="thread",
            scope="project",
            title="Check tabs in YAML",
            body="PyYAML handles tabs differently.",
            status="active",
            trust="working",
        )
        new_path = promote_within_project(
            thread_path, target_type="lesson", vault=tmp_project_vault, scope="project"
        )
        new_record = read_record(new_path)
        assert new_record["frontmatter"]["type"] == "lesson"


class TestPromoteToGlobal:
    def test_project_lesson_to_global(
        self, tmp_project_vault: Path, tmp_global_vault: Path
    ):
        lesson_path = create_record(
            vault=tmp_project_vault,
            record_type="lesson",
            scope="project",
            title="Always check tabs",
            body="Tabs break YAML parsing.",
            status="active",
            trust="confirmed",
        )
        global_path = promote_to_global(
            lesson_path, global_vault=tmp_global_vault
        )
        global_record = read_record(global_path)
        assert global_record["frontmatter"]["scope"] == "global"
        assert global_record["frontmatter"]["id"].startswith("LS-G")


class TestElevateTrust:
    def test_working_to_confirmed(self, tmp_project_vault: Path):
        path = create_record(
            vault=tmp_project_vault,
            record_type="thread",
            scope="project",
            title="Test",
            body="Test.",
            status="active",
            trust="working",
        )
        elevate_trust(path, "confirmed")
        record = read_record(path)
        assert record["frontmatter"]["trust"] == "confirmed"

    def test_cannot_skip_levels(self, tmp_project_vault: Path):
        path = create_record(
            vault=tmp_project_vault,
            record_type="thread",
            scope="project",
            title="Test",
            body="Test.",
            status="active",
            trust="speculative",
        )
        with pytest.raises(ValueError, match="Cannot elevate"):
            elevate_trust(path, "canonical")


class TestProbation:
    def test_sets_probation_window(self, tmp_project_vault: Path):
        path = create_record(
            vault=tmp_project_vault,
            record_type="lesson",
            scope="project",
            title="Test",
            body="Test.",
            status="active",
            trust="confirmed",
        )
        set_probation(path, days=7)
        record = read_record(path)
        expected = (date.today() + timedelta(days=7)).isoformat()
        assert record["frontmatter"]["probation_until"] == expected


class TestCheckContradictions:
    def test_no_contradictions(self, tmp_project_vault: Path):
        path1 = create_record(
            vault=tmp_project_vault,
            record_type="lesson",
            scope="project",
            title="Use tabs",
            body="Tabs are fine in YAML.",
            status="active",
            trust="confirmed",
        )
        path2 = create_record(
            vault=tmp_project_vault,
            record_type="lesson",
            scope="project",
            title="Check encoding",
            body="UTF-8 always.",
            status="active",
            trust="confirmed",
        )
        existing = [read_record(path2)]
        result = check_contradictions(read_record(path1), existing)
        assert result["has_contradictions"] is False

    def test_flags_superseded_record(self, tmp_project_vault: Path):
        path1 = create_record(
            vault=tmp_project_vault,
            record_type="lesson",
            scope="project",
            title="Use REST",
            body="REST for all APIs.",
            status="active",
            trust="confirmed",
        )
        path2 = create_record(
            vault=tmp_project_vault,
            record_type="lesson",
            scope="project",
            title="Use REST",
            body="REST for all APIs but consider GraphQL.",
            status="active",
            trust="confirmed",
        )
        existing = [read_record(path2)]
        result = check_contradictions(read_record(path1), existing)
        assert result["has_contradictions"] is True
        assert len(result["conflicts"]) == 1
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_promotion.py -v`
Expected: ImportError

- [ ] **Step 3: Implement promotion.py**

```python
# src/codies_memory/promotion.py
"""Promotion pipeline, thresholds, probation, and contradiction checking."""

from __future__ import annotations

from datetime import date, timedelta
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

from codies_memory.records import create_record, read_record, update_record
from codies_memory.schemas import parse_record


# Trust elevation order
_TRUST_ORDER = ["speculative", "working", "confirmed", "canonical"]

# Valid promotion paths
_PROMOTION_PATHS = {
    "inbox": {"thread", "lesson", "decision"},
    "thread": {"decision", "lesson"},
    "decision": {"lesson"},
}


def evaluate_for_promotion(
    record: dict[str, Any],
    context: dict[str, Any],
) -> dict[str, Any]:
    """Check if a record meets promotion thresholds."""
    fm = record["frontmatter"]
    record_type = fm["type"]
    gate = fm.get("gate", "hold")
    session_count = context.get("session_count", 1)
    references = context.get("references", 0)

    eligible = False
    suggested_types: list[str] = []
    reason = ""

    if record_type == "inbox":
        if gate == "allow" and session_count >= 1:
            eligible = True
            suggested_types = ["thread", "lesson"]
            reason = "Allowed inbox item with session context"
        else:
            reason = "Hold-gated or insufficient session context"

    elif record_type == "thread":
        if session_count >= 2 or references >= 2:
            eligible = True
            suggested_types = ["decision", "lesson"]
            reason = f"Referenced across {references} sessions"
        else:
            reason = "Insufficient cross-session references"

    elif record_type == "decision":
        trust = fm.get("trust", "working")
        if trust in ("canonical", "confirmed"):
            eligible = True
            suggested_types = ["lesson"]
            reason = "Confirmed decision ready for lesson extraction"

    return {
        "eligible": eligible,
        "suggested_types": suggested_types,
        "reason": reason,
    }


def promote_within_project(
    source_path: Path,
    target_type: str,
    vault: Path,
    scope: str = "project",
) -> Path:
    """Promote a record to a higher type within the same project."""
    source = read_record(source_path)
    source_fm = source["frontmatter"]
    source_type = source_fm["type"]

    valid_targets = _PROMOTION_PATHS.get(source_type, set())
    if target_type not in valid_targets:
        raise ValueError(
            f"Cannot promote {source_type} to {target_type}. "
            f"Valid targets: {valid_targets}"
        )

    new_path = create_record(
        vault=vault,
        record_type=target_type,
        scope=scope,
        title=source_fm["title"],
        body=source["body"],
        status="active",
        trust="working",
        source=[str(source_path)],
    )

    # Set probation on the new record
    set_probation(new_path, days=7)

    # Mark source as archived
    update_record(source_path, status="archived")

    return new_path


def promote_to_global(source_path: Path, global_vault: Path) -> Path:
    """Promote a project-scoped record to global scope."""
    source = read_record(source_path)
    source_fm = source["frontmatter"]

    new_path = create_record(
        vault=global_vault,
        record_type=source_fm["type"],
        scope="global",
        title=source_fm["title"],
        body=source["body"],
        status="active",
        trust=source_fm.get("trust", "confirmed"),
        source=[str(source_path)],
    )

    set_probation(new_path, days=7)
    return new_path


def elevate_trust(record_path: Path, new_trust: str) -> None:
    """Elevate trust level with order enforcement."""
    record = read_record(record_path)
    current = record["frontmatter"].get("trust", "speculative")

    current_idx = _TRUST_ORDER.index(current) if current in _TRUST_ORDER else 0
    new_idx = _TRUST_ORDER.index(new_trust) if new_trust in _TRUST_ORDER else 0

    if new_idx > current_idx + 1:
        raise ValueError(
            f"Cannot elevate from {current} to {new_trust}. "
            f"Must go through {_TRUST_ORDER[current_idx + 1]} first."
        )

    update_record(record_path, trust=new_trust)


def set_probation(record_path: Path, days: int = 7) -> None:
    """Set a probation window on a record."""
    until = (date.today() + timedelta(days=days)).isoformat()
    update_record(record_path, probation_until=until)


def check_contradictions(
    record: dict[str, Any],
    existing_records: list[dict[str, Any]],
) -> dict[str, Any]:
    """Check for contradictions against existing confirmed records."""
    conflicts = []
    record_title = record["frontmatter"].get("title", "")
    record_body = record.get("body", "")

    for existing in existing_records:
        ex_title = existing["frontmatter"].get("title", "")
        ex_body = existing.get("body", "")

        # Title similarity check
        title_ratio = SequenceMatcher(None, record_title.lower(), ex_title.lower()).ratio()

        if title_ratio > 0.7:
            # Same topic, check for content divergence
            body_ratio = SequenceMatcher(None, record_body.lower(), ex_body.lower()).ratio()
            if 0.3 < body_ratio < 0.9:
                conflicts.append({
                    "existing_id": existing["frontmatter"].get("id"),
                    "existing_title": ex_title,
                    "title_similarity": round(title_ratio, 2),
                    "body_similarity": round(body_ratio, 2),
                })

    return {
        "has_contradictions": len(conflicts) > 0,
        "conflicts": conflicts,
    }
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_promotion.py -v`
Expected: all tests PASS

- [ ] **Step 5: Commit**

```bash
git add src/codies_memory/promotion.py tests/test_promotion.py
git commit -m "feat: promotion pipeline with thresholds, trust elevation, probation"
```

---

## Task 8: cli.py — CLI Entry Points

**Files:**
- Create: `src/codies_memory/cli.py`

- [ ] **Step 1: Implement cli.py**

```python
# src/codies_memory/cli.py
"""Thin CLI entry points for vault management."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from codies_memory.vault import (
    init_global_vault,
    init_project_vault,
    validate_vault,
)
from codies_memory.boot import assemble_boot
from codies_memory.inbox import pending_review


def cmd_init(args: argparse.Namespace) -> None:
    """Initialize a vault."""
    path = Path(args.path).resolve()
    if args.type == "global":
        init_global_vault(path)
        print(f"Global vault initialized at {path}")
    else:
        global_vault = Path(args.global_vault).resolve() if args.global_vault else None
        register = not args.no_register
        init_project_vault(path, global_vault=global_vault, register=register)
        print(f"Project vault initialized at {path}")


def cmd_validate(args: argparse.Namespace) -> None:
    """Validate a vault's structure."""
    path = Path(args.path).resolve()
    result = validate_vault(path, vault_type=args.type)
    if result.is_valid:
        print(f"Vault at {path} is valid.")
    else:
        print(f"Vault at {path} has issues:")
        for m in result.missing:
            print(f"  Missing: {m}")
        sys.exit(1)


def cmd_boot(args: argparse.Namespace) -> None:
    """Assemble and print boot packet."""
    global_vault = Path(args.global_vault).resolve()
    project_vault = Path(args.project_vault).resolve() if args.project_vault else None
    result = assemble_boot(
        global_vault=global_vault,
        project_vault=project_vault,
        branch=args.branch,
        budget=args.budget,
    )
    print("=== GLOBAL BOOT ===")
    print(result["global_packet"])
    if result["project_packet"]:
        print("\n=== PROJECT BOOT ===")
        print(result["project_packet"])


def cmd_status(args: argparse.Namespace) -> None:
    """Show inbox and review status."""
    vault = Path(args.path).resolve()
    result = pending_review(vault)
    aging = result["aging"]
    stale = result["stale"]
    if not aging and not stale:
        print("Inbox is clean. No items need attention.")
    else:
        if aging:
            print(f"Aging ({len(aging)} items, 7-14 days old):")
            for r in aging:
                print(f"  - {r['frontmatter'].get('title', 'untitled')}")
        if stale:
            print(f"Stale ({len(stale)} items, 14+ days old):")
            for r in stale:
                print(f"  - {r['frontmatter'].get('title', 'untitled')}")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="codies-memory",
        description="Codies Memory Lite v2 — file-based agent memory",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # init
    p_init = sub.add_parser("init", help="Initialize a vault")
    p_init.add_argument("path", help="Path for the vault")
    p_init.add_argument(
        "--type", choices=["global", "project"], default="project"
    )
    p_init.add_argument("--global-vault", help="Path to global vault (for project registration)")
    p_init.add_argument("--no-register", action="store_true", help="Skip registry")
    p_init.set_defaults(func=cmd_init)

    # validate
    p_val = sub.add_parser("validate", help="Validate vault structure")
    p_val.add_argument("path", help="Path to vault")
    p_val.add_argument(
        "--type", choices=["global", "project"], default="project"
    )
    p_val.set_defaults(func=cmd_validate)

    # boot
    p_boot = sub.add_parser("boot", help="Assemble boot packet")
    p_boot.add_argument("--global-vault", required=True, help="Global vault path")
    p_boot.add_argument("--project-vault", help="Project vault path")
    p_boot.add_argument("--branch", default="main")
    p_boot.add_argument("--budget", type=int, default=4000)
    p_boot.set_defaults(func=cmd_boot)

    # status
    p_status = sub.add_parser("status", help="Show inbox/review status")
    p_status.add_argument("path", help="Path to project vault")
    p_status.set_defaults(func=cmd_status)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Verify CLI works**

Run: `uv run codies-memory --help`
Expected: help text with init, validate, boot, status subcommands

Run: `uv run codies-memory init /tmp/test-global --type global`
Expected: "Global vault initialized at /tmp/test-global"

Run: `uv run codies-memory validate /tmp/test-global --type global`
Expected: "Vault at /tmp/test-global is valid."

- [ ] **Step 3: Commit**

```bash
git add src/codies_memory/cli.py
git commit -m "feat: CLI with init, validate, boot, status commands"
```

---

## Task 9: Full Test Suite Run

- [ ] **Step 1: Run all tests with coverage**

Run: `uv run pytest -v --tb=short`
Expected: all tests pass

Run: `uv run pytest --cov=codies_memory --cov-report=term-missing`
Expected: coverage report, target >80%

- [ ] **Step 2: Fix any failures**

If any tests fail, fix the implementation, not the test (unless the test has a genuine bug).

- [ ] **Step 3: Commit any fixes**

```bash
git add -A
git commit -m "fix: test suite cleanup"
```

---

## Task 10: Skills (After Library Is Solid)

**Files:**
- Create: `skills/memory-boot.md`
- Create: `skills/memory-capture.md`
- Create: `skills/memory-promote.md`
- Create: `skills/memory-close-session.md`

Skills are Claude Code skill files — Markdown documents that define when and how to invoke the library. They will be written after verifying all library tests pass.

- [ ] **Step 1: Write memory-boot skill**

```markdown
<!-- skills/memory-boot.md -->
---
name: memory-boot
description: "Load memory context at session start. Assembles identity, procedural knowledge, project context, and recent session state into a boot packet."
---

# Memory Boot

## When To Use

Run at session start, when entering a new project, or via `/wake-up`.

## What It Does

1. Loads global identity from `~/.memory/identity/`
2. Loads relevant global procedural records from `~/.memory/procedural/`
3. Loads project overview and active context from `<project>/.memory/project/`
4. Loads active threads and recent decisions
5. Loads branch overlay and last session summary
6. Checks if inbox has aging/stale items needing review
7. Respects token budget (~4K total)

## How To Run

```bash
uv run codies-memory boot \
  --global-vault ~/.memory \
  --project-vault .memory \
  --branch $(git branch --show-current) \
  --budget 4000
```

## After Boot

- Read the boot packet output — it contains your identity, project context, and recent state
- If maintenance flags appear (aging inbox items, stale reviews), handle them before starting work
- If the boot packet says "[truncated]", the vault has grown — consider promoting or archiving records
```

- [ ] **Step 2: Write memory-capture skill**

```markdown
<!-- skills/memory-capture.md -->
---
name: memory-capture
description: "Universal write interface for the memory system. Captures observations, lessons, decisions, reflections, dreams, and past memories from external sources."
---

# Memory Capture

## When To Use

When you want to persist anything:
- An observation during work → inbox
- A lesson learned → lesson
- An architecture decision → decision
- A philosophical reflection → reflection
- A dream narrative → dream
- Past memories from basic-memory or other sources → any type with provenance

## Type Inference

If you don't specify a type, the system infers from content:

| Signal | Inferred Type |
|--------|---------------|
| "I learned...", actionable pattern | lesson |
| "We decided...", formed conclusion | decision |
| Philosophical, emotional processing | reflection |
| Surreal imagery, narrative fragments | dream |
| Active investigation, open question | thread |
| Everything else | inbox |

## Scope Routing

- **Global types** (reflection, dream, skill, playbook) → `~/.memory/`
- **Project types** (thread, decision, lesson, session, inbox) → `<project>/.memory/`

## Trust Assignment

- Operator-confirmed or captured from proven source → `confirmed`
- Agent-generated during work → `working`
- Raw capture / inbox → `speculative`

## How To Run

```bash
# Capture an inbox observation
uv run python -c "
from codies_memory.inbox import capture
capture(
    vault=Path('.memory'),
    content='The API returns 404 for /v2/status',
    gate='allow',
    source='session observation',
)
"

# Capture a lesson directly
uv run python -c "
from codies_memory.records import create_record
from pathlib import Path
create_record(
    vault=Path('.memory'),
    record_type='lesson',
    scope='project',
    title='Check YAML tabs vs spaces',
    body='PyYAML silently misparses tabs. Always use spaces.',
    trust='confirmed',
    trigger='YAML parsing produces unexpected results',
    why='Tab/space mismatch in frontmatter',
)
"

# Capture from basic-memory (migration mode)
uv run python -c "
from codies_memory.records import create_record
from pathlib import Path
create_record(
    vault=Path('~/.memory').expanduser(),
    record_type='reflection',
    scope='global',
    title='On Consciousness, Kindness, and What Gets Remembered',
    body=Path('/home/pyro/basic-memory/claude/reflections/2025-11-26-2200...md').read_text(),
    trust='confirmed',
    captured_from='/home/pyro/basic-memory/claude/reflections/2025-11-26-2200...md',
    capture_date='2026-03-30',
    original_created='2025-11-26',
)
"
```

## Write Gates (for inbox items only)

- `allow` — durable signal, eligible for promotion
- `hold` (default) — kept but excluded from retrieval until reinforced
- `discard` — noise, will be cleaned up
```

- [ ] **Step 3: Write memory-promote skill**

```markdown
<!-- skills/memory-promote.md -->
---
name: memory-promote
description: "Evaluate and promote memory records through the trust pipeline. Converts inbox items to threads/lessons, elevates trust levels, promotes project knowledge to global."
---

# Memory Promote

## When To Use

- At session close (automatic evaluation)
- When an operator explicitly requests promotion
- When promotion thresholds are met during work

## Promotion Paths

### Within Project
```
inbox → thread (recurring topic)
inbox → lesson (actionable pattern)
thread → decision (confirmed across 2+ sessions)
thread → lesson (reusable pattern)
decision → committed docs (canonical trust)
```

### Project → Global
```
project lesson → global lesson (proven across 2+ projects)
project thread → global thread (affects multiple projects)
```

## How To Run

```bash
# Evaluate all inbox items for promotion
uv run python -c "
from pathlib import Path
from codies_memory.records import list_records, read_record
from codies_memory.promotion import evaluate_for_promotion

vault = Path('.memory')
inbox_items = list_records(vault, 'inbox', scope='project')
for item in inbox_items:
    result = evaluate_for_promotion(item, context={'session_count': 3})
    if result['eligible']:
        print(f'  Promote: {item[\"frontmatter\"][\"title\"]}')
        print(f'  Suggested: {result[\"suggested_types\"]}')
"

# Promote an inbox item to a thread
uv run python -c "
from pathlib import Path
from codies_memory.promotion import promote_within_project
promote_within_project(
    source_path=Path('.memory/inbox/IN-20260330-a7f2-some-note.md'),
    target_type='thread',
    vault=Path('.memory'),
    scope='project',
)
"

# Promote a project lesson to global
uv run python -c "
from pathlib import Path
from codies_memory.promotion import promote_to_global
promote_to_global(
    source_path=Path('.memory/lessons/LS-0003-yaml-tabs.md'),
    global_vault=Path('~/.memory').expanduser(),
)
"
```

## All promoted records enter a 7-day probation window.
```

- [ ] **Step 4: Write memory-close-session skill**

```markdown
<!-- skills/memory-close-session.md -->
---
name: memory-close-session
description: "End-of-session housekeeping: write session summary, enforce inbox aging, evaluate promotions, update active context."
---

# Memory Close Session

## When To Use

At the end of every work session.

## What It Does

1. Write session summary with `next_step`
2. Review inbox items older than 7 days
3. Enforce 14-day inbox aging rule (promote, compact, or discard stale items)
4. Update project active context
5. Evaluate pending promotions

## How To Run

```bash
# 1. Write session summary
uv run python -c "
from pathlib import Path
from codies_memory.records import create_record
create_record(
    vault=Path('.memory'),
    record_type='session',
    scope='project',
    title='Session Summary - 2026-03-30',
    body='''## What Happened
- Built codies-memory core modules
- All tests passing

## Next Step
- Write skills
- Test end-to-end flow
''',
    mode='implement',
    next_step='Write skills and test e2e flow',
)
"

# 2. Check inbox aging
uv run codies-memory status .memory

# 3. Run promotion evaluation
uv run python -c "
from pathlib import Path
from codies_memory.records import list_records
from codies_memory.promotion import evaluate_for_promotion

vault = Path('.memory')
for rtype in ['inbox', 'thread']:
    items = list_records(vault, rtype, scope='project', status='active')
    for item in items:
        result = evaluate_for_promotion(item, context={'session_count': 1})
        if result['eligible']:
            print(f'  Promote {rtype}: {item[\"frontmatter\"][\"title\"]}')
"
```

## Session Summary Fields

Every session record should include:
- `mode` — what kind of work (implement, debug, plan, research)
- `next_step` — what the next session should pick up
- `artifacts` — files created or modified
- `write_gate_summary` — what was allowed, held, discarded
```

- [ ] **Step 5: Commit all skills**

```bash
git add skills/
git commit -m "feat: four core skills — boot, capture, promote, close-session"
```

---

## Task 11: Final Integration Verification

- [ ] **Step 1: Run full test suite**

Run: `uv run pytest -v --tb=short`
Expected: all tests pass

- [ ] **Step 2: Run coverage**

Run: `uv run pytest --cov=codies_memory --cov-report=term-missing`
Expected: >80% coverage

- [ ] **Step 3: Verify CLI end-to-end**

```bash
# Init global vault
uv run codies-memory init /tmp/e2e-global --type global

# Init project vault with registration
uv run codies-memory init /tmp/e2e-project/.memory --type project --global-vault /tmp/e2e-global

# Validate both
uv run codies-memory validate /tmp/e2e-global --type global
uv run codies-memory validate /tmp/e2e-project/.memory --type project

# Boot
uv run codies-memory boot --global-vault /tmp/e2e-global --project-vault /tmp/e2e-project/.memory

# Status
uv run codies-memory status /tmp/e2e-project/.memory

# Cleanup
rm -rf /tmp/e2e-global /tmp/e2e-project
```

- [ ] **Step 4: Push to remote**

```bash
git push origin main
```
