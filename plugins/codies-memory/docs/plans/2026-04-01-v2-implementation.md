# v2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement agent-namespaced vaults, fix all known bugs, and add CLI write commands so codies-memory is ready for multi-agent live testing.

**Architecture:** Three-phase approach — fix the foundation (vault layout + schemas), fix the bugs (library layer), then build the CLI surface. Each phase produces passing tests before the next begins.

**Tech Stack:** Python 3.11+, PyYAML, argparse, pytest, uv

**Spec:** `docs/specs/2026-04-01-v2-vault-layout-bugfixes-cli.md`

---

## File Map

### Modified Files

| File | Changes |
|------|---------|
| `src/codies_memory/vault.py` | Agent-namespaced paths, project resolution, marker files, required-file validation, `_PATH_MAP` fix |
| `src/codies_memory/schemas.py` | `validate_frontmatter()` enforcement, session field alignment, status validation |
| `src/codies_memory/records.py` | `update_record()` revalidation, `_slugify()` empty guard |
| `src/codies_memory/inbox.py` | `active_inbox()`, updated `pending_review()` |
| `src/codies_memory/promotion.py` | Type guard on `promote_to_global()`, demotion guard on `elevate_trust()` |
| `src/codies_memory/profile.py` | `copy.deepcopy()` fix |
| `src/codies_memory/boot.py` | `build_cache_key()` serialization fix |
| `src/codies_memory/cli.py` | Full rewrite: v2 paths + 4 new subcommands |
| `tests/test_vault.py` | New tests for v2 layout, project resolution, required-file validation |
| `tests/test_schemas.py` | New tests for status validation, type enforcement |
| `tests/test_records.py` | New tests for update validation, empty slugify |
| `tests/test_inbox.py` | New tests for active_inbox, updated pending_review |
| `tests/test_promotion.py` | New tests for type guard, demotion guard |
| `tests/test_profile.py` | New test for deepcopy isolation |
| `tests/test_boot.py` | New tests for non-serializable cache key inputs |
| `tests/test_cli.py` | New file: CLI integration tests |
| `skills/memory-boot.md` | Path updates, remove false inbox claim |
| `skills/memory-capture.md` | Path updates, complete gate docs |
| `skills/memory-close-session.md` | Path updates, fix `$(date)`, fix schema fields |
| `skills/memory-promote.md` | Path updates, fix promotion path docs |
| `pyproject.toml` | Version bump to 1.0.0 |
| `INSTALL.md` | Rewrite for v2 paths |
| `README.md` | Update file map, fix broken relative links |

---

## Phase 1: Vault Layout v2

Foundation changes. Everything else depends on this.

### Task 1: Add `resolve_global_vault()` and update constants

**Files:**
- Modify: `src/codies_memory/vault.py`
- Modify: `tests/test_vault.py`

- [ ] **Step 1: Write failing test for `resolve_global_vault()`**

```python
def test_resolve_global_vault():
    result = resolve_global_vault("claude")
    assert result == Path.home() / ".memory" / "claude"

def test_resolve_global_vault_codie():
    result = resolve_global_vault("codie")
    assert result == Path.home() / ".memory" / "codie"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_vault.py::test_resolve_global_vault -v`
Expected: FAIL — `ImportError: cannot import name 'resolve_global_vault'`

- [ ] **Step 3: Implement `resolve_global_vault()` and update `GLOBAL_DIRS`**

In `vault.py`:

```python
def resolve_global_vault(agent: str) -> Path:
    """Return the global vault path for the given agent name."""
    return Path.home() / ".memory" / agent
```

Add `"projects"` to `GLOBAL_DIRS` list.

Add `("identity", "global"): "identity"` to `_PATH_MAP`.

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_vault.py::test_resolve_global_vault tests/test_vault.py::test_resolve_global_vault_codie -v`
Expected: PASS

- [ ] **Step 5: Run full test suite to check for regressions**

Run: `uv run pytest -v`
Expected: All 116+ tests pass

- [ ] **Step 6: Commit**

```bash
git add src/codies_memory/vault.py tests/test_vault.py
git commit -m "feat: add resolve_global_vault() and update vault constants"
```

---

### Task 2: Rework `init_project_vault()` for project-external storage

**Files:**
- Modify: `src/codies_memory/vault.py`
- Modify: `tests/test_vault.py`

- [ ] **Step 1: Write failing tests for new project init behavior**

```python
def test_init_project_vault_v2(tmp_path):
    global_vault = tmp_path / "global"
    init_global_vault(global_vault)
    working_dir = tmp_path / "my-project"
    working_dir.mkdir()

    vault = init_project_vault(
        global_vault=global_vault,
        slug="my-project",
        working_dir=working_dir,
    )

    # Vault lives under global/projects/slug/
    assert vault == global_vault / "projects" / "my-project"
    assert (vault / "inbox").is_dir()
    assert (vault / "profile.yaml").exists()

    # Marker file created in working dir
    marker = working_dir / ".codies-memory"
    assert marker.exists()
    assert marker.read_text().strip() == "my-project"

    # Registered in global registry
    import yaml
    registry = yaml.safe_load((global_vault / "registry" / "projects.yaml").read_text())
    slugs = [p["slug"] for p in registry["projects"]]
    assert "my-project" in slugs


