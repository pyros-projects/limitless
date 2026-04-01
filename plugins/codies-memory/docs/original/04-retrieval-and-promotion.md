# Retrieval And Promotion

## Core Rule

Capture broadly.
Promote narrowly.
Retrieve intentionally.
Compact continuously.

## The Promotion Pipeline

### Stage 1: Capture

New information lands in `episodic` memory unless one of these is true:

- it is already known to be a durable identity rule
- it is an explicit "remember this" request
- it is a confirmed project-state mutation

### Stage 2: Write Gate

Each captured observation should be classified before candidate extraction:

- `allow`: eligible for default episodic retrieval and candidate extraction
- `hold`: preserved, but excluded from default retrieval until reinforced
- `discard`: dropped from behavioral memory because it is judged to be noise

The default bias should be toward `hold`, not `allow`.
This prevents low-grade session residue from flooding the candidate pool.

### Stage 3: Candidate Extraction

At session end or during compaction, the system identifies candidates for promotion:

- lesson candidates
- project update candidates
- preference candidates
- relationship candidates

Each candidate should include provenance and confidence.

Each candidate should also track lightweight reinforcement signals:

- `support_count`
- `success_count`
- `contradiction_count`
- `last_seen`
- `retrieval_count`

### Stage 4: Validation

Before promotion, ask:

- is this general or only situational
- is it still true
- is it already represented elsewhere
- does it belong in identity, procedure, project, or relation
- should it remain a candidate instead

### Validation Operator

Validation should use a hybrid operator:

1. agent extraction proposes the candidate
2. rule-based heuristics score reinforcement and risk
3. low-risk cases may auto-promote
4. high-risk, identity-affecting, or conflicting cases enter the review queue

This avoids two bad extremes:

- pretending the agent can safely self-canonize everything
- making every useful memory wait for human review forever

### Stage 5: Promotion

Only after validation should a record move into:

- `identity`
- `procedural`
- `project`
- `relational`

Promotion thresholds should start simple and become more precise only after real data exists.

Suggested initial thresholds:

- `episodic -> project`: explicit confirmed mutation, or repeated project-local observation across `>= 2` sessions
- `episodic -> procedural`: `support_count >= 3`, `success_count >= 2`, and no unresolved contradiction
- `episodic -> relational`: repeated reference across `>= 2` contexts
- `episodic -> identity`: explicit "remember this" or review-required stable signal; do not auto-promote from one inferred observation
- `candidate -> confirmed`: survives probation window without contradiction and is retrieved or reinforced again

These are deliberately rough starting rules, not sacred numbers.

### Stage 6: Compaction

The original episodic record remains, but retrieval preference shifts toward the promoted record and its summary.

Compaction should never destroy forensic traceability.

The compaction output should contain:

- a compact summary
- links to the source record(s)
- retained blocker or contradiction markers if unresolved

An episodic record is safe to compact when:

- it is outside the active session window
- its important outcomes have been distilled
- it has no unresolved blocker requiring foreground visibility

### Stage 7: Probation, Demotion, And Rollback

New promotions should enter a probation period before being treated as settled memory behavior.

During probation:

- contradictory evidence can demote the record back to candidate
- stronger newer records can supersede it
- the review queue should surface conflicts early

This is the primary defense against memory poisoning from confidently wrong sessions.

## Retrieval Modes

### 1. Boot Retrieval

Used at session start.

Priority order:

1. identity essentials
2. current project brain
3. branch overlay
4. last relevant session summary
5. top procedural reminders

Strict budget:

- small
- high confidence
- low noise

Default target budget:

- roughly `3K-4.5K` tokens total

Boot retrieval should also support cached reuse keyed by the source hashes of the records that fed it.

### 2. Intent Retrieval

Used when work mode is known.

Intent classes:

- implement
- debug
- review
- research
- brainstorm
- plan
- document

For each intent, retrieval should prefer:

- matching project records
- matching procedural records
- recent relevant episodes
- linked skills and lessons

### 3. Recovery Retrieval

Used when I need to resume after interruption.

Priority order:

- current branch state
- current blocker
- last unfinished action
- decision trail leading to the current state
- exact next step if known

### 4. Forensic Retrieval

Used when something seems contradictory.

Priority order:

- provenance chain
- older versions of the same belief
- conflicting project notes
- session records that created the conflict

This is where historical memory matters more than compactness.

## Ranking Rules

Ranking should not be semantic-only.
Use a weighted blend of:

- scope match
- intent match
- project match
- branch match
- trust level
- recency
- explicit link distance
- retrieval history
- reinforcement signals
- contradiction penalties

This produces better behavior than pure embedding similarity.

The system does not need full statistical confidence modeling on day one.
Simple counts and penalties are enough for the first implementation as long as provenance remains intact.

## What Skills Change

Skills should influence retrieval in two ways.

### 1. Skill-Triggered Retrieval

If a skill is active, the system should load:

- the skill's companion record
- recent lesson cards for that skill
- common failure patterns
- repo-specific adaptations

### 2. Skill Suggestion Retrieval

If the task intent resembles a known skill posture, the system should surface candidate skills and supporting procedural memory.

This turns the memory system into a behavior shaper, not just an archive.

## Promotion Heuristics By Memory Type

### Promote To Identity When

- it is stable across sessions
- it affects collaboration or safety
- it clearly describes Codie, Pyro, or a standing rule

### Promote To Procedural When

- it is reusable across repos
- it encodes a successful operating pattern
- it prevents repeated mistakes

### Promote To Project When

- it changes how work in one repo should proceed
- it captures architecture, commands, or known blockers
- it should be loaded when entering that repo again

### Promote To Relational When

- the connection itself is useful
- the same relationship is referenced from multiple contexts

## Supersession

Promoted memory should evolve by supersession rather than silent overwrite.

If a lesson, project belief, or preference changes materially:

- create a new record
- link it to the older record
- let retrieval prefer the newer confirmed version
- preserve the older one for forensic retrieval

This is how "older versions of the same belief" become real instead of rhetorical.

## Anti-Patterns

### Anti-Pattern: Promote Everything

Result:

- bloated durable memory
- conflicting rules
- bad boot packets

### Anti-Pattern: Search Everything Every Time

Result:

- noisy retrieval
- weak task focus
- slower reasoning

### Anti-Pattern: Store Facts Without Scope

Result:

- branch leakage
- project contamination
- stale assumptions

### Anti-Pattern: Treat Skills As Detached Manuals

Result:

- poor skill selection
- repeated overuse or underuse
- no learning from actual use

## My Ideal End-State

I should be able to start a session and feel:

- oriented
- bounded
- up to date
- not overloaded

That is the real success criterion for retrieval and promotion.
