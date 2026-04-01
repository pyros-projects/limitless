"""Vault structure, validation, registry, and path resolution for codies-memory."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml


# ---------------------------------------------------------------------------
# Constants — directory layouts
# ---------------------------------------------------------------------------

GLOBAL_DIRS: list[str] = [
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
    "feedback",
]

PROJECT_DIRS: list[str] = [
    "project/branch-overlays",
    "threads",
    "decisions",
    "lessons",
    "sessions",
    "inbox",
    "boot",
]

GLOBAL_REQUIRED_FILES: list[str] = [
    "profile.yaml",
    "registry/projects.yaml",
    "identity/self.md",
]

PROJECT_REQUIRED_FILES: list[str] = [
    "profile.yaml",
]

# ---------------------------------------------------------------------------
# Path map: (record_type, scope) -> subdirectory name (relative to vault root)
# ---------------------------------------------------------------------------

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
    ("identity", "global"): "identity",
}


# ---------------------------------------------------------------------------
# Dataclass
# ---------------------------------------------------------------------------

@dataclass
class VaultValidationResult:
    is_valid: bool
    missing: list[str] = field(default_factory=list)
    missing_files: list[str] = field(default_factory=list)
    extra: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _write_if_missing(path: Path, content: str) -> None:
    """Write *content* to *path* only if the file does not already exist."""
    if not path.exists():
        path.write_text(content)


def _read_registry(global_vault: Path) -> dict:
    registry_path = global_vault / "registry" / "projects.yaml"
    data = yaml.safe_load(registry_path.read_text()) or {}
    if "projects" not in data:
        data["projects"] = []
    return data


def _write_registry(global_vault: Path, data: dict) -> None:
    registry_path = global_vault / "registry" / "projects.yaml"
    registry_path.write_text(yaml.dump(data, default_flow_style=False, allow_unicode=True))


def _update_registry_working_dir(global_vault: Path, slug: str, working_dir: str) -> None:
    """Lazily update the working_dir for a project in the registry."""
    data = _read_registry(global_vault)
    for entry in data.get("projects", []):
        if entry.get("slug") == slug and entry.get("working_dir") != working_dir:
            entry["working_dir"] = working_dir
            _write_registry(global_vault, data)
            break


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def resolve_global_vault(agent: str) -> Path:
    """Return the global vault path for *agent*: ``~/.memory/<agent>``."""
    return Path.home() / ".memory" / agent


def resolve_project_vault(global_vault: Path, working_dir: Path) -> Path | None:
    """Resolve a working directory to its project vault path.

    Uses a three-tier lookup:

    1. **Marker file** — read ``.codies-memory`` in *working_dir* for the slug.
    2. **Registry working_dir** — match *working_dir* against registry entries.
    3. **Git remote URL** — match git remote against registry entries.

    Returns the project vault path, or ``None`` if no match is found.
    """
    # --- Tier 1: marker file ---
    marker = working_dir / ".codies-memory"
    if marker.is_file():
        slug = marker.read_text().strip()
        if slug:
            vault_path = global_vault / "projects" / slug
            if vault_path.is_dir():
                _update_registry_working_dir(global_vault, slug, str(working_dir))
                return vault_path

    # --- Tier 2: registry working_dir ---
    data = _read_registry(global_vault)
    working_dir_str = str(working_dir)
    for entry in data.get("projects", []):
        if entry.get("working_dir") == working_dir_str:
            slug = entry["slug"]
            vault_path = global_vault / "projects" / slug
            if vault_path.is_dir():
                return vault_path

    # --- Tier 3: git remote URL ---
    git_remote = _get_git_remote(working_dir)
    if git_remote:
        for entry in data.get("projects", []):
            if entry.get("git_remote") == git_remote:
                slug = entry["slug"]
                vault_path = global_vault / "projects" / slug
                if vault_path.is_dir():
                    _update_registry_working_dir(global_vault, slug, working_dir_str)
                    return vault_path

    return None


def init_global_vault(root: Path) -> Path:
    """Create the global vault directory structure at *root*.

    Idempotent — existing files are never overwritten.

    Returns *root*.
    """
    for d in GLOBAL_DIRS:
        (root / d).mkdir(parents=True, exist_ok=True)

    # profile.yaml
    _write_if_missing(
        root / "profile.yaml",
        "boot_mode: operational\nwrite_gate_bias: hold\n",
    )

    # registry/projects.yaml
    _write_if_missing(root / "registry" / "projects.yaml", "projects: []\n")

    # identity seed files
    for name in ("self.md", "user.md", "rules.md"):
        _write_if_missing(
            root / "identity" / name,
            f"---\ntitle: {name[:-3]}\ntype: identity\n---\n",
        )

    return root


def init_project_vault(
    global_vault: Path,
    slug: str | None = None,
    working_dir: Path | None = None,
    register: bool = True,
) -> Path:
    """Create project vault under ``global_vault/projects/slug/``.

    Creates a marker file (``.codies-memory``) in *working_dir* and
    registers the project in the global registry.

    *slug* defaults to ``working_dir.name`` if not provided.
    *working_dir* defaults to ``Path.cwd()`` if not provided.

    Returns the project vault root (``global_vault / "projects" / slug``).
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


