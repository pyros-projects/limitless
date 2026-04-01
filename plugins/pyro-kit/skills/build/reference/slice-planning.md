# Slice Planning Reference

Load this reference on first /build invocation. It provides slice ordering heuristics, verification checklist templates, the progressive hardening sequence, and the release readiness evidence template.

## Slice Ordering Heuristics

When mapping contract flows to slices, use these ordering rules:

### Priority Order

1. **Highest-value user-facing flow first.** The flow that delivers the most visible value to the end user. If not obvious from contract.md, ask the developer: "Which flow matters most to you?"
2. **Data-producing flows before data-consuming flows.** If Flow B reads data that Flow A creates, Flow A goes first. This avoids building consumers before producers exist.
3. **Independent flows before dependent flows.** Flows with no dependencies on other flows are easier to verify in isolation. Build them first to establish a working baseline.
4. **User-facing before infrastructure.** Flows the user interacts with directly take priority over background processes, internal APIs, or admin tooling.

### Flow-to-Slice Mapping

- **One flow = one slice** is the default. Each slice makes exactly one surface flow real end-to-end.
- **Exception: shared critical infrastructure.** If two flows share a critical component (e.g., both need a database connection or auth layer), group the infrastructure setup with the first flow that needs it.
- **Never group unrelated flows.** Grouping is only justified by shared infrastructure, not by convenience or perceived similarity.

### Handling Ambiguity

If the ordering is unclear (flows seem equally valuable, no obvious dependencies):
- Ask the developer: "Flows X, Y, and Z seem equally important. Which one do you want working first?"
- Default to the flow with the most acceptance criteria in contract.md (more criteria = more behavioral surface = higher value signal).

## Verification Checklist Template

Use this template after every slice completion. The checklist must cover ALL flows, not just the one just implemented.

```markdown
## Slice {N} Complete -- Verification

Run the app and verify against the surface baseline:

### Real Flows (backed by implementation)
- [ ] **Flow {name} [REAL]:** {acceptance criteria steps from contract.md}

### Mock Flows (still using mock data)
- [ ] **Flow {name} [MOCK]:** {surface.md expected behavior -- still works?}

### Mock Preservation
Verify these mock flows still work after implementing {slice flow name}:
- [ ] {mock flow 1}: {specific behavior to check}
- [ ] {mock flow 2}: {specific behavior to check}

---

All green? Say "next" to proceed to slice {N+1}.
Any failures? Describe what went wrong.
```

### Verification Rules

- **Every flow gets checked.** No exceptions. A real flow that passes but breaks a mock flow is a failure.
- **Mock flows verify against surface.md baseline.** The expected behavior from ## Flows in surface.md is the reference for mock verification.
- **Real flows verify against contract.md acceptance criteria.** The testable assertions from ## Acceptance Criteria are the reference for real verification.
- **Developer confirms each check.** The /build skill never marks verification as passed -- only the developer can confirm.

## Progressive Hardening Sequence

After all slices are complete (all flows are [REAL]), work through hardening steps. The sequence below applies only to categories present in the project's contract.md ## Hardening Plan.

### Hardening Order

1. **Mock data -> Real persistence.** Replace hardcoded/mock data with actual database or file storage. This is always first because real data flow validates the entire pipeline.
2. **Placeholder auth -> Real identity.** Replace any placeholder authentication with real identity management. Depends on persistence being real (step 1).
3. **Simulated behavior -> Domain logic.** Replace any simplified or stubbed business logic with the real rules from domain invariants in contract.md.
4. **Happy-path only -> Error handling.** Add validation, error messages, loading states, and edge case handling per the edge cases documented in surface.md and invariants in contract.md.
5. **Baseline perf -> Optimization.** Only if NFR targets in contract.md specify measurable thresholds. Measure first, optimize only what fails to meet targets.

### Hardening Rules

- **One step at a time.** Complete and verify one hardening step before starting the next.
- **Full verification after each step.** Same checklist as after slices, but now all flows should be [REAL]. Verify that hardening did not break anything.
- **Only applicable categories.** Skip categories that do not appear in the project's ## Hardening Plan. A CLI tool with no auth does not need step 2.
- **Trace to contract.md.** Every hardening step must correspond to an item in ## Hardening Plan. No speculative hardening.

## Release Readiness Evidence Template

Use this template when the developer requests a readiness check via `/build readiness`.

```markdown
## Release Readiness

**Contract version:** v{N}
**Surface type:** {surface_type}
**Freeze date:** {freeze_date}

### Build Progress
- **Slices complete:** {N}/{total} (all flows real)
- **Hardening complete:** {N}/{total applicable steps}
- **Acceptance criteria:** {passed}/{total}

### Slice Evidence
| Slice | Flow | Status | Verified |
|-------|------|--------|----------|
| 1 | {flow name} | Real | {date} |
| 2 | {flow name} | Real | {date} |

### Hardening Evidence
| Component | Was | Now | Verified |
|-----------|-----|-----|----------|
| {component} | {mock state} | {real state} | {date} |

### Acceptance Criteria
{Per-flow checklist with pass/fail marks}

### Verdict
{RELEASE READY | NOT READY -- with remaining gaps listed}
```

### Readiness Rules

- **All slices complete** -- no flows still in [MOCK] state.
- **All applicable hardening steps complete** -- no mock data, placeholder auth, or stubbed logic remaining.
- **All acceptance criteria pass** -- every testable assertion from contract.md verified by the developer.
- **Contract version match** -- the build was done against the current frozen contract version.
