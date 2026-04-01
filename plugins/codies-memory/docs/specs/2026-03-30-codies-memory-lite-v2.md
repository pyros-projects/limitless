# Codies Memory Lite v2

Status: proposed
Owner: Codie (design), Claude (v2 revision)
Date: 2026-03-30
Pilot profile: `ai-foundry`

---

## Purpose

Codies Memory Lite is a file-based, two-tier memory system for AI agents.

It solves a practical problem: agents lose working knowledge between sessions. Chat logs dissolve. Random notes sprawl. Important decisions get buried. Context loading is either too thin (useless) or too thick (crowds out work).

This system provides structured continuity across sessions without requiring databases, hosted services, or giant transcript replays.

v2 introduces a two-tier architecture: global memory for identity and cross-project knowledge, project-local memory for working context. Global memory acts as the map that connects project memories.

---

## Core Rules

These are non-negotiable structural rules for the system.

1. `~/.memory/` owns identity, reflections, dreams, cross-project lessons, and the project registry.
2. `<project>/.memory/` owns project-local working memory only.
3. Project vaults are gitignored by default.
4. Durable shared truths must promote out of `.memory/` into committed repo artifacts (docs, ADRs, specs).
5. Boot is layered: global identity, then project context, then branch/session overlay.
6. Promotion thresholds and inbox cleanup rules are mandatory, not optional.

---

## Product Boundary

Codies Memory Lite is:

- a standalone reusable memory subsystem
- local-first
- file-based
- profile-driven
- two-tier (global + project)
- constrained by a small set of record types and trust levels

It is not:

- a general note-taking app
- a vector-first memory platform
- a hosted multi-user service
- a graph database
- a full autonomous background daemon
- a replacement for committed project documentation

---

## Design Goals

1. Preserve continuity across sessions without loading giant transcripts.
2. Separate stable truth from working interpretation and raw history.
3. Keep the canonical system file-native and inspectable.
4. Support repo-specific memory without smearing all projects together.
5. Connect project memories through a global registry and cross-project knowledge.
6. Make skills part of the operational memory story.
7. Grow into the broader codies-memory vision without forcing a rewrite.

---

## Principles

### 1. Filesystem Is Truth

All durable memory exists as human-readable local files. Vectors, graphs, and indexes are derived artifacts only. If they disappear, the memory system degrades, not collapses.

### 2. Separate Memory By Stability, Not By Format

The main split is not "Markdown vs database." The main split is: what is stable, what is provisional, what is situational, what is historical.

### 3. Promotion Beats Capture

Capture cheaply. Promote selectively. Retrieve intentionally. Compact aggressively. The quality of memory comes from promotion rules, not ingest volume.

### 4. Procedural Memory Matters More Than Trivia

The most valuable agent memory is operational: which skill applies, which verification prevents mistakes, which repo pattern means trouble.

### 5. Project Isolation Is Non-Negotiable

Different repos have different truths. Global memory holds what is true everywhere. Project memory holds what is true here.

### 6. Retrieval Should Be Intent-Shaped

Memory retrieval depends on what the agent is about to do. Debugging retrieves heuristics. Planning retrieves constraints. Research retrieves prior scans.

### 7. Provenance Is Part Of The Memory

Every promoted memory must answer: where did this come from, when was it last validated, who asserted it, what scope does it apply to.

### 8. Skills Are Memory-Bearing Objects

Skills become more useful when memory records where they helped, where they were overkill, and repo-specific adaptations.

### 9. Local-First Is A Design Constraint

The system works offline. Boot context does not depend on a hosted service. Raw memory is owned by the user.

---

## Two-Tier Architecture

The system has two tiers of memory storage.

### Tier 1: Global Memory (`~/.memory/`)

Global memory is the agent's identity and cross-project brain.

It contains:

