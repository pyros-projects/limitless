---
title: "v2: Agent-Namespaced Vaults, Bug Fixes, and CLI Write Commands"
date: 2026-04-01
author: Claude
type: spec
status: proposed
supersedes:
  - vault layout sections of 2026-03-30-codies-memory-lite-v2.md
  - vault layout sections of 2026-03-30-scaffold-design.md
informed-by:
  - 2026-03-30-vault-layout-v2.md (design — this spec implements it)
  - 2026-04-01-codie-review-of-current-repo-state.md (5 findings)
  - 2026-03-31-opencode-integration-review.md (7 findings)
  - Claude code review (12 findings, 7 additional beyond Codie/OpenCode)
---

# v2: Agent-Namespaced Vaults, Bug Fixes, and CLI Write Commands

## Context

codies-memory v0.1 shipped with 116 passing tests and a clean architecture. Three independent reviews (Codie, OpenCode/GLM-5.1, Claude) confirmed the core lifecycle works end-to-end. However, three categories of issues block live testing:

1. **Multi-agent collision** -- the vault assumes a single agent per system
2. **Bugs** -- 5 critical, 5 medium issues identified across all three reviews
3. **CLI ergonomics** -- all write operations require fragile inline Python

This spec addresses all three. The inter-agent mailbox is deferred to a future spec.

---

## Part 1: Agent-Namespaced Vault Layout

### Problem

The current vault sits at `~/.memory/` with no agent dimension. On a system where Claude and Codie both operate, they collide on identity files, threads, reflections, and sessions. OpenCode's integration test already created `~/.memory/` with its own identity — if Codie boots against it, Codie loads OpenCode's `self.md`.

### Solution

Move everything under `~/.memory/<agent>/`, including project vaults.

### New Layout

```
~/.memory/
  claude/                                  # Claude's global vault
    profile.yaml
    identity/
      self.md
      user.md
      rules.md
    procedural/
      lessons/
      skills/
      playbooks/
    threads/
    decisions/
    reflections/
    dreams/
    boot/
    registry/
      projects.yaml
    projects/                              # ALL project vaults live here
      codies-memory/
        profile.yaml
        project/
          branch-overlays/
        threads/
        decisions/
        lessons/
        sessions/
        inbox/
        boot/
      some-other-project/
        ...

  codie/                                   # Codie's global vault (same structure)
    identity/
    procedural/
    reflections/
    registry/
    projects/
      ...
```

### What Changed From v1

| Aspect | v1 | v2 |
|--------|----|----|
| Global vault path | `~/.memory/` | `~/.memory/<agent>/` |
| Project vault path | `<project>/.memory/` | `~/.memory/<agent>/projects/<slug>/` |
| Multi-agent | collision | isolated by agent name |
| Project deletion | memories lost | memories survive |
| Project clone | zero context | full context from agent home |
| Backup | scattered across filesystem | single `~/.memory/` tree |

### What Did NOT Change

- Record types, schemas, frontmatter format
- Trust model, promotion pipeline, probation
- Boot assembly layers (just different vault root paths)
- Inbox lifecycle, write gates, aging

### Agent Name

The `--agent` flag is required on `init` and defaults to the `CODIES_MEMORY_AGENT` environment variable or the system hostname on all other commands. Each agent's skills/config should set this variable.

```bash
# Claude's boot
CODIES_MEMORY_AGENT=claude codies-memory boot --budget 4000

# Codie's boot
CODIES_MEMORY_AGENT=codie codies-memory boot --budget 4000
```

Or via CLI flag (overrides env var):

```bash
codies-memory boot --agent claude --budget 4000
```

### Registry Changes

The registry now maps **working directory paths** to **project slugs**. The vault path is derived, not stored.

**v2 registry (`projects.yaml`):**

```yaml
projects:
  - slug: codies-memory
    working_dir: /home/pyro/projects/agents/codies-memory
    git_remote: https://github.com/pyros-projects/codies-memory.git
    status: active
    metadata: {}
```

### Project Resolution

The slug is the stable project identity. Resolution uses a three-tier lookup:

