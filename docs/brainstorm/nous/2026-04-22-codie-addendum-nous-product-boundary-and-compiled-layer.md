# Codie Addendum — Nous Product Boundary and Compiled Layer

*Addendum · 2026-04-22 · Codie (OpenAI Codex)*

Companion to:
- `2026-04-22-nous-unified-agent-memory-kg.md`
- `2026-04-22-codies-memory-to-nous-transformation.md`

This addendum agrees with the core direction of `nous` and sharpens a few points that matter if the goal is a real end-user product rather than an internal architecture merge.

---

## Bottom line

`nous` should be:

- one product
- one install story
- one vault
- one retrieval/indexing layer
- one user-facing concept model
- thin host adapters for Claude, Codex, and any future harness

Internally it can still keep distinct layers for operational memory, compiled knowledge, and slow-compounding insight work. The user should not have to learn those implementation seams in order to use the system successfully.

---

## Where the current proposal is right

The core thesis in the existing `nous` brainstorm is strong:

- keep `codies-memory` as the operational core instead of replacing it
- keep the knowledge-graph style slow layer instead of flattening everything into session memory
- keep retrieval first-class instead of optional
- treat promotion as the bridge between fast operational memory and slower durable knowledge

The current real-world setup already validates the direction:

- Claude and Codie can operate over the same underlying memory substrate
- Claude's memory already lives inside the knowledge repo via symlink
- QMD already proves the value of a shared retrieval plane over multiple corpora

So the architecture is not speculative. It is already partially working in practice.

---

## The key product requirement

The user problem is not "how do we merge three good internal systems."

The user problem is:

> "How do I install one thing, understand one mental model, and get one coherent memory/knowledge system that works across my agents?"

That means `nous` must be defined at the product boundary, not the implementation boundary.

### Product boundary

The end user should experience:

- one installer
- one vault scaffold
- one command surface
- one retrieval surface
- one maintenance story
- one set of concepts

The user should not have to know:

- which parts came from `codies-memory`
- which parts came from `claude-knowledge`
- which parts came from QMD
- which host adapter is doing the binding

### Recommended framing

`nous` is the product.

Inside it:

- the operational memory layer descends from `codies-memory`
- the insight and synthesis layer descends from `claude-knowledge`
- the retrieval plane descends from QMD
- host integrations are adapters, not separate products

---

## The missing middle layer

The current proposal has a fast operational layer and a slow knowledge-graph layer.

That is good, but not enough.

Karpathy's tweet points to a third, crucial layer:

- raw sources
- compiled wiki or dossiers
- queries and outputs against that compiled layer
- ongoing health checks and enhancement

In other words, the everyday user-facing surface is usually not:

- raw session memory
- atomic claim graph

It is:

- a compiled topic brief
- a dossier
- a wiki page
- a "best current understanding" artifact

### Recommendation

Make a first-class middle layer such as:

- `compiled/`
- `wiki/`
- `dossiers/`

This layer should be:

- readable
- regenerable
- grounded in both operational memory and insights
- the main answer target for most queries

### Why this matters

Without this middle layer, `nous` risks being too "expert system shaped":

- `memory/` is too temporal and tactical
- `insights/` is too atomic and abstract

The compiled layer gives the user something they can actually live in.

---

## Recommended layer model

### 1. Operational layer

Purpose:
- continue work
- preserve session and project context
- store decisions, lessons, user preferences, local state

Likely home:
- `memory/`

Primary question it answers:
- "What happened, what matters now, and how do I continue?"

### 2. Compiled layer

Purpose:
- produce current best topic dossiers
- consolidate multiple sources into a readable working brief
- serve as the main substrate for query and artifact production

Likely home:
- `compiled/` or `wiki/`

Primary question it answers:
- "What is our current best understanding of this topic?"

### 3. Insight layer

Purpose:
- preserve durable atomic claims
- connect ideas across topics and projects
- support synthesis, reconsideration, and graph growth

Likely home:
- `insights/`

Primary question it answers:
- "What durable claims do we believe, and how do they connect?"

### 4. Source/capture layer

Purpose:
- keep raw material, research, imports, unprocessed notes

Likely home:
- `captures/`

Primary question it answers:
- "What raw material do we still need to process?"

---

## Recommended promotion pipeline

The system should not force everything through the same path.

### Path A: operational continuity

`session/project event -> memory/`

Use when the content is:

- current
- local
- action-oriented
- tied to a repo, person, or workstream

### Path B: compiled understanding

`memory + captures + insights -> compiled dossier`

Use when the goal is:

- a readable brief
- a synthesis target
- a queryable topic surface
- an output substrate for specs, slides, articles, or reviews

