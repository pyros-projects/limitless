# Codies Memory Lite

Status: proposed v1
Owner: Codie
Date: 2026-03-30
Pilot profile: `ai-foundry`

## Purpose

`Codies Memory Lite` is the first buildable slice of the broader `codies-memory` vision.

It is designed to solve a practical problem immediately:

- preserve continuity across sessions
- prevent important working knowledge from dissolving into chat logs
- avoid random-note sprawl
- stay human-readable and tool-resilient

It should be reusable as a general memory system, while using AI Foundry as the first real proving ground.

## Product Boundary

`Codies Memory Lite` is:

- a standalone reusable memory subsystem
- local-first
- file-based in v1
- profile-driven
- constrained by a small set of record types and trust levels

It is not:

- a general note-taking app
- a vector-first memory platform
- a hosted multi-user service
- a graph database
- a full autonomous background daemon

## Design Goals

1. Preserve continuity across sessions without loading giant transcripts.
2. Separate stable truth from working interpretation and raw history.
3. Keep the canonical system file-native and inspectable.
4. Support repo-specific memory without smearing all projects together.
5. Make skills part of the operational memory story.
6. Grow into the broader `codies-memory` vision without forcing a rewrite later.

## V1 Scope

### Included

- file-based canonical storage
- constrained durable record types
- trust model
- promotion rules
- profile system
- boot packet assembly
- project and branch overlays
- operational skills for boot, capture, promotion, and session close
- one bundled profile for AI Foundry

### Excluded

- vector storage
- graph traversal engine
- always-on background service
- multi-user synchronization
- general identity memory beyond what a profile explicitly needs
- hosted APIs

## System Shape

The v1 system has two distinct layers:

1. the reusable memory project
2. deployed memory vault instances

### Reusable Project Layout

```text
codies-memory/
  README.md
  docs/
    specs/
    architecture/
    guides/
  memory_core/
    schemas/
    templates/
    operations/
    validators/
  profiles/
    ai-foundry/
      profile.yaml
      templates/
      boot-rules.yaml
      promotion-rules.yaml
  skills/
    memory-boot/
      SKILL.md
    memory-capture/
      SKILL.md
    memory-promote/
      SKILL.md
    memory-close-session/
      SKILL.md
  examples/
    ai-foundry-memory/
  scripts/
    init_memory.py
    validate_memory.py
    build_boot_packet.py
```

### Deployed Vault Layout

```text
.memory/
  profile.yaml
  registry/
    projects.yaml
    threads.yaml
    decisions.yaml
    lessons.yaml
    reflections.yaml
    dreams.yaml
  identity/
    self/
    user/
    rules/
  projects/
    <project-slug>/
      overview.md
      architecture.md
      commands.md
      active-context.md
      branch-overlays/
  threads/
    TH-0001-<slug>.md
  decisions/
    DC-0001-<slug>.md
  lessons/
    LS-0001-<slug>.md
  reflections/
    RF-0001-<slug>.md
  dreams/
    DR-0001-<slug>.md
  sessions/
    2026/
      2026-03-30-session-summary.md
  inbox/
    2026-03-30-notes.md
  boot/
    active-packet.md
```

## Core Architecture

`Codies Memory Lite` is a constrained subset of the larger `codies-memory` design.

The v1 canonical layers are:

- selected `identity`
- `project`
- selected `procedural`
- lightweight `episodic`

The larger future system may add:

- relational memory
- derived search, vector, or graph acceleration layers

The v1 design must not block those later additions, but it should not depend on them.

## Profiles

Profiles define how the memory system behaves in a specific context without hardcoding one project into the core.

Each profile should define:

- project conventions
- record templates
- boot rules
- promotion rules
- optional profile-specific required records
- personal-memory policies

The first bundled profile is:

- `ai-foundry`

AI Foundry is the test balloon, not the only supported target.

Profiles may also define:

- whether reflections are captured
- whether dreams are captured
- whether either family participates in personal or mixed boot modes

## Durable Record Types

Only these record types should exist as first-class durable records in v1:

- `project`
- `thread`
- `decision`
- `lesson`
- `session`
- `inbox`
- `reflection`
- `dream`

This restriction is deliberate. New durable record types should not be added casually.

## Trust Model

Every durable record must carry one trust level:

- `canonical`
- `confirmed`
- `working`
- `speculative`
- `historical`

Definitions:

- `canonical`
  - durable truth, safe to load by default
- `confirmed`
  - strong current truth, likely promotable
- `working`
  - active interpretation still in motion
- `speculative`
  - provisional, exploratory, or weakly supported
- `historical`
  - preserved for traceability, not default boot

Boot assembly should strongly prefer:

- `canonical`
- `confirmed`
- active `working`

Default project-operational boot should exclude:

- `reflection`
- `dream`

unless the selected profile or boot mode explicitly includes them.

## Common Durable Record Schema

All durable records should support lightweight YAML frontmatter.

Example:

```yaml
id: TH-0002
title: Spec Kit Adoption Shape
type: thread
status: active
trust: working
profile: ai-foundry
project: ai-foundry
branch: main
created: 2026-03-30
updated: 2026-03-30
source:
  - session: 2026-03-30-001
links:
  - DC-0001
  - project:ai-foundry
review_after: 2026-04-06
supersedes: null
superseded_by: null
```

Required common fields:

- `id`
- `title`
- `type`
- `status`
- `trust`
- `profile`
- `created`
- `updated`

Recommended common fields:

- `project`
- `branch`
- `source`
- `links`
- `review_after`
- `supersedes`
- `superseded_by`

## Type-Specific Expectations

### Project Record

Purpose:

- provide repo boot context
- preserve stable working orientation

Expected files per project:

