# Contract Output Format

`.pyro/contract.md` is the frozen contract bundle written by `/contract`. It is the sole input for `/build`, which uses it to plan vertical slices and track hardening progress. Every item in contract.md must trace back to a specific artifact in surface.md.

## Full Schema

### Frontmatter Fields

| Field | Type | Required | Default | Producer | Consumer |
|-------|------|----------|---------|----------|----------|
| `version` | Number | Yes | `1` | `/contract` (incremented on revision) | `/build` |
| `freeze_date` | Date (YYYY-MM-DD) | Yes | N/A | `/contract` (date of freeze) | `/build` |
| `surface_type` | String: `gui` \| `cli` \| `api` \| `pipeline` \| `agent` | Yes | N/A | `/contract` (copied from surface.md) | `/build` |
| `flows_count` | Number | Yes | N/A | `/contract` (from surface.md) | `/build` |
| `contracts_count` | Number | Yes | N/A | `/contract` (count of API contracts derived) | Diagnostic |
| `invariants_count` | Number | Yes | N/A | `/contract` (count of invariants derived) | Diagnostic |
| `nfr_count` | Number | Yes | N/A | `/contract` (count of NFRs derived) | Diagnostic |

### Body Sections

| Section | Required | Content |
|---------|----------|---------|
| `## API Contracts` | Yes | Per-contract blocks: name, endpoint/interface, input, output, error shapes, "Derived from:" |
| `## Domain Invariants` | Yes | Per-invariant blocks: ID, rule, enforced at, "Derived from:" |
| `## Non-Functional Requirements` | Yes | Per-NFR blocks: ID, target, "Derived from:", verification |
| `## Acceptance Criteria` | Yes | Per-flow checklists of testable Given/When/Then assertions |
| `## Hardening Plan` | Yes | Table: component, current state, target state, priority |

## Surface-Type-Specific Derivation Guidance

Contract shapes differ by surface type. Use the appropriate shape when deriving API contracts:

### GUI Surfaces
```
**Endpoint/Interface:** POST /api/items
**Input:** { name: String, category: String }
**Output:** { id: Number, name: String, created_at: Date }
**Error shapes:** 400 { error: "name required" }, 409 { error: "duplicate name" }
```

### CLI Surfaces
```
**Endpoint/Interface:** `command [flags] [args]`
**Input:** flags: --flag (type), args: positional (type), stdin: (format)
**Output:** stdout: (format), exit code: 0 (success) / 1 (error)
**Error shapes:** stderr: "error message", exit code: 1
```

### API Surfaces
```
**Endpoint/Interface:** fn method_name(param: Type) -> ReturnType
**Input:** param description and type constraints
**Output:** return type and shape
**Error shapes:** exceptions/errors and when they are raised
```

### Pipeline Surfaces
```
**Endpoint/Interface:** event: event_name
**Input:** payload: { field: Type }
**Output:** downstream event: { field: Type }
**Error shapes:** dead letter: { original: payload, error: String }
```

### Agent Surfaces
```
**Endpoint/Interface:** trigger: trigger_description
**Input:** context: { field: Type }
**Output:** action: { type: String, detail: String }
**Error shapes:** fallback: { reason: String, suggested_action: String }
```

## Worked Example: CLI Leave Tool

This continues the Leave Tool example chain from surface-output-format.md.

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

### Contract 3: History (List Notes)
**Endpoint/Interface:** `leave --history`
**Input:** flags: --history (no value)
**Output:** stdout: date-sorted list with first line of each note, exit code: 0
**Error shapes:** No notes -> stdout: "No leave notes yet." exit code: 0
**Derived from:** Flow 3 -- History, SSI: `leave --history`, No notes

### Contract 4: Storage Init
**Endpoint/Interface:** internal: ensure_storage()
**Input:** none (checks .leave/ directory existence)
**Output:** .leave/ directory exists after call
**Error shapes:** permission denied -> stderr: error, exit code: 1
**Derived from:** Flow 1 -- Basic Leave, SSI: .leave/ missing -> Create directory silently