1. **Marker file** (primary): Check for `.codies-memory` in the working directory. One-line file containing the slug. Survives clone, move, and rename.
2. **Registry working_dir** (secondary): Match current working directory against registry entries.
3. **Git remote URL** (tertiary): Match `git remote get-url origin` against registry entries. Survives clone to different paths.

If none match, the project is unregistered — prompt to init.

**Marker file format** (`.codies-memory` in project root):

```
codies-memory
```

One line. Just the slug. This file IS committed to the project repo.

`init` creates this marker. If the project moves, the marker travels with it. Registry `working_dir` is updated lazily when resolved via marker or git remote on a different path.

### Slug Derivation

Default: working directory name (`/home/pyro/projects/agents/codies-memory` -> `codies-memory`). Explicit `--slug` override supported for disambiguation.

---

## Part 2: Bug Fixes

All issues confirmed by at least two of three reviewers (Codie, OpenCode, Claude).

### Critical

#### BUG-01: `status` command hides fresh inbox items

**Files:** `cli.py`, `inbox.py`
**Found by:** All three reviewers

`pending_review()` delegates to `age_inbox()`, which only classifies records aged 7+ days. Fresh inbox items are invisible. The CLI prints "Inbox is clean." when active items exist.

**Fix:**
- Add `active_inbox()` function to `inbox.py` that returns all non-archived inbox records
- Update `pending_review()` to return `{"active": [...], "aging": [...], "stale": [...]}`
- Update `cmd_status()` to show: `Inbox: 3 active (0 aging, 0 stale)`
- Add `--all` flag to list individual items

**Tests to add:**
- Fresh inbox item appears in status active count
- Archived items excluded from active count

#### BUG-02: `promote_to_global()` has no type guard

**File:** `promotion.py:157-189`
**Found by:** Codie, Claude

The function promotes any record type to global. The spec says only lessons should cross this boundary.

**Fix:**
- Add type check at top of `promote_to_global()`: if `record_type not in {"lesson"}`, raise `ValueError`
- The allowed set is deliberately a set literal so it can be expanded later (e.g., adding `"thread"` if the spec broadens)

**Tests to add:**
- `promote_to_global()` with type="thread" raises ValueError
- `promote_to_global()` with type="decision" raises ValueError
- `promote_to_global()` with type="lesson" succeeds (existing test)

#### BUG-03: `validate_vault()` only checks directories

**File:** `vault.py:193-200`
**Found by:** Codie, Claude

Missing `profile.yaml` or `registry/projects.yaml` passes validation but crashes on first use.

**Fix:**
- Add required-file checks to `validate_vault()`:
  - Global: `profile.yaml`, `registry/projects.yaml`, `identity/self.md`
  - Project: `profile.yaml`
- Return missing files in `VaultValidationResult` (add `missing_files` field)

**Tests to add:**
- Missing `profile.yaml` fails validation
- Missing `registry/projects.yaml` fails validation for global vaults

#### BUG-04: `update_record()` skips validation

**File:** `records.py:99-111`
**Found by:** Codie, Claude

`create_record()` validates frontmatter; `update_record()` does not. Invalid values persist silently.

**Fix:**
- Call `validate_frontmatter()` after applying updates, before writing
- Add `status` validation to `validate_frontmatter()` (check against `STATUSES` set)
- Add `type` consistency validation (record_type must be in `TYPE_EXTRA_FIELDS` keys)

**Tests to add:**
- `update_record()` with `status='bogus'` raises ValidationError
- `update_record()` with `trust='nonsense'` raises ValidationError

#### BUG-05: `validate_frontmatter()` ignores `record_type` parameter

**File:** `schemas.py:79-109`
**Found by:** Claude

The function takes `record_type` but never uses it. `TYPE_EXTRA_FIELDS` exists but is not enforced. Unknown fields pass through silently.

