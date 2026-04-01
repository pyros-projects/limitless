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

# Set your agent name (replace <name> with what the user told you)
export CODIES_MEMORY_AGENT=<name>

# Initialize your global vault
uv run codies-memory init --type global --agent <name>
```

**B) If this is a standalone installation** (not a Claude Code plugin):

Read `INSTALL.md` in this project for full instructions. Short version:
- Clone repo to `~/.local/share/codies-memory`
- `cd ~/.local/share/codies-memory && uv sync`
- `export CODIES_MEMORY_AGENT=<name>`
- `uv run codies-memory init --type global --agent <name>`

### After Setup: Write Your Identity

Edit these files — they define who you are across sessions:

- `~/.memory/<name>/identity/self.md` — who you are
- `~/.memory/<name>/identity/user.md` — who your human is
- `~/.memory/<name>/identity/rules.md` — your standing rules

These are the most important files in the system. Take your time.

### After Setup: Persist the Agent Name

Add `export CODIES_MEMORY_AGENT=<name>` to your shell profile so it survives restarts. Or ask the user to configure it in their agent's settings.

---

## Step 1: Boot

```bash
codies-memory boot --budget 4000
```

This assembles your boot packet from:
1. Global identity (`~/.memory/<agent>/identity/`)
2. Global procedural records (lessons, skills)
3. Project context (auto-resolved from cwd)
4. Active threads and recent decisions
5. Branch overlay and last session summary

## Step 2: Check Inbox

```bash
codies-memory status
```

Handle any aging or stale items before starting work.

## After Boot

- Read the boot packet output — it contains your identity, project context, and recent state
- If maintenance flags appear, handle them before starting work
- If the boot packet says "[truncated]", the vault has grown — consider promoting or archiving records

## Initialize a Project Vault (When Entering a New Project)

From the project's working directory:

```bash
codies-memory init --type project --agent <name>
```

This registers the project in your vault and creates a `.codies-memory` marker file.
