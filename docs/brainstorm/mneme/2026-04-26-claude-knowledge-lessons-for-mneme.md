# Claude-Knowledge Lessons For Mneme

*Research synthesis - 2026-04-26 - Codie*

Status: **orientation and product insight note**. This document distills what
Mneme should learn from `/home/pyro/projects/agents/claude-knowledge`, the
current KG-focused "big brother" implementation.

Use this as input to Mneme phase 1 planning. It does not supersede the canonical
product spec, decisions log, or ADR-001.

Companion note: `2026-04-26-discriminator-authoring-spine-for-mneme.md`
captures the later Akinator-for-ideas synthesis. Treat it as an
implementation-facing principle for `compile`, future `distill`, future
`ideate`, and `doctor`.

---

## Source Surfaces Read

Mneme docs:

- `2026-04-23-mneme-product-spec.md`
- `2026-04-26-decisions-resolved.md`
- `2026-04-26-adr-001-retrieval-packaging.md`
- `2026-04-22-mneme-unified-agent-memory-kg.md`
- `2026-04-22-codies-memory-to-mneme-transformation.md`
- `2026-04-22-codie-addendum-mneme-product-boundary-and-compiled-layer.md`

Claude-knowledge surfaces:

- `CLAUDE.md`
- `CHEATSHEET.md`
- `manual/skills.md`
- `.claude/skills/*/SKILL.md`, with emphasis on `seed`, `distill`,
  `connect`, `deepen`, `verify`, `pipeline`, `ralph`, `graph`,
  `synthesize`, `harvest`, `remember`, `reconsider`, and `next`
- `.claude/hooks/*.sh`
- `ops/config.yaml`
- `ops/derivation-manifest.md`
- `ops/methodology/*.md`
- `templates/*.md`
- selected insight files and maps around memory systems, skill architecture,
  QMD, graph synthesis, and pipeline discipline

Live state observed:

- `claude-knowledge` lives at `/home/pyro/projects/agents/claude-knowledge`.
- The repo currently contains 310 markdown files in `insights/`, including
  12 maps by local file count.
- `captures/` is empty at time of read.
- `ops/observations/` and `ops/tensions/` have no pending items by local grep.
- The working tree is not clean. During this read it was already ahead of
  origin and had unstaged changes; the exact dirty-file set changed while I was
  inspecting it, so do not attribute those `claude-knowledge` changes to this
  synthesis pass.
- Running multiple `qmd query` commands in parallel produced a live SQLite
  `database is locked` failure and a hung Bun process. I killed the hung query
  process. Mneme should treat QMD subprocess concurrency as a real product
  failure mode, not a theoretical edge case.

---

## The Actual Shape Of Claude-Knowledge

Claude-knowledge is not just "a folder of insights." It is a working
knowledge-production machine with five interacting surfaces:

1. **The graph:** `insights/*.md` atomic prose-claim notes plus insight maps.
2. **The intake layer:** `captures/` for unprocessed source material and
   `archive/` for claimed or processed material.
3. **The operational memory bridge:** `memory/`, a codies-memory-style fast
   lane embedded inside the KG repo.
4. **The ops layer:** `ops/` for queue state, observations, tensions, sessions,
   methodology, reminders, and maintenance.
5. **The skill layer:** `.claude/skills/` as executable workflow documents.

The most important product lesson: the KG's intelligence is not mostly in the
storage model. It is in the disciplined flows that transform material:

```text
capture/source
  -> seed
  -> distill
  -> connect
  -> deepen
  -> verify
  -> graph/synthesize/reconsider over time
```

The repo is "slow memory." It deliberately rejects quick operational facts as
first-class KG material unless they have been processed into durable claims,
lessons, or methodology.

---

## Core Flow Model

### 1. Seed

`seed` claims a source for processing. It checks duplicates, creates an archive
folder, moves capture files into their permanent archive path, creates a queue
task, and assigns globally unique claim numbers.

Product lesson for Mneme: import/capture and processing are separate states.
Raw material is not "in the knowledge base" just because it exists on disk.

### 2. Distill

`distill` extracts atomic claims, implementation ideas, tensions, validations,
open questions, and enrichment tasks. It defaults toward comprehensive extraction
for domain-relevant sources, while still requiring claim-shaped outputs.

The newest important change is the **framing-questioning gate**. Before
extracting, the skill identifies the source's central premise and searches the
vault for support, complications, or contradictions. If the premise is wrong,
the pipeline pauses before it can produce well-structured wrongness.

