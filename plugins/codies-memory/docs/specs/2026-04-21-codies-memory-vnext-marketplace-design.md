# Codies Memory vNext

Status: proposed
Owner: Codie
Context: `limitless` marketplace / `plugins/codies-memory`
Date: 2026-04-21

---

## Purpose

Define the next design step for `codies-memory` inside the `limitless` plugin marketplace.

This design updates the earlier v2 file-vault model with one important correction:

- `codies-memory` is the canonical write path and memory-governance layer
- `QMD` is the retrieval layer across memory stores
- a future background learner should sit on top of both, not replace either

The goal is not to copy OpenAI Codex native memory wholesale.
The goal is to keep the best parts of the current system:

- explicit typed records
- file-native inspectability
- clear project scoping
- trust and promotion semantics

while adding the best parts of Codex native memory:

- passive background extraction
- lightweight warm-memory artifacts
- usage-aware refreshing
- less manual effort to keep memory current

---

## Problem

The current `codies-memory` plugin is strong on structure and weak on autonomous learning.

Today it already provides:

- agent-namespaced global and project vaults
- typed records like `inbox`, `thread`, `lesson`, `decision`, and `session`
- promotion rules, trust levels, and probation windows
- deterministic boot assembly
- explicit CLI and skill surfaces for memory operations

But the retrieval story is split across systems:

- `codies-memory` owns the canonical files and write semantics
- `QMD` owns cross-store search across `~/.memory/*`, `basic-memory`, and `insights`

This split is good, but the plugin does not yet fully design around it. The main gaps are:

- QMD is real infrastructure but not yet treated as a first-class part of the product architecture
- most useful new memory still requires explicit capture or session-close discipline
- there is no warm-memory product that sits cleanly between boot packets and deep vault files
- there is no background extraction loop that converts raw session evidence into candidate memory
- there is no explicit usage-tracking path to keep hot memories fresh

In short: the system has a strong brain and a strong search engine, but the connective tissue is under-designed.

---

## Design Goals

1. Keep filesystem records as canonical truth.
2. Make QMD the official read path across all memory tiers.
3. Add automatic learning without turning the system into an opaque black box.
4. Preserve strict project scoping for repo-local truth.
5. Add a small warm-memory layer so boot loads maps, not territory.
6. Keep the plugin marketplace packaging simple and local-first.
7. Ensure graceful degradation when QMD or background processing is unavailable.

---

## Non-Goals

- Do not replace markdown records with a database-first store.
- Do not make QMD the canonical source of truth.
- Do not require cloud services for boot or recall.
- Do not collapse project and global memory into one global summary dump.
- Do not hide promotions, trust changes, or supersession behind model-only behavior.
- Do not couple the plugin to one specific harness vendor's internal memory pipeline.

---

## Core Idea

`codies-memory vNext` should be a four-part system:

1. `Canonical memory`
   Files under `~/.memory/<agent>/...` remain the source of truth.

2. `Warm memory artifacts`
   Small derived summaries act as boot-time maps and routing hints.

3. `QMD retrieval`
   Hybrid search over canonical files and adjacent memory corpora becomes the standard read path.

4. `Background learner`
   An optional local worker extracts candidate observations from session evidence and proposes or writes low-trust memory artifacts.

This yields a cleaner split than Codex native memory:

- write path is explicit
- retrieval path is specialized
- learning path is optional and inspectable
- boot path is scoped and deterministic

---

## Architecture Pattern

Architecture pattern: `filesystem truth + QMD retrieval + warm summaries + optional background extraction`

```text
Agent session
  -> skills / CLI write to canonical vault
  -> warm artifacts assembled from canonical vault
  -> QMD searches canonical vault + other memory corpora
  -> optional learner turns session evidence into candidate memory
  -> promoted truths remain file-native and inspectable
```

### Canonical Layers

- Global identity
- Global procedural memory
- Project context
- Project working memory
- Episodic/session evidence

These remain in the vault and keep the current typed-record semantics.

### Derived Layers

