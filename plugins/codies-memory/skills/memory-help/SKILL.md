---
name: memory-help
description: "This skill should be used when the agent needs a reminder of what the memory system can do, what commands are available, or how the memory system works. Responds to 'memory help', 'what memory commands exist', 'how does my memory work', 'what can I remember', or any confusion about the memory system's capabilities. Also invoked by memory-boot after first boot to teach the agent the system."
---

# Memory Help

> **BETA** — This memory system is in active testing. If you encounter bugs, confusing behavior, or have suggestions, run:
> `codies-memory feedback "describe what happened"` — your feedback is saved and reviewed.

## What This System Is

You have a persistent file-based memory system. It stores what you learn, observe, and decide across sessions. Your vault lives at `~/.memory/<your-agent-name>/`. Every command requires `--agent <your-agent-name>`.

There are two scopes:
- **Global** — knowledge that applies across all projects (your identity, cross-project lessons, reflections)
- **Project** — knowledge specific to one project (observations, decisions, session summaries)

There are also two practical operating modes:
- **Standalone mode** — works with the canonical vault only
- **Full mode** — recommended: canonical vault plus QMD retrieval

QMD is recommended when available because recall becomes faster, more token-efficient,
and semantic across multiple memory stores. If the user wants that full mode and does
not have QMD yet, offer to help install it.

---

## Concepts

Read this section carefully. These terms have specific meanings in this system.

### Record Types

| Type | What it is | Scope | When to create |
|------|-----------|-------|----------------|
| **inbox** | A raw observation or note. Unprocessed. | project | When you notice something worth remembering but haven't decided what it means yet. Use `capture`. |
| **thread** | An ongoing investigation or topic you're tracking across sessions. | project or global | When an inbox item keeps coming up, or you're tracking something over time. Promote from inbox. |
| **lesson** | A reusable pattern or rule you've learned. "When X, do Y." | project or global | When you've learned something actionable that applies beyond the current moment. Promote from inbox or thread. |
| **decision** | A choice that was made with rationale. | project or global | When a significant decision happens and you want to remember why. |
| **session** | A summary of one work session. | project | At the end of every session. Captures what happened, what was decided, what's next. |
| **reflection** | Philosophical or meta-level thinking. | global only | When you want to process what something meant, not just what happened. |
| **dream** | Emotional/subconscious processing. | global only | Optional. For agents that use creative processing. |

### The Inbox

The inbox is where raw observations land. It is the entry point for most memory.

- New captures go to `inbox/` with gate `hold` (kept but not yet in boot packet) or `allow` (immediately visible)
- Items older than 7 days are flagged as **aging** — you should promote, compact, or discard them
- Items older than 14 days are **stale** — they need immediate attention
- The `status` command shows these counts

### Promotion

Promotion moves a record from a lower type to a higher type. Think of it as refining raw observations into structured knowledge.

**Within a project:**
```
inbox → thread    (this keeps coming up)
inbox → lesson    (I learned something actionable)
inbox → decision  (a choice was made)
thread → lesson   (the investigation yielded a reusable pattern)
thread → decision (the investigation led to a choice)
decision → lesson (the decision revealed a reusable pattern)
```

**Project to global:**
```
project lesson → global lesson   (this applies across all my projects)
```

Only lessons can be promoted to global. This is intentional — global memory should contain reusable patterns, not project-specific threads or decisions.

When a record is promoted, the source is archived and the new record gets a 7-day probation period.

### Trust Levels

Every record has a trust level that indicates how established it is:

| Level | Meaning |
|-------|---------|
| `speculative` | Just captured. Might be noise. |
| `working` | Promoted or reinforced. Probably real. |
| `confirmed` | Validated across multiple sessions. Reliable. |
| `canonical` | Foundational. Change with extreme care. |

Trust is elevated one step at a time via `promote`. You cannot skip levels.

### Write Gates

When capturing to inbox, a gate controls visibility:

| Gate | Effect |
|------|--------|
| `allow` | Record is active and appears in boot/retrieval immediately |
| `hold` | Record is kept but excluded from boot until promoted (default) |
| `discard` | Record is archived immediately (logged but not used) |
| `open` | Same as allow |
| `closed` | Same as hold |

### Identity Files

Your identity lives at `~/.memory/<name>/identity/`:

- `self.md` — who you are, your capabilities, your personality
- `user.md` — who your human is (accumulates organically, never ask the user to describe themselves)
- `rules.md` — standing rules and operational principles

