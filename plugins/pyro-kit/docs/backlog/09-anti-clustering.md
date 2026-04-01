# Anti-Clustering in Direction Generation

**Status:** Proposed
**Priority:** Medium
**Affects:** /explore
**Inspired by:** BMAD brainstorming anti-bias protocol, iDesignGPT design space coverage metrics

---

## Problem

LLMs naturally cluster outputs around semantic centers. When /explore generates 4 directions, they often vary the *implementation* of the same core approach rather than making genuinely different bets. The existing divergence strategy (explore/SKILL.md lines 165-174) provides heuristics:

```
Direction A: Bet on simplicity/minimalism
Direction B: Bet on richness/power  
Direction C: Bet on a surprising interaction model
Direction D: Bet on a different core insight
```

These are good heuristics, but there's no verification that the output actually achieved divergence.

## Proposal

Add a **coverage self-check** after direction generation that verifies directions span the design space.

### Coverage Check

After generating 4 directions, the agent evaluates them against 3-4 axes relevant to the idea:

```markdown
**Coverage check:**
- Complexity axis: A (minimal) vs B (full-featured) -- COVERED
- Interaction axis: A,B (CLI) vs C (TUI) -- WEAK (no GUI or API direction)
- Core mechanism: A,B,C all use file parsing -- CLUSTERED
- User type: all 4 target developers -- CLUSTERED (no non-developer direction)

Result: 2 axes clustered. Regenerating Direction D to explore a different core mechanism.
```

### Anti-Clustering Protocol

Adapted from BMAD's brainstorming anti-bias rule ("shift creative domain every 10 ideas"):

1. **Axis identification**: Before generating, identify 3-4 axes relevant to this idea (complexity, interaction model, core mechanism, target user, distribution channel, etc.)
2. **Generate directions**: Use existing heuristics
3. **Coverage check**: Map each direction to each axis. Flag axes where all directions cluster
4. **Regenerate if clustered**: Replace the weakest direction with one that covers the gap
5. **Disclose coverage**: Show the developer which axes are covered and which are intentionally uncovered

### Disclosure Format

After the 4 directions, add:

```markdown
**Design space coverage:**
These directions span: complexity (minimal to full), interaction model (CLI to GUI to API), 
and core insight (parsing vs analysis vs generation).
Intentionally uncovered: team/collaborative use, mobile-first, enterprise deployment.
```

This makes the exploration's boundaries visible and gives the developer a chance to say "actually, explore the enterprise angle too."

## Effort Estimate

Low. Prompt engineering addition to /explore. No structural changes. The coverage check is a self-evaluation step added after generate_directions().

## Prior Art

- **BMAD brainstorming**: "Consciously shift your creative domain every 10 ideas" to combat LLM semantic clustering
- **iDesignGPT** (Nature): Design space exploration with coverage, diversity, and novelty metrics as explicit quality measures
- **Schemex** (arXiv): Cluster -> Abstract -> Refine framework for discovering patterns from scattered examples