def test_init_project_vault_v2_default_slug(tmp_path):
    global_vault = tmp_path / "global"
    init_global_vault(global_vault)
    working_dir = tmp_path / "cool-app"
    working_dir.mkdir()

    vault = init_project_vault(
        global_vault=global_vault,
        working_dir=working_dir,
    )
    # Slug defaults to working dir name
    assert vault == global_vault / "projects" / "cool-app"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_vault.py::test_init_project_vault_v2 -v`
Expected: FAIL — signature mismatch

- [ ] **Step 3: Implement new `init_project_vault()` signature**

```python
def init_project_vault(
    global_vault: Path,
    slug: str | None = None,
    working_dir: Path | None = None,
    register: bool = True,
) -> Path:
    """Create project vault under global_vault/projects/slug/.

    Creates marker file in working_dir. Registers in global registry.
    Slug defaults to working_dir.name if not provided.
    working_dir defaults to Path.cwd() if not provided.
    """
    if working_dir is None:
        working_dir = Path.cwd()
    if slug is None:
        slug = working_dir.name

    root = global_vault / "projects" / slug
    for d in PROJECT_DIRS:
        (root / d).mkdir(parents=True, exist_ok=True)

    _write_if_missing(root / "profile.yaml", f"project_name: {slug}\n")

    # Write marker file in working directory
    marker = working_dir / ".codies-memory"
    marker.write_text(f"{slug}\n")

    if register:
        git_remote = _get_git_remote(working_dir)
        register_project_vault(
            global_vault=global_vault,
            slug=slug,
            working_dir=str(working_dir),
            metadata={},
            git_remote=git_remote,
        )

    return root
```

Add helper:

```python
def _get_git_remote(working_dir: Path) -> str | None:
    """Try to get git remote URL from working_dir. Returns None on failure."""
    import subprocess
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=working_dir, capture_output=True, text=True, timeout=5,
        )
        return result.stdout.strip() if result.returncode == 0 else None
    except Exception:
        return None
```

Update `register_project_vault()` to accept `working_dir`, `git_remote`:

```python
def register_project_vault(
    global_vault: Path,
    slug: str,
    working_dir: str,
    metadata: dict,
    status: str = "active",
    git_remote: str | None = None,
) -> None:
    data = _read_registry(global_vault)
    projects: list[dict] = data["projects"]

    existing_index: int | None = None
    for i, entry in enumerate(projects):
        if entry.get("slug") == slug:
            existing_index = i
            break

    new_entry: dict = {
        "slug": slug,
        "working_dir": working_dir,
        "status": status,
        "metadata": metadata,
    }
    if git_remote:
        new_entry["git_remote"] = git_remote

    if existing_index is not None:
        projects[existing_index] = new_entry
    else:
        projects.append(new_entry)

    _write_registry(global_vault, data)
```

- [ ] **Step 4: Update existing tests that use old `init_project_vault()` signature**

All existing tests pass `root` as first arg. Update them to use the new `global_vault` + `working_dir` pattern. Use `tmp_path` fixtures.

- [ ] **Step 5: Run full test suite**

Run: `uv run pytest -v`
Expected: All tests pass

- [ ] **Step 6: Commit**

```bash
git add src/codies_memory/vault.py tests/test_vault.py
git commit -m "feat: project-external storage with marker files and registry v2"
```

---

### Task 3: Add `resolve_project_vault()` with three-tier lookup

**Files:**
- Modify: `src/codies_memory/vault.py`
- Modify: `tests/test_vault.py`

- [ ] **Step 1: Write failing tests for three-tier resolution**

```python
def test_resolve_via_marker(tmp_path):
    global_vault = tmp_path / "global"
    init_global_vault(global_vault)
    working_dir = tmp_path / "my-project"
    working_dir.mkdir()
    init_project_vault(global_vault=global_vault, slug="my-project", working_dir=working_dir)

    resolved = resolve_project_vault(global_vault, working_dir)
    assert resolved == global_vault / "projects" / "my-project"


def test_resolve_via_registry_working_dir(tmp_path):
    global_vault = tmp_path / "global"
    init_global_vault(global_vault)
    working_dir = tmp_path / "my-project"
    working_dir.mkdir()
    init_project_vault(global_vault=global_vault, slug="my-project", working_dir=working_dir)

    # Remove marker, fall through to registry
    (working_dir / ".codies-memory").unlink()

    resolved = resolve_project_vault(global_vault, working_dir)
    assert resolved == global_vault / "projects" / "my-project"


