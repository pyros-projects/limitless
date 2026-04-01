"""Boot assembly: layered context packets with budgets, truncation, and caching."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


# ---------------------------------------------------------------------------
# Token estimation
# ---------------------------------------------------------------------------

def estimate_tokens(text: str) -> int:
    """Estimate token count for *text*.

    Returns 0 for empty strings, otherwise ``int(len(text.split()) * 1.3)``.
    """
    if not text:
        return 0
    return int(len(text.split()) * 1.3)


# ---------------------------------------------------------------------------
# Layer budgets
# ---------------------------------------------------------------------------

def compute_layer_budgets(total: int = 4000) -> dict:
    """Return token budgets for the five memory layers.

    Proportions:
      - global_identity    25%   (1000 of 4000)
      - global_procedural  12.5% (500  of 4000)
      - project_context    37.5% (1500 of 4000)
      - project_working    12.5% (500  of 4000)
      - branch_session     12.5% (500  of 4000)
    """
    return {
        "global_identity": int(total * 0.25),
        "global_procedural": int(total * 0.125),
        "project_context": int(total * 0.375),
        "project_working": int(total * 0.125),
        "branch_session": int(total * 0.125),
    }


# ---------------------------------------------------------------------------
# Truncation
# ---------------------------------------------------------------------------

def truncate_to_budget(content: str, budget: int) -> str:
    """Return *content* truncated so that ``estimate_tokens`` fits within *budget*.

    If the content already fits, it is returned unchanged.
    Otherwise the first N words are kept where ``N = int(budget / 1.3)``,
    and ``"\\n\\n[truncated]"`` is appended.
    """
    if estimate_tokens(content) <= budget:
        return content

    max_words = int(budget / 1.3)
    words = content.split()
    truncated = " ".join(words[:max_words])
    return truncated + "\n\n[truncated]"


# ---------------------------------------------------------------------------
# Internal helper: read layer files
# ---------------------------------------------------------------------------

def _read_layer_files(vault: Path, subdirs: list[str]) -> str:
    """Read all ``*.md`` files from *subdirs* under *vault* and join them.

    Files are joined with ``"\\n\\n---\\n\\n"`` as a separator.  Missing
    directories are silently skipped.
    """
    parts: list[str] = []
    for subdir in subdirs:
        target = vault / subdir
        if not target.is_dir():
            continue
        for md_file in sorted(target.glob("*.md")):
            text = md_file.read_text(encoding="utf-8").strip()
            if text:
                parts.append(text)
    return "\n\n---\n\n".join(parts)


# ---------------------------------------------------------------------------
# Assemble boot packet
# ---------------------------------------------------------------------------

def assemble_boot(
    global_vault: Path,
    project_vault: Path | None = None,
    branch: str = "main",
    budget: int = 4000,
) -> dict:
    """Assemble the five-layer boot packet from *global_vault* and *project_vault*.

    Returns a dict with two keys:

    - ``"global_packet"`` — layers 1 + 2 joined with ``"\\n\\n---\\n\\n"``
    - ``"project_packet"`` — layers 3 + 4 + 5 joined (empty string if no project vault)

    Each layer is independently truncated to its budget before joining.
    """
    budgets = compute_layer_budgets(budget)

    # Layer 1: global identity
    layer1_raw = _read_layer_files(global_vault, ["identity"])
    layer1 = truncate_to_budget(layer1_raw, budgets["global_identity"])

    # Layer 2: global procedural (lessons + skills)
    layer2_raw = _read_layer_files(global_vault, ["procedural/lessons", "procedural/skills"])
    layer2 = truncate_to_budget(layer2_raw, budgets["global_procedural"])

    separator = "\n\n---\n\n"
    global_layers = [l for l in [layer1, layer2] if l]

    # Global-only boot: no project context
    if project_vault is None:
        return {
            "global_packet": separator.join(global_layers),
            "project_packet": "",
        }

    # Layer 3: project context (project/ files)
    layer3_raw = _read_layer_files(project_vault, ["project"])
    layer3 = truncate_to_budget(layer3_raw, budgets["project_context"])

    # Layer 4: project working memory (threads + decisions)
    layer4_raw = _read_layer_files(project_vault, ["threads", "decisions"])
    layer4 = truncate_to_budget(layer4_raw, budgets["project_working"])

    # Layer 5: branch overlay + most recent session
    branch_overlay_dir = project_vault / "project" / "branch-overlays"
    overlay_parts: list[str] = []
    if branch_overlay_dir.is_dir():
        for md_file in sorted(branch_overlay_dir.glob(f"{branch}*.md")):
            text = md_file.read_text(encoding="utf-8").strip()
            if text:
                overlay_parts.append(text)

    sessions_dir = project_vault / "sessions"
    if sessions_dir.is_dir():
        session_files = sorted(sessions_dir.rglob("*.md"))
        if session_files:
            latest_session = session_files[-1].read_text(encoding="utf-8").strip()
            if latest_session:
                overlay_parts.append(latest_session)

    layer5_raw = "\n\n---\n\n".join(overlay_parts)
    layer5 = truncate_to_budget(layer5_raw, budgets["branch_session"])

    project_layers = [l for l in [layer3, layer4, layer5] if l]

    return {
        "global_packet": separator.join(global_layers),
        "project_packet": separator.join(project_layers),
    }


# ---------------------------------------------------------------------------
# Cache key
# ---------------------------------------------------------------------------

def build_cache_key(
    global_inputs: object,
    project_inputs: object,
    branch: str,
    profile_name: str,
    boot_mode: str,
    budget: int,
) -> str:
    """Return a 16-character hex cache key derived from all inputs.

    All inputs are serialised with ``json.dumps(sort_keys=True)`` then hashed
    with SHA-256.  The first 16 hex characters of the digest are returned.
    """
    payload = json.dumps(
        {
            "global_inputs": global_inputs,
            "project_inputs": project_inputs,
            "branch": branch,
            "profile_name": profile_name,
            "boot_mode": boot_mode,
            "budget": budget,
        },
        sort_keys=True,
        default=str,
    )
    digest = hashlib.sha256(payload.encode()).hexdigest()
    return digest[:16]


# ---------------------------------------------------------------------------
# Cache I/O
# ---------------------------------------------------------------------------

def cache_boot_packet(
    boot_dir: Path,
    key: str,
    packet: str,
    manifest: dict,
) -> None:
    """Write *packet* and *manifest* to *boot_dir* under *key*.

    Creates:
      - ``{key}.md``             — the serialised packet text
      - ``{key}.manifest.json``  — the manifest dict as JSON
    """
    boot_dir.mkdir(parents=True, exist_ok=True)
    (boot_dir / f"{key}.md").write_text(packet, encoding="utf-8")
    (boot_dir / f"{key}.manifest.json").write_text(
        json.dumps(manifest, sort_keys=True, indent=2), encoding="utf-8"
    )


def is_cache_valid(boot_dir: Path, key: str, manifest: dict) -> bool:
    """Return True if the cached manifest for *key* matches *manifest*.

    Returns False if the manifest file does not exist or the stored manifest
    differs from the provided one.
    """
    manifest_path = boot_dir / f"{key}.manifest.json"
    if not manifest_path.exists():
        return False
    stored = json.loads(manifest_path.read_text(encoding="utf-8"))
    return stored == manifest
