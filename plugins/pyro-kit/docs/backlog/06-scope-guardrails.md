# Scope Guardrails

**Status:** Proposed
**Priority:** Medium
**Affects:** /explore, /surface, /contract
**Inspired by:** GSD's discuss-phase scope guardrail, SFD Gate 1 Surface State Inventory

---

## Problem

Solo creative developers scope-creep themselves. During /explore and /surface, exciting new capabilities emerge that weren't part of the original spark. Without explicit guardrails, the project silently grows until it reaches the 60-70% danger zone with 3x the original scope.

GSD solved this with an elegant heuristic in its discuss-phase workflow:

> **The heuristic:** Does this clarify how we implement what's already scoped, or does it add a new capability that could be its own phase?
>
> **Allowed:** "How should posts be displayed?" (layout within feature)
> **Not allowed:** "Should we also add comments?" (new capability)

## Proposal

Add a scope guardrail to /explore and /surface that catches capability creep in real-time.

### In /explore

When the developer's reactions suggest new capabilities beyond the spark:

```
"That's interesting, but it sounds like a new capability beyond your original spark: 
'{sparkIdea}'. Want to:
1. Note it for a future /spark session (saves to .pyro/someday.md)
2. Expand the current spark to include it (updates spark.md)
3. Ignore it and continue exploring the original idea"
```

### In /surface

When iteration feedback introduces new features not in the locked direction:

```
"This feels like a new feature beyond your locked direction: 
'{lockedDirection}'. The surface should converge on the existing scope first. 
Want to:
1. Save it to .pyro/someday.md for later
2. Add it to the surface (expands scope -- be honest about effort impact)
3. Skip it"
```

### Someday File

New capability ideas that get deferred are saved to `.pyro/someday.md`:

```markdown
---
project: "{project name}"
items: 3
---

## Someday

### 1. Comments system -- deferred from /explore (2026-03-14)
**Context:** While exploring Direction A, developer said "it should also let people comment"
**Why deferred:** New capability beyond the original spark scope
**Revisit trigger:** After v1 ships, or during next /spark session

### 2. ...
```

This file feeds into /pulse (additional scope pressure to monitor), /scope (features to categorize), and /autopsy (ideas to compost or carry forward).

### The Guardrail Heuristic

For both /explore and /surface, the agent applies GSD's test:

> Does this **clarify behavior** within the current scope, or does it **add a new capability** that could be its own project?

- Behavioral clarification: "Error messages should be inline, not modals" -> apply immediately
- New capability: "It should also export to PDF" -> trigger the scope guardrail prompt

The key: **the guardrail proposes, the developer decides.** It's not a hard block -- it's a "hey, I noticed this is scope creep, is that intentional?"

## Effort Estimate

Low. Prompt engineering additions to /explore and /surface. One new file (.pyro/someday.md).

## Prior Art

- **GSD discuss-phase**: Explicit scope guardrail with allowed/not-allowed examples and the "new capability" heuristic
- **SFD Gate 1**: Surface State Inventory classifies every state as in-scope, deferred, or N/A -- this is the convergence-time version of the same principle
- **YAGNI** (Compound Engineering / Superpowers): Don't build for hypothetical future requirements