def test_resolve_unregistered_returns_none(tmp_path):
    global_vault = tmp_path / "global"
    init_global_vault(global_vault)
    unknown_dir = tmp_path / "unknown"
    unknown_dir.mkdir()

    resolved = resolve_project_vault(global_vault, unknown_dir)
    assert resolved is None
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_vault.py::test_resolve_via_marker -v`
Expected: FAIL — `ImportError: cannot import name 'resolve_project_vault'`

- [ ] **Step 3: Implement `resolve_project_vault()`**

```python
def resolve_project_vault(global_vault: Path, working_dir: Path) -> Path | None:
    """Resolve project vault from working_dir using three-tier lookup.

    1. Marker file (.codies-memory) in working_dir
    2. Registry working_dir match
    3. Git remote URL match

    Returns vault path or None if unresolved. Lazily updates registry
    working_dir if resolved via marker or git on a different path.
    """
    # Tier 1: marker file
    marker = working_dir / ".codies-memory"
    if marker.exists():
        slug = marker.read_text().strip()
        vault = global_vault / "projects" / slug
        if vault.is_dir():
            # Lazy update registry working_dir
            _update_registry_working_dir(global_vault, slug, str(working_dir))
            return vault

    # Tier 2: registry working_dir
    data = _read_registry(global_vault)
    for entry in data.get("projects", []):
        if entry.get("working_dir") == str(working_dir):
            slug = entry["slug"]
            vault = global_vault / "projects" / slug
            if vault.is_dir():
                return vault

    # Tier 3: git remote
    git_remote = _get_git_remote(working_dir)
    if git_remote:
        for entry in data.get("projects", []):
            if entry.get("git_remote") == git_remote:
                slug = entry["slug"]
                vault = global_vault / "projects" / slug
                if vault.is_dir():
                    _update_registry_working_dir(global_vault, slug, str(working_dir))
                    return vault

    return None


def _update_registry_working_dir(global_vault: Path, slug: str, working_dir: str) -> None:
    """Lazily update the working_dir for a project in the registry."""
    data = _read_registry(global_vault)
    for entry in data.get("projects", []):
        if entry.get("slug") == slug and entry.get("working_dir") != working_dir:
            entry["working_dir"] = working_dir
            _write_registry(global_vault, data)
            break
```

- [ ] **Step 4: Run tests**

Run: `uv run pytest tests/test_vault.py -v`
Expected: All pass

- [ ] **Step 5: Commit**

```bash
git add src/codies_memory/vault.py tests/test_vault.py
git commit -m "feat: three-tier project resolution (marker, registry, git remote)"
```

---

## Phase 2: Bug Fixes

Independent fixes. Each task is one commit.

### Task 4: BUG-01 — Fix `status` hiding fresh inbox items

**Files:**
- Modify: `src/codies_memory/inbox.py`
- Modify: `src/codies_memory/cli.py`
- Modify: `tests/test_inbox.py`

- [ ] **Step 1: Write failing test**

```python
def test_active_inbox_returns_fresh_items(tmp_vault):
    from codies_memory.inbox import capture, active_inbox
    capture(vault=tmp_vault, content="Fresh observation", source="test", gate="allow")
    result = active_inbox(tmp_vault)
    assert len(result) == 1
    assert result[0]["frontmatter"]["title"] == "Fresh observation"


def test_pending_review_includes_active_key(tmp_vault):
    from codies_memory.inbox import capture, pending_review
    capture(vault=tmp_vault, content="Fresh observation", source="test", gate="allow")
    result = pending_review(tmp_vault)
    assert "active" in result
    assert len(result["active"]) == 1
```

- [ ] **Step 2: Run to verify fail**

Run: `uv run pytest tests/test_inbox.py::test_active_inbox_returns_fresh_items -v`
Expected: FAIL

- [ ] **Step 3: Implement `active_inbox()` and update `pending_review()`**

In `inbox.py`:

```python
def active_inbox(vault: Path) -> list[dict]:
    """Return all non-archived inbox records."""
    inbox_dir = resolve_path(vault, "inbox", "project")
    if not inbox_dir.is_dir():
        return []
    results: list[dict] = []
    for md_file in inbox_dir.glob("*.md"):
        try:
            record = parse_record(md_file)
        except Exception:
            continue
        if record["frontmatter"].get("status") != "archived":
            results.append(record)
    return results


def pending_review(vault: Path) -> dict:
    """Return inbox records grouped by urgency."""
    active = active_inbox(vault)
    aged = age_inbox(vault)
    return {
        "active": active,
        "aging": aged.get("aging", []),
        "stale": aged.get("stale", []),
    }
```

- [ ] **Step 4: Run tests**

Run: `uv run pytest tests/test_inbox.py -v`
Expected: All pass

- [ ] **Step 5: Commit**

```bash
git add src/codies_memory/inbox.py tests/test_inbox.py
git commit -m "fix: status now shows fresh inbox items (BUG-01)"
```

---

### Task 5: BUG-02 — Type guard on `promote_to_global()`

**Files:**
- Modify: `src/codies_memory/promotion.py`
- Modify: `tests/test_promotion.py`

- [ ] **Step 1: Write failing tests**

```python
def test_promote_to_global_rejects_thread(tmp_global, tmp_project, thread_path):
    with pytest.raises(ValueError, match="Only lessons can be promoted to global"):
        promote_to_global(source_path=thread_path, global_vault=tmp_global)


def test_promote_to_global_rejects_decision(tmp_global, tmp_project, decision_path):
    with pytest.raises(ValueError, match="Only lessons can be promoted to global"):
        promote_to_global(source_path=decision_path, global_vault=tmp_global)
```

- [ ] **Step 2: Run to verify fail** (currently passes without error — that IS the bug)

- [ ] **Step 3: Add type guard**

At top of `promote_to_global()`:

```python
    source = read_record(source_path)
    frontmatter = source["frontmatter"]
    record_type = frontmatter.get("type", "")

    if record_type not in {"lesson"}:
        raise ValueError(
            f"Only lessons can be promoted to global. Got type='{record_type}'."
        )
