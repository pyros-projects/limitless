from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_install_mentions_update_path_for_existing_clone() -> None:
    install = (REPO_ROOT / "INSTALL.md").read_text(encoding="utf-8")

    assert "git pull" in install
    assert "codies-memory -h" in install
    assert "which codies-memory" in install


def test_close_session_skill_uses_v2_resolution_examples() -> None:
    skill = (REPO_ROOT / "skills" / "memory-close-session" / "SKILL.md").read_text(encoding="utf-8")

    assert "$(date" not in skill
    assert "Path('.memory')" not in skill
    assert "resolve_global_vault" in skill or "resolve_project_vault" in skill
