"""Tests for derived warm-memory artifacts."""

from __future__ import annotations

from pathlib import Path

from codies_memory.warm import (
    build_global_summary,
    build_project_summary,
    build_recent_episodes,
    write_warm_artifacts,
)


class TestBuildGlobalSummary:
    def test_includes_identity_and_lessons(self, tmp_global_vault: Path) -> None:
        (tmp_global_vault / "identity" / "self.md").write_text(
            "---\ntitle: self\ntype: identity\n---\nCodie remembers durable patterns."
        )
        lesson = tmp_global_vault / "procedural" / "lessons" / "LS-G0001-test.md"
        lesson.write_text(
            "---\nid: LS-G0001\ntitle: Check retrieval freshness\ntype: lesson\nstatus: active\ntrust: working\nscope: global\ncreated: '2026-04-22'\nupdated: '2026-04-22'\napplies_to: qmd\n---\n\nAlways inspect timestamps before trusting a miss.\n"
        )

        summary = build_global_summary(tmp_global_vault)

        assert "# Global Summary" in summary
        assert "Codie remembers durable patterns." in summary
        assert "Check retrieval freshness" in summary


class TestBuildProjectSummary:
    def test_stays_project_scoped(self, tmp_project_vault: Path) -> None:
        (tmp_project_vault / "project" / "overview.md").write_text(
            "---\nid: PJ-0001\ntitle: Overview\ntype: project\nstatus: active\ntrust: working\nscope: project\ncreated: '2026-04-22'\nupdated: '2026-04-22'\n---\n\nThis project owns warm summaries.\n"
        )
        (tmp_project_vault / "decisions" / "DC-0001-choice.md").write_text(
            "---\nid: DC-0001\ntitle: Use markdown summaries\ntype: decision\nstatus: active\ntrust: working\nscope: project\ncreated: '2026-04-22'\nupdated: '2026-04-22'\nrationale: Inspectable and diffable\n---\n\nDecision body.\n"
        )

        summary = build_project_summary(tmp_project_vault)

        assert "# Project Summary" in summary
        assert "This project owns warm summaries." in summary
        assert "Use markdown summaries" in summary
        assert "Global Summary" not in summary


class TestBuildRecentEpisodes:
    def test_is_bounded_to_latest_three_sessions(self, tmp_project_vault: Path) -> None:
        for idx in range(5):
            session = tmp_project_vault / "sessions" / f"SS-2026042{idx}-session-{idx}.md"
            session.write_text(
                f"---\nid: SS-2026042{idx}\ntitle: Session {idx}\ntype: session\nstatus: active\ntrust: working\nscope: project\ncreated: '2026-04-2{idx}'\nupdated: '2026-04-2{idx}'\nnext_step: Next {idx}\n---\n\nEpisode {idx} body.\n"
            )

        summary = build_recent_episodes(tmp_project_vault)

        assert "Session 4" in summary
        assert "Session 3" in summary
        assert "Session 2" in summary
        assert "Session 1" not in summary
        assert "Session 0" not in summary


class TestWriteWarmArtifacts:
    def test_writes_expected_files(self, tmp_global_vault: Path, tmp_project_vault: Path) -> None:
        written = write_warm_artifacts(tmp_global_vault, tmp_project_vault)

        assert "global_summary" in written
        assert "project_summary" in written
        assert "recent_episodes" in written
        assert written["global_summary"].is_file()
        assert written["project_summary"].is_file()
        assert written["recent_episodes"].is_file()
