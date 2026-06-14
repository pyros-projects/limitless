from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_install_mentions_update_path_for_existing_clone() -> None:
    install = (REPO_ROOT / "INSTALL.md").read_text(encoding="utf-8")

    assert "git pull" in install
    assert "codies-memory -h" in install
    assert "which codies-memory" in install
    assert "standalone mode" in install.lower()
    assert "full mode" in install.lower()
    assert "qmd" in install.lower()
    assert "qmd status" in install.lower()
    assert "timestamps" in install.lower() or "last updated" in install.lower()
    assert "recommended" in install.lower()
    assert "token-efficient" in install.lower() or "token efficient" in install.lower()
    assert "offer to help install qmd" in install.lower() or "help install qmd" in install.lower()


def test_close_session_skill_uses_v2_resolution_examples() -> None:
    skill = (REPO_ROOT / "skills" / "memory-close-session" / "SKILL.md").read_text(encoding="utf-8")

    assert "$(date" not in skill
    assert "Path('.memory')" not in skill
    assert "resolve_global_vault" in skill or "resolve_project_vault" in skill


def test_boot_and_help_skills_explain_qmd_recall_workflow() -> None:
    boot_skill = (REPO_ROOT / "skills" / "memory-boot" / "SKILL.md").read_text(encoding="utf-8")
    help_skill = (REPO_ROOT / "skills" / "memory-help" / "SKILL.md").read_text(encoding="utf-8")

    assert "qmd status" in boot_skill.lower()
    assert "qmd query" in boot_skill.lower()
    assert "qmd get" in help_skill.lower()
    assert "timestamps" in boot_skill.lower() or "last updated" in boot_skill.lower()
    assert "not found in the current index" in help_skill.lower()
    assert "hyphenated" in help_skill.lower()
    assert "ace step" in help_skill.lower() or "codies memory" in help_skill.lower()
    assert "works without qmd" in boot_skill.lower()
    assert "offer to help install qmd" in boot_skill.lower() or "help install qmd" in help_skill.lower()


def test_smoke_script_covers_general_and_project_flows() -> None:
    smoke = REPO_ROOT / "scripts" / "smoke.sh"
    checklist = (REPO_ROOT / "docs" / "TESTING-CHECKLIST.md").read_text(encoding="utf-8")

    assert smoke.is_file()
    assert smoke.stat().st_mode & 0o111
    assert "scripts/smoke.sh" in checklist
    assert "temporary HOME" in checklist

    text = smoke.read_text(encoding="utf-8")
    required_markers = [
        "mktemp -d",
        "HOME=",
        "init --type global",
        "init --type project",
        "validate --type global",
        "validate --type project",
        "capture",
        "create lesson",
        "create decision",
        "create session",
        "create reflection",
        "list inbox",
        "list lessons",
        "list sessions",
        "list daily-log --scope global",
        "status",
        "promote",
        "--to-global",
        "refresh",
        "boot",
        "--general",
        "user",
        "feedback",
    ]
    missing = [marker for marker in required_markers if marker not in text]
    assert missing == []


def test_agent_smoke_recipe_is_documented() -> None:
    recipe = REPO_ROOT / "docs" / "agent-smoke.md"
    checklist = (REPO_ROOT / "docs" / "TESTING-CHECKLIST.md").read_text(encoding="utf-8")

    assert recipe.is_file()
    assert "agent-smoke.md" in checklist

    text = recipe.read_text(encoding="utf-8")
    required_markers = [
        "fresh subagent",
        "temporary HOME",
        "wrapper",
        "memory-boot/SKILL.md",
        "memory-help/SKILL.md",
        "memory-capture/SKILL.md",
        "memory-close-session/SKILL.md",
        "Y/N scorecard",
        "did not touch real ~/.memory",
        "normal vault-less reads",
        "--general",
        "raw working data",
    ]
    missing = [marker for marker in required_markers if marker not in text]
    assert missing == []
