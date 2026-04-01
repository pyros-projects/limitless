# Pyro Kit

A Claude Code plugin for managing the creative lifecycle of solo projects. Pyro Kit helps you excavate ideas, track momentum, detect abandonment patterns, and extract value from projects you shelve.

**MVP v0.1.0** — 4 skills available, 20+ planned.

## Installation

### Quick test (development)

Load the plugin for a single session without installing:

```bash
claude --plugin-dir /path/to/pyro-kit
```

### Persistent install

From inside Claude Code, add the plugin directory as a local marketplace, then install:

```
/plugin marketplace add /path/to/pyro-kit
/plugin install pyro-kit@pyro-kit
```

Once installed, Pyro Kit activates automatically in every Claude Code session via the SessionStart hook.

## Quick Start

### 1. Initialize a project

```
/pyro init
```

Creates `.pyro/` in your project directory and registers the project in `~/.pyro/project-registry.yaml`. Run this once per project.

### 2. Excavate an idea

```
/spark
```

Start with a vague feeling ("something about CLI tools bugs me") and Pyro will generate 3-5 idea thumbnails using propose-react-iterate. Select one, expand it, refine it, and crystallize it into a one-sentence concept stored in `.pyro/spark.md`.

### 3. Check momentum

```
/pulse
```

Generates a momentum dashboard from your git history: commit frequency sparkline, novelty depletion signal, progress estimate, and your original spark quoted verbatim. Ends with three concrete paths (push, pivot, shelve) and a specific recommendation.

### 4. Compost a dead project

```
/autopsy
```

When you're done with a project (by choice or by drift), `/autopsy` extracts what fascinated you, diagnoses why you stopped, and feeds those fascinations back into `/spark` for your next project. Nothing is wasted.

### 5. Navigate the lifecycle

```
/pyro          # Get a routing recommendation based on current state
/pyro status   # See phase, momentum, last activity, gate history
/pyro list     # See all skills grouped by phase
```

## Available Skills

| Skill | Phase | What it does |
|-------|-------|-------------|
| `/pyro` | Meta | Lifecycle navigator — reads state, suggests next skill |
| `/spark` | 0: Ignition | Excavates vague feelings into crystallized ideas |
| `/pulse` | 5: Momentum | Git-powered momentum dashboard with push/pivot/shelve paths |
| `/autopsy` | 6: Lifecycle | Extracts fascinations from shelved/dead projects |

20+ additional skills are planned across all 7 phases. Run `/pyro list` to see the full roadmap.

## The 7 Phases

```
Phase 0: Ignition    — Vague feeling -> crystallized idea
Phase 1: Exploration — Idea -> explored design space
Phase 2: Surface     — Direction -> converged prototype
Phase 3: Contract    — Prototype -> frozen specifications
Phase 4: Build       — Contracts -> working software
Phase 5: Momentum    — Anti-abandonment intervention (any phase)
Phase 6: Lifecycle   — Completion or composting
```

Phases are soft-gated: Pyro warns when gates aren't met but never blocks you.

## State Files

### Per-project (`.pyro/`)

| File | Created by | Purpose |
|------|-----------|---------|
| `state.md` | `/pyro init` | Phase, momentum, soul, gate history |
| `spark.md` | `/spark` | Crystallized idea with metadata |
| `pulse-log.md` | `/pulse` | Append-only log of momentum check-ins |
| `config.yaml` | `/pyro init` | Project-local config overrides |
| `session-notes/` | `/pyro init` | Per-session working notes |

### Global (`~/.pyro/`)

| File | Purpose |
|------|---------|
| `config.yaml` | Dormancy threshold, auto-suggest settings |
| `project-registry.yaml` | All tracked projects with status and activity dates |
| `fascination-index.md` | Cross-project fascination themes (written by `/autopsy`, read by `/spark`) |
| `autopsies/` | Full autopsy reports, one per shelved project |

## How It Works

Pyro Kit is built on three core ideas:

**Propose-React-Iterate**: Every skill leads with a concrete proposal. You react to something tangible rather than answering open-ended questions. This is how `/spark` generates thumbnails and `/pulse` builds paths.

**Anti-Abandonment Psychology**: Solo developers abandon ~60-70% of projects, usually when novelty depletes and maintenance work takes over. `/pulse` detects this by analyzing your commit message sentiment — the shift from `feat:` and `add:` to `fix:` and `chore:` is the signal.

**Fascination Composting**: When you shelve a project, `/autopsy` extracts what fascinated you and feeds it into your fascination index. Next time you run `/spark`, those threads resurface naturally. Nothing is wasted — dead projects become fertilizer for new ones.

## Configuration

Edit `~/.pyro/config.yaml`:

```yaml
dormancy_threshold_days: 5        # Days of inactivity before dormancy warning
pulse_auto_suggest: true          # Suggest /pulse when momentum declines
fascination_intensity_decay: true # Reduce fascination intensity over time
default_start_phase: 0            # Phase for new projects
```

## Session Hook

Pyro Kit runs a lightweight check at every Claude Code session start. It reads your project state and, if the project appears dormant (no activity beyond the threshold), injects context suggesting a `/pulse` check-in. This is invisible when everything is healthy.

## Requirements

- Claude Code CLI
- bash (for shell scripts)
- git (for `/pulse` momentum analysis)

## License

MIT