```

- [ ] **Step 4: Run tests**

Run: `uv run pytest tests/test_promotion.py -v`
Expected: All pass

- [ ] **Step 5: Commit**

```bash
git add src/codies_memory/promotion.py tests/test_promotion.py
git commit -m "fix: restrict promote_to_global() to lessons only (BUG-02)"
```

---

### Task 6: BUG-03 — Validate required files in `validate_vault()`

**Files:**
- Modify: `src/codies_memory/vault.py`
- Modify: `tests/test_vault.py`

- [ ] **Step 1: Write failing tests**

```python
def test_validate_global_missing_profile(tmp_path):
    vault = tmp_path / "vault"
    init_global_vault(vault)
    (vault / "profile.yaml").unlink()
    result = validate_vault(vault, vault_type="global")
    assert not result.is_valid
    assert "profile.yaml" in str(result.missing_files)


def test_validate_global_missing_registry(tmp_path):
    vault = tmp_path / "vault"
    init_global_vault(vault)
    (vault / "registry" / "projects.yaml").unlink()
    result = validate_vault(vault, vault_type="global")
    assert not result.is_valid
```

- [ ] **Step 2: Run to verify fail**

- [ ] **Step 3: Add `missing_files` to `VaultValidationResult` and file checks**

```python
@dataclass
class VaultValidationResult:
    is_valid: bool
    missing: list[str] = field(default_factory=list)
    missing_files: list[str] = field(default_factory=list)
    extra: list[str] = field(default_factory=list)

GLOBAL_REQUIRED_FILES = ["profile.yaml", "registry/projects.yaml", "identity/self.md"]
PROJECT_REQUIRED_FILES = ["profile.yaml"]

def validate_vault(root: Path, vault_type: str = "global") -> VaultValidationResult:
    expected = GLOBAL_DIRS if vault_type == "global" else PROJECT_DIRS
    required_files = GLOBAL_REQUIRED_FILES if vault_type == "global" else PROJECT_REQUIRED_FILES

    missing_dirs = [d for d in expected if not (root / d).is_dir()]
    missing_files = [f for f in required_files if not (root / f).is_file()]

    is_valid = len(missing_dirs) == 0 and len(missing_files) == 0
    return VaultValidationResult(
        is_valid=is_valid,
        missing=missing_dirs,
        missing_files=missing_files,
    )
```

- [ ] **Step 4: Run tests**

Run: `uv run pytest tests/test_vault.py -v`

- [ ] **Step 5: Commit**

```bash
git add src/codies_memory/vault.py tests/test_vault.py
git commit -m "fix: validate required files in validate_vault() (BUG-03)"
```

---

### Task 7: BUG-04 + BUG-05 + SKILL-01 — Schema enforcement and update validation

**Files:**
- Modify: `src/codies_memory/schemas.py`
- Modify: `src/codies_memory/records.py`
- Modify: `tests/test_schemas.py`
- Modify: `tests/test_records.py`

- [ ] **Step 1: Write failing tests**

```python
# test_schemas.py
def test_validate_rejects_invalid_status():
    data = {"id": "TH-0001", "title": "t", "type": "thread", "status": "bogus",
            "trust": "working", "scope": "project", "created": "2026-04-01", "updated": "2026-04-01"}
    errors = validate_frontmatter(data, "thread")
    assert any("status" in e.lower() for e in errors)


def test_validate_warns_unknown_extra_fields(capsys):
    data = {"id": "TH-0001", "title": "t", "type": "thread", "status": "active",
            "trust": "working", "scope": "project", "created": "2026-04-01",
            "updated": "2026-04-01", "totally_fake_field": "lol"}
    errors = validate_frontmatter(data, "thread")
    # Should not reject (soft enforcement) but may warn to stderr
    assert len(errors) == 0  # no hard errors


# test_records.py
def test_update_record_rejects_invalid_status(tmp_vault):
    path = create_record(vault=tmp_vault, record_type="thread", scope="project",
                         title="test", body="body")
    with pytest.raises(ValidationError):
        update_record(path, status="bogus-status")
```

- [ ] **Step 2: Run to verify fail**

- [ ] **Step 3: Implement**

In `schemas.py` — update `validate_frontmatter()`:

```python
def validate_frontmatter(data: dict[str, Any], record_type: str) -> list[str]:
    errors: list[str] = []

    for field in REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"Missing required field: '{field}'")

    if "trust" in data and data["trust"] not in TRUST_LEVELS:
        errors.append(f"Invalid trust level: '{data['trust']}'. Must be one of: {sorted(TRUST_LEVELS)}")

    if "scope" in data and data["scope"] not in SCOPES:
        errors.append(f"Invalid scope: '{data['scope']}'. Must be one of: {sorted(SCOPES)}")

    if "gate" in data and data["gate"] not in _VALID_GATES:
        errors.append(f"Invalid gate: '{data['gate']}'. Must be one of: {sorted(_VALID_GATES)}")

    # NEW: validate status
    if "status" in data and data["status"] not in STATUSES:
        errors.append(f"Invalid status: '{data['status']}'. Must be one of: {sorted(STATUSES)}")

    # NEW: soft-warn unknown extra fields (stderr, no error)
    if record_type in TYPE_EXTRA_FIELDS:
        known = REQUIRED_FIELDS | TYPE_EXTRA_FIELDS[record_type] | PROVENANCE_FIELDS | {"probation_until", "promoted_from", "supersedes", "superseded_by", "compacted_into"}
        for key in data:
            if key not in known:
                import sys
                print(f"Warning: unknown field '{key}' for type '{record_type}'", file=sys.stderr)

    return errors
