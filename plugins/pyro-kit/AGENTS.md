# AGENTS.md — Pyro Kit Plugin Guide

## What This Is

**Pyro Kit** is a Claude Code plugin that helps solo creative developers navigate the full project lifecycle — from vague idea to shipped product (or properly composted one).

17 skills across 7 phases, with anti-abandonment psychology built into the architecture.

## Plugin Structure

```
pyro-kit/
  .claude-plugin/       # Plugin manifest and marketplace config
  skills/               # 17 skill definitions (SKILL.md files)
  agents/               # Subagent definitions (excavator)
  hooks/                # Session start hook
  scripts/              # Shell scripts (init, git analysis, session hook, smoke test)
  docs/                 # User docs, testing guide, backlog, reference material
  specs/                # Formal specifications (PRD, SDD, PLAN)
```

## Key Conventions

- **PICS+Workflow**: All SKILL.md files follow Persona/Interface/Constraints/State + Workflow format
- **Soft gating**: Gates warn but don't block (G0-G7)
- **`${CLAUDE_PLUGIN_ROOT}`**: Use this for portable path resolution, never hardcoded paths
- **State files**: `.pyro/` (per-project) and `~/.pyro/` (global). YAML frontmatter + markdown body
- **Propose-react-iterate**: Never ask the user to write specs — show them something and let them react

## The 7 Phases

| Phase | Skills | Purpose |
|-------|--------|---------|
| 0: Ignition | /spark, /remix, /fascination | Excavate ideas from feelings |
| 1: Exploration | /explore, /narrow | Diverge then converge on direction |
| 2: Surface | /surface | Build and iterate a prototype |
| 3: Contract | /contract | Derive and freeze requirements |
| 4: Build | /build | Vertical slices from contracts |
| 5: Momentum | /pulse, /reframe, /scope, /decide | Track health, inject novelty, cut scope |
| 6: Lifecycle | /autopsy, /ship, /revive, /patterns | Ship, compost, or revive |

## Anti-Abandonment Psychology

Pyro Kit is specifically designed for developers who abandon projects at 60-70% completion. Features like novelty depletion detection, fascination composting, and momentum tracking are core — not nice-to-haves.
