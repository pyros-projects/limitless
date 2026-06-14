# Codies Memory Explicit General Read Mode Implementation Plan

> **For agentic workers:** Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans when available to implement this plan task-by-task. If those skills are unavailable, follow the inline execution rules below. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add intentional read access to the reserved `_general` memory project while preserving implicit writes and avoiding silent vault-less boot pollution.

**Architecture:** Keep `create` and `capture` as implicit write fallbacks to `_general` so notes are not lost from vault-less folders. Add explicit `--general` read mode for `boot`, `status`, and `list`; normal vault-less boot stays global-only but shows the global daily-log tail for awareness. Do not change project resolution for `validate`, `promote`, `create`, or `capture`.

**Tech Stack:** Python CLI with `argparse`, pytest, Markdown skill docs, existing `codies_memory` vault/boot/list helpers.

---

## Scope And Decisions

This plan implements the rule: implicit for not losing writes, explicit for loading context, daily log for awareness.

In scope:
- `codies-memory boot --agent Codie --general`
- `codies-memory status --agent Codie --general`
- `codies-memory list sessions --agent Codie --general`
- global-only boot includes the latest global daily-log tail even when no project vault resolves
- skill docs explain how to remember and retrieve notes from vault-less folders
- explicit read commands may lazily create `_general` on older global vaults through `ensure_general_project_vault`

Out of scope:
- no implicit `_general` loading for normal `boot`, `status`, or `list`
- no `validate --general`
- no `promote --general`
- no project slug selector beyond the reserved `_general` affordance
- no schema or vault-layout migration

## Execution Rules If Sub-Skills Are Unavailable

If `superpowers:subagent-driven-development` or `superpowers:executing-plans`
is not available to the worker, execute this document directly in task order.
For each task: write the failing test first, run the focused failing command,
make only the described minimal code or docs change, run the focused passing
command, then commit before moving to the next task. Do not batch code changes
from later tasks into an earlier task.

## File Structure

- Modify `plugins/codies-memory/src/codies_memory/boot.py`
  - Responsibility: assemble boot packets and include global daily-log awareness during global-only boot.
- Modify `plugins/codies-memory/src/codies_memory/cli.py`
  - Responsibility: expose `--general` on read commands and route those commands to the reserved `_general` project vault.
- Modify `plugins/codies-memory/pyproject.toml`
  - Responsibility: bump the package version for the new CLI behavior.
- Modify `plugins/codies-memory/uv.lock`
  - Responsibility: keep the locked editable package metadata aligned with `pyproject.toml`.
- Modify `plugins/codies-memory/src/codies_memory/__init__.py`
  - Responsibility: keep the module runtime version aligned with package metadata.
- Modify `plugins/codies-memory/.claude-plugin/plugin.json`
  - Responsibility: bump the Claude plugin marketplace version and description.
- Modify `.claude-plugin/marketplace.json`
  - Responsibility: update the marketplace entry copy for the changed codies-memory operator surface.
- Modify `README.md`
  - Responsibility: update the public plugin table copy for the changed codies-memory operator surface.
- Modify `plugins/codies-memory/tests/test_boot.py`
  - Responsibility: verify global-only boot includes daily-log awareness without loading `_general`.
- Modify `plugins/codies-memory/tests/test_cli.py`
  - Responsibility: verify explicit `--general` read behavior for boot, status, and list.
- Modify `plugins/codies-memory/skills/memory-boot/SKILL.md`
  - Responsibility: teach agents the new boot behavior and the explicit `_general` read command.
- Modify `plugins/codies-memory/skills/memory-help/SKILL.md`
  - Responsibility: document the CLI affordance and the write/read split.
- Modify `plugins/codies-memory/skills/memory-capture/SKILL.md`
  - Responsibility: make the fallback write path discoverable with its matching read path.

## Task 1: Global-Only Boot Shows Daily Log Tail

**Files:**
- Modify: `plugins/codies-memory/src/codies_memory/boot.py`
- Test: `plugins/codies-memory/tests/test_boot.py`

