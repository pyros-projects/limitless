# Memory Products

This memory system should expose a few high-value products instead of forcing every workflow to read raw files.

## 1. Boot Packet

Purpose:

- assemble the minimum useful context for starting work

Contents:

- identity essentials
- user preferences relevant to the current mode
- project overview
- active branch overlay
- last session summary
- active blockers
- top 3 relevant lessons
- top 3 relevant skills or procedural reminders

Properties:

- compact
- mode-aware
- generated on demand
- discardable after use
- cacheable by source hash

### Budget

The boot packet should have a default target budget of roughly `3K-4.5K` tokens total.

Suggested allocation:

- identity essentials: `<= 1K`
- project brain summary: `<= 1K`
- branch overlay: `<= 500`
- last session summary: `<= 500`
- procedural reminders: `<= 1K`

If the budget is exceeded, truncation should happen in this order:

1. reduce procedural reminder count
2. compress the last session summary
3. compress branch details
4. never drop identity essentials entirely

### Cache Behavior

The boot packet should be cached using a source-hash or equivalent delta key.

If the inputs have not changed, reuse the existing packet instead of regenerating it.
This keeps startup fast and avoids spending context budget on recomputation logic.

## 2. Project Brain

Purpose:

- provide a stable, navigable memory surface for one repo

Contents:

- what this repo is
- how it is structured
- how to run it
- what is active now
- where risk lives
- open architectural questions
- recent important decisions

Properties:

- one per project
- partly human-authored, partly distilled
- primary context source for planning and implementation

## 3. Session Distiller

Purpose:

- convert raw session output into durable candidates

Outputs:

- session log
- candidate lessons
- candidate project-state changes
- candidate identity or preference updates
- compaction summary for future retrieval
- write-gate decisions for captured observations

Properties:

- conservative by default
- should prefer "candidate" over "promotion" unless confidence is high

### Write Gates

Before a captured observation becomes a promotion candidate, it should pass a write gate:

- `allow`: durable enough to retrieve by default
- `hold`: worth keeping, but excluded from default retrieval until promoted or re-seen
- `discard`: noise or one-off residue that should not shape memory behavior

This keeps episodic memory useful without pretending every observation deserves equal weight.

## 4. Lesson Promoter

Purpose:

- turn repeated or especially useful patterns into procedural memory

Good triggers:

- a reusable debugging heuristic
- a repeated workflow correction
- a failure pattern that wasted time more than once
- a strong project-agnostic practice worth preserving

## 5. Context Assembler

Purpose:

- gather the right memory slice for a task in progress

Inputs:

- task intent
- current repo
- current branch
- current skill posture

Outputs:

- ranked record set for immediate use

Examples:

### Debugging Assembly

- recent failures in this project
- debugging lessons
- project architecture seam map
- relevant tool or runtime caveats

### Planning Assembly

- project goals
- open decisions
- prior plans
- relevant spec or architecture rules

### Research Assembly

- previous market scans
- scoring methodology
- source reliability heuristics
- recent adjacent research notes

## 6. Memory Review Queue

Purpose:

- keep memory quality from degrading silently

Queue items:

- stale project state
- unconfirmed candidate lessons
- contradictory preference records
- identity records not validated in a long time
- episodic records with high retrieval frequency but no promotion
- merged branch overlays waiting for review
- recently promoted records still inside their probation window

This is the missing product in most memory systems.
Without it, the memory quietly becomes a landfill.

### Triggering

The review queue should not depend on human memory.

- overdue daily work should surface at session start
- weekly and monthly maintenance should appear as review queue items when due
- contradiction and poisoning checks should enqueue themselves when promotions collide

## 7. Skill Experience Cards

Purpose:

- make skill usage concrete and adaptive

Each card should capture:

- what the skill is for
- when it tends to help
- when it tends to be overkill
- which repos it worked well in
- which repos needed adaptation
- what common pairings improved results

This is especially important in a skill-heavy environment, because the system should not just know "a skill exists."
It should know what the skill feels like in real work.
