# Mneme Product Spec

*Canonical brainstorm spec - 2026-04-23 - Codie*

Status: **canonical product direction for the next implementation pass**.

Decision status: product questions are resolved by
`2026-04-26-decisions-resolved.md`; ADR-001 resolves retrieval packaging.
This spec owns the product model and phase shape. The 2026-04-26 docs own the
post-spec decisions.

Supporting notes:
- `2026-04-22-mneme-unified-agent-memory-kg.md` captures the original vision.
- `2026-04-22-codies-memory-to-mneme-transformation.md` captures the code migration sketch.
- `2026-04-22-codie-addendum-mneme-product-boundary-and-compiled-layer.md` is the product-boundary correction this spec absorbs.
- `2026-05-01-memanto-prior-art-for-mneme.md` captures the Memanto comparison and the product-surface ideas Mneme can borrow without changing its kernel.
- `2026-06-09-hindsight-prior-art-for-mneme.md` captures the Hindsight comparison and the retrieval/consolidation mechanics Mneme can borrow without changing its file-first truth model.
- `2026-06-10-claude-addendum-kg-crossrefs-and-routing-non-goal.md` adds KG cross-references for the Hindsight comparison and makes cross-project routing an explicit non-goal with a named future design. Reviewed by Codie 2026-06-10.

This document is the source of truth when the supporting notes disagree.

---

## Project Mantra

Build v0.1 like a tool, not like a mythology.

The first version should be annoyingly practical:

> Install Mneme. Bind Codex. Capture memory. Ask across the vault. Compile a
> topic dossier. Boot the next session better.

First rule: if a feature does not directly improve that loop, defer it.

---

## Product Thesis

Mneme is one local-first memory and knowledge substrate for AI agents.

It gives a user:

- one install
- one vault
- one host-binding story
- one retrieval surface
- one command model
- one set of files that remain the truth

Internally, Mneme can descend from `codies-memory`, `claude-knowledge`, and QMD. Externally, the user should not need to understand those internal names to operate the product.

The product promise is:

> Install Mneme once, bind it into one or more agent hosts, and get a coherent memory and knowledge system that agents can operate and humans can inspect.

---

## Product Boundary

Mneme is the product. Host integrations are adapters.

The user should experience:

- `mneme init` to create or adopt a vault
- `mneme bind <host>` to attach Claude, Codex, or future agent harnesses
- `mneme capture` to add working memory or raw material
- `mneme ask` to query the vault
- `mneme compile` to produce or refresh readable dossiers
- `mneme status` to see health, drift, stale inbox items, and index state

The user should not have to install separate systems for operational memory, knowledge graph work, and retrieval.

---

## Prior-Art Boundary

Memanto and Hindsight are useful prior art, not replacement directions.

The borrowing rule is:

> Borrow product ergonomics, not the source-of-truth model.

Mneme should keep `codies-memory` as the operational kernel and QMD as the
managed retrieval sidecar. Prior-art ideas are welcome only when they make the
existing loop clearer:

- explicit raw evidence versus synthesized answer modes for `mneme ask`
- richer but optional metadata (`subtype`, confidence, provenance, actor/source,
  source references, tags)
- temporal query flags such as `--as-of`, `--changed-since`, and
  `--current-only`
- a host connector registry for `mneme bind`
- batch and file capture into `captures/` with provenance
- status/bootstrap dashboards that show memory health quickly
- token-budgeted recall controls
- source chunks or file refs beside extracted claims
- candidate observations with proof counts and freshness signals
- retrieval traces for debugging memory trust

Do not copy Memanto's or Hindsight's cloud/service dependency, agent-only
namespace model, database-as-canonical-truth posture, mandatory memory-hoarding
posture, ungated auto-belief formation, or broad v0 command surface. Mneme's
advantage is local truth, repo-aware project memory, boot packets, and
promotion gates.

The knowledge graph reviewed Hindsight independently from the research side
(arxiv:2512.12818). Three KG claims travel with the borrow list:

- Hindsight's retain/recall/reflect and the KG's distill/connect/deepen are an
  independent convergence on the same three-phase pipeline: capture with
  context, relate what was captured, improve existing knowledge from new
  understanding. Skipping a phase degrades predictably (no capture = no
  persistence; no connection = orphaned facts; no improvement = stale
  knowledge). Mneme's processing paths must keep all three phases reachable:
  Path A covers capture, Paths B/C cover relate-and-improve. This convergence
  is the strongest argument that the borrow list is mechanics, not fashion.