```

Update `TYPE_EXTRA_FIELDS["session"]`:

```python
"session": {"review_after", "related", "tags", "gate", "mode", "next_step", "artifacts", "write_gate_summary"},
```

In `records.py` — update `update_record()`:

```python
def update_record(filepath: Path, **fields: Any) -> None:
    record = read_record(filepath)
    frontmatter = record["frontmatter"]
    body = record["body"]

    frontmatter.update(fields)
    frontmatter["updated"] = str(date.today())

    # NEW: revalidate before writing
    record_type = frontmatter.get("type", "")
    errors = validate_frontmatter(frontmatter, record_type)
    if errors:
        raise ValidationError(f"Invalid frontmatter after update: {errors}")

    _write_record(filepath, frontmatter, body)
```

- [ ] **Step 4: Run full test suite** (existing tests may need updating if they write invalid data)

Run: `uv run pytest -v`

- [ ] **Step 5: Commit**

```bash
git add src/codies_memory/schemas.py src/codies_memory/records.py tests/test_schemas.py tests/test_records.py
git commit -m "fix: enforce status validation, revalidate on update (BUG-04, BUG-05, SKILL-01)"
```

---

### Task 8: BUG-06 + BUG-07 + BUG-08 + BUG-09 + BUG-10 — Remaining medium/low fixes

**Files:**
- Modify: `src/codies_memory/promotion.py`
- Modify: `src/codies_memory/profile.py`
- Modify: `src/codies_memory/boot.py`
- Modify: `src/codies_memory/records.py`
- Modify: `tests/test_promotion.py`
- Modify: `tests/test_profile.py`
- Modify: `tests/test_boot.py`
- Modify: `tests/test_records.py`

- [ ] **Step 1: Write failing tests for all remaining bugs**

```python
# test_promotion.py
def test_elevate_trust_rejects_demotion(tmp_vault):
    path = create_record(vault=tmp_vault, record_type="thread", scope="project",
                         title="test", body="body", trust="confirmed")
    with pytest.raises(ValueError, match="Cannot demote"):
        elevate_trust(path, "working")


# test_profile.py
def test_profile_deepcopy_isolation(tmp_path):
    vault = tmp_path / "vault"
    vault.mkdir()
    (vault / "profile.yaml").write_text("boot_mode: operational\n")
    p1 = load_profile(vault)
    p1["promotion_overrides"]["test"] = True
    p2 = load_profile(vault)
    assert "test" not in p2.get("promotion_overrides", {})


# test_boot.py
def test_cache_key_with_path_inputs():
    from pathlib import Path
    key = build_cache_key(Path("/tmp/test"), Path("/tmp/project"), "main", "default", "operational", 4000)
    assert isinstance(key, str) and len(key) == 16


def test_cache_key_with_date_inputs():
    from datetime import date
    key = build_cache_key(date.today(), date.today(), "main", "default", "operational", 4000)
    assert isinstance(key, str) and len(key) == 16


# test_records.py
def test_slugify_empty_title():
    from codies_memory.records import _slugify
    assert _slugify("") == "untitled"
    assert _slugify("!!!") == "untitled"
    assert _slugify("   ") == "untitled"
```

- [ ] **Step 2: Run to verify they fail**

- [ ] **Step 3: Apply all fixes**

`promotion.py` — add demotion guard to `elevate_trust()`:

```python
    if new_idx < current_idx:
        raise ValueError(
            f"Cannot demote trust from '{current_trust}' to '{new_trust}' via elevate_trust(). "
            f"Use update_record() directly if demotion is intentional."
        )
```

`profile.py` — use deepcopy:

```python
import copy
# ...
profile = copy.deepcopy(DEFAULT_PROFILE)
```

`boot.py` — fix serialization:

```python
    payload = json.dumps(
        { ... },
        sort_keys=True,
        default=str,
    )
```

`records.py` — fix empty slugify:

```python
def _slugify(title: str) -> str:
    slug = title.lower()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    slug = slug.strip("-")
    slug = slug[:60]
    return slug if slug else "untitled"
```

- [ ] **Step 4: Run full test suite**

Run: `uv run pytest -v`
Expected: All pass

- [ ] **Step 5: Commit**

```bash
git add src/codies_memory/promotion.py src/codies_memory/profile.py src/codies_memory/boot.py src/codies_memory/records.py tests/
git commit -m "fix: demotion guard, deepcopy, cache key serialization, empty slug, path map (BUG-06-10)"
```

---

## Phase 3: CLI Rewrite + New Commands

### Task 9: Rework existing CLI commands for v2 paths

**Files:**
- Modify: `src/codies_memory/cli.py`
- Create: `tests/test_cli.py`

- [ ] **Step 1: Write CLI integration tests for reworked commands**

```python
import subprocess