- [ ] **Step 1: Write the failing boot test**

Add this test to `plugins/codies-memory/tests/test_boot.py` inside `class TestAssembleBoot`, after `test_boot_includes_latest_daily_log_tail`:

```python
    def test_global_only_boot_includes_daily_log_tail(
        self, tmp_global_vault: Path
    ) -> None:
        sessions = tmp_global_vault / "sessions"
        sessions.mkdir()
        lines = [
            f"- [[SS-20260614-{i:04d}]] Daily item {i:02d} (project-{i:02d})"
            for i in range(1, DAILY_LOG_TAIL_LINES + 4)
        ]
        (sessions / "2026-06-14.md").write_text(
            "---\n"
            "id: DL-20260614\n"
            "title: '2026-06-14'\n"
            "type: daily-log\n"
            "status: active\n"
            "trust: canonical\n"
            "scope: global\n"
            "created: '2026-06-14T12:00:00+02:00'\n"
            "updated: '2026-06-14T12:00:00+02:00'\n"
            "---\n\n"
            + "\n".join(lines)
            + "\n"
        )

        result = assemble_boot(tmp_global_vault, project_vault=None, budget=4000)

        assert result["project_packet"].startswith("## Global Daily Log")
        assert "Daily item 01" not in result["project_packet"]
        assert f"Daily item {DAILY_LOG_TAIL_LINES + 3:02d}" in result["project_packet"]
        assert "branch_session" in result["usage"]["layers"]
```

- [ ] **Step 2: Run the test to verify it fails**

Run:

```bash
cd /home/pyro/projects/private/limitless
plugins/codies-memory/.venv/bin/pytest -q plugins/codies-memory/tests/test_boot.py::TestAssembleBoot::test_global_only_boot_includes_daily_log_tail
```

Expected: FAIL because `assemble_boot(..., project_vault=None)` currently returns an empty `project_packet`.

- [ ] **Step 3: Implement global-only daily-log awareness**

In `plugins/codies-memory/src/codies_memory/boot.py`, replace the existing global-only boot block:

```python
    # Global-only boot: no project context
    if project_vault is None:
        return {
            "global_packet": separator.join(global_layers),
            "project_packet": "",
            "usage": _usage(usage_layers),
        }
```

with:

```python
    # Global-only boot: no project context, but keep cross-project awareness.
    if project_vault is None:
        daily_log_lines = _read_latest_daily_log_tail_lines(global_vault)
        daily_log_raw = _format_daily_log(daily_log_lines)
        layer5 = _fit_recent_activity("", daily_log_lines, budgets["branch_session"])
        usage_layers["branch_session"] = {
            "used": estimate_tokens(daily_log_raw),
            "budget": budgets["branch_session"],
        }
        return {
            "global_packet": separator.join(global_layers),
            "project_packet": layer5,
            "usage": _usage(usage_layers),
        }
```

- [ ] **Step 4: Run the focused boot tests**

Run:

```bash
cd /home/pyro/projects/private/limitless
plugins/codies-memory/.venv/bin/pytest -q plugins/codies-memory/tests/test_boot.py::TestAssembleBoot
```

Expected: PASS.

- [ ] **Step 5: Commit Task 1**

Run:

```bash
cd /home/pyro/projects/private/limitless
git add plugins/codies-memory/src/codies_memory/boot.py plugins/codies-memory/tests/test_boot.py
git commit -m "feat: show daily log during global-only memory boot"
```

## Task 2: Add `--general` To Boot

**Files:**
- Modify: `plugins/codies-memory/src/codies_memory/cli.py`
- Test: `plugins/codies-memory/tests/test_cli.py`

- [ ] **Step 1: Write the failing CLI boot test**

Add this test to `plugins/codies-memory/tests/test_cli.py` inside `class TestCmdBoot`, after `test_global_only_boot`:

