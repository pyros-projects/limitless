---
name: openspec
description: Spec-driven development using OpenSpec — a lightweight, fluid framework for defining what to build before writing code. Use for feature planning, brownfield changes, and structured AI-assisted development.
homepage: https://github.com/Fission-AI/OpenSpec
read_when:
  - You're starting a new feature and want structured planning before code.
  - You need to agree on requirements, design, and tasks before implementation.
  - You're making changes to an existing codebase and want spec-anchored artifacts.
  - Someone mentions "spec", "proposal", "change request", or "feature planning".
  - You need to understand what the current system does before modifying it.
metadata:
  openclaw:
    emoji: "📋"
---

# OpenSpec — Spec-Driven Development

OpenSpec is a lightweight, fluid spec framework for AI-assisted development. It helps you and your AI agree on **what to build** before writing code, using structured artifacts that persist as the source of truth.

**Philosophy:** Fluid not rigid. Iterative not waterfall. Brownfield-first.

## Which Workflow?

Pick the right pattern before starting:

| Situation | Workflow | Commands |
|-----------|----------|----------|
| Clear scope, <5 tasks, single session | **Quick Feature** | `/opsx:new` → `/opsx:ff` → `/opsx:apply` → `/opsx:verify` → `/opsx:archive` |
| Unclear requirements, need investigation | **Exploratory** | `/opsx:explore` → `/opsx:new` → `/opsx:continue` (repeat) → `/opsx:apply` |
| Complex change, want review at each step | **Incremental** | `/opsx:new` → `/opsx:continue` → [review] → repeat → `/opsx:apply` |
| 10+ tasks, multi-session, dependencies | **Large Feature + Beads** | `/opsx:new` → `/opsx:ff` → [import to Beads] → `bd ready` loop → `/opsx:verify` → `/opsx:archive` |

## Installation & Setup

Requires Node.js 20.19+.

```bash
npm install -g @fission-ai/openspec@latest
cd /path/to/your/project
openspec init --tools claude   # or: codex, cursor, copilot, all
```

**Prerequisite:** Run `openspec init` so your agent has the `/opsx:*` slash command instructions installed.

## Session Start Protocol

Always check current state at the start of a session:

```bash
openspec list                    # Shows active changes
openspec status --change <name>  # Shows artifact + task completion status
```

## Project Structure

```
openspec/
├── specs/              # Source of truth (how the system currently works)
│   └── <domain>/
│       └── spec.md
├── changes/            # One folder per proposed change
│   └── <change-name>/
│       ├── proposal.md     # WHY — intent, scope, approach
│       ├── specs/          # WHAT — delta specs (ADDED/MODIFIED/REMOVED)
│       ├── design.md       # HOW — technical approach, architecture
│       └── tasks.md        # DO — implementation checklist
└── config.yaml         # Project configuration (optional)
```

## Core Concepts

### Specs = Source of Truth

`openspec/specs/` describes how your system currently works, organized by domain. These are living documents that evolve as you ship features. Always read relevant specs before proposing changes.

**RFC 2119 keywords:** MUST/SHALL = absolute requirement, SHOULD = recommended, MAY = optional.

### Changes = Proposed Modifications

Each feature or bugfix gets its own isolated folder under `openspec/changes/`. Artifacts build on each other but you can update any artifact at any time.

| Artifact | Purpose |
|----------|---------|
| `proposal.md` | **WHY** — captures intent, scope, approach |
| `specs/` | **WHAT** — delta specs (ADDED/MODIFIED/REMOVED requirements) |
| `design.md` | **HOW** — technical approach and architecture decisions |
| `tasks.md` | **DO** — implementation checklist with checkboxes |

### Delta Specs

Instead of rewriting entire specs, deltas describe what changes:

```markdown
## ADDED Requirements
### Requirement: Two-Factor Authentication
The system MUST require a second factor during login.

## MODIFIED Requirements
### Requirement: Session Timeout
The system SHALL expire sessions after 30 minutes of inactivity.
(Previously: 60 minutes)

## REMOVED Requirements
### Requirement: Remember Me
(Deprecated in favor of 2FA)
```

On archive: ADDED gets appended, MODIFIED replaces, REMOVED deletes from the main specs.

## Workflow Commands

| Command | Purpose |
|---------|---------|
| `/opsx:explore` | Investigate ideas before committing to a change |
| `/opsx:new <name>` | Start a new change (creates folder under `changes/`) |
| `/opsx:continue` | Create the next artifact (one at a time, review between steps) |
| `/opsx:ff` | Fast-forward: generate all planning artifacts at once |
| `/opsx:apply` | Implement tasks from tasks.md |
| `/opsx:verify` | Validate implementation matches artifacts (completeness, correctness, coherence) |
| `/opsx:sync` | Merge delta specs into main specs |
| `/opsx:archive` | Archive a completed change (merges deltas, moves to archive folder) |
| `/opsx:bulk-archive` | Archive multiple completed changes at once |
| `/opsx:onboard` | Guided tutorial through the complete workflow |

## Combining OpenSpec with Beads

OpenSpec owns **what to build** (specs, proposals, design). Beads owns **what to do next** (dependency graph, execution state). Use Beads when you have 10+ tasks, cross-task dependencies, or multi-session work. For smaller changes, plain `/opsx:apply` is sufficient.

### The Combined Process

