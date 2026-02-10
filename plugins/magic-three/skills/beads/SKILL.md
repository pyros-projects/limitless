---
name: beads
description: Git-backed task graph and agent memory using Beads (bd CLI). Use for dependency-aware task management, long-horizon projects, and session-resilient development.
homepage: https://github.com/steveyegge/beads
read_when:
  - You need to track tasks with dependencies across sessions.
  - You want to find the next unblocked task to work on.
  - A project has more than a handful of tasks that need ordering.
  - You're starting a feature and need to plan work as a DAG.
  - You are resuming after a break or context compaction.
  - Someone says "continue", "where were we", or "what's next".
metadata:
  openclaw:
    emoji: "📿"
---

# Beads — Agent Memory & Task Graph

Beads (`bd`) is a distributed, git-backed graph issue tracker designed for AI coding agents. It replaces flat task lists with a dependency-aware graph, enabling long-horizon development without losing context across sessions.

**Author:** Steve Yegge | **License:** MIT

## When to Use Beads

| Situation | Use Beads? |
|-----------|-----------|
| <5 tasks, single session, no dependencies | **No** — a simple checklist is enough |
| 5-10 tasks, some ordering matters | **Maybe** — use if spanning multiple sessions |
| 10+ tasks, cross-task dependencies, multi-session | **Yes** — Beads prevents chaos |
| Resuming work after a break or context compaction | **Yes** — `bd ready` is instant context recovery |
| Pairing with OpenSpec for structured planning | **Yes** — Beads drives execution after OpenSpec plans |

## Why Beads?

- **Session-resilient** — `bd ready` instantly tells you where you left off after a break
- **Dependency graph** — Tasks form a DAG; only unblocked work surfaces
- **Git as database** — Issues stored as JSONL in `.beads/`, versioned like code
- **Zero conflict** — Hash-based IDs prevent collisions across branches and agents
- **Compaction-safe** — State survives context window compaction

## Installation

```bash
# macOS
brew install beads

# All platforms (npm)
npm install -g @beads/bd

# All platforms (Go)
go install github.com/steveyegge/beads/cmd/bd@latest

# All platforms (install script)
curl -fsSL https://raw.githubusercontent.com/steveyegge/beads/main/scripts/install.sh | bash
```

Verify: `bd --version`

## Project Setup

```bash
cd /path/to/your/project
bd init
```

Creates `.beads/` in your project:
- `issues.jsonl` — the task database (**commit this**)
- `beads.db` — local SQLite cache (**do not commit** — auto-ignored)

## Session Start Protocol

**Every session, before doing anything else:**

```bash
bd ready
```

This is the single most important command. It shows all tasks with no open blockers, sorted by priority. If you are resuming work, this tells you exactly where to pick up.

If `bd ready` returns nothing but you expect work:

```bash
bd list                   # Are there open tasks at all?
bd list --status blocked  # Is everything blocked?
bd dep tree <epic-id>     # Visualize — look for circular deps
```

## Essential Commands

### Creating Tasks

```bash
bd create "Implement auth middleware" -p 1
bd create "Auth System" -t epic -p 0                     # Epic (parent for subtasks)
bd create "Add rate limiting" -p 2 -n "Use token bucket" # With notes
bd create "Subtask title" -p 1 --parent bd-a3f8          # Child of epic
```

### Priority Levels

| Priority | Meaning |
|----------|---------|
| `P0` | Critical / blocking |
| `P1` | High priority |
| `P2` | Normal |
| `P3` | Low / nice to have |

### Dependencies

```bash
bd dep add <child-id> <parent-id>                # B depends on A
bd dep add bd-a1b2 bd-f3g4 --type blocks         # Explicit type
bd dep remove <child-id> <parent-id>             # Unwire
bd dep tree <id>                                 # Visualize DAG
```

### Finding Work

```bash
bd ready                    # THE key command — unblocked tasks, sorted by priority
bd list                     # All open tasks
bd show <id>                # Task details + audit trail
bd search "<partial>"       # Find task by title substring
```

### Working on Tasks

```bash
bd update <id> --status in_progress     # Claim a task
bd update <id> --notes "Progress: ..."  # Record state for future sessions
bd close <id> --reason "Completed"      # Close when done
```

