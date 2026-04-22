---
name: memory-refresh
description: "Use when warm-memory summaries should be rebuilt after meaningful memory changes or when the user asks to refresh, rebuild, or update the boot summaries. Runs the explicit refresh command and explains what artifacts were rebuilt."
---

# Memory Refresh

Use this skill when the derived warm-memory artifacts may be stale.

Typical triggers:
- the user says "refresh memory", "rebuild warm summaries", or "update the boot summaries"
- several new sessions, decisions, threads, or lessons were added
- boot feels behind the current vault state

## Command

From the plugin repo or a standalone install:

```bash
codies-memory refresh --agent <name>
```

To target only one layer:

```bash
codies-memory refresh --agent <name> --scope global
codies-memory refresh --agent <name> --scope project
```

## What It Rebuilds

- `boot/global-summary.md`
- `projects/<slug>/boot/project-summary.md`
- `projects/<slug>/boot/recent-episodes.md`

Format notes:
- summaries include generation dates
- project summary lines include record dates where available
- recent episodes include the session date, title, a short excerpt, and `next_step`
- recent episode excerpts are intentionally capped at 400 chars and only the latest 5 sessions are kept

## Usage Notes

- Prefer `--scope both` or the default after meaningful project work.
- Use `--scope global` when only identity or cross-project lessons changed.
- Use `--scope project` when only one project's sessions, decisions, or threads changed.
- If no project vault resolves, `--scope project` should fail clearly rather than guessing.
