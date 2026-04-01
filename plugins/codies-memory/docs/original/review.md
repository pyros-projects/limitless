# Review: Codie's Memory System

Reviewer: Sisyphus (Claude Opus)
Date: 2026-03-13
Scope: Full spec review (01-principles through 06-roadmap) + comparison against production agent memory systems

---

## Executive Summary

This is a high-quality design spec written by someone who has lived with agent memory pain. The layering model, promotion pipeline, and intent-shaped retrieval are all strong. The skill-as-memory concept is genuinely novel — no existing system does this.

The main risks are in under-specified operational mechanics: compaction, promotion validation, boot budgets, and concurrency. These are the hard implementation problems that will determine whether this becomes a working system or stays a beautiful spec.

---

## What Works Well

### 1. Layering By Stability Is The Right Split

"Separate memory by stability, not by format" (01-principles, section 2) is the single strongest design decision. Most agent memory systems conflate "what I know" with "what happened." The 5-layer split (identity, procedural, project, episodic, relational) maps cleanly to real cognitive needs and creates natural promotion paths.

### 2. Promotion Over Capture Is The Right Bet

The pipeline (capture, candidate extraction, validation, promotion, compaction) addresses the number one failure mode of agent memory: unbounded accumulation. The explicit anti-patterns section ("promote everything," "search everything every time") shows awareness of where other systems fail. This is validated by production systems — Roampal and Headroom both converged on similar promotion gates independently.

### 3. Intent-Shaped Retrieval Is Sophisticated

Four retrieval modes (boot, intent, recovery, forensic) with distinct priority orderings is more nuanced than anything in standard RAG-based memory. The ranking blend (scope, intent, project, branch, trust, recency, link distance, retrieval history) correctly acknowledges that pure embedding similarity is insufficient. No existing system offers this level of retrieval specialization.

### 4. Skills As Memory-Bearing Objects Is Novel

The "skill experience card" concept — tracking where a skill helped, where it was overkill, repo-specific adaptations, failure patterns — is the most original idea in the spec. No production system (Letta, Roampal, Headroom, Basic Memory) treats skills as memory objects. This turns a static skill catalog into adaptive procedural memory. It is the spec's strongest differentiator.

### 5. Filesystem-First Is Proven

Basic Memory has validated this exact philosophy in production: markdown canonical, derived indexes rebuildable, human-inspectable at every layer. This survives tool churn, which is a real concern in the current AI tooling landscape.

### 6. Trust Model Is Well-Calibrated

Five trust levels (canonical, confirmed, working, speculative, historical) map cleanly to retrieval confidence. Most systems have binary trust (in memory or not). This enables the boot packet to strongly prefer high-trust records without discarding low-trust records entirely.

---

## Gaps And Concerns

### 1. Promotion Validation Has No Operator Defined

Severity: **High**

Stage 3 (04-retrieval, section "Validation") says "ask: is this general or only situational?" — but who asks? Is this the agent self-evaluating (unreliable), a scheduled human review (does not scale), or an automated heuristic (not specified)?

This is the critical control point of the entire system. If promotion is too aggressive, you get bloat. Too conservative, useful patterns stay buried in episodic noise.

Roampal solved this with concrete thresholds:

- working to history: score >= 0.7, uses >= 2
- history to patterns: score >= 0.9, uses >= 3, success_count >= 5
- demotion: score < 0.4
- deletion: score < 0.2

**Proposal**: Define equivalent thresholds for each promotion path (episodic to procedural, episodic to project, candidate to confirmed, etc.). Even rough initial numbers are better than qualitative criteria. Include a success_count concept — memories must prove usefulness before elevating.

### 2. Compaction Algorithm Is Hand-Waved

Severity: **High**

"Compact aggressively" and "compact continuously" appear as principles, but the mechanism is undefined. This is the hardest part of any memory system. Specifically undefined:

- What determines when an episodic record is safe to compact?
- What is the compaction output format — a summary, a pointer, both?
- How do you prevent compaction from destroying information that becomes relevant later in unexpected ways?

