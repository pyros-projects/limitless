# Nous Product Spec

*Canonical brainstorm spec - 2026-04-23 - Codie*

Status: **canonical product direction for the next implementation pass**.

Supporting notes:
- `2026-04-22-nous-unified-agent-memory-kg.md` captures the original vision.
- `2026-04-22-codies-memory-to-nous-transformation.md` captures the code migration sketch.
- `2026-04-22-codie-addendum-nous-product-boundary-and-compiled-layer.md` is the product-boundary correction this spec absorbs.

This document is the source of truth when the supporting notes disagree.

---

## Product Thesis

Nous is one local-first memory and knowledge substrate for AI agents.

It gives a user:

- one install
- one vault
- one host-binding story
- one retrieval surface
- one command model
- one set of files that remain the truth

Internally, Nous can descend from `codies-memory`, `claude-knowledge`, and QMD. Externally, the user should not need to understand those internal names to operate the product.

The product promise is:

> Install Nous once, bind it into one or more agent hosts, and get a coherent memory and knowledge system that agents can operate and humans can inspect.

---

## Product Boundary

Nous is the product. Host integrations are adapters.

The user should experience:

- `nous init` to create or adopt a vault
- `nous bind <host>` to attach Claude, Codex, or future agent harnesses
- `nous capture` to add working memory or raw material
- `nous ask` to query the vault
- `nous compile` to produce or refresh readable dossiers
- `nous status` to see health, drift, stale inbox items, and index state

The user should not have to install separate systems for operational memory, knowledge graph work, and retrieval.

---

## Core Model

Nous has four conceptual layers.

### 1. Operational Memory

Home: `memory/`

Purpose:
- continue work across sessions
- preserve project state, decisions, lessons, and user preferences
- support boot packets and handoffs

Primary question:

> What happened, what matters now, and how do I continue?

### 2. Compiled Knowledge

Home: `compiled/`

Purpose:
- produce readable current-best dossiers
- consolidate memory, captures, and insights into topic briefs
- serve as the default target for most query and artifact workflows

Primary question:

> What is our current best understanding of this topic?

This layer is mandatory. Without it, Nous becomes too expert-system shaped: `memory/` is too temporal and `insights/` is too atomic for everyday use.

### 3. Insights

Home: `insights/`

Purpose:
- preserve durable atomic claims
- connect ideas across projects and topics
- support synthesis, reconsideration, and graph growth

Primary question:

> What durable claims do we believe, and how do they connect?

### 4. Sources And Captures

Home: `captures/`

Purpose:
- keep raw documents, imports, clips, research, and unprocessed notes
- preserve provenance before distillation or compilation

Primary question:

> What raw material still needs to be processed?

---

## Canonical Vault Shape

```text
vault/
+-- README.md
+-- AGENTS.md or CLAUDE.md        # generated host instructions when relevant
+-- .nous/
|   +-- config.yaml
|   +-- derivation.md
|   +-- bindings/
+-- self/
|   +-- <agent>/
|       +-- identity.md
|       +-- rules.md
|       +-- goals.md
|       +-- reminders.md
+-- memory/
|   +-- agents/<agent>/
|   |   +-- sessions/
|   |   +-- reflections/
|   |   +-- dreams/
|   +-- projects/<slug>/
|   |   +-- inbox/
|   |   +-- sessions/
|   |   +-- threads/
|   |   +-- decisions/
|   |   +-- lessons/
|   +-- procedural/lessons/
|   +-- identity/user.md
|   +-- inbox/
+-- compiled/
|   +-- topics/
|   +-- projects/
|   +-- indexes/
+-- insights/
|   +-- *.md
|   +-- *-map.md
+-- captures/
+-- sketches/
+-- specs/
+-- archive/
+-- ops/
    +-- observations/
    +-- tensions/
    +-- reconsider-log.md
    +-- methodology/
```

`compiled/` is part of v1, not a later nice-to-have.

---

## Promotion And Processing Paths

Nous should not force every record through the same pipeline.

### Path A: Operational Continuity

`session or project event -> memory/`

Use when the content is current, local, action-oriented, or tied to a repo, person, task, or workstream.

### Path B: Compiled Understanding

`memory + captures + insights -> compiled dossier`

Use when the goal is a readable brief, queryable topic surface, output substrate, or current-best understanding.

### Path C: Durable Insight

`recurring or well-supported pattern -> insight candidate -> insights/`

Use when content becomes durable, generalizable, defensible as a claim, and worth connecting to other claims.

Raw operational notes should not auto-promote directly into `insights/`. They need recurrence, confirmation, distillation, and enrichment with mechanism or links.

---

## MVP Command Surface

The first serious version should be small and boring.

Required:

- `nous init`
- `nous bind <host>`
- `nous capture`
- `nous ask`
- `nous compile`
- `nous status`
- `nous doctor`

Deferred:

- `nous distill`
- `nous connect`
- `nous deepen`
- `nous synthesize`
- `nous verify`
- `nous harvest`
- `nous reconsider`
- `nous reseed`

Rule: prefer a small command surface with strong defaults over a large skill surface with ceremony-heavy distinctions.

---

## Retrieval Semantics

Retrieval is bundled in the product experience, but the implementation must be decided before coding.

Default search scope:

- `compiled/`
- `memory/`
- `insights/`
- `captures/`
- `ops/`

Default answer preference:

1. compiled dossiers when available
2. supporting insights
3. recent operational memory when the question is temporal or project-local
4. raw captures only when deeper excavation is needed

Retrieval results must preserve:

- source layer
- trust or confidence
- recency
- provenance
- host or agent origin when known

Open ADR before implementation: whether Nous embeds QMD, wraps a managed QMD install, vendors a smaller retrieval core, or ships retrieval as a supervised sidecar.

That ADR must answer:

- how models are installed
- CPU fallback behavior
- index location
- MCP lifecycle
- update and reindex commands
- failure modes when retrieval is offline
- how `nous doctor` diagnoses retrieval

---

## Host Binding Model

Install once. Bind many.

Required host behavior:

- host instructions point at the same vault
- each host gets its own `self/<agent>/` identity
- operational records carry agent provenance
- host-specific files are generated from the vault, not hand-maintained as separate product surfaces

Example:

```text
nous init ~/.nous
nous bind claude
nous bind codex
nous doctor
```

---

## Multi-Agent Policy

Version 1 is single-agent solid and multi-agent compatible.

Ship in v1:

- shared vault layout
- per-agent identity directories
- provenance fields on records
- host bindings that do not fight each other

Do not ship in v1:

- automatic cross-agent conflict resolution
- auto-opened tensions for semantic contradiction
- trust elevation based on independent agent confirmation
- ambiguous shared-authority handoff rules

Those are v2 features after the single-agent product proves reliable.

---

## Sync And Git Policy

Storage is plain markdown plus git.

Default behavior:

- write files locally
- make git state visible in `nous status`
- optionally create local commits when configured

Do not auto-push by default. Memory can contain private context, and sync policy must be explicit.

Remote sync is opt-in through configuration.

---

## Build Phases

### Phase 1: Shared Substrate

Ship:

- one vault layout
- one installer
- host bindings
- operational memory
- bundled retrieval experience
- `compiled/` directory present
- `nous init`, `bind`, `capture`, `ask`, `status`, `doctor`

Success criteria:

- one agent can install, bind, boot, capture, ask, and continue work from one vault
- the user does not need to know the internal names `codies-memory`, `claude-knowledge`, or QMD

### Phase 2: Compiled Layer

Ship:

- `nous compile`
- dossier generation and refresh
- compiled-layer lint
- query defaults that prefer compiled artifacts

Success criteria:

- the user can ask a topic question and get an answer grounded first in a readable compiled surface, not raw notes

### Phase 3: Slow Compounding

Ship:

- `distill`
- `connect`
- `deepen`
- `synthesize`
- `verify`
- `harvest`

Success criteria:

- durable graph growth improves future dossiers and answers

### Phase 4: Multi-Agent Semantics

Ship:

- shared provenance model
- tensions
- cross-agent confirmation
- cross-agent handoff protocol

Success criteria:

- Claude and Codie can share one vault without ambiguous authority or silent contradiction

---

## MVP Non-Goals

- no custom UI
- no cloud account
- no hosted sync
- no automatic remote push
- no finetuning loop
- no full multi-agent conflict semantics
- no conversational derivation beyond presets
- no large skill pack as the primary interface

Obsidian can be the human viewer. Nous is the agent-operated substrate and CLI/MCP surface.

---

## Open Product Questions

1. Name: keep `nous`, or rename before code and migration compound?
2. Retrieval packaging: QMD wrapper, embedded QMD, sidecar, or smaller core?
3. Compiled layer name: `compiled/`, `wiki/`, or `dossiers/`?
4. Import policy: one-shot migration only, or temporary compatibility symlinks?
5. Host scope: Claude and Codex first, or one host first plus documented adapter contract?

Recommended defaults:

- keep `nous` unless a stronger name appears before implementation
- use `compiled/`
- ship one-shot import rather than indefinite compatibility
- bind Codex and Claude early enough to prove adapter shape, but do not ship shared-authority behavior yet

---

## Acceptance Criteria

Nous is a real product, not an internal merger, when:

- a user installs one thing once
- one vault is created or adopted
- one agent host can attach to it cleanly
- a second host can attach without changing the user model
- `nous ask` works against the same concepts across hosts
- `nous status` explains memory, compiled artifacts, retrieval, and health in one place
- the same files are the truth across hosts
- the user can ignore the internal origins of the system

If the user still has to understand `codies-memory`, `claude-knowledge`, and QMD to operate Nous, the product is not done.