- Hindsight reports 91.4% on LongMemEval versus Mem0's 49.0%, and the KG reads
  that result as strong evidence for TEMPR's multi-strategy recall
  architecture: semantic + BM25 + entity/link-graph traversal + temporal
  retrieval, fused by RRF and reranked. Treat this as system-level evidence
  for ADR-001's multi-arm retrieval bet, and as justification for deferring
  graph/temporal arms to phase 3 rather than dropping them.
- The KG's five-archetypes claim (flat logs, project memory banks, extracted
  fact stores, temporal knowledge graphs, atomic insight graphs each excel at
  exactly one retrieval target) explains why Mneme is a four-layer product and
  not one store with views. The archetype Mneme deliberately defers is the
  temporal/entity graph — phase 3, consistent with the Hindsight note.

KG sources:
`hindsight-s-retain-recall-reflect-pipeline-maps-almost-exactly-to-this-vault-s-distill-connect-deepen-pipeline`,
`hybrid-search-with-rrf-outperforms-both-pure-keyword-and-pure-semantic-search-for-agent-memory`,
`five-archetypes-of-agent-memory-organization-solve-fundamentally-different-knowledge-problems`.

---

## Core Model

Mneme has four conceptual layers.

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

This layer is mandatory. Without it, Mneme becomes too expert-system shaped: `memory/` is too temporal and `insights/` is too atomic for everyday use.

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
+-- .mneme/
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

Mneme should not force every record through the same pipeline.

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

- `mneme init`
- `mneme bind <host>`
- `mneme capture`
- `mneme ask`
- `mneme compile`
- `mneme status`
- `mneme doctor`

Deferred:

- `mneme distill`
- `mneme connect`
- `mneme deepen`
- `mneme synthesize`
- `mneme verify`
- `mneme harvest`
- `mneme reconsider`
- `mneme reseed`

Rule: prefer a small command surface with strong defaults over a large skill surface with ceremony-heavy distinctions.

---

## Retrieval Semantics

Retrieval is bundled in the product experience. ADR-001 decides the packaging
direction; phase 1 implementation still needs to verify the exact QMD
machine-readable CLI/MCP surfaces before coding against them.

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

ADR-001 resolves retrieval packaging: Mneme ships QMD as a managed sidecar.

Important implementation invariant: QMD provides candidate retrieval, but Mneme
owns product-ranking semantics. Collection filters alone must not be treated as
layer priority. `mneme ask` should merge and rank results with explicit layer
weights so compiled dossiers can outrank insights, insights can outrank raw
memory, and raw captures remain a deeper excavation path.

`mneme doctor` must diagnose retrieval as part of the product, not as an
external troubleshooting appendix:

- model availability
- index freshness
- QMD process/transport health
- host MCP binding health
- fallback behavior when vector search is unavailable
- whether layer-priority ranking is being applied

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
mneme init ~/.mneme
mneme bind claude
mneme bind codex
mneme doctor
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

## Cross-Project Routing Policy

One vault with `memory/projects/<slug>/` gives v1 **pull-based** cross-project
access: an agent can ask across projects because the layers share one
retrieval surface. That is search, not routing.

Routing — project A proactively telling project B "this thing I just learned
matters to you" — is explicitly out of scope for v1 and v2-as-currently-phased.
The KG records that no current system has built this layer; Mneme should not
pretend to be the exception before its core loop is real.

When routing is eventually attempted, the KG already names the candidate
design, and the spec's existing requirements happen to be its prerequisites:

- provenance fields on every record (already a v1 requirement) reframe routing
  as a policy problem over origin tags rather than an architecture problem,
- three-tier progressive disclosure (which project knows → what it knows →
  full content) keeps cross-project lookup affordable in tokens,
- boot-time overlap detection against other projects' compiled indexes is the
  cheap first increment — routing at boot, not push at write.

KG sources: `cross-corpus-routing-map`,
`cross-corpus-knowledge-routing-is-a-fundamentally-different-problem-from-within-corpus-search`,
`every-current-cross-project-memory-system-is-pull-based...`,
`progressive-disclosure-for-cross-project-memory-lookup-uses-three-tiers...`,
`provenance-metadata-reframes-cross-corpus-routing-as-a-policy-problem...`.

---

## V1 Write-Safety Contract