Product lesson for Mneme: every extraction or compilation workflow needs a
premise check before the system applies rigor. Otherwise Mneme will faithfully
compound bad frames.

### 3. Connect

`connect` finds semantic relationships between a target insight and the graph.
It uses dual discovery:

- curated insight-map browsing
- QMD semantic or hybrid search

Every connection must pass the articulation test:

```text
[[A]] connects to [[B]] because [specific reason]
```

Product lesson for Mneme: graph edges are judgments, not search hits. Search
can propose candidates, but Mneme must own the relationship semantics.

The 2026-04-26 discriminator-authoring pass showed a second job for `connect`:
it reconciles vocabulary drift. After `distill` creates or enriches insights,
some links point at older names, candidate claims that were not promoted, source
artifacts outside `insights/`, or concepts whose titles changed during the
distill pass. Those are not always "bad links" in the same sense. They are
evidence that the graph's ontology moved faster than the edge layer.

Product lesson for Mneme: `connect` should treat broken links and near-miss
links as graph-evolution signals. It should classify whether a failed edge is a
rename, missing source, unpromoted candidate, stale edge, or ontology drift
before treating it as a simple typo.

### 4. Deepen

`deepen` is the backward pass. It asks:

```text
If I wrote this insight today, with everything I now know, what would be different?
```

It can add connections, rewrite content, sharpen claims, split broad insights,
or challenge old claims.

Product lesson for Mneme: knowledge graph maintenance is not just adding new
nodes. Old nodes need reconsideration when new material changes their meaning.

### 5. Verify

`verify` combines description quality, schema validation, and graph health. The
important boundary is deterministic vs probabilistic:

- deterministic hard gates: schema, enum validity, YAML parse, link existence
- probabilistic soft gates: extraction quality, connection quality, claim
  sharpness, premise judgment

Product lesson for Mneme: `doctor` should distinguish hard mechanical failures
from judgment-quality warnings. Mixing them will make the tool feel both too
strict and not strict enough.

### 6. Graph And Synthesize

`graph` exposes structural analysis: health, triangles, bridges, clusters, hubs,
siblings, and traversal.

`synthesize` turns the graph into an idea engine through:

- trisociation
- bridge synthesis
- counterfactuals
- deliberately distant retrieval

The crucial distinction:

```text
answering wants nearest relevant results
ideation wants distant but non-random results
```

Product lesson for Mneme: `ask` and `synthesize` should not share one ranking
profile. They need different retrieval semantics.

### 7. Harvest, Remember, Reconsider

`harvest` mines operational memory for transferable lessons. `remember` turns
friction into methodology notes. `reconsider` triages observations and tensions,
detects patterns, and proposes system changes with approval.

Product lesson for Mneme: the route from operational memory to durable knowledge
must exist, but it should be deliberate. This is the bridge between
`memory/` and `insights/`.

---

## Skill-System Lessons For Mneme

Claude-knowledge's skills are not independent commands. They form a stateful
lifecycle graph through shared artifacts:

```text
captures/
  -> ops/queue/
  -> insights/
  -> insight maps
  -> ops/observations and ops/tensions
  -> ops/methodology
```

Each skill reads files written by earlier skills and writes files consumed by
later skills. This is the blackboard pattern at skill level.

Mneme should steal the architecture, not the surface area.

The canonical spec is right to keep v0.1 to:

- `init`
- `bind`
- `capture`
- `ask`
- `compile`
- `status`
- `doctor`

But internally Mneme should model every command as a typed flow with declared:

- inputs
- outputs
- deterministic gates
- probabilistic judgments
- state transitions
- provenance requirements
- recovery/resume point

That gives Mneme the power of the skill DAG without exposing users to 20+
commands on day one.

---

## What Mneme Should Inherit

### Atomic Claims

Insights should remain prose-sentence claims, not labels. Titles should pass:

```text
This insight argues that [title].
```

This is what makes links composable in prose.

### Insight Maps

Maps are not categories. They are maintained navigation surfaces. Mneme's
`compiled/` layer should probably produce human-readable dossiers, while
`insights/*-map.md` or an equivalent map layer preserves graph navigation.

### Framing Gate

The framing-questioning gate should become a first-class Mneme primitive.
Recommended places:

- before `mneme compile <topic>`
- before future `mneme distill`
- before migration-generated dossiers that summarize old corpora

### Dual Discovery

Connection finding should always combine:

- curated structure (`compiled/`, maps, existing links)
- retrieval candidates (QMD)

Either one alone is weaker.

### Agentic Memory Management

The system should let agents decide what matters, but only through controlled
write paths. The agent has context external heuristics do not, but invariants
belong in the CLI.

### CLI-As-Write-Path

Humans inspect markdown directly. Agents write through typed commands. This
keeps write gates, provenance, locks, validation, and auditability centralized.

### Slow-Layer Boundary

Claude-knowledge's strongest discipline is saying no to quick facts. Mneme must
preserve that by routing raw operational facts to `memory/`, source material to
`captures/`, current-best briefs to `compiled/`, and durable claims to
`insights/`.

---

## What Mneme Should Avoid

### Exposing The Whole Skill Pack As Product Surface

The KG works, but the visible command surface is too expert-shaped for Mneme
v0.1. `distill`, `connect`, `deepen`, `verify`, `reconsider`, `harvest`, and
`synthesize` are real capabilities, but they should initially appear as internal
flows behind `compile`, `ask`, `doctor`, and future advanced commands.

### Treating QMD As Infinitely Concurrent

Live experiment: parallel `qmd query` calls caused `SQLiteError: database is
locked`, then a Bun crash and hung query process.

Mneme's managed sidecar needs:

- a sidecar-owned lock around QMD cache writes, update, embed, and rerank
- bounded timeouts on every QMD call
- `doctor` checks for stale locks and hung sidecar processes
- a fallback path that does not leave orphaned query processes running
- maybe a single long-lived QMD MCP process instead of many competing CLI
  invocations for heavy operations

This is now phase 1, not polish.

### Flattening Retrieval Semantics

QMD returns candidates. Mneme owns product ranking:

- `ask`: prefer `compiled/`, then high-confidence insights, then recent
  operational memory, then raw captures
- `compile`: use broad retrieval but cite source layer and staleness
- future `synthesize`: prefer bridge nodes and medium-distance results

One retrieval profile cannot serve all three.

### Auto-Promoting Operational Notes To Insights

Operational notes can be important, but they are not automatically durable
claims. Promotion needs recurrence, confirmation, or cross-project relevance.

### Confusing Candidate Generation With Knowledge

`synthesize` writes candidates to `captures/`, not `insights/`. This is exactly
right. Generated ideas become knowledge only after curation and distillation.

---

## Novel Mneme Ideas From The Existing KG

### 1. Retrieval Modes As Product Semantics

Add explicit retrieval modes behind the CLI:

```text
mneme ask       -> nearest relevant, compiled first
mneme compile   -> broad evidence gather, dossier shaped
mneme ideate    -> medium-distance bridge search, novelty first
mneme doctor    -> deterministic health probes
```

This is more honest than one generic "search" primitive. It turns the insight
"QA wants nearest; ideation wants distant but non-random" into product behavior.

### 2. Flow Manifests

Every Mneme command should have a hidden flow manifest:

```yaml
name: compile
reads: [compiled/cache, memory, insights, captures, ops]
writes: [compiled/cache, ops/observations]
deterministic_gates: [source_exists, qmd_healthy, citations_resolve]
probabilistic_steps: [premise_check, synthesis, summary]
resume_from: [retrieval_done, draft_written, verify_failed]
```

This makes the internal lifecycle graph inspectable without making users learn
the whole skill system.

### 3. Compiled Dossiers As The Human Interface To The KG

In claude-knowledge, maps are the navigation surface. In Mneme, `compiled/`
should be the everyday human surface:

- current-best understanding
- source trail
- relevant insights
- recent operational updates
- open tensions
- "what changed since last compile"

This turns `compiled/` into more than a cache. It becomes the readable bridge
between atomic graph and working user understanding.

### 4. Premise-Aware Compilation

`mneme compile <topic>` should begin by stating the dossier premise:

```text
This dossier assumes the topic is about [premise].
```

Then it should check for:

- supporting insights
- contradicting insights
- unresolved tensions
- stale source files

This directly imports the distill framing gate and prevents pretty dossiers
that summarize the wrong question.

### 5. Graph-Distance-Aware Ideation

Future `mneme synthesize` or `mneme ideate` should support:

- `--near`: incremental improvements
- `--bridge`: medium-distance cross-map synthesis
- `--wild`: distant analogical transfer with lower confidence

The graph already has the theory for this: bridge nodes and knowledge-distance
control are the difference between search and invention.

### 6. Doctor As Health Plus Drift, Not Just Install Check

`mneme doctor` should report:

- mechanical health: vault, config, hooks, QMD, locks, index freshness
- knowledge health: orphan insights, stale dossiers, broken links, pending
  captures, unresolved tensions
- process health: deterministic failures vs probabilistic warnings
- migration health: old hooks or configs still pointing at codies-memory or
  claude-knowledge

For link health specifically, `doctor` should not collapse every missing
wikilink into one bucket. It should classify:

- missing source artifact: the link points to a capture, PDF, archive, or other
  source outside `insights/`
- renamed insight: a semantically matching insight exists under a newer title
- unpromoted candidate: the link points to a candidate claim that never became
  an insight
- stale edge: the source and target both exist conceptually, but the edge was
  not updated after distill/connect changed one side
- ontology drift: the link failure reflects a vocabulary shift that should be
  resolved by `connect`, not patched mechanically

The current `claude-knowledge` system spreads this across `stats`, `graph`,
`verify`, hooks, scripts, and `next`. Mneme can unify it.

### 7. Harvest As The Operational-To-KG Bridge

Mneme should keep a route like:

```text
memory/projects/*/sessions
  -> harvest
  -> memory/procedural/lessons
  -> insight candidate
  -> insights/
```

This is the mechanism that prevents operational memory from staying local and
prevents KG insights from being divorced from real work.

### 8. Warm Boot Packets Should Prefer Pointers To Dossiers

Claude-knowledge proves a slow graph can become huge. Mneme boot should not
inject graph process. It should inject:

- current project memory
- relevant compiled dossier pointers
- a few high-confidence insight titles
- "ask/compile these topics if needed"

This applies the context-isolation insight: retrieval and processing happen
out-of-band; the active session receives clean results.

### 9. Dossier Staleness Should Be Citation-Based

The decisions log says compiled cache is stale when cited sources changed. That
should become a concrete invariant:

```yaml
compiled_at: ...
source_fingerprints:
  path: sha256 or mtime+size
```

Then `doctor` can deterministically say which dossiers are stale and why.

### 10. QMD Should Be Treated As A Managed Kernel

The sidecar should look more like a language server or Jupyter kernel than a
random subprocess:

- pinned version
- one config
- one index root
- one lifecycle owner
- serialized writes
- structured health
- graceful restart
- clear fallback

ADR-001 already points here. The live lock failure makes it mandatory.

---

## Recommended Implementation Implications

For phase 1, do not port all of claude-knowledge's skills. Port these
structural contracts instead:

1. **Vault layout:** `memory/`, `compiled/`, `insights/`, `captures/`, `ops/`,
   `self/`.
2. **CLI write path:** all agent writes go through `mneme`.
3. **QMD sidecar with locking:** no parallel unmanaged QMD queries.
4. **Layer-aware ranking:** QMD candidates in, Mneme-ranked results out.
5. **Dossier cache with citation staleness.**
6. **Doctor that covers retrieval, binding, stale compiled artifacts, and old
   system residue.**
7. **Flow-manifest style internals** so commands are resumable and inspectable.

For phase 2, bring in:

1. Framing gate for `compile`.
2. Compiled dossier templates.
3. Source-citation lint.
4. Harvest from operational memory to lessons.
5. Basic graph health checks.

For phase 3, bring in:

1. `distill`.
2. `connect`.
3. `deepen`.
4. `verify`.
5. `synthesize` or `ideate`, with explicit graph-distance modes.

---

## Bottom Line

Claude-knowledge's core contribution to Mneme is not "use markdown files for
insights." Mneme already knows that.

The deeper contribution is:

> durable knowledge is produced by stateful, inspectable, quality-gated flows
> over plain files, with search proposing candidates and the product owning the
> semantics.

Mneme should productize that without exposing the machinery too early.

The v0.1 product should feel like:

```text
Install. Bind. Capture. Ask. Compile. Continue.
```

But under the hood it should already be shaped like:

```text
raw material -> premise check -> typed transformation -> citation/provenance
-> layer-aware retrieval -> deterministic health -> slow compounding
```

That is the bridge from `codies-memory` and `claude-knowledge` into a single
product rather than an internal merger.