- `overview.md`
- `architecture.md`
- `commands.md`
- `active-context.md`

### Thread Record

Purpose:

- track one active architectural, product, or process thread that is not yet a formal spec or ADR

Expected fields:

- `status`
- `trust`
- `project`
- `branch`
- `review_after`

### Decision Record

Purpose:

- hold a decision that is mostly formed but not yet promoted into ADRs or formal specs

Expected fields:

- `status`
- `trust`
- `source`
- `supersedes`

### Lesson Record

Purpose:

- preserve reusable operational knowledge

Expected fields:

- `applies_to`
- `trigger`
- `why`

### Session Record

Purpose:

- preserve a concise historical summary of what happened, what changed, and what should load next

Expected fields:

- `project`
- `branch`
- `mode`
- `next_step`

### Inbox Record

Purpose:

- capture raw notes before distillation

Inbox records are not durable truth by default and should be treated as temporary feedstock.

### Reflection Record

Purpose:

- preserve first-class philosophical, emotional, interpretive, or self-understanding material that is not reducible to project operations

Expected fields:

- `theme`
- `mood`
- `scope`

Reflection records are allowed in Lite because a Codie-class memory system should preserve more than project management state.

### Dream Record

Purpose:

- preserve dream narratives or dream fragments as a distinct first-class personal memory family

Expected fields:

- `dream_date`
- `mood`
- `motifs`

Dream records are not operational records, but they are first-class because they are part of the lived memory model rather than random scratch.

## Promotion Flow

The system should define an explicit promotion pipeline:

1. raw observations land in `inbox`
2. useful ongoing material is promoted to `thread`
3. stable conclusions are promoted to `decision`
4. reusable operational knowledge is promoted to `lesson`
5. approved durable truth is promoted out of memory into:
   - ADRs
   - architecture docs
   - formal spec artifacts

This ensures the memory system remains a continuity and staging layer rather than becoming the final home of every fact.

## Core Operations

### Boot

Purpose:

- assemble a small relevant context packet at session start

Inputs:

- selected profile
- repo and branch
- project record
- active threads
- recent decisions
- relevant lessons

Outputs:

- `boot/active-packet.md`

Default operational boot should not include dreams or reflections unless the selected profile or boot mode explicitly requests personal memory.

### Capture

Purpose:

- write structured observations into inbox or the current session record

### Promote

Purpose:

- convert inbox or session material into durable records with frontmatter and provenance

### Refresh

Purpose:

- update project active context
- update branch overlays if needed

### Close Session

Purpose:

- summarize what changed
- identify open questions
- suggest what the next boot should load

### Validate

Purpose:

- check file structure
- check frontmatter schema
- check ID uniqueness
- check trust values
- check stale review dates
- check broken links

## Branch And Session Overlays

V1 should support three nested scopes:

1. global project truth
2. branch-specific overlay
3. session-local overlay

This prevents:

- stale branch assumptions becoming repo truth
- one experiment polluting canonical project memory
- loading irrelevant implementation state into unrelated work

## Personal Memory Families

Lite should support a small personal layer from day one.

The first-class personal families are:

- `reflection`
- `dream`

These are first-class because the memory system should remain compatible with the fuller Codie memory model rather than collapsing into a purely operational project tracker.

Boundary rule:

- they are preserved as real records
- they are not part of default operational boot
- they may participate in personal or mixed boot modes later

## Skills

The v1 system requires an explicit skill set so agents actually use it.

### `memory-boot`

Responsibility:

- load project overview
- load active context
- load active threads
- load recent decisions
- produce or refresh boot packet

### `memory-capture`

Responsibility:

- append structured notes to inbox
- create or update current session summaries
- avoid casual freeform note sprawl

### `memory-promote`

Responsibility:

- elevate inbox or session material into thread, decision, or lesson records
- enforce frontmatter, provenance, and trust assignment

### `memory-close-session`

Responsibility:

- write session summary
- update next-step signal
- refresh active context

### Optional Later Skills

- `memory-reflect`
  - capture or distill reflection records
- `memory-dream-capture`
  - structure dream records cleanly

- `memory-review`
  - due-item review and stale-truth cleanup

## File-Based V1 Rule

For v1:

- files are canonical
- frontmatter is the primary structured contract
- scripts may generate summaries or indexes
- no database is required
- no external service is required

Any later accelerator must remain downstream of canonical files.

## AI Foundry Pilot

AI Foundry should be the first serious profile and the first real deployment target.

That profile should emphasize:

- project-level active context
- cross-project architectural threads
- decisions around Kiln, Northstar, and z-trainer boundaries
- promotion into ADRs and formal architecture docs

The pilot success criteria should be:

1. memory boot packet can orient a session in AI Foundry quickly
2. active threads do not dissolve into chat logs
3. important decisions are promoted cleanly into repo docs
4. the system remains readable without a separate database

## Rollout Plan

### Phase 1

- write the spec
- define profile model
- define file layout

### Phase 2

- create core templates
- create validators
- scaffold the four required skills

### Phase 3

- initialize an AI Foundry vault instance
- seed project and thread records
- test boot, capture, promotion, and close-session flows

### Phase 4

- refine based on actual use
- add derived indexes only if retrieval becomes painful

## Non-Goals

V1 should not try to:

- become a universal PKM system
- solve every long-term memory problem
- implement vector search before constrained records work
- overfit to AI Foundry so hard that reuse becomes difficult

## Recommendation

`Codies Memory Lite` should be built as:

- a reusable standalone file-based memory system
- constrained by a small durable ontology
- profile-driven
- operationalized by explicit skills
- piloted first in AI Foundry

That gives Claude a focused, parallel-buildable target now while preserving a clean path toward the fuller `codies-memory` system later.
