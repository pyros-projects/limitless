# State File Schemas

Canonical schema definitions for all Pyro Kit state files. This is the single source of truth.

## Schema Freeze Policy

**FND-01 commitment:** Existing fields must not be renamed or removed during expansion. New fields may be added as optional with defaults. All MVP skills conform to these schemas. Any field change that would break an existing skill consumer is a breaking change and requires a new schema version.

This file documents the ACTUAL current schema as written by existing code. If inconsistencies exist between what `pyro-init.sh` writes and what skills expect, they are noted in the "Known Inconsistencies" section at the bottom rather than silently resolved.

## Foundation Principles

**FND-03 -- Interleaving Principle:** The wave/phase structure interleaves novel creative work with mechanical infrastructure work to prevent meta-abandonment. The ROADMAP.md design applies this principle:

- Phase 1 (mechanical): Foundation hardening -- schemas, budgets, catalogs
- Phase 2 (creative): Ignition expansion -- /remix, /fascination, /explore
- Phase 3 (mixed): Direction lock + SFD wrapper proof-of-concept
- Phase 4 (mechanical): SFD core wrappers -- /contract, /build
- Phase 5 (creative): Momentum expansion -- /reframe, /scope, /decide
- Phase 6 (mixed): Lifecycle expansion -- /ship, /revive, /patterns

This alternation ensures the developer building Pyro Kit does not hit a long stretch of pure infrastructure work, which is the exact pattern that triggers the 60-70% abandonment this tool is designed to prevent.

---

## .pyro/state.md

The primary project state file. Created by `pyro-init.sh`, read and updated by all skills.

### Frontmatter Fields

| Field | Type | Required | Default | Producer | Consumer(s) |
|-------|------|----------|---------|----------|-------------|
| `project` | String | Yes | Directory name or argument | `pyro-init.sh` | All skills |
| `phase` | Number (0-6) | Yes | `0` | `pyro-init.sh`; updated by `/autopsy` | `/pyro`, `/pulse`, `/spark`, `/autopsy` |
| `status` | String: `active` \| `shelved` \| `composted` | Yes | `active` | `pyro-init.sh`; updated by `/autopsy` | `/pyro`, `/pulse`, `/autopsy` |
| `soul` | String | Yes | `""` (empty) | `/spark` (on crystallize) | `/pyro`, `/pulse`, `/autopsy` |
| `original_spark` | String | Yes | `""` (empty) | `/spark` (on crystallize, never overwritten) | `/autopsy` |
| `last_skill` | String | Yes | `none` | Updated by each skill after execution | `/pyro` |
| `last_activity` | Date (YYYY-MM-DD) | Yes | Today's date | Updated by each skill | `/pyro`, `/pulse` |
| `momentum` | String: `steady` \| `rising` \| `declining` \| `stalled` \| `composted` | Yes | `steady` | `pyro-init.sh`; updated by `/pulse`, `/spark`, `/autopsy` | `/pyro`, `/pulse` |
| `gate_history` | Array of objects | Yes | `[]` (empty) | `/spark` (G0), `/pulse` (G6), `/autopsy` (G7) | `/pyro`, `/autopsy` |
| `pulse_count` | Number | Yes | `0` | `/pulse` (incremented on each completed pulse) | `/pyro`, `/pulse` |

### Body Sections

| Section | Required | Content Format |
|---------|----------|----------------|
| `## Current State` | Yes | Freeform status text describing current project state |
| `## Decisions Made` | Optional | Date-prefixed list: `- YYYY-MM-DD: {decision}` |

### Example (as written by `pyro-init.sh`)

```yaml
---
project: my-project
phase: 0
status: active
soul: ""
original_spark: ""
last_skill: none
last_activity: 2026-03-13
momentum: steady
gate_history: []
pulse_count: 0
---

## Current State
Project initialized. No work started yet.

## Decisions Made
- 2026-03-13: Project tracking initialized with Pyro Kit
```

### Gate History Entry Schema

Each entry in `gate_history` is an object with:

| Field | Type | Description |
|-------|------|-------------|
| `gate` | String | Gate identifier: `G0` (spark), `G6` (shelve decision), `G7` (autopsy) |
| `passed` | Boolean | Whether the gate was passed |
| `notes` | String | Date and description: `"YYYY-MM-DD -- {what happened}"` |

---