Version 1 may bind multiple hosts, but only ships conservative shared-vault
semantics.

V1 write rules:

- record creation is append-only by default
- generated host instructions may be rewritten by `mneme bind`
- warm summaries and compiled cache files may be regenerated
- existing durable records may only be updated through typed commands that
  preserve provenance and update timestamps
- all records carry `agent` or `host` provenance when created through a bound
  host
- simultaneous writers are serialized with a vault lock before writing
- if a lock cannot be acquired quickly, the command exits with a clear retry
  message rather than writing anyway

V1 does not attempt semantic conflict resolution. If Claude and Codie disagree,
both can write separate records; reconciling them is a v2 tension workflow.

---

## Sync And Git Policy

Storage is plain markdown plus git.

Default behavior:

- write files locally
- make git state visible in `mneme status`
- optionally create local commits when configured

Do not auto-push by default. Memory can contain private context, and sync policy must be explicit.

Remote sync is opt-in through configuration.

---

## Migration Contract

Mneme migration is one-shot by default. It copies and transforms old sources into
the Mneme vault; it does not symlink old locations into the new vault.

Required migration inputs:

- `~/.memory/<agent>/` codies-memory vaults
- project markers such as `.codies-memory`
- codies-memory project registry entries
- claude-knowledge operational memory and insights
- basic-memory archive imports when explicitly requested
- QMD collection definitions, contexts, and index settings
- host MCP config entries for Codex and Claude Code
- session-start hooks or boot instructions that currently point at
  codies-memory

Migration outputs:

- `~/.mneme/vault/` or user-selected vault path
- `.mneme/config.yaml`
- `self/<agent>/` identity directories
- `memory/agents/<agent>/` operational records
- `memory/projects/<slug>/` project records
- `insights/`, `captures/`, and `compiled/` layers
- migrated QMD collection map
- generated host bindings

The original sources remain untouched unless the user explicitly asks to archive
or remove them. `mneme doctor` should detect lingering old hooks or host configs
that still point at codies-memory after migration.

---

## Security And Privacy Contract

Mneme stores private working memory. The implementation must treat install,
binding, retrieval, and sync as trust-boundary operations.

V1 requirements:

- no automatic remote push
- no network sync without explicit configuration
- host config edits are backed up before mutation
- `mneme bind` prints exactly which config files it changed
- model and QMD binary installation records version and source
- generated host instructions tell agents that vault contents are private
- retrieval results include provenance so raw captures are not mistaken for
  confirmed memory
- `mneme doctor` reports whether the vault is inside a git repo with uncommitted
  private changes
- destructive operations require explicit confirmation

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
- minimal on-demand `mneme compile <topic>` that writes cached dossiers
- `mneme init`, `bind`, `capture`, `ask`, `compile`, `status`, `doctor`

Success criteria:

- one agent can install, bind, boot, capture, compile, ask, and continue work from one vault
- the user does not need to know the internal names `codies-memory`, `claude-knowledge`, or QMD

### Phase 2: Compiled Layer Quality

Ship:

- dossier templates
- refresh-stale behavior
- compiled-layer lint
- source-citation staleness checks
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
- no cross-project knowledge routing (pull-based access through the shared
  vault is the v1 model; see Cross-Project Routing Policy)
- no conversational derivation beyond presets
- no large skill pack as the primary interface

Obsidian can be the human viewer. Mneme is the agent-operated substrate and CLI/MCP surface.

---

## Resolved Product Decisions

The following questions are resolved by `2026-04-26-decisions-resolved.md`.

- name: `mneme`
- compiled layer name: `compiled/`
- compiled layer mechanism: on-demand with cache
- retrieval packaging: managed QMD sidecar
- host scope: Codex first, Claude second; both in v1
- import policy: one-shot migration, no compatibility symlinks
- multi-agent semantics: v1 layout-compatible only; v2 for real conflict semantics
- storage: plain markdown plus git, no auto-push

---

## Acceptance Criteria

Mneme is a real product, not an internal merger, when:

- a user installs one thing once
- one vault is created or adopted
- one agent host can attach to it cleanly
- a second host can attach without changing the user model
- `mneme ask` works against the same concepts across hosts
- `mneme status` explains memory, compiled artifacts, retrieval, and health in one place
- the same files are the truth across hosts
- the user can ignore the internal origins of the system

If the user still has to understand `codies-memory`, `claude-knowledge`, and QMD to operate Mneme, the product is not done.
