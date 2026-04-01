---
title: "Pyro Kit — Surface-First Development Framework for the Full Project Lifecycle"
status: draft
version: "1.0"
---

# Product Requirements Document

## Validation Checklist

### CRITICAL GATES (Must Pass)

- [x] All required sections are complete
- [x] No [NEEDS CLARIFICATION] markers remain
- [x] Problem statement is specific and measurable
- [x] Every feature has testable acceptance criteria (Gherkin format)
- [x] No contradictions between sections

### QUALITY CHECKS (Should Pass)

- [x] Problem is validated by evidence (not assumptions)
- [x] Context -> Problem -> Solution flow makes sense
- [x] Every persona has at least one user journey
- [x] All MoSCoW categories addressed (Must/Should/Could/Won't)
- [x] Every metric has corresponding tracking events
- [x] No feature redundancy (check for duplicates)
- [x] No technical implementation details included
- [x] A new team member could understand this PRD

---

## Scope

| Version | What's Included | Status |
|---------|----------------|--------|
| **v0.1.0 (MVP)** | /pyro, /spark, /pulse, /autopsy + infrastructure (hooks, scripts, state schemas) | **Shipped** |
| **v1.0.0 (Full Vision)** | All 27 skills across 7 lifecycle phases | Roadmap |

Features in this PRD describe the **full v1.0.0 vision**. MVP-scope items are tagged with `[MVP]` where applicable.

## Product Overview

### Vision

Pyro Kit is a framework that takes a developer from a vague feeling ("something about X bugs me") to a shipped project, using a single interaction pattern: the agent proposes concrete things, the developer evaluates and steers. The developer never has to generate ideas, write specs, or answer abstract questions — they only need to know what they like.

### Problem Statement

Solo creative developers with strong creative instincts frequently abandon projects at 60-70% completion. Evidence from the target user's GitHub shows 20+ repositories following this pattern across projects like z-Explorer (prompt DSL started, roadmap abandoned), clawde/hangar (IDE concepts, pivoted), mira-OSS (elegant concept, stalled), and wishful.

The root causes, validated by psychology research (Tiimo ADHD research, Scott Belsky's "The Messy Middle", Ira Glass's taste-ability gap):
1. **Novelty depletion** — dopamine surge from new problems is gone by 60%; remaining work is error handling, edge cases, polish
2. **Taste-ability gap** — the project is complete enough to evaluate but not complete enough to be good
3. **Invisible progress** — same effort that produced visible results early now produces invisible infrastructure
4. **No explicit decision** — projects aren't abandoned by choice; they drift into silence
5. **Premature coding** — jumping to implementation before the idea is fully explored means hard design decisions surface at 60%, not at the start

The cost: thousands of hours of creative work across 20+ projects producing no shipped outcomes and no accumulated learning.

### Value Proposition

No existing tool addresses the full lifecycle from pre-idea to post-abandonment:
- **Brainstorming tools** (Superpowers, robertguss) assume you already have an idea and interrogate you about it
- **Spec-driven frameworks** (BMAD, GSD, Spec Kit) assume you know what to build and help you build it well
- **Anti-drift tools** (Compound Engineering) compound learning within a project but not across projects

Pyro Kit fills the three gaps no tool covers:
1. **Pre-idea excavation** — going from a feeling to an idea without requiring the developer to articulate it
2. **Messy middle intervention** — detecting and addressing momentum loss during implementation
3. **Abandonment as input** — extracting value from dead projects and feeding it into future ideas

The unique interaction model (propose-react-iterate from Surface-First Development) means the developer's only required input is taste — evaluating concrete proposals rather than generating abstract descriptions.

## User Personas

### Primary Persona: The Solo Creative Developer

- **Demographics:** Individual developer, strong technical skills, works alone on personal/side projects. Not motivated by market success or revenue — motivated by pushing ideas to their full potential.
- **Goals:** Ship creative projects that fully realize their vision. Stop the cycle of starting exciting things and abandoning them. Accumulate creative momentum across projects instead of starting from zero each time.
- **Pain Points:**
  - Jumps to coding before thinking ideas through — the exciting part is starting, not planning
  - Hits hard design decisions at 60-70% that should have been resolved earlier
  - Hates traditional brainstorming ("imagine X, then Y") — finds it effortful and unproductive
  - Has excellent taste and judgment but struggles to articulate ideas from scratch
  - 20+ abandoned repos representing thousands of hours with no shipped outcomes
  - Each new project starts from zero — no learning carries forward from past attempts

### Secondary Personas

None for v1. Pyro Kit is personal tooling for one person's brain. Team support is explicitly out of scope.

## User Journey Maps

### Primary User Journey: From Vague Feeling to Shipped Project

1. **Spark** (Phase 0): Developer has a vague feeling — an annoyance, a fascination, something that caught their attention. They invoke `/spark`. The agent proposes 3-5 concrete "idea thumbnails" (one-paragraph scenarios). Developer points at one: "that one." Agent iterates. An idea crystallizes.

2. **Explore** (Phase 1): The crystallized idea could go several directions. The agent proposes 3-4 concrete design directions, each as a tangible scenario. Developer evaluates, steers, narrows. One direction is locked.

3. **Surface** (Phase 2): The agent generates a working prototype (click dummy, CLI simulation, API consumer code). Developer interacts with it, critiques behavior ("when I do X, I expect Y"). Agent iterates until the surface converges — all critical flows feel right.

4. **Contract** (Phase 3): The agent extracts contracts from the converged surface — API shapes, domain rules, non-functional targets. Developer confirms: "yes, that captures it." Contracts freeze.

5. **Build** (Phase 4): Vertical slices, one at a time. Each slice makes one surface flow real end-to-end. Progressive hardening replaces mocks with real implementations.

6. **Momentum** (Phase 5): Midway through building, commit frequency drops. The agent auto-suggests `/pulse`. It shows git metrics, names the novelty depletion, quotes the original spark, and proposes three concrete paths: push (with specific scope cut), pivot (different form factor), or shelve (with value extraction). Developer picks one.

7. **Lifecycle** (Phase 6): Project ships — or gets shelved with a full autopsy that extracts reusable code, patterns, and fascinations into a persistent index. The fascination index feeds the next `/spark` session. Nothing is wasted. The cycle continues.

### Secondary User Journey: Reviving an Abandoned Project

1. Developer points `/revive` at an old repo
2. Agent reads code, commits, README — reconstructs what the project was trying to be, how far it got, and what caused abandonment
3. Agent proposes four options: full revival (with plan), soul transplant (fresh implementation preserving the core idea), organ harvest (extract reusable parts), or let it rest (with autopsy)
4. Developer evaluates and picks one
5. If revived: re-enters the main journey at the appropriate phase

### Tertiary User Journey: Cross-Project Pattern Discovery

1. After several projects (active, completed, and shelved), developer invokes `/patterns`
2. Agent analyzes the fascination index, autopsy reports, and project history
3. Agent proposes insights: recurring themes, completion correlations (which project types ship vs. die), the developer's deepest fascination
4. Developer reacts: "yeah, that's what I keep building toward"
5. Insight feeds the next `/spark` — future projects are more aligned with deep fascinations

## Feature Requirements

### Must Have Features

#### Feature 1: Propose-React-Iterate Core Interaction `[MVP]`

- **User Story:** As a solo developer, I want the agent to propose concrete things at every phase so that I only need to evaluate and steer, never generate from scratch.
- **Acceptance Criteria:**
  - [ ] Given the developer invokes any Pyro Kit skill, When the skill activates, Then it produces a concrete proposal (not a question) as its first output
  - [ ] Given the developer provides feedback on a proposal ("more like this", "not that"), When the agent receives the feedback, Then it produces a revised proposal incorporating the feedback within the same session
  - [ ] Given the developer says "yes" or equivalent approval, When the skill receives approval, Then it persists the converged output and suggests the next appropriate skill
  - [ ] Given the developer has not articulated a clear idea, When any skill runs, Then it never asks open-ended creative questions like "what excites you?" or "imagine if..." — it proposes options instead

#### Feature 2: Phase 0 — Ignition (Pre-Idea to Idea) `[MVP: /spark only]`

- **User Story:** As a developer with a vague feeling or fascination, I want to discover what I actually want to build without having to articulate it myself.
- **Acceptance Criteria:**
  - [ ] Given the developer invokes `/spark` with a vague input (a feeling, annoyance, or topic), When the skill runs, Then it produces 3-5 "idea thumbnails" — one-paragraph concrete scenarios of what a tool/project would look like in use
  - [ ] Given the developer selects a thumbnail ("that one"), When they provide the selection, Then the agent expands it into a more detailed concept and proposes variations
  - [ ] Given the developer invokes `/remix`, When the skill runs, Then it reframes the current idea through 4-6 non-developer creative domain lenses (game design, music, screenwriting, architecture, improv, cooking) with a concrete actionable move for each lens
  - [ ] Given the developer invokes `/thumbnail`, When the skill runs, Then it generates a quick, disposable, detailed sketch of one idea direction — explicitly marked as throwaway
  - [ ] Given the developer invokes `/fascination`, When the skill runs, Then it displays the current fascination index with themes, connections between past projects, and what patterns suggest

#### Feature 3: Phase 1 — Exploration (Idea to Developed Idea) `[Roadmap]`

- **User Story:** As a developer with a crystallized idea, I want to explore the design space before committing to one direction so I don't anchor on the first approach.
- **Acceptance Criteria:**
  - [ ] Given the developer invokes `/explore` with a crystallized idea, When the skill runs, Then it proposes 3-4 fundamentally different design directions, each as a concrete scenario (not abstract options)
  - [ ] Given the developer invokes `/sketch` for a direction, When the skill runs, Then it generates a rough-but-tangible representation (wireframe description, CLI session transcript, or API usage example)
  - [ ] Given the developer invokes `/contrast` with two directions, When the skill runs, Then it produces a side-by-side comparison with explicit tradeoffs for each
  - [ ] Given the developer invokes `/narrow`, When the skill runs, Then it proposes a recommended direction with reasoning based on the developer's reactions, which the developer can accept or redirect

#### Feature 4: Phase 2 — Surface (SFD Proper) `[Roadmap]`

- **User Story:** As a developer with a locked direction, I want a working prototype I can interact with and critique so the design converges through experience, not speculation.
- **Acceptance Criteria:**
  - [ ] Given the developer invokes `/surface`, When the skill runs, Then it identifies the surface type (GUI, CLI, API, pipeline, agent) and generates a working interactive prototype with mock data
  - [ ] Given the developer provides behavioral critique ("when I do X, I expect Y"), When `/iterate` processes the critique, Then it produces an updated prototype incorporating the feedback plus proactive edge case exploration
  - [ ] Given the developer invokes `/converge`, When the skill runs, Then it walks through all critical flows asking "anything still feel wrong?" and produces an explicit convergence declaration
  - [ ] Given the surface is converged, When `/state-map` runs, Then it produces a Surface State Inventory classifying every observable state as in-scope, deferred, or N/A

#### Feature 5: Phase 3 — Contract (Surface to Frozen Specs) `[Roadmap]`

- **User Story:** As a developer with a converged surface, I want contracts derived from what I approved so that specs reflect validated behavior, not speculation.
- **Acceptance Criteria:**
  - [ ] Given a converged surface exists, When `/derive` runs, Then it extracts API contracts (endpoints, methods, payloads, error shapes) from the surface behavior
  - [ ] Given a converged surface exists, When `/invariants` runs, Then it proposes domain rules that must hold for the surface behavior to remain valid
  - [ ] Given a converged surface exists, When `/nfr` runs, Then it proposes non-functional requirement targets (latency, availability, throughput) with measurable numbers
  - [ ] Given contracts are proposed, When the developer approves and `/freeze` runs, Then contracts are versioned and locked, producing a frozen contract bundle

#### Feature 6: Phase 4 — Build (Contracts to Working Software) `[Roadmap]`

- **User Story:** As a developer with frozen contracts, I want to build one vertical slice at a time so the surface stays working throughout implementation.
- **Acceptance Criteria:**
  - [ ] Given frozen contracts exist, When `/slice` runs, Then it proposes a prioritized list of vertical slices, highest-value first, each making one surface flow real end-to-end
  - [ ] Given a slice is selected, When `/implement` runs, Then it produces working code for that slice from surface interaction through logic to persistence
  - [ ] Given a slice is implemented, When `/harden` runs, Then it proposes the next hardening step (mock to real) with before/after surface verification
  - [ ] Given hardening is complete, When `/verify` runs, Then it runs acceptance tests against the converged surface baseline and produces release readiness evidence

#### Feature 7: Phase 5 — Momentum (Anti-Abandonment Intervention) `[MVP: /pulse only]`

- **User Story:** As a developer losing steam on a project, I want the framework to detect this and propose concrete options so I make an explicit decision instead of silently drifting away.
- **Acceptance Criteria:**
  - [ ] Given the developer invokes `/pulse` (or it is auto-suggested), When the skill runs, Then it displays: git activity metrics (commit frequency trend, gap analysis), progress visualization (features done, TODOs, estimated remaining effort), a novelty depletion signal (commit message analysis showing creation-to-maintenance transition), the original spark quoted verbatim, and three concrete paths (push with scope cut, pivot with alternative form, shelve with /autopsy)
  - [ ] Given the developer invokes `/reframe`, When the skill runs, Then it proposes 3-4 creative domain lenses applied to the specific remaining work, each with a concrete actionable move (not abstract inspiration)
  - [ ] Given the developer invokes `/scope`, When the skill runs, Then it identifies the project's "soul statement" (the one fascination that makes it worth building), categorizes all features as soul-critical / soul-serving / nice-to-have, proposes a specific cut, and shows "the smallest thing that would satisfy your curiosity"
  - [ ] Given the developer invokes `/decide`, When the skill runs, Then it makes a specific recommendation (push, pivot, or shelve) based on evidence, with pre-built plans for all three options including concrete first steps

#### Feature 8: Phase 6 — Lifecycle (Completion or Composting) `[MVP: /autopsy only]`

- **User Story:** As a developer finishing or shelving a project, I want the outcome to feed forward so nothing is wasted and every project makes the next one better.
- **Acceptance Criteria:**
  - [ ] Given a project is ready to ship, When `/ship` runs, Then it proposes a release checklist with gaps highlighted and concrete steps to close them
  - [ ] Given a project is being shelved, When `/autopsy` runs, Then it produces a structured report: what the soul was, what worked, what killed it (from a taxonomy: novelty depletion, scope creep, taste gap, technical wall, new shiny thing), reusable code/patterns, the underlying fascination, and an automatic fascination index update
  - [ ] Given the developer points `/revive` at an abandoned repo, When the skill runs, Then it reads code/commits/docs, reconstructs the project's intent and state, and proposes four options: full revival, soul transplant, organ harvest, or let it rest
  - [ ] Given the developer invokes `/patterns`, When the skill runs, Then it analyzes the fascination index and project history, proposing: recurring themes (with frequency), abandonment patterns (average completion %, common causes, danger signals), what project types succeed vs. fail, and the developer's deepest fascination

#### Feature 9: Fascination Index (Cross-Project Memory) `[MVP: write + read pipeline]`

- **User Story:** As a developer with many past projects, I want a persistent record of what fascinates me so patterns become visible and future projects align with deep interests.
- **Acceptance Criteria:**
  - [ ] Given `/autopsy` completes, When the report is generated, Then the fascination index is automatically updated with extracted themes, connections to past projects, and fascination intensity
  - [ ] Given `/spark` is invoked, When the skill starts, Then it reads the fascination index and uses existing themes to inform idea generation ("you've been fascinated by X before — does this connect?")
  - [ ] Given `/fascination` is invoked, When the skill runs, Then it displays all indexed fascinations with status (active/dormant), intensity, related projects, and cross-fascination connections
  - [ ] Given `/patterns` is invoked, When the skill runs, Then it analyzes the fascination index for clusters, completion correlations, and fascination drift over time

#### Feature 10: Gate System (Explicit Phase Transitions) `[MVP: soft gating]`

- **User Story:** As a developer, I want explicit checkpoints between phases so I consciously advance rather than accidentally skipping important steps.
- **Acceptance Criteria:**
  - [ ] Given the developer completes Phase 0 work, When Gate 0 (Idea Crystallized) is reached, Then the agent verifies: a one-sentence intent exists, at least one idea thumbnail was selected, and the developer confirms readiness to proceed
  - [ ] Given the developer completes Phase 1 work, When Gate 1 (Direction Locked) is reached, Then the agent verifies: one direction is chosen, rejected alternatives are logged, and key constraints are identified
  - [ ] Given the developer completes Phase 2 work, When Gate 2 (Surface Converged) is reached, Then the agent verifies per SFD Gate 1: critical flows demonstrated, Surface State Inventory completed, edge cases explored, decision log current
  - [ ] Given the developer completes Phase 3 work, When Gate 3 (Contracts Frozen) is reached, Then the agent verifies: API contracts versioned, invariants documented, NFRs with targets, architecture reviewed
  - [ ] Given implementation is underway, When Gate 6 (Momentum Check) triggers, Then it fires based on signals (commit frequency decline, stale branches, new repos created) regardless of current phase, requiring an explicit push/pivot/shelve decision
  - [ ] Given a project reaches resolution, When Gate 7 (Lifecycle Complete) is reached, Then the project has exactly one terminal state: shipped, shelved (with autopsy), or composted (value in pattern library) — no undead projects

#### Feature 11: Orchestrator Skill (`/pyro`) `[MVP]`

- **User Story:** As a developer, I want a single entry point that reads my current state and suggests what to do next so I don't have to remember which of 25+ skills to invoke.
- **Acceptance Criteria:**
  - [ ] Given the developer invokes `/pyro` in a project with existing state, When the skill runs, Then it reads project state and recommends the most appropriate next skill with reasoning
  - [ ] Given the developer invokes `/pyro` in a project with no state, When the skill runs, Then it initializes project tracking and suggests starting with `/spark` or `/surface` depending on whether an idea exists
  - [ ] Given the developer invokes `/pyro` and git analysis shows declining momentum, When the skill runs, Then it prioritizes suggesting `/pulse` over forward-phase skills
  - [ ] Given the developer invokes `/pyro list`, When the skill runs, Then it displays all available skills organized by phase with the current phase highlighted

### Should Have Features

#### Auto-Suggestion via Session Hook

- **User Story:** As a developer who forgets to check in, I want the framework to automatically surface relevant context when I start a session.
- **Acceptance Criteria:**
  - [ ] Given a project has been inactive for more than 5 days, When a new session starts in that project directory, Then the framework suggests running `/pulse` for a momentum check
  - [ ] Given a project has Pyro Kit state, When a session starts, Then the framework injects current phase and last activity as context

#### Dormancy Detection Across Projects

- **User Story:** As a developer with multiple active projects, I want to be notified about dormant projects so nothing silently dies.
- **Acceptance Criteria:**
  - [ ] Given the project registry tracks multiple projects, When a session starts, Then projects inactive beyond the configured threshold are surfaced with a suggestion to run `/pulse` or `/autopsy`

### Could Have Features

#### Visual Fascination Map

A visual representation (Mermaid diagram or similar) of the fascination index showing theme clusters, project connections, and intensity over time.

#### Scope Reduction Templates

Pre-built scope cut patterns for common project types (CLI tool, web app, library, API) that `/scope` can propose as starting points.

#### Creative Domain Lens Library

An extensible library of creative domain lenses for `/remix` and `/reframe`, with domain-specific vocabulary and analogies (game design mechanics, music composition structures, screenwriting beats, architectural patterns, culinary techniques).

### Won't Have (This Phase)

- **Team collaboration features** — Pyro Kit is personal tooling for one developer's brain
- **Market research or competitive analysis** — the developer doesn't care about market fit
- **Project management features** — no sprints, no story points, no velocity tracking
- **IDE integration** — works in Claude Code terminal only for v1
- **Database or external service dependencies** — all state is local files
- **Automated code generation** — Phase 4 skills suggest what to build, but code generation uses existing tools (Claude Code's native capabilities)

## Detailed Feature Specifications

### Feature: `/pulse` — Momentum Dashboard (Most Complex Feature)

**Description:** The momentum dashboard is the centerpiece of the anti-abandonment system. It combines automated git analysis with psychological insight to detect momentum loss and propose concrete options. It operates on the principle that the developer only needs to evaluate — every element is computed or proposed, never asked.

**User Flow:**
1. Developer invokes `/pulse` (or it is auto-suggested by the session hook)
2. System analyzes git history: commit frequency trend, message sentiment shift (feature vs. fix), branch staleness, TODO accumulation, new repo detection
3. System retrieves the original spark statement from `.pyro/spark.md`
4. System computes progress estimates from code structure and TODO counts
5. System generates a dashboard showing: activity metrics with trend, progress visualization, novelty depletion signal (named explicitly), the original spark quoted verbatim, and three concrete paths forward
6. Developer evaluates the three paths and selects one (or articulates what's actually hard)
7. System records the decision in the pulse log and updates project state

**Business Rules:**
- Rule 1: The "novelty depletion signal" is computed by analyzing commit message patterns — a shift from "Add/Create/Implement" to "Fix/Update/Refactor" indicates the creation-to-maintenance transition
- Rule 2: The "new shiny thing detector" checks whether new repositories were created during this project's active period
- Rule 3: The original spark is ALWAYS quoted verbatim, never paraphrased — it serves as an emotional anchor
- Rule 4: All three options (push/pivot/shelve) must include: a concrete first step, an effort estimate, and what is preserved vs. lost
- Rule 5: The agent makes a specific recommendation (not three equal options) based on evidence, but the developer can override

**Edge Cases:**
- Scenario 1: No `.pyro/spark.md` exists (project predates Pyro Kit) → Expected: Infer original intent from README and first commit messages, note it as inferred
- Scenario 2: Git history is minimal (< 5 commits) → Expected: Skip trend analysis, focus on progress assessment and soul statement
- Scenario 3: Developer selects "not now" → Expected: Record the non-decision, schedule a future prompt, but don't nag
- Scenario 4: Developer disagrees with the recommendation → Expected: Pre-built alternative plans are already displayed, no re-computation needed

### Feature: `/scope` — Soul-Preserving Scope Cuts

**Description:** When a project needs to be cut down to survive, `/scope` identifies the "soul" — the core fascination that makes the project worth building — and proposes cuts that preserve it. Inspired by game design pillars, screenwriting premise, and musical hooks.

**User Flow:**
1. Developer invokes `/scope`
2. System proposes a "soul statement" extracted from the spark session and early development
3. Developer confirms or refines the soul statement
4. System categorizes all features/components into three tiers: soul-critical (the project dies without these), soul-serving (supports the core but isn't the core), nice-to-have (could be a different project)
5. System proposes a specific cut: what to keep, what to remove, effort saved, and "the smallest thing that would satisfy your curiosity"
6. Developer accepts, adjusts, or requests alternative cuts

**Business Rules:**
- Rule 1: Soul identification always comes before feature categorization — the soul is the filter
- Rule 2: A valid soul statement must be about a fascination or curiosity, not a feature list
- Rule 3: The "smallest satisfying thing" is always proposed — the minimal version that preserves the soul
- Rule 4: Effort math is always explicit (hours saved, hours remaining)

## Success Metrics

### Key Performance Indicators

- **Completion Rate:** Target: developer ships 30%+ of projects started with Pyro Kit (vs. current ~10% estimated baseline)
- **Explicit Decisions:** Target: 100% of project endings are explicit (shipped, shelved with autopsy, or composted) — zero silent abandonments
- **Fascination Index Growth:** Target: after 5+ projects, the fascination index surfaces a "deepest fascination" pattern
- **Pulse Effectiveness:** Target: 60%+ of `/pulse` check-ins result in continued engagement (push or pivot, not shelve)
- **Time to First Ship:** Target: first project completed using full Pyro Kit lifecycle within 60 days of framework adoption

### Tracking Requirements

| Event | Properties | Purpose |
|-------|------------|---------|
| Skill invoked | skill name, phase, project, timestamp | Track which skills are actually used |
| Gate passed | gate number, project, duration in phase | Measure time spent in each phase |
| Proposal accepted | skill, iteration count | Measure how many iterations to convergence |
| Pulse outcome | decision (push/pivot/shelve), recommendation match | Track anti-abandonment effectiveness |
| Autopsy completed | project, primary cause, fascinations extracted | Feed pattern analysis |
| Project terminal state | shipped/shelved/composted, total duration, completion % | The ultimate success metric |

Note: All tracking is local files (pulse-log.md, project-registry.yaml). No external analytics.

---

## Constraints and Assumptions

### Constraints

- **Solo developer only** — no team features, no shared state, no collaboration workflows
- **Claude Code only** — SKILL.md format, plugin architecture, hooks system. No IDE-specific features
- **Local files only** — all state in `.pyro/` (project) and `~/.pyro/` (global). No databases, no cloud services
- **Propose-react-iterate only** — every skill must propose concrete things. No Socratic questioning, no open-ended creative prompts, no "imagine X"
- **~25 skills target** — frameworks with 14 (Superpowers) feel lean, 68 (BMAD) feel bloated. Target the 15-25 range

### Assumptions

- The developer already uses Claude Code as their primary AI coding tool
- The developer will invoke skills voluntarily (auto-suggestion helps but isn't sufficient alone)
- The SKILL.md format and plugin architecture are stable and won't have breaking changes
- Git is used for version control in all projects
- The propose-react-iterate pattern works for all phases (validated by SFD for phases 2-4, hypothesized for phases 0, 1, 5, 6)

## Risks and Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Developer skips Phase 0-1 and jumps straight to coding (the exact problem Pyro Kit solves) | High | High | SessionStart hook reminds; `/pyro` orchestrator detects missing state and suggests starting from Phase 0 |
| Fascination index becomes noise after many projects | Medium | Medium | Intensity decay over time; `/patterns` actively prunes and clusters |
| `/pulse` auto-suggestion feels nagging | Medium | Medium | Configurable dormancy threshold; "not now" is always an option with no repeat for N days |
| Proposal quality depends on Claude model capability | High | Low | SFD's scaling hypothesis: effectiveness improves with model capability. Current Opus 4.6 is sufficient |
| Context window limits restrict how much state skills can read | Medium | Medium | Progressive disclosure: skills read only what they need. State files have size limits (state.md < 100 lines) |
| The 25-skill framework itself gets abandoned at 60% | High | Medium | Build in phases. MVP is 4 skills (/spark, /pulse, /pyro, /autopsy). Ship MVP first, expand incrementally |

## Open Questions

- [x] Should Pyro Kit be a plugin or standalone skills? — **Decision: Plugin** (bundles skills + agents + hooks + state scripts)
- [x] What interaction model? — **Decision: Propose-react-iterate** (SFD philosophy, never Socratic)
- [x] How many skills? — **Decision: ~25 across 7 phases**, with 4-skill MVP
- [ ] Should `/remix` lenses be user-extensible or curated? — Leaning curated for v1, extensible later
- [ ] How should the fascination index handle conflicting themes across autopsies? — Needs design in SDD
- [ ] What's the right dormancy threshold default? — 5 days proposed, needs real-world testing

---

## Supporting Research

### Competitive Analysis

Extensive analysis of 40+ tools across the pre-spec and spec-driven ecosystem. Key findings:
- **BMAD** (27 agents, 68 skills): Closest in scope but execution-focused, starts at "idea" not "feeling"
- **Superpowers** (14 skills): Best brainstorming skill but uses Socratic questioning pattern
- **GSD** (24 commands, 11 agents): Best state management but no ideation phase
- **EveryInc Compound Engineering** (26 agents, 23 workflows): Compounds learning but project-scoped, not cross-project
- **No existing tool** combines pre-idea excavation, propose-react-iterate interaction, anti-abandonment intervention, and cross-project fascination tracking

Full research: `.internal/research/ideation-research/12-solo-creative-developer-tools.md` (30+ tools), `.internal/research/ideation-research/13-pyro-kit-feasibility.md` (gap analysis, architecture, psychology)

### User Research

Based on analysis of the target user's 20+ GitHub repositories, conversation history, and explicit feedback:
- The user self-describes as "lazy" and "not creative" in the generative sense but has excellent evaluative taste
- Explicitly rejected Socratic questioning: "I absolutely hate [brainstorm questions like 'imagine X and then Y'] because I need no AI for that"
- Proposed the core interaction model themselves: "agent propose solution -> user gives feedback -> agent iterates"
- Connected Pyro Kit to their own Surface-First Development project, validating that propose-react-iterate is their preferred interaction pattern universally

### Market Data

Not applicable. Pyro Kit is personal tooling, not a commercial product. The developer explicitly stated they don't care about market research or revenue. The only "market" is one person's creative process.

### Psychology Research

6 validated factors driving project abandonment (from ADHD research, creative psychology, Scott Belsky's "The Messy Middle"):
1. Novelty depletion (dopamine phenomenon, not laziness)
2. Taste-ability gap (Ira Glass)
3. Messy middle structural difference (Belsky)
4. Invisible progress
5. Out of sight, out of mind
6. No explicit decision (drift, not choice)

Anti-abandonment techniques from creative professionals:
- **Game design**: Design pillars survive scope cuts; prototype core mechanics before committing
- **Screenwriting**: Premise is the one sentence that survives every rewrite
- **Music**: The hook never changes; everything else serves it
- **ADHD research**: Inject novelty, make progress visible, continuous task breakdown, reframe success

Full research: `.internal/research/ideation-research/13-pyro-kit-feasibility.md` (Section 5)