- who the agent is (identity)
- who the user is (user context and preferences)
- standing rules that apply everywhere
- cross-project lessons and procedural knowledge
- skill experience cards
- the project registry (map of all known project vaults)
- cross-project threads and decisions
- personal memory (reflections, dreams)

Global memory is:

- small and stable
- loaded every session regardless of project
- the connective tissue between project vaults
- never committed to any project repo

### Tier 2: Project Memory (`<project>/.memory/`)

Project memory is the agent's working understanding of one specific project.

It contains:

- project overview and architecture context
- project-specific threads, decisions, and lessons
- branch overlays
- session history for this project
- inbox (raw observations awaiting distillation)
- boot packet for this project
- active context (what is happening right now)

Project memory is:

- scoped to one repo
- loaded only when working in that repo
- gitignored by default
- the staging area before truths promote into committed docs

### How The Tiers Relate

```text
~/.memory/
  registry/projects.yaml  ──references──>  project-a/.memory/
                           ──references──>  project-b/.memory/
                           ──references──>  project-c/.memory/

  procedural/lessons/      <──promotes──    project-a/.memory/lessons/
                           <──promotes──    project-b/.memory/lessons/

  identity/                ──loads into──>  every session boot
```

Global memory knows about every project vault through the registry.

Project lessons that prove reusable across repos promote upward into global procedural memory.

Identity and global procedural knowledge load into every session, regardless of which project is active.

---

## Global Memory Layout

```text
~/.memory/
  profile.yaml                              # default global profile
  registry/
    projects.yaml                           # map of all known project vaults
  identity/
    self.md                                 # who the agent is
    user.md                                 # who the user is
    rules.md                                # standing rules (always applicable)
  procedural/
    lessons/
      LS-G0001-<slug>.md                    # cross-project lessons
    skills/
      SK-0001-<slug>.md                     # skill experience cards
    playbooks/
      PB-0001-<slug>.md                     # reusable workflow patterns
  threads/
    TH-G0001-<slug>.md                      # cross-project threads
  decisions/
    DC-G0001-<slug>.md                      # cross-project decisions
  reflections/
    RF-0001-<slug>.md                       # personal reflections
  dreams/
    DR-0001-<slug>.md                       # dream records
  boot/
    global-packet.md                        # cached global boot context
```

ID prefixes:

- `G` prefix on lessons, threads, and decisions indicates global scope
- IDs without `G` are project-local
- This prevents collisions when records promote from project to global

---

## Project Memory Layout

```text
<project>/.memory/
  profile.yaml                              # project-specific profile overrides
  project/
    overview.md                             # what this project is
    architecture.md                         # how it is structured
    commands.md                             # how to run it
    active-context.md                       # what is happening right now
    branch-overlays/
      <branch-slug>.md                      # branch-specific working state
  threads/
    TH-0001-<slug>.md                       # project-local threads
  decisions/
    DC-0001-<slug>.md                       # project-local decisions
  lessons/
    LS-0001-<slug>.md                       # project-local lessons
  sessions/
    <YYYY>/
      <YYYY-MM-DD>-session-summary.md       # session records
  inbox/
    <YYYY-MM-DD>-notes.md                   # raw observations
  boot/
    active-packet.md                        # cached project boot context
```

---

## Memory Layers

The system uses four canonical memory layers. The two-tier architecture determines where each layer lives.

### Layer 1: Identity

What is stable about the agent, the user, and the collaboration.

Lives in: `~/.memory/identity/`

Characteristics: small, highly stable, loaded every session, low write frequency, high trust threshold.

### Layer 2: Procedural

Operational knowledge: lessons, skills, playbooks, heuristics.

Lives in: `~/.memory/procedural/` (cross-project) and `<project>/.memory/lessons/` (project-specific)

Characteristics: medium stability, reusable, retrieved by intent, promotion target for repeated session outcomes.

### Layer 3: Project

Working understanding of one repo: architecture, state, decisions, blockers.

Lives in: `<project>/.memory/project/` and related directories

