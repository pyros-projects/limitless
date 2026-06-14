# Codies Memory Testing Checklist

Use this checklist from the plugin root:

```bash
cd /home/pyro/projects/private/limitless/plugins/codies-memory
```

## 1. Unit And Integration Tests

```bash
./.venv/bin/pytest -q
```

Expected: the full test suite passes.

## 2. Package Consistency Smoke

Run the maintained smoke script:

```bash
./scripts/smoke.sh
```

The script creates a temporary HOME and temporary working directories, then
removes them on exit. It does not touch the operator's real `~/.memory` vault.

The smoke exercises:

- global vault init and validation
- named project init, marker resolution, and validation
- user and feedback writes
- project capture, status, list, and promote-to-thread flow
- project lesson, decision, and body-file session creation
- project lesson promotion to global
- global reflection auto-routing
- refresh and named-project boot
- vault-less `create` and `capture` fallback to `_general`
- normal vault-less reads refusing to silently load `_general`
- explicit `_general` reads through `boot --general`, `status --general`, and
  `list --general`
- `list daily-log --scope global` plus daily-log body checks
- final global and project validation

Expected final line:

```text
PASS: codies-memory smoke completed with isolated HOME=...
```

## 3. Agent Skill Smoke

When changing skill docs or `_general` operator behavior, run the agent smoke
recipe:

```bash
cat docs/agent-smoke.md
```

Then launch a fresh subagent with the scenario prompt from
`docs/agent-smoke.md`. The agent smoke is intentionally not a shell script: it
tests whether the skill docs make a fresh agent use codies-memory correctly
with a temporary HOME.

Expected result: the subagent returns a Y/N scorecard with `PASS` or a clear
`PARTIAL`/`FAIL` plus the exact loophole.

## 4. Optional Manual Spot Checks

After changing CLI parsing or help text:

```bash
./.venv/bin/codies-memory boot -h | rg -- "--general"
./.venv/bin/codies-memory status -h | rg -- "--general"
./.venv/bin/codies-memory list -h | rg -- "--general"
```

After changing release metadata:

```bash
rg -n '^version = "1\.2\.2"$' pyproject.toml uv.lock
rg -n '^__version__ = "1\.2\.2"$' src/codies_memory/__init__.py
python3 -m json.tool .claude-plugin/plugin.json >/dev/null
```

## 5. Pre-Commit Checks

From the repository root:

```bash
git diff --check
git status --short
```