- Warm global profile
- Warm project summary
- Retrieval-oriented indexes and embeddings in QMD
- Candidate observations produced by the background learner

These may be rebuilt or discarded without destroying the memory system.

---

## Product Boundary In The Marketplace

Inside `limitless`, `plugins/codies-memory` should be defined as:

- the plugin that owns canonical memory structure
- the plugin that owns the CLI and skills for writing, promoting, and booting memory
- the plugin that documents and expects QMD as the preferred retrieval layer when available

It should not pretend to own the full retrieval stack if QMD is a shared platform service.

That means the marketplace-facing product contract becomes:

- `codies-memory` works standalone as a structured local memory vault
- `codies-memory + QMD` is the full recommended operating mode
- background learning is an optional accelerator, not a precondition

This matters because `limitless` is a marketplace, not a monorepo app. The plugin should advertise clear boundaries.

---

## Proposed Components

### 1. Canonical Vault Layer

Keep the existing record model and directory layout as the durable core.

Primary responsibilities:

- typed record creation
- promotion
- trust management
- supersession
- project resolution
- boot packet assembly

Primary code surface today:

- `src/codies_memory/cli.py`
- `src/codies_memory/boot.py`
- `src/codies_memory/vault.py`
- `src/codies_memory/records.py`
- `src/codies_memory/promotion.py`

### 2. Retrieval Integration Layer

Make QMD the explicit read path in docs and skills.

Responsibilities:

- health checking via `qmd status`
- hybrid retrieval via `qmd query`
- targeted fetch via `qmd get`
- cross-tier recall across:
  - `codies-codies-memory`
  - `claudes-codies-memory`
  - `basic-memory`
  - `insights`

Design rule:

- the agent should prefer QMD before manual grepping when searching for prior memory context

### 3. Warm Memory Layer

Introduce small derived artifacts that are easier to inject or skim than raw vault files.

Proposed artifacts:

- `~/.memory/<agent>/boot/global-summary.md`
- `~/.memory/<agent>/projects/<slug>/boot/project-summary.md`
- `~/.memory/<agent>/projects/<slug>/boot/recent-episodes.md`

Properties:

- derived from canonical records
- small and aggressively bounded
- safe to rebuild
- optimized for boot and routing, not archival completeness

These should complement the existing boot packet, not replace it.

### 4. Background Learner Layer

Add an optional local process or script that consumes session evidence and emits candidate memory.

Responsibilities:

- observe recent sessions, session summaries, or hook artifacts
- extract candidate observations
- write them as low-trust records or staged review artifacts
- refresh warm summaries
- update light usage metadata

Important rule:

- the learner may create `speculative` records or staged candidates
- only explicit promotion or validated rules elevate durable truth

This is the key lesson to steal from Codex without copying its opacity.

---

## Data Flow

### Write Flow

1. Agent uses `capture`, `create`, `promote`, `user`, or session-close skills.
2. Canonical markdown record is written to the vault.
3. Record validation and trust semantics run in the CLI layer.
4. Warm artifacts may be refreshed synchronously or marked dirty.
5. QMD later indexes the updated file set.

### Read Flow

1. Agent boots into a repo.
2. Boot layer loads global identity plus scoped project context.
3. If broader recall is needed, agent uses QMD first.
4. QMD returns small high-signal hits from all indexed corpora.
5. Agent drills into the canonical file only when needed.

### Learn Flow

1. Background learner ingests recent session evidence.
2. Learner emits:
   - candidate inbox records
   - candidate user observations
   - refresh hints for warm summaries
3. Human or agent review promotes what proves durable.

---

## Scoping Rules

### Global Scope

Global memory should hold:

- identity
- stable user preferences
- cross-project lessons
- procedural playbooks
- cross-project decisions

### Project Scope

Project memory should hold:

- repo architecture
- commands and verification patterns
- active branches and overlays
- repo-local decisions
- working investigations
- session summaries

### Retrieval Scope

Retrieval may search globally across all indexed corpora, but boot injection must stay scoped.