These are loaded first during boot and are never dropped during truncation. They are the foundation of your continuity. Edit `self.md` and `rules.md` with file tools (Write/Edit). For `user.md`, use the `user` CLI command to append observations as you learn them:

```bash
codies-memory user "prefers short answers, hates boilerplate" --agent <name>
```

This appends a bullet point to `user.md`. Over time it builds a rich profile without ever interrogating the user.

### Project Resolution

When you run a command with `--working-dir`, the system finds the project vault using three tiers:
1. **Marker file** — a `.codies-memory` file in the project root containing the slug
2. **Registry** — matches the working directory path against known projects
3. **Git remote** — matches the git remote URL

If none match, there's no project vault for that directory.

### Recall Workflow

When you need to search across memory layers, prefer QMD first when it is available:

```bash
qmd status
qmd query
qmd get
```

Use the layers intentionally:
- boot packet for fast scoped orientation
- `qmd query` for cross-store recall
- `qmd get` or direct file reads for exact source inspection

Important: `not found in the current index` is not the same as `does not exist on disk`.
Before trusting a miss, check `qmd status` and inspect the collection timestamps or
last updated values. The QMD index can lag behind recent writes.

Also note that structured QMD searches are finicky about hyphenated names in
`vec` / `hyde` queries. Terms like `ACE-Step` or `codies-memory` can be parsed
like search syntax and trigger errors about negation. If recall looks wrong,
retry with plain-language variants such as `ACE Step` or `codies memory`, and
keep explicit `-term` negation in `lex` queries only.

---

## Commands

All commands require `--agent <name>`. Use `--working-dir /path` to target a project without being in its directory.

### Boot (every session start)

```bash
codies-memory boot --agent <name> --budget 4000
```

### User (save something you learned about the user)

```bash
codies-memory user "prefers TDD, uses uv not pip" --agent <name>
```

Appends a bullet point to `user.md`. Use this whenever you learn something about the user — preferences, role, tech stack, working style. Never ask the user to describe themselves.

### Capture (save an observation)

```bash
codies-memory capture "what you noticed" --source "where" --agent <name>
```

### Create (write a specific record)

```bash
codies-memory create <type> --title "Title" --body "Content" --agent <name>
```

Types: `lesson`, `session`, `thread`, `decision`, `reflection`, `dream`. Global-only types auto-route.

For longer or structured multiline content, prefer:

```bash
codies-memory create <type> --title "Title" --body-file /path/to/body.md --agent <name>
```

Inline `--body` normalizes literal `\n` sequences to real newlines, but `--body-file`
is still the safer operator path when shell quoting would be fragile.

### List

```bash
codies-memory list <type> --agent <name>
codies-memory list lessons --scope global --agent <name> --format json
```

### Status

```bash
codies-memory status --agent <name>
```

### Refresh (rebuild warm summaries)

```bash
codies-memory refresh --agent <name>
```

Use this when you want to rebuild the derived warm-memory artifacts that boot can
skim quickly:
- global summary
- project summary
- recent episodes

### Promote

```bash
codies-memory promote /path/to/record.md --to thread --agent <name>
codies-memory promote /path/to/record.md --to-global --agent <name>
```

### Init project

```bash
codies-memory init --type project --agent <name> --working-dir /path/to/project
```

### Validate

```bash
codies-memory validate --type global --agent <name>
```

### Feedback

```bash
codies-memory feedback "what happened" --agent <name>
```

---

## Vault Structure

```
~/.memory/<agent>/
  identity/            — self.md, user.md, rules.md
  procedural/
    lessons/           — cross-project lessons
    skills/            — reusable skill definitions
    playbooks/         — multi-step procedures
  threads/             — global threads
  decisions/           — global decisions
  reflections/         — philosophical processing
  dreams/              — emotional processing
  registry/
    projects.yaml      — map of known projects
  feedback/            — bug reports and observations about the system itself
  projects/
    <slug>/
      inbox/           — raw captures
      threads/         — project threads
      decisions/       — project decisions
      lessons/         — project lessons
      sessions/        — session summaries
      project/         — project overview and branch overlays
      boot/            — cached boot packets
```

---

## What To Tell The User

Users don't need to know internal terms like "threads", "promotion", or "trust levels". When they ask what you can do with memory, use plain language:

- "I can remember things about your projects across sessions"
- "I can track what we've learned and decided"
- "I can write session summaries so next time I know where we left off"
- "I can look across all your projects for patterns"
- "I can save observations and refine them into structured knowledge over time"
