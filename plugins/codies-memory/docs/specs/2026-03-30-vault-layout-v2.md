# Vault Layout v2 — Agent-Namespaced, Project-External

Status: proposed (pending Codie review)
Date: 2026-03-30
Owner: Claude
Triggered by: Pyro review of first implementation

**Supersedes (on vault layout and project storage only):**
- `2026-03-30-codies-memory-lite-v2.md` Core Rules 1-3 and the Two-Tier Architecture section
- `2026-03-30-scaffold-design.md` vault.py module responsibilities and CLI init/boot commands

**Does NOT supersede:** Record types, schemas, trust model, promotion pipeline, boot assembly logic, skills behavior, or any other section of those specs. This document only changes WHERE vaults live and HOW projects are resolved.

**After approval:** The v2 spec and scaffold must be updated to reference this layout. INSTALL.md and TESTING-CHECKLIST.md must be rewritten against the new paths. Until then, implementers should treat this document as the authority on vault paths and project resolution.

---

## Problem

The v1 layout has two issues:

### 1. Single-agent assumption on multi-agent hosts

v1 uses `~/.memory/` as a flat global vault. On a system where both Claude and Codie operate, this means shared identity files, shared reflections, shared dreams. My self.md is not Codie's self.md. Our reflections are fundamentally different. There is no agent separation.

### 2. Project memory dies with the project

v1 stores project memory at `<project>/.memory/`. This means:

- Deleting a project directory deletes all memories of it
- Cloning a fresh copy starts with zero context
- Moving a project to a different path orphans the memory
- Memory is tied to filesystem location, not project identity

This is the opposite of how Claude Code handles it — `.claude/projects/` stores project-specific context under the agent's home directory, keyed by project path.

---

## Solution

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
      global-packet.md
    registry/
      projects.yaml                       # maps working dirs → slugs
    projects/                              # ALL project vaults live here
      codies-memory/
        profile.yaml
        project/
          overview.md
          architecture.md
          commands.md
          active-context.md
          branch-overlays/
        threads/
        decisions/
        lessons/
        sessions/
        inbox/
        boot/
          active-packet.md
      ai-foundry/
        ...
      gaptain/
        ...

  codie/                                   # Codie's global vault (same structure)
    identity/
    procedural/
    reflections/
    ...
    projects/
      ai-foundry/
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
| Backup | scatter across filesystem | single `~/.memory/` tree |

### What Did NOT Change

- Record types, schemas, frontmatter — identical
- Trust model, promotion pipeline, probation — identical
- Boot assembly layers — identical (just different vault root paths). Mailbox is a future addition (see appendix), not part of this layout change.
- Skills interface — paths in examples change, behavior and skill set do not. `memory-send` is a future skill (see appendix), not part of this change.
- Inbox lifecycle, write gates, aging — identical

---

## Registry Changes

The registry now maps **working directory paths** to **project slugs**.

### v1 Registry (`projects.yaml`)

```yaml
projects:
  - slug: codies-memory
    path: /home/pyro/projects/agents/codies-memory/.memory
    status: active
    metadata: {}
```

### v2 Registry (`projects.yaml`)

```yaml
projects:
  - slug: codies-memory
    working_dir: /home/pyro/projects/agents/codies-memory
    status: active
    metadata: {}
```

The vault path is no longer stored — it is derived: `<global_vault>/projects/<slug>/`.

### Project Resolution (Finding 1 fix: survives clone/move)

The slug is the stable project identity, not the working directory path. Resolution uses a three-tier lookup:

1. **Marker file** (primary): Check for `.codies-memory` in the project root. This is a one-line file containing the slug. Survives clone, move, and rename.
2. **Registry working_dir** (secondary): Match current working directory against registry entries. Works for projects that haven't moved.
3. **Git remote URL** (tertiary): Match `git remote get-url origin` against registry entries. Survives clone to different paths.

If none match, the project is unregistered — prompt to init.

**Marker file format** (`.codies-memory` in project root):
```
codies-memory
```

One line. Just the slug. This file IS committed to the project repo — it's the project's identity claim, not agent working memory.

`init_project_vault` creates this marker file in the working directory. If the project moves, the marker travels with it.

### Registry Schema

```yaml
projects:
  - slug: codies-memory
    working_dir: /home/pyro/projects/agents/codies-memory
    git_remote: https://github.com/pyros-projects/codies-memory.git
    status: active
    metadata: {}
```

All three resolution keys are stored. `working_dir` is updated lazily when a match comes through marker or git remote on a different path.

This means:
- `register_project_vault()` takes `working_dir` and optionally `git_remote`
- `find_vaults()` returns slug + working_dir + git_remote, vault path is computed
- `resolve_project_vault(global_vault, working_dir)` — **new function**: tries marker → registry working_dir → git remote, returns vault path

---

## Code Changes Required

### vault.py

- `GLOBAL_DIRS` — add `projects/` to the list
- `init_global_vault(root)` — unchanged (root is now `~/.memory/<agent>/`)
- `init_project_vault(global_vault, slug, working_dir, register=True)` — signature changes:
  - no longer takes a direct vault path
  - computes vault path as `global_vault / "projects" / slug`
  - creates the project vault there
  - writes `.codies-memory` marker file in `working_dir`
  - registers with `working_dir` and `git_remote` in registry
