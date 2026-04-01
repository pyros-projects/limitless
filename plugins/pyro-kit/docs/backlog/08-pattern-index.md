# Pattern Index: Technical Learnings Across Projects

**Status:** Proposed
**Priority:** Medium
**Affects:** /autopsy, /build, /contract, /spark
**Inspired by:** Compound Engineering /ce:compound, Codie's Memory procedural layer, Roampal pattern promotion

---

## Problem

Pyro Kit's fascination index compounds **what interests you** across projects. But there's no equivalent for **what you've learned technically**. Each new project starts from zero on technical patterns:

- "Last time I used SQLite for local state and it worked great" -- not captured
- "Event sourcing was overkill for a solo project" -- not captured
- "The propose-react-iterate pattern works for CLI design" -- captured in SFD whitepaper but not in project-level memory

Compound Engineering's `/ce:compound` solves this by documenting solved problems into `docs/solutions/` with YAML frontmatter. But it's project-scoped, not cross-project.

## Proposal

Add `~/.pyro/patterns.md` (global, cross-project) as a companion to the fascination index.

### Schema

```markdown
---
patterns_count: {N}
last_updated: {date}
---

## Patterns

### P1: {Pattern Name} -- {date}
**Learned in:** {project name}
**Category:** architecture | tooling | interaction | process | anti-pattern
**Pattern:** {What works or doesn't work, concisely}
**Evidence:** {Specific experience -- what happened}
**Confidence:** confirmed | working | speculative
**Projects using:** [{list of projects where this applies}]

### P2: ...
```

### Example Entries

```markdown
### P3: SQLite for local state -- 2026-02-20
**Learned in:** pyro-kit
**Category:** tooling
**Pattern:** For solo-dev tools with local state, SQLite is always the right choice over custom file formats. The query capability pays for itself within a week.
**Evidence:** Started with YAML files for pyro-kit state, migrated to SQLite after state queries became unwieldy. Migration took 2 hours. Should have started there.
**Confidence:** confirmed
**Projects using:** [pyro-kit, codies-memory]

### P7: Propose-react-iterate beats Socratic questioning -- 2026-03-01
**Learned in:** pyro-kit (SFD research)
**Category:** interaction
**Pattern:** When a user has strong evaluative taste but weak generative ability, proposing concrete options and iterating on reactions converges faster than asking questions.
**Evidence:** Validated across 4 SFD case studies (whitepaper Appendix C). User explicitly rejected Socratic questioning in brainstorming tools.
**Confidence:** confirmed
**Projects using:** [pyro-kit, sfd-whitepaper]
```

### How Patterns Flow

**Write path:**
- `/autopsy` extracts technical patterns from the completed/shelved project and appends to patterns.md
- Manual: developer can run `/pattern "learned X from Y"` to capture a pattern immediately

**Read path:**
- `/spark` reads patterns.md to avoid suggesting project shapes that conflict with known anti-patterns
- `/contract` reads patterns.md to suggest technical choices aligned with confirmed patterns
- `/build` reads patterns.md to select tools and architectures that have worked before
- `/explore` reads patterns.md to flag when a direction conflicts with a learned lesson

### Promotion

Patterns follow a confidence lifecycle similar to Codie's Memory:
```
speculative -> working -> confirmed
```

A pattern starts as `speculative` when first captured. After it's validated in a second project, it becomes `working`. After 3+ projects, `confirmed`.

Anti-patterns follow the same lifecycle -- a pattern that repeatedly causes problems gets promoted to a confirmed anti-pattern.

## Interaction with Fascination Index

The fascination index tracks **what interests you** (themes, curiosities, emotional pulls).
The pattern index tracks **what you've learned** (technical decisions, architectural lessons, process insights).

Together they answer: "What should I build next (fascination) and how should I build it (patterns)?"

## Effort Estimate

Medium. New global file + append logic in /autopsy + read integration in /spark, /contract, /build, /explore. Optional: new `/pattern` micro-skill for immediate capture.

## Prior Art

- **Compound Engineering /ce:compound**: Documents solved problems to `docs/solutions/` with YAML frontmatter, category-based organization, 5 parallel subagents for comprehensive capture
- **Codie's Memory procedural layer**: Reusable methods, debugging heuristics, configuration recipes
- **Roampal pattern promotion**: Score-based promotion with confidence levels and usage tracking
