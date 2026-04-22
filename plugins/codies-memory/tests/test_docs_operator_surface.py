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
