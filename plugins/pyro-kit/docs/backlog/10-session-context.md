# Boot Packet / Session Start Context

**Status:** Proposed
**Priority:** Medium
**Affects:** /pyro orchestrator, session hooks, all skills
**Inspired by:** Codie's Memory boot packet concept, GSD's init context injection, Athena's hash-based delta caching

---

## Problem

When a developer starts a new session in a project with Pyro Kit state, there's no structured "here's where you left off" summary. The /pyro orchestrator reads state.md and suggests the next skill, but each skill independently reads its own state files. There's no cohesive session-start context.

This matters because:
- Session gaps lose momentum (the developer forgets what they decided and why)
- New agent instances have no project memory beyond file state
- The anti-abandonment system needs to remind the developer of their spark and decisions
- Skills can't reference cross-skill context without each one independently loading every state file

## Proposal

Generate a **boot packet** at session start -- a compact summary of project state that every skill receives.

### Boot Packet Contents

```markdown
## Session Context for {project name}

**Phase:** Surface (Phase 2)
**Last activity:** 3 days ago (/surface iterate, 7 iterations)
**Spark:** "{one-sentence idea from spark.md}"
**Direction:** "{locked direction from explore.md}"
**Recent decisions:** 
- D12: Card layout over table (prefers density)
- D13: Inline errors over modals (prefers contextual)
**Momentum:** Commit frequency declining (12/week -> 4/week)
**Open questions:** Edge case handling for empty state not resolved
```

### Generation Strategy

The boot packet is assembled from existing state files:
- `.pyro/state.md` -> phase, last skill, last activity
- `.pyro/spark.md` -> idea (one sentence)
- `.pyro/explore.md` -> locked direction (if exists)
- `.pyro/decisions.md` -> last 3-5 decisions
- `.pyro/surface.md` -> convergence status (if exists)
- Git analysis -> commit frequency trend (last 2 weeks)

### Caching (Stolen from Athena)

Don't regenerate the boot packet every session. Use hash-based delta detection:
1. Hash each input file (state.md, spark.md, explore.md, decisions.md)
2. If no file has changed since last boot packet generation, use cached version
3. If any file changed, regenerate only the changed sections

Store cached boot packet at `.pyro/.boot-cache.md` with file hashes in frontmatter.

### Token Budget

The boot packet must fit within a token budget to avoid competing with task context:

| Section | Target |
|---|---|
| Phase + last activity | ~50 tokens |
| Spark summary | ~30 tokens |
| Direction summary | ~50 tokens |
| Recent decisions (top 3-5) | ~150 tokens |
| Momentum signal | ~30 tokens |
| Open questions | ~50 tokens |
| **Total** | **~360 tokens** |

If the boot packet exceeds budget, truncate from the bottom (open questions first, then older decisions).

### Delivery Mechanism

**Option A: Session hook injection** (automatic)
The SessionStart hook (already in pyro-kit's hooks/hooks.json) generates and injects the boot packet as context for every session in a project with .pyro/ state.

**Option B: /pyro reads it** (manual)
The /pyro orchestrator generates and displays the boot packet when invoked. Skills read it from .boot-cache.md.

Recommend starting with Option B (simpler, explicit) and graduating to Option A once the format stabilizes.

### Integration with /pulse

If the boot packet detects momentum decline (commit frequency dropping, days since last activity > threshold), it adds a line:

```
**Momentum warning:** 5 days since last activity. Consider running /pulse for a check-in.
```

This is the lightest possible anti-abandonment nudge -- not a nag, just a data point in the session context.

## Effort Estimate

Medium. New generation logic + caching + token budgeting. Integrates with session hook infrastructure.

## Prior Art

- **Codie's Memory boot packet**: Layered session-start context assembled from identity + project + procedural + branch state
- **GSD init context**: init.cjs computes comprehensive context (models, flags, phase info, artifact existence) injected into every command
- **Athena**: Hash-based delta detection for boot summaries, ~125 tokens per summary