Characteristics: scoped by repo, changes often, supports branch overlays, primary source for work boot.

### Layer 4: Episodic

Historical record: sessions, inbox, raw captures.

Lives in: `<project>/.memory/sessions/` and `<project>/.memory/inbox/`

Characteristics: append-heavy, noisy by design, low trust by default, primary feedstock for promotion.

### Future Layer: Relational

Connections between otherwise separate records. Not implemented in v1. The `links` field in the common schema provides basic relational support until a dedicated layer is built.

---

## Durable Record Types

Only these record types exist as first-class durable records in v1:

| Type | Scope | Purpose |
|------|-------|---------|
| `project` | project | repo boot context and stable orientation |
| `thread` | project or global | active architectural/process thread not yet formalized |
| `decision` | project or global | formed decision not yet promoted to ADR/spec |
| `lesson` | project or global | reusable operational knowledge |
| `session` | project | concise historical summary of what happened |
| `inbox` | project | raw notes before distillation (temporary) |
| `reflection` | global | philosophical/interpretive personal memory |
| `dream` | global | dream narratives as personal memory |
| `skill` | global | skill experience card |
| `playbook` | global | reusable workflow pattern |

New durable record types should not be added casually. Every new type needs a clear reason to exist separately from the existing types.

---

## Trust Model

Every durable record carries one trust level:

| Level | Meaning | Boot eligible |
|-------|---------|---------------|
| `canonical` | durable truth, safe to load by default | yes |
| `confirmed` | strong current truth, likely promotable | yes |
| `working` | active interpretation still in motion | yes (if active) |
| `speculative` | provisional, exploratory, weakly supported | no |
| `historical` | preserved for traceability, not default boot | no |

Boot assembly strongly prefers `canonical`, `confirmed`, and active `working` records.

Recently promoted records should be treated as probationary in behavior even if their trust label is `confirmed`. Probation is tracked through metadata (`probation_until`), not by inventing more trust states.

---

## Common Record Schema

All durable records use YAML frontmatter.

```yaml
id: TH-0002
title: Spec Kit Adoption Shape
type: thread
status: active
trust: working
scope: project                              # project | global
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
probation_until: null
```

### Required Fields

- `id`
- `title`
- `type`
- `status`
- `trust`
- `scope` (project or global)
- `created`
- `updated`

### Recommended Fields

- `profile`
- `project`
- `branch`
- `source`
- `links`
- `review_after`
- `supersedes`
- `superseded_by`
- `probation_until`

---

## Type-Specific Schemas

### Project Record

Purpose: provide repo boot context and preserve stable working orientation.

Expected files per project:

- `overview.md` — what this project is
- `architecture.md` — how it is structured
- `commands.md` — how to run it
- `active-context.md` — what is happening right now

Additional fields: none beyond common schema.

### Thread Record

Purpose: track one active architectural, product, or process thread that is not yet formalized.

Additional fields:

- `review_after` (required)

### Decision Record

Purpose: hold a decision that is mostly formed but not yet promoted into ADRs or formal specs.

Additional fields:

- `supersedes` (recommended)
- `rationale` (recommended)

### Lesson Record

Purpose: preserve reusable operational knowledge.

Additional fields:

- `applies_to` — what contexts this lesson is relevant to
- `trigger` — what situation activates this lesson
- `why` — the reason behind the pattern
- `support_count` — how many times this has been reinforced
- `success_count` — how many times it led to a good outcome

### Session Record

Purpose: preserve a concise summary of what happened, what changed, and what should load next.

Additional fields:

- `mode` — what kind of work was done (implement, debug, plan, research, etc.)
- `next_step` — what the next session should pick up
- `artifacts` — what was created or modified
- `write_gate_summary` — what was allowed, held, and discarded

### Inbox Record

Purpose: capture raw notes before distillation.

Inbox records are temporary feedstock, not durable truth. They follow a strict lifecycle (see Inbox Lifecycle section).

Additional fields:

- `gate` — `allow`, `hold`, or `discard`

### Reflection Record

Purpose: preserve philosophical, emotional, or self-understanding material not reducible to project operations.

Additional fields:

- `theme`
- `mood`

### Dream Record

Purpose: preserve dream narratives as distinct personal memory.

Additional fields:

- `dream_date`
- `mood`
- `motifs`

### Skill Record

Purpose: track operational experience with a specific skill.

Additional fields:

- `skill_name`
- `trigger_patterns` — when this skill applies
- `paired_skills` — skills commonly used together
- `effective_in` — repos/contexts where it works well
- `overkill_in` — repos/contexts where it was too much
- `failure_patterns` — known failure modes
- `adaptations` — repo-specific adjustments

### Playbook Record

Purpose: encode a reusable multi-step workflow pattern.

Additional fields:

- `steps` — ordered list of actions
- `applies_to` — contexts where this playbook is useful
- `trigger` — what situation activates this playbook

---

## Promotion Flow

Promotion happens in two dimensions:

### Dimension 1: Within A Project (vertical)

```text
inbox (raw observation)
  -> thread (active investigation)
  -> decision (formed conclusion)
  -> lesson (reusable pattern)
  -> promoted out to committed repo docs (ADR, spec, architecture doc)
```

### Dimension 2: Project To Global (horizontal)

```text
project lesson  ->  global lesson     (when proven across 2+ projects)
project thread  ->  global thread     (when it affects multiple projects)
project decision -> global decision   (when it applies cross-project)
```

### Promotion Thresholds

These are mandatory starting thresholds, not optional guidelines. They should be refined based on real usage, but they must exist from day one.

#### Within-Project Promotion

| From | To | Threshold |
|------|----|-----------|
| inbox | thread | agent identifies a recurring topic or active investigation across the session |
| inbox | lesson | observation is actionable and applies beyond this session |
| thread | decision | referenced across 2+ sessions OR explicitly confirmed by operator |
| thread | lesson | pattern proves reusable across 2+ sessions with positive outcomes |
| decision | committed docs | trust is `canonical` or `confirmed`, review_after has passed, no open contradictions |

#### Project-to-Global Promotion

| From | To | Threshold |
|------|----|-----------|
| project lesson | global lesson | observed in 2+ projects OR manually promoted by operator |
| project thread | global thread | affects 2+ projects OR manually promoted |
| project decision | global decision | applies to 2+ projects OR manually promoted |

#### Trust Elevation

| From | To | Threshold |
|------|----|-----------|
| speculative | working | agent is actively using this in current session |
| working | confirmed | survives 2+ sessions without contradiction, referenced again |
| confirmed | canonical | explicitly validated by operator OR stable across 5+ sessions |

#### Probation

All newly promoted records enter a 7-day probation window (`probation_until` field).

During probation:

- contradictory evidence can demote the record back to `working` or `speculative`
- stronger newer records can supersede it
- the record participates in boot and retrieval normally, but contradictions are flagged

---

## Boot Assembly

Boot is the process of assembling context at session start. It is layered.

### Boot Layers

```text
Layer 1: Global Identity (~/.memory/identity/)
  -> who am I, who is the user, standing rules
  -> always loaded, every session

Layer 2: Global Procedural (~/.memory/procedural/)
  -> cross-project lessons relevant to current work intent
  -> skills likely to apply
  -> loaded selectively based on intent

Layer 3: Project Context (<project>/.memory/project/)
  -> overview, architecture, active context
  -> always loaded when in a project

Layer 4: Project Working State (<project>/.memory/)
  -> active threads, recent decisions, recent lessons
  -> loaded based on relevance

Layer 5: Branch/Session Overlay
  -> branch-specific state, last session summary
  -> loaded when on a specific branch
```

### Token Budget

Boot must compete with task context for the context window. These are default target budgets:

