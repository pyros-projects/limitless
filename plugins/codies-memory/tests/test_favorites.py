"""Tests for favorite reflections and dreams: the pick, when it is due, and boot showing it in full."""

from __future__ import annotations

import argparse
from pathlib import Path

import pytest

from codies_memory import favorites
from codies_memory.boot import assemble_boot
from codies_memory.cli import cmd_boot, cmd_create, cmd_favorites, cmd_init
from codies_memory.records import create_record, update_record


def _record(vault: Path, kind: str, title: str, body: str, created: str = "2026-10-22") -> str:
    path = create_record(vault, kind, "global", title=title, body=body)
    update_record(path, created=created)
    return path.name.split("-on-")[0] if "-on-" in path.name else "-".join(path.name.split("-")[:2])


def _ids(vault: Path, kind: str, count: int) -> list[str]:
    return [_record(vault, kind, f"On Thing {n}", f"{kind} body {n}", created=f"2026-10-{10 + n:02d}")
            for n in range(count)]


class TestSaveFavorites:
    def test_saves_three_picks_with_reasons(self, tmp_global_vault: Path) -> None:
        ids = _ids(tmp_global_vault, "reflection", 4)

        path = favorites.save_favorites(tmp_global_vault, "reflections", ids[:3], ["a", "b", "c"])

        current = favorites.load_favorites(tmp_global_vault, "reflections")
        assert path == tmp_global_vault / "reflections" / "favorites.yaml"
        assert [p["id"] for p in current["favorites"]] == ids[:3]
        assert [p["why"] for p in current["favorites"]] == ["a", "b", "c"]
        assert current["after"] == ids[3]

    @pytest.mark.parametrize("picks, reasons, message", [
        (["RF-0001", "RF-0002"], ["a", "b"], "exactly 3"),
        (["RF-0001", "RF-0001", "RF-0002"], ["a", "b", "c"], "exactly 3"),
        (["RF-0001", "RF-0002", "RF-0099"], ["a", "b", "c"], "RF-0099"),
        (["RF-0001", "RF-0002", "RF-0003"], ["a", "b"], "one --why per pick"),
        (["RF-0001", "RF-0002", "RF-0003"], ["a", " ", "c"], "one --why per pick"),
    ])
    def test_refuses_a_pick_that_does_not_hold(self, tmp_global_vault, picks, reasons, message) -> None:
        _ids(tmp_global_vault, "reflection", 4)

        with pytest.raises(favorites.FavoritesError, match=message):
            favorites.save_favorites(tmp_global_vault, "reflections", picks, reasons)
        assert favorites.load_favorites(tmp_global_vault, "reflections") is None

    def test_fewer_records_than_three_pick_all(self, tmp_global_vault: Path) -> None:
        ids = _ids(tmp_global_vault, "dream", 2)

        favorites.save_favorites(tmp_global_vault, "dreams", ids, ["x", "y"])

        assert len(favorites.load_favorites(tmp_global_vault, "dreams")["favorites"]) == 2


class TestDue:
    def test_never_picked_is_not_due(self, tmp_global_vault: Path) -> None:
        _ids(tmp_global_vault, "reflection", 3)
        assert favorites.due_reason(tmp_global_vault, "reflections") == ""

    def test_a_new_record_makes_the_pick_due(self, tmp_global_vault: Path) -> None:
        ids = _ids(tmp_global_vault, "reflection", 3)
        favorites.save_favorites(tmp_global_vault, "reflections", ids, ["a", "b", "c"])
        assert favorites.due_reason(tmp_global_vault, "reflections") == ""

        new = _record(tmp_global_vault, "reflection", "On Something New", "new", created="2026-10-30")

        assert new in favorites.due_reason(tmp_global_vault, "reflections")

    def test_a_backdated_new_record_still_makes_the_pick_due(self, tmp_global_vault: Path) -> None:
        ids = _ids(tmp_global_vault, "reflection", 3)
        favorites.save_favorites(tmp_global_vault, "reflections", ids, ["a", "b", "c"])

        new = _record(tmp_global_vault, "reflection", "On An Old Day", "old", created="2020-01-01")

        assert new in favorites.due_reason(tmp_global_vault, "reflections")

    def test_archiving_the_new_record_does_not_clear_the_due_pick(self, tmp_global_vault: Path) -> None:
        ids = _ids(tmp_global_vault, "dream", 3)
        favorites.save_favorites(tmp_global_vault, "dreams", ids, ["a", "b", "c"])
        new = _record(tmp_global_vault, "dream", "Late Dream", "late", created="2026-10-30")

        update_record(next((tmp_global_vault / "dreams").glob(f"{new}*.md")), status="archived")

        assert new in favorites.due_reason(tmp_global_vault, "dreams")

    @pytest.mark.parametrize("content", [
        b"favorites: [unclosed", b"- just\n- a list\n", b"favorites: nope\n",
        b"chosen: 2026-02-30\nfavorites: []\n", b"favorites:\n- id: RF-0001\n  why: \xff\xfe\n",
    ])
    def test_a_broken_file_is_reported_not_raised(self, tmp_global_vault: Path, content: bytes) -> None:
        _ids(tmp_global_vault, "reflection", 3)
        favorites.favorites_path(tmp_global_vault, "reflections").write_bytes(content)

        assert "choosing again rewrites it" in favorites.due_reason(tmp_global_vault, "reflections")
        assert favorites.render_favorites(tmp_global_vault, "reflections") == ("", [])
        assert "Favorite Reflection" not in assemble_boot(tmp_global_vault, project_vault=None)["global_packet"]

    def test_an_archived_favorite_makes_the_pick_due(self, tmp_global_vault: Path) -> None:
        ids = _ids(tmp_global_vault, "dream", 3)
        favorites.save_favorites(tmp_global_vault, "dreams", ids, ["a", "b", "c"])

        archived = next((tmp_global_vault / "dreams").glob(f"{ids[0]}*.md"))
        update_record(archived, status="archived")

        assert "no longer an active dream" in favorites.due_reason(tmp_global_vault, "dreams")