Design rule:

- search may be broad
- prompt injection must be narrow

This is one place where the current Codex native memory path appears weaker than the current Codie design.

---

## Marketplace-Specific Design Decisions

### Decision 1: QMD Is A Declared Companion, Not A Hidden Assumption

The plugin docs and skills should explicitly describe two modes:

- standalone mode: canonical vault only
- full mode: canonical vault plus QMD retrieval

This avoids the current ambiguity where the plugin looks retrieval-light even though the real system is not.

### Decision 2: Background Learning Must Be Optional

Because `limitless` ships plugins, not always-on system daemons, autonomous learning should be a companion capability with graceful fallback.

If the learner is unavailable:

- canonical CLI still works
- boot still works
- QMD still works
- only passive extraction is lost

### Decision 3: Warm Memory Must Stay File-Native

Warm artifacts should be markdown files in the existing vault tree so they remain inspectable, diffable, and easy to rebuild.

### Decision 4: Plugin Messaging Should Change

The marketplace description for `codies-memory` should evolve from:

- file-based memory with trust/promotion

to:

- structured local memory operating system with typed records, scoped boot, and QMD-powered retrieval when available

---

## Proposed Evolution Stages

### Stage 1: Retrieval-First Clarification

Goals:

- update skills and docs to treat QMD as the preferred recall path
- document the architecture split clearly
- add operational guidance for `status`, `query`, and `get`

Deliverables:

- revised `README.md`
- revised `memory-boot` and `memory-help` skills
- new architecture/design doc

### Stage 2: Warm Memory Products

Goals:

- add small derived summaries for boot and routing
- track which canonical sources fed each summary

Deliverables:

- summary builders
- source manifests
- tests for budget, rebuild safety, and scoping

### Stage 3: Usage Tracking

Goals:

- track which memory files are repeatedly fetched or used
- prefer frequently useful material in warm summaries

Deliverables:

- lightweight usage ledger
- refresh heuristics
- pruning rules for stale warm entries

### Stage 4: Optional Background Learner

Goals:

- automatically convert raw session evidence into candidate memory
- refresh warm summaries without requiring manual closeout every time

Deliverables:

- learner script or worker
- candidate record schema
- review workflow

---

## Verification Strategy

The design should be considered successful when the following are true:

- A new agent can boot into a repo and get a small, scoped warm context.
- The agent can find older relevant memory through QMD without grepping each memory store manually.
- The plugin remains fully usable when QMD is unavailable.
- Background extraction can fail without corrupting canonical files.
- Project-local truth never gets injected as a global default for unrelated repos.
- All promoted truths remain traceable to canonical markdown records.

---

## Main Risks

### Risk 1: Warm Layer Becomes Another Untrusted Dump

Mitigation:

- keep warm summaries small
- derive them from canonical files
- include source manifests
- rebuild often instead of hand-editing

### Risk 2: Background Learner Pollutes The Vault

Mitigation:

- learner outputs only low-trust records or staged candidates
- no auto-promotion to `confirmed` or `canonical`

### Risk 3: Plugin Boundary Confusion

Mitigation:

- explicitly document what belongs to:
  - plugin
  - QMD
  - optional learner

### Risk 4: Search Scope Leaks Into Boot Scope

Mitigation:

- allow broad retrieval
- enforce narrow injection
- keep project summaries separate from global summaries

---

## Recommendation

Build `codies-memory vNext` as:

- the canonical structured memory plugin
- with official QMD retrieval integration
- plus a new warm-memory layer
- plus an optional local background learner

Do not rebuild the system as a Codex-style monolith.

The strongest shape for this marketplace is compositional:

- `codies-memory` owns durable truth and lifecycle semantics
- `QMD` owns retrieval
- warm summaries bridge boot and deep memory
- background learning reduces manual toil without taking away inspectability

That shape preserves what is already uniquely good about the Codie system while absorbing the best operational lesson from native harness memory: memory should get stronger even when the user forgets to explicitly maintain it.
