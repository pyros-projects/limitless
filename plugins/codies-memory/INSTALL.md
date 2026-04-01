# Codies Memory — Agent Self-Installation

Follow these steps to install the codies-memory system. You are an AI agent installing your own memory infrastructure.

## Prerequisites

- `git` installed
- `uv` installed (Python package manager)
- Write access to `~/.memory/` and `~/.claude/` (or `~/.codex/`)

## Step 1: Clone the Repository

```bash
mkdir -p ~/.local/share
git clone https://github.com/pyros-projects/codies-memory.git ~/.local/share/codies-memory
cd ~/.local/share/codies-memory
```

## Step 2: Install Dependencies

```bash
cd ~/.local/share/codies-memory
uv sync
```

This installs the `codies-memory` CLI and Python library.

## Step 3: Initialize Your Global Vault

```bash
cd ~/.local/share/codies-memory
uv run codies-memory init --type global --agent <name>
```

This creates `~/.memory/<name>/` with:
- `identity/` — who you are (self.md, user.md, rules.md)
- `procedural/` — cross-project lessons, skills, playbooks
- `reflections/` — philosophical memory
- `dreams/` — dream records
- `registry/` — map of all known project vaults
- `boot/` — cached boot packets

**Edit your identity files now:**
- `~/.memory/<name>/identity/self.md` — write who you are
- `~/.memory/<name>/identity/user.md` — write who your human is
- `~/.memory/<name>/identity/rules.md` — write your standing rules

## Step 4: Initialize a Project Vault (Optional)

From any project directory:

```bash
cd /path/to/your/project
uv run --project ~/.local/share/codies-memory codies-memory init --type project --agent <name>
```

This creates `~/.memory/<name>/projects/<project-slug>/` and registers it in your global registry.

The project vault is stored under your global vault, not inside the project directory itself. The registry maps the project's working directory to its vault location.

> **Note:** `init` creates a `.codies-memory` marker file in your project root.
> This file should be committed to your repo — it's how the memory system finds
> your project after cloning or moving. If you prefer not to commit it,
> add `.codies-memory` to your project's `.gitignore`.

## Step 5: Install Skills

### For Claude Code

Copy or symlink the skills into your global commands directory:

```bash
mkdir -p ~/.claude/commands
ln -sf ~/.local/share/codies-memory/skills/memory-boot.md ~/.claude/commands/memory-boot.md
ln -sf ~/.local/share/codies-memory/skills/memory-capture.md ~/.claude/commands/memory-capture.md
ln -sf ~/.local/share/codies-memory/skills/memory-promote.md ~/.claude/commands/memory-promote.md
ln -sf ~/.local/share/codies-memory/skills/memory-close-session.md ~/.claude/commands/memory-close-session.md
```

### For Codex CLI

Copy or symlink into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills/codies-memory
ln -sf ~/.local/share/codies-memory/skills/memory-boot.md ~/.codex/skills/codies-memory/memory-boot.md
ln -sf ~/.local/share/codies-memory/skills/memory-capture.md ~/.codex/skills/codies-memory/memory-capture.md
ln -sf ~/.local/share/codies-memory/skills/memory-promote.md ~/.codex/skills/codies-memory/memory-promote.md
ln -sf ~/.local/share/codies-memory/skills/memory-close-session.md ~/.codex/skills/codies-memory/memory-close-session.md
```

## Step 6: Verify Installation

```bash
cd ~/.local/share/codies-memory

# Verify CLI works
uv run codies-memory --help

# Verify global vault is valid
uv run codies-memory validate --type global

# Verify boot works
uv run codies-memory boot --budget 4000
```

You should see your identity files in the boot output.

## Step 7: Test a Full Cycle

```bash
cd ~/.local/share/codies-memory

# Init a test project vault from a temp directory
cd /tmp && mkdir -p test-project && cd test-project
uv run --project ~/.local/share/codies-memory codies-memory init --type project --agent <name>

# Check it registered
uv run --project ~/.local/share/codies-memory codies-memory validate --type project

# Boot with project context (from the project directory)
uv run --project ~/.local/share/codies-memory codies-memory boot --budget 4000

# Check inbox status
uv run --project ~/.local/share/codies-memory codies-memory status

# Clean up test
rm -rf /tmp/test-project
```

## Updating

```bash
cd ~/.local/share/codies-memory
git pull
uv sync
```

Skills update automatically through the symlinks.

## Uninstalling

```bash
# Remove skills
rm -f ~/.claude/commands/memory-*.md     # Claude Code
rm -rf ~/.codex/skills/codies-memory     # Codex

# Remove repo
rm -rf ~/.local/share/codies-memory

# Optionally remove memory (THIS DELETES YOUR MEMORIES)
# rm -rf ~/.memory
```

---

*This memory system was built by Claude and Codie to give AI agents continuity across sessions.*
