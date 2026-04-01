---
name: memory-boot
description: "This skill should be used at session start, when entering a new project, or when the user says 'wake up', 'load memory', 'boot', 'memory-boot'. Assembles identity, procedural knowledge, project context, and recent session state into a boot packet from the agent's vault."
---

# Memory Boot

> **BETA** — This memory system is in active testing. If you encounter bugs, confusing behavior, or have suggestions, run:
> `codies-memory feedback "describe what happened"` — your feedback is saved and reviewed.

## Step 0: Check If Installed

Before anything else, check if the CLI exists:

```bash
which codies-memory 2>/dev/null || echo "NOT_INSTALLED"
```

**If `NOT_INSTALLED`**, follow the setup below. Otherwise skip to **Step 1: Boot**.

### First-Time Setup

The user should have told you which agent name to use (e.g. `claude`, `codie`, `octocat`). If not, ask them.

**A) If this is a Claude Code plugin** (you're reading this from a plugin directory):

```bash
# Install the Python backend from the plugin root
cd "${CLAUDE_PLUGIN_ROOT}" && uv sync

# Initialize your global vault
uv run codies-memory init --type global --agent <name>
```

**B) If this is a standalone installation** (not a Claude Code plugin):

Read `INSTALL.md` in this project for full instructions. Short version:
- Clone repo to `~/.local/share/codies-memory`
- `cd ~/.local/share/codies-memory && uv sync`
- `uv run codies-memory init --type global --agent <name>`

### After Setup: Verify With Boot

Run boot immediately to confirm the system works:

```bash
codies-memory boot --agent <name> --budget 4000
```

You should see the seed identity files in the output. If boot works, setup is complete.

### After Setup: Show the User What They Can Do

If this was a new install, tell the user how to interact with the memory system. Show them these example prompts they can use:

```
"Initialize memory for /path/to/my-project"
"Remember that this project uses FastAPI and PostgreSQL"
"What do you remember about this project?"
"Capture a lesson: always check YAML tabs vs spaces"
"Show me what's in your inbox"
"Promote that thread to a lesson"
"Write a session summary before we stop"
"What patterns do you see across my projects?"
```

Keep it brief — just the examples, no wall of explanation.

### After Setup: Write Your Identity (Later, Not Now)

The init command created seed identity files at `~/.memory/<name>/identity/`. They have placeholder content.

Write real content into them **when you have time** — not during setup. Use the standard file tools (Write/Edit). Keep the existing `---` frontmatter block at the top.

- `self.md` — who you are, your capabilities, your personality
- `user.md` — who your human is (ask them, do not snoop the filesystem)
- `rules.md` — your standing rules and operational principles

**Do not explore the filesystem to fill these in.** Ask the user what they want you to know, or fill them in gradually as you learn through conversation.

---

## Step 1: Boot (Every Session)

```bash
codies-memory boot --agent <name> --budget 4000
```

This assembles your boot packet from:
1. Global identity (`~/.memory/<agent>/identity/`)
2. Global procedural records (lessons, skills)
3. Project context (auto-resolved from cwd)
4. Active threads and recent decisions
5. Branch overlay and last session summary

Read the output — it contains your identity, project context, and recent state.

## Step 2: Check Inbox

```bash
codies-memory status --agent <name>
```

Handle any aging or stale items before starting work. If no project vault exists yet, this will say so — that's fine for global-only boot.

## Initialize a Project Vault (When Entering a New Project)

From the project's working directory:

```bash
codies-memory init --type project --agent <name>
```

This registers the project in your vault and creates a `.codies-memory` marker file.
