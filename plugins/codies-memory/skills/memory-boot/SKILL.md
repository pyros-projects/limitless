---
name: memory-boot
description: "This skill should be used at session start, when entering a new project, or when the user says 'wake up', 'load memory', 'boot', 'memory-boot'. Assembles identity, procedural knowledge, project context, and recent session state into a boot packet from the agent's vault."
---

# Memory Boot

> **BETA** — This memory system is in active testing. If you encounter bugs, confusing behavior, or have suggestions, run:
> `codies-memory feedback "describe what happened" --agent <name>` — your feedback is saved and reviewed.

## Step 0: Verify CLI, Vault, and Identity

Keep the user's original project working directory throughout setup and boot.
Check these three things independently, even when `codies-memory` already exists.

### A. Current CLI

On Linux/macOS, run `command -v codies-memory`; on native Windows PowerShell, run
`Get-Command codies-memory -All`. Then run:

```bash
codies-memory --version
```

Require CLI 1.2.4 or newer and verify that `codies-memory promote --help` includes
`--check`, `--session-count`, and `--references`. Compare the version with the
plugin's `pyproject.toml` (two directories above this skill), when available:
update an older backend, or refresh a stale plugin if the CLI is newer.

If the CLI is absent, outdated, or resolves to a legacy/plugin-cache `.venv`,
follow [INSTALL.md](../../INSTALL.md) to install or migrate to `uv tool` from the
public Limitless repository. Its PATH instructions cover `uv tool update-shell`,
reopening the shell, and removing an old codies-memory venv's PATH entry without
deleting it. Repeat executable, version, and capability checks before continuing.

### B. This Agent's Global Vault

Use the agent name already established in the session, including casing. Ask only
if none is known. Always run the idempotent initialization:

```bash
codies-memory init --type global --agent <name>
```

This creates missing files and preserves existing ones. An installed CLI does not
mean this agent's vault is initialized.

### C. Real Identity

Read `self.md`, `rules.md`, and `user.md` in `~/.memory/<name>/identity/`.
Preserve existing real content and frontmatter; fill only empty or placeholder
sections using file editing tools:

- `self.md`: your name, model, capabilities, personality, and working style.
- `rules.md`: standing operational rules from the applicable AGENTS.md,
  CLAUDE.md, or equivalent instructions.
- `user.md`: only facts already known from the conversation. Leave it empty if
  none are known. Do not ask the user to describe themselves or explore the
  filesystem for personal information.

**Continue only when `self.md` and `rules.md` contain real content.** Never replace
an established identity with fresh setup text.

## Step 1: Boot (Every Session)

```bash
codies-memory boot --agent <name> --budget 12000
```

This assembles your boot packet from:
1. Global identity (`~/.memory/<agent>/identity/`)
2. Global procedural records (lessons, skills)
3. Project context (auto-resolved from cwd)
4. Active threads and recent decisions
5. Branch overlay, last session summary, and the latest global daily-log tail

Read the output — it contains your identity, project context, and recent state.
Verify that it shows your real identity, not seed placeholders. Run from the
original project directory or pass `--working-dir /path/to/project` explicitly.

After a new setup, give the user a short introduction with example prompts:

- "Start tracking memory for this project"
- "Remember that this project uses FastAPI and PostgreSQL"
- "Remember that I always want tests before implementation"
- "What do you remember about this project?"
- "Wrap up this session and save what we did"
- "Check if there's anything in memory that needs attention"

Codies-memory works without QMD. Offer to help install QMD if the user wants
keyword and semantic recall across memory stores.

Boot does not implicitly fall back to `_general`. If no project vault resolves,
normal boot reports a global-only boot and still includes the latest
`Global Daily Log` tail for cross-project awareness. To intentionally load the
reserved catch-all project, use:

```bash
codies-memory boot --agent <name> --general
```

If the resolved project vault is `_general`, tell the user records are landing
in the default catch-all project, not a named project.

The packet ends with a `=== Boot Budget ===` section showing token usage per slice and in total (identity is exempt and unlimited). **If any slice or the total is at 90% or more — look for the `⚠ over 90% full` markers — tell the user.** Plain language, e.g. "heads up: my boot memory is at 94% for project working memory." Suggest either compacting/archiving records or raising `--budget`.

## Step 2: Learn How Memory Works

After booting, invoke the `memory-help` skill to understand the memory system's concepts, commands, and vocabulary. This is essential — terms like "threads", "promotions", "trust levels", and "inbox" have specific meanings in this system that you need to know before using it.

## Step 3: Recall Workflow

When you need to search beyond the boot packet, use QMD first when it is available:

```bash
qmd status
qmd query
qmd get
```

Preferred order:
1. boot for scoped startup context
2. QMD for cross-store recall
3. direct file inspection for exact on-disk truth

Important caveat: a miss from QMD is not always proof that the memory does not exist.
Check `qmd status` and the collection timestamps / last updated values before treating
`not found in the current index` as `does not exist on disk`.

## Step 4: Check Inbox

```bash
codies-memory status --agent <name>
```

Handle any aging or stale items before starting work. If no project vault exists
yet, this will say so — that's fine for global-only boot. `status` also does
not implicitly fall back to `_general`; run `codies-memory status --agent <name> --general --all`
when you intentionally want the catch-all project.

## Available Commands

Memory commands require `--agent <name>`; `--version` and `--help` do not. Run from
the user's project directory or use `--working-dir` to target another project.

```bash
# Initialize a project vault (from anywhere)
codies-memory init --type project --agent <name> --working-dir /path/to/project

# Capture an observation to a project's inbox
codies-memory capture "what you noticed" --source "session" --short "one-line summary" --agent <name>

# Create a record (lesson, session, thread, decision, reflection, dream)
codies-memory create lesson --title "Title" --short "one-line summary" --body "Content" --agent <name>

# List records
codies-memory list inbox --agent <name>
codies-memory list lessons --scope global --agent <name>

# Intentionally boot the catch-all project for vault-less notes
codies-memory boot --agent <name> --general

# Check inbox status (active, aging, stale counts)
codies-memory status --agent <name>

# Promote a record (e.g. inbox item to thread, or lesson to global)
codies-memory promote /path/to/record.md --to thread --agent <name>
codies-memory promote /path/to/record.md --to-global --agent <name>

# Save something you learned about the user (appends to user.md)
codies-memory user "prefers TDD, uses uv not pip" --agent <name>

# Report bugs or feedback about the memory system itself
codies-memory feedback "what happened" --agent <name>
```

**Important:** Whenever you learn something about the user during a session — preferences, tech stack, working style, name, role — save it with `codies-memory user`. This builds up over time.
