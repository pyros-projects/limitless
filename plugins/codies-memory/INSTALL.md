# Codies Memory — Agent Self-Installation

This guide is for agents that cannot use Claude Code plugins (e.g. Codie/Codex, OpenCode). If you're running as a Claude Code plugin, the `memory-boot` skill handles setup automatically.

## Supported Modes

`codies-memory` works in two supported modes:

- **Standalone mode** — local canonical vault only
- **Full mode** — local canonical vault plus QMD retrieval across memory layers

The plugin owns structured writes, promotion, trust, and boot behavior. QMD is the
recommended read path when available, but it is not packaged inside this plugin.

Standalone mode is fully usable. Full mode is recommended because QMD makes recall:

- faster
- more token-efficient
- semantic as well as keyword-based
- better across multiple memory stores

If the user wants the better recall path, recommend installing QMD and offer to
help install QMD instead of making them discover it later.

## Step 0: Check If Already Installed

```bash
which codies-memory 2>/dev/null || echo "NOT_INSTALLED"
```

**If the CLI exists**, do not assume it is current. First verify which copy you are using:

```bash
which codies-memory
codies-memory -h
```

If `which codies-memory` points at `~/.local/share/codies-memory/.venv/bin/codies-memory`, update that clone before continuing:

```bash
cd ~/.local/share/codies-memory
git pull
uv sync
```

Then continue with **Step 3**.

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

**If `ALREADY_CLONED`**, update it before continuing:

```bash
cd ~/.local/share/codies-memory
git pull
uv sync
```

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

3. **`user.md`** — If you already know things about the user from this conversation, write them. Otherwise leave it empty. User knowledge accumulates over time via `uv run codies-memory user "observation" --agent <name>`. **Do not ask the user to describe themselves and do not explore the filesystem.**

Only proceed after `self.md` and `rules.md` have real content.

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

# Rebuild warm summaries
uv run codies-memory refresh --agent <name> --working-dir /path/to/project

# Save something you learned about the user
uv run codies-memory user "prefers short, high-signal answers" --agent <name>

# Close session
uv run codies-memory create session --title "Session Summary" --body "What happened..." --agent <name> --working-dir /path/to/project

# Report feedback about the memory system itself
uv run codies-memory feedback "describe what happened" --agent <name>
```

For rich multiline record bodies, prefer `--body-file` over shell-quoted `--body`.
Inline `--body` now normalizes literal `\n` sequences to real newlines, but
`--body-file` remains the safer operator path for longer structured content.

## How Recall Works

Use the system in this order:

1. `codies-memory boot` for scoped startup context
2. `qmd query` for broader recall across memory stores
3. direct file reads when you need exact on-disk truth

Useful QMD commands when it is available:

```bash
qmd status
qmd query
qmd get
```

Do not treat a QMD miss as proof of absence until you check `qmd status`. The
current index can lag behind on-disk writes, so collection timestamps or "last
updated" values matter.

One more practical gotcha: QMD structured searches are finicky about hyphenated
names in `vec` / `hyde` queries. A term like `ACE-Step` or `codies-memory` can
be interpreted like search syntax and trigger errors such as `Negation (-term)
is not supported in vec/hyde queries`. When that happens, retry with a plain
language variant like `ACE Step` or `codies memory`, and keep explicit `-term`
negation only in `lex` queries.

## Quick Sanity Check

When something feels off, verify that you are using the expected copy of the CLI:

```bash
which codies-memory
codies-memory -h
```

The help output should include newer commands like `user` and `feedback`. If it does not, you are probably running a stale install and should update the repo you are resolving from.

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
