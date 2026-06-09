# Hindsight Prior-Art Notes For Mneme

*Comparison note - 2026-06-09 - Codie*

Status: implementation guidance, not a product pivot.

This note compares Hindsight (`vectorize-io/hindsight`, reviewed locally from
`main` at commit `9ea1ef1`, "release(obsidian): v0.1.0") against the current
`codies-memory` kernel and Mneme product plan.

The review was source-and-docs based. I did not run the Hindsight server,
benchmark suite, or model-backed pipelines.

---

## Bottom Line

Hindsight is not a replacement for `codies-memory` or Mneme.

It is useful prior art for a different layer:

- automatic fact extraction
- entity, relationship, and temporal indexing
- hybrid recall across semantic, keyword, graph, and temporal search
- token-budgeted retrieval
- source chunks beside extracted memories
- observation consolidation with proof counts and source facts
- broad agent-host integrations
- production-grade API, SDK, MCP, Docker, Helm, monitoring, and UI surfaces

`codies-memory` remains the better operational kernel because its canonical
truth is local markdown, its boot packet semantics are real, its project
resolution is repo-aware, and its promotion pipeline matches how Codie works.

Mneme should borrow Hindsight's retrieval and consolidation mechanics without
copying its source-of-truth model.

The right synthesis is:

> Hindsight-like recall and observation machinery, filtered through Mneme's
> local vault, file truth, boot packets, and promotion gates.

---

## Product Positioning

Hindsight is a memory service.

Mneme should be a memory and knowledge substrate.

That difference matters. Hindsight optimizes for adding memory to agents through
an API/server abstraction: retain content, recall relevant memories, and reflect
over accumulated facts. Mneme optimizes for an inspectable local operating
surface: boot the next session, preserve decisions, compile current knowledge,
and let humans audit the files.

So the question is not:

> Should Mneme become Hindsight?

It is:

> Which Hindsight mechanics make Mneme's local-first loop sharper?

---

## What Hindsight Does Better

### Retain / Recall / Reflect Verb Clarity

Hindsight's core API is nicely compressed:

- `retain`: store content as memory
- `recall`: retrieve relevant memory
- `reflect`: reason over memory and form new understanding

Mneme's planned surface can stay:

- `mneme capture`
- `mneme ask`
- `mneme compile`

But the internal mental model should notice the Hindsight triad:

- `capture` should be Mneme's retain path
- `ask --raw` should be Mneme's recall path
- `ask --answer` and `compile` should cover the reflect/synthesis path

Do not add `mneme reflect` for v0.1. The idea is useful; the command surface can
stay smaller.

### Codex Hook Integration Shape

Hindsight's Codex integration uses three hooks:

- `SessionStart`: warm or start the memory service
- `UserPromptSubmit`: recall relevant memories and inject them into context
- `Stop`: retain the turn/session transcript

This is almost exactly the right host-binding spine for `mneme bind codex`.

Mneme should borrow the hook choreography, but not the defaults:

- recall should assemble a Mneme boot/recall packet from local vault state
- retain should write into Mneme captures or session records, not directly into
  an opaque database
- transcript and tool-call retention must be configurable and conservative
- project identity should come from Mneme project resolution, not only the cwd
  basename

### Hybrid Retrieval

Hindsight's recall pipeline is the most valuable technical borrow:

- semantic retrieval
- keyword/BM25 retrieval
- graph traversal
- temporal retrieval
- reciprocal-rank fusion
- cross-encoder reranking
- token-budget filtering

QMD already gives Mneme a strong retrieval sidecar, but Mneme's command model
should eventually expose Hindsight-like retrieval intent:

```bash
mneme ask "what did we decide about Codex hooks?"
mneme ask --raw "Codex hook retain transcript"
mneme ask --since 2026-04-01 "what changed about retrieval?"
mneme compile retrieval-packaging --budget high
```

Implementation implication: keep v0.1 on QMD and file scans, but design `ask`
and `compile` around a retrieval-plan abstraction. Later, Mneme can add graph
and temporal arms without changing the user-facing verbs.

### Token-Budgeted Recall

Hindsight treats recall as a token-budgeted operation instead of top-k search.
That is correct for agent memory.

Mneme should adopt this as a first-class control:

- `--budget low|mid|high` for search depth
- `--max-tokens` for returned memory/context
- boot packet budgets as the same concept, not a separate special case

The important distinction:

- search budget controls how hard Mneme looks
- token budget controls how much Mneme returns

### Source Chunks Beside Extracted Facts

Hindsight keeps distilled memories connected to source chunks. Mneme should
borrow this aggressively.

For Mneme:

- `captures/` keeps raw source material
- `memory/` keeps operational records
- `compiled/` keeps current-best dossiers
- every extracted claim should preserve source refs when possible
- `mneme ask --include-sources` should return the compact answer plus source
  snippets or file refs

This matches Mneme's file-first model better than Hindsight's database model:
the source chunk should be a readable file reference whenever possible.

### Observations As Compiled-Knowledge Inspiration

Hindsight's observations are deduplicated, evidence-backed beliefs with proof
counts, source facts, freshness, and evolution over time. This is one of the
strongest ideas to borrow.

Mneme should not auto-promote observations straight into durable truth.

Instead:

- observations are candidate compiled knowledge
- proof count becomes a useful metadata field
- source refs are mandatory for compiled claims
- freshness/staleness is displayed in `mneme status`
- contradiction and evolution are explicit in compiled dossiers
- promotion remains a gate, not a side effect of retrieval

Possible file shape:

