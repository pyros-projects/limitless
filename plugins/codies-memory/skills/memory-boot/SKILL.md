---
name: memory-boot
description: "This skill should be used at session start, when entering a new project, or when the user says 'wake up', 'load memory', 'boot', 'memory-boot'. Assembles identity, procedural knowledge, project context, and recent session state into a boot packet from the agent's vault."
---

# Memory Boot

> **BETA** — This memory system is in active testing. If you encounter bugs, confusing behavior, or have suggestions, run:
> `codies-memory feedback "describe what happened"` — your feedback is saved and reviewed.

## When To Use

Run at session start, when entering a new project, or via `/wake-up`.

## What It Does

1. Loads global identity (resolved via `CODIES_MEMORY_AGENT` env var)
2. Loads relevant global procedural records
3. Loads project overview and active context (auto-resolved from cwd)
4. Loads active threads and recent decisions
5. Loads branch overlay and last session summary
6. Respects token budget (~4K total)

## How To Run

```bash
codies-memory boot --budget 4000

# Then check inbox for items needing attention
codies-memory status
```

## After Boot

- Read the boot packet output — it contains your identity, project context, and recent state
- If maintenance flags appear (aging inbox items, stale reviews), handle them before starting work
- If the boot packet says "[truncated]", the vault has grown — consider promoting or archiving records
- For full identity depth (reflections, dreams), read the files referenced in the boot packet