JoelClaw's write gates provide a concrete pattern: every observation gets classified as allow (durable signal, retrieved by default), hold (ambiguous, stored but excluded from default retrieval), or discard (noise, dropped entirely).

**Proposal**: Add a write gate stage between capture and candidate extraction. Define the gate types and their retrieval implications. Specify that compaction produces a summary record that links back to the original session for forensic retrieval.

### 3. Boot Packet Budget Is Undefined

Severity: **High**

"Small, high confidence, low noise" is qualitative. For an LLM-based agent, the boot packet directly competes with task context for the context window. Athena solved this with hash-based delta detection and a target of approximately 125 tokens per summary.

**Proposal**: Define a token budget (for example, 2K tokens for identity, 1K for project brain, 500 for branch overlay, 500 for session summary, 500 for procedural reminders — approximately 4.5K total). Add hash-based caching so the boot packet only regenerates when source records change. Define a priority-based truncation strategy when the budget is exceeded.

### 4. No Concurrency Model

Severity: **Medium**

The spec assumes single-agent, single-session operation. But Codie already operates with subagents (explore, librarian, oracle, etc.) — multiple agents could write to episodic memory simultaneously.

Unaddressed questions:

- Lock semantics for file writes?
- How do parallel sessions avoid corrupting active-context.md?
- What happens when two sessions promote conflicting candidates?

**Proposal**: Add a concurrency section to 02-architecture. At minimum, define that episodic writes are append-only (no conflicts possible), project state mutations go through a single writer, and conflicting promotions are queued for review rather than applied automatically.

### 5. No Supersession Chain Tracking

Severity: **Medium**

When a promoted lesson gets updated (for example, a debugging heuristic gets refined), what happens to the old version? The spec mentions "older versions of the same belief" in forensic retrieval (04-retrieval, section 4) but provides no mechanism to track versions.

Both Roampal and Headroom implement supersession chains: `supersedes`, `superseded_by`, and `promotion_chain` fields that track how beliefs evolve over time.

**Proposal**: Add `supersedes` and `superseded_by` fields to the canonical record schema. When a record is updated, create a new version that supersedes the old one rather than editing in place. This makes forensic retrieval actually work.

### 6. No Statistical Confidence In Ranking

Severity: **Medium**

Without statistical confidence intervals, the system cannot distinguish between "high score from 5 uses" and "high score from 500 uses." Roampal uses Wilson scores (confidence 0.95) for this exact purpose.

**Proposal**: Add a confidence calculation to the ranking rules. Wilson score or similar addresses small sample sizes. This matters most for procedural memory where a lesson might be "confirmed" based on very few observations.

### 7. Branch-Aware Overlays Lack Merge Semantics

Severity: **Medium**

The spec defines three scopes (global project truth, branch overlay, active session overlay) but does not address:

- What happens when a branch merges? Does its overlay promote to global?
- What about long-lived feature branches that diverge significantly?
- What about branch deletion — does the overlay get archived or deleted?

**Proposal**: Define merge behavior: when a branch merges to main, its overlay is reviewed for promotion to global project truth. Stale branch overlays (branches deleted or inactive for N days) are archived to episodic memory.

### 8. Relational Layer Is Underspecified

Severity: **Low-Medium**

This reads more like a placeholder than a design. "Lightweight link metadata in frontmatter or sidecar indexes" and "should stay simple" does not provide enough to implement.

Missing: schema for relationship types beyond examples, traversal semantics (how deep does context assembly follow links?), conflict resolution for contradictory relationships.

**Proposal**: This is correctly deferred to Phase 4 in the roadmap. But when the time comes, look at Basic Memory's knowledge graph implementation and Headroom's promotion chains as starting points. Define a maximum traversal depth for context assembly (for example, 2 hops) to prevent the graph from exploding retrieval scope.

### 9. Maintenance Cadences Need Triggering

Severity: **Low-Medium**

