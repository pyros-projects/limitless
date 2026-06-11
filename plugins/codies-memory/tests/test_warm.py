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
        assert "Generated:" in summary
        assert "Codie remembers durable patterns." in summary
        assert "Check retrieval freshness" in summary


    def test_identity_excerpt_skips_markdown_headings(self, tmp_global_vault: Path) -> None:
        (tmp_global_vault / "identity" / "self.md").write_text(
            "---\ntitle: self\ntype: identity\n---\n\n## Who I Am\nCodie remembers durable patterns."
        )

        summary = build_global_summary(tmp_global_vault)

        assert "Codie remembers durable patterns." in summary
        assert "## Who I Am" not in summary

    def test_includes_most_recent_active_global_threads(self, tmp_global_vault: Path) -> None:
        for idx in range(6):
            thread = tmp_global_vault / "threads" / f"TH-G000{idx + 1}-topic-{idx}.md"
            thread.write_text(
                f"---\nid: TH-G000{idx + 1}\ntitle: Global thread {idx}\ntype: thread\nstatus: active\ntrust: working\nscope: global\ncreated: '2026-06-0{idx + 1}'\nupdated: '2026-06-0{idx + 1}'\n---\n\nThread {idx} body.\n"
            )
        archived = tmp_global_vault / "threads" / "TH-G0099-old.md"
        archived.write_text(
            "---\nid: TH-G0099\ntitle: Archived global thread\ntype: thread\nstatus: archived\ntrust: working\nscope: global\ncreated: '2026-06-09'\nupdated: '2026-06-09'\n---\n\nDone.\n"
        )

        summary = build_global_summary(tmp_global_vault)

        assert "## Global Threads" in summary
        # The five most recent active threads survive; the oldest is dropped.
        for idx in range(1, 6):
            assert f"Global thread {idx}" in summary
        assert "Global thread 0" not in summary
        assert "Archived global thread" not in summary
        assert summary.index("Global thread 5") < summary.index("Global thread 1")

    def test_includes_recent_reflections(self, tmp_global_vault: Path) -> None:
        for idx in range(4):
            reflection = tmp_global_vault / "reflections" / f"RF-000{idx + 1}-thought-{idx}.md"
            reflection.write_text(
                f"---\nid: RF-000{idx + 1}\ntitle: Reflection {idx}\ntype: reflection\nstatus: active\ntrust: working\nscope: global\ncreated: '2026-05-0{idx + 1}'\nupdated: '2026-05-0{idx + 1}'\n---\n\nReflection {idx} body.\n"
            )

        summary = build_global_summary(tmp_global_vault)

        assert "## Recent Reflections" in summary
        # The three most recent reflections survive; the oldest is dropped.
        for idx in range(1, 4):
            assert f"Reflection {idx}" in summary
        assert "Reflection 0" not in summary
        assert summary.index("Reflection 3") < summary.index("Reflection 1")

    def test_includes_active_global_decisions(self, tmp_global_vault: Path) -> None:
        decision = tmp_global_vault / "decisions" / "DC-G0001-choice.md"
        decision.write_text(
            "---\nid: DC-G0001\ntitle: Always sign commits per-repo\ntype: decision\nstatus: active\ntrust: working\nscope: global\ncreated: '2026-06-01'\nupdated: '2026-06-01'\nrationale: Identity separation\n---\n\nDecision body.\n"
        )

        summary = build_global_summary(tmp_global_vault)

        assert "## Global Decisions" in summary
        assert "Always sign commits per-repo" in summary
        assert "Identity separation" in summary


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
        assert "Generated:" in summary
        assert "This project owns warm summaries." in summary
        assert "Use markdown summaries" in summary
        assert "[2026-04-22]" in summary
        assert "Global Summary" not in summary


class TestBuildRecentEpisodes:
    def test_is_bounded_to_latest_five_sessions(self, tmp_project_vault: Path) -> None:
        for idx in range(7):
            session = tmp_project_vault / "sessions" / f"SS-2026042{idx}-session-{idx}.md"
            session.write_text(
                f"---\nid: SS-2026042{idx}\ntitle: Session {idx}\ntype: session\nstatus: active\ntrust: working\nscope: project\ncreated: '2026-04-2{idx}'\nupdated: '2026-04-2{idx}'\nnext_step: Next {idx}\n---\n\nEpisode {idx} body.\n"
            )

        summary = build_recent_episodes(tmp_project_vault)

        assert "Generated:" in summary
        assert "max 400 chars" in summary
        assert "Session 6" in summary
        assert "Session 5" in summary
        assert "Session 4" in summary
        assert "Session 3" in summary
        assert "Session 2" in summary
        assert "Session 0" not in summary
        assert "Session 1" not in summary

    def test_episode_excerpt_skips_markdown_headings(self, tmp_project_vault: Path) -> None:
        session = tmp_project_vault / "sessions" / "SS-20260611-headed.md"
        session.write_text(
            "---\nid: SS-20260611\ntitle: Headed Session\ntype: session\nstatus: active\ntrust: working\nscope: project\ncreated: '2026-06-11'\nupdated: '2026-06-11'\nnext_step: Keep going\n---\n\n"
            "## What Happened\n- Fixed the parser bug in warm excerpts.\n\n## Decisions Made\n- Ship it.\n"
        )

        summary = build_recent_episodes(tmp_project_vault)

        assert "Fixed the parser bug in warm excerpts." in summary
        assert "## What Happened" not in summary

    def test_recent_episode_excerpt_is_truncated(self, tmp_project_vault: Path) -> None:
        session = tmp_project_vault / "sessions" / "SS-20260424-long.md"
        session.write_text(
            "---\nid: SS-20260424\ntitle: Long Session\ntype: session\nstatus: active\ntrust: working\nscope: project\ncreated: '2026-04-24'\nupdated: '2026-04-24'\nnext_step: Keep going\n---\n\n"
            + ("word " * 200)
            + "\n"
        )

        summary = build_recent_episodes(tmp_project_vault)

        assert "Long Session" in summary
        assert "..." in summary


class TestWriteWarmArtifacts:
    def test_writes_expected_files(self, tmp_global_vault: Path, tmp_project_vault: Path) -> None:
        written = write_warm_artifacts(tmp_global_vault, tmp_project_vault)

        assert "global_summary" in written
        assert "project_summary" in written
        assert "recent_episodes" in written
        assert written["global_summary"].is_file()
        assert written["project_summary"].is_file()
        assert written["recent_episodes"].is_file()