def _get_git_remote(working_dir: Path) -> str | None:
    """Try to get git remote URL from *working_dir*. Returns None on failure."""
    import subprocess

    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=working_dir,
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode != 0:
            return None
        url = result.stdout.strip()
        return url if url else None
    except Exception:
        return None


def register_project_vault(
    global_vault: Path,
    slug: str,
    working_dir: str,
    metadata: dict,
    status: str = "active",
    git_remote: str | None = None,
) -> None:
    """Add or update a project entry in the global registry.

    Entries are keyed by *slug* — no duplicates are created.
    """
    data = _read_registry(global_vault)
    projects: list[dict] = data["projects"]

    # Find existing entry by slug
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


def validate_vault(root: Path, vault_type: str = "global") -> VaultValidationResult:
    """Check that all expected subdirectories and required files are present under *root*.

    Returns a :class:`VaultValidationResult`.
    """
    expected: list[str] = GLOBAL_DIRS if vault_type == "global" else PROJECT_DIRS
    required_files: list[str] = GLOBAL_REQUIRED_FILES if vault_type == "global" else PROJECT_REQUIRED_FILES

    missing_dirs: list[str] = [d for d in expected if not (root / d).is_dir()]
    missing_files: list[str] = [f for f in required_files if not (root / f).is_file()]

    is_valid = len(missing_dirs) == 0 and len(missing_files) == 0
    return VaultValidationResult(is_valid=is_valid, missing=missing_dirs, missing_files=missing_files)


def resolve_path(vault_root: Path, record_type: str, scope: str) -> Path:
    """Return the absolute path for *record_type* + *scope* under *vault_root*.

    Raises :class:`ValueError` for unknown (record_type, scope) combinations.
    """
    key = (record_type, scope)
    if key not in _PATH_MAP:
        raise ValueError(
            f"Unknown record type/scope combination: {record_type!r}/{scope!r}. "
            f"Valid combinations: {sorted(_PATH_MAP.keys())}"
        )
    return vault_root / _PATH_MAP[key]


def find_vaults(global_vault: Path, include_archived: bool = False) -> list[dict]:
    """Return project entries from the global registry.

    Each returned dict includes a computed ``vault_path`` pointing to
    ``global_vault / "projects" / slug``.

    By default archived projects are excluded; pass *include_archived=True*
    to include them.
    """
    data = _read_registry(global_vault)
    projects: list[dict] = data.get("projects", [])
    if not include_archived:
        projects = [p for p in projects if p.get("status") != "archived"]

    results: list[dict] = []
    for p in projects:
        entry = dict(p)
        entry["vault_path"] = str(global_vault / "projects" / entry["slug"])
        results.append(entry)
    return results
