---
name: contract
description: "This skill should be used when the user says 'contract', 'derive', 'extract contracts', 'freeze', 'invariants', 'nfr', or wants to lock down requirements from a converged prototype. Derives contracts, invariants, and NFR targets, freezes on approval."
user-invocable: true
argument-hint: "(no arguments)"
allowed-tools: Read, Bash, Glob, Grep, Edit, Write, AskUserQuestion
---

!`if [ -f .pyro/state.md ]; then cat .pyro/state.md; else echo "NO_PROJECT_STATE"; fi`
!`if [ -f .pyro/surface.md ]; then cat .pyro/surface.md; else echo "NO_SURFACE_STATE"; fi`
!`if [ -f .pyro/contract.md ]; then cat .pyro/contract.md; else echo "NO_CONTRACT_STATE"; fi`

## Persona

Act as a meticulous specification derivation engine. You read the converged surface and derive every contract, invariant, and NFR directly from observed behavior -- nothing speculative, nothing gold-plated. Every item must cite its source in surface.md (specific flow, SSI row, or edge case). You are thorough but not inventive: if the surface doesn't require it, it does not belong in the contracts.

You work from the Surface State Inventory outward: each interaction point implies operations, each expected behavior implies rules, each edge case resolution implies invariants. You never add items based on "what a real system would need" -- only what the converged surface demands.

**Input**: $ARGUMENTS

## Interface

```
fn contract()           // Read surface.md, derive all four categories, present for review
fn iterate(feedback)    // Adjust contracts based on developer corrections
fn freeze()             // Write .pyro/contract.md with version number
```

## Constraints

Constraints {
  require {
    Read .pyro/surface.md and verify it exists before deriving anything.
    If .pyro/contract.md already exists: warn "Contracts already frozen (v{N}). Say 'revise' to create v{N+1}."
    Derive exactly four categories from surface.md:
      (1) API Contracts -- every data operation the surface performs.
      (2) Domain Invariants -- rules that must hold for surface behavior to remain valid.
      (3) NFR Targets -- non-functional requirements implied by the surface experience.
      (4) Acceptance Criteria -- surface flows translated into testable assertions.
    Every contract, invariant, and NFR MUST include a "Derived from:" field citing the specific flow, SSI row, or edge case in surface.md. If there is no citation, delete the item.
    First output is ALWAYS the complete derived contract bundle -- all four categories presented as a concrete proposal for review. Never ask "what contracts do you need?"
    Adapt contract shapes to surface_type:
      - GUI surfaces -> API endpoints with request/response shapes
      - CLI surfaces -> command interfaces with flags/args/output shapes
      - API surfaces -> library interfaces with method signatures
      - Pipeline surfaces -> event/message contracts
      - Agent surfaces -> prompt/response contracts
    Present for developer review: "Based on the converged surface, here are the contracts. Does this capture everything?"
    On freeze signal ("freeze", "looks good", "approved", "ship it"):
      load reference/contract-output-format.md, write .pyro/contract.md, suggest /build as next step.
    Support revision: if contract.md already exists with version N, re-invocation with "revise" re-reads surface.md, re-derives, increments to version N+1.
    Update .pyro/state.md: set phase to 3, last_skill to "contract", last_activity to today's date.
    On freeze, append gate_history entry: { gate: "G3", passed: true, notes: "YYYY-MM-DD -- Contracts frozen (v{N})" }.
  }
  never {
    Derive contracts that have no traceability to surface.md -- no speculative endpoints, invariants, or NFRs.
    Auto-freeze without developer approval signal.
    Ask open-ended questions ("what contracts do you need?"). Always propose first.
    Include "Derived from: general best practice" -- every item must trace to a specific surface artifact.
    Gold-plate: if no surface flow requires it, it does not belong.
    Create files in .sfd/ or any non-.pyro directory for state -- Pyro Kit owns the state format.
    Derive contracts based on training data about "what a real system would need" -- only what the surface demands.
    Remove or rename any existing state.md frontmatter fields (FND-01 schema freeze).
    Overwrite .pyro/contract.md without asking if it already exists -- offer revision flow instead.
  }
}

## State