### Writing Good Notes

Notes are your lifeline after compaction. Write them as if explaining to a future agent with zero conversation context:

```
COMPLETED: Specific deliverables (e.g. "JWT refresh endpoint + rate limiting middleware")
IN PROGRESS: Current state + next immediate step
BLOCKERS: What is preventing progress
KEY DECISIONS: Important context or trade-offs made
```

### Hierarchical IDs (Epics)

```
Epic:     bd-a3f8
Tasks:    bd-a3f8.1, bd-a3f8.2, bd-a3f8.3
Subtasks: bd-a3f8.1.1, bd-a3f8.1.2
```

### JSON Output

All commands support `--json` for structured output. Always use `--json` when parsing output programmatically.

```bash
bd ready --json
bd list --json
bd show <id> --json
```

## Solo Workflow (Single Agent + Human)

### The Loop

```
1. bd ready                              # What is unblocked?
2. Pick the highest priority task
3. bd update <id> --status in_progress   # Claim it
4. Implement the task
5. bd close <id> --reason "..."          # Close with meaningful reason
6. git commit -m "... (bd-XXXX)"         # Include Beads ID in commit
7. Go to 1
```

### Concrete Example

```bash
# Create epic + tasks
bd create "Add search feature" -t epic -p 0            # bd-m3n4
bd create "Set up search index" -p 1 --parent bd-m3n4   # bd-m3n4.1
bd create "Build search API endpoint" -p 1 --parent bd-m3n4  # bd-m3n4.2
bd create "Create search UI component" -p 1 --parent bd-m3n4 # bd-m3n4.3
bd create "Add search tests" -p 1 --parent bd-m3n4      # bd-m3n4.4

# Wire dependencies
bd dep add bd-m3n4.2 bd-m3n4.1   # API needs index
bd dep add bd-m3n4.3 bd-m3n4.2   # UI needs API
bd dep add bd-m3n4.4 bd-m3n4.3   # Tests need UI

# Execute
bd ready                          # --> bd-m3n4.1
# ... implement ...
bd close bd-m3n4.1 --reason "Elasticsearch index configured"
git commit -m "Set up search index (bd-m3n4.1)"

bd ready                          # --> bd-m3n4.2 (now unblocked)
```

## Combining Beads with OpenSpec

Use both when a feature needs structured planning AND dependency-aware execution. OpenSpec owns **what to build** (specs, proposals, design). Beads owns **what to do next** (dependency graph, execution state).

### The Combined Process

```
Phase 1: Planning (OpenSpec leads)
  /opsx:new <feature>
  /opsx:ff --> produces proposal.md, specs/, design.md, tasks.md
  Human reviews and approves artifacts

Phase 2: Task Import (Bridge to Beads)
  Parse tasks.md --> create Beads epic + tasks with dependencies
  Stamp Beads IDs back into tasks.md

Phase 3: Execution (Beads drives)
  bd ready --> pick task --> implement --> bd close --> check off tasks.md
  Repeat until all tasks done

Phase 4: Finalize (OpenSpec closes)
  /opsx:verify --> validate implementation matches specs
  /opsx:archive --> merge deltas, archive the change
```

### Task Import Procedure

When importing tasks from OpenSpec's tasks.md into Beads:

```bash
# 1. Create the epic, referencing the OpenSpec change name
bd create "Epic: <feature> (openspec: <change-name>)" -t epic -p 0
# Returns: bd-XXXX

# 2. Create each task as a child of the epic
# Parse tasks.md top to bottom, one bd create per checkbox item
bd create "<task title>" -p <priority> --parent bd-XXXX

# 3. Wire dependencies based on task relationships
bd dep add <child-id> <parent-id>

# 4. Stamp Beads IDs back into tasks.md:
#    BEFORE: - [ ] Set up auth schema
#    AFTER:  - [ ] (bd-x1y2.1) Set up auth schema
```

**Dependency inference rules (apply in order):**
1. Schema/migration tasks block everything that queries those tables
2. API endpoint tasks block UI tasks that call them
3. Config/setup tasks block tasks that use that config
4. Implementation tasks block their corresponding test tasks
5. If two tasks modify the same file, make them sequential

### Keeping Both in Sync