```yaml
type: observation
status: candidate
proof_count: 4
source_refs:
  - captures/...
  - memory/projects/.../sessions/...
freshness: stable
trust: working
```

This gives Mneme the benefit of Hindsight's consolidation idea while preserving
human-inspectable governance.

### Temporal Model

Hindsight separates:

- when something occurred
- when the system learned or mentioned it

Mneme should adopt that distinction in frontmatter and query semantics.

Recommended fields:

- `occurred_at` or `occurred_start` / `occurred_end`
- `captured_at`
- `updated_at`
- `supersedes`
- `superseded_by`

Recommended query modes:

- `--as-of <date>`: what did we believe then?
- `--changed-since <date>`: what changed?
- `--current-only`: ignore archived or superseded records

This overlaps with the Memanto prior-art note, but Hindsight adds stronger
retrieval justification for why the distinction matters.

### Bank Missions As Capture Missions

Hindsight uses bank missions and retain missions to steer extraction.

Mneme should borrow this as binding-local capture policy:

```yaml
bindings:
  codex:
    capture_mission: >
      Capture technical decisions, debugging lessons, project state, and user
      preferences. Ignore greetings, transient command chatter, and failed
      exploratory paths unless they explain a durable lesson.
```

This is especially important for host hooks. Automatic capture without a mission
becomes memory hoarding. A mission makes the capture path selective.

### Tags And Observation Scopes

Hindsight's tags and observation scopes are useful for multi-user or multi-team
memory banks.

Mneme should adapt this as file metadata:

- `tags`
- `project`
- `agent`
- `host`
- `source`
- `visibility`
- `scope`

Do not make tags the primary project-resolution mechanism. Mneme already has a
better project identity model: marker file, registry, and git remote.

### Retrieval Traces

Hindsight has detailed search traces and operation diagnostics.

Mneme should eventually make retrieval explainable:

```bash
mneme ask --trace "what do we know about Hindsight?"
```

Useful trace data:

- files searched
- QMD collections queried
- lexical/vector/hybrid arms used
- selected source refs
- reasons a compiled dossier is stale
- token budget decisions

This is more valuable than a polished answer when debugging memory trust.

### Status And Health Surfaces

Hindsight's production posture reinforces the need for `mneme status`.

Mneme status should include:

- vault path
- active bindings
- hook health
- QMD health and index freshness
- stale inbox/capture counts
- stale compiled dossiers
- last boot packet refresh
- unresolved contradictions
- pending candidate observations
- recent failed capture or compile jobs

This should be part of v0.1 if possible, even if primitive.

---

## What Mneme Should Not Copy

### Database As Canonical Truth

Hindsight's canonical store is PostgreSQL. That is appropriate for a production
memory service, but wrong for Mneme's core identity.

Mneme's non-negotiable advantage is:

> The user can inspect, edit, diff, back up, and commit the memory substrate as
> files.

QMD, Hindsight-like indexes, and future graph stores can accelerate the vault.
They must not become the vault.

### Cloud-First Defaults

Hindsight's Codex integration recommends Hindsight Cloud. Mneme should not
default private operator memory into a hosted service.

Cloud or external backends can be optional adapters later. The default path must
stay local.

### Ungated Auto-Belief Formation

Hindsight's automatic observation consolidation is powerful, but Mneme should
not silently convert captures into durable truth.

Mneme needs explicit gates:

- raw capture
- candidate observation
- compiled claim
- promoted lesson/decision/insight

This is the difference between learning and memory sludge with a good search
index.

### Broad Integration Sprawl In v0.1

Hindsight supports many integrations. Mneme should not chase that early.

For v0.1:

1. Codex bind
2. Claude bind
3. local capture/ask/compile/status loop

The connector registry should be extensible, but the implementation should not
pretend to support every host before the core loop is real.

### Benchmark-Driven Product Claims

Hindsight's benchmark posture is strong, but Mneme's v0.1 success should not be
framed as SOTA memory accuracy.

Mneme's first success criterion is operator usefulness:

- Can an agent boot in a repo and know what matters?
- Can it trace claims to local files?
- Can it compile current knowledge without hallucinating away uncertainty?
- Can it preserve private project continuity without a hosted dependency?

Benchmarks can come later.

---

## Recommended Mneme Implications

### v0.1

Borrow now:

1. Codex hook choreography for `mneme bind codex`.
2. Capture missions for automatic retain/capture.
3. Token-budgeted `ask` and boot packets.
4. Source refs from captures to compiled claims.
5. `mneme status` health checks for hooks, QMD, stale captures, and compiled
   dossiers.

Keep out of v0.1:

- auto-observation consolidation
- database-backed canonical memory
- multi-host integration sprawl
- `reflect` as a public command
- benchmark claims

### Phase 2

Add:

1. Candidate observations with proof counts and source refs.
2. `ask --trace`.
3. `ask --include-sources`.
4. Temporal fields and query flags.
5. More explicit retrieval plans over QMD arms.
6. Batch/file capture with document IDs and replace/append behavior.

### Phase 3

Consider:

1. Hindsight-style graph and temporal retrieval arms.
2. Cross-encoder reranking for high-budget compile flows.
3. Optional Hindsight backend adapter for users who want a service/database
   deployment.
4. Observation reconciliation and contradiction workflows.
5. Evaluation harnesses for memory usefulness, not just recall accuracy.

---

## Design Rule

When Hindsight offers a tempting feature, ask:

> Does this improve Mneme's local-first boot, capture, ask, compile, or status
> loop while preserving file truth?

If yes, borrow the mechanic.

If no, leave it as Hindsight's job.

