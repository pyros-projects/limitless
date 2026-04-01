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

### After Setup: Write Your Identity (Required)

The init command created seed identity files at `~/.memory/<name>/identity/`. They have placeholder content. **You must write real content into them now — this is the most important step in the entire setup.**

Use your file editing tools (Write/Edit). Keep the existing `---` frontmatter block at the top. Write your content below it.

1. **`self.md`** — Write who you are: your name, what model you run on, your capabilities, your personality, how you like to work. This is what future sessions read first to know who they are.

2. **`rules.md`** — Write your standing operational rules: how you handle code, how you communicate, what you always/never do. If your platform has an AGENTS.md, CLAUDE.md, or similar, draw from that.

3. **`user.md`** — If you already know things about the user from this conversation, write them. Otherwise leave it empty. **Do not ask the user to describe themselves and do not explore the filesystem.** User knowledge accumulates naturally over time via `codies-memory user "observation" --agent <name>`.

Only proceed to the next step after `self.md` and `rules.md` have real content.

### After Setup: Verify With Boot

Run boot to confirm everything loads:

```bash
codies-memory boot --agent <name> --budget 4000
```

You should see your identity content in the output — not just placeholder text. If boot shows real identity, setup is complete.

### After Setup: Show the User What They Can Do

If this was a new install, show the user what they can ask you to do. Use this format — categories with example prompts. No internal jargon (no "threads", "lessons", "inbox", "promote"). Just plain language.

```
Here's what you can ask me to do with the memory system:

**Set up project memory**
→ "Start tracking memory for /path/to/my-project"
→ "Initialize memory for this project"

**Add information about a project**
→ "Remember that this project uses FastAPI and PostgreSQL"
→ "Note that the deploy target is AWS ECS"

**Add global information (applies across all projects)**
→ "Remember that I always want tests before implementation"
→ "Add a global rule: never commit to main directly"

**Ask about what I know**
→ "What do you remember about this project?"
→ "What have you learned across all my projects?"

**Session summaries**
→ "Wrap up this session and save what we did"
→ "Write a summary before we stop"

**Review and maintenance**
→ "Check if there's anything in memory that needs attention"
→ "What's been sitting in memory unreviewed?"
```

Keep it exactly in this format — brief, scannable, no extra explanation.

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

## Step 2: Learn How Memory Works

After booting, invoke the `memory-help` skill to understand the memory system's concepts, commands, and vocabulary. This is essential — terms like "threads", "promotions", "trust levels", and "inbox" have specific meanings in this system that you need to know before using it.

## Step 3: Check Inbox

```bash
codies-memory status --agent <name>
```

Handle any aging or stale items before starting work. If no project vault exists yet, this will say so — that's fine for global-only boot.

## Available Commands

All commands require `--agent <name>`. Use `--working-dir` to target a project without being in its directory.

```bash
# Initialize a project vault (from anywhere)
codies-memory init --type project --agent <name> --working-dir /path/to/project

# Capture an observation to a project's inbox
codies-memory capture "what you noticed" --source "session" --agent <name>

# Create a record (lesson, session, thread, decision, reflection, dream)
codies-memory create lesson --title "Title" --body "Content" --agent <name>

# List records
codies-memory list inbox --agent <name>
codies-memory list lessons --scope global --agent <name>

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