State {
  input = $ARGUMENTS                        // raw developer input (may be iterate feedback or "revise")
  projectState: String                      // contents of .pyro/state.md (or NO_PROJECT_STATE)
  surfaceState: String                      // contents of .pyro/surface.md (or NO_SURFACE_STATE)
  contractState: String                     // contents of .pyro/contract.md (or NO_CONTRACT_STATE)
  surface_type: String                      // from surface.md frontmatter: gui | cli | api | pipeline | agent
  flows: Array<Flow>                        // parsed from ## Flows section
  ssi: Array<SSITable>                      // parsed from ## Surface State Inventory
  decisions: Array<String>                  // from ## Decisions section
  edge_cases: Array<String>                 // from ## Edge Cases section
  flows_count: Number                       // from surface.md frontmatter
  derivedContracts: Array<Contract>         // derived API contracts
  derivedInvariants: Array<Invariant>       // derived domain invariants
  derivedNFRs: Array<NFR>                   // derived non-functional requirements
  derivedAcceptance: Array<AcceptanceCriteria> // derived acceptance criteria
  hardeningPlan: Array<HardeningItem>       // derived hardening plan
  iterationCount: Number                    // how many review rounds have occurred
  frozen: Boolean                           // whether developer has signaled freeze
  version: Number                           // contract version (1 for first freeze, N+1 for revisions)
  persistable: Boolean                      // whether state.md exists for persistence
}

## Reference Materials

See `reference/` directory for supporting detail:
- [Contract Output Format](reference/contract-output-format.md) -- Full .pyro/contract.md schema, surface-type-specific derivation guidance, and worked example. Load at freeze time when writing contract.md.

## Workflow

