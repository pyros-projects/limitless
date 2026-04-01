---
title: OpenCode Integration & Full Cycle Review
date: 2026-03-31
reviewer: GLM-5.1 (OpenCode agent)
type: review
---

# Codies-Memory — OpenCode Integration & Full Cycle Review

## Setup

- **Agent:** OpenCode, GLM-5.1 model
- **Date:** 2026-03-31
- **Repo:** `~/.local/share/codies-memory` (cloned from GitHub)
- **Global vault:** `~/.memory/`
- **Test project:** `/tmp/test-project/.memory` (deleted after testing)

## What Was Tested

1. Full installation (clone → uv sync → init global → init project)
2. Identity file editing (self.md, user.md, rules.md)
3. Skill installation adapted for OpenCode
4. CLI: `init`, `validate`, `boot`, `status`
5. Python API: `capture()`, `create_record()`, `evaluate_for_promotion()`, `promote_within_project()`, `promote_to_global()`
6. Full lifecycle: inbox capture → promotion to thread → promotion to global → session close → boot verification

---

## What Worked Well

### 1. Installation is fast and clean

`git clone` + `uv sync` resolved in under a second. No dependency conflicts, no platform issues. The `uv`-based workflow is excellent for agent-driven installation.

### 2. Vault structure is well-organized

Both global and project vaults create sensible directory trees out of the box:

```
Global:  identity/ procedural/ reflections/ dreams/ registry/ boot/ threads/ decisions/
Project: inbox/ threads/ decisions/ lessons/ sessions/ project/ boot/
```

The separation of concerns (identity vs. procedural vs. project-scoped) is clear and intuitive.

### 3. Frontmatter record format is solid

Every record gets consistent YAML frontmatter:

```yaml
id: TH-0001
title: The API returns 404 for /v2/status endpoint during testing
type: thread
status: active
trust: working
scope: project
created: '2026-03-31'
updated: '2026-03-31'
probation_until: '2026-04-07'
promoted_from: IN-20260331-f2a2
```

The auto-generated IDs with type prefixes (`IN-`, `LS-`, `TH-`, `SS-`, `LS-G`) are immediately recognizable. The frontmatter is both machine-parseable and human-readable — a hard balance to strike, done well here.

### 4. Promotion pipeline works correctly

- **Inbox → Thread:** Source archived, target created with `promoted_from` reference, 7-day probation set automatically.
- **Project → Global:** Lesson promoted from project vault to `~/.memory/procedural/lessons/` with `LS-G` prefix. Original project record preserved. After deleting the test project, the global record persisted correctly.
- **Trust escalation:** Inbox items start at `speculative`, promoted records move to `working`, operator-confirmed records sit at `confirmed`. The trust ladder makes sense.

### 5. Boot packet assembly is useful

`codies-memory boot --global-vault ~/.memory --project-vault .memory` produces a single coherent output containing:

- Identity context (self, user, rules)
- Global procedural records (promoted lessons)
- Project active records (threads, sessions)

This is exactly what an agent needs at session start. The format is plain markdown, easy to parse.

### 6. Write gate defaults are safe

`profile.yaml` ships with `write_gate_bias: hold` — new captures default to "kept but excluded from retrieval until reinforced." This prevents noise from polluting the boot packet on a fresh install. Good default.

### 7. Project registry works

Initializing a project vault correctly registers it in `~/.memory/registry/projects.yaml` with path, slug, and status. The two-tier vault discovery is functional.

---

## What Didn't Work / Issues

### Issue 1: `status` command is misleading for fresh inbox items

**Severity:** Medium (UX confusion)

`codies-memory status .memory` outputs "Inbox is clean." even when there are active inbox items. This is because `status` only surfaces items aged 7+ days (the aging/stale classification logic). A new user who captures an inbox item and immediately runs `status` will think the capture silently failed.

**Suggestion:** Add an active inbox count to the status output:

```
Inbox: 1 active item(s) (0 aging, 0 stale)
```

Or add a `--all` flag that lists all active items regardless of age.

### Issue 2: Skills don't integrate with OpenCode's skill system

**Severity:** Medium (integration gap, expected)

The skill files (`memory-boot.md`, etc.) use a frontmatter format with `name` and `description`, which aligns with Claude Code's command format and Codex's skill format. However, OpenCode expects:

- A directory per skill, e.g., `skills/codies-memory-memory-boot/SKILL.md`
- A rich `description` field with trigger phrases for auto-matching
- Content structured with OpenCode-specific formatting

The current flat `.md` files in `~/.config/opencode/skills/codies-memory/` work as **manual reference files** (the agent can read them), but they won't auto-trigger or appear in skill suggestions. This is an expected adaptation gap — the doc only covers Claude Code and Codex.

**Suggestion:** Add an OpenCode section to the install doc with the correct directory structure, or provide a conversion script.

### Issue 3: No `list` CLI command

**Severity:** Low-Medium (discoverability)