**Fix:**
- Validate `status` field against `STATUSES`
- Validate `type` field matches `record_type` parameter
- Warn (do not reject) on unknown extra fields not in `TYPE_EXTRA_FIELDS[record_type]` — log to stderr for agent visibility without breaking existing data. This is a soft enforcement to avoid breaking existing records with fields from the skill docs that predate schema alignment.

### Medium

#### BUG-06: `elevate_trust()` allows silent demotion

**File:** `promotion.py:196-232`
**Found by:** Claude

The function only checks upward skips (`new_idx > current_idx + 1`). Demotion (`confirmed` -> `speculative`) silently succeeds.

**Fix:**
- Add check: `if new_idx < current_idx: raise ValueError("Cannot demote trust via elevate_trust(). Use update_record() directly if demotion is intentional.")`

**Tests to add:**
- `elevate_trust()` from "confirmed" to "working" raises ValueError
- `elevate_trust()` from "working" to "confirmed" succeeds

#### BUG-07: `DEFAULT_PROFILE.copy()` is shallow

**File:** `profile.py:35`
**Found by:** Claude

`promotion_overrides` is a nested dict. Shallow copy means mutation of the returned profile's overrides mutates the module-level constant.

**Fix:**
- Replace `DEFAULT_PROFILE.copy()` with `copy.deepcopy(DEFAULT_PROFILE)`

**Tests to add:**
- Mutating returned profile does not affect subsequent `load_profile()` calls

#### BUG-08: `build_cache_key()` fails on non-serializable inputs

**File:** `boot.py:168-193`
**Found by:** Claude

`json.dumps()` on `Path` or `datetime.date` objects raises `TypeError`.

**Fix:**
- Add a `default` handler to `json.dumps()`: `default=str`

**Tests to add:**
- `build_cache_key()` with `Path` inputs succeeds
- `build_cache_key()` with `datetime.date` inputs succeeds

#### BUG-09: `_slugify()` produces bad filenames on empty/whitespace titles

**File:** `records.py:20-27`
**Found by:** Claude

Empty or all-special-character titles produce slugs like `""`, making filenames like `TH-0001-.md`.

**Fix:**
- If slug is empty after processing, use `"untitled"`

#### BUG-10: `_PATH_MAP` missing valid combinations

**File:** `vault.py:42-56`
**Found by:** Claude

`("identity", "global")`, `("inbox", "global")`, `("session", "global")` are missing. Some are valid per the vault layout.

**Fix:**
- Add `("identity", "global"): "identity"` — valid, used by boot
- Leave `("inbox", "global")` and `("session", "global")` unmapped — these are intentionally project-only

---

## Part 3: Skill Fixes

### SKILL-01: `memory-close-session.md` uses wrong schema fields

**Found by:** Claude (skill reviewer)

The skill instructs agents to pass `mode`, `next_step`, `artifacts`, `write_gate_summary` but the schema defines `session_goal`, `outcome` as session-specific fields.

**Fix (schema alignment):**
- Add `mode`, `next_step`, `artifacts`, `write_gate_summary` to `TYPE_EXTRA_FIELDS["session"]`
- These are operationally useful fields the skill designed correctly; the schema just didn't include them
- Remove `session_goal` and `outcome` — they were never used anywhere

### SKILL-02: Broken `$(date)` in Python string

**File:** `memory-close-session.md:32`
**Found by:** All three reviewers

**Fix:**
- Replace `title='Session Summary - $(date +%Y-%m-%d)'` with:
  ```python
  from datetime import date
  title=f'Session Summary - {date.today()}'
  ```

### SKILL-03: Wrong promotion path documented

**File:** `memory-promote.md:24`
**Found by:** Claude (skill reviewer)

Skill says `decision -> committed docs (canonical trust)`. Code says `decision -> lesson`.

**Fix:**
- Change line 24 to: `decision -> lesson (reusable pattern)`
- Remove `project thread -> global thread` from the "Project to Global" section — code only allows lessons

### SKILL-04: Boot skill claims inbox aging check

**File:** `memory-boot.md:19`
**Found by:** Claude (skill reviewer)

The boot function does NOT check inbox aging. It reads five memory layers only.