```python
    def test_boot_general_flag_loads_general_project(self, tmp_path, monkeypatch, capsys):
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: fake_home))

        cmd_init(argparse.Namespace(agent="claude", type="global"))
        unrelated = tmp_path / "no-project"
        unrelated.mkdir()
        monkeypatch.chdir(unrelated)
        capsys.readouterr()

        cmd_create(argparse.Namespace(
            agent="claude",
            type="session",
            title="General closeout",
            body="This is a session stored in the general project.",
            body_file=None,
            scope="project",
            trust="working",
            field=None,
            short="General closeout",
            working_dir=None,
        ))
        capsys.readouterr()

        cmd_boot(argparse.Namespace(
            agent="claude",
            branch="main",
            budget=4000,
            working_dir=None,
            general=True,
        ))

        captured = capsys.readouterr()
        assert "no project vault found" not in captured.err
        assert "Using reserved _general project vault" in captured.err
        assert "## Global Daily Log" in captured.out
        assert "General closeout (_general)" in captured.out
```

Add this regression test to the same class, immediately after `test_boot_general_flag_loads_general_project`:

```python
    def test_normal_vaultless_boot_after_general_write_does_not_load_general_project(
        self, tmp_path, monkeypatch, capsys
    ):
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: fake_home))

        cmd_init(argparse.Namespace(agent="claude", type="global"))
        unrelated = tmp_path / "no-project"
        unrelated.mkdir()
        monkeypatch.chdir(unrelated)
        capsys.readouterr()

        cmd_create(argparse.Namespace(
            agent="claude",
            type="session",
            title="General-only body guard",
            body="This body must not appear during normal vaultless boot.",
            body_file=None,
            scope="project",
            trust="working",
            field=None,
            short="General-only body guard",
            working_dir=None,
        ))
        capsys.readouterr()

        cmd_boot(argparse.Namespace(
            agent="claude",
            branch="main",
            budget=4000,
            working_dir=None,
            general=False,
        ))

        captured = capsys.readouterr()
        assert "no project vault found" in captured.err
        assert "## Global Daily Log" in captured.out
        assert "General-only body guard (_general)" in captured.out
        assert "This body must not appear during normal vaultless boot." not in captured.out
```

- [ ] **Step 2: Run the test to verify it fails**

Run:

```bash
cd /home/pyro/projects/private/limitless
plugins/codies-memory/.venv/bin/pytest -q plugins/codies-memory/tests/test_cli.py::TestCmdBoot::test_boot_general_flag_loads_general_project
```

Expected: FAIL because `cmd_boot` does not read `args.general` yet.

- [ ] **Step 3: Add a read helper for explicit `_general`**

In `plugins/codies-memory/src/codies_memory/cli.py`, add this helper immediately after `_resolve_project_vault`:

```python
def _resolve_project_vault_for_read(
    args: argparse.Namespace,
    global_vault: Path,
) -> tuple[Path | None, Path]:
    """Resolve project context for read commands.

    Normal reads use the working directory. Explicit ``--general`` reads use
    the reserved catch-all project vault and create it if an older global vault
    does not have it yet.
    """
    working_dir = Path(args.working_dir).resolve() if getattr(args, "working_dir", None) else Path.cwd()
    if getattr(args, "general", False):
        return ensure_general_project_vault(global_vault), working_dir
    return resolve_project_vault(global_vault, working_dir), working_dir
```

- [ ] **Step 4: Route boot through the helper**

In `cmd_boot`, replace:

```python
    working_dir = Path(args.working_dir).resolve() if getattr(args, "working_dir", None) else Path.cwd()
    project_vault = resolve_project_vault(global_vault, working_dir)

    if project_vault is None:
        print("Warning: no project vault found; global-only boot.", file=sys.stderr)
```

with:

```python
    project_vault, working_dir = _resolve_project_vault_for_read(args, global_vault)

    if project_vault is None:
        print("Warning: no project vault found; global-only boot.", file=sys.stderr)
    elif getattr(args, "general", False):
        print("Using reserved _general project vault.", file=sys.stderr)
```

- [ ] **Step 5: Add parser support for `boot --general`**

In `main()`, where the parsers are built, add this argument to the boot parser after `--working-dir`:

```python
    boot_parser.add_argument(
        "--general",
        action="store_true",
        default=False,
        help="Load the reserved _general project vault instead of resolving from the working directory.",
    )
```

- [ ] **Step 6: Run the focused boot CLI tests**

Run:

```bash
cd /home/pyro/projects/private/limitless
plugins/codies-memory/.venv/bin/pytest -q plugins/codies-memory/tests/test_cli.py::TestCmdBoot
```

Expected: PASS.

- [ ] **Step 7: Commit Task 2**

Run:

```bash
cd /home/pyro/projects/private/limitless
git add plugins/codies-memory/src/codies_memory/cli.py plugins/codies-memory/tests/test_cli.py
git commit -m "feat: add explicit general memory boot"
```

## Task 3: Add `--general` To Status And List

**Files:**
- Modify: `plugins/codies-memory/src/codies_memory/cli.py`
- Test: `plugins/codies-memory/tests/test_cli.py`

- [ ] **Step 1: Write failing status and list tests**

Add these tests to `plugins/codies-memory/tests/test_cli.py`.

Inside `class TestCmdStatus`, add:

```python
    def test_status_general_flag_reads_general_inbox(self, tmp_path, monkeypatch, capsys):
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: fake_home))

        cmd_init(argparse.Namespace(agent="claude", type="global"))
        unrelated = tmp_path / "no-project"
        unrelated.mkdir()
        monkeypatch.chdir(unrelated)
        capsys.readouterr()

        cmd_capture(argparse.Namespace(
            agent="claude",
            content="General inbox item",
            source="test",
            gate="allow",
            short="General inbox item",
            working_dir=None,
        ))
        capsys.readouterr()

        cmd_status(argparse.Namespace(
            agent="claude",
            all=True,
            working_dir=None,
            general=True,
        ))

        out = capsys.readouterr().out
        assert "Project vault:" in out
        assert "/_general" in out
        assert "Active: 1" in out
        assert "General inbox item" in out
```

Inside `class TestCmdList`, add:

```python
    def test_cmd_list_general_flag_reads_general_sessions(self, tmp_path, monkeypatch, capsys):
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: fake_home))

        cmd_init(argparse.Namespace(agent="claude", type="global"))
        unrelated = tmp_path / "no-project"
        unrelated.mkdir()
        monkeypatch.chdir(unrelated)
        capsys.readouterr()

        cmd_create(argparse.Namespace(
            agent="claude",
            type="session",
            title="General session",
            body="Session body in _general.",
            body_file=None,
            scope="project",
            trust="working",
            field=None,
            short="General session",
            working_dir=None,
        ))
        capsys.readouterr()

        cmd_list(argparse.Namespace(
            agent="claude",
            type="sessions",
            scope="project",
            status=None,
            trust=None,
            format="table",
            working_dir=None,
            general=True,
        ))

        out = capsys.readouterr().out
        assert "General session" in out

    def test_cmd_list_general_conflicts_with_global_scope(self, tmp_path, monkeypatch, capsys):
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: fake_home))

        cmd_init(argparse.Namespace(agent="claude", type="global"))
        capsys.readouterr()

        with pytest.raises(SystemExit):
            cmd_list(argparse.Namespace(
                agent="claude",
                type="reflections",
                scope="global",
                status=None,
                trust=None,
                format="table",
                working_dir=None,
                general=True,
            ))

        err = capsys.readouterr().err
        assert "--general can only be used with --scope project" in err
```

- [ ] **Step 2: Run the tests to verify they fail**

Run:

```bash
cd /home/pyro/projects/private/limitless
plugins/codies-memory/.venv/bin/pytest -q \
  plugins/codies-memory/tests/test_cli.py::TestCmdStatus::test_status_general_flag_reads_general_inbox \
  plugins/codies-memory/tests/test_cli.py::TestCmdList::test_cmd_list_general_flag_reads_general_sessions \
  plugins/codies-memory/tests/test_cli.py::TestCmdList::test_cmd_list_general_conflicts_with_global_scope
```