### Contract 5: Note Write
**Endpoint/Interface:** internal: write_note(answer1, answer2)
**Input:** answer1: String, answer2: String (both may be empty)
**Output:** .leave/note.md written with timestamp, answer1, answer2
**Error shapes:** disk full -> stderr: error, exit code: 1
**Derived from:** Flow 1 -- Basic Leave, step 5: Writes .leave/note.md

## Domain Invariants

### INV-1: Empty Answers Are Valid
**Rule:** The system must never reject empty input for either question.
**Enforced at:** Input validation (or lack thereof) -- no validation on answer content.
**Derived from:** Flow 1 -- Basic Leave, SSI: Empty answer -> Accept empty, write anyway

### INV-2: Storage Created on First Use
**Rule:** The .leave/ directory must be created silently if it does not exist.
**Enforced at:** Storage initialization before any read or write operation.
**Derived from:** Flow 1 -- Basic Leave, SSI: .leave/ missing -> Create directory silently

### INV-3: Interruption Safety
**Rule:** If the user interrupts (Ctrl+C) during prompts, no partial file may be written.
**Enforced at:** Signal handling -- write only after both answers collected.
**Derived from:** Flow 1 -- Basic Leave, SSI: Ctrl+C during prompt -> Abort, no file written

## Non-Functional Requirements

### NFR-1: Instant Response
**Target:** leave command completes in under 200ms (excluding user input time).
**Derived from:** Flow 1 -- Basic Leave: the ritual metaphor implies near-instant response. Any perceptible delay would break the ritual quality.
**Verification:** Time the command execution excluding prompt wait time.

### NFR-2: No External Dependencies
**Target:** Zero runtime dependencies beyond Python/shell standard library.
**Derived from:** Surface decisions: ".leave/ directory, not .pyro/ -- tool is standalone." Standalone means no install step, no package manager.
**Verification:** Run in a fresh environment with no prior setup.

## Acceptance Criteria

### Flow: Basic Leave
- [ ] Given a project directory, when user runs `leave`, then two questions are prompted in sequence
- [ ] Given prompted questions, when user answers both, then .leave/note.md is written with timestamp and answers
- [ ] Given prompted questions, when user provides empty answers, then note is still written (empty answers accepted)
- [ ] Given no .leave/ directory, when user runs `leave`, then .leave/ is created silently before writing
- [ ] Given user is mid-prompt, when user presses Ctrl+C, then no file is written and command exits cleanly

### Flow: Return
- [ ] Given a project with leave notes, when user runs `leave --return`, then the last note's answers are displayed
- [ ] Given a project with no leave notes, when user runs `leave --return`, then "No leave notes yet." is displayed

### Flow: History
- [ ] Given a project with multiple leave notes, when user runs `leave --history`, then notes are listed by date with first line shown
- [ ] Given a project with no leave notes, when user runs `leave --history`, then "No leave notes yet." is displayed

## Hardening Plan

### Simulated Components
| Component | Current State | Target State | Priority |
|-----------|--------------|--------------|----------|
| Note storage | Mock data in variables | Real .leave/note.md file I/O | 1 |
| Prompt interaction | Simulated in prototype | Real stdin prompts | 1 |
| Date/time formatting | Hardcoded dates | Real timestamps | 2 |
| History listing | Mock note list | Real directory scan | 2 |
| Error handling | Happy-path only | Permission errors, disk full, signal handling | 3 |
```

---

## Note for /build

This file is the sole input for `/build`. The API Contracts define what to implement. The Domain Invariants define rules to enforce. The NFR Targets define quality thresholds. The Acceptance Criteria define what to test after each vertical slice. The Hardening Plan defines the sequence from prototype to production.

Each "Derived from:" field traces back to surface.md, forming the chain: surface behavior -> frozen contract -> implementation slice -> acceptance test.