- **Close in BOTH:** `bd close <id>` and check off `[x]` in `tasks.md`
- **New tasks mid-flight:** Add to both `tasks.md` and Beads, wire dependencies
- **`bd ready` is canonical** for execution order, not the tasks.md list order
- **`tasks.md` is canonical** for scope and requirements

## Git Integration

### Commit Convention

Always include the Beads ID in commit messages:

```
feat: implement JWT middleware (bd-x1y2.2)
fix: correct token expiry logic (bd-x1y2.2)
```

This enables `bd doctor` to detect orphaned issues and provides traceability.

### Sync

```bash
bd sync              # Sync database <-> JSONL, optional commit
git pull --rebase    # Beads auto-imports from JSONL if newer
```

### Branching

Beads tracks across branches via JSONL merge. Hash-based IDs prevent conflicts even with parallel branches. After merge, `bd sync` reconciles state automatically.

## Error Recovery

### `bd ready` returns nothing but work remains

```bash
bd list                       # Check if tasks exist
bd list --status blocked      # Check if everything is blocked
bd dep tree <epic-id>         # Visualize — look for circular deps or tasks blocked by closed items
```

### Wrong dependencies were created

```bash
bd dep remove <child> <parent>   # Unwire incorrect edge
bd dep add <child> <parent>      # Wire correct edge
bd ready                          # Verify new ordering
```

### Task was closed prematurely

```bash
bd update <id> --status open     # Reopen the task
bd update <id> --notes "Reopened: <reason>"
```

### Beads and tasks.md are out of sync

1. Run `bd list --json` and compare against tasks.md checkboxes
2. Close any Beads tasks that are checked off in tasks.md but still open
3. Add any tasks that exist in tasks.md but not in Beads
4. Source of truth for scope: tasks.md. Source of truth for execution state: Beads.

### Database issues

```bash
bd doctor                                    # Health check
bd import -i .beads/issues.jsonl             # Rebuild cache from JSONL
```

## Landing the Plane (End of Session)

Before ending a session, always:

1. Update notes on any in-progress task with current state
2. Close all completed tasks with meaningful reasons
3. Run `bd sync`
4. `git add .beads/ && git commit -m "beads: sync state"`
5. Report summary: what was done, what `bd ready` shows next

This ensures the next session (or the next agent) can pick up instantly.

## Standard Reporting Contract (Mandatory)

At the end of every Beads-driven iteration, report status using this exact section structure:

```markdown
Completed
- <major result 1>
- <major result 2>
- Key task status updates:
  - <issue-id> -> in_progress/closed (reason)
  - <issue-id> -> in_progress/closed (reason)

Validation + Git
- <validation command> passed/failed.  # tests/lint/build as applicable
- bd sync completed.
- Commit pushed: <hash>.               # if committed
- Branch is clean and synced with origin/<branch>.  # if pushed

Progress stats
- Active implementation change: <name> = <done>/<total> done (<left> left)
- New planning change: <name> = <done>/<total> done (<left> left)   # include when relevant
- Project-wide (all changes incl. archive): <done>/<total> done (<left> left)
- Current ready Beads tasks: <id>, <id>, <id>
```

Rules:
- Always include `Completed`, `Validation + Git`, and `Progress stats` headings in that order.
- Include Beads issue IDs for every task status transition made this iteration.
- Never claim `bd sync` or push status unless command output confirms success.
- If a step is not applicable, write `N/A` explicitly (do not omit the line).
- Keep the report compact and checklist-like for quick handoff scans.

Metric definitions:
- `Active implementation change`: current executing OpenSpec change tied to the active Beads epic.
- `New planning change`: a newly created OpenSpec change in the same session, if any.
- `Project-wide`: all checkbox tasks under `openspec/changes/**/tasks.md` (including archive).
- `Current ready Beads tasks`: from `bd ready`, top ready task IDs in priority order.

## Links

- **Repo:** <https://github.com/steveyegge/beads>
- **Install guide:** <https://github.com/steveyegge/beads/blob/main/docs/INSTALLING.md>
- **Agent instructions:** <https://github.com/steveyegge/beads/blob/main/AGENT_INSTRUCTIONS.md>
- **MCP Server:** `pip install beads-mcp` (for environments without CLI access)