```
Phase 1: Planning (OpenSpec leads)
  /opsx:new <feature>
  /opsx:ff --> produces proposal.md, specs/, design.md, tasks.md
  Human reviews and approves artifacts

Phase 2: Task Import (Bridge to Beads)
  Parse tasks.md --> create Beads epic + tasks with dependencies
  Stamp Beads IDs back into tasks.md

Phase 3: Execution (Beads drives)
  bd ready --> pick task --> implement --> bd close --> check off tasks.md
  Repeat until all tasks done

Phase 4: Finalize (OpenSpec closes)
  /opsx:verify --> validate implementation matches specs
  /opsx:archive --> merge deltas, archive the change
```

### Task Import Procedure

When importing tasks.md into Beads, follow this sequence:

```bash
# 1. Create the epic, referencing the OpenSpec change name
bd create "Epic: <feature> (openspec: <change-name>)" -t epic -p 0
# Returns: bd-XXXX

# 2. Create each task as a child of the epic
# Parse tasks.md top to bottom, one bd create per checkbox item
bd create "<task title>" -p <priority> --parent bd-XXXX

# 3. Wire dependencies based on task relationships:
#    - Data dependencies: task B reads what task A writes --> B depends on A
#    - File overlap: tasks touching the same files --> sequential dependency
#    - Logical ordering: tests depend on implementation, UI depends on API
bd dep add <child-id> <parent-id>

# 4. Stamp Beads IDs back into tasks.md:
#    BEFORE: - [ ] Set up auth schema
#    AFTER:  - [ ] (bd-x1y2.1) Set up auth schema
```

**Dependency inference rules (apply in order):**
1. Schema/migration tasks block everything that queries those tables
2. API endpoint tasks block UI tasks that call them
3. Config/setup tasks block tasks that use that config
4. Implementation tasks block their corresponding test tasks
5. If two tasks modify the same file, make them sequential

### Keeping Both in Sync

- **Close in BOTH:** `bd close <id>` and check off `[x]` in `tasks.md`
- **New tasks mid-flight:** Add to both `tasks.md` and Beads, wire dependencies
- **`bd ready` is canonical** for execution order, not the tasks.md list order
- **`tasks.md` is canonical** for what the feature requires (scope)

## Error Recovery

### `/opsx:verify` fails

1. Read the verification output to identify which requirements are unmet
2. Check if the issue is missing implementation or spec drift
3. If implementation is incomplete: resume with `/opsx:apply` or `bd ready`
4. If spec changed during implementation: update the delta specs, then re-verify

### tasks.md and Beads are out of sync

1. Run `bd list` and compare against tasks.md checkboxes
2. Close any Beads tasks that are checked off in tasks.md but still open in Beads
3. Add any tasks that exist in tasks.md but not in Beads
4. Source of truth for scope is tasks.md; source of truth for execution state is Beads

### Agent created wrong dependencies

1. `bd dep remove <child> <parent>` to unwire incorrect edges
2. `bd dep add <child> <parent>` to add correct ones
3. `bd ready` to verify the new ordering makes sense

### Change needs to be abandoned

```bash
# Remove the change folder (specs were never merged)
rm -rf openspec/changes/<change-name>
# If Beads tasks were created, close the epic
bd close <epic-id> --reason "Change abandoned"
```

## CLI Quick Reference

```bash
openspec list                          # Active changes
openspec show <change-name>            # Change details
openspec status --change <name>        # Artifact + task status
openspec validate <change-name>        # Validate spec formatting
openspec archive <change-name>         # Archive via CLI
openspec view                          # Interactive dashboard
openspec update                        # Update tool configs after CLI upgrade
openspec list --json                   # JSON output for scripting
```

## Standard Reporting Contract (Mandatory)

At the end of every OpenSpec iteration, report status using this exact section structure:

```markdown
Completed
- <major result 1>
- <major result 2>
- Full artifact set created/updated:
  - <path>
  - <path>

Validation + Git
- <validation command> passed/failed.
- <test command> passed/failed.  # if code changed
- Commit pushed: <hash>.         # if committed
- Branch is clean and synced with origin/<branch>.  # if pushed

Progress stats
- Active implementation change: <name> = <done>/<total> done (<left> left)
- New planning change: <name> = <done>/<total> done (<left> left)   # include when relevant
- Project-wide (all changes incl. archive): <done>/<total> done (<left> left)
- Current ready Beads tasks: <id>, <id>, <id>
```

Rules:
- Always include `Completed`, `Validation + Git`, and `Progress stats` headings in that order.
- Prefer file paths over prose for artifact reporting.
- Never claim validation success without running the command.
- If a step is not applicable, write `N/A` explicitly (do not omit the line).
- Keep the report concise and machine-scannable; avoid narrative paragraphs in this section.

Metric definitions:
- `Active implementation change`: the change currently being executed.
- `New planning change`: a newly created change in the same session, if any.
- `Project-wide`: all checkbox tasks under `openspec/changes/**/tasks.md` (including archive).
- `Current ready Beads tasks`: from `bd ready`, top ready task IDs in priority order.

## Links

- **Repo:** <https://github.com/Fission-AI/OpenSpec>
- **Docs:** <https://openspec.dev/>
- **Getting Started:** <https://github.com/Fission-AI/OpenSpec/blob/main/docs/getting-started.md>
- **Commands:** <https://github.com/Fission-AI/OpenSpec/blob/main/docs/commands.md>