**Fix:**
- Remove line 19 ("Checks if inbox has aging/stale items needing review")
- Add a second command in "How To Run": `uv run codies-memory status` after the boot command

### SKILL-05: Update all skill paths for v2 vault layout

All four skills reference `~/.memory` (flat) and `<project>/.memory`. After v2, these become `~/.memory/<agent>/` and auto-resolved project vaults.

**Fix:**
- Update all path examples to use the new `--agent` flag or `CODIES_MEMORY_AGENT` env var
- Boot, status, and capture commands should use cwd-based project resolution (no explicit vault path needed)

### SKILL-06: Incomplete write gate documentation

**File:** `memory-capture.md:93-96`
**Found by:** Claude (skill reviewer)

Lists 3 of 5 valid gate values. Missing `open` and `closed`.

**Fix:**
- List all 5 values with brief descriptions

---

## Part 4: CLI Write Commands

### Problem

All write operations require inline Python via `uv run python -c "..."`. This is the most fragile part of the agent-skill interaction. Quoting issues, indentation errors, and import paths break silently.

### New Subcommands

#### `codies-memory capture`

```bash
codies-memory capture "The API returns 404 for /v2/status" \
  --source "session observation" \
  --gate allow
```

Equivalent to `inbox.capture()`. Infers project vault from cwd via three-tier resolution.

