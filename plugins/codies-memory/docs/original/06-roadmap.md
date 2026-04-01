# Roadmap

This design is intentionally more ambitious than the current `basic-memory` usage pattern.
The right implementation path is incremental.

## Phase 1: Clean Layering

Goal:

- separate existing memory into explicit layers

Work:

- define canonical folders
- normalize frontmatter
- tag current records by scope and trust
- create a stable project-brain template
- add supersession and review metadata to durable records

Success criteria:

- identity, procedural, project, and episodic records are visibly distinct
- booting a session no longer depends on reading arbitrary files by habit

## Phase 2: Memory Products

Goal:

- generate high-value working views

Work:

- boot packet generator
- project brain views
- session distiller
- lesson promotion queue
- boot packet cache and truncation policy
- write gates for captured observations

Success criteria:

- session start becomes compact and reliable
- repeated session review work decreases

## Phase 3: Skill-Aware Retrieval

Goal:

- bind skills to lived procedural memory

Work:

- add skill companion records
- track pairings, overkill contexts, and repo-specific adaptations
- surface skill-aware context assembly

Success criteria:

- skill choice feels informed by experience, not just by static matching

## Phase 4: Relational Layer

Goal:

- make cross-project and cross-concept memory navigable

Work:

- entity and link extraction
- lightweight graph index
- relation-aware search and context assembly

Success criteria:

- easier recovery of "how does this connect to that"
- less manual stitching across old research and sessions

## Phase 5: Review And Compaction Automation

Goal:

- prevent silent memory decay

Work:

- stale record detection
- contradiction queue
- high-retrieval episodic review queue
- branch overlay cleanup
- probation and rollback handling for new promotions

Success criteria:

- memory quality stays high without massive manual gardening

## What I Would Build First

If I were really implementing this tomorrow, I would start with:

1. boot packet generator with cache and token budget
2. session distiller with write gates
3. lesson promoter with simple promotion thresholds and probation windows
4. explicit layered folder structure
5. project brain template
6. supersession-chain support in the frontmatter schema

That order gives the highest practical gain fastest.

## Non-Goals

Not trying to build:

- a giant cloud memory SaaS
- an opaque vector-first memory black box
- a fully autonomous self-editing memory graph from day one
- a replacement for skills

This system should strengthen skills and continuity, not replace disciplined workflow.
