# Schemas And Operations

## Canonical Record Schema

Every durable record should support lightweight frontmatter like:

```yaml
title: Example Record
type: lesson
scope: procedural
status: confirmed
confidence: high
support_count: 3
success_count: 2
contradiction_count: 0
retrieval_count: 4
project: null
branch: null
intent:
  - debug
  - review
skills:
  - systematic-debugging
created: 2026-03-13
updated: 2026-03-13
source:
  - session: 2026-03-13-2302
  - file: codex/sessions/Session Log - ...
supersedes: null
superseded_by: null
review_after: 2026-03-20
probation_until: 2026-03-20
links:
  - project:z-trainer
  - skill:systematic-debugging
```

This is enough to support:

- file-native readability
- derived indexes
- ranked retrieval
- provenance tracking

## Suggested Record Types

### Identity Record

Fields:

- `subject`
- `stability`
- `validation_rule`

### Lesson Record

Fields:

- `pattern`
- `trigger`
- `why`
- `applies_to`

### Project Record

Fields:

- `project`
- `branch`
- `status`
- `last_verified`
- `overlay_state`

### Session Record

Fields:

- `project`
- `branch`
- `mode`
- `artifacts`
- `next_step`
- `write_gate_summary`

### Relationship Record

Fields:

- `from`
- `relation`
- `to`
- `confidence`
- `source`
- `evidence_count`

## Supersession Fields

Durable records that may evolve should support:

- `supersedes`
- `superseded_by`

The default update rule should be:

- append a new record when the belief materially changes
- do not silently rewrite old confirmed records when forensic history matters

## Operational Flows

### Session Start Flow

1. detect repo and branch
2. check whether daily maintenance is due
3. load identity essentials
4. load project brain
5. load branch overlay if present
6. load last session summary
7. load top procedural reminders by likely intent
8. assemble or reuse cached boot packet

### During Work

1. capture important events into episodic memory
2. apply write gates to new observations
3. update project working state if a material local truth changes
4. retrieve intent-shaped procedural memory when mode shifts
5. record candidate lessons when reusable patterns appear

Project-state mutation should use a single-writer rule within a given project scope.

### Session End

1. write session log
2. extract candidate lessons and project updates
3. update project active context
4. compact temporary scratch into a summary with source links
5. queue uncertain promotions for later review
6. enqueue overdue maintenance if encountered

## Maintenance Cadences

### Per Session

- boot
- capture
- distill

### Daily

- compact noisy scratch
- merge duplicate candidate records
- refresh active project overlays
- surface review items whose `review_after` is due

### Weekly

- review stale project state
- inspect highly retrieved episodic records
- promote proven patterns
- archive dead branch overlays

### Monthly

- validate identity records
- prune contradictory preferences
- rebuild derived indexes if needed
- review long-lived probationary or conflicting records

## Maintenance Triggers

Cadence should be enforced by the system, not by hope.

- daily work is checked at session start
- weekly and monthly work enters the memory review queue when due
- merged branch overlays should enqueue a promotion review automatically
- contradictory promotions should enqueue a poisoning review automatically

## Derived Layer Operations

### Search Index

Purpose:

- fast lexical lookup
- exact-match and nearby-match retrieval

Can be rebuilt at any time.

### Vector Index

Purpose:

- semantic similarity
- fuzzy recall for older or differently worded records

Should be treated as advisory, never authoritative.

### Entity Graph

Purpose:

- cross-project and cross-skill connections
- better context assembly

Should stay lightweight.
The graph is a servant of the files, not the owner of them.

Initial relational constraints:

- keep traversal depth shallow by default, such as `1-2` hops
- prefer typed links over open-ended graph expansion
- do not let graph traversal bypass trust and scope filters

## Failure Modes And Defenses

### Failure: Memory Bloat

Defense:

- promotion gates
- compact summaries
- review queue

### Failure: Stale Project Truth

Defense:

- branch overlays
- last-verified fields
- recovery retrieval

### Failure: Skill Over-Application

Defense:

- skill experience cards
- record "overkill" contexts explicitly

### Failure: Contradictory Durable Records

Defense:

- provenance metadata
- explicit trust statuses
- review queue for conflicts
- supersession chains instead of silent overwrite

### Failure: Memory Poisoning

Defense:

- probation windows on new promotions
- contradiction-triggered demotion
- review queue for collisions with confirmed records

### Failure: Tool Dependency Rot

Defense:

- filesystem-first truth
- rebuildable indexes
- plain text records