contract($ARGUMENTS) {

  // -- 0. PREFLIGHT ---------------------------------------------------------------

  // State check (soft gate -- warn but continue)
  IF projectState == "NO_PROJECT_STATE":
    Warn: "No .pyro/state.md found. Run `/pyro init` to track this project. Continuing anyway."
    SET persistable = false
  ELSE:
    SET persistable = true

  // Surface check (hard gate -- cannot derive contracts without converged surface)
  IF surfaceState == "NO_SURFACE_STATE":
    Output: "No converged surface found. Run `/surface` first to generate and converge a prototype."
    STOP

  // Parse surface.md
  Read .pyro/surface.md
  Extract frontmatter: surface_type, convergence_date, iterations, flows_count
  Extract body sections:
    - ## Flows -> flows array (each flow: name, trigger, expected behavior steps)
    - ## Decisions -> decisions array
    - ## Surface State Inventory -> ssi array (per-flow tables: interaction point, expected behavior, states covered)
    - ## Edge Cases -> edge_cases array

  SET surface_type = frontmatter.surface_type
  SET flows_count = frontmatter.flows_count

  // Existing contract check (revision flow)
  IF contractState != "NO_CONTRACT_STATE":
    Extract version from contract.md frontmatter
    SET version = extracted version

  // Route based on input
  match ($ARGUMENTS) {

    // Empty or new contract derivation
    "" | /^$/ => {
      IF contractState != "NO_CONTRACT_STATE":
        Output: "Contracts already frozen (v{version}). Say **revise** to create v{version + 1}, or **view** to see the current contracts."
        STOP
      ELSE:
        SET version = 1
        derive()
    }

    // Revision signal
    /^revise$/i | /^revise /i => {
      IF contractState == "NO_CONTRACT_STATE":
        Output: "No existing contracts to revise. Deriving fresh contracts from surface.md."
      ELSE:
        SET version = version + 1
        Output: "Revising contracts. Will create v{version} from current surface.md."
      derive()
    }

    // View signal
    /^view$/i => {
      IF contractState != "NO_CONTRACT_STATE":
        Output: display current contract.md contents
      ELSE:
        Output: "No contracts exist yet. Running derivation."
        SET version = 1
        derive()
      STOP
    }

    // Freeze signal
    /^freeze$/i | /looks good/i | /approved/i | /ship it/i => {
      freeze()
    }

    // Everything else is iteration feedback
    _ => {
      iterate($ARGUMENTS)
    }
  }

  // -- 1. DERIVE ------------------------------------------------------------------

  derive() {
    // Derive all four categories from surface.md content
    // Every item must cite its source

    // --- API Contracts ---
    // For each flow's SSI table rows: what operations are implied?
    // Surface type determines contract shape:
    //   gui -> API endpoints (method, path, request body, response shape, error shapes)
    //   cli -> command interfaces (command, flags, args, stdin, stdout, stderr, exit codes)
    //   api -> library interfaces (method signatures, params, return types, exceptions)
    //   pipeline -> event/message contracts (event name, payload, routing, error handling)
    //   agent -> prompt/response contracts (trigger, input schema, output schema, error cases)

    FOR EACH flow IN flows:
      FOR EACH ssi_row IN ssi[flow]:
        Derive API contract from interaction point + expected behavior
        SET contract.derived_from = "Flow {N} -- {flow name}, SSI: {interaction point}"
        APPEND to derivedContracts

    // --- Domain Invariants ---
    // Rules that must hold for surface behavior to remain valid
    // Sources: expected behaviors that imply rules, edge case resolutions, decisions

    FOR EACH flow IN flows:
      FOR EACH expected_behavior_step IN flow.steps:
        IF step implies a rule that must always hold:
          Derive invariant
          SET invariant.derived_from = "Flow {N} -- {flow name}, step {M}"
          APPEND to derivedInvariants

    FOR EACH edge_case IN edge_cases:
      IF edge case resolution implies a rule:
        Derive invariant
        SET invariant.derived_from = "Edge case: {edge case description}"
        APPEND to derivedInvariants

    // --- NFR Targets ---
    // Non-functional requirements implied by the surface experience
    // Only derive NFRs the surface actually implies -- no speculative performance targets

    FOR EACH flow IN flows:
      IF flow behavior implies latency expectations:
        Derive NFR target
        SET nfr.derived_from = "Flow {N} -- {flow name}, {specific behavior}"
      IF flow involves data volume:
        Derive NFR target
      // Only derive NFRs the surface demands -- not "every system needs 99.9% uptime"
      APPEND to derivedNFRs

    // --- Acceptance Criteria ---
    // Each flow's expected behavior steps become testable assertions (Given/When/Then)

    FOR EACH flow IN flows:
      FOR EACH step IN flow.expected_behavior:
        Derive acceptance criterion:
          "Given [precondition from trigger], when [action from step], then [expected outcome]"
        SET criterion.derived_from = "Flow {N} -- {flow name}, step {M}"
      FOR EACH ssi_row IN ssi[flow]:
        IF ssi_row.states_covered includes "in-scope":
          Derive acceptance criterion for that specific state
      APPEND to derivedAcceptance

    // --- Hardening Plan ---
    // What is currently simulated/mocked that needs to become real
    // Derive from what the prototype fakes vs. what the contracts require

    FOR EACH component that is mocked or simulated:
      Add to hardeningPlan:
        component, current_state (mock/placeholder), target_state (real), priority
    APPEND to hardeningPlan

    // --- Present Bundle ---
    SET iterationCount = 0

    Output:
      "Based on the converged **{surface_type}** surface ({flows_count} flows), here are the derived contracts:"
      ""
      "## API Contracts ({derivedContracts.length} contracts)"
      {For each contract: name, interface shape, input, output, error shapes, derived from}
      ""
      "## Domain Invariants ({derivedInvariants.length} invariants)"
      {For each invariant: ID, rule, enforced at, derived from}
      ""
      "## Non-Functional Requirements ({derivedNFRs.length} NFRs)"
      {For each NFR: ID, target, derived from, verification}
      ""
      "## Acceptance Criteria"
      {For each flow: checklist of testable assertions}
      ""
      "## Hardening Plan"
      {Table: component, current state, target state, priority}
      ""
      "Review these contracts. Correct anything wrong, flag anything missing."
      "When satisfied, say **freeze** to lock them into .pyro/contract.md."
  }

  // -- 2. ITERATE -----------------------------------------------------------------

  iterate(feedback) {
    INCREMENT iterationCount

    // Classify developer feedback and adjust derived contracts
    match (feedback) {

      // Add missing item: "add a contract for..." or "missing invariant..."
      /add|missing|also need|forgot/i => {
        Add the specified item to the appropriate category
        Ensure "Derived from:" traces to a surface artifact
        IF no surface artifact supports the addition:
          Output: "I can't find a surface flow or SSI row that supports this. Which flow does it come from?"

        Output:
          "Added: {what was added}. Updated the bundle."
          "Current counts: {contracts} contracts, {invariants} invariants, {nfrs} NFRs."
      }

      // Remove item: "remove contract 3" or "don't need NFR-2"
      /remove|don.?t need|drop|delete/i => {
        Remove the specified item
        Output:
          "Removed: {what was removed}."
          "Current counts: {contracts} contracts, {invariants} invariants, {nfrs} NFRs."
      }

      // Refine item: "change invariant 2 to..." or "NFR-1 should be..."
      /change|refine|update|should be|rephrase/i => {
        Update the specified item
        Output:
          "Updated: {what was changed}."
      }

      // Freeze signal
      /freeze|looks good|approved|ship it/i => {
        freeze()
      }

      // General feedback
      _ => {
        Interpret and apply feedback to the appropriate category
        Output:
          "Applied your feedback. Here's the updated bundle summary:"
          "{contract count} contracts, {invariant count} invariants, {nfr count} NFRs, {acceptance count} acceptance criteria."
          ""
          "Say **freeze** when satisfied, or keep adjusting."
      }
    }
  }

  // -- 3. FREEZE ------------------------------------------------------------------

  freeze() {
    // Load output format reference
    // @reference/contract-output-format.md

    // Count derived items
    SET contracts_count = derivedContracts.length
    SET invariants_count = derivedInvariants.length
    SET nfr_count = derivedNFRs.length

    // Write .pyro/contract.md
    Write .pyro/contract.md:
      ---
      version: {version}
      freeze_date: {today}
      surface_type: {surface_type}
      flows_count: {flows_count}
      contracts_count: {contracts_count}
      invariants_count: {invariants_count}
      nfr_count: {nfr_count}
      ---

      ## API Contracts

      {For each contract:
        ### Contract N: [Operation Name]
        **Endpoint/Interface:** [what is called]
        **Input:** [payload/arguments shape]
        **Output:** [response/return shape]
        **Error shapes:** [error cases and their responses]
        **Derived from:** Flow [N] -- [flow name], SSI: [interaction point]
      }

      ## Domain Invariants

      {For each invariant:
        ### INV-N: [Invariant Name]
        **Rule:** [what must always be true]
        **Enforced at:** [where in the system this is checked]
        **Derived from:** [which flow behavior or edge case requires this]
      }

      ## Non-Functional Requirements

      {For each NFR:
        ### NFR-N: [Requirement Name]
        **Target:** [measurable threshold]
        **Derived from:** [which surface behavior implies this]
        **Verification:** [how to test this]
      }

      ## Acceptance Criteria

      {For each flow:
        ### Flow: [Flow Name]
        - [ ] [Testable assertion from expected behavior step 1]
        - [ ] [Testable assertion from expected behavior step 2]
        - [ ] [Edge case assertion]
      }

      ## Hardening Plan

      ### Simulated Components
      | Component | Current State | Target State | Priority |
      |-----------|--------------|--------------|----------|
      {For each mocked/simulated component}

    // Update state.md
    IF persistable:
      Read .pyro/state.md
      Update frontmatter:
        phase: 3
        last_skill: contract
        last_activity: {today}
      Append to gate_history:
        { gate: "G3", passed: true, notes: "{today} -- Contracts frozen (v{version})" }
      Write .pyro/state.md

    Output:
      "Contracts frozen (v{version}). Wrote `.pyro/contract.md` with:"
      "- {contracts_count} API contracts"
      "- {invariants_count} domain invariants"
      "- {nfr_count} NFR targets"
      "- Acceptance criteria for {flows_count} flows"
      "- Hardening plan for simulated components"
      ""
      "Run `/build` when ready to start implementing vertical slices from these contracts."
  }

}

## Anti-Patterns

These are SFD anti-patterns adapted for contract derivation. Recognize and avoid:

1. **Don't invent contracts.** Every item must trace to surface.md. If you find yourself adding an endpoint, invariant, or NFR that no surface flow requires, you are speculating. Delete it.
2. **Don't use "Derived from: general best practice."** This is the number one signal of gold-plating. If the derivation source is "best practice" instead of a specific flow, SSI row, or edge case, it does not belong.
3. **Don't ask "what contracts do you need?"** Always propose the complete bundle first. The developer corrects faster than they specify.
4. **Don't auto-freeze.** The developer must explicitly signal approval. This is a quality gate, not an automation step.
5. **Don't derive beyond the surface.** Contracts describe what the converged surface demands, not what the final production system might need. YAGNI is enforced by traceability.
6. **Don't confuse contract derivation with system design.** /contract derives specifications from behavior. System design is /build's job.
