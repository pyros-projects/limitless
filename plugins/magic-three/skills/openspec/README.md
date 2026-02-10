# OpenSpec — Spec-Driven Development

> **Skill file:** [`SKILL.md`](SKILL.md) — load this into your AI coding agent

## What is OpenSpec?

[OpenSpec](https://github.com/Fission-AI/OpenSpec) is a lightweight, open-source spec framework for AI-assisted development. Instead of ad-hoc prompting, you write structured specifications first, then let your AI implement against them.

**Core philosophy:** Fluid not rigid. Iterative not waterfall. Brownfield-first.

## Why Use It?

- **Predictable output** — AI agents produce better code when they have clear specs to follow
- **Brownfield-ready** — Delta specs describe *changes* to existing behavior, not just new systems
- **Session-resilient** — Specs persist on disk, so you don't lose context when starting a new chat
- **Auditable** — Every change gets its own folder with proposal, specs, design, and tasks
- **Tool-agnostic** — Works with 20+ AI coding tools

## Quick Start

```bash
# Install
npm install -g @fission-ai/openspec@latest

# Initialize in your project
cd your-project
openspec init --tools claude  # or: codex, cursor, copilot, all

# Start your AI agent and run:
/opsx:new add-feature-name
/opsx:ff          # generates all planning artifacts
/opsx:apply       # implements the tasks
/opsx:verify      # validates implementation
/opsx:archive     # merges specs, archives the change
```

## Which Workflow?

| Situation | Pattern |
|-----------|---------|
| Clear scope, <5 tasks | **Quick Feature** — `/opsx:new` → `/opsx:ff` → `/opsx:apply` → `/opsx:archive` |
| Unclear requirements | **Exploratory** — `/opsx:explore` → `/opsx:new` → `/opsx:continue` (repeat) |
| Complex, want review at each step | **Incremental** — `/opsx:new` → `/opsx:continue` → [review] → repeat |
| 10+ tasks, multi-session | **Large Feature + Beads** — add dependency-aware task execution |

## Key Concepts

### Specs = Source of Truth

Your `openspec/specs/` folder describes how your system currently works, organized by domain. These are living documents that evolve as you ship features.

### Changes = Proposed Modifications

Each feature/bugfix gets its own folder under `openspec/changes/` with:
- **proposal.md** — Why are we doing this?
- **specs/** — What requirements change? (ADDED / MODIFIED / REMOVED)
- **design.md** — How will we implement it?
- **tasks.md** — Checklist of implementation steps

### Delta Specs

Instead of rewriting specs from scratch, you describe what changes:

```markdown
## ADDED Requirements
### Requirement: Dark Mode
The system SHALL support a dark color theme.

## MODIFIED Requirements
### Requirement: Theme Persistence
Sessions SHALL persist theme preference. (Previously: no persistence)
```

When you archive, deltas merge into the main specs automatically.

## Combining with Beads

For complex features (10+ tasks, multi-session work), pair OpenSpec with [Beads](../beads/) for dependency-aware task execution. OpenSpec handles *what to build*; Beads handles *what to do next*.

See the [SKILL.md](SKILL.md) for the detailed combined workflow, task import procedure, and dependency inference rules.

## Links

- **Repo:** https://github.com/Fission-AI/OpenSpec
- **Docs:** https://openspec.dev/
- **Getting Started:** https://github.com/Fission-AI/OpenSpec/blob/main/docs/getting-started.md
- **Commands:** https://github.com/Fission-AI/OpenSpec/blob/main/docs/commands.md