## .pyro/spark.md

The crystallized idea output from `/spark`. Read by `/explore` (planned) and referenced by `/pulse` and `/autopsy`.

### Frontmatter Fields

| Field | Type | Required | Default | Producer | Consumer(s) |
|-------|------|----------|---------|----------|-------------|
| `idea` | String | Yes | N/A | `/spark` (on crystallize) | `/explore`, `/pulse`, `/autopsy` |
| `sparked` | Date (YYYY-MM-DD) | Yes | N/A | `/spark` (on crystallize) | `/pulse`, `/autopsy` |
| `fascination_threads` | Array of strings | Yes | `[]` (empty if none matched) | `/spark` (from fascination index matching) | `/explore`, `/autopsy` |
| `thumbnails_considered` | Number | Yes | N/A | `/spark` (total generated across iterations) | Diagnostic only |
| `iterations` | Number | Yes | N/A | `/spark` (iterate() cycle count; 0 if first proposal accepted) | Diagnostic only |
| `remixed_from` | String | No | `""` (empty) | `/remix` (original idea text before remixing) | Diagnostic, traceability |
| `lenses_applied` | Array of strings | No | `[]` (empty) | `/remix` (appends lens names after each run) | `/remix` (excludes used lenses on re-invocation) |

### Body Sections

| Section | Required | Content Format |
|---------|----------|----------------|
| `## The Idea` | Yes | 2-3 paragraphs: what the thing IS (not what it does) |
| `## Why This` | Yes | Why this direction from input and fascination threads |
| `## Key Tensions` | Yes | 2-3 tensions or open questions for `/explore` to investigate |
| `## Original Input` | Yes | Verbatim developer input (or `"[no explicit input -- inferred from context]"`) |

### Example

```yaml
---
idea: "A CLI tool that captures your mental state before you leave a project"
sparked: 2026-03-12
fascination_threads: ["productivity-rituals", "context-preservation"]
thumbnails_considered: 6
iterations: 2
# Optional fields (added by /remix):
remixed_from: ""
lenses_applied: []
---

## The Idea
A tiny command-line utility called `leave` that you run before switching projects...

## Why This
The developer's frustration was with losing mental state during context switches...

## Key Tensions
- How minimal is minimal?
- Does it need habit formation affordances?
- "Context" vs. "state" -- mental state or code state?

## Original Input
"I hate how I lose context when switching between projects."
```

**Source:** `skills/spark/SKILL.md` (crystallize workflow, lines 273-337), `skills/spark/reference/spark-output-format.md`, `skills/remix/SKILL.md` (apply workflow)

---

## .pyro/explore.md

The exploration output from `/explore`. Records design directions, developer reactions, and leaning. Read by `/narrow` (planned).

### Frontmatter Fields

