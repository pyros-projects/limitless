# Decision Log as First-Class Artifact

**Status:** Proposed
**Priority:** High
**Affects:** /spark, /explore, /narrow, /surface, /contract, /scope, /autopsy, fascination index
**Inspired by:** GSD's CONTEXT.md (locked decisions flow downstream), Compound Engineering's compounding knowledge, SFD's decision log artifact

---

## Problem

Decisions are captured late and unevenly across the Pyro Kit pipeline:

| Skill | Where decisions live | Failure mode |
|---|---|---|
| /spark | `spark.md` at crystallization | Rejected thumbnails and their reasons are lost |
| /explore | Freeform strings in `explore.md` ## Reactions | No structured format, no rejected-alternative tracking |
| /narrow | `explore.md` frontmatter update | Why alternatives were rejected is implicit only |
| /surface | **In-memory `decisions[]` array** | **Everything lost if session crashes before `converge()`** |
| /contract | `contract.md` at freeze | Fine -- but has no upstream decision context |

The surface skill is the worst offender: decisions exist only in a runtime array (line 87 of surface/SKILL.md) and are written to `surface.md` only inside `converge()`. A session crash mid-iteration loses every decision.

But the deeper problem: decisions are treated as state to persist, not as **vectors to explore**. Every "I prefer X over Y" is a signal about taste, constraints, and mental model that should flow forward and backward through the system.

## Proposal

Introduce `.pyro/decisions.md` -- a running log that every skill appends to immediately when a decision is made or captured.

### Schema

```markdown
---
project: "{project name}"
created: {date of first decision}
updated: {date of last decision}
decision_count: {N}
---

## Decisions

### D1 -- {Phase}: {Skill} -- {Date}
**Choice**: {What was decided}
**Over**: {What was rejected}
**Signal**: {What this reveals about preferences/taste}
**Context**: {Why -- developer's words quoted if available}
```

### Example Entries

```markdown
### D3 -- Explore: /explore -- 2026-03-14
**Choice**: Leaning toward Direction A (minimal CLI)
**Over**: Direction B (full IDE integration), C (web dashboard), D (VS Code extension)
**Signal**: Simplicity bet wins consistently. Distribution channel not important.
**Context**: "I just want something I can pipe into other tools."

### D7 -- Surface: /surface -- 2026-03-14
**Choice**: Card layout with 3-column grid
**Over**: Table layout, list view
**Signal**: Prefers visual density, scanability over detail
**Context**: "Tables feel too enterprise. I want to see everything at a glance."

### D8 -- Surface: /surface -- 2026-03-14
**Choice**: Error states shown inline (red border + message)
**Over**: Modal error dialogs, toast notifications
**Signal**: Prefers non-disruptive feedback, contextual over global
**Context**: "I hate modals. Just show me what's wrong where it's wrong."
```

### Integration Per Skill

| Skill | When to append | What to capture |
|---|---|---|
| /spark | Thumbnail selected/rejected | Which thumbnails chosen and rejected, what resonated |
| /explore | Every reaction, contrast, direction lean | Direction preferences, tradeoff choices, tone/scope feedback |
| /narrow | Direction locked | Lock decision with full rejected-alternatives context |
| /surface | **Every iterate() call** (critical fix) | Behavioral choices, edge case resolutions, rejections |
| /contract | Invariant locked, NFR target chosen | Technical constraint decisions |
| /scope | Feature categorized as soul-critical vs nice-to-have | Scope cut decisions and reasoning |

### Changes to Existing Skills

The change is small per skill -- add an append call:

**surface/SKILL.md**: In `iterate()`, replace the in-memory `APPEND to decisions` pattern with an immediate write to `.pyro/decisions.md`. The `converge()` function then references decisions.md rather than being the sole record.

**explore/SKILL.md**: In the react loop, after `Append to ## Reactions`, also append a structured decision entry to decisions.md.

**spark/SKILL.md**: After thumbnail selection, append a decision entry capturing what was chosen and what was rejected.

## What This Enables

1. **Session crash resilience.** Decisions survive even if convergence/crystallization never happens.

2. **Cross-skill context.** /contract reads decisions.md to understand *why* the surface looks the way it does. /build knows which tradeoffs were intentional.

3. **Decision-as-vector exploration.** /explore and /scout can mine decisions.md for search queries:
   - Decisions show "hates modals," "prefers CLIs," "wants offline-first"
   - Scout query: "offline-first CLI tools with inline error handling"
   - Explore constraint: no modal-heavy directions

4. **Fascination index enrichment.** /autopsy reads decisions.md to extract taste patterns across projects. Over multiple projects: "Pyro consistently rejects enterprise patterns, prefers minimalism, values offline-first."

5. **Momentum diagnostics.** /pulse can analyze decision velocity: "You made 12 decisions in 3 days, then 0 in 5 days. The last decision was about error handling -- is that where the energy died?"

## Effort Estimate

Low-Medium. One new file schema + append calls added to 6 existing skills. No new skill needed.

## Open Questions

- Should decisions.md be append-only (simpler) or support editing/reordering (more useful for review)?
- Should the Signal field be auto-generated by the agent or left for /autopsy to synthesize?
- How does decisions.md interact with branch-aware overlays if those are implemented?

## Prior Art

- **GSD CONTEXT.md**: Locked decisions, deferred ideas, and Claude's discretion -- structured decision capture that flows to downstream agents
- **SFD Decision Log** (whitepaper Appendix E, artifact #3): "What was tried, what was rejected, and why"
- **Compound Engineering /ce:compound**: Documents solved problems with YAML frontmatter for searchability
