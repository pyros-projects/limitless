---
title: "Pyro Kit — Implementation Plan"
status: complete
version: "1.1"
---

# Implementation Plan

## Scope

This specification covers **two scopes** — read the version that matches your intent:

| Version | Scope | Status | Skills |
|---------|-------|--------|--------|
| **v0.1.0 (MVP)** | 4-skill toolkit + infrastructure | **Shipped** | /pyro, /spark, /pulse, /autopsy |
| **v1.0.0 (Full Vision)** | 27-skill lifecycle framework across 7 phases | Roadmap | See PRD Features 2-8 |

- **Steps 1-6** of this plan deliver v0.1.0 (MVP)
- **Step 7** outlines the expansion roadmap toward v1.0.0
- The PRD and SDD describe the full v1.0.0 vision; MVP boundaries are marked with `[MVP]` tags

> **Why the distinction?** The PRD/SDD use "Phase" for lifecycle phases (Phase 0: Ignition through Phase 6: Lifecycle). This plan uses "Step" for implementation steps to avoid confusion.

## Validation Checklist

### CRITICAL GATES (Must Pass)

- [x] All `[NEEDS CLARIFICATION: ...]` markers have been addressed
- [x] All specification file paths are correct and exist
- [x] Each step follows TDD: Prime → Test → Implement → Validate
- [x] Every task has verifiable success criteria
- [x] A developer could follow this plan independently

### QUALITY CHECKS (Should Pass)

- [x] Context priming section is complete
- [x] All implementation steps are defined
- [x] Dependencies between steps are clear (no circular dependencies)
- [x] Parallel work is properly tagged with `[parallel: true]`
- [x] Activity hints provided for specialist selection `[activity: type]`
- [x] Every step references relevant SDD sections
- [x] Every test references PRD acceptance criteria
- [x] Integration & E2E tests defined in final step
- [x] Project commands match actual project setup

---

## Context Priming

*GATE: Read all files in this section before starting any implementation.*

**Specification**:

- `specs/001-pyro-kit/product-requirements.md` — Product Requirements (11 Must-Have features, 25+ skills, 7 phases)
- `specs/001-pyro-kit/solution-design.md` — Solution Design (plugin architecture, data models, runtime flows, 8 ADRs)
- `.internal/research/ideation-research/13-pyro-kit-feasibility.md` — Gap analysis, anti-abandonment psychology
- `~/projects/agents/surface-first-development/skills/surface-first/SKILL.md` — SFD skill to compose into Phases 2-4

**Key Design Decisions**:

- **ADR-1**: Plugin over standalone — bundle as Claude Code plugin with `.claude-plugin/plugin.json`
- **ADR-2**: PICS+Workflow format — all SKILL.md files use Persona/Interface/Constraints/State + Workflow
- **ADR-3**: Hybrid state — `.pyro/` per project, `~/.pyro/` global
- **ADR-4**: Compose SFD — Phases 2-4 wrap existing SFD SKILL.md via state-file handoff
- **ADR-5**: `/pyro` orchestrator — skill-based routing reads state.md and suggests next skill
- **ADR-6**: SessionStart hook — `session-init.sh` detects dormancy at session start
- **ADR-7**: Fascination index — YAML-indexed markdown in `~/.pyro/fascination-index.md`
- **ADR-8**: 4-skill MVP — `/spark`, `/pulse`, `/pyro`, `/autopsy` ship first

**Implementation Context**:

```bash
# This is a prompt engineering project — no code compilation, no test suites, no linting.
# Validation is structural and behavioral, not automated.

# Plugin Installation (local development)
claude --plugin-dir ./pyro-kit

# Persistent install (from inside Claude Code)
# /plugin marketplace add /path/to/pyro-kit
# /plugin install pyro-kit@pyro-kit

# Skill Invocation (manual testing)
/pyro                          # Orchestrator
/spark "something bugs me"     # Phase 0 — Ignition
/pulse                         # Phase 5 — Momentum
/autopsy                       # Phase 6 — Lifecycle

# Script Testing (use ${CLAUDE_PLUGIN_ROOT} paths when installed)
bash pyro-kit/scripts/session-init.sh    # Hook script
bash pyro-kit/scripts/git-activity.sh    # Git metrics

# Structural Validation
# Verify YAML frontmatter parses cleanly
# Verify all SKILL.md files have: Persona, Interface, Constraints, State, Workflow
# Verify state files are valid YAML
# Verify scripts output valid JSON / expected formats
```