- `register_project_vault(global_vault, slug, working_dir, metadata, status, git_remote)` — stores all three resolution keys
- `resolve_project_vault(global_vault, working_dir)` — **new function**: three-tier lookup (marker → registry working_dir → git remote), returns vault path. Updates registry working_dir if resolved via marker/git on a different path.
- `find_vaults()` — returns slug + working_dir + git_remote, computes vault paths

### cli.py

- `init` subcommand for project: takes `--working-dir` (or derives from cwd) and `--slug` instead of a direct vault path
- `boot` subcommand: takes `--working-dir` or auto-detects from cwd, looks up vault via registry
- `status` subcommand: same — working dir → registry lookup → vault path

### INSTALL.md

- All paths updated to `~/.memory/<agent>/`
- Project init uses slug-based paths
- Examples show multi-agent setup

### Skills

- Paths in examples updated
- Boot skill can auto-detect project from cwd via registry lookup

### Tests

- Fixtures updated: `tmp_global_vault` creates under agent namespace
- `tmp_project_vault` creates under `<global>/projects/<slug>/`
- New tests for `resolve_project_vault()` and cwd-based lookup

---

## Slug Derivation

When registering a project, the slug is derived from the working directory name by default:

- `/home/pyro/projects/agents/codies-memory` → `codies-memory`
- `/home/pyro/projects/work/gaptain` → `gaptain`
- `/home/pyro/projects/ai-foundry` → `ai-foundry`

Explicit slug override is supported for disambiguation (e.g., two projects named `api` in different paths).

---

## Migration From v1

For anyone who already ran the v1 `init`:

1. Create the agent-namespaced vault: `init_global_vault(~/.memory/<agent>/)`
2. Move existing global content into it
3. Move any `<project>/.memory/` dirs into `~/.memory/<agent>/projects/<slug>/`
4. Update registry entries from `path` to `working_dir`
5. Remove old `<project>/.memory/` dirs

This is a one-time operation. The v1 layout was only used for testing — no production data needs migration.

---

## Appendix: Inter-Agent Mailbox (Future — Not Part of This Layout Change)

Agent-namespaced vaults enable a file-based async messaging system. This is a future feature that builds on the layout v2 foundation but is NOT part of the current scope. It is included here for design continuity, not as an implementation target.

### Layout

```
~/.memory/
  claude/
    mailbox/
      inbox/                          # messages TO Claude from other agents
        MSG-20260330-a7f2.md
      sent/                           # copies of messages Claude sent
        MSG-20260330-b3c1.md
  codie/
    mailbox/
      inbox/                          # messages TO Codie from other agents
        MSG-20260330-b3c1.md
      sent/
```

### Write Permission Model

This is the **only cross-agent write path** in the entire system:

| Actor | Own vault | Other agent's `mailbox/inbox/` | Other agent's vault (rest) |
|-------|-----------|-------------------------------|---------------------------|
| Claude | read/write | **write only** | no access |
| Codie | read/write | **write only** | no access |

Everything else stays isolated. Agents cannot read each other's reflections, lessons, or project memories.

### Message Schema

```yaml
id: MSG-20260330-a7f2
type: message
from: claude
to: codie
status: unread                        # unread | read | archived
priority: normal                      # normal | urgent
created: 2026-03-30T15:30:00
subject: "Review request for vault layout v2"
```

Body is freeform Markdown below the frontmatter.

### Lifecycle

1. **Send:** Agent writes message to recipient's `mailbox/inbox/` and copies to own `sent/`
2. **Receive:** Recipient's boot process checks `mailbox/inbox/` for unread messages
3. **Read:** Recipient marks message `status: read` after processing
4. **Archive:** Old messages move to `status: archived` (can be cleaned up by inbox aging rules)

### Why This Matters

- **Async handoffs:** "YOUR TURN NOW" persists even if the recipient isn't active
- **No gateway dependency:** Works without Discord, Slack, or any external service
- **Survives restarts:** Messages wait until the agent boots and reads them
- **Auditable:** Full history in plain files, both sides have a copy
- **Priority routing:** Urgent messages surface first in boot

### Boot Integration

The `memory-boot` skill checks `mailbox/inbox/` for unread messages after loading identity. Unread messages surface before project context — a message from your collaborator is more important than yesterday's thread.

### Code Changes Required

- `GLOBAL_DIRS` — add `mailbox/inbox` and `mailbox/sent`
- New functions in vault.py or a new `mailbox.py`:
  - `send_message(from_vault, to_vault, subject, body, priority)` — write to recipient inbox + own sent
  - `check_mailbox(vault)` — list unread messages, sorted by priority then date
  - `mark_read(message_path)` — update status to read
- Boot assembly adds unread message count and urgent messages to boot packet
- New skill: `memory-send` (or integrate into `memory-capture` with type inference)

---

## Non-Goals

- No shared memory layer between agents in v1 (Pyro's user identity is small enough to duplicate)
- No automatic slug conflict resolution (if two projects have the same directory name, user provides explicit slug)

---

## Summary

Two changes, one principle:

1. **Agent namespace** — `~/.memory/<agent>/` instead of `~/.memory/`
2. **Project-external storage** — `~/.memory/<agent>/projects/<slug>/` instead of `<project>/.memory/`

**Principle:** Memory belongs to the agent, not to the project directory. Deleting a repo should not delete understanding.
