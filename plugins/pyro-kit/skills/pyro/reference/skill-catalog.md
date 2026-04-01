# Pyro Kit Skill Catalog

## How to Read This Catalog

- **[Available]** -- Implemented in MVP, ready to use
- **[Planned]** -- Coming in post-MVP expansion

---

## Phase 0: Ignition

### /spark [Available]
- **Description**: Excavates a concrete idea from a vague feeling using propose-react-iterate
- **Triggers**: "I have a feeling", "something bugs me", "spark", vague project descriptions
- **Prerequisites**: None (entry point)
- **Outputs**: `.pyro/spark.md`, updates `.pyro/state.md`
- **Reads**: `~/.pyro/fascination-index.md`

### /remix [Available]
- **Description**: Reframes current idea through creative domain lenses -- produces concrete alternative proposals
- **Triggers**: "remix", "different angle", "creative lens"
- **Prerequisites**: `.pyro/spark.md`
- **Outputs**: Updates `.pyro/spark.md` with `remixed_from` field
- **Reads**: `.pyro/spark.md`, `skills/spark/reference/domain-lenses.md` (shared)
- **Replaces**: /remix + /thumbnail from original catalog

### /fascination [Available]
- **Description**: View fascination index -- browse themes, intensities, and cross-fascination connections
- **Triggers**: "fascination", "what am I into", "patterns"
- **Prerequisites**: `~/.pyro/fascination-index.md`
- **Outputs**: Read-only viewer, two modes: list (default), map (Mermaid diagram)
- **Reads**: `~/.pyro/fascination-index.md`

---

## Phase 1: Exploration

### /explore [Available]
- **Description**: Proposes 3-4 fundamentally different design directions with inline sketches and contrast capability
- **Triggers**: "explore", "directions", "design space", "sketch", "contrast", "compare"
- **Prerequisites**: `.pyro/spark.md`
- **Outputs**: `.pyro/explore.md`
- **Reads**: `.pyro/spark.md`
- **Replaces**: /explore + /sketch + /contrast from original catalog

