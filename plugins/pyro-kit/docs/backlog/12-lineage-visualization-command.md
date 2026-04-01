# Lineage Visualization Command (/lineage)

**Status:** Proposed
**Priority:** High
**Affects:** /pyro orchestrator, /spark, /explore, /narrow, /surface, /contract, /build, /pulse, /autopsy
**Inspiration:** `_bmad-output/planning-artifacts/ux-comparison-lineage.html`

---

## Why this is a strong idea

This is exactly the kind of missing interface for creative projects:
- text files hold the state, but they do not show the shape of the journey
- decisions are hard to feel as a sequence of forks and commitments
- momentum and abandonment risk are easier to notice visually than in prose

Pyro Kit already captures rich process artifacts; this command turns them into a narrative map.

## Problem

Today, understanding "what happened so far" requires manually reading multiple files:
- `.pyro/state.md`
- `.pyro/spark.md`
- `.pyro/explore.md`
- `.pyro/surface.md`
- `.pyro/contract.md`
- `.pyro/decisions.md` (proposed)

This makes retrospection and course correction slow, especially after session gaps.

## Proposal

Add a command that generates a self-contained interactive HTML visualization of project lineage.

### Command

```
/lineage
/lineage --open
/lineage --project <path>
/lineage --format html|md
```

Default output path:
`._pyro-output/lineage/lineage-YYYY-MM-DD-HHMM.html`

### What it visualizes

1. **Phase timeline**
   - spark -> explore -> narrow -> surface -> contract -> build
   - timestamps and duration between milestones

2. **Decision graph**
   - each major decision node
   - alternatives considered/rejected
   - edges showing decision dependencies

3. **Branch lineage**
   - direction forks from /explore
   - selected branch and dead branches
   - optional merge markers if branches are revisited

4. **Momentum signals**
   - iteration velocity
   - session gaps
   - commit trend (if git available)
   - pulse events and risk windows

5. **State snapshots**
   - quick cards for Spark summary, locked direction, current scope, unresolved questions

### Interaction model (HTML)

- zoom/pan timeline
- toggle lanes (decisions, phases, momentum, branches)
- click node -> side panel with source excerpts and file references
- filter by phase or date window
- export PNG or markdown summary

## Data sources

- `.pyro/state.md` -- current phase, last activity
- `.pyro/spark.md` -- initial idea and tensions
- `.pyro/explore.md` -- directions, contrasts, leaning, lock event
- `.pyro/surface.md` -- flow evolution and edge cases
- `.pyro/contract.md` -- freeze and constraints
- `.pyro/decisions.md` -- structured decision history
- git log (optional) -- timeline correlation and momentum

## Minimal MVP

Start with static HTML (no framework):

1. **Timeline lane** (phase events)
2. **Decision lane** (top 10 decisions with links)
3. **Current state card**
4. **Momentum strip** (days active vs idle)

No heavy graph engine required initially; CSS + vanilla JS is enough.

## How this improves Pyro Kit

- **Faster re-entry:** one glance to understand current context after time away
- **Better reflection:** makes hidden patterns visible (scope creep, oscillation, repeated reversals)
- **Trust calibration:** shows why current state exists (traceability from decisions to output)
- **Anti-abandonment:** visual idle zones and decision droughts are immediate warning signs

## Future extensions

- portfolio view across multiple projects (`/lineage --portfolio`)
- compare two lineage snapshots to show drift
- anomaly detection: "you've reversed direction 4 times in 6 days"
- "what changed since last week" automatic digest

## Effort Estimate

Medium.

- MVP: Medium-Low (single HTML generator)
- Full interactive graph + portfolio mode: Medium-High

## Open Questions

- Should /lineage auto-generate on every phase transition, or only on explicit command?
- Should unresolved questions/deferred items be a separate lane?
- Should this live in `.pyro/` (state) or `._pyro-output/` (derived artifact)?