def run_cli(*args, env=None):
    """Helper to run codies-memory CLI and return (returncode, stdout, stderr)."""
    result = subprocess.run(
        ["uv", "run", "codies-memory", *args],
        capture_output=True, text=True, env=env,
        cwd="/home/pyro/projects/agents/codies-memory",
    )
    return result.returncode, result.stdout, result.stderr


def test_cli_init_global(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path))
    rc, out, _ = run_cli("init", "--type", "global", "--agent", "testbot")
    assert rc == 0
    assert (tmp_path / ".memory" / "testbot" / "profile.yaml").exists()


def test_cli_init_project(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path))
    # First init global
    run_cli("init", "--type", "global", "--agent", "testbot")
    # Then init project
    project_dir = tmp_path / "my-project"
    project_dir.mkdir()
    rc, out, _ = run_cli("init", "--type", "project", "--agent", "testbot",
                         "--working-dir", str(project_dir))
    assert rc == 0
    assert (project_dir / ".codies-memory").exists()
```

- [ ] **Step 2: Run to verify fail**

- [ ] **Step 3: Rewrite `cli.py` with agent resolution**

Add `_resolve_agent()` helper:

```python
import os

def _resolve_agent(args: argparse.Namespace) -> str:
    """Resolve agent name from --agent flag or CODIES_MEMORY_AGENT env var."""
    agent = getattr(args, "agent", None) or os.environ.get("CODIES_MEMORY_AGENT")
    if not agent:
        print("Error: --agent flag or CODIES_MEMORY_AGENT env var required.", file=sys.stderr)
        sys.exit(1)
    return agent
```

Rewrite each `cmd_*` function to use `resolve_global_vault(agent)` and `resolve_project_vault()`.

Add `--agent` argument to all subparsers. Add `--working-dir` to init project.

- [ ] **Step 4: Run tests**

Run: `uv run pytest tests/test_cli.py -v`

- [ ] **Step 5: Commit**

```bash
git add src/codies_memory/cli.py tests/test_cli.py
git commit -m "feat: rework CLI for v2 agent-namespaced paths"
```

---

### Task 10: Add `capture` CLI subcommand

**Files:**
- Modify: `src/codies_memory/cli.py`
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Write failing test**

```python
def test_cli_capture(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path))
    run_cli("init", "--type", "global", "--agent", "testbot")
    project_dir = tmp_path / "my-project"
    project_dir.mkdir()
    run_cli("init", "--type", "project", "--agent", "testbot",
            "--working-dir", str(project_dir))

    rc, out, _ = run_cli("capture", "The API returns 404",
                         "--source", "testing", "--gate", "allow",
                         "--agent", "testbot", "--working-dir", str(project_dir))
    assert rc == 0
    assert "IN-" in out  # Should print the created record ID
```

- [ ] **Step 2: Run to verify fail**

- [ ] **Step 3: Implement `cmd_capture()`**

```python
def cmd_capture(args: argparse.Namespace) -> None:
    agent = _resolve_agent(args)
    global_vault = resolve_global_vault(agent)
    working_dir = Path(args.working_dir) if args.working_dir else Path.cwd()
    project_vault = resolve_project_vault(global_vault, working_dir)

    if project_vault is None:
        print("Error: No project vault found. Run 'codies-memory init --type project' first.", file=sys.stderr)
        sys.exit(1)

    gate = args.gate or get_write_gate_bias(load_profile(global_vault, project_vault))

    path = capture(vault=project_vault, content=args.content, source=args.source, gate=gate)
    record = read_record(path)
    print(f"Captured: {record['frontmatter']['id']} — {record['frontmatter']['title']}")
```

Add the subparser:

```python
capture_parser = subparsers.add_parser("capture", help="Capture an inbox observation.")
capture_parser.add_argument("content", help="The observation text.")
capture_parser.add_argument("--source", required=True, help="Source of the observation.")
capture_parser.add_argument("--gate", default=None, help="Write gate (allow/hold/discard).")
capture_parser.add_argument("--agent", default=None)
capture_parser.add_argument("--working-dir", default=None)
capture_parser.set_defaults(func=cmd_capture)
```

- [ ] **Step 4: Run tests**

- [ ] **Step 5: Commit**

```bash
git add src/codies_memory/cli.py tests/test_cli.py
git commit -m "feat: add 'capture' CLI subcommand"
```

---

### Task 11: Add `create` CLI subcommand

**Files:**
- Modify: `src/codies_memory/cli.py`
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Write failing test**

```python
def test_cli_create_lesson(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path))
    run_cli("init", "--type", "global", "--agent", "testbot")
    project_dir = tmp_path / "my-project"
    project_dir.mkdir()
    run_cli("init", "--type", "project", "--agent", "testbot",
            "--working-dir", str(project_dir))

    rc, out, _ = run_cli("create", "lesson",
                         "--title", "Check YAML tabs",
                         "--body", "YAML rejects tabs silently.",
                         "--agent", "testbot", "--working-dir", str(project_dir))
    assert rc == 0
    assert "LS-" in out