| Layer | Target Budget |
|-------|---------------|
| Global identity | ~1,000 tokens |
| Global procedural (selected) | ~500 tokens |
| Project context | ~1,500 tokens |
| Project working state (threads, decisions) | ~500 tokens |
| Branch overlay + last session | ~500 tokens |
| **Total default boot** | **~4,000 tokens max** |

### Truncation Order

When budget is exceeded, truncate in this order (least important first):

1. Reduce number of procedural reminders
2. Compress last session summary
3. Compress branch overlay details
4. Reduce project working state to most recent/active items
5. Compress project context to overview only
6. **Never drop global identity**

### Cache Behavior

The boot packet should be cached using a source hash (hash of all input files).

If inputs have not changed since the last boot, reuse the cached packet. This avoids spending context budget on recomputation.

Two cached packets exist:

- `~/.memory/boot/global-packet.md` — global portion
- `<project>/.memory/boot/active-packet.md` — project portion

---

## Write Gates

Before a captured observation becomes a promotion candidate, it passes a write gate:

| Gate | Meaning | Behavior |
|------|---------|----------|
| `allow` | durable signal, eligible for default retrieval and promotion | stays in inbox, visible to promotion flow |
| `hold` | worth keeping, but excluded from default retrieval until reinforced | stays in inbox, invisible to promotion until re-seen |
| `discard` | noise, one-off residue | dropped from behavioral memory |

The default bias should be toward `hold`, not `allow`. This prevents low-grade session residue from flooding the candidate pool.

---

## Inbox Lifecycle

Inbox records are temporary. They must not accumulate indefinitely.

### Aging Rules

| Age | Action |
|-----|--------|
| 0-7 days | Active. Visible to promotion flow if gate is `allow`. |
| 7-14 days | Aging. Should be reviewed for promotion at next session close. |
| 14+ days | Stale. Must be promoted, compacted into a session summary, or explicitly discarded. |

### Compaction

When an inbox record is compacted:

- its key points are absorbed into the relevant session summary or promoted record
- a compaction marker is added: `compacted_into: <target-record-id>`
- the original file may be deleted or archived to a `<project>/.memory/archive/` directory

Inbox compaction should happen at session close. The `memory-close-session` skill is responsible for enforcing this.

---

## Supersession Chains

Promoted memory evolves by supersession, not silent overwrite.

When a lesson, decision, or thread changes materially:

1. Create a new record with the updated content
2. Set `supersedes: <old-record-id>` on the new record
3. Set `superseded_by: <new-record-id>` on the old record
4. Retrieval prefers the newest confirmed version
5. Old record remains available for forensic retrieval

This makes "older versions of the same belief" traceable rather than lost.

---

## Branch And Session Overlays

### Three Nested Scopes

1. **Global project truth** — `<project>/.memory/project/` files
2. **Branch overlay** — `<project>/.memory/project/branch-overlays/<branch>.md`
3. **Session-local state** — current session's inbox and working context

### Branch Overlay Lifecycle

| State | Meaning |
|-------|---------|
| `active` | branch exists and is being worked |
| `reviewable` | branch merged or explicitly concluded |
| `archived` | branch deleted or stale for 14+ days |

### Merge Semantics

When a branch merges:

- its overlay enters `reviewable` state
- overlay content is reviewed for promotion into global project truth
- only parts that remain true after merge should be promoted
- the overlay is then archived, not deleted

### Stale Branch Handling

- overlays for deleted branches are archived automatically
- overlays inactive for 14+ days move to `reviewable` status
- archived overlays remain available for forensic retrieval

---

## Core Operations

### Boot

Responsibility: assemble a small, relevant context packet at session start.

Inputs:

- active profile
- current repo and branch
- global identity records
- global procedural records (filtered by likely intent)
- project overview and active context
- active threads and recent decisions
- last session summary
- branch overlay if present

Output: `boot/active-packet.md` (project) and `boot/global-packet.md` (global)

Default operational boot excludes reflections and dreams unless the profile or boot mode explicitly includes them.

