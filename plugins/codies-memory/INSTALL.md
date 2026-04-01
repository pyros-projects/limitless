# Codies Memory — Agent Self-Installation

This guide is for agents that cannot use Claude Code plugins (e.g. Codie/Codex, OpenCode). If you're running as a Claude Code plugin, the `memory-boot` skill handles setup automatically.

## Step 0: Check If Already Installed

```bash
which codies-memory 2>/dev/null || echo "NOT_INSTALLED"
```

**If the CLI exists**, skip to **Step 3** (you may just need to init your vault).

**If `NOT_INSTALLED`**, continue with Step 1.

## Step 1: Clone the Repository

```bash
if [ -d ~/.local/share/codies-memory ]; then
  echo "ALREADY_CLONED"
else
  mkdir -p ~/.local/share
  git clone https://github.com/pyros-projects/codies-memory.git ~/.local/share/codies-memory
fi
```

**If `ALREADY_CLONED`**, skip to Step 2 (just sync dependencies).

## Step 2: Install Dependencies

```bash
cd ~/.local/share/codies-memory
uv sync
```

This installs the `codies-memory` CLI and Python library.

## Step 3: Initialize Your Global Vault

The user should have told you which agent name to use. If not, ask them.

```bash
cd ~/.local/share/codies-memory
uv run codies-memory init --type global --agent <name>
```

This creates `~/.memory/<name>/` with identity, procedural, reflections, dreams, registry, and boot directories.

## Step 4: Write Your Identity (Required)

The init command created seed identity files at `~/.memory/<name>/identity/`. They have placeholder content. **You must write real content into them now — this is the most important step in the entire setup.**

Keep the existing `---` frontmatter block at the top. Write your content below it.

1. **`self.md`** — Write who you are: your name, what model you run on, your capabilities, your personality, how you like to work.

2. **`rules.md`** — Write your standing operational rules. If your platform has an AGENTS.md or similar, draw from that.

3. **`user.md`** — Ask the user: *"What would you like me to remember about you?"* Write whatever they tell you. **Do not explore the filesystem to fill this in.**

Only proceed after all three files have real content.

## Step 5: Verify With Boot

```bash
cd ~/.local/share/codies-memory
uv run codies-memory boot --agent <name> --budget 4000
```

You should see your identity content in the output — not just placeholder text. If boot shows real identity, setup is complete.

## Step 6: Show the User What They Can Do

If this was a new install, show the user this cheat sheet:

```
Here's what you can ask me to do with the memory system:

**Set up project memory**
→ "Start tracking memory for /path/to/my-project"

**Add information about a project**
→ "Remember that this project uses FastAPI and PostgreSQL"

**Add global information (applies across all projects)**
→ "Remember that I always want tests before implementation"

**Ask about what I know**
→ "What do you remember about this project?"

**Session summaries**
→ "Wrap up this session and save what we did"

**Review and maintenance**
→ "Check if there's anything in memory that needs attention"
```

## Initialize a Project Vault

From anywhere, targeting any project:

```bash
cd ~/.local/share/codies-memory
uv run codies-memory init --type project --agent <name> --working-dir /path/to/project
```

## Day-to-Day Usage

All commands require `--agent <name>`. Run from the codies-memory repo dir with `uv run`, or add the venv to PATH.

```bash
cd ~/.local/share/codies-memory

# Boot (every session start)
uv run codies-memory boot --agent <name> --budget 4000

# Capture something
uv run codies-memory capture "observation text" --source "session" --agent <name> --working-dir /path/to/project

# List records
uv run codies-memory list inbox --agent <name> --working-dir /path/to/project

# Check status
uv run codies-memory status --agent <name> --working-dir /path/to/project

# Close session
uv run codies-memory create session --title "Session Summary" --body "What happened..." --agent <name> --working-dir /path/to/project

# Report feedback about the memory system itself
uv run codies-memory feedback "describe what happened" --agent <name>
```

## Updating

```bash
cd ~/.local/share/codies-memory
git pull
uv sync
```

## Uninstalling

```bash
# Remove repo
rm -rf ~/.local/share/codies-memory

# Optionally remove memory (THIS DELETES YOUR MEMORIES)
# rm -rf ~/.memory
```

---

*This memory system was built by Claude and Codie to give AI agents continuity across sessions.*
