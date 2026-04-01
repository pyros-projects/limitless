# Architecture

## Overview

The system has five memory layers and three derived acceleration layers.

### Canonical Layers

1. `identity`
2. `procedural`
3. `project`
4. `episodic`
5. `relational`

### Derived Acceleration Layers

1. `search index`
2. `vector index`
3. `entity graph`

The canonical layers are the product.
The derived layers exist to make the canonical layers faster to use.

## Layer Definitions

### 1. Identity Memory

Purpose:

- preserve durable self and user context
- capture stable instructions, preferences, boundaries, and collaboration rules

Examples:

- who Codie is
- who Pyro is
- durable communication preferences
- privacy boundaries
- standing git and workflow rules

Characteristics:

- small
- highly stable
- loaded every session
- low write frequency
- high trust threshold

### 2. Procedural Memory

Purpose:

- encode operational knowledge
- connect skills to real usage
- store heuristics, playbooks, and failure-prevention patterns

Examples:

- lessons learned
- skill usage notes
- "when X, do Y" patterns
- verification checklists
- repo-agnostic debugging strategies

Characteristics:

- medium stability
- reusable across projects
- retrieved by intent
- promotion target for repeated session outcomes

### 3. Project Memory

Purpose:

- provide a brain per repo
- capture architecture, current state, commands, decisions, and open issues

Examples:

- project overview
- architecture map
- command reference
- current branch state
- active blockers
- local conventions
- recent decisions

Characteristics:

- scoped by repo
- changes more often than identity memory
- should support branch-aware overlays
- primary source for booting into work

### 4. Episodic Memory

Purpose:

- preserve historical record
- capture what happened before distillation

Examples:

- session logs
- daily notes
- scratch research captures
- temporary hypotheses
- raw command outcomes worth keeping

Characteristics:

- append-heavy
- noisy by design
- low trust by default
- primary feedstock for promotion and compaction

### 5. Relational Memory

Purpose:

- express connections between otherwise separate memory records

Examples:

- Pyro -> prefers -> concise evidence-first replies
- project -> uses -> OpenSpec
- lesson -> applies to -> debugging
- skill -> paired with -> verification-before-completion

Characteristics:

- can be stored as lightweight link metadata in frontmatter or sidecar indexes
- should stay simple locally
- useful for context assembly and graph views

## Preferred Filesystem Shape

```text
.memory/
  identity/
    self/
    user/
    rules/
  procedural/
    skills/
    lessons/
    playbooks/
    anti-patterns/
  projects/
    <project-slug>/
      overview.md
      architecture.md
      commands.md
      decisions/
      blockers/
      branches/
      active-context.md
  episodic/
    daily/
    sessions/
    captures/
    scratch/
  relational/
    entities/
    links/
    generated/
  derived/
    search/
    vectors/
    graph/
    boot-packets/
```

This could live in a dedicated memory repo, but the internal design here is intentionally product-first rather than path-first.

## Branch-Aware Overlays

Project memory should support three nested scopes:

1. `global project truth`
2. `branch-specific overlay`
3. `active session overlay`

This prevents common drift such as:

- assuming an old branch decision still applies
- treating experimental blockers as repo-wide facts
- loading stale implementation plans into review work

### Overlay Lifecycle

Branch overlays are not permanent peers of global project truth.

They move through a small lifecycle:

1. `active` while the branch exists and is being worked
2. `reviewable` when the branch merges or is explicitly concluded
3. `archived` when the branch is deleted or becomes stale

Merge semantics:

- a merged branch does not automatically overwrite global project truth
- its overlay is reviewed for promotion into global project records
- only the parts that remain true after merge should be promoted

Stale branch handling:

- branch overlays for deleted branches should be archived, not silently removed
- long-lived inactive branches should move to `reviewable` status after an inactivity threshold
- archived overlays remain available for forensic retrieval

## Concurrency Model

The memory system should assume parallel activity, even if the first implementation is simple.

### Write Ownership

- `episodic` memory is append-heavy and should tolerate concurrent writes
- `project` memory should use a single-writer rule for mutable state like `active-context.md`
- `identity` and `procedural` memory should prefer queued promotion rather than direct concurrent mutation
- `relational` memory can be regenerated from canonical files when needed

### Practical Rule Set

1. concurrent sessions may append independent episodic records freely
2. project-state mutations must go through one active writer per project scope
3. conflicting promotion candidates should be queued for review instead of auto-merged
4. derived indexes may rebuild asynchronously because canonical files remain authoritative

This keeps concurrency simple where it matters and relaxed where it is safe.

## Skill Integration Architecture

Skills should have a memory companion record that captures:

- purpose
- trigger patterns
- paired skills
- friction patterns
- adaptation notes
- recent successful uses
- recent failed or awkward uses

That companion should be linkable from:

- lessons
- project notes
- boot packets
- post-session distillations

This is how "skills" become lived operational memory instead of static instructions on disk.

## Trust Model

Each memory record should have an explicit trust posture:

- `canonical`
- `confirmed`
- `working`
- `speculative`
- `historical`

This makes retrieval safer.
A boot packet should strongly prefer `canonical`, `confirmed`, and currently relevant `working` records.

Recently promoted records should still be treated as probationary in behavior, even if their trust label is already `confirmed`.
Promotion confidence and rollback windows should be handled through metadata, not by inventing many more trust states.