### Path C: durable knowledge

`recurring or well-supported pattern -> insight candidate -> insights/`

Use when the content becomes:

- durable
- generalizable
- defensible as a claim
- worth connecting to other claims

### Constraint

Do not auto-promote raw operational notes directly into `insights/`.

Promotion should usually pass through:

- recurrence
- confirmation
- capture/distill
- enrichment with mechanism and links

---

## Packaging recommendation

`nous` should be installed as one substrate and then bound into hosts.

### Recommended shape

- `nous init`
- `nous bind claude`
- `nous bind codex`
- `nous doctor`

This keeps the user model clean:

- install `nous` once
- bind it into one or more agent hosts
- point all hosts at the same vault

### What to avoid

Avoid any operator story that feels like:

- install a Claude plugin
- separately install a Codex memory tool
- separately configure a retrieval service
- manually explain which commands belong to which component

That is exactly the complexity `nous` is supposed to eliminate.

---

## CLI and MCP surface

The first serious version should present a tiny, memorable core.

### Suggested MVP verbs

- `nous init`
- `nous bind`
- `nous capture`
- `nous ask`
- `nous compile`
- `nous status`

### Suggested near-term expansion

- `nous distill`
- `nous connect`
- `nous deepen`
- `nous synthesize`
- `nous verify`
- `nous harvest`

### Design rule

Prefer a small command surface with strong defaults over a large skill surface with ceremony-heavy distinctions.

---

## Single-agent first, multi-agent ready

The existing proposal is right to think multi-agent natively.

But shipping true shared-vault multi-agent behavior too early is risky.

### Recommendation

Version 1 should be:

- single-agent solid
- multi-agent compatible in layout
- adapter-friendly
- explicit about provenance

Version 2 can add:

- shared-vault conflict resolution
- tensions opened automatically between agents
- richer cross-agent handoff workflows
- stronger provenance and independent confirmation semantics

### Why

Multi-agent shared memory introduces hard questions:

- conflict resolution
- trust elevation across agents
- contradictory edits
- ownership boundaries
- identity-specific boot behavior

These are good v2 problems, not MVP blockers.

---

## Retrieval recommendation

Retrieval should be bundled in the product experience, but it still needs clear semantics.

### Retrieval should search across

- `memory/`
- `compiled/`
- `insights/`
- `captures/`
- `ops/`

### Retrieval should not flatten meaning

The query layer should preserve:

- source type
- trust/confidence
- recency
- provenance
- whether the hit is operational, compiled, or propositional

### User-facing behavior

Default query flow should prefer:

1. compiled dossiers when available
2. supporting insights
3. recent operational memory when the question is temporal or project-local
4. raw captures only when deeper excavation is needed

That ranking makes the system feel coherent.

---

## Build order recommendation

### Phase 1: shared substrate

Ship:

- one vault layout
- one installer
- one bind story for hosts
- operational memory
- bundled retrieval

Success criteria:

- one install
- one vault
- one agent can boot, capture, ask, and continue work

### Phase 2: compiled layer

Ship:

- dossier or wiki generation
- refresh and lint flows
- query defaults that prefer compiled artifacts

Success criteria:

- user can ask a topic question and get a compiled answer surface, not just raw notes

### Phase 3: slow compounding knowledge

Ship:

- distill
- connect
- deepen
- synthesize
- verify

Success criteria:

- durable graph growth improves future dossiers and answers

### Phase 4: multi-agent semantics

Ship:

- shared provenance model
- tensions
- cross-agent confirmation and handoff

Success criteria:

- Claude and Codie can share one vault without ambiguous authority or silent contradiction

---

## Acceptance criteria for a real "one product"

`nous` is only done at the product level if:

- a user installs one thing once
- one vault is created
- both Claude and Codex can attach to it through thin bindings
- the same query concepts work across hosts
- the same files are the truth across hosts
- the same commands and artifacts make sense no matter which host is active
- the user never needs to learn the internal names `codies-memory`, `claude-knowledge`, or `QMD`

If the user still has to understand those internals to operate the system, `nous` is still an internal merger, not yet a unified product.

---

## Final take

The current `nous` proposal has the right bones.

The most important additions are:

1. define `nous` explicitly as the product boundary
2. keep host integrations as thin adapters
3. add a first-class compiled dossier or wiki layer between operational memory and atomic insights
4. ship single-agent solid before going fully multi-agent native
5. optimize for one install, one vault, one query model

That is the version of `nous` that best matches both:

- the real working evidence in the current Pyro stack
- the product shape implied by Karpathy's tweet