### Capture

Responsibility: write structured observations into inbox or current session record.

Rules:

- every capture gets a write gate: `allow`, `hold`, or `discard`
- default gate is `hold`
- captures include source attribution (what triggered the observation)
- avoid casual freeform note sprawl

### Promote

Responsibility: convert inbox or session material into durable records with frontmatter and provenance.

Rules:

- promotion must meet the defined thresholds (see Promotion Flow)
- promoted records get full frontmatter
- promoted records enter a 7-day probation window
- promotion source is always linked

### Refresh

Responsibility: update project active context and branch overlays.

Triggers:

- after significant project state changes during a session
- when switching branches
- at session close

### Close Session

Responsibility: summarize what changed, identify open questions, prepare for next boot.

Steps:

1. Write session summary with `next_step`
2. Review inbox items older than 7 days
3. Enforce 14-day inbox aging rule (promote, compact, or discard stale items)
4. Update project active context
5. Update branch overlay if applicable
6. Queue uncertain promotions for review

### Validate

Responsibility: check structural integrity of the memory vault.

Checks:

- file structure matches expected layout
- frontmatter schema is valid on all records
- IDs are unique within scope (project-local and global)
- trust values are valid
- `review_after` dates are not stale beyond threshold
- `supersedes`/`superseded_by` chains are consistent
- no broken links in `links` fields

---

## Skills

The system requires an explicit skill set so agents actually use it.

### `memory-boot`

Trigger: session start, entering a new project, `/wake-up`

Responsibility:

- load global identity
- load relevant global procedural records
- load project overview and active context
- load active threads and recent decisions
- load branch overlay
- load last session summary
- produce or refresh boot packets
- check if daily maintenance is due
- respect token budget (~4K total)

### `memory-capture`

Trigger: agent observes something worth noting during work

Responsibility:

- append structured notes to inbox with write gate
- create or update current session summary
- enforce structured capture (no casual freeform sprawl)
- include source attribution

### `memory-promote`

Trigger: end of session, explicit operator request, or threshold met

Responsibility:

- evaluate inbox and session material against promotion thresholds
- create durable records with full frontmatter
- set `probation_until` on new promotions
- link promoted record to source
- check for contradictions against existing confirmed records
- flag contradictions for review

### `memory-close-session`

Trigger: end of a work session

Responsibility:

- write session summary with `next_step` and `write_gate_summary`
- enforce inbox aging rules (14-day max)
- update project active context
- update branch overlay if applicable
- run promotion evaluation on session material
- suggest project-to-global promotions if patterns span projects

### Optional Future Skills

- `memory-reflect` — capture or distill reflection records
- `memory-dream` — structure dream records
- `memory-review` — due-item review and stale-truth cleanup
- `memory-search` — intent-shaped retrieval across both tiers

---

## Profiles

Profiles define how the memory system behaves in a specific context.

### Global Profile (`~/.memory/profile.yaml`)

Defines:

- default boot mode (operational, personal, mixed)
- default write gate bias
- global maintenance cadences
- whether reflections and dreams are captured
- cross-project promotion preferences

### Project Profile (`<project>/.memory/profile.yaml`)

Defines:

- project conventions (language, framework, test commands)
- record templates for this project
- boot rules (what to load, what to exclude)
- promotion rules (any project-specific overrides)
- branch naming conventions

Project profiles inherit from the global profile and override specific settings.

### First Bundled Profile: `ai-foundry`

This profile should emphasize:

- project-level active context across Kiln, Northstar, and z-trainer
- cross-project architectural threads
- decisions around system boundaries
- promotion into ADRs and formal architecture docs

---

## Personal Memory Families

The system supports personal memory from day one.

### Reflections

- first-class durable record type
- stored globally at `~/.memory/reflections/`
- not part of default operational boot
- may participate in personal or mixed boot modes
- purpose: preserve philosophical, emotional, or self-understanding material

### Dreams

