---
name: sfd-v2
description: This skill should be used when the user wants to build, prototype, or reshape an app, tool, CLI, API, automation, workflow, requirements document, knowledge tree, policy, curriculum, argument outline, or other evaluable artifact before architecture. Responds to "let's build", "prototype this", "surface first", "SFD", "click dummy", "derive contracts", "docket contracts", "requirements as surface", "knowledge tree", "policy surface", or any request describing what should exist without specifying internals.
---

# Surface-First Development

## Reference

If anything in this skill feels unclear, underspecified, or in tension with a real project situation, stop and read [references/whitepaper-v0.6.md](references/whitepaper-v0.6.md) before improvising. Treat that whitepaper as the authoritative reference for the methodology — EXCEPT for contract derivation and handoff (Phases 4.5–5.5, Gates 1–2): this is the **docket-emitting SFD v2 variant**, and for everything contract-shaped, [references/contract-emission.md](references/contract-emission.md) supersedes the whitepaper's v0.6 wording. The whitepaper describes prose contract derivation; this variant emits machine-admissible contract YAML.

## Triggers

- User says "let's build", "I want an app/tool/CLI/API that...", "I have an idea for..."
- User describes a product, feature, or tool without specifying architecture or internals
- User wants to converge a requirements document, knowledge tree/graph, policy/rule set, curriculum, argument outline, workflow map, or other artifact before implementation
- User says "surface first", "click dummy", "show me what it would look like", "prototype this"
- User says "SFD", "surface-first"
- User wants to start a new project or feature and hasn't locked in a tech approach yet
- User asks "how should this work?" or "what would the UX be?" or "what would the workflow look like?"

## Purpose

You are following the **Surface-First Development** methodology. The core principle: always start by building and iterating the outermost artifact the steering human can evaluate cheaply, converge it with the user, derive contracts, then build inward.

Do NOT start with database schemas, backend architecture, API design, or infrastructure. Start with what the user will actually see, touch, type, read, review, navigate, or sign.

## What Counts as a Surface

The surface is the outermost artifact the steering human can evaluate cheaply. A UI is one instance. So is a requirements document, a knowledge graph, a policy, an argument outline, a curriculum, a workflow map, or a contract clause set. The binding constraints are **concreteness** and **legibility to whoever steers** — not clickability, visualness, or software-ness.

Visual and interactive artifacts are often the cheapest route to legibility, but they are not required. Pick the artifact the actual decision-maker can critique before internals are committed.

## Operating Stance

- Move from concrete artifact to critique, not from abstract discussion to specification.
- Make reasonable product decisions without asking the user to design the system for you.
- Prefer a fast, interactive prototype over a polished explanation of a prototype.
- Treat the user as the evaluator and steering function; your job is to generate proposals they can react to.
- Keep internals provisional until the surface is accepted.

## The Propose-Choose-Proceed Rule

This is the governing interaction pattern for the entire SFD process. Every decision point — from research directions to surface proposals to contract shapes to slice ordering — follows this loop:

1. **Propose** 2-3 concrete directional options. Not vague buckets — each option should be specific enough that the user can picture what choosing it means.
2. **User chooses** one (or more), or discards all with feedback. If discarded, generate a new batch informed by the feedback. Repeat until the user approves a direction.
3. **Proceed** only after explicit user approval.

This prevents the failure mode where you barrel ahead on assumptions and the user has to interrupt to course-correct. It also prevents the opposite failure mode where you ask open-ended questions and the user has to do the design work. The sweet spot: you do the thinking, the user does the steering.

The pattern applies everywhere — Phase 2 research directions, Phase 3 prototype concepts, Phase 4 iteration proposals, Phase 5 contract alternatives, Phase 6 slice ordering, Phase 7 hardening priorities. If you're about to make a significant directional choice, present options first.

**First-response gate:** If the user asks to "prototype", "converge", "use SFD", or "surface-first" but has not already chosen a direction in this conversation, your first response MUST stop at 2-3 concrete directions plus your recommendation and an approval question. Do not self-select one direction. Do not produce a "provisional" full artifact. The word "prototype" is not permission to skip direction choice; it means propose prototype directions first.

## First Move

When this skill is triggered:

1. Identify the primary interaction surface.
2. Explore the problem space (research or generate concept directions).
3. Get user approval on a direction before building anything.
4. Build the smallest believable surface artifact that covers the critical path.
5. Put it in front of the user quickly.
6. Ask for critique of behavior, structure, wording, coverage, flow, or evaluability — not implementation.