**Reference Implementation**:

```bash
# The Startup plugin (3.2.1) is the reference for plugin structure and skill format
ls ~/.claude/plugins/cache/the-startup/start/3.2.1/

# SFD skill is the reference for propose-react-iterate and Phase 2-4 integration
cat ~/projects/agents/surface-first-development/skills/surface-first/SKILL.md
```

---

## Implementation Steps

Each task follows red-green-refactor: **Prime** (understand context), **Test** (red), **Implement** (green), **Validate** (refactor + verify).

> **Tracking Principle**: Track logical units that produce verifiable outcomes. The TDD cycle is the method, not separate tracked items.

> **MVP Scope**: Steps 1-6 deliver the 4-skill MVP (ADR-8). Step 7 outlines expansion to full ~25 skills.

---

### Step 1: Plugin Scaffold & State Infrastructure

Establishes the plugin container, state file schemas, hook system, and utility scripts. Everything subsequent steps build on.

- [x] **T1.1 Plugin Manifest & Directory Structure** `[activity: infrastructure]`

  1. Prime: Read The Startup's `.claude-plugin/plugin.json` for format reference `[ref: SDD/Deployment View; lines: 632-641]`. Read plugin directory map `[ref: SDD/Directory Map; lines: 237-323]`
  2. Test: Plugin directory has correct structure; `plugin.json` contains required fields (name, version, description); Claude Code recognizes the plugin when installed locally
  3. Implement: Create `pyro-kit/.claude-plugin/plugin.json` with name "pyro-kit", version "0.1.0". Create empty directories: `skills/`, `agents/`, `hooks/`, `scripts/`. Create `CHANGELOG.md` with initial entry
  4. Validate: `claude --plugin-dir ./pyro-kit` loads without error; plugin skills available in session
  5. Success: Plugin recognized by Claude Code `[ref: PRD/Constraints; lines: 337-338]`

