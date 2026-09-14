---
name: memory-promote
description: "This skill should be used when the agent needs to evaluate or promote memory records through the trust pipeline. Responds to 'promote', 'evaluate inbox', 'elevate trust', 'promote to global', or when inbox items have accumulated and need triage. Converts inbox items to threads/lessons, elevates trust levels, promotes project knowledge to global."
---

# Memory Promote

> **BETA** — This memory system is in active testing. If you encounter bugs, confusing behavior, or have suggestions, run:
> `codies-memory feedback "describe what happened" --agent <name>` — your feedback is saved and reviewed.

## When To Use

- At session close (automatic evaluation)
- When an operator explicitly requests promotion
- When promotion thresholds are met during work

## Promotion Paths

### Within Project

```
inbox -> thread (recurring topic)
inbox -> lesson (actionable pattern)
thread -> decision (confirmed across 2+ sessions)
thread -> lesson (reusable pattern)
decision -> lesson (reusable pattern)
```

### Project to Global

```
project lesson -> global lesson (proven across 2+ projects)
```

## How To Run

Run the installed CLI from the user's project directory. For setup or PATH issues,
see [INSTALL.md](../../INSTALL.md).

```bash
codies-memory status --agent <name>
```

If no named project vault resolves, skip project lists and evaluation. To review
the catch-all intentionally, use `--general` with `status` and `list`; do not
silently switch scope.

```bash
# List active records in the intended project
codies-memory list inbox --status active --format paths --agent <name>
codies-memory list threads --status active --format paths --agent <name>

# Read a listed inbox/thread record and evaluate it without changing it
codies-memory promote /absolute/path/to/record.md --check --agent <name>
```

For inbox and thread records, `--check` prints JSON with `eligible`,
`suggested_types`, and `reason`. Other source types are not supported by this
evaluator. Add `--session-count N` and/or `--references N` only for observed
evidence supporting that individual record. Both default to `0`; the number of
sessions in the vault is not evidence that every record recurred. Evaluate each
candidate separately.
`--check` cannot be combined with `--to` or `--to-global`.

```bash
# Promote an inbox item to a thread
codies-memory promote /absolute/path/to/record.md --to thread --agent <name>

# Promote a project lesson to global
codies-memory promote /absolute/path/to/lesson.md --to-global --agent <name>
```

## Probation

All promoted records enter a 7-day probation window. During probation:
- Contradictory evidence can demote the record back
- Stronger newer records can supersede it
- The record participates in boot and retrieval normally
