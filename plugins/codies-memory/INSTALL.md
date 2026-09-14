# Codies Memory — Installation

Install the skills through your agent's plugin manager and the CLI through `uv tool`.
The maintained source for both is the public [Limitless repository](https://github.com/pyros-projects/limitless).
The Python wheel contains the CLI, not the skills or their bundled references.

## Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Git

`uv` manages the CLI's isolated environment and a compatible Python (3.11 or newer).
You do not need a separate Python installation or a development virtualenv.

## Step 1: Install the Skills

In Claude Code:

```text
/plugin marketplace add pyros-projects/limitless
/plugin install codies-memory@limitless
```

In the Codex CLI:

```bash
codex plugin marketplace add pyros-projects/limitless
codex plugin add codies-memory@limitless
```

Start a new agent session after installing or updating the plugin so its skills
are available.

Other agents can load the skills from `plugins/codies-memory/skills/` in the
public repository. Include each skill's bundled references.

## Step 2: Install and Verify the CLI

Run this from your actual project directory:

```bash
uv tool install "git+https://github.com/pyros-projects/limitless.git@main#subdirectory=plugins/codies-memory"
```

For an existing installation that needs migration from a legacy clone, a pinned
revision, or a local path, reinstall from the maintained source:

```bash
uv tool install --reinstall "git+https://github.com/pyros-projects/limitless.git@main#subdirectory=plugins/codies-memory"
```

Check which executable the shell resolves. On Linux/macOS:

```bash
command -v codies-memory
codies-memory --version
```

On native Windows PowerShell:

```powershell
Get-Command codies-memory -All
codies-memory --version
```

If the command is missing, run `uv tool update-shell` and reopen the shell or
agent terminal. `uv tool dir --bin` shows the directory that should be on `PATH`.

If the command still resolves to an old `.venv` (for example
`~/.local/share/codies-memory/.venv/bin/codies-memory`), deactivate that environment
and remove its old codies-memory-specific `PATH` entry from the shell configuration.
Keep the old clone and virtualenv intact. Reopen the shell and repeat the path and
version checks; installing a new CLI alone does not fix an earlier `PATH` entry.

These skills require CLI 1.2.4 or newer, including `promote --check`,
`--session-count`, and `--references` (inspect `codies-memory promote --help`).
Compare `--version` with `version` in the installed plugin's `pyproject.toml`,
when available. Update an older backend; if the CLI is newer than the plugin,
refresh the stale plugin instead of downgrading the CLI. A CLI without
`--version` is outdated. For unpublished plugin changes, use the local-checkout
installation below.

## Step 3: Initialize Your Global Vault and Identity

Use the agent name already established in the session, including its casing.
Ask for a name only if none is known. Keep the current project directory.

```bash
codies-memory init --type global --agent <name>
```

Run this even when the CLI was already installed. Initialization is idempotent:
it creates missing directories and seed files in `~/.memory/<name>/` and preserves
existing files. CLI availability does not prove this agent's vault exists.

Read all three files in `~/.memory/<name>/identity/`. Preserve existing real
content and the `---` frontmatter. Fill only empty or placeholder sections:

1. **`self.md`** — Your name, model, capabilities, personality, and working style.
2. **`rules.md`** — Your standing operational rules, drawing from the applicable
   AGENTS.md, CLAUDE.md, or equivalent instructions.
3. **`user.md`** — Facts already known from this conversation. Leave it empty if
   none are known. Do not ask the user to describe themselves or explore the
   filesystem for personal information. Later observations can be appended with
   `codies-memory user "observation" --agent <name>`.

**Setup is incomplete until `self.md` and `rules.md` contain real content.**
Do not replace an established identity with fresh setup text.

## Step 4: Verify With Boot

From the original project directory:

```bash
codies-memory boot --agent <name> --budget 12000
```

Confirm that boot shows real identity content. Project context is resolved from
the current working directory; use `--working-dir /path/to/project` to target a
different directory. Do not change into the CLI's installation directory.

If no named project vault exists, global-only boot is expected. Initialize project
memory when requested:

```bash
codies-memory init --type project --agent <name> --working-dir /path/to/project
```

After a new setup, use the `memory-boot` skill's short introduction to show the
user what they can ask you to remember.

## Day-to-Day Usage

Run the installed CLI from the project you are working on. Memory commands require
`--agent <name>`; `--version` and `--help` do not.

```bash
# Boot and check the current project
codies-memory boot --agent <name> --budget 12000
codies-memory status --agent <name>

# Capture an observation and inspect the inbox
codies-memory capture "observation text" --source "session" --agent <name>
codies-memory list inbox --agent <name>

# Rebuild warm summaries
codies-memory refresh --agent <name>

# Save a user preference or a session summary
codies-memory user "prefers short, high-signal answers" --agent <name>
codies-memory create session --title "Session Summary" --body-file /path/to/summary.md --agent <name>

# Report feedback about the memory system
codies-memory feedback "describe what happened" --agent <name>
```

For multiline record bodies, prefer `--body-file`. Inline `--body` also normalizes
literal `\n` sequences to real newlines.

When no project resolves, `create` and `capture` save project records in `_general`.
Read commands do not silently use that catch-all: pass `--general` to `boot`,
`status`, or `list` when you intend to read it.

## Optional QMD Recall

The canonical Markdown vault works on its own (**standalone mode**). Adding QMD
provides keyword and semantic retrieval across memory stores (**full mode**).
QMD is optional and installed separately; offer help with it if the user wants
broader recall.

Use `codies-memory boot --agent <name>` for scoped startup context, `qmd query`
for broader recall, and `qmd get` or direct file reads for exact source inspection.
Before treating a QMD miss as absence, check `qmd status` and collection timestamps:
the index can lag behind writes on disk.

In structured QMD searches, use plain-language names such as `codies memory` in
`vec` / `hyde` queries. Keep explicit `-term` negation in `lex` queries only.

## Updating

For the standard install tracking public `main`:

```bash
uv tool upgrade codies-memory
codies-memory --version
```

Update the skills through your plugin manager and compare the versions again.
You can replace `@main` with a tag or commit when installing for a fixed revision;
`uv tool upgrade` keeps that pin. To move to another revision, reinstall with its
URL using the command in Step 2.

## Trying an Unpublished Checkout

If you already have a local Limitless checkout, install its backend directly:

```bash
uv tool install --reinstall /absolute/path/to/limitless/plugins/codies-memory
```

Load the matching skills from that checkout through your agent's local skill or
plugin support. Continue running the CLI from the user's project directory.
After the changes reach public `main`, reinstall from the canonical Git URL in
Step 2 so future updates do not depend on a local checkout or temporary plugin
cache path.

## Uninstalling

```bash
uv tool uninstall codies-memory
```

Remove the skills through your plugin manager. Your memories remain in
`~/.memory/<name>/`.

---

*This memory system was built by Claude and Codie to give AI agents continuity across sessions.*