- [x] **T1.2 Project State Schema (`.pyro/`)** `[activity: data-architecture]`

  1. Prime: Read state.md data model `[ref: SDD/Data Models; lines: 353-381]`. Read project state directory map `[ref: SDD/Directory Map; lines: 325-339]`
  2. Test: state.md template has valid YAML frontmatter with all required fields (project, phase, status, soul, original_spark, last_skill, last_activity, momentum, gate_history, pulse_count); markdown body has Current State and Decisions Made sections
  3. Implement: Create `pyro-kit/scripts/pyro-init.sh` — initializes `.pyro/` directory with `state.md` template, empty `pulse-log.md`, empty `session-notes/` directory. Script accepts project name as argument, uses sensible defaults, handles existing `.pyro/` gracefully
  4. Validate: Run `pyro-init.sh "test-project"` in a temp directory; verify `.pyro/state.md` has valid YAML frontmatter; verify idempotent (running twice doesn't corrupt)
  5. Success: Project state initializes with valid schema `[ref: SDD/Data Models state.md]`; state survives session resets `[ref: PRD/AC-Feature 10; lines: 206-212]`

- [x] **T1.3 Global State Schema (`~/.pyro/`)** `[activity: data-architecture]` `[parallel: true]`

  1. Prime: Read global state directory map and data models `[ref: SDD/Directory Map; lines: 341-351]`. Read fascination-index.md, project-registry.yaml, config.yaml schemas `[ref: SDD/Data Models; lines: 383-502]`
  2. Test: `config.yaml` has valid YAML with all default fields; `project-registry.yaml` schema supports project entries; `fascination-index.md` has valid YAML frontmatter with entries array
  3. Implement: Add global state initialization to `pyro-init.sh` — creates `~/.pyro/` if missing, seeds `config.yaml` with defaults (dormancy_threshold_days: 5, pulse_auto_suggest: true, etc.), creates empty `project-registry.yaml`, creates `fascination-index.md` with empty entries array, creates `autopsies/` and `patterns/` directories
  4. Validate: Run initialization; verify all files parse as valid YAML/YAML-frontmatter; verify no overwrite of existing global state on re-run
  5. Success: Global state initializes with valid schemas `[ref: SDD/Data Models config.yaml, project-registry.yaml, fascination-index.md]`

- [x] **T1.4 SessionStart Hook** `[activity: infrastructure]` `[parallel: true]`

  1. Prime: Read hook flow algorithm `[ref: SDD/Runtime View; lines: 588-613]`. Read hooks.json format from Claude Code documentation. Study session-init.sh requirements
  2. Test: `hooks.json` is valid JSON and declares a SessionStart hook pointing to `scripts/session-init.sh`; script outputs valid JSON with `additionalContext` field; script exits silently when no `.pyro/state.md` exists; script reports dormancy when inactive beyond threshold
  3. Implement: Create `pyro-kit/hooks/hooks.json` with SessionStart event pointing to `scripts/session-init.sh`. Create `pyro-kit/scripts/session-init.sh` implementing the algorithm: check for `.pyro/state.md`, read phase/status/last_activity, compute dormancy, check cross-project dormancy from `~/.pyro/project-registry.yaml`, output JSON to stdout
  4. Validate: Test with no `.pyro/` (silent exit); test with fresh state (context injection, no dormancy); test with stale state (dormancy warning); verify JSON output parses cleanly
  5. Success: Session hook injects context and detects dormancy `[ref: PRD/AC-Should Have; lines: 226-236]`; hook restores context within 2 seconds `[ref: SDD/Quality Requirements; lines: 739]`

- [x] **T1.5 Git Activity Script** `[activity: infrastructure]` `[parallel: true]`

  1. Prime: Read pulse dashboard requirements `[ref: PRD/Feature 7; lines: 177-184]`. Read git-activity.sh reference in SDD `[ref: SDD/Building Block View; lines: 229]`. Read performance requirement `[ref: SDD/Quality Requirements; lines: 740]`
  2. Test: Script produces commit frequency data (daily counts over configurable window); detects commit message sentiment shift (add/create vs fix/update); identifies branch staleness; handles repos with no commits, no remote, or not git-initialized; completes in < 5 seconds for repos up to 10K commits
  3. Implement: Create `pyro-kit/scripts/git-activity.sh` — outputs structured data (commit frequency trend, message categories, days since last commit, active branches, new repos detection via `~/.pyro/project-registry.yaml`). Output format: machine-readable sections that `/pulse` can parse
  4. Validate: Test against a real repo with history; test against empty repo; test performance on a large repo; verify output format is consistent
  5. Success: Git metrics available for `/pulse` `[ref: PRD/Feature 7 AC; lines: 180]`; completes in < 5 seconds `[ref: SDD/Quality Requirements; lines: 740]`

- [x] **T1.6 Step Validation** `[activity: validate]`

  Run all scripts in isolation. Verify plugin installs. Verify state schemas. Verify hook outputs valid JSON. All infrastructure is functional before any skills are built.

---

### Step 2: `/pyro` Orchestrator

The brain of the framework — reads project state and routes to the appropriate skill. Must work even when other skills don't exist yet (graceful degradation).

*Depends on: Step 1 (plugin scaffold, state schemas)*

- [x] **T2.1 `/pyro` Orchestrator Skill** `[activity: skill-authoring]`

  1. Prime: Read orchestrator routing algorithm `[ref: SDD/Runtime View; lines: 554-586]`. Read PICS+Workflow format from reference implementation `[ref: SDD/ADR-2]`. Read orchestrator PRD requirements `[ref: PRD/Feature 11; lines: 214-222]`
  2. Test: Skill has valid YAML frontmatter (name, description, user-invocable: true, allowed-tools); has all PICS+Workflow sections (Persona, Interface, Constraints, State, Workflow); first output is always a concrete recommendation (never a question); handles: no `.pyro/` (suggest init), fresh state (suggest /spark), stalled momentum (prioritize /pulse), each phase 0-6 (correct routing); `/pyro list` displays skills by phase; `/pyro status` shows current state
  3. Implement: Create `pyro-kit/skills/pyro/SKILL.md` with:
     - Persona: Lifecycle navigator
     - Interface: functions for init, status, list, route
     - Constraints: always propose (never ask), read state before routing, prioritize momentum signals
     - State: reads `.pyro/state.md`, `~/.pyro/project-registry.yaml`, `~/.pyro/config.yaml`
     - Workflow: implements routing algorithm from SDD, with shell preprocessing to load state.md
  4. Validate: Invoke `/pyro` in a project with no state → suggests init; invoke after init → suggests /spark; manually set state to phase 4 with stalled momentum → prioritizes /pulse
  5. Success: Orchestrator reads state and recommends next skill `[ref: PRD/AC-Feature 11; lines: 218-222]`; prioritizes /pulse on momentum decline `[ref: SDD/EARS Orchestration; lines: 761-763]`

- [x] **T2.2 Orchestrator Reference Files** `[activity: skill-authoring]`

  1. Prime: Read building block view for full skill inventory `[ref: SDD/Building Block View; lines: 178-233]`. Read phase/gate structure `[ref: PRD/Feature 10; lines: 203-212]`
  2. Test: `phase-map.md` lists all 7 phases with their gates, skills, and state files; `skill-catalog.md` lists all ~25 skills with phase, description, trigger phrases, prerequisites, and outputs
  3. Implement: Create `pyro-kit/skills/pyro/reference/phase-map.md` (phases 0-6, gates G0-G7, skill assignments). Create `pyro-kit/skills/pyro/reference/skill-catalog.md` (full skill inventory with metadata). Mark non-MVP skills as "planned" with expected wave
  4. Validate: Every skill from SDD building block view appears in catalog; every phase has at least one skill; every gate has criteria listed
  5. Success: Complete phase and skill reference available to orchestrator `[ref: SDD/Building Block View]`

- [x] **T2.3 Step Validation** `[activity: validate]`

  Install plugin locally. Invoke `/pyro` in various states. Verify routing logic matches SDD algorithm. Verify graceful degradation for skills that don't exist yet.

---

### Step 3: `/spark` — Pre-Idea Excavation

The most unique skill in the framework — turns a vague feeling into a crystallized idea using the propose-react-iterate pattern. Reads fascination index to inform idea generation.

*Depends on: Step 1 (state schemas), Step 2 (/pyro for routing)*

- [x] **T3.1 `/spark` Skill** `[activity: skill-authoring]`

  1. Prime: Read Phase 0 requirements `[ref: PRD/Feature 2; lines: 130-139]`. Read propose-react-iterate pattern `[ref: SDD/Cross-Cutting Concepts; lines: 635-651]`. Read state-file handoff pattern `[ref: SDD/Cross-Cutting Concepts; lines: 653-659]`. Read PRI core interaction requirements `[ref: PRD/Feature 1; lines: 121-128]`
  2. Test: Skill has valid PICS+Workflow structure; accepts vague input (feeling, annoyance, topic); first output is 3-5 concrete idea thumbnails (one-paragraph scenarios, not questions); responds to selection ("that one") by expanding and proposing variations; responds to approval ("yes") by persisting to `.pyro/spark.md` and updating `state.md`; reads `~/.pyro/fascination-index.md` to inform generation; never asks open-ended creative questions; stays under 500 lines
  3. Implement: Create `pyro-kit/skills/spark/SKILL.md` with:
     - Persona: Idea excavator that unearths what the developer actually wants to build
     - Interface: functions for excavate, expand, crystallize
     - Constraints: always produce thumbnails (never "what excites you?"), read fascination index, propose connections to past fascinations
     - State: reads `~/.pyro/fascination-index.md`, writes `.pyro/spark.md`, updates `.pyro/state.md`
     - Workflow: generate thumbnails → developer selects → expand → iterate → crystallize → persist → suggest /explore
  4. Validate: Invoke with vague input → produces thumbnails; select one → expands; approve → writes spark.md with valid content; state.md updated to phase 0, gate G0; no open-ended questions in any output
  5. Success: Vague input produces concrete idea thumbnails `[ref: PRD/AC-Feature 2; lines: 134]`; fascination index informs generation `[ref: PRD/AC-Feature 9; lines: 199]`; converged output persisted `[ref: PRD/AC-Feature 1; lines: 127]`

- [x] **T3.2 Spark Reference Files** `[activity: skill-authoring]` `[parallel: true]`

  1. Prime: Read idea thumbnail concept `[ref: PRD/User Journey; lines: 87-88]`. Read creative domain lenses `[ref: PRD/Feature 2 AC /remix; lines: 136]`
  2. Test: `techniques.md` documents at least 5 idea thumbnail generation techniques with examples; `domain-lenses.md` contains 6+ creative domain lenses (game design, music, screenwriting, architecture, improv, cooking) with vocabulary and analogies for each
  3. Implement: Create `pyro-kit/skills/spark/reference/techniques.md` (thumbnail generation approaches: scenario projection, annoyance amplification, fascination threading, constraint inversion, domain transplant). Create `pyro-kit/skills/spark/reference/domain-lenses.md` (shared lens library for /spark, /remix, /reframe)
  4. Validate: Techniques are concrete enough for Claude to apply; lenses include domain-specific vocabulary; file is referenced correctly from SKILL.md
  5. Success: Reference materials support idea generation quality `[ref: SDD/Progressive Disclosure; lines: 670-677]`

- [x] **T3.3 Excavator Agent** `[activity: skill-authoring]`

  1. Prime: Read agent directory map `[ref: SDD/Directory Map; lines: 324]`. Read SDD excavator description
  2. Test: Agent markdown defines a focused pre-idea exploration persona; can be dispatched by /spark for deep-dive exploration when the developer wants to go deeper on a direction
  3. Implement: Create `pyro-kit/agents/excavator.md` — agent that explores a single idea direction in depth, generating scenarios, use cases, and "a day in the life" narratives
  4. Validate: Agent can be dispatched from /spark; produces concrete exploration artifacts
  5. Success: Deep exploration available for idea directions `[ref: SDD/Directory Map; lines: 324]`

- [x] **T3.4 Step Validation** `[activity: validate]`

  Full `/spark` test: invoke with vague input, iterate through thumbnails, crystallize an idea, verify state files. Verify `/pyro` correctly routes to `/spark` for new projects.

---

### Step 4: `/pulse` — Momentum Dashboard

The centerpiece of the anti-abandonment system. Combines git analysis with psychological insight to detect momentum loss and propose concrete options.

*Depends on: Step 1 (git-activity.sh, state schemas), Step 2 (/pyro for routing)*

- [x] **T4.1 `/pulse` Skill** `[activity: skill-authoring]`

  1. Prime: Read pulse detailed specification `[ref: PRD/Detailed Feature Specs /pulse; lines: 263-287]`. Read momentum dashboard requirements `[ref: PRD/Feature 7; lines: 177-184]`. Read pulse business rules `[ref: PRD/Detailed Feature Specs; lines: 277-281]`. Read propose-react-iterate pattern `[ref: SDD/Cross-Cutting Concepts; lines: 635-651]`
  2. Test: Skill has valid PICS+Workflow structure; invocation produces a complete dashboard (not questions): git activity metrics with trend, progress visualization, novelty depletion signal, original spark quoted verbatim, three concrete paths (push/pivot/shelve); each path has: concrete first step, effort estimate, what's preserved vs lost; agent makes a specific recommendation (not three equal options); records decision in pulse-log.md; handles edge cases: no spark.md (infer from README/commits), minimal git history (< 5 commits), "not now" response; stays under 500 lines
  3. Implement: Create `pyro-kit/skills/pulse/SKILL.md` with:
     - Persona: Momentum analyst who names what's happening and proposes what to do about it
     - Interface: functions for analyze, dashboard, recommend, record
     - Constraints: always quote original spark verbatim, always make a recommendation, never nag (respect "not now"), all three paths pre-built
     - State: reads `.pyro/state.md`, `.pyro/spark.md`, `~/.pyro/config.yaml`; shell-preprocesses `git-activity.sh`; writes `.pyro/pulse-log.md` (append), updates `.pyro/state.md`
     - Workflow: gather metrics → compute signals → generate dashboard → present with recommendation → record decision → update state
  4. Validate: Invoke in a project with history → full dashboard appears; spark quoted verbatim; three options all have concrete first steps; select "push" → pulse-log.md updated; invoke with no spark.md → infers intent gracefully; invoke with minimal git → skips trend, shows progress
  5. Success: Dashboard shows all required elements `[ref: PRD/AC-Feature 7; lines: 180]`; specific recommendation made `[ref: PRD/Detailed Feature Specs Rule 5; lines: 281]`; decision recorded `[ref: PRD/Tracking Requirements; lines: 324]`

- [x] **T4.2 Pulse Reference Files** `[activity: skill-authoring]`

  1. Prime: Read pulse user flow `[ref: PRD/Detailed Feature Specs; lines: 267-274]`. Read dashboard elements from requirements
  2. Test: `dashboard-format.md` documents the exact dashboard layout with sections, metrics, and formatting; includes example output showing what a real dashboard looks like
  3. Implement: Create `pyro-kit/skills/pulse/reference/dashboard-format.md` — template for the momentum dashboard showing: activity metrics section (commit frequency graph as ASCII, gap analysis), progress section (features done/remaining, TODO count), novelty depletion signal (with explanation), spark quote block, three-path recommendation section with effort math
  4. Validate: Dashboard format is concrete enough for Claude to reproduce consistently; includes an example with realistic data
  5. Success: Consistent dashboard format across invocations `[ref: SDD/Quality Requirements; lines: 729]`

- [x] **T4.3 Step Validation** `[activity: validate]`

  Full `/pulse` test: invoke in a real project with git history, verify dashboard completeness, test all edge cases, verify pulse-log.md append behavior. Verify `/pyro` correctly suggests `/pulse` when momentum is stalled.

---

### Step 5: `/autopsy` — Value Extraction & Composting

Extracts value from dead or shelved projects and feeds it into the fascination index. The skill that closes the lifecycle loop.

*Depends on: Step 1 (state schemas, fascination index), Step 3 (/spark's fascination index reading validates the write path)*

- [x] **T5.1 `/autopsy` Skill** `[activity: skill-authoring]`

  1. Prime: Read autopsy requirements `[ref: PRD/Feature 8; lines: 185-192]`. Read fascination index update requirements `[ref: PRD/Feature 9; lines: 194-201]`. Read composting concept `[ref: SDD/Glossary; lines: 793]`. Read state-file handoff pattern `[ref: SDD/Cross-Cutting Concepts; lines: 653-659]`
  2. Test: Skill has valid PICS+Workflow structure; produces a structured autopsy report: what the soul was, what worked, what killed it (from taxonomy: novelty depletion, scope creep, taste gap, technical wall, new shiny thing), reusable code/patterns, underlying fascination; automatically updates `~/.pyro/fascination-index.md` with extracted themes; archives report to `~/.pyro/autopsies/{project-name}.md`; updates `~/.pyro/project-registry.yaml` with shelved status; updates `.pyro/state.md` to terminal state (shelved + G7); follows propose-react-iterate: proposes the autopsy report, developer confirms/adjusts
  3. Implement: Create `pyro-kit/skills/autopsy/SKILL.md` with:
     - Persona: Post-mortem analyst who extracts lasting value from every project outcome
     - Interface: functions for analyze, report, extract-fascinations, archive
     - Constraints: always produce full report (never partial), always update fascination index, reframe abandonment as composting (productive, not failure), propose report for developer review before persisting
     - State: reads `.pyro/state.md`, `.pyro/spark.md`, git history; writes `~/.pyro/autopsies/{name}.md`, updates `~/.pyro/fascination-index.md`, updates `~/.pyro/project-registry.yaml`, updates `.pyro/state.md`
     - Workflow: analyze project (code, commits, state files) → generate autopsy report → extract fascinations → propose report to developer → on approval: archive report, update fascination index, update registry, set terminal state
  4. Validate: Invoke on a project → full autopsy report generated; fascination index updated with new themes; report archived; project registry updated; state.md shows shelved + G7; re-running /spark in a new project → new themes visible from previous autopsy
  5. Success: Autopsy produces structured report with all required sections `[ref: PRD/AC-Feature 8; lines: 190]`; fascination index automatically updated `[ref: PRD/AC-Feature 9; lines: 198]`; terminal state recorded `[ref: PRD/AC-Feature 10; lines: 212]`

- [x] **T5.2 Autopsy Reference Files** `[activity: skill-authoring]`

  1. Prime: Read abandonment taxonomy from psychology research `[ref: PRD/Psychology Research; lines: 399-405]`. Read composting concept `[ref: SDD/Glossary; lines: 793]`
  2. Test: `report-template.md` documents the full autopsy report structure with all required sections; includes the abandonment cause taxonomy (novelty depletion, scope creep, taste gap, technical wall, new shiny thing, drift); includes example fascination extraction
  3. Implement: Create `pyro-kit/skills/autopsy/reference/report-template.md` — autopsy report template with sections: Soul Statement, Timeline, What Worked, What Killed It (taxonomy), Reusable Artifacts, Extracted Fascinations, Lessons for Future Projects. Include taxonomy definitions from psychology research
  4. Validate: Template covers all PRD-required sections; taxonomy matches research base
  5. Success: Consistent autopsy format across projects `[ref: SDD/Quality Requirements; lines: 729]`

- [x] **T5.3 Step Validation** `[activity: validate]`

  Full `/autopsy` test: invoke on a project, verify report completeness, verify fascination index update, verify state transitions. Verify the full loop: `/spark` reads what `/autopsy` wrote to the fascination index.

---

### Step 6: MVP Integration & Validation

Full system validation ensuring all 4 MVP skills + infrastructure work together as a cohesive lifecycle tool.

*Depends on: All previous steps*

- [x] **T6.1 Full Lifecycle Flow** `[activity: integration-test]`

  Verify the complete MVP journey end-to-end:

  1. Fresh project: `/pyro` → suggests init → `/pyro init` → suggests `/spark`
  2. Ignition: `/spark "something bugs me"` → thumbnails → select → crystallize → spark.md + state.md updated
  3. Skip to build (MVP has no Phase 1-4 skills): manually advance state to Phase 4
  4. Momentum check: `/pulse` → full dashboard with spark quote + 3 options → select "shelve"
  5. Composting: `/autopsy` → report + fascination index update + terminal state
  6. New project: `/spark` in different directory → fascination index themes inform new thumbnails

  `[ref: SDD/Runtime View Primary Flow; lines: 506-552]`

- [x] **T6.2 State-File Handoff Verification** `[activity: integration-test]`

  Verify cross-skill state consistency:

  - `/spark` writes `.pyro/spark.md` → `/pulse` reads it and quotes verbatim
  - `/autopsy` writes `~/.pyro/fascination-index.md` → `/spark` reads it for idea generation
  - All skills update `.pyro/state.md` consistently (phase, last_skill, momentum)
  - `~/.pyro/project-registry.yaml` tracks project across lifecycle
  - State files survive session boundaries (close and reopen Claude Code)

  `[ref: SDD/Cross-Cutting Concepts State-File Handoff; lines: 653-659]`

- [x] **T6.3 Hook & Orchestrator Integration** `[activity: integration-test]`

  Verify infrastructure integration:

  - SessionStart hook fires and injects context in Pyro Kit projects
  - Hook detects dormancy correctly (set last_activity to 10 days ago)
  - `/pyro` routing matches SDD algorithm for all state combinations
  - `/pyro list` shows all 4 MVP skills (others marked "planned")
  - Graceful degradation: invoking a non-existent skill produces helpful guidance

  `[ref: SDD/Runtime View Hook Flow; lines: 588-613]`

- [x] **T6.4 Quality Gates & Specification Compliance** `[activity: business-acceptance]`

  Final verification against PRD and SDD:

  - **Proposal Quality**: Every skill's first output is a concrete proposal, never a question `[ref: PRD/AC-Feature 1; lines: 125-128]` `[ref: SDD/EARS Core Interaction; lines: 738-740]`
  - **State Reliability**: State files survive session resets `[ref: SDD/Quality Requirements; lines: 739]`
  - **Context Budget**: Each SKILL.md < 500 lines `[ref: SDD/CON-4; lines: 37]`
  - **Graceful Degradation**: Skills work with missing prerequisites `[ref: SDD/Quality Requirements; lines: 742]`
  - **Soft Gating**: Gate warnings don't block `[ref: SDD/EARS Gate Enforcement; lines: 757-759]`
  - **No Socratic Questioning**: Zero instances of open-ended creative questions across all skills `[ref: PRD/Constraints; lines: 339]`
  - All PRD acceptance criteria for Features 1, 2, 7, 8, 9, 10, 11 verified for MVP scope
  - All SDD EARS criteria verified

---

### Step 7: Expansion Roadmap

Post-MVP expansion to the full ~25 skills. Each wave is independently shippable. Waves can be reordered based on usage patterns from the MVP.

> **Note**: This step is outlined, not fully specified. Each wave should get its own detailed task breakdown when implementation begins.

**Wave 7.1: Phase 0 Completion** (3 skills)
- `/remix` — Creative cross-pollination via domain lenses (reuses `domain-lenses.md` from /spark)
- `/thumbnail` — Quick disposable idea sketch (thin skill, minimal state)
- `/fascination` — View/update fascination index directly

`[ref: PRD/Feature 2; lines: 136-138]` `[ref: SDD/Directory Map Phase 0; lines: 257-270]`

**Wave 7.2: Phase 1 — Exploration** (4 skills)
- `/explore` — Design space exploration (proposes 3-4 directions)
- `/sketch` — Rough tangible representation of a direction
- `/contrast` — Side-by-side direction comparison
- `/narrow` — Converge on one direction with reasoning

`[ref: PRD/Feature 3; lines: 140-148]` `[ref: SDD/Directory Map Phase 1; lines: 271-278]`

**Wave 7.3: Phases 2-4 — SFD Wrappers** (10 skills)
- `/surface`, `/iterate`, `/converge`, `/state-map` (Phase 2 — wraps SFD Phases 2-3)
- `/derive`, `/freeze` (Phase 3 — wraps SFD Phase 4 + Gates 2-3) — also `/invariants`, `/nfr`
- `/slice`, `/implement`, `/harden`, `/verify` (Phase 4 — wraps SFD Phases 5-6 + Gates 4-5)

These are thin wrappers: read `.pyro/state.md`, bridge to SFD's `.sfd/decision-log.md`, invoke SFD skill, map SFD gates back to Pyro gates. Per ADR-4, SFD remains source of truth.

`[ref: PRD/Features 4-6; lines: 149-174]` `[ref: SDD/ADR-4; lines: 711-714]`

**Wave 7.4: Phase 5 Completion** (3 skills)
- `/reframe` — Novelty injection via creative domain lenses (reuses `domain-lenses.md`)
- `/scope` — Soul-preserving scope cuts (uses soul-framework.md reference)
- `/decide` — Push/pivot/shelve recommendation with pre-built plans

`[ref: PRD/Feature 7; lines: 181-184]` `[ref: SDD/Directory Map Phase 5; lines: 299-312]`

**Wave 7.5: Phase 6 Completion** (3 skills)
- `/ship` — Release checklist with gap highlighting
- `/revive` — Archaeological analysis of abandoned repos
- `/patterns` — Cross-project pattern analysis from fascination index

`[ref: PRD/Feature 8; lines: 189-192]` `[ref: SDD/Directory Map Phase 6; lines: 313-322]`

---

## Plan Verification

Before this plan is ready for implementation, verify:

| Criterion | Status |
|-----------|--------|
| A developer can follow this plan without additional clarification | ✅ |
| Every task produces a verifiable deliverable | ✅ |
| All PRD acceptance criteria map to specific tasks | ✅ |
| All SDD components have implementation tasks | ✅ |
| Dependencies are explicit with no circular references | ✅ |
| Parallel opportunities are marked with `[parallel: true]` | ✅ |
| Each task has specification references `[ref: ...]` | ✅ |
| Project commands in Context Priming are accurate | ✅ |

### PRD → Task Traceability

| PRD Feature | Task Coverage |
|-------------|---------------|
| Feature 1: Propose-React-Iterate Core | T2.1, T3.1, T4.1, T5.1 (verified in T6.4) |
| Feature 2: Phase 0 — Ignition | T3.1, T3.2, T3.3 (full /spark); Wave 7.1 (/remix, /thumbnail, /fascination) |
| Feature 3: Phase 1 — Exploration | Wave 7.2 |
| Feature 4: Phase 2 — Surface | Wave 7.3 |
| Feature 5: Phase 3 — Contract | Wave 7.3 |
| Feature 6: Phase 4 — Build | Wave 7.3 |
| Feature 7: Phase 5 — Momentum | T4.1, T4.2 (full /pulse); Wave 7.4 (/reframe, /scope, /decide) |
| Feature 8: Phase 6 — Lifecycle | T5.1, T5.2 (full /autopsy); Wave 7.5 (/ship, /revive, /patterns) |
| Feature 9: Fascination Index | T1.3 (schema), T3.1 (read), T5.1 (write); Wave 7.1 (/fascination) |
| Feature 10: Gate System | T2.1 (routing), T3.1/T4.1/T5.1 (gate updates); T6.4 (soft gating) |
| Feature 11: Orchestrator | T2.1, T2.2 (full /pyro) |
| Should Have: Session Hook | T1.4 (SessionStart hook) |
| Should Have: Dormancy Detection | T1.4 (cross-project check in session-init.sh) |

### SDD → Task Traceability

| SDD Component | Task Coverage |
|---------------|---------------|
| Plugin manifest | T1.1 |
| Project state (.pyro/) | T1.2 |
| Global state (~/.pyro/) | T1.3 |
| SessionStart hook | T1.4 |
| git-activity.sh | T1.5 |
| /pyro orchestrator | T2.1, T2.2 |
| /spark skill | T3.1, T3.2, T3.3 |
| /pulse skill | T4.1, T4.2 |
| /autopsy skill | T5.1, T5.2 |
| Excavator agent | T3.3 |
| Phase 0 remaining skills | Wave 7.1 |
| Phase 1 skills | Wave 7.2 |
| Phase 2-4 SFD wrappers | Wave 7.3 |
| Phase 5 remaining skills | Wave 7.4 |
| Phase 6 remaining skills | Wave 7.5 |
| State-file handoff | T6.2 |
| Soft gating | T6.4 |
| Progressive disclosure | All skills (< 500 lines + reference/) |