```

- [ ] **Step 2: Implement `cmd_create()`**

```python
def cmd_create(args: argparse.Namespace) -> None:
    agent = _resolve_agent(args)
    global_vault = resolve_global_vault(agent)

    if args.scope == "global":
        vault = global_vault
    else:
        working_dir = Path(args.working_dir) if args.working_dir else Path.cwd()
        vault = resolve_project_vault(global_vault, working_dir)
        if vault is None:
            print("Error: No project vault found.", file=sys.stderr)
            sys.exit(1)

    body = args.body
    if args.body_file:
        body = Path(args.body_file).read_text()

    extra = {}
    for field_str in (args.field or []):
        key, _, value = field_str.partition("=")
        extra[key] = value

    path = create_record(
        vault=vault, record_type=args.type, scope=args.scope,
        title=args.title, body=body, trust=args.trust, **extra,
    )
    record = read_record(path)
    print(f"Created: {record['frontmatter']['id']} — {record['frontmatter']['title']}")
```

- [ ] **Step 3: Run tests**

- [ ] **Step 4: Commit**

```bash
git add src/codies_memory/cli.py tests/test_cli.py
git commit -m "feat: add 'create' CLI subcommand"
```

---

### Task 12: Add `list` CLI subcommand

**Files:**
- Modify: `src/codies_memory/cli.py`
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Write failing test**

```python
def test_cli_list_inbox(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path))
    run_cli("init", "--type", "global", "--agent", "testbot")
    project_dir = tmp_path / "my-project"
    project_dir.mkdir()
    run_cli("init", "--type", "project", "--agent", "testbot",
            "--working-dir", str(project_dir))
    run_cli("capture", "Test item", "--source", "test", "--gate", "allow",
            "--agent", "testbot", "--working-dir", str(project_dir))

    rc, out, _ = run_cli("list", "inbox", "--agent", "testbot",
                         "--working-dir", str(project_dir))
    assert rc == 0
    assert "IN-" in out
```

- [ ] **Step 2: Implement `cmd_list()`**

```python
def cmd_list(args: argparse.Namespace) -> None:
    agent = _resolve_agent(args)
    global_vault = resolve_global_vault(agent)

    if args.scope == "global":
        vault = global_vault
    else:
        working_dir = Path(args.working_dir) if args.working_dir else Path.cwd()
        vault = resolve_project_vault(global_vault, working_dir)
        if vault is None:
            print("Error: No project vault found.", file=sys.stderr)
            sys.exit(1)

    filters = {}
    if args.status:
        filters["status"] = args.status
    if args.trust:
        filters["trust"] = args.trust

    records = list_records(vault, args.type, scope=args.scope, **filters)

    if args.format == "json":
        import json
        print(json.dumps([{"id": r["frontmatter"]["id"], "title": r["frontmatter"]["title"],
                           "status": r["frontmatter"].get("status"), "trust": r["frontmatter"].get("trust"),
                           "created": r["frontmatter"].get("created")} for r in records], indent=2))
    elif args.format == "paths":
        for r in records:
            print(r["path"])
    else:
        # Table format
        if not records:
            print("No records found.")
            return
        print(f"{'ID':<12} {'Title':<45} {'Status':<10} {'Trust':<12} {'Created'}")
        for r in records:
            fm = r["frontmatter"]
            print(f"{fm.get('id', ''):<12} {fm.get('title', '')[:44]:<45} {fm.get('status', ''):<10} {fm.get('trust', ''):<12} {fm.get('created', '')}")
```

- [ ] **Step 3: Run tests**

- [ ] **Step 4: Commit**

```bash
git add src/codies_memory/cli.py tests/test_cli.py
git commit -m "feat: add 'list' CLI subcommand with table/json/paths output"
```

---

### Task 13: Add `promote` CLI subcommand

**Files:**
- Modify: `src/codies_memory/cli.py`
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Write failing test**

```python
def test_cli_promote_to_thread(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path))
    run_cli("init", "--type", "global", "--agent", "testbot")
    project_dir = tmp_path / "my-project"
    project_dir.mkdir()
    run_cli("init", "--type", "project", "--agent", "testbot",
            "--working-dir", str(project_dir))
    run_cli("capture", "Recurring API issue", "--source", "test", "--gate", "allow",
            "--agent", "testbot", "--working-dir", str(project_dir))

    # Find the inbox item
    rc, out, _ = run_cli("list", "inbox", "--format", "paths",
                         "--agent", "testbot", "--working-dir", str(project_dir))
    inbox_path = out.strip()

    rc, out, _ = run_cli("promote", inbox_path, "--to", "thread",
                         "--agent", "testbot", "--working-dir", str(project_dir))
    assert rc == 0
    assert "TH-" in out
```

- [ ] **Step 2: Implement `cmd_promote()`**

```python
def cmd_promote(args: argparse.Namespace) -> None:
    agent = _resolve_agent(args)
    global_vault = resolve_global_vault(agent)
    source_path = Path(args.source)

    if args.to_global:
        new_path = promote_to_global(source_path=source_path, global_vault=global_vault)
    else:
        working_dir = Path(args.working_dir) if args.working_dir else Path.cwd()
        vault = resolve_project_vault(global_vault, working_dir)
        if vault is None:
            print("Error: No project vault found.", file=sys.stderr)
            sys.exit(1)
        new_path = promote_within_project(
            source_path=source_path, target_type=args.to, vault=vault,
        )

    record = read_record(new_path)
    print(f"Promoted: {record['frontmatter']['id']} — {record['frontmatter']['title']}")