### /narrow [Available]
- **Description**: Proposes a recommended direction with reasoning from your reactions, locks on acceptance
- **Triggers**: "narrow", "decide", "pick one", "lock direction"
- **Prerequisites**: `.pyro/explore.md`
- **Outputs**: Updates `.pyro/explore.md` (locked, locked_direction, ## Constraints), updates `.pyro/state.md`
- **Reads**: `.pyro/explore.md`

---

## Phase 2: Surface

### /surface [Available]
- **Description**: Generates a working interactive prototype from your locked direction, iterates on behavioral critique to convergence
- **Triggers**: "surface", "prototype", "build it", "show me"
- **Prerequisites**: `.pyro/explore.md` (locked: true)
- **Outputs**: `.pyro/surface.md`, prototype files in project directory
- **Reads**: `.pyro/explore.md`
- **Replaces**: /surface + /iterate + /converge + /state-map from original catalog

---

## Phase 3: Contract

### /contract [Available]
- **Description**: Derives API contracts, domain invariants, and NFR targets from your converged surface, freezes on approval
- **Triggers**: "contract", "derive", "extract contracts", "freeze", "invariants", "nfr"
- **Prerequisites**: Converged surface (G2)
- **Outputs**: `.pyro/contract.md`
- **Reads**: `.pyro/surface.md`
- **Replaces**: /derive + /invariants + /nfr + /freeze from original catalog

---

## Phase 4: Build

### /build [Available]
- **Description**: Proposes vertical slices from frozen contracts, implements one at a time while keeping the surface working, and reports release readiness
- **Triggers**: "build", "slice", "implement", "harden", "verify", "what to build first"
- **Prerequisites**: Frozen contracts (G3)
- **Outputs**: Working code, release readiness evidence
- **Reads**: `.pyro/contract.md`, `.pyro/surface.md`
- **Replaces**: /slice + /implement + /harden + /verify from original catalog

---

## Phase 5: Momentum

### /pulse [Available]
- **Description**: Momentum dashboard -- git metrics, spark quote, three concrete paths (push/pivot/shelve)
- **Triggers**: "pulse", "momentum", "am I stuck?", "check in"
- **Prerequisites**: `.pyro/state.md` (works without spark.md by inferring)
- **Outputs**: `.pyro/pulse-log.md` (append), updates `.pyro/state.md`
- **Reads**: git history via `git-activity.sh`, `.pyro/spark.md`

### /reframe [Available]
- **Description**: Injects novelty into stuck remaining work through creative domain lenses -- each lens produces one concrete actionable move
- **Triggers**: "reframe", "bored", "novelty", "stuck", "different angle on remaining work"
- **Prerequisites**: Active project (works best with .pyro/contract.md)
- **Outputs**: Appends to `.pyro/pulse-log.md` (reframe entry)
- **Reads**: `.pyro/contract.md`, `.pyro/surface.md`, `skills/spark/reference/domain-lenses.md` (shared)

### /scope [Available]
- **Description**: Soul-preserving scope cuts -- finds the minimum version that satisfies your core curiosity
- **Triggers**: "scope", "cut", "too big", "soul", "minimum viable"
- **Prerequisites**: `.pyro/spark.md` (for soul derivation)
- **Outputs**: `.pyro/scope.md`, writes `soul` field to `.pyro/state.md`
- **Reads**: `.pyro/spark.md`, `.pyro/contract.md`

### /decide [Available]
- **Description**: Expands your push/pivot/shelve decision into a milestone plan with natural re-evaluation points
- **Triggers**: "decide", "what should I do?", "plan", "milestones", "next steps"
- **Prerequisites**: /pulse decision in `.pyro/pulse-log.md`
- **Outputs**: `.pyro/decide.md`
- **Reads**: `.pyro/pulse-log.md`, `.pyro/scope.md`, `.pyro/contract.md`, `.pyro/surface.md`

---

## Phase 6: Lifecycle

### /autopsy [Available]
- **Description**: Extracts value from dead/shelved projects -- report, fascination update, composting
- **Triggers**: "autopsy", "shelve", "done with this", "extract value"
- **Prerequisites**: `.pyro/state.md`
- **Outputs**: `~/.pyro/autopsies/{name}.md`, updates `~/.pyro/fascination-index.md`, updates state (G7)

### /ship [Available]
- **Description**: Release checklist with gap analysis -- reads contracts and codebase to show what's left to ship
- **Triggers**: "ship", "release", "publish", "ready?", "what's left"
- **Prerequisites**: Built and verified (G5) -- works with degraded data if no contract.md
- **Outputs**: Release checklist (read-only, no state file)
- **Reads**: `.pyro/contract.md`, `.pyro/surface.md`, codebase, `phase-map.md`

### /revive [Available]
- **Description**: Archaeological analysis of abandoned repos -- revival options
- **Triggers**: "revive", "old project", "bring back", "resurrect"
- **Prerequisites**: Git repo with history (works on any repo, .pyro/ optional)
- **Outputs**: Revival options. Conditional writes: `.pyro/spark.md` (soul transplant), `.pyro/harvest.md` (organ harvest)
- **Reads**: code, commits, README, `.pyro/state.md`, `.pyro/spark.md`

### /patterns [Available]
- **Description**: Cross-project pattern analysis from fascination index and project history
- **Triggers**: "patterns", "what do I keep building?", "meta", "trends"
- **Prerequisites**: `~/.pyro/fascination-index.md` with entries
- **Outputs**: Pattern analysis (read-only, no state file)
- **Reads**: `~/.pyro/fascination-index.md`, `~/.pyro/project-registry.yaml`, `~/.pyro/autopsies/`

---

## Cross-phase

### /pyro [Available]
- **Description**: Lifecycle navigator -- reads state, suggests next skill
- **Triggers**: "pyro", "what's next?", "where am I?"
- **Subcommands**: init, status, list
- **Prerequisites**: None
- **Outputs**: Recommendation with reasoning

---

## Shared Infrastructure

Domain lenses (game design, music, screenwriting, architecture, improv, cooking) are shared reference material loaded by /spark, /remix, and /reframe -- not a separate skill. /reframe uses the same lens selection algorithm as /remix (vocabulary term matching + domain proximity bonus). See IGN-04 in REQUIREMENTS.md.