Expected: FAIL because `cmd_status` and `cmd_list` do not read `args.general` yet.

- [ ] **Step 3: Route status through the read helper**

In `cmd_status`, replace:

```python
    working_dir = Path(args.working_dir).resolve() if getattr(args, "working_dir", None) else Path.cwd()
    project_vault = resolve_project_vault(global_vault, working_dir)
```

with:

```python
    project_vault, working_dir = _resolve_project_vault_for_read(args, global_vault)
```

Do not change the existing `project_vault is None` behavior.

- [ ] **Step 4: Route list through explicit `_general`**

In `cmd_list`, replace the current vault resolution block:

```python
    if scope == "global":
        vault = global_vault
    else:
        working_dir = Path(args.working_dir).resolve() if getattr(args, "working_dir", None) else Path.cwd()
        vault = resolve_project_vault(global_vault, working_dir)
        if vault is None:
            print(f"Error: no project vault found for {working_dir}", file=sys.stderr)
            sys.exit(1)
```

with:

```python
    if scope == "global":
        if getattr(args, "general", False):
            print("Error: --general can only be used with --scope project.", file=sys.stderr)
            sys.exit(1)
        vault = global_vault
    else:
        vault, working_dir = _resolve_project_vault_for_read(args, global_vault)
        if vault is None:
            print(f"Error: no project vault found for {working_dir}", file=sys.stderr)
            sys.exit(1)
```

- [ ] **Step 5: Add parser support for `status --general` and `list --general`**

In `main()`, where the parsers are built, add this argument to the status parser after `--working-dir`:

```python
    status_parser.add_argument(
        "--general",
        action="store_true",
        default=False,
        help="Read the reserved _general project vault instead of resolving from the working directory.",
    )
```

In `main()`, add this argument to the list parser after `--working-dir`:

```python
    list_parser.add_argument(
        "--general",
        action="store_true",
        default=False,
        help="List records from the reserved _general project vault instead of resolving from the working directory.",
    )
```

- [ ] **Step 6: Run the focused status and list tests**

Run:

```bash
cd /home/pyro/projects/private/limitless
plugins/codies-memory/.venv/bin/pytest -q \
  plugins/codies-memory/tests/test_cli.py::TestCmdStatus \
  plugins/codies-memory/tests/test_cli.py::TestCmdList
```

Expected: PASS.

- [ ] **Step 7: Commit Task 3**

Run:

```bash
cd /home/pyro/projects/private/limitless
git add plugins/codies-memory/src/codies_memory/cli.py plugins/codies-memory/tests/test_cli.py
git commit -m "feat: add explicit general memory reads"
```

## Task 4: Update Memory Skill Docs

**Files:**
- Modify: `plugins/codies-memory/skills/memory-boot/SKILL.md`
- Modify: `plugins/codies-memory/skills/memory-help/SKILL.md`
- Modify: `plugins/codies-memory/skills/memory-capture/SKILL.md`

- [ ] **Step 1: Update boot skill wording**

In `plugins/codies-memory/skills/memory-boot/SKILL.md`, replace:

```markdown
Boot does not fall back to `_general`. If no project vault resolves, it reports a
global-only boot. When a project vault does resolve, the recent activity layer
also includes `Global Daily Log`, a cross-project tail from
`~/.memory/<agent>/sessions/YYYY-MM-DD.md`. If the resolved project vault is
`_general`, tell the user records are landing in the default catch-all project,
not a named project.
```

with:

````markdown
Boot does not implicitly fall back to `_general`. If no project vault resolves,
normal boot reports a global-only boot and still includes the latest
`Global Daily Log` tail for cross-project awareness. To intentionally load the
reserved catch-all project, use:

```bash
codies-memory boot --agent <name> --general
```

If the resolved project vault is `_general`, tell the user records are landing
in the default catch-all project, not a named project.
````

In the command examples, add:

```bash
# Intentionally boot the catch-all project for vault-less notes
codies-memory boot --agent <name> --general
```

