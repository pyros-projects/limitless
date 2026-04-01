# Explore Without Artifacts (Delay Persistence)

**Status:** Proposed
**Priority:** Medium
**Affects:** /explore, /narrow
**Inspired by:** OpenSpec's /opsx:explore (purely conversational, no artifacts created)

---

## Problem

Currently /explore writes `.pyro/explore.md` immediately after generating directions (line 37 of explore/SKILL.md: "Write .pyro/explore.md after generating directions"). This means:

1. Every exploration creates state, even throwaway explorations
2. Exploring 3 different angles before committing pollutes the state directory
3. There's no distinction between "I'm thinking out loud" and "I've decided to pursue this"

OpenSpec solved this elegantly: `/opsx:explore` is purely conversational -- no files created. When insights crystallize, you transition to `/opsx:new` which creates artifacts.

## Proposal

Split exploration into two phases:

### Phase A: Free Exploration (no artifacts)

`/explore` generates directions, contrasts, and reactions **in the conversation only**. No `.pyro/explore.md` is written. The developer can explore as many directions, angles, and ideas as they want without creating persistent state.

This makes exploration cheap. You can run `/explore` five times with different framings without polluting `.pyro/`.

### Phase B: Lock (creates artifacts)

Only `/narrow` writes `.pyro/explore.md`. When the developer says "lock it" or runs `/narrow`, the system:
1. Compiles all exploration results from the session into explore.md
2. Writes the locked direction with constraints
3. Creates the persistent state that /surface consumes

### What Changes

**explore/SKILL.md:**
- Remove: write_explore_md() call after generate_directions()
- Remove: incremental writes on contrast and reaction
- Keep: all generation and interaction logic unchanged
- Add: session-scoped state (directions, reactions, contrasts, leaning) held in conversation context

**narrow/SKILL.md:**
- Add: compile exploration state from conversation into explore.md
- Change: no longer reads explore.md as input -- reads from session context or accepts direction summary as argument

### Resume Behavior

If the developer starts a new session after exploring but before narrowing, the exploration is lost (intentionally -- it was conversation, not state). To preserve explorations across sessions:

```
/explore save     # Explicitly save current exploration state to explore.md (opt-in persistence)
/explore resume   # Resume from saved state (current behavior)
```

This makes persistence explicit rather than automatic.

### Edge Case: Multi-Session Exploration

Some explorations span multiple sessions. The `save` command handles this:
```
Session 1: /explore -> react -> contrast -> /explore save  (writes explore.md)
Session 2: /explore resume -> more reactions -> /narrow      (locks direction)
```

## Effort Estimate

Low-Medium. Restructure of when explore.md gets written. No new capabilities.

## Trade-offs

**Pro:** Exploration is cheap. No state pollution. Clear distinction between thinking and committing.
**Con:** Exploration is lost on session end unless explicitly saved. This is intentional (cheap explorations should be disposable) but might frustrate some workflows.

## Prior Art

- **OpenSpec /opsx:explore**: "Purely conversational -- no artifacts created. When insights crystallize, transition to structured skills."
- **SFD whitepaper**: The surface prototype is intentionally disposable. Exploration should be too.