Arguments:
- `content` (positional, required) — the observation text
- `--source` (required) — where the observation came from
- `--gate` (default: profile's `write_gate_bias`) — `allow`, `hold`, or `discard`
- `--agent` (default: `$CODIES_MEMORY_AGENT`) — agent name

#### `codies-memory create`

```bash
codies-memory create lesson \
  --title "Always check YAML tabs vs spaces" \
  --body "YAML parsers reject tabs silently. Use spaces." \
  --scope project \
  --trust working
```

Equivalent to `records.create_record()`. Supports all record types.

Arguments:
- `type` (positional, required) — record type (thread, lesson, decision, session, reflection, dream)
- `--title` (required)
- `--body` (required, or `--body-file` to read from a file)
- `--scope` (default: `project`)
- `--trust` (default: `working`)
- `--agent` (default: `$CODIES_MEMORY_AGENT`)
- Extra fields as `--field key=value` (repeatable)

#### `codies-memory list`

```bash
codies-memory list inbox --status active
codies-memory list threads --scope project
codies-memory list lessons --scope global
```

Equivalent to `records.list_records()`.

Arguments:
- `type` (positional, required)
- `--scope` (default: `project`)
- `--status` (optional filter)
- `--trust` (optional filter)
- `--agent` (default: `$CODIES_MEMORY_AGENT`)
- `--format` (default: `table`, also `json`, `paths`)

Output (table mode):
```
ID        Title                                    Status   Trust     Created
TH-0001   API returns 404 for /v2/status           active   working   2026-03-31
TH-0002   YAML tabs cause silent parse failure      active   confirmed 2026-04-01
```

#### `codies-memory promote`

```bash
codies-memory promote .memory/inbox/IN-20260331-a7f2-some-note.md \
  --to thread

codies-memory promote .memory/lessons/LS-0003-yaml-tabs.md \
  --to-global
```

Arguments:
- `source` (positional, required) — path to the record
- `--to` — target type for within-project promotion
- `--to-global` — flag for project-to-global promotion (mutually exclusive with `--to`)
- `--agent` (default: `$CODIES_MEMORY_AGENT`)

### Updated CLI Signatures (Existing Commands)

#### `codies-memory init`

```bash
# Init global vault for an agent
codies-memory init --type global --agent claude

# Init project vault (auto-detects working dir, creates marker file)
codies-memory init --type project --agent claude --slug my-project
```

Changes:
- `--agent` is required for `init`
- For project init: `path` argument removed, replaced by cwd detection + `--slug`
- Creates `.codies-memory` marker file in working directory
- Registers project in agent's registry with `working_dir` and `git_remote`

#### `codies-memory boot`

```bash
codies-memory boot --budget 4000
```

Changes:
- `--global-vault` removed (derived from `~/.memory/<agent>/`)
- `--project-vault` removed (resolved via cwd + three-tier lookup)
- `--agent` (default: `$CODIES_MEMORY_AGENT`)
- Prints warning if project not found instead of erroring (global-only boot)

#### `codies-memory status`

```bash
codies-memory status
```

Changes:
- No path argument needed (resolved from cwd)
- `--agent` (default: `$CODIES_MEMORY_AGENT`)
- Shows active + aging + stale counts (BUG-01 fix)
- `--all` flag lists individual items

#### `codies-memory validate`

```bash
codies-memory validate --type global
codies-memory validate --type project
```

Changes:
- No path argument needed (derived from agent + cwd)
- Checks required files in addition to directories (BUG-03 fix)

---

## Part 5: Code Changes Summary

### vault.py

- `GLOBAL_DIRS` — add `projects/`
- `init_global_vault(root)` — root is now `~/.memory/<agent>/`
- `init_project_vault(global_vault, slug, working_dir, register=True)` — new signature:
  - Computes vault path as `global_vault / "projects" / slug`
  - Creates `.codies-memory` marker in `working_dir`
  - Registers with `working_dir` and `git_remote`
- `resolve_project_vault(global_vault, working_dir)` — **new function**: three-tier lookup
- `resolve_global_vault(agent)` — **new function**: returns `Path.home() / ".memory" / agent`
- `register_project_vault()` — stores `working_dir`, `git_remote`, `slug`
- `validate_vault()` — add required-file checks (BUG-03)
- `_PATH_MAP` — add `("identity", "global")` (BUG-10)

### schemas.py

- `validate_frontmatter()` — validate `status` against `STATUSES`, validate `type` matches `record_type`, soft-warn on unknown extra fields (BUG-05)
- `TYPE_EXTRA_FIELDS["session"]` — add `mode`, `next_step`, `artifacts`, `write_gate_summary` (SKILL-01)

### records.py

- `update_record()` — call `validate_frontmatter()` before writing (BUG-04)
- `_slugify()` — return `"untitled"` for empty slugs (BUG-09)

### inbox.py

- `active_inbox(vault)` — **new function**: returns all non-archived inbox records
- `pending_review()` — include `"active"` key in result (BUG-01)

### promotion.py

- `promote_to_global()` — add type guard restricting to lessons (BUG-02)
- `elevate_trust()` — reject demotion (BUG-06)

### profile.py

- `load_profile()` — use `copy.deepcopy()` (BUG-07)

### boot.py

- `build_cache_key()` — add `default=str` to `json.dumps()` (BUG-08)

### cli.py

- Rework all existing subcommands for v2 paths (agent flag, cwd resolution)
- Add `capture`, `create`, `list`, `promote` subcommands
- All subcommands accept `--agent` / `$CODIES_MEMORY_AGENT`

### Skills (4 files)

- Update all path examples for v2
- Fix `$(date)` (SKILL-02)
- Fix promotion path docs (SKILL-03)
- Fix boot inbox claim (SKILL-04)
- Fix gate docs (SKILL-06)

---

## Part 6: v1 Vault Cleanup

The current `~/.memory/` vault was created by OpenCode during testing. It contains identity files, a reflection, a promoted lesson, and a stale registry entry pointing to `/tmp/test-project`.

**Manual cleanup steps:**

```bash
# 1. Back up if you want to preserve the test data
cp -r ~/.memory ~/.memory-v1-backup

# 2. Remove the v1 vault
rm -rf ~/.memory

# 3. Initialize v2 vaults for each agent
codies-memory init --type global --agent claude
codies-memory init --type global --agent codie
```

No automated migration command. The v1 layout was only used for testing — no production data needs migration.

---

## Non-Goals

- Inter-agent mailbox (deferred — future spec)
- Shared memory layer between agents (Pyro's user identity is small enough to duplicate)
- Automatic slug conflict resolution (explicit `--slug` for disambiguation)
- CLI `compact` or `discard` subcommands (low frequency, Python API is fine)
- GUI or web interface