- [ ] **Step 2: Update help skill project-resolution wording**

In `plugins/codies-memory/skills/memory-help/SKILL.md`, replace the project-resolution paragraph:

```markdown
For `create` and `capture`, if no project vault resolves, the command falls back
to `_general`. Other commands (`status`, `boot`, `validate`, `list`) report
which vault resolved, or None, without fallback.
```

with:

```markdown
For `create` and `capture`, if no project vault resolves, the command falls back
to `_general` so the memory is not lost. Read commands do not implicitly load
`_general`: use `--general` with `boot`, `status`, or `list` when you want the
reserved catch-all project. `validate` still requires a normally resolved
project vault.
```

- [ ] **Step 3: Add help skill command examples**

In `plugins/codies-memory/skills/memory-help/SKILL.md`, add these examples under `## Commands`:

```bash
# Boot vault-less notes intentionally
codies-memory boot --agent <name> --general

# Inspect the catch-all inbox
codies-memory status --agent <name> --general --all

# List catch-all sessions
codies-memory list sessions --agent <name> --general
```

- [ ] **Step 4: Update capture skill routing note**

In `plugins/codies-memory/skills/memory-capture/SKILL.md`, after the scope routing note that says project-scoped writes fall back to `_general`, add:

````markdown
To read those catch-all records later, use explicit read mode:

```bash
codies-memory boot --agent <name> --general
codies-memory status --agent <name> --general --all
codies-memory list sessions --agent <name> --general
```
````

- [ ] **Step 5: Verify docs mention the new flag**

Run:

```bash
cd /home/pyro/projects/private/limitless
rg -n -- "--general|_general|Global Daily Log" \
  plugins/codies-memory/skills/memory-boot/SKILL.md \
  plugins/codies-memory/skills/memory-help/SKILL.md \
  plugins/codies-memory/skills/memory-capture/SKILL.md
```

Expected: output includes `memory-boot`, `memory-help`, and `memory-capture`.

- [ ] **Step 6: Commit Task 4**

Run:

```bash
cd /home/pyro/projects/private/limitless
git add plugins/codies-memory/skills/memory-boot/SKILL.md plugins/codies-memory/skills/memory-help/SKILL.md plugins/codies-memory/skills/memory-capture/SKILL.md
git commit -m "docs: document explicit general memory reads"
```

## Task 5: Bump Release Metadata And Marketplace Copy

**Files:**
- Modify: `plugins/codies-memory/pyproject.toml`
- Modify: `plugins/codies-memory/uv.lock`
- Modify: `plugins/codies-memory/src/codies_memory/__init__.py`
- Modify: `plugins/codies-memory/.claude-plugin/plugin.json`
- Modify: `.claude-plugin/marketplace.json`
- Modify: `README.md`

- [ ] **Step 1: Bump Python package metadata**

In `plugins/codies-memory/pyproject.toml`, replace:

```toml
version = "1.1.0"
```

with:

```toml
version = "1.2.2"
```

- [ ] **Step 2: Bump module runtime version**

In `plugins/codies-memory/src/codies_memory/__init__.py`, replace:

```python
__version__ = "0.1.0"
```

with:

```python
__version__ = "1.2.2"
```

- [ ] **Step 3: Bump Claude plugin manifest**

In `plugins/codies-memory/.claude-plugin/plugin.json`, replace:

```json
  "version": "1.2.1",
  "description": "File-based two-tier memory system for AI agents. Agent-namespaced vaults with promotion pipelines, trust levels, and CLI write commands. Gives any agent persistent memory across sessions.",
```

with:

```json
  "version": "1.2.2",
  "description": "File-based two-tier memory system for AI agents. Agent-namespaced vaults with promotion pipelines, trust levels, CLI write commands, and explicit _general read mode for vault-less notes. Gives any agent persistent memory across sessions.",
```

- [ ] **Step 4: Refresh the uv lockfile**

Run:

```bash
cd /home/pyro/projects/private/limitless/plugins/codies-memory
uv lock
```

