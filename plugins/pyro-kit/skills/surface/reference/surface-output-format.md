# Surface Output Format

`.pyro/surface.md` is the converged surface state written by `/surface`. It is the sole input for Phase 4's `/contract` skill. The Surface State Inventory must enumerate every interaction point so `/contract` can derive API contracts and domain invariants.

## Full Schema

### Frontmatter Fields

| Field | Type | Required | Default | Producer | Consumer |
|-------|------|----------|---------|----------|----------|
| `surface_type` | String: `gui` \| `cli` \| `api` \| `pipeline` \| `agent` | Yes | N/A | `/surface` (keyword detection) | `/contract` |
| `convergence_date` | Date (YYYY-MM-DD) | Yes | N/A | `/surface` (on convergence) | `/contract` |
| `iterations` | Number | Yes | N/A | `/surface` (count of iteration rounds) | Diagnostic |
| `flows_count` | Number | Yes | N/A | `/surface` (count of flows in prototype) | `/contract` |

### Body Sections

#### `## Flows`

Each flow that was prototyped and converged. Every flow has:

- **Name:** Descriptive flow name
- **Trigger:** What initiates this flow (user action, command, event)
- **Expected behavior:** Numbered steps describing the interaction end-to-end

Cover every flow that was demonstrated in the prototype. This is the behavioral contract.

#### `## Decisions`

Chronological list of design decisions made during iteration. Format:

```
- YYYY-MM-DD: [what was decided] -- [reasoning and rejected alternatives]
```

Captures what was tried, what was kept, what was rejected, and why.

#### `## Surface State Inventory`

Per-flow table enumerating every interaction point with expected behavior and state classifications. This is the behavioral contract `/contract` will consume to derive API contracts and domain invariants.

Format:

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

#### `## Edge Cases`

Edge cases explored during iteration and their resolution. Format:

```
- [edge case description]: [how it was resolved]
```

---

## Worked Example: CLI Leave Tool

```yaml
---
surface_type: cli
convergence_date: 2026-03-14
iterations: 4
flows_count: 3
---

## Flows

### Flow 1: Basic Leave
**Trigger:** User runs `leave` in a project directory
**Expected behavior:**
1. Prompt: "What's the one thing you'd tell yourself tomorrow morning?"
2. User types answer
3. Prompt: "What's stuck or unresolved?"
4. User types answer
5. Writes .leave/note.md with timestamp and answers
6. Prints: "Noted. See you tomorrow."

### Flow 2: Return
**Trigger:** User runs `leave --return` or enters a project with a recent leave note
**Expected behavior:**
1. Reads most recent .leave/note.md
2. Prints: "Last time you said: [answer to Q1]"
3. Prints: "Still stuck on: [answer to Q2]"

### Flow 3: History
**Trigger:** User runs `leave --history`
**Expected behavior:**
1. Lists all leave notes by date
2. Shows first line of each note

## Decisions
- 2026-03-14: Two questions, not three -- developer said "two is the right ritual weight"
- 2026-03-14: No --force flag -- rejected as over-engineering for a ritual tool
- 2026-03-14: .leave/ directory, not .pyro/ -- tool is standalone, not Pyro-dependent

## Surface State Inventory

### Flow: Basic Leave
| Interaction Point | Expected Behavior | States Covered |
|-------------------|-------------------|----------------|
| `leave` command | Prompt first question | happy-path |
| Empty answer | Accept empty, write anyway | empty-state (in-scope) |
| .leave/ missing | Create directory silently | first-run (in-scope) |
| Ctrl+C during prompt | Abort, no file written | interruption (in-scope) |

### Flow: Return
| Interaction Point | Expected Behavior | States Covered |
|-------------------|-------------------|----------------|
| `leave --return` | Display last note | happy-path |
| No leave notes exist | "No leave notes yet." | empty-state (in-scope) |

### Flow: History
| Interaction Point | Expected Behavior | States Covered |
|-------------------|-------------------|----------------|
| `leave --history` | List notes by date | happy-path |
| No notes | "No leave notes yet." | empty-state (in-scope) |

## Edge Cases
- Multiple leave notes in one day: append with time suffix
- Very long answers: no truncation, write full text
- Non-git directory: still works -- leave notes are per-directory, not per-repo
```

---

## Note for /contract

This file is the sole input for Phase 4's `/contract` skill. The Surface State Inventory must enumerate every interaction point so `/contract` can derive API contracts and domain invariants. Each "in-scope" state is a behavior that must be preserved through implementation. Each "deferred" state is a known gap that `/contract` should flag for coverage.