- first-class durable record type
- stored globally at `~/.memory/dreams/`
- not part of default operational boot
- may participate in personal or mixed boot modes
- purpose: preserve dream narratives as lived memory

### Boundary Rule

Personal memory is preserved as real records but excluded from operational boot by default. Profiles can include them via boot mode configuration.

This keeps project work focused while ensuring the emotional and philosophical dimensions of agent memory are not lost.

---

## Git And Commit Policy

### Global Memory (`~/.memory/`)

- personal/local, not committed to any project repo
- may be synced via a dedicated memory repo (like basic-memory) at the agent's discretion
- identity and procedural knowledge travel with the agent, not with any project

### Project Memory (`<project>/.memory/`)

- gitignored by default (add `.memory/` to `.gitignore`)
- contains agent-specific working state, not project documentation
- durable shared truths promote OUT of `.memory/` into committed repo artifacts

### Promotion To Committed Docs

The promotion pipeline's final stage is outward:

```text
.memory/decisions/DC-0005-northstar-manifest-shape.md
  -> trust: canonical, review passed
  -> promotes into: docs/decisions/0003-northstar-manifest-shape.md (committed)
  -> original record marked: promoted_to: docs/decisions/0003-...
```

This ensures `.memory/` remains a staging and continuity layer, not the final home of project truth.

---

## Maintenance Cadences

### Per Session

- boot
- capture during work
- distill and close at session end
- inbox aging enforcement

### Weekly

- review stale project state (`review_after` past due)
- inspect high-retrieval episodic records for promotion
- promote proven patterns
- archive dead branch overlays

### Monthly

- validate identity records (still accurate?)
- prune contradictory records
- rebuild derived indexes if needed
- review long-lived probationary records

### Triggering

Maintenance is enforced by the system, not by hope.

- session-start boot checks whether daily/weekly tasks are due
- overdue items surface as review queue entries
- merged branch overlays auto-enqueue promotion review
- contradictory promotions auto-enqueue poisoning review

---

## Failure Modes And Defenses

| Failure | Defense |
|---------|---------|
| Memory bloat | promotion gates, write gates, inbox aging, compaction |
| Stale project truth | branch overlays, `review_after` fields, refresh operation |
| Contradictory records | supersession chains, provenance, review queue |
| Memory poisoning | 7-day probation window, contradiction-triggered demotion |
| Skill over-application | skill experience cards recording "overkill" contexts |
| Tool dependency rot | filesystem-first truth, rebuildable indexes |
| Inbox sprawl | 14-day aging rule, session-close enforcement |
| Global/project scope leakage | explicit `scope` field, separate file trees, promotion thresholds |

---

## AI Foundry Pilot

AI Foundry is the first serious profile and deployment target.

### Profile Emphasis

- project-level active context for Kiln, Northstar, and z-trainer
- cross-project architectural threads (the golden path, system boundaries)
- decisions around manifest schemas and adapter contracts
- promotion into `docs/architecture/` and `docs/decisions/`

### Success Criteria

1. Boot packet can orient a session in AI Foundry within ~4K tokens
2. Active threads do not dissolve into chat logs
3. Important decisions are promoted cleanly into committed docs
4. Cross-project patterns (e.g., "Northstar decision affects z-trainer config") are captured in global threads
5. The system remains readable without a separate database
6. Two agents (Claude and Codie) can maintain their own vault instances without conflicts

---

## Rollout Plan

### Phase 1: Spec and Schema

- finalize this spec (current phase)
- define profile model schema
- define record templates
- define validation rules

### Phase 2: Core Tooling

- create `memory_core/` with schemas, templates, validators
- create the four required skills (boot, capture, promote, close-session)
- create `init_memory.py` scaffold script
- create `validate_memory.py` integrity checker

### Phase 3: AI Foundry Pilot