Expected: `plugins/codies-memory/uv.lock` updates the editable `codies-memory`
package entry to `version = "1.2.2"`.

- [ ] **Step 5: Update marketplace entry copy**

In `.claude-plugin/marketplace.json`, replace the `codies-memory` plugin entry description:

```json
      "description": "Persistent agent memory with agent-namespaced vaults, promotion pipelines, trust levels, and CLI write commands. Requires uv sync setup."
```

with:

```json
      "description": "Persistent agent memory with agent-namespaced vaults, promotion pipelines, trust levels, CLI write commands, and explicit _general read mode for vault-less notes. Requires uv sync setup."
```

- [ ] **Step 6: Update README plugin table copy**

In `README.md`, replace the `codies-memory` plugin table row:

```markdown
| [**codies-memory**](plugins/codies-memory/) | 4 | Persistent agent memory with agent-namespaced vaults, promotion pipelines, trust levels, and CLI write commands. Requires `uv sync` setup — see INSTALL.md. |
```

with:

```markdown
| [**codies-memory**](plugins/codies-memory/) | 4 | Persistent agent memory with agent-namespaced vaults, promotion pipelines, trust levels, CLI write commands, and explicit `_general` read mode for vault-less notes. Requires `uv sync` setup — see INSTALL.md. |
```

- [ ] **Step 7: Verify all version surfaces and marketplace copy**

Run:

```bash
cd /home/pyro/projects/private/limitless
rg -n '^version = "1\\.2\\.2"$' plugins/codies-memory/pyproject.toml plugins/codies-memory/uv.lock
rg -n '^__version__ = "1\\.2\\.2"$' plugins/codies-memory/src/codies_memory/__init__.py
rg -n '"version": "1\\.2\\.2"' plugins/codies-memory/.claude-plugin/plugin.json
rg -n "explicit _general read mode|explicit `_general` read mode" \
  plugins/codies-memory/.claude-plugin/plugin.json \
  .claude-plugin/marketplace.json \
  README.md
python3 -m json.tool plugins/codies-memory/.claude-plugin/plugin.json >/dev/null
python3 -m json.tool .claude-plugin/marketplace.json >/dev/null
```

Expected:
- `pyproject.toml`, `uv.lock`, `__init__.py`, and plugin manifest all report `1.2.2`
- plugin manifest, marketplace entry, and README mention explicit `_general` read mode
- both JSON files parse successfully

- [ ] **Step 8: Commit Task 5**

Run:

```bash
cd /home/pyro/projects/private/limitless
git add plugins/codies-memory/pyproject.toml plugins/codies-memory/uv.lock plugins/codies-memory/src/codies_memory/__init__.py plugins/codies-memory/.claude-plugin/plugin.json .claude-plugin/marketplace.json README.md
git commit -m "chore: bump codies-memory to 1.2.2"
```

## Task 6: Full Verification And Live Smoke

**Files:**
- Verify: `plugins/codies-memory/pyproject.toml`
- Verify: `plugins/codies-memory/uv.lock`
- Verify: `plugins/codies-memory/src/codies_memory/__init__.py`
- Verify: `plugins/codies-memory/.claude-plugin/plugin.json`
- Verify: `.claude-plugin/marketplace.json`
- Verify: `README.md`
- Verify: `plugins/codies-memory/src/codies_memory/boot.py`
- Verify: `plugins/codies-memory/src/codies_memory/cli.py`
- Verify: `plugins/codies-memory/tests/test_boot.py`
- Verify: `plugins/codies-memory/tests/test_cli.py`
- Verify: `plugins/codies-memory/skills/memory-boot/SKILL.md`
- Verify: `plugins/codies-memory/skills/memory-help/SKILL.md`
- Verify: `plugins/codies-memory/skills/memory-capture/SKILL.md`

- [ ] **Step 1: Run the full codies-memory test suite**

Run:

```bash
cd /home/pyro/projects/private/limitless/plugins/codies-memory
./.venv/bin/pytest -q
```

Expected: PASS.

- [ ] **Step 2: Run CLI help smoke checks**