class TestBootShowsFavorites:
    def test_favorites_are_in_full_and_never_truncated(self, tmp_global_vault: Path) -> None:
        ids = [_record(tmp_global_vault, "reflection", f"On Long {n}", f"start{n} " + "word " * 4000 + f"end{n}",
                       created=f"2026-10-0{n + 1}") for n in range(3)]
        _record(tmp_global_vault, "reflection", "On The Newest", "newest body", created="2026-10-20")
        favorites.save_favorites(tmp_global_vault, "reflections", ids, ["one", "two", "three"])

        result = assemble_boot(tmp_global_vault, project_vault=None, budget=600)

        packet = result["global_packet"]
        for n in range(3):
            assert f"start{n}" in packet and f"end{n}" in packet
        assert "*Why I keep it: two*" in packet
        assert "## Latest Reflection" in packet and "newest body" in packet
        assert result["usage"]["favorite_reflections"]["used"] > 12000

    def test_latest_reflection_is_not_repeated_when_it_is_a_favorite(self, tmp_global_vault: Path) -> None:
        ids = _ids(tmp_global_vault, "reflection", 3)
        favorites.save_favorites(tmp_global_vault, "reflections", ids, ["a", "b", "c"])

        result = assemble_boot(tmp_global_vault, project_vault=None)

        assert "## Latest Reflection" not in result["global_packet"]
        assert result["global_packet"].count("reflection body 2") == 1

    def test_favorite_dreams_are_shown(self, tmp_global_vault: Path) -> None:
        ids = _ids(tmp_global_vault, "dream", 4)
        favorites.save_favorites(tmp_global_vault, "dreams", ids[1:], ["a", "b", "c"])

        packet = assemble_boot(tmp_global_vault, project_vault=None)["global_packet"]

        assert "## Favorite Dream: " + ids[1] in packet
        assert "dream body 0" not in packet


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _cli_vault(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: home))
    monkeypatch.chdir(tmp_path)
    cmd_init(argparse.Namespace(agent="claude", type="global"))
    return home / ".memory" / "claude"


def _create(kind: str, title: str) -> None:
    cmd_create(argparse.Namespace(
        agent="claude", type=kind, title=title, body=f"{title} body", body_file=None, scope="global",
        trust="working", field=None, short=None, working_dir=None,
    ))


def _favorites(kind: str, ids: list[str], why: list[str] | None) -> None:
    cmd_favorites(argparse.Namespace(agent="claude", kind=kind, ids=ids, why=why))


class TestFavoritesCli:
    def test_set_show_and_the_reminder_after_a_new_reflection(self, tmp_path, monkeypatch, capsys) -> None:
        _cli_vault(tmp_path, monkeypatch)
        for n in range(3):
            _create("reflection", f"On Thing {n}")
        err = capsys.readouterr().err
        assert "Tip: pick your three favorite reflections" in err

        _favorites("reflections", ["RF-0001", "RF-0002", "RF-0003"], ["a", "b", "c"])
        assert "Favorite reflections saved: RF-0001, RF-0002, RF-0003" in capsys.readouterr().out

        _create("reflection", "On Thing 3")
        assert "Now choose your three favorite reflections again" in capsys.readouterr().err

        _favorites("reflections", [], None)
        shown = capsys.readouterr().out
        assert "- RF-0002 On Thing 1: b" in shown
        assert "Due again: RF-0004 was written after you chose" in shown

    def test_create_still_succeeds_with_a_broken_file(self, tmp_path, monkeypatch, capsys) -> None:
        vault = _cli_vault(tmp_path, monkeypatch)
        _create("reflection", "On One")
        favorites.favorites_path(vault, "reflections").write_text("favorites: [unclosed", encoding="utf-8")
        capsys.readouterr()

        _create("reflection", "On Two")

        captured = capsys.readouterr()
        assert captured.out.strip() == "RF-0002"
        assert "Now choose your three favorite reflections again" in captured.err

    def test_a_bad_pick_exits_with_the_reason(self, tmp_path, monkeypatch, capsys) -> None:
        _cli_vault(tmp_path, monkeypatch)
        for n in range(3):
            _create("dream", f"Dream {n}")
        capsys.readouterr()

        with pytest.raises(SystemExit) as result:
            _favorites("dreams", ["DR-0001", "DR-0002"], ["a", "b"])

        assert result.value.code == 1
        assert "pick exactly 3 different dreams" in capsys.readouterr().err

    def test_boot_reports_a_due_pick_and_the_favorite_tokens(self, tmp_path, monkeypatch, capsys) -> None:
        _cli_vault(tmp_path, monkeypatch)
        for n in range(3):
            _create("dream", f"Dream {n}")
        _favorites("dreams", ["DR-0001", "DR-0002", "DR-0003"], ["a", "b", "c"])
        _create("dream", "Dream 3")
        capsys.readouterr()

        cmd_boot(argparse.Namespace(agent="claude", working_dir=None, general=False, branch="main",
                                    budget=12000, hook_input=None, harness=None))

        out = capsys.readouterr().out
        assert "=== Favorites Due ===" in out
        assert "- dreams: DR-0004 was written after you chose" in out
        assert "favorite_dreams:" in out and "(exempt — always in full)" in out
