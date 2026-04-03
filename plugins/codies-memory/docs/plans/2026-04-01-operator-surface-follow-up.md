# Operator Surface Follow-Up Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix the remaining operator-surface drift in `codies-memory` so live agents land on the current CLI and the session-close skill examples match the v2 vault layout.

**Architecture:** Keep the implementation narrow and docs-first. The current CLI behavior is mostly correct; the remaining problems are install/update ergonomics and stale skill examples. Fix the docs and skill paths, then verify the documented flows against the current plugin-local venv.

**Tech Stack:** Python CLI (`argparse`), Markdown skill docs, `uv`, pytest

---

### Task 1: Fix Install And Upgrade Guidance

**Files:**
- Modify: `INSTALL.md`

- [ ] Update Step 0 so an existing `codies-memory` binary does not automatically imply “skip ahead and trust it”.
- [ ] Add an explicit “existing clone/update” path:
  - if `~/.local/share/codies-memory` exists, run `git pull` and `uv sync`
  - if the command resolves from another location, tell the operator to verify which copy they are using
- [ ] Clarify the intended operator surface for Codex/OpenCode:
  - either “standalone clone in `~/.local/share/codies-memory` is the supported path”
  - or “prefer the plugin copy when working from the `limitless` repo”
- [ ] Add a short verification step that checks:
  - `which codies-memory`
  - `codies-memory -h`
  - the expected commands include `user` and `feedback`

### Task 2: Refresh `memory-close-session` For V2 Reality

**Files:**
- Modify: `skills/memory-close-session/SKILL.md`

- [ ] Replace the literal `$(date ...)` shell substitution in the session title example with a version that works as written.
- [ ] Remove the stale `Path('.memory')` example from the promotion-evaluation snippet.
- [ ] Rewrite the example so it resolves the project vault using the current v2 conventions:
  - namespaced global vault under `~/.memory/<agent>/`
  - project resolution via `--agent` and current working directory, or via the Python helpers that resolve the project vault correctly
- [ ] Keep the example short enough that an agent can copy it without hand-repairing broken assumptions.

### Task 3: Verify The Operator Path End To End

**Files:**
- Modify if needed: `INSTALL.md`
- Modify if needed: `skills/memory-close-session/SKILL.md`
- Test: `tests/test_cli.py`

- [ ] Run the focused CLI test slice:

```bash
cd /home/pyro/projects/private/limitless/plugins/codies-memory
./.venv/bin/pytest -q tests/test_cli.py tests/test_promotion.py tests/test_vault.py tests/test_records.py
```

- [ ] Smoke-test the documented install/update flow manually from the plugin repo:

```bash
cd /home/pyro/projects/private/limitless/plugins/codies-memory
./.venv/bin/codies-memory -h
./.venv/bin/codies-memory status --agent Codie --working-dir /home/pyro/projects/private/limitless
```

- [ ] If the docs now describe a behavior that is not yet enforced by code, either:
  - add the missing code/test in the same pass, or
  - explicitly narrow the docs so they only promise what is true today

### Task 4: Close The Loop In Project Memory

**Files:**
- Modify or create: project memory record after implementation

- [ ] After the fixes land, replace the old remembered “Codex install gap” framing with the more accurate issue:
  - first-time install is mostly fine
  - stale preexisting installs need better upgrade guidance
- [ ] Record that `memory-close-session` was one of the remaining stale v2 examples if that fix lands.