Run:

```bash
cd /home/pyro/projects/private/limitless/plugins/codies-memory
./.venv/bin/codies-memory boot -h | rg -- "--general"
./.venv/bin/codies-memory status -h | rg -- "--general"
./.venv/bin/codies-memory list -h | rg -- "--general"
```

Expected: each command prints a matching `--general` help line.

- [ ] **Step 3: Run an isolated live smoke without touching real memory**

Run:

```bash
set -euo pipefail
tmp_home="$(mktemp -d)"
tmp_work="$(mktemp -d)"
trap 'rm -rf "$tmp_home" "$tmp_work"' EXIT
cd /home/pyro/projects/private/limitless/plugins/codies-memory
HOME="$tmp_home" ./.venv/bin/codies-memory init --type global --agent Smoke
create_out="$(HOME="$tmp_home" ./.venv/bin/codies-memory create session \
  --agent Smoke \
  --working-dir "$tmp_work" \
  --title "Smoke general session" \
  --short "Smoke general session" \
  --body "This session should land in _general.")"
case "$create_out" in
  SS-*) ;;
  *) echo "expected SS- record id, got: $create_out" >&2; exit 1 ;;
esac
boot_out="$(HOME="$tmp_home" ./.venv/bin/codies-memory boot --agent Smoke --working-dir "$tmp_work" --general 2>&1)"
printf '%s\n' "$boot_out" | rg "Using reserved _general project vault"
printf '%s\n' "$boot_out" | rg "Global Daily Log"
printf '%s\n' "$boot_out" | rg "Smoke general session \\(_general\\)"
HOME="$tmp_home" ./.venv/bin/codies-memory list sessions --agent Smoke --working-dir "$tmp_work" --general | rg "Smoke general session"
HOME="$tmp_home" ./.venv/bin/codies-memory status --agent Smoke --working-dir "$tmp_work" --general
```

Expected:
- the create command prints an `SS-...` record id
- boot output contains `Using reserved _general project vault`, `Global Daily Log`, and the daily-log line for `_general`
- list output contains `Smoke general session`
- status output names a project vault ending in `_general`

- [ ] **Step 4: Check formatting and repo state**

Run:

```bash
cd /home/pyro/projects/private/limitless
git diff --check
git status --short
```

Expected: `git diff --check` exits 0. `git status --short` shows only intended files if Task 6 has not been committed yet.

- [ ] **Step 5: Commit final verification-only doc adjustments if any exist**

If Step 4 shows only intended documentation or test adjustments from verification, run:

```bash
cd /home/pyro/projects/private/limitless
git add plugins/codies-memory
git commit -m "test: verify explicit general memory reads"
```

If Step 4 shows no changes, skip the commit.

## Self-Review

Spec coverage:
- implicit writes remain unchanged through existing `create` and `capture` behavior
- explicit reads are covered for `boot`, `status`, and `list`
- global-only boot daily-log awareness is covered in `tests/test_boot.py`
- normal vault-less read commands still do not silently load `_general`
- docs explain how to remember from `/home/pyro` or another vault-less folder and how to retrieve those records
- release metadata bump is included as a first-class task and aligns Python/package/plugin surfaces at `1.2.2`

Placeholder scan:
- no unresolved placeholders remain in this plan
- every code step names exact files and includes concrete code snippets
- every verification step includes exact commands and expected outcomes

Type consistency:
- all new CLI examples use the same flag name: `--general`
- all command handlers use the same helper: `_resolve_project_vault_for_read`
- `_general` remains the reserved project slug managed by `ensure_general_project_vault`

## Execution Handoff

Plan complete and saved to `docs/plans/2026-06-14-codies-memory-explicit-general-read-mode.md`. Two execution options:

1. Subagent-Driven (recommended) - dispatch a fresh subagent per task, review between tasks, fast iteration
2. Inline Execution - execute tasks in this session using executing-plans, batch execution with checkpoints

Recommended path: Inline Execution is probably enough because this is a tight CLI-and-docs patch with focused tests.
