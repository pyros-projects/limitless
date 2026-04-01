# Final Ideation Phase -- Novel Ideas Not Previously Captured

**Status:** Proposed
**Priority:** High
**Source:** Final external research pass (creative domains, AI agent frontier, failure-mode inversion, portfolio patterns)

---

## Goal

Capture genuinely new ideas that were not already in the existing Pyro Kit backlog and are not just minor variants of current skills.

Each concept below includes:
- Why it is novel for AI coding tools
- How it maps to Pyro Kit
- A minimal MVP shape

## 1) Idea View <-> Ship View Toggle

**Source pattern:** Ableton Session View vs Arrangement View.

**Novelty:** Most coding assistants force a single mode (task execution). This introduces a first-class mode switch between non-linear exploration and linear shipping.

**Pyro Kit adaptation:**
- **Idea View:** fragments, alternatives, riffs, no strict sequence
- **Ship View:** ordered tasks, explicit dependencies, completion pressure
- One command to "record" exploration artifacts into ship-ready sequence

**MVP:** `/pyro mode idea|ship` + a converter that turns selected exploration fragments into a scoped build plan.

## 2) Project Pillars as Hard Decision Filter

**Source pattern:** Game design pillars.

**Novelty:** Pillars are stronger than preferences; they are non-negotiable decision constraints that prevent drift.

**Pyro Kit adaptation:**
- Define 3-5 project pillars right after spark (e.g., "offline-first", "keyboard-first", "zero setup")
- Every major suggestion references which pillar it serves
- Suggestions violating pillars are flagged by default

**MVP:** `pillars:` in `.pyro/state.md` + skill-side check: "This option conflicts with pillar #2."

## 3) Commitment Threshold (Point of No Return)

**Source pattern:** Screenwriting "Thrusted Into 2" beat.

**Novelty:** Makes irreversibility explicit. Most tools treat all project stages as equally reversible.

**Pyro Kit adaptation:**
- During /contract, define the project's first irreversible milestone
- Before threshold: encourage pivots and wild exploration
- After threshold: prioritize stability and compatibility

**MVP:** `commitment_threshold:` in `contract.md` + /pulse awareness of pre/post-threshold behavior.

## 4) Negative Results Notebook

**Source pattern:** Scientific publication of negative results.

**Novelty:** Failed attempts become primary assets, not post-mortem leftovers.

**Pyro Kit adaptation:**
- Structured failed-attempt entries: hypothesis, attempt, failure signal, wrong assumption, reusable lesson
- Queried by /spark and /explore to avoid repeat dead-ends

**MVP:** `.pyro/negative-results.md` + append hooks from /autopsy and /pulse.

## 5) Creative Friction Mode (Deliberate Constraint)

**Source pattern:** Huevember-like constraint creativity + anti-optimization research gap.

**Novelty:** Most tools remove friction; this intentionally introduces controlled constraints to increase originality.

**Pyro Kit adaptation:**
- Optional constrained rounds: "no external deps", "single file", "CLI only", "no abstraction"
- Forces unusual solutions and reveals hidden assumptions

**MVP:** `/explore --friction "no external deps"` and `/surface --friction "single-file"`.

## 6) Trust Calibration Layer

**Source pattern:** AI trust research (high usage, low trust) and provenance-driven systems.

**Novelty:** Not just "suggestions" but calibrated suggestions with explicit trust metadata.

**Pyro Kit adaptation:**
- Each major recommendation includes confidence + provenance + verification hints
- Flag "almost-right risk" suggestions as requiring manual pressure-test

**MVP:** suggestion footer standard:
- `Confidence: high|medium|low`
- `Basis: decisions|scout|patterns`
- `Verify with: one concrete test`

## 7) Energy Budget Router (Portfolio-Level WIP)

**Source pattern:** Portfolio kanban + WIP limits.

**Novelty:** Moves from per-project intelligence to cross-project attention allocation.

**Pyro Kit adaptation:**
- Hard cap active projects (e.g., max 2 build-phase projects)
- Route attention based on momentum and decay signals
- Prevents silent dilution across 10 half-active repos

**MVP:** global file `~/.pyro/portfolio.md` with states: active, parked, dormant, composted + WIP rules.

## 8) Parked, Not Dead (Intentional Hibernation)

**Source pattern:** Parking lot / keep-kill-pause systems.

**Novelty:** Introduces a structured middle state between active and abandoned.

**Pyro Kit adaptation:**
- Explicit park operation with review date, revival trigger, and extraction notes
- Parked projects feed spark context without emotional "failure" framing

**MVP:** `/pause-project` flow writing to portfolio registry and scheduling future /pulse check-in.

## 9) Project Genetics (Donate Organs)

**Source pattern:** Parent-child project structures and inheritance patterns.

**Novelty:** Treats old projects as donors of modules, decisions, and patterns for new descendants.

**Pyro Kit adaptation:**
- New project can declare parent project(s)
- Inherit selected artifacts: constraints, decisions, patterns, unresolved questions
- Track lineage and divergence

**MVP:** `parent_projects:` in state + `/spark inherit from <project>`.

## 10) Pattern-Based Affective Detection (Beyond Sentiment)

**Source pattern:** Affective agents + observed gap in behavior-based emotional inference.

**Novelty:** Detects state from interaction patterns, not just explicit text sentiment.

**Pyro Kit adaptation:**
- Infer likely modes: flow, friction, boredom, avoidance from behavior markers
- Markers: iteration latency, context switching, repeated rewrites, aborted sessions
- /pulse adapts tone and intervention style to inferred mode

**MVP:** lightweight "energy signals" block in `.pyro/state.md` updated by hooks.

---

## Highest-Leverage Bundle (If you only build 3)

1. **Project Pillars** -- immediate anti-drift effect with minimal implementation cost
2. **Negative Results Notebook** -- compounds learning from every failed attempt
3. **Idea View <-> Ship View Toggle** -- gives a first-class answer to exploration vs execution tension

## Why these ideas matter

Your current roadmap is already strong on lifecycle mechanics. These ideas add a different layer: they improve creative quality and longevity by shaping how attention, trust, reversibility, and learning work over time.

They are less about "better prompts" and more about **better creative operating systems**.