```

- [ ] **Step 3: Run tests**

- [ ] **Step 4: Commit**

```bash
git add src/codies_memory/cli.py tests/test_cli.py
git commit -m "feat: add 'promote' CLI subcommand"
```

---

## Phase 4: Skills + Docs

### Task 14: Update all 4 skill files

**Files:**
- Modify: `skills/memory-boot.md`
- Modify: `skills/memory-capture.md`
- Modify: `skills/memory-close-session.md`
- Modify: `skills/memory-promote.md`

- [ ] **Step 1: Fix `memory-close-session.md`**

Replace `$(date +%Y-%m-%d)` with `from datetime import date` + `f'Session Summary - {date.today()}'`.

Replace `mode='implement'` and `next_step=` with valid fields (these are now in the schema after SKILL-01).

Update all `uv run python -c` examples to use CLI commands instead:
```bash
codies-memory create session --title "Session Summary - 2026-04-01" --body "..." --field mode=implement --field next_step="..."
codies-memory status
```

Update "Session Summary Fields" section to match `TYPE_EXTRA_FIELDS["session"]`.

- [ ] **Step 2: Fix `memory-promote.md`**

Change `decision -> committed docs (canonical trust)` to `decision -> lesson (reusable pattern)`.

Remove `project thread -> global thread` from "Project to Global" — only lessons cross this boundary.

Replace inline Python examples with CLI:
```bash
codies-memory list inbox --status active
codies-memory promote /path/to/record.md --to thread
codies-memory promote /path/to/lesson.md --to-global
```

- [ ] **Step 3: Fix `memory-boot.md`**

Remove line 19 (false inbox aging claim).

Update path examples — remove `--global-vault ~/.memory` and `--project-vault .memory`, replace with:
```bash
codies-memory boot --budget 4000
```

Add after boot: `codies-memory status` to check inbox.

- [ ] **Step 4: Fix `memory-capture.md`**

Replace inline Python examples with CLI:
```bash
codies-memory capture "The API returns 404" --source "session observation" --gate allow
```

Add `open` and `closed` to write gate documentation.

- [ ] **Step 5: Update all skill paths for v2**

All references to `~/.memory` become `~/.memory/<agent>/` (or just note that `CODIES_MEMORY_AGENT` env var handles it). All references to `<project>/.memory` become "auto-resolved from cwd".

- [ ] **Step 6: Commit**

```bash
git add skills/
git commit -m "fix: update all skills for v2 paths and CLI commands (SKILL-01 through SKILL-06)"
```

---

### Task 15: Update INSTALL.md, README.md, version bump

**Files:**
- Modify: `INSTALL.md`
- Modify: `README.md`
- Modify: `pyproject.toml`

- [ ] **Step 1: Update INSTALL.md for v2**

Rewrite installation steps:
- Clone + `uv sync` (unchanged)
- `codies-memory init --type global --agent <name>` (new)
- Edit identity files at `~/.memory/<agent>/identity/`
- `codies-memory init --type project --agent <name>` from project dir (new)
- Skill installation (unchanged, still symlinks)
- Verification with `codies-memory boot` and `codies-memory status`

- [ ] **Step 2: Fix README.md broken relative links**

Lines 45-51 reference `./01-principles.md` etc. — update to `docs/original/01-principles.md`.

- [ ] **Step 3: Bump version**

In `pyproject.toml`: `version = "1.0.0"`

- [ ] **Step 4: Commit**

```bash
git add INSTALL.md README.md pyproject.toml
git commit -m "docs: update INSTALL.md and README for v2, bump to 1.0.0"
```

---

### Task 16: Final integration test + cleanup

- [ ] **Step 1: Run full test suite**

```bash
uv run pytest -v --tb=short
```

Expected: All tests pass (should be 140+ after new tests).

- [ ] **Step 2: Run smoke test if it exists**

```bash
bash scripts/smoke-test.sh
```

- [ ] **Step 3: Manual end-to-end verification**

```bash
# Clean slate
rm -rf /tmp/test-v2-memory

# Init global for two agents
CODIES_MEMORY_AGENT=alice codies-memory init --type global --agent alice
CODIES_MEMORY_AGENT=bob codies-memory init --type global --agent bob

# Verify isolation
ls ~/.memory/alice/identity/
ls ~/.memory/bob/identity/

# Init project for alice
mkdir -p /tmp/test-v2-project && cd /tmp/test-v2-project
codies-memory init --type project --agent alice
cat .codies-memory  # should show slug

# Capture, list, promote
codies-memory capture "Test observation" --source "manual" --gate allow --agent alice
codies-memory list inbox --agent alice
codies-memory status --agent alice

# Boot
codies-memory boot --agent alice

# Cleanup
rm -rf /tmp/test-v2-project ~/.memory/alice ~/.memory/bob
```

- [ ] **Step 4: Commit any remaining fixes**

- [ ] **Step 5: Tag release**

```bash
git tag v1.0.0
git push && git push --tags
```