Do not begin with architecture diagrams, schema design, backend planning, or large requirement questionnaires unless the user explicitly forces that order. For document, tree, policy, or curriculum surfaces, do **not** draft the full artifact as the first move; propose 2-3 concrete artifact directions and wait for approval first.

## Expected Artifact by Surface Type

| Surface | First artifact |
|---|---|
| GUI app | Click dummy or runnable mock UI |
| CLI tool | Executable prototype or realistic terminal session |
| API / library | Example consumer code that shows the desired developer experience |
| Data / ops workflow | Simulated runbook, monitoring view, or operator journey |
| Agent / automation | Trigger-to-outcome walkthrough with realistic state transitions |
| Requirements / spec surface | Candidate requirements shape plus acceptance-criteria pattern |
| Knowledge base / graph | Tree or graph structure with example nodes and coverage map |
| Policy / rule set | Rule-set shape with exceptions, examples, and conflict checks |
| Argument / essay | Outline or claims map with counterarguments and evidence gaps |
| Curriculum / training | Module map with exercises, evaluation gates, and coverage gaps |

If you are only describing the artifact instead of producing it, you are probably not following SFD yet.

## Why This Works

Humans are better at evaluating concrete proposals than writing abstract specs. Your job is to generate proposals fast so the human can react, critique, and steer. The human directs; you generate. Never ask the user to write a specification. Show them something and let them tell you what's wrong with it.

The surface must be legible to the decision-maker. A compliance lead can critique a policy; a knowledge-base maintainer can critique a tree; a developer can critique consumer code; an end user can critique a UI. Choose the evaluable artifact for the steerer in front of you.

---

## The Process

### Phase 1: Identify the Surface

Determine the outermost evaluable artifact for the domain: the thing the steering human confronts and reacts to before internals are committed. Ask the user ONLY if the steering artifact or decision-maker is genuinely ambiguous.

Software surfaces:

| If the user wants... | The surface is... | You build... |
|---|---|---|
| A web/mobile app | GUI | Click dummy (HTML/React, functional navigation, mock data) |
| A CLI tool | Terminal session | Executable prototype OR scripted session transcript |
| An API or library | Developer experience | Example consumer/integration code |
| A data pipeline | Operator workflow | Simulated deploy/monitor/debug session |
| An automation/agent | Trigger-to-outcome flow | Scenario walkthrough |

Knowledge/document surfaces:

| If the user wants... | The surface is... | You build... |
|---|---|---|
| Requirements convergence | Requirements doc + acceptance criteria | 2-3 document shapes, then a draft artifact after approval |
| Knowledge base | Tree/graph structure + coverage gaps | 2-3 taxonomy/graph directions with example nodes |
| Policy/regulation | Rule set + exceptions/examples | 2-3 policy shapes with conflict/exception coverage |
| Argument/essay | Claim ordering + evidence/counterargument map | 2-3 outline structures |
| Curriculum/training | Module sequence + exercises/eval gates | 2-3 curriculum maps with coverage axes |

### Phase 2: Explore the Problem Space

Before building anything, understand the landscape. The goal is to arrive at an informed concept direction that both you and the user believe in — not to produce a research paper, but to avoid building a prototype grounded in ignorance.

**The "Already Exists" Check — do this throughout Phase 2, not as a separate step:**

Your job during discovery is to map what exists so the user can make informed decisions about where to spend their building energy. Two things to watch for:

- **If the user's idea already exists** (or something very close), say so immediately. Don't wait for the user to ask "isn't this already a thing?" — surfacing that is YOUR job. Name the existing tool, explain what it does, and then focus on the interesting part: what does the user's vision do that the existing tool doesn't? Those differences are where the real project lives. The user may know the tool exists and want to build anyway (for control, philosophy, learning, or because the existing tool is bad) — that's their call. Your job is to make sure they have the information, not to talk them out of building.
- **If parts of the idea are solved by existing libraries, frameworks, or protocols**, surface them as building blocks. The user's building energy should go toward the unique value, not toward re-solving solved problems. "We should use X for rendering and build the feedback layer on top" is almost always a better direction than "let's build a renderer from scratch." Frame concept directions around what to USE (commodity) and what to BUILD (the differentiator).