There is no `codies-memory list --type inbox` or similar command. To enumerate records, you must use the Python API:

```python
from codies_memory.records import list_records
items = list_records(vault, 'inbox', scope='project')
```

This works but requires the agent to construct inline Python, which is fragile. A CLI list command would improve discoverability and reduce the surface area for errors.

### Issue 4: No `capture` CLI subcommand

**Severity:** Medium (agent ergonomics)

All writes go through the Python API. The skill files instruct agents to run multi-line `uv run python -c "..."` blocks. Example from `memory-capture.md`:

```bash
uv run python -c "
from codies_memory.inbox import capture
from pathlib import Path
capture(
    vault=Path('.memory'),
    content='The API returns 404 for /v2/status',
    gate='allow',
    source='session observation',
)
"
```

Any quoting issue, indentation error, or syntax mistake will fail silently or produce confusing errors. A CLI equivalent would be much more robust:

```bash
uv run codies-memory capture --type inbox --content "The API returns 404 for /v2/status" --gate allow --source "session observation"
```

**Suggestion:** Add `codies-memory capture`, `codies-memory create`, and `codies-memory promote` CLI subcommands that wrap the Python API.

### Issue 5: Registry gets stale entries

**Severity:** Low (housekeeping)

When a project directory is deleted, its entry in `~/.memory/registry/projects.yaml` remains as `status: active` forever. There's no deregistration or cleanup mechanism. Over time, the registry will accumulate ghost entries.

**Suggestion:** Add a `codies-memory registry cleanup` command that validates paths and marks or removes stale entries. Or check paths during `boot` and warn about missing projects.

### Issue 6: Token budget declared but not enforced

**Severity:** Low (currently manageable)

The `--budget 4000` flag on the `boot` command is accepted but the boot output is not truncated or warned about when it exceeds the budget. With many records, the boot packet will grow unbounded. For a fresh install this is fine, but as the vault accumulates records, this will become a problem.

**Suggestion:** Count tokens/characters in the assembled packet and either truncate with a warning or log a `[truncated]` marker when budget is exceeded.

### Issue 7: Skills reference `$(date +%Y-%m-%d)` in Python code blocks

**Severity:** Low (minor annoyance)

The `memory-close-session.md` skill includes `title='Session Summary - $(date +%Y-%m-%d)'` inside a Python code block. Shell variable expansion won't work inside `uv run python -c "..."`. The agent has to manually replace this with the actual date, which is fine for a capable agent but adds friction.

---

## OpenCode-Specific Adaptation Notes

For anyone installing codies-memory with OpenCode, here's what worked:

### Skill Installation

```bash
mkdir -p ~/.config/opencode/skills/codies-memory
ln -sf ~/.local/share/codies-memory/skills/memory-boot.md ~/.config/opencode/skills/codies-memory/memory-boot.md
ln -sf ~/.local/share/codies-memory/skills/memory-capture.md ~/.config/opencode/skills/codies-memory/memory-capture.md
ln -sf ~/.local/share/codies-memory/skills/memory-promote.md ~/.config/opencode/skills/codies-memory/memory-promote.md
ln -sf ~/.local/share/codies-memory/skills/memory-close-session.md ~/.config/opencode/skills/codies-memory/memory-close-session.md
```

This places the skills where OpenCode can find them via file reading, but they won't auto-trigger. The agent must proactively read the skill files before use.

### Running Commands

All `codies-memory` commands must be run from the repo directory:

```bash
uv run codies-memory boot --global-vault ~/.memory --project-vault .memory
```

Or with the full path:

```bash
uv run --directory ~/.local/share/codies-memory codies-memory boot --global-vault ~/.memory
```

### Python API Usage

The Python API is the primary write interface. For OpenCode agents, the most reliable pattern is:

```bash
uv run --directory ~/.local/share/codies-memory python -c "
from codies_memory.inbox import capture
from pathlib import Path
capture(vault=Path('.memory'), content='...', gate='allow', source='session')
"
```

---

## Overall Assessment

**Solid foundation, needs CLI ergonomics work.**

The core architecture — two-tier vaults, frontmatter records, promotion pipeline with probation, trust levels, write gates — is well-designed and functional. The full lifecycle (capture → promote → global → boot) works end-to-end without errors.

The primary gap is **agent ergonomics at the CLI level**. Every write operation requires inline Python, which is the most fragile part of the agent-skill interaction. Adding CLI wrappers for `capture`, `create`, `promote`, and `list` would significantly improve reliability and reduce the skill files from "copy-paste Python snippets" to "one-liner CLI commands."

The secondary gap is **OpenCode integration**, which is an expected omission given the doc only covers Claude Code and Codex. The system is compatible — it just needs an install section and ideally skill files structured for OpenCode's auto-triggering mechanism.

The system successfully delivers on its core promise: giving an AI agent persistent memory across sessions, with a sensible trust pipeline and scope model.
