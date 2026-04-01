# Prior Art Sweep in /explore

**Status:** Proposed
**Priority:** High
**Affects:** /explore
**Depends on:** 03-scout-skill.md
**Inspired by:** iDesignGPT (Nature, design space coverage metrics), Schemex (schema induction from examples), BMAD anti-bias protocol

---

## Problem

`/explore` currently generates 4 design directions entirely from the agent's internal knowledge. It doesn't know:
- What already exists that solves the same problem
- What's been tried and failed
- What adjacent innovations are happening in related domains
- Whether its 4 directions are clustered in one corner of the design space or genuinely spanning it

This makes exploration blind. The developer might get excited about a direction only to discover (much later) that a mature open-source tool already does exactly that.

## Proposal

Inject an optional research phase into /explore before direction generation.

### Flow Change

**Current:**
```
spark.md -> /explore -> 4 directions (from agent knowledge) -> react -> crystallize
```

**Proposed:**
```
spark.md -> /explore -> [optional: quick scout] -> 4 directions (informed by findings) -> react -> crystallize
```

### Quick Scout (60-Second Prior Art Sweep)

When /explore starts, it optionally fires a lightweight scout:

**Trigger:** Auto if register is balanced/wild/unhinged. Skip if register is serious and `--no-scout` flag. Always skip if /scout was already run in this project (check `.pyro/scout/` for recent reports).

**Scope:** 3-5 searches, max 60 seconds total. Not a full /scout invocation -- a quick sweep:
1. GitHub search for tools solving the same problem
2. One web search for "[core concept] alternatives"  
3. One web search for "[core concept] failed / abandoned / post-mortem"

**Output:** Injected into direction generation context, not displayed separately.

### Prior Art Disclosure

Each direction in /explore output gets a **Landscape line**:

```markdown
### Direction A: The CLI Archaeologist

**Scenario:** ...
**Sketch:** ...
**Key Bet:** ...

**Landscape:** 3 existing tools do parts of this (tool-a, tool-b, tool-c). 
None combine X with Y. Your unique angle: [specific delta].
```

If a direction is substantially similar to an existing tool, flag it honestly:
```markdown
**Landscape:** tool-x already does 80% of this. Your delta is [specific difference]. 
Consider: is that delta worth a new project, or should you contribute to tool-x?
```

### Design Space Coverage Check

After generating 4 directions, self-evaluate coverage (stolen from iDesignGPT):

```
Coverage check: Do these 4 directions span the design space?
- Axis 1: [complexity spectrum] -- covered by A (simple) and B (complex)
- Axis 2: [interaction model] -- covered by C (CLI) and D (GUI)
- Axis 3: [core mechanism] -- all 4 use the same mechanism (CLUSTERED)
  -> Regenerating Direction D to explore alternative mechanism
```

If directions are clustered on any major axis, regenerate the most expendable direction to cover the gap.

### Anti-Clustering Protocol

Stolen from BMAD brainstorming: "Consciously shift creative domain every N ideas to combat LLM semantic clustering."

Applied to /explore: each of the 4 directions must make a **fundamentally different bet on a different axis**, not just vary parameters of the same approach. The existing direction divergence strategy (lines 165-174 of explore/SKILL.md) is good but needs the coverage check as a verification step.

## Changes to explore/SKILL.md

1. Add quick scout call before `generate_directions()` (gated on register + existing scout reports)
2. Add Landscape line to direction output format
3. Add coverage self-check after direction generation
4. Add anti-clustering regeneration if coverage check fails

## Effort Estimate

Medium. Requires /scout infrastructure (03-scout-skill.md). The coverage check and anti-clustering protocol are prompt engineering changes.

## Prior Art

- **iDesignGPT** (Nature): Design space exploration with coverage, diversity, and novelty metrics
- **Schemex** (arXiv): Cluster -> Abstract -> Refine for discovering patterns from examples
- **BMAD brainstorming**: Anti-bias protocol shifting creative domain every 10 ideas
- **OpenSpec /opsx:explore**: Purely conversational exploration, no artifacts until crystallization