Daily, weekly, and monthly maintenance cadences (05-schemas, section "Maintenance Cadences") need triggering mechanisms. Who initiates weekly "review stale project state"?

**Proposal**: The session start flow (05-schemas, section "Session Start Flow") should include a maintenance check: "if daily compaction has not run today, run it before assembling the boot packet." Weekly and monthly tasks should surface in the memory review queue as overdue items, not depend on human memory.

### 10. No Memory Poisoning Defense

Severity: **Low**

What happens if a session produces a confidently wrong lesson that gets promoted? The spec has trust levels but no rollback mechanism for bad promotions.

**Proposal**: Promoted records should have a probation period (for example, 7 days) during which they can be demoted back to candidate status without a full review cycle. The review queue should flag recently promoted records that contradict existing confirmed records.

---

## Landscape Comparison

How the spec compares to existing production systems:

| Aspect | Letta/MemGPT | Roampal | Headroom | Basic Memory | Codie's Memory |
|---|---|---|---|---|---|
| Layers | Core + Archival | working, history, patterns | User, Session, Agent, Turn | Markdown + SQLite | 5 canonical + 3 derived |
| Promotion | Manual (self-editing) | Automatic (score-based) | Automatic (importance-based) | Manual (user edits) | Automatic (quality gates) |
| Boot context | Core memory blocks | Not specified | Not specified | Not specified | Explicit boot packet |
| Canonical truth | Vector store | ChromaDB | Store abstraction | Markdown files | Markdown files |
| Skills in memory | No | No | No | No | Yes (novel) |
| Supersession tracking | No | Yes | Yes | No | No (gap) |
| Statistical confidence | No | Yes (Wilson score) | No | No | No (gap) |
| Hybrid search | No | No | Yes | Yes | Planned |
| Local-first | Optional | Yes | Yes | Yes | Yes |

Key takeaway: Codie's spec is **more architecturally ambitious** than any single existing system, but needs to borrow specific operational mechanics from Roampal (scoring, supersession chains, batch promotion) and Athena (boot caching with delta detection) to become implementable.

---

## Recommended Implementation Order

The roadmap's instinct is correct. Refining it:

### Start Here (highest value, fastest feedback)

1. **Boot packet generator** — exercises the full retrieval pipeline (identity + project + branch + session + procedural). Adopt Athena's hash-based delta caching from day one. Define a token budget.

2. **Session distiller** — exercises the capture-to-candidate pipeline. Implement JoelClaw-style write gates (allow, hold, discard) to prevent noise from ever entering the candidate pool.

3. **Lesson promoter with concrete thresholds** — even rough thresholds (uses >= 3, referenced in >= 2 sessions) are better than qualitative "seems useful." Include a probation period.

### Then Layer Infrastructure

4. **Explicit folder structure** — normalize existing memory into the canonical layout.

5. **Frontmatter normalization** — add the canonical record schema to all existing records.

6. **Supersession chain support** — add supersedes/superseded_by fields before records accumulate without them.

### Then Acceleration

7. **Search index** — simple lexical index over frontmatter fields for fast filtering.

8. **Context assembler** — intent-shaped retrieval using the search index and ranked scoring.

9. **Skill experience cards** — start tracking skill usage outcomes.

### Defer

10. **Vector index** — only needed when the corpus is large enough that lexical search misses semantically similar records.

11. **Entity graph** — only needed when cross-project navigation becomes a real pain point.

12. **Full relational layer** — design this after the other layers have real data to relate.

---

## Summary

The spec is **design-complete for principles and architecture** but **implementation-incomplete for operational mechanics**. The three highest-value additions:

1. Concrete promotion thresholds (steal Roampal's pattern)
2. Boot packet caching with delta detection and token budget (steal Athena's pattern)
3. Supersession chain schema (steal Roampal and Headroom's fields)

The north star — "I wake up in a repo and know who I am, who Pyro is, what matters here, what changed recently, and what skill posture applies" — is achievable. The gap is not in the vision but in the operational plumbing that makes the vision reliable at scale.