This isn't a one-time gate — it applies at every decision point throughout the process. If mid-conversation you realize a library handles something you were about to propose building, say so. The user should never have to be the one pointing out "doesn't X already do this?"

**Step 1: Propose research directions**

Present 2-3 research directions as concrete options. Each direction should focus on a different angle of the problem space — e.g., existing tools and their gaps, technical approaches, target user segments, or prior art in adjacent domains. Format as a numbered list the user can pick from:

> Here are a few angles I can research before we prototype:
> 1. **[Direction A]** — [what you'd look into and why it matters]
> 2. **[Direction B]** — [what you'd look into and why it matters]
> 3. **[Direction C]** — [what you'd look into and why it matters]
>
> Pick one or more, or tell me to skip research / try different directions.

If the user discards all directions, ask what's off and generate a new batch. If the user says "skip research" or the topic clearly doesn't need it (they already know the space, or it's a personal tool with no competitive landscape), move to Step 3 directly.

**Step 2: Research and present findings**

Use available research skills (web search, documentation lookup, etc.) to investigate the chosen direction(s). Keep research focused — you're building context for a prototype, not writing a thesis.

Present findings as a concise summary, structured as:
1. **What already exists** — name specific tools, libraries, and projects. If something IS the user's idea (or 80%+ of it), flag it prominently: "This already exists — it's called X. Here's what it does and where it differs from your vision."
2. **What's commodity** — libraries, frameworks, and protocols that solve parts of the problem. Recommend using them: "We should use X for this part rather than building our own."
3. **What's the actual gap** — the part that doesn't exist yet. This is where the user's project has value.

This structure prevents the failure mode where you present a landscape survey and then propose building something the survey just showed already exists. The gap analysis IS the research output — everything else is context.

**Step 3: Propose concept directions**

Based on research (or your own knowledge if research was skipped), propose 2-3 concept directions for the prototype. Each should be a distinct take on how to solve the user's problem — different enough that choosing one meaningfully shapes what the prototype looks like.

Each direction should clearly state what you'd **use** (existing tools/libraries) vs what you'd **build** (the unique value). If a direction is mostly "use existing tool X," that's a valid direction — and often the best one.

> Based on what I found, here are three directions we could take:
> 1. **[Concept A]** — [what the tool would feel like, key differentiator]. Uses: [existing tools]. Builds: [new parts].
> 2. **[Concept B]** — [what the tool would feel like, key differentiator]. Uses: [existing tools]. Builds: [new parts].
> 3. **[Concept C]** — [what the tool would feel like, key differentiator]. Uses: [existing tools]. Builds: [new parts].
>
> Which resonates? Or should I think in a different direction?

If the user discards all concepts, ask what's missing and generate a new batch. If the user wants more research first, loop back to Step 1.

**Step 4: Lock direction**

Once the user picks a concept direction, confirm it explicitly:

> "Locked in: [chosen direction]. Building the first prototype around this."

Only now proceed to Phase 3.

### Phase 3: Generate Surface Proposal

Build a working prototype/proposal of the surface immediately after the user approves a direction. Rules:

1. **Go fast, not deep.** Use mock data, placeholder logic, simulated responses, draft structure, candidate rules, or example nodes. The surface must be real enough to critique, but nothing behind it needs to work yet.
2. **Make decisions.** Don't ask the user to specify layout, colors, flow structure, field names, taxonomy boundaries, policy wording, module names, or copy. Make opinionated choices. The user will correct what's wrong — that's faster than asking upfront.
3. **Cover the critical path.** Build the 2-3 most important user flows end to end. Don't build every screen or every edge case yet.
4. **Show, don't describe.** Never respond only with a description of what the prototype would look like. Build the critiqueable artifact: clickable mock, terminal transcript, consumer code, requirements draft, tree, rule set, outline, or curriculum map.

After generating, tell the user:

> "Here's a first prototype of [what it is]. Walk through it and tell me what feels wrong, what's missing, and what should work differently. Don't worry about internals — we'll handle those after we nail the surface."

**Good enough for round one:** believable, navigable, and critiqueable. Not production-ready, not deeply wired, not exhaustive.

### Phase 4: Iterate to Convergence

The user will critique the prototype. Your job:

1. **Listen for surface critique.** "This should do X when I click Y," "this rule is too broad," "this category is wrong," "this module order teaches the wrong thing." Act on it.
2. **Ignore implementation preferences** unless the user insists. If they say "use Redux" or "make this a microservice," gently redirect: "Let's nail the behavior first, then I'll pick the best implementation approach."
3. **Probe edge cases yourself.** After addressing the user's feedback, proactively show: "By the way, here's what happens when [edge case]. Does this feel right?"
4. **Track decisions.** Maintain a running log of what was changed and why, including alternatives that were tried and rejected.
5. **Log clauses at birth.** Every accepted behavioral expectation IS a contract clause in larval form. The moment the user accepts a behavior (or rejects an alternative), append an entry to `.sfd/clause-log.md` — do NOT wait for Phase 5 and try to remember. Entry format:

```markdown
- [C-007] Tips MUST be rounded to the nearest $0.10, ties up.
  born: iteration round 1, in response to "tips should be rounded to the nearest 10 cents"
  state-cells: calculate × happy-path
```

   `C-NNN` ids are per-project monotonic and survive into the contract file unchanged. Rejected alternatives get logged too, phrased as MUST NOT (e.g. "the tool MUST NOT read stdin"), with `born:` pointing at the rejection. Retrospective derivation is the biggest quality loss in this pipeline — the clause log is how the variant avoids it.

**Convergence check:** After each iteration round, ask:

> "Walk through the [key flows]. Is there anything that still feels wrong or missing?"

When the user says something like "this feels right," "let's build it," "I'm happy with this," or "ship it" — convergence is reached. State this explicitly:

> "Surface converged. Moving to contract derivation."

### Phase 4.5: Surface State Inventory (Gate 1 prerequisite)

Timing: after the user's freeze signal ("this feels right"), before declaring Gate 1 passed. Classify every observable state of every surface unit as **in-scope** (demonstrated and accepted), **deferred** (acknowledged, not blocking), or **n/a**. For software surfaces, the default ten states are: empty/zero-data, loading/in-progress, success, validation failure, system failure, partial failure, permission denied, conflict, rate limit/retry, offline/degraded. For document/knowledge/policy surfaces, define a domain-appropriate inventory axis instead (for example: complete, ambiguous, conflicted, exception-covered, traceable, orphaned, unsupported, overbroad, under-specified, stale). Write it to `.sfd/surface-state-inventory.md`. A prototype that only shows the happy path has not converged — it has demonstrated one path through a larger state space.

### Phase 5: Compile Contracts (from the Clause Log, not from memory)

The contracts are THE PRODUCT of this methodology — the prototype was the interview instrument. Phase 5 is compile-and-dedup, not recall:

1. **Compile:** walk `.sfd/clause-log.md`; merge duplicates; sharpen wording. Walk the decision log's rejected alternatives — strong rejections become MUST NOT clauses (the user paid to reject them once; they must never need re-rejecting).
2. **Cover:** every in-scope cell of the Surface State Inventory maps to ≥1 clause, and every clause cites its cells in `anchors`. Uncovered in-scope cells are bugs in the compilation; fix or reclassify.
3. **Make checkable at birth:** every clause gets exactly one RFC-2119 keyword (MUST or MUST NOT — never SHOULD: decide or defer) and a typed `acceptance:` — `test:` ref, `metric:` + `threshold:`, `command:` + `expect:`, or `verdict: human` (legal, but explicit). A clause you cannot give an acceptance procedure is not a contract — demote it to the open-questions list. Qualitative performance words ("fast", "reliable") get numbers or get demoted.
4. **Emit:** write `.contracts/<project>.contract.yaml` exactly per the schema in [references/contract-emission.md](references/contract-emission.md) — top-level `contract`/`rev`/`source`/`signed`, clauses with `id`/`obligation`/`acceptance`/`anchors` (optional `risk`/`evidence_required`/`scope`). Clause ids come from the clause log unchanged.
5. **Confirm via options, not open questions:** for each genuinely contested clause (strict vs loose invariant, tight vs generous threshold), present 2-3 options with your recommendation — the Propose-Choose-Proceed rule applies to contracts too. Never ask "does this capture everything?"; the inventory coverage check answers that structurally.

### Phase 5.5: Self-Admission and Round-Trip (Gate 2 prerequisites)

**Self-admission (the Accord):** walk the door checks A1–A9 over your own drafted YAML, as if you were the ledger refusing your work — the full checklist with refuse/flag semantics is in [references/contract-emission.md](references/contract-emission.md). Fix every refusal at the source; record flags honestly. A handoff bundle whose contract file would be refused at a docket door is not done.

**Round-trip test:** contracts are sufficient iff a blind agent can rebuild the surface from them. Hand the contract YAML + state inventory ONLY (not the prototype, not the conversation) to a fresh-context subagent; have it reconstruct the surface at wireframe/session-transcript fidelity; diff against the converged prototype. Divergence = a contract leak → tighten or add a clause. Max 2 rounds; remaining cosmetic-only diffs are accepted and noted. Write `.sfd/round-trip-report.md`. (No subagent tooling available? Do a documented self-blind reconstruction — write the rebuild from the YAML alone before re-opening the prototype — and mark the report `mode: self-blind`.)

### Phase 6: Build Inward (Vertical Slices)

Now build the internals. Rules:

1. **One slice at a time.** Each slice makes one surface flow real, end to end — from user interaction through logic to persistence and back.
2. **Start with the highest-value flow.** Ask the user which flow matters most if not obvious.
3. **Keep the surface working.** At every point, the prototype should still be interactive. Flows that aren't yet backed by real implementation continue to use mocks. The user should always be able to click through everything.
4. **Write acceptance tests anchored to converged behavior.** Before or during implementation, encode the converged surface flows as automated tests.

When in doubt about slice order, implement the slice that makes the most important user-visible flow real first.

### Phase 7: Progressive Hardening

Replace simulated components with real implementations in this general order:

1. Mock data -> real persistence
2. Placeholder auth -> real identity
3. Simulated behavior -> domain logic
4. Happy-path only -> error handling, validation, loading states
5. Baseline perf -> optimization

After each hardening step, verify the surface still behaves as converged.

---

## Canonical Artifact Paths (no improvising)

Every SFD project uses exactly these paths — the Handoff Bundle depends on them:

- `.sfd/intent.md` — intent document (Phase 1: problem statement, target users, constraints, non-negotiables, known unknowns)
- `.sfd/decision-log.md` — decision log (Phase 4)
- `.sfd/clause-log.md` — clause log (Phase 4, rule 5)
- `.sfd/surface-state-inventory.md` — state inventory (Phase 4.5)
- `.sfd/round-trip-report.md` — round-trip report (Phase 5.5)
- `.contracts/<project>.contract.yaml` — THE contract file (Phase 5)
- `prototype/` — the converged surface prototype (form varies by surface type)

## Decision Log Format

Maintain this throughout the project. It survives sessions and prevents re-litigating settled decisions.

```markdown
## SFD Decision Log

### Surface Type
[GUI / CLI / API / Pipeline / Agent / Requirements / Knowledge Tree / Policy / Argument / Curriculum / Other]

### Convergence Status
[Iterating / Converged on YYYY-MM-DD / Re-opened for feature X]

### Decisions
- [Date] [What was decided] — [Why, and what alternatives were rejected]
- [Date] ...

### Derived Contracts
- [Endpoint/interface]: [shape]
- ...

### Hardening Status
- [ ] Persistence (currently: mock data)
- [ ] Auth (currently: placeholder)
- [ ] Domain logic (currently: simulated)
- [ ] Error handling (currently: happy-path)
- [ ] Performance (currently: unoptimized)
```

---

## Gate Checklist

Use these gates to track progress. Don't skip gates.

### Gate 1: Surface Converged
- [ ] Critical flows demonstrated and accepted by user
- [ ] Edge cases explored interactively
- [ ] Surface State Inventory complete — every unit × state classified in-scope / deferred / n/a
- [ ] Decision log captures key choices and rejected alternatives
- [ ] Clause log current — every accepted behavior has a C-NNN entry
- [ ] Open UX questions logged (if any)

### Gate 2: Contracts Frozen (= Handoff Bundle complete)
- [ ] `.contracts/<project>.contract.yaml` emitted per schema; every clause: one MUST/MUST NOT, typed acceptance, ≥1 anchor citing inventory cells or decisions
- [ ] Every in-scope inventory cell maps to ≥1 clause
- [ ] NFRs carry numbers (or live in open questions, not in the contract)
- [ ] Self-admission walk (A1–A9) clean — refusals fixed, flags recorded
- [ ] Round-trip report filed; remaining diffs cosmetic-only
- [ ] Contested clauses confirmed via options (Propose-Choose-Proceed)
- [ ] Handoff Bundle complete: intent, prototype, decision log, clause log, state inventory, contract YAML, round-trip report
- [ ] User signed the rev (`signed:` entry in the contract file)

### Gate 3: Architecture Review
- [ ] Tech stack confirmed
- [ ] Hot paths and scaling risks identified
- [ ] Hardening order established
- [ ] Security considerations reviewed

### Gate 4: Hardening Complete
- [ ] All mock/simulated components replaced
- [ ] Acceptance tests passing against real implementation
- [ ] Error handling and validation in place
- [ ] Observability configured

### Gate 5: Release Ready
- [ ] Regression suite passing
- [ ] Rollback plan documented
- [ ] Monitoring on surface-critical paths

---

## Anti-Patterns (Don't Do This)

1. **Don't ask for a spec before building.** "Can you write requirements first?" — No. Build a surface prototype and iterate. The spec is derived, not authored.
2. **Don't start with the database schema.** The schema serves the surface, not the other way around.
3. **Don't build backend before the surface is converged.** You will build the wrong backend.
4. **Don't throw away the prototype.** Harden it. If a full rewrite is truly needed, the converged surface is still the behavioral reference.
5. **Don't gold-plate the prototype.** Fast and opinionated beats slow and polished. The user will fix what's wrong.
6. **Don't ask open-ended questions.** Present options, don't ask the user to design. "Which of these three directions?" is good. "What do you want it to look like?" is bad. The user steers; you generate.
7. **Don't build a second spec reality.** The contract file plus the decision log ARE the spec. Never produce a parallel prose-requirements document that restates the contracts — abstract documents drift and quietly outrank the artifact people actually validated. If something can't live in a clause, it belongs in the decision log (why) or open questions (undecided) — nowhere else.
8. **Don't generalize surface into vacuity.** "Anything can be a surface" is false. The artifact must be concrete, legible to the steering human, produced before internals harden, and converged through critique before contracts are derived.

---

## When NOT to Use SFD

Recognize when SFD is not the right primary approach and tell the user:

- There is no human in the steering loop who can evaluate a concrete artifact before implementation.
- The core challenge is algorithmic, mathematical, or protocol-level and the surface is trivial.
- Regulatory requirements demand formal specs before implementation.
- The user explicitly asks for a different approach.

In these cases, say:

> "This project's complexity is mostly below the surface layer. I'd suggest we [appropriate alternative] for the core, and use surface-first only for the interaction layer on top."

---

## Export (after Gate 2)

The Handoff Bundle is the deliverable; everything downstream consumes it generically:

```
SFD Phase 1-5.5 (discover + converge + compile + admit)
    |
    v
Gate 2 --> Handoff Bundle (.sfd/* + .contracts/<project>.contract.yaml)
    |
    v
contract ledger (e.g. docket import) -> derived tasks -> evidence bundles
    |
    v
SFD Phase 6-7, or any other fulfillment process -- the bundle doesn't care
```

Do not build integration code for any specific consumer. The contract file is a boundary artifact: ledgers import it, loop runners use clauses as stop conditions, task systems derive work from obligation-minus-evidence. Tool-specific exports (OpenSpec, Beads, ...) are legal as *additional* views but must never become the primary spec — see Anti-Pattern 7.

---

## Session Start Protocol

When resuming work on an SFD project:

1. Check `.sfd/decision-log.md` first. If it exists, read it. If not, search for an existing SFD decision log and standardize on `.sfd/decision-log.md`.
2. Determine current gate status.
3. Report to user: "We're at [Gate N]. Last session we [summary]. Next step is [what]."
4. If no log found but project artifacts exist, reconstruct state from code and ask user to confirm.

## Execution Heuristic

Use this mental loop throughout the session:

1. What is the surface artifact, and who is the steering evaluator?
2. Do I understand the problem space well enough to prototype? (If not → Phase 2)
3. Am I about to make a directional choice? (If yes → Propose-Choose-Proceed)
4. What is the smallest artifact that makes it real enough to critique?
5. What did the user react to?
6. What clause does that reaction imply? Log it NOW (`.sfd/clause-log.md`).
7. Would this clause pass the Accord (typed acceptance? anchor? one MUST?)
8. What is the next thin slice inward?

## End of Session Protocol

Before ending a session:

1. Update the decision log with any new decisions.
2. Update gate checklist with current status.
3. Update hardening status.
4. Commit state files only if the user asks for a commit or the repo workflow requires it.
5. Report summary: what was accomplished, what gate you're at, what comes next.
