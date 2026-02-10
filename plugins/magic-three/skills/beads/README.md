# Beads — Agent Memory & Task Graph

> **Skill file:** [`SKILL.md`](SKILL.md) — load this into your AI coding agent

## What is Beads?

[Beads](https://github.com/steveyegge/beads) is a git-backed graph issue tracker designed specifically for AI coding agents. Created by Steve Yegge, it stores tasks as a dependency graph (DAG) so agents always know what's unblocked and ready to work on.

**Core idea:** Replace flat TODO lists with a dependency-aware graph that survives session restarts.

## When to Use It

| Situation | Use Beads? |
|-----------|-----------|
| <5 tasks, single session | **No** — a simple checklist is enough |
| 5-10 tasks, some ordering | **Maybe** — use if spanning multiple sessions |
| 10+ tasks, dependencies, multi-session | **Yes** — Beads prevents chaos |
| Resuming after a break | **Yes** — `bd ready` is instant context recovery |
| Pairing with OpenSpec | **Yes** — Beads drives execution after OpenSpec plans |

## Why Use It?

- **Session resilience** — `bd ready` instantly tells you where you left off, even in a fresh context window
- **Dependency ordering** — Can't accidentally skip ahead; the graph enforces correct order
- **Git-native** — Tasks stored as JSONL, versioned and merged like code
- **Zero conflict** — Hash-based IDs prevent collisions across branches
- **Compaction-safe** — State survives context window compaction

## Quick Start

```bash
# Install (macOS)
brew install beads

# Install (any platform)
npm install -g @beads/bd

# Initialize in your project
cd your-project
bd init

# Create tasks
bd create "Set up database schema" -p 1            # bd-a1b2
bd create "Build API endpoints" -p 1               # bd-a1b3
bd create "Add tests" -p 1                         # bd-a1b4

# Add dependencies
bd dep add bd-a1b3 bd-a1b2    # API needs schema first
bd dep add bd-a1b4 bd-a1b3    # Tests need API first

# Find what's ready to work on
bd ready   # → bd-a1b2 (Set up database schema)

# Work on it, then close
bd close bd-a1b2 --reason "Schema migration created"
git commit -m "Set up database schema (bd-a1b2)"

bd ready   # → bd-a1b3 (Build API endpoints) — now unblocked!
```

## The Workflow

```
bd create    Create tasks with priorities
     ↓
bd dep add   Wire up dependencies between tasks
     ↓
bd ready     See what's unblocked → pick a task
     ↓
  [implement] Do the work
     ↓
bd close     Mark done with a reason
     ↓
git commit   Include Beads ID in commit message
     ↓
  [repeat]   bd ready → next unblocked task
```

## Key Concepts

### Session Start Protocol

**Every session, before doing anything else:** run `bd ready`. This is the single most important command — it shows all unblocked tasks sorted by priority and tells you exactly where to pick up.

### Dependency Graph (DAG)

Tasks aren't a flat list — they form a directed acyclic graph. `bd ready` computes which tasks have no open blockers, so you always work on the right thing next.

### Hierarchical IDs

Epics organize related tasks:
```
bd-a3f8        (Epic: Auth System)
bd-a3f8.1      (Task: Design schema)
bd-a3f8.2      (Task: Implement JWT)
bd-a3f8.1.1    (Subtask: User table)
```

### Writing Good Notes

Notes are your lifeline after compaction. Write them as if explaining to a future agent with zero context: what was COMPLETED, what's IN PROGRESS, any BLOCKERS, and KEY DECISIONS made.

## Combining with OpenSpec

For structured feature development, pair Beads with [OpenSpec](../openspec/). OpenSpec handles *what to build* (specs, design, proposals); Beads handles *what to do next* (task dependencies, execution tracking).

See the [SKILL.md](SKILL.md) for the detailed combined workflow, task import procedure, and dependency inference rules.

## Links

- **Repo:** https://github.com/steveyegge/beads
- **Author:** Steve Yegge
- **Platforms:** macOS, Linux, Windows, FreeBSD
- **Install methods:** Homebrew, npm, Go, install script