| Field | Type | Required | Default | Producer | Consumer(s) |
|-------|------|----------|---------|----------|-------------|
| `idea` | String | Yes | N/A | `/explore` (copied from spark.md) | `/narrow` |
| `explored` | Date (YYYY-MM-DD) | Yes | N/A | `/explore` (date of first exploration) | `/narrow` |
| `directions_count` | Number | Yes | `4` | `/explore` (number of directions generated) | `/narrow` |
| `leaning` | String or Array | Yes | `""` (empty) | `/explore` (developer's preferred direction(s)) | `/narrow` |
| `contrasts_performed` | Array of strings | Yes | `[]` (empty) | `/explore` (pairs compared, e.g., "A-C") | `/narrow` |
| `iterations` | Number | Yes | `0` | `/explore` (reaction cycle count) | Diagnostic |
| `locked` | Boolean | No | `false` | `/narrow` (set to `true` on lock) | `/surface` |
| `locked_direction` | String | No | `""` (empty) | `/narrow` (set to `"{letter}: {name}"` on lock) | `/surface` |

### Body Sections

| Section | Required | Content Format |
|---------|----------|----------------|
| `## Direction A: {Name}` | Yes | Scenario, Sketch, Key Bet (repeated for B, C, D) |
| `## Reactions` | Yes | Developer reactions logged during session |
| `## Contrasts` | Optional | Side-by-side tradeoff tables from contrast(A, B) calls |
| `## Leaning` | Yes | Developer's current preference and reasoning |
| `## Constraints` | No (added by `/narrow`) | Scope boundaries, interface constraints, core bet, key limitations for the locked direction |

### Example

```yaml
---
idea: "A CLI tool that captures your mental state before you leave a project"
explored: 2026-03-13
directions_count: 4
leaning: "A"
contrasts_performed: ["A-C"]
iterations: 2
---

## Direction A: The Two-Question Ritual
**Scenario:** You're about to switch repos. You run `leave`. Two questions appear in sequence...
**Sketch:** [CLI transcript]
**Key Bet:** Two questions is enough.

## Direction B: The Ambient Watcher
...

## Reactions
- "I like A's simplicity but C's data richness"
- "B feels too invasive"

## Contrasts
### A vs C
| Dimension | Direction A | Direction C |
|-----------|------------|------------|
| User Experience | Minimal, ritual-like | Rich, ambient |
| Technical Complexity | Low -- two prompts, one file | Medium -- file watchers, git hooks |
| Time to First Version | Weekend project | 1-2 weeks |
| Key Risk | Too simple to be useful | Too complex to become habit |
| Soul Alignment | Matches productivity-rituals fascination | Matches context-preservation fascination |

## Leaning
Leaning toward A. The ritual quality matches the fascination thread around productivity-rituals.
```

### Locked State (after /narrow)

When `/narrow` locks a direction, it adds two frontmatter fields and appends a `## Constraints` section:

```yaml
---
idea: "A CLI tool that captures your mental state before you leave a project"
explored: 2026-03-13
directions_count: 4
leaning: "A"
contrasts_performed: ["A-C"]
iterations: 2
locked: true
locked_direction: "A: The Two-Question Ritual"
---

## Direction A: The Two-Question Ritual
...

## Reactions
...

## Contrasts
...

## Leaning
...

## Constraints
- **Scope:** Two questions only -- no ambient watching, no git hooks
- **Interface:** CLI only, no GUI, no daemon
- **Core bet:** Ritual simplicity over data richness
- **Key limitations:** No context-awareness beyond what the developer types; no automatic detection of what changed
```

The `## Constraints` section captures scope boundaries and key limitations derived from the direction content, developer reactions, and contrast tradeoffs. It is the primary input for `/surface` to understand what to prototype and what is out of scope.

**Updated by:** `/explore` (all fields except locked, locked_direction, ## Constraints), `/narrow` (locked, locked_direction, ## Constraints)

**Source:** `skills/explore/SKILL.md` (explore workflow), `skills/explore/reference/explore-output-format.md`, `skills/narrow/SKILL.md` (lock workflow)

---

## .pyro/surface.md

The converged surface state written by `/surface`. It is the sole input for Phase 4's `/contract` skill. The Surface State Inventory must enumerate every interaction point so `/contract` can derive API contracts and domain invariants.

### Frontmatter Fields

| Field | Type | Required | Default | Producer | Consumer(s) |
|-------|------|----------|---------|----------|-------------|
| `surface_type` | String: `gui` \| `cli` \| `api` \| `pipeline` \| `agent` | Yes | N/A | `/surface` (keyword detection from locked direction) | `/contract` |
| `convergence_date` | Date (YYYY-MM-DD) | Yes | N/A | `/surface` (date convergence was declared) | `/contract` |
| `iterations` | Number | Yes | N/A | `/surface` (count of iteration rounds) | Diagnostic |
| `flows_count` | Number | Yes | N/A | `/surface` (count of flows in the prototype) | `/contract` |

### Body Sections

| Section | Required | Content Format |
|---------|----------|----------------|
| `## Flows` | Yes | Each flow with trigger and expected behavior (numbered steps) |
| `## Decisions` | Yes | Chronological design decisions: `- YYYY-MM-DD: [decision] -- [reasoning]` |
| `## Surface State Inventory` | Yes | Per-flow table of interaction points, expected behavior, states covered |
| `## Edge Cases` | Yes | Explored edge cases and their resolutions |

### Surface State Inventory Detail

The Surface State Inventory is the behavioral contract `/contract` will consume. Each flow gets a table:

```markdown
### Flow: [Flow Name]
| Interaction Point | Expected Behavior | States Covered |
|-------------------|-------------------|----------------|
| [button/command/endpoint] | [what happens] | [state list] |
```

**State classifications:**
- **in-scope** -- demonstrated in the prototype, behavior is converged
- **deferred** -- acknowledged as needed but not yet built into the prototype
- **n/a** -- not applicable to this interaction point

**Note:** This schema mirrors the spec in `skills/surface/reference/surface-output-format.md`.

**Source:** `skills/surface/SKILL.md` (converge workflow), `skills/surface/reference/surface-output-format.md`

---

## .pyro/contract.md

The frozen contract bundle written by `/contract`. It is the sole input for `/build`, which uses it to plan vertical slices and track hardening progress. Every item in contract.md must trace back to a specific artifact in surface.md.

### Frontmatter Fields

| Field | Type | Required | Default | Producer | Consumer(s) |
|-------|------|----------|---------|----------|-------------|
| `version` | Number | Yes | `1` | `/contract` (incremented on revision) | `/build` |
| `freeze_date` | Date (YYYY-MM-DD) | Yes | N/A | `/contract` (date of freeze) | `/build` |
| `surface_type` | String: `gui` \| `cli` \| `api` \| `pipeline` \| `agent` | Yes | N/A | `/contract` (copied from surface.md) | `/build` |
| `flows_count` | Number | Yes | N/A | `/contract` (from surface.md) | `/build` |
| `contracts_count` | Number | Yes | N/A | `/contract` (count of API contracts derived) | Diagnostic |
| `invariants_count` | Number | Yes | N/A | `/contract` (count of invariants derived) | Diagnostic |
| `nfr_count` | Number | Yes | N/A | `/contract` (count of NFRs derived) | Diagnostic |

### Body Sections

| Section | Required | Content Format |
|---------|----------|----------------|
| `## API Contracts` | Yes | Per-contract blocks: name, endpoint/interface, input, output, error shapes, "Derived from:" |
| `## Domain Invariants` | Yes | Per-invariant blocks: ID, rule, enforced at, "Derived from:" |
| `## Non-Functional Requirements` | Yes | Per-NFR blocks: ID, target, "Derived from:", verification |
| `## Acceptance Criteria` | Yes | Per-flow checklists of testable Given/When/Then assertions |
| `## Hardening Plan` | Yes | Table: component, current state, target state, priority |

### Example

```yaml
---
version: 1
freeze_date: 2026-03-15
surface_type: cli
flows_count: 3
contracts_count: 5
invariants_count: 3
nfr_count: 2
---

## API Contracts

### Contract 1: Leave (Create Note)
**Endpoint/Interface:** `leave` (no flags, no args)
**Input:** stdin: two prompted answers (strings, may be empty)
**Output:** stdout: "Noted. See you tomorrow." exit code: 0
**Error shapes:** Ctrl+C during prompt -> no file written, exit code: 130
**Derived from:** Flow 1 -- Basic Leave, SSI: `leave` command, Empty answer, Ctrl+C during prompt

### Contract 2: Return (Read Last Note)
**Endpoint/Interface:** `leave --return`
**Input:** flags: --return (no value)
**Output:** stdout: "Last time you said: {answer1}\nStill stuck on: {answer2}" exit code: 0
**Error shapes:** No notes exist -> stdout: "No leave notes yet." exit code: 0
**Derived from:** Flow 2 -- Return, SSI: `leave --return`, No leave notes exist

## Domain Invariants

### INV-1: Empty Answers Are Valid
**Rule:** The system must never reject empty input for either question.
**Enforced at:** Input validation -- no validation on answer content.
**Derived from:** Flow 1 -- Basic Leave, SSI: Empty answer -> Accept empty, write anyway

### INV-2: Storage Created on First Use
**Rule:** The .leave/ directory must be created silently if it does not exist.
**Enforced at:** Storage initialization before any read or write operation.
**Derived from:** Flow 1 -- Basic Leave, SSI: .leave/ missing -> Create directory silently

## Non-Functional Requirements

### NFR-1: Instant Response
**Target:** leave command completes in under 200ms (excluding user input time).
**Derived from:** Flow 1 -- Basic Leave: ritual metaphor implies near-instant response.
**Verification:** Time the command execution excluding prompt wait time.

## Acceptance Criteria

### Flow: Basic Leave
- [ ] Given a project directory, when user runs `leave`, then two questions are prompted in sequence
- [ ] Given prompted questions, when user answers both, then .leave/note.md is written with timestamp and answers
- [ ] Given no .leave/ directory, when user runs `leave`, then .leave/ is created silently

### Flow: Return
- [ ] Given a project with leave notes, when user runs `leave --return`, then the last note's answers are displayed
- [ ] Given no leave notes, when user runs `leave --return`, then "No leave notes yet." is displayed

## Hardening Plan

### Simulated Components
| Component | Current State | Target State | Priority |
|-----------|--------------|--------------|----------|
| Note storage | Mock data in variables | Real .leave/note.md file I/O | 1 |
| Prompt interaction | Simulated in prototype | Real stdin prompts | 1 |
| Error handling | Happy-path only | Signal handling, permission errors | 3 |
```

**Note:** The contract.md schema mirrors the spec in `skills/contract/reference/contract-output-format.md`. The "Derived from:" field on every contract, invariant, and NFR traces back to surface.md, forming the chain: surface behavior -> contract.md -> /build implementation slices.

**Source:** `skills/contract/SKILL.md` (freeze workflow), `skills/contract/reference/contract-output-format.md`

---

## .pyro/pulse-log.md

Append-only log of `/pulse` check-ins. No frontmatter. Body is a sequence of pulse entries.

### Structure

No YAML frontmatter. The file begins with a markdown heading and description, followed by append-only pulse entries.

### Header (written by `pyro-init.sh`)

```markdown
# Pulse Log

Append-only log of /pulse check-ins.
```

### Pulse Entry Format

Each `/pulse` invocation appends one entry:

```markdown
### Pulse -- {YYYY-MM-DD}

**Momentum**: {momentum assessment: rising | steady | declining | stalled | unknown}
**Novelty**: {create_ratio} create-ratio -> {sentiment_trend} trend
**Recommendation**: {recommendation} -- {reasoning}
**Decision**: {decision: push | pivot | shelve | not now}
**Next step**: {first step from chosen path, or "none -- not now"}
```

### Reframe Entry Format

Each `/reframe` invocation appends one entry:

```markdown
### Reframe -- {YYYY-MM-DD}
Lenses applied: {lens1}, {lens2}, {lens3}
Remaining work targeted: {summary}
Moves proposed: ...
Resonated: {which moves}
```

### Rules

- **Append-only**: Never overwrite existing entries. Always append after the last entry.
- **Create if missing**: If the file does not exist, create it with the header before appending.
- **One entry per invocation**: Each completed `/pulse` produces exactly one entry. Each completed `/reframe` produces exactly one reframe entry.

**Source:** `skills/pulse/SKILL.md` (record workflow, lines 356-394), `skills/reframe/SKILL.md`

---

## .pyro/scope.md

The scope analysis output from `/scope`. Records the soul statement, feature categorization, and smallest satisfying version.

### Frontmatter Fields

| Field | Type | Required | Default | Producer | Consumer(s) |
|-------|------|----------|---------|----------|-------------|
| `soul` | String | Yes | N/A | `/scope` (derived from spark.md fascination + contract.md evidence) | `/decide`, `/spark --smaller`, `/pyro` |
| `derived_from` | Array of strings | Yes | `["spark.md", "contract.md"]` | `/scope` | Diagnostic |
| `categorized` | Date (YYYY-MM-DD) | Yes | N/A | `/scope` (date of categorization) | `/decide` |
| `features_total` | Number | Yes | N/A | `/scope` (total features from contract) | `/decide` |
| `soul_critical` | Number | Yes | N/A | `/scope` (features that define the soul) | `/decide` |
| `soul_serving` | Number | Yes | N/A | `/scope` (features that support the soul) | `/decide` |
| `nice_to_have` | Number | Yes | N/A | `/scope` (features that can be cut) | `/decide` |
| `smallest_version` | String | Yes | N/A | `/scope` (one-line description of minimum version) | `/decide`, `/spark --smaller` |
| `hours_saved` | Number | Yes | N/A | `/scope` (estimated hours cut) | `/decide` |
| `hours_remaining` | Number | Yes | N/A | `/scope` (estimated hours for smallest version) | `/decide` |

### Body Sections

| Section | Required | Content Format |
|---------|----------|----------------|
| `## Soul Statement` | Yes | The core curiosity that makes this project worth building |
| `## Feature Categorization` | Yes | Table of features with soul-critical / soul-serving / nice-to-have labels |
| `## The Smallest Satisfying Thing` | Yes | 2-3 smallest version proposals (Essence/Core/Ship) ranked by scope reduction |
| `## Effort Math` | Yes | Hours saved vs remaining, effort comparison |

### Example

```yaml
---
soul: "The fascination with ritual-driven context preservation"
derived_from: ["spark.md", "contract.md"]
categorized: 2026-03-15
features_total: 8
soul_critical: 3
soul_serving: 3
nice_to_have: 2
smallest_version: "Two-question leave ritual with file storage"
hours_saved: 12
hours_remaining: 6
---

## Soul Statement
The fascination with ritual-driven context preservation...

## Feature Categorization
| Feature | Category | Reasoning |
|---------|----------|-----------|
| Two-question prompt | Soul-critical | Defines the ritual |
| File storage | Soul-critical | Preserves context |
| Return command | Soul-critical | Completes the loop |
| History browsing | Soul-serving | Supports reflection |
| Export | Nice-to-have | Not core to ritual |

## The Smallest Satisfying Thing
### Essence (3 features, ~6 hours)
Two-question leave ritual with file storage and return...

## Effort Math
Original scope: ~18 hours (8 features)
Smallest version: ~6 hours (3 features)
Hours saved: 12
```

Producer: /scope. Consumer: /decide, /spark --smaller.

**Source:** `skills/scope/SKILL.md`

---

## .pyro/decide.md

The milestone plan output from `/decide`. Expands a push/pivot/shelve decision into concrete milestones with re-evaluation points.

### Frontmatter Fields

| Field | Type | Required | Default | Producer | Consumer(s) |
|-------|------|----------|---------|----------|-------------|
| `path` | String: `push` \| `pivot` \| `shelve` | Yes | N/A | `/decide` | Developer reference |
| `decided` | Date (YYYY-MM-DD) | Yes | N/A | `/decide` (date of decision) | Developer reference |
| `milestones` | Number | Yes | N/A | `/decide` (count of milestones) | Developer reference |
| `source_pulse` | String | Yes | N/A | `/decide` (date of the pulse entry that triggered decision) | Traceability |
| `soul_aware` | Boolean | Yes | N/A | `/decide` (true if scope.md was available) | Diagnostic |

### Body Sections

| Section | Required | Content Format |
|---------|----------|----------------|
| `## Path: {Push\|Pivot\|Shelve}` | Yes | Decision summary with reasoning |
| `## Milestones` | Yes | Numbered milestones with deliverables and re-evaluation points |

### Example

```yaml
---
path: "push"
decided: 2026-03-15
milestones: 3
source_pulse: "2026-03-14"
soul_aware: true
---

## Path: Push
Pushing forward with scoped version. The soul of this project is ritual-driven context preservation...

## Milestones
### Milestone 1: Core Ritual
- Deliverable: Two-question prompt + file storage
- Effort: ~2 hours
- Re-evaluate: Does the ritual feel right?

### Milestone 2: Return Loop
- Deliverable: `leave --return` reads last note
- Effort: ~2 hours
- Re-evaluate: Is the return moment satisfying?

### Milestone 3: Ship
- Deliverable: README, npm publish
- Effort: ~2 hours
- Re-evaluate: Done?
```

Producer: /decide. Consumer: developer reference.

**Source:** `skills/decide/SKILL.md`

---

## ~/.pyro/fascination-index.md

Cross-project fascination registry. Written by `/autopsy`, read by `/spark`. Lives in the global `~/.pyro/` directory (not project-local).

### Frontmatter Fields

The frontmatter contains a single `entries` array. Each entry is an object:

| Field | Type | Required | Default | Producer | Consumer(s) |
|-------|------|----------|---------|----------|-------------|
| `theme` | String (kebab-case) | Yes | N/A | `/autopsy` (extract_fascinations) | `/spark` |
| `description` | String | Yes | N/A | `/autopsy` (one sentence description) | `/spark` |
| `intensity` | String: `high` \| `medium` \| `low` | Yes | N/A | `/autopsy` (assigned via 5-lens algorithm) | `/spark` |
| `last_seen` | Date (YYYY-MM-DD) | Yes | N/A | `/autopsy` (date of extraction) | `/spark` |
| `projects` | Array of strings | Yes | N/A | `/autopsy` (project names where theme appeared) | `/spark` |
| `last_rejected` | Date (YYYY-MM-DD) | No | `""` (empty) | `/spark` (rejection signal tracking) | `/fascination` (display) |
| `rejection_count` | Number | No | `0` | `/spark` (incremented on rejection) | `/fascination` (display) |
| `resonance_count` | Number | No | `0` | `/spark` (incremented on resonance) | `/fascination` (display) |
| `intensity_numeric` | Number (1-5) | No | Derived from `intensity`: low=1, medium=3, high=5 | `/spark` (incremented on resonance, cap 5) | `/fascination` (display), `/spark` (resonance updates) |

### Body Sections

| Section | Required | Content Format |
|---------|----------|----------------|
| `# Fascination Index` | Yes | Freeform description text |

### Example (initial state from `pyro-init.sh`)

```yaml
---
entries: []
---

# Fascination Index

Cross-project fascination registry. Updated by /autopsy, read by /spark.
```

### Example (after one autopsy)

```yaml
---
entries:
  - theme: "ritual-driven-ux"
    description: "Designing interactions that feel like meaningful rituals rather than mechanical steps"
    intensity: high
    last_seen: 2026-03-12
    projects: ["leave-cli"]
    # Optional fields (added by /spark rejection tracking):
    last_rejected: ""
    rejection_count: 0
    resonance_count: 0
    intensity_numeric: 5
  - theme: "context-preservation"
    description: "Techniques for maintaining mental context across task switches"
    intensity: medium
    last_seen: 2026-03-12
    projects: ["leave-cli"]
---

# Fascination Index

Cross-project fascination registry. Updated by /autopsy, read by /spark.
```

**Source:** `pyro-init.sh` (initial creation, lines 47-58), `skills/autopsy/SKILL.md` (update logic, lines 359-407), `skills/spark/SKILL.md` (rejection/resonance signal tracking)

---

## ~/.pyro/project-registry.yaml

Global project registry tracking all Pyro-initialized projects. Written by `pyro-init.sh`, updated by `/autopsy`.

### Structure

A single YAML file with a `projects` array. Each entry:

| Field | Type | Required | Default | Producer | Consumer(s) |
|-------|------|----------|---------|----------|-------------|
| `path` | String (absolute path) | Yes | Current working directory | `pyro-init.sh` (register_project) | `/pyro`, `/autopsy` |
| `name` | String | Yes | Directory name or argument | `pyro-init.sh` | `/pyro`, `/autopsy` |
| `status` | String: `active` \| `shelved` \| `composted` | Yes | `active` | `pyro-init.sh`; updated by `/autopsy` | `/pyro` |
| `phase` | Number (0-6) | Yes | `0` | `pyro-init.sh`; updated by `/spark`, `/autopsy` | `/pyro` |
| `last_activity` | Date (YYYY-MM-DD) | Yes | Today's date | `pyro-init.sh`; updated by `/spark`, `/autopsy` | `/pyro`, `/pulse` |
| `spark_date` | String (date or empty) | Yes | `""` (empty) | `/spark` (on crystallize) | `/pyro` |
| `fascinations` | Array | Yes | `[]` (empty) | Not currently populated by any skill | `/pyro` |
| `shelved_date` | Date (YYYY-MM-DD) | Optional | Not present | `/autopsy` (on archive) | Diagnostic |
| `autopsy_date` | Date (YYYY-MM-DD) | Optional | Not present | `/autopsy` (on archive) | Diagnostic |

### Example (initial state)

```yaml
projects: []
```

### Example (after registration)

```yaml
projects:
  - path: /home/dev/projects/leave-cli
    name: leave-cli
    status: active
    phase: 0
    last_activity: 2026-03-13
    spark_date: ""
    fascinations: []
```

### Example (after autopsy)

```yaml
projects:
  - path: /home/dev/projects/leave-cli
    name: leave-cli
    status: shelved
    phase: 6
    last_activity: 2026-03-13
    spark_date: "2026-03-10"
    fascinations: []
    shelved_date: 2026-03-13
    autopsy_date: 2026-03-13
```

**Source:** `pyro-init.sh` (registration logic, lines 79-110), `skills/autopsy/SKILL.md` (update logic, lines 410-433)

---

## ~/.pyro/config.yaml (Global)

Global Pyro Kit configuration. Created by `pyro-init.sh`.

### Fields

| Field | Type | Required | Default | Producer | Consumer(s) |
|-------|------|----------|---------|----------|-------------|
| `dormancy_threshold_days` | Number | Yes | `5` | `pyro-init.sh` | `/pyro` (route dormancy check) |
| `pulse_auto_suggest` | Boolean | Yes | `true` | `pyro-init.sh` | `/pyro` (session hook suggestion) |
| `fascination_intensity_decay` | Boolean | Yes | `true` | `pyro-init.sh` | Future: fascination index maintenance |
| `default_start_phase` | Number | Yes | `0` | `pyro-init.sh` | Future: non-zero start phase |

### Example

```yaml
dormancy_threshold_days: 5
pulse_auto_suggest: true
fascination_intensity_decay: true
default_start_phase: 0
```

**Source:** `pyro-init.sh` (lines 28-34)

---

## .pyro/config.yaml (Project-local)

Project-local configuration overrides. Created by `pyro-init.sh`. Empty by default.

### Structure

A YAML file for local overrides of global config values. Any field from `~/.pyro/config.yaml` can be overridden here.

### Example (as created by `pyro-init.sh`)

```yaml
# Project-local Pyro config overrides
```

**Source:** `pyro-init.sh` (lines 150-153 repair path, lines 213-215 init path)

---

## .pyro/harvest.md

The harvest manifest written by `/revive` (organ harvest option). Documents extractable artifacts from an abandoned project with their source paths and extraction instructions.

### Frontmatter Fields

| Field | Type | Required | Default | Producer | Consumer(s) |
|-------|------|----------|---------|----------|-------------|
| `source_project` | String | Yes | N/A | `/revive` (organ harvest) | Developer reference |
| `harvested` | Date (YYYY-MM-DD) | Yes | N/A | `/revive` (date of harvest) | Developer reference |
| `source_path` | String (absolute path) | Yes | N/A | `/revive` (original repo path) | Developer reference |
| `artifacts_count` | Number | Yes | N/A | `/revive` (count of extractable artifacts) | Developer reference |

### Body Sections

| Section | Required | Content Format |
|---------|----------|----------------|
| `# Harvest Manifest -- {project-name}` | Yes | Title with project name |
| `## Artifacts` | Yes | Numbered artifact entries |

### Artifact Entry Format

Each artifact is a numbered subsection:

```markdown
### 1. {Artifact Name}
**Source:** `{file path in original repo}`
**What it does:** {description}
**How to extract:** {specific instructions}
**Dependencies:** {what else it needs}
```

### Example

```yaml
---
source_project: "leave-cli"
harvested: 2026-03-15
source_path: "/home/dev/projects/leave-cli"
artifacts_count: 3
---

# Harvest Manifest -- leave-cli

Extracted from leave-cli on 2026-03-15. Each artifact includes its
original location and extraction instructions.

## Artifacts

### 1. Two-Question Prompt Engine
**Source:** `src/prompt.ts`
**What it does:** Minimal sequential prompt with empty-input tolerance
**How to extract:** Copy src/prompt.ts. Replace chalk with your preferred color lib.
**Dependencies:** Node.js readline module (stdlib)

### 2. Leave Note Storage
**Source:** `src/storage.ts`
**What it does:** Append-only markdown file storage with date-stamped entries
**How to extract:** Copy src/storage.ts. Update the default directory path.
**Dependencies:** Node.js fs module (stdlib)
```

Producer: /revive (organ harvest option). Consumer: developer reference.

**Source:** `skills/revive/SKILL.md` (execute workflow, organ harvest branch)

---

## Additional Directories

These directories are created by `pyro-init.sh` but do not have file schemas:

| Directory | Scope | Purpose | Producer |
|-----------|-------|---------|----------|
| `~/.pyro/autopsies/` | Global | Archived autopsy reports (one `.md` per project) | `/autopsy` |
| `~/.pyro/patterns/` | Global | Cross-project pattern files (future) | `/patterns` (planned) |
| `.pyro/session-notes/` | Project | Session note files (future) | Session hook (planned) |

---

## Known Inconsistencies

None identified. The schemas documented above accurately reflect what `pyro-init.sh` writes and what the MVP skills (`/spark`, `/pulse`, `/autopsy`, `/pyro`) expect. The `fascinations` field in `project-registry.yaml` is written as an empty array by `pyro-init.sh` but is never populated by any current skill -- it exists as a placeholder for future use.