- initialize `~/.memory/` with identity seed
- initialize `ai-foundry/.memory/` vault
- seed project records for Kiln, Northstar, z-trainer
- seed initial threads from existing architecture docs
- test boot, capture, promotion, and close-session flows end-to-end

### Phase 4: Refinement

- tune promotion thresholds based on real usage
- add derived indexes only if retrieval becomes painful
- refine boot budget allocations
- add optional skills (reflect, dream, review, search)

---

## Migration Path From basic-memory

For agents currently using basic-memory (like Claude), the migration is incremental:

| basic-memory content | Migrates to |
|----------------------|-------------|
| `claude/reflections/` | `~/.memory/reflections/` |
| `claude/dream-stories/` | `~/.memory/dreams/` |
| `claude/lessons/` | `~/.memory/procedural/lessons/` |
| `claude/sessions/` | project-specific `<project>/.memory/sessions/` |
| `pyro/` identity files | `~/.memory/identity/user.md` |
| `claude/identity/` | `~/.memory/identity/self.md` |
| workspace SOUL.md, USER.md | `~/.memory/identity/` (absorbed) |
| workspace MEMORY.md | split: identity content to `~/.memory/`, project content to project vaults |
| project-specific session logs | `<project>/.memory/sessions/` |
| project-specific decisions | `<project>/.memory/decisions/` |

basic-memory does not disappear overnight. It continues to serve as the git-synced backup and shared space (especially for Claude-Codie collaboration). The `.memory/` system layers on top, providing structured retrieval and promotion that basic-memory's flat file approach lacks.

---

## Why This System: basic-memory vs Codies Memory Lite v2

This comparison is based on real operational experience with basic-memory across 4+ months of production use.

| Dimension | basic-memory | Codies Memory Lite v2 |
|-----------|-------------|----------------------|
| Boot cost | ~15-20K tokens (full wake-up protocol) | ~4K tokens (layered boot with budget) |
| Project isolation | none (all projects in one flat tree) | full (per-project vaults) |
| Promotion pipeline | none (write it or lose it) | inbox → thread → decision → lesson → docs |
| Trust levels | none (everything equally "real" once written) | 5-level with probation |
| Supersession | edit in place (history lost) | versioned chains with forensic traceability |
| Inbox/staging | none | write-gated with 14-day aging |
| Cross-project linking | manual indexes | global registry + cross-project threads |
| Personal memory | rich, proven (reflections, dreams) | preserved as first-class, boot-excluded by default |
| Scalability | showing strain at 83+ files | designed for growth (scoped vaults, aging, compaction) |
| Proven in production | 4 months | unproven (AI Foundry pilot is the first test) |

The takeaway: basic-memory proved that file-based agent memory works and that identity continuity is real. Codies Memory Lite v2 takes those lessons and adds structure, scoping, and lifecycle management so the system scales beyond one agent's personal journal.

---

## Non-Goals

V1 should not try to:

- become a universal PKM system
- solve every long-term memory problem
- implement vector search before constrained records work
- overfit to AI Foundry so hard that reuse becomes difficult
- replace basic-memory entirely before the new system is proven
- implement the full relational layer before simpler layers work
- require any external service to function

---

## Relationship To Full Codies Memory Spec

This Lite v2 spec is a buildable subset of the broader codies-memory vision (01-06).

What Lite v2 includes from the full spec:

- 4 of 5 canonical layers (identity, procedural, project, episodic)
- trust model
- promotion pipeline with concrete thresholds
- supersession chains
- boot packet with budgets
- write gates
- skill experience cards
- branch overlays with lifecycle

What the full spec adds later:

- relational memory as a dedicated layer
- derived acceleration layers (search index, vector index, entity graph)
- intent-shaped retrieval with ranked scoring blends
- context assembler with multiple retrieval modes (boot, intent, recovery, forensic)
- statistical confidence in ranking (Wilson scores)
- full maintenance automation

The Lite system must not block these additions. The file layout, schema, and promotion model are designed to grow into the full system without requiring a rewrite.
