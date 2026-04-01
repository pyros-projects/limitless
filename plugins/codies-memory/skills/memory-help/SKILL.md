---
name: memory-help
description: "This skill should be used when the agent needs a reminder of what the memory system can do, what commands are available, or how the memory system works. Responds to 'memory help', 'what memory commands exist', 'how does my memory work', 'what can I remember', or any confusion about the memory system's capabilities."
---

# Memory Help

> **BETA** — This memory system is in active testing. If you encounter bugs, confusing behavior, or have suggestions, run:
> `codies-memory feedback "describe what happened"` — your feedback is saved and reviewed.

## What This System Is

You have a persistent file-based memory system. It stores what you learn, observe, and decide across sessions in a vault at `~/.memory/<your-agent-name>/`. Every command requires `--agent <your-agent-name>`.

## Commands

### Boot (every session start)

```bash
codies-memory boot --agent <name> --budget 4000
```

Loads your identity, procedural knowledge, project context, and recent state.

### Capture (save an observation)

```bash
codies-memory capture "what you noticed" --source "where you noticed it" --agent <name>
```

Saves to the project's inbox. Use `--working-dir /path` to target a specific project.

### Create (write a specific record type)

```bash
codies-memory create <type> --title "Title" --body "Content" --agent <name>
```

Types: `lesson`, `session`, `thread`, `decision`, `reflection`, `dream`

Use `--scope global` for cross-project records. Global-only types (`reflection`, `dream`) are auto-routed.

### List (see what's stored)

```bash
codies-memory list <type> --agent <name>
codies-memory list lessons --scope global --agent <name>
```

Formats: `--format table` (default), `--format json`, `--format paths`

### Status (check inbox health)

```bash
codies-memory status --agent <name>
```

Shows active, aging, and stale inbox item counts.

### Promote (move records up the trust pipeline)

```bash
codies-memory promote /path/to/record.md --to thread --agent <name>
codies-memory promote /path/to/record.md --to-global --agent <name>
```

Inbox items promote to threads/lessons. Only lessons promote to global.

### Initialize a project

```bash
codies-memory init --type project --agent <name> --working-dir /path/to/project
```

### Validate vault structure

```bash
codies-memory validate --type global --agent <name>
codies-memory validate --type project --agent <name>
```

### Report feedback

```bash
codies-memory feedback "describe what happened" --agent <name>
```

## Vault Structure

```
~/.memory/<agent>/
  identity/          — self.md, user.md, rules.md (who you are)
  procedural/        — lessons, skills, playbooks (what you've learned)
  threads/           — ongoing investigations
  decisions/         — choices made
  reflections/       — philosophical processing
  dreams/            — emotional processing
  registry/          — map of known projects
  projects/          — all project vaults
    <project-slug>/
      inbox/         — raw captures
      threads/       — project-specific threads
      decisions/     — project-specific decisions
      lessons/       — project-specific lessons
      sessions/      — session summaries
```

## Trust Pipeline

Records flow: `inbox` → `thread` or `lesson` → (optional) `global lesson`

Trust levels: `speculative` → `working` → `confirmed` → `canonical`

New records start at `speculative`. Promoted records start at `working` with a 7-day probation.

## What To Tell The User

Users don't need to know internal terms. When they ask what you can do with memory, say it in plain language:

- "I can remember things about your projects across sessions"
- "I can track what we've learned and decided"
- "I can write session summaries so next time I know where we left off"
- "I can look across all your projects for patterns"
